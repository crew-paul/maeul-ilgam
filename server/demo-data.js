// Fictional examples only. Nothing is written to disk or to an external service.
const samples=[
 ['Photograph strawberries for our online shop','Gimje · 김제시','09:00','12:00','50000','total','1'],
 ['Pack freshly harvested sweet potatoes','Haenam · 해남군','09:00','16:00','90000','day','2'],
 ['Sort apples and prepare delivery boxes','Yeongju · 영주시','09:00','15:00','14000','hour','3'],
 ['Prepare pear gift boxes','Naju · 나주시','10:00','15:00','70000','total','2'],
 ['Label and pack honey jars','Yangpyeong · 양평군','10:00','14:00','60000','total','1'],
 ['Help set up a farmers market stall','Wanju · 완주군','08:00','12:00','60000','total','2'],
 ['Write short descriptions for our vegetables','Goesan · 괴산군','09:00','12:00','50000','total','1'],
 ['Organize supplies in the greenhouse','Nonsan · 논산시','09:00','14:00','15000','hour','2'],
 ['Pack dried persimmons for delivery','Sangju · 상주시','09:00','16:00','90000','day','2'],
 ['Update product listings in our farm shop','Namwon · 남원시','10:00','14:00','75000','total','1'],
];
export async function seedDemoData(db){
 const owner='d0000000-0000-4000-8000-000000000000';
 await db.transaction(async tx=>{
  await tx.query("INSERT INTO users(id,identity,channel) VALUES($1,'demo:fixtures','guest') ON CONFLICT DO NOTHING",[owner]);
  for(let i=0;i<samples.length;i++){
   const [task,location,startTime,endTime,payAmount,payUnit,headcount]=samples[i];
   const date=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Seoul',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(Date.now()+(i+1)*86400000));
   const data={task,location,date,startTime,endTime,payAmount,payUnit,headcount,currency:'KRW'};
   const id=`d0000000-0000-4000-8000-${String(i+1).padStart(12,'0')}`;
   await tx.query("INSERT INTO jobs(id,owner_id,status,data,is_demo) VALUES($1,$2,'published',$3,true) ON CONFLICT DO NOTHING",[id,owner,JSON.stringify(data)]);
  }
 });
}
