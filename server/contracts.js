import {z} from 'zod';
export const fieldKeys=['task','location','date','startTime','endTime','payAmount','payUnit','headcount'];
export const draftSchema=z.object({task:z.string().max(1500).default(''),location:z.string().max(120).default(''),date:z.string().max(10).default(''),startTime:z.string().max(5).default(''),endTime:z.string().max(5).default(''),payAmount:z.string().max(12).default(''),payUnit:z.enum(['hour','day','total','']).default(''),headcount:z.string().max(3).default(''),currency:z.enum(['KRW','USD']).default('KRW')}).strict();
export const emptyDraft=()=>draftSchema.parse({});
export function validTime(s){return /^([01]\d|2[0-3]):[0-5]\d$/.test(s)}
export function missingFields(data){const d=draftSchema.parse(data);return fieldKeys.filter(k=>{
 if(k==='date'){return !/^\d{4}-\d{2}-\d{2}$/.test(d.date)||isNaN(Date.parse(d.date))||new Date(`${d.date}T00:00:00Z`).toISOString().slice(0,10)!==d.date;}
 if(k==='startTime'||k==='endTime')return !validTime(d[k]);
 if(k==='payAmount')return !/^\d+$/.test(d[k])||Number(d[k])<=0||Number(d[k])>100000000;
 if(k==='headcount')return !/^\d+$/.test(d[k])||Number(d[k])<1||Number(d[k])>100;
 return !d[k].trim();
 });}
export function publicationErrors(d){const missing=missingFields(d);if(missing.length)return missing;if(d.endTime<=d.startTime)return ['endTime'];const now=new Date();const today=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Seoul',year:'numeric',month:'2-digit',day:'2-digit'}).format(now);if(d.date<today)return ['date'];if(new Date(`${d.date}T${d.startTime}:00+09:00`).getTime()<=Date.now())return ['startTime'];if(containsContact(d.task)||containsContact(d.location))return ['privateContact'];return [];}
export function normalizeContact(type,value){if(typeof value!=='string')return null;const s=value.trim();if(type==='email')return z.string().email().max(254).safeParse(s).success?s.toLowerCase():null;if(type!=='phone')return null;let digits=s.replace(/[\s().-]/g,'');if(/^01\d{8,9}$/.test(digits))digits='+82'+digits.slice(1);return /^\+[1-9]\d{7,14}$/.test(digits)?digits:null;}
export function containsContact(text){return /[\w.+-]+@[\w.-]+\.[a-z]{2,}|(?:\+?\d[\s().-]*){9,}/i.test(text);}
export const redactContacts=text=>text.replace(/[\w.+-]+@[\w.-]+\.[a-z]{2,}/gi,'[contact removed]').replace(/(?:\+?\d[\s().-]*){9,}/g,'[contact removed]');
export function publicJob(row){return {id:row.id,status:row.status,data:row.data,isDemo:row.is_demo===true,version:row.version,createdAt:row.created_at,updatedAt:row.updated_at};}
