import crypto from 'node:crypto';
export const hash=value=>crypto.createHash('sha256').update(value).digest('hex');
export const id=()=>crypto.randomUUID();
export const authMode=()=>process.env.AUTH_MODE || 'disabled';
export async function sendCode(channel,identity,code,lang){
 if(authMode()==='development'&&process.env.NODE_ENV!=='production')return {provider:'development',developmentCode:code};
 if(channel==='email'&&process.env.RESEND_API_KEY&&process.env.AUTH_EMAIL_FROM){
 const r=await fetch('https://api.resend.com/emails',{method:'POST',signal:AbortSignal.timeout(15000),headers:{Authorization:`Bearer ${process.env.RESEND_API_KEY}`,'Content-Type':'application/json'},body:JSON.stringify({from:process.env.AUTH_EMAIL_FROM,to:[identity],subject:lang==='ko'?'마을일감 인증번호':'Ma-eul Ilgam verification code',text:`${code}\n${lang==='ko'?'5분 안에 입력해 주세요. 다른 사람에게 알려주지 마세요.':'Enter within 5 minutes. Do not share this code.'}`})});if(!r.ok)throw new Error('DELIVERY_FAILED');return {provider:'resend'};}
 if(channel==='phone'&&process.env.TWILIO_ACCOUNT_SID&&process.env.TWILIO_AUTH_TOKEN&&process.env.TWILIO_VERIFY_SERVICE_SID){
 const r=await fetch(`https://verify.twilio.com/v2/Services/${process.env.TWILIO_VERIFY_SERVICE_SID}/Verifications`,{method:'POST',signal:AbortSignal.timeout(15000),headers:{Authorization:'Basic '+Buffer.from(`${process.env.TWILIO_ACCOUNT_SID}:${process.env.TWILIO_AUTH_TOKEN}`).toString('base64'),'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams({To:identity,Channel:'sms',Locale:lang==='ko'?'ko':'en'})});if(!r.ok)throw new Error('DELIVERY_FAILED');return {provider:'twilio'};}
 throw new Error('AUTH_UNAVAILABLE');
}
export async function verifyProvider(challenge,code){if(challenge.provider!=='twilio')return hash(`${challenge.id}:${code}`)===challenge.code_hash;const r=await fetch(`https://verify.twilio.com/v2/Services/${process.env.TWILIO_VERIFY_SERVICE_SID}/VerificationCheck`,{method:'POST',signal:AbortSignal.timeout(15000),headers:{Authorization:'Basic '+Buffer.from(`${process.env.TWILIO_ACCOUNT_SID}:${process.env.TWILIO_AUTH_TOKEN}`).toString('base64'),'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams({To:challenge.identity,Code:code})});return r.ok&&(await r.json()).status==='approved';}
