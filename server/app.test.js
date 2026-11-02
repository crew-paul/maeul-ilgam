import {test,before,after} from 'node:test';
import assert from 'node:assert/strict';
import {randomUUID} from 'node:crypto';
import {openDatabase} from './db.js';
import {createApp,validWav} from './app.js';
process.env.AUTH_MODE='development';process.env.NODE_ENV='test';
let db,server,base,owner,worker,job,interestId;
const details={task:'Photograph strawberries',location:'Gimje',date:'2099-11-08',startTime:'09:00',endTime:'12:00',payAmount:'50000',payUnit:'total',headcount:'1',currency:'KRW'};
async function request(endpoint,{method='GET',body,cookie}={}){const r=await fetch(base+endpoint,{method,headers:{'X-Requested-With':'maeul',...(body?{'Content-Type':'application/json'}:{}),...(cookie?{Cookie:cookie}:{})},body:body?JSON.stringify(body):undefined});return {status:r.status,data:await r.json(),cookie:r.headers.get('set-cookie')?.split(';')[0]};}
async function login(value){const sent=await request('/api/auth/code',{method:'POST',body:{channel:'email',value}});assert.equal(sent.status,200);const verified=await request('/api/auth/verify',{method:'POST',body:{challengeId:sent.data.challengeId,code:sent.data.developmentCode}});assert.equal(verified.status,200);return verified.cookie;}
before(async()=>{db=await openDatabase();server=createApp(db).listen(0,'127.0.0.1');await new Promise(resolve=>server.once('listening',resolve));base=`http://127.0.0.1:${server.address().port}`;owner=await login('farmer@example.com');worker=await login('worker@example.com');});
after(async()=>{await new Promise(resolve=>server.close(resolve));await db.close();});
test('owner can save drafts; public and other account cannot read or change them',async()=>{let r=await request('/api/jobs',{method:'POST',body:{data:details,clientId:randomUUID()},cookie:owner});assert.equal(r.status,201);job=r.data.job;assert.equal((await request(`/api/jobs/${job.id}`)).status,404);assert.equal((await request(`/api/jobs/${job.id}`,{method:'PATCH',cookie:worker,body:{data:details,version:job.version}})).status,404);});
test('missing pay cannot be published; stale changes cannot overwrite saved work',async()=>{const r=await request('/api/jobs',{method:'POST',cookie:owner,body:{clientId:randomUUID(),data:{...details,payAmount:''}}});assert.equal((await request(`/api/jobs/${r.data.job.id}/publish`,{method:'POST',cookie:owner,body:{version:1}})).status,422);assert.equal((await request(`/api/jobs/${job.id}`,{method:'PATCH',cookie:owner,body:{data:details,version:99}})).status,409);});
test('publication is visible to independent users and is region searchable',async()=>{const r=await request(`/api/jobs/${job.id}/publish`,{method:'POST',cookie:owner,body:{version:job.version}});assert.equal(r.status,200);job=r.data.job;assert.equal((await request('/api/jobs?region=Gimje')).data.items.length,1);assert.equal((await request('/api/jobs?region=unknown')).data.items.length,0);assert.equal((await request(`/api/jobs/${job.id}`,{cookie:worker})).data.isOwner,false);});
test('interest consent, owner-only contacts, idempotent repeat and withdrawal',async()=>{const input={name:'Participant',memo:'Available',contactType:'phone',contactValue:'010-1234-5678',consent:true};assert.equal((await request(`/api/jobs/${job.id}/interests`,{method:'POST',cookie:worker,body:{...input,consent:false}})).status,422);for(let i=0;i<2;i++)assert.equal((await request(`/api/jobs/${job.id}/interests`,{method:'POST',cookie:worker,body:input})).status,201);assert.equal((await request(`/api/jobs/${job.id}/interests`,{cookie:worker})).status,404);const contacts=(await request(`/api/jobs/${job.id}/interests`,{cookie:owner})).data.items;assert.equal(contacts.length,1);assert.equal(contacts[0].contactValue,'+821012345678');interestId=(await request('/api/me/interests',{cookie:worker})).data.items[0].id;assert.equal((await request(`/api/interests/${interestId}/withdraw`,{method:'POST',cookie:owner,body:{}})).status,404);assert.equal((await request(`/api/interests/${interestId}/withdraw`,{method:'POST',cookie:worker,body:{}})).status,200);assert.equal((await request(`/api/jobs/${job.id}/interests`,{cookie:owner})).data.items.length,0);});
test('closed jobs reject new interest, logout revokes session',async()=>{assert.equal((await request(`/api/jobs/${job.id}/close`,{method:'POST',cookie:owner,body:{version:job.version}})).status,200);assert.equal((await request(`/api/jobs/${job.id}/interests`,{method:'POST',cookie:worker,body:{name:'Worker',contactType:'email',contactValue:'worker@example.com',consent:true}})).status,409);await request('/api/auth/logout',{method:'POST',cookie:worker,body:{}});assert.deepEqual((await request('/api/me/jobs',{cookie:worker})).data.items,[]);});
test('separate memory databases begin empty; malformed audio is rejected',async()=>{const fresh=await openDatabase();assert.equal((await fresh.query('SELECT count(*)::int AS n FROM jobs')).rows[0].n,0);await fresh.close();assert.equal(validWav(Buffer.from('not a recording')),false);});

