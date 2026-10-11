/** Accent-specific speech for FajnAnglictina. Independent of existing /api/tts. */
export default async function handler(req,res){
 res.setHeader('Access-Control-Allow-Origin','*');res.setHeader('Access-Control-Allow-Methods','POST, OPTIONS');res.setHeader('Access-Control-Allow-Headers','Content-Type');
 if(req.method==='OPTIONS')return res.status(204).end();
 if(req.method!=='POST')return res.status(405).json({error:'Metoda není povolena.'});
 const {text,locale='en-GB'}=req.body||{};
 if(typeof text!=='string'||!text.trim()||text.length>500||!['en-GB','en-US'].includes(locale))return res.status(400).json({error:'Neplatný text nebo přízvuk.'});
 if(!process.env.OPENAI_API_KEY)return res.status(503).json({error:'Přehrávání není dostupné.'});
 try{
  const response=await fetch('https://api.openai.com/v1/audio/speech',{method:'POST',signal:AbortSignal.timeout(18000),headers:{Authorization:'Bearer '+process.env.OPENAI_API_KEY,'Content-Type':'application/json'},body:JSON.stringify({model:'gpt-4o-mini-tts',voice:'coral',input:text,response_format:'mp3',instructions:locale==='en-GB'?'Read only the supplied text in clear, natural British English, using a contemporary standard southern British accent. Use British vowel sounds and non-rhotic pronunciation. Speak at a relaxed teaching pace. Do not add any words.':'Read only the supplied text in clear, natural American English, using a General American accent with rhotic pronunciation. Speak at a relaxed teaching pace. Do not add any words.'})});
  if(!response.ok)return res.status(503).json({error:'Vzor se teď nepodařilo připravit.'});
  const bytes=Buffer.from(await response.arrayBuffer());res.setHeader('Content-Type','audio/mpeg');res.setHeader('Cache-Control','public, max-age=86400');return res.status(200).send(bytes);
 }catch{return res.status(503).json({error:'Vzor se teď nepodařilo připravit.'})}
}
export const config={maxDuration:25};
