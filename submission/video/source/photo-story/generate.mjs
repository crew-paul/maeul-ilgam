import 'dotenv/config';
import fs from 'node:fs/promises';
import path from 'node:path';
const out=path.resolve('submission/video/raw/photo-story');
await fs.mkdir(out,{recursive:true});
const scenes=JSON.parse(await fs.readFile(new URL('./photos.json',import.meta.url),'utf8'));
const key=process.env.META_API_KEY||process.env.MODEL_API_KEY;
if(!key)throw new Error('Meta API key missing');
// Exactly eight requests at $0.01/image; existing files are reused. No automatic retries.
const common='Use case: photorealistic-natural. Documentary-style fictional photo story in Gimje, rural South Korea. Natural daylight, ordinary contemporary Korean countryside, understated warm colors, realistic skin texture, candid 35mm film photography, landscape 16:9. Respectful everyday life, not melodramatic or a glamorous advertisement. No text, no subtitles, no logos, no watermarks. All depicted people are fictional adults. One coherent film: elderly Korean woman farmer around 73, short softly curled gray hair, muted plum cardigan over cream blouse, moss-green work apron; young Korean adult man around 27, short black hair, clean shaven, oatmeal overshirt over white T-shirt, dark trousers. Keep these identities and outfits consistent across scenes.';
let ledger=JSON.parse(await fs.readFile(path.join(out,'generation-ledger.json'),'utf8').catch(()=>'[]'));
for(const s of scenes){
 const file=path.join(out,s.file);
 try{await fs.access(file);console.log('reuse',s.id);continue;}catch{}
 const content=[{type:'input_text',text:common+'\nShot: '+s.prompt}];
 for(const ref of s.references||[]){
  const data=await fs.readFile(path.join(out,ref));
  content.push({type:'input_text',text:'Character continuity reference only; create the new shot described above. Keep the face and clothing of the matching character.'},{type:'input_image',image_url:'data:image/png;base64,'+data.toString('base64')});
 }
 const body={model:'muse-image-1.0',input:[{role:'user',content}],tools:[{type:'image_generation',size:'1536x1024',output_format:'png',enable_image_search:false,enable_web_search:false,enable_shell:false}],store:false};
 const res=await fetch('https://api.meta.ai/v1/responses',{method:'POST',headers:{Authorization:`Bearer ${key}`,'Content-Type':'application/json'},body:JSON.stringify(body),signal:AbortSignal.timeout(240000)});
 if(!res.ok){const e=await res.json().catch(()=>({}));throw new Error('Meta image request failed '+s.id+' HTTP '+res.status+' '+String(e.error?.message||'').slice(0,500).replaceAll(key,'[REDACTED]'));}
 const json=await res.json();
 const items=json.output?.filter(o=>o.type==='image_generation_call'&&o.result)||[];
 if(items.length!==1)throw new Error('Expected one image for '+s.id);
 await fs.writeFile(file,Buffer.from(items[0].result,'base64'));
 ledger.push({id:s.id,model:json.model||body.model,responseId:json.id,images:1,publishedPriceUsd:.01});
 await fs.writeFile(path.join(out,'generation-ledger.json'),JSON.stringify(ledger,null,2)+'\n');
 console.log('generated',s.id);
}