test('working drafts survive refresh and sign-in without leaking to another browser',async()=>{
 const working={data:{...details,payUnit:''},request:'A request in progress',phase:'questions',jobId:null,version:null};
 const saved=await request('/api/working-draft',{method:'PUT',body:working});assert.equal(saved.status,200);assert.match(saved.cookie,/^working=/);
 assert.deepEqual((await request('/api/working-draft',{cookie:saved.cookie})).data.draft,working);
 assert.equal((await request('/api/working-draft',{cookie:owner})).data.draft,null);
 assert.deepEqual((await request('/api/working-draft',{cookie:`${saved.cookie}; ${owner}`})).data.draft,working);
 await request('/api/working-draft',{method:'DELETE',cookie:saved.cookie});assert.equal((await request('/api/working-draft',{cookie:saved.cookie})).data.draft,null);
});
test('old work is hidden from discovery and missing pay basis blocks publication',async()=>{
 const expired=randomUUID();const ownerId=(await db.query('SELECT id FROM users WHERE identity=$1',['farmer@example.com'])).rows[0].id;
 await db.query("INSERT INTO jobs(id,owner_id,status,data) VALUES($1,$2,'published',$3)",[expired,ownerId,JSON.stringify({...details,date:'2020-01-01'})]);
 assert.ok(!(await request('/api/jobs')).data.items.some(j=>j.id===expired));
 const draft=(await request('/api/jobs',{method:'POST',cookie:owner,body:{clientId:randomUUID(),data:{...details,payUnit:''}}})).data.job;
 const r=await request(`/api/jobs/${draft.id}/publish`,{method:'POST',cookie:owner,body:{version:draft.version}});assert.equal(r.status,422);assert.ok(r.data.error.fields.includes('payUnit'));
});
test('verification rejects wrong or reused codes and unsafe cross-origin writes',async()=>{
 const sent=await request('/api/auth/code',{method:'POST',body:{channel:'email',value:'auth-check@example.com'}});
 const code=sent.data.developmentCode;const body={challengeId:sent.data.challengeId,code:code==='111111'?'222222':'111111'};
 assert.equal((await request('/api/auth/verify',{method:'POST',body})).status,422);
 body.code=code;assert.equal((await request('/api/auth/verify',{method:'POST',body})).status,200);
 assert.equal((await request('/api/auth/verify',{method:'POST',body})).status,422);
 const cross=await fetch(base+'/api/jobs',{method:'POST',headers:{Origin:'https://other.example','Content-Type':'application/json','X-Requested-With':'maeul',Cookie:owner},body:JSON.stringify({clientId:randomUUID(),data:details})});assert.equal(cross.status,403);
});

test('guest can post and read without signing in; browser ownership protects changes and contacts',async()=>{
 const saved=await request('/api/jobs',{method:'POST',body:{clientId:randomUUID(),data:details}});assert.equal(saved.status,201);const guest=saved.cookie;assert.match(guest,/^posting_owner=/);let own=saved.data.job;
 assert.equal((await request('/api/me',{cookie:guest})).data.user,null);
 assert.equal((await request(`/api/jobs/${own.id}`,{cookie:guest})).data.isOwner,true);
 assert.equal((await request(`/api/jobs/${own.id}`)).status,404);
 assert.equal((await request(`/api/jobs/${own.id}`,{cookie:owner})).status,404);
 const posted=await request(`/api/jobs/${own.id}/publish`,{method:'POST',cookie:guest,body:{version:own.version}});assert.equal(posted.status,200);own=posted.data.job;
 const publicView=await request(`/api/jobs/${own.id}`);assert.equal(publicView.status,200);assert.equal(publicView.data.isOwner,false);assert.equal((await db.query('SELECT count(*)::int AS n FROM interests WHERE job_id=$1',[own.id])).rows[0].n,0);assert.equal((await request(`/api/jobs/${own.id}/interests`,{method:'POST',cookie:guest,body:{name:'Guest',contactType:'email',contactValue:'guest@example.com',consent:true}})).status,401);
 assert.equal((await request('/api/me/jobs',{cookie:guest})).data.items[0].id,own.id);
 assert.equal((await request(`/api/jobs/${own.id}`,{method:'PATCH',body:{data:details,version:own.version}})).status,404);
 assert.equal((await request(`/api/jobs/${own.id}/interests`)).status,404);
 assert.equal((await request(`/api/jobs/${own.id}/interests`,{cookie:owner})).status,404);
 assert.equal((await request(`/api/jobs/${own.id}/interests`,{cookie:guest})).status,200);
 const changed=await request(`/api/jobs/${own.id}`,{method:'PATCH',cookie:guest,body:{data:{...details,task:'Guest edit'},version:own.version}});assert.equal(changed.status,200);own=changed.data.job;
 assert.equal((await request(`/api/jobs/${own.id}/close`,{method:'POST',cookie:owner,body:{version:own.version}})).status,404);
 assert.equal((await request(`/api/jobs/${own.id}/close`,{method:'POST',cookie:guest,body:{version:own.version}})).status,200);
});
