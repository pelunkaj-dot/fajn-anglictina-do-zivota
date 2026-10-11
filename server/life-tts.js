/** Dedicated locale-specific model voices; existing /api/tts is unchanged. */
const escapeXml=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
export default async function handler(req,res){
 res.setHeader('Access-Control-Allow-Origin','*');res.setHeader('Access-Control-Allow-Methods','POST, OPTIONS');res.setHeader('Access-Control-Allow-Headers','Content-Type');
 if(req.method==='OPTIONS')return res.status(204).end();
 if(req.method!=='POST')return res.status(405).json({error:'Metoda není povolena.'});
 const {text,locale='en-GB'}=req.body||{};
 if(typeof text!=='string'||!text.trim()||text.length>500||!['en-GB','en-US'].includes(locale))return res.status(400).json({error:'Neplatný text nebo přízvuk.'});
 const key=process.env.AZURE_SPEECH_KEY,region=process.env.AZURE_SPEECH_REGION;
 if(!key||!region||!/^[a-z0-9-]+$/.test(region))return res.status(503).json({error:'Přehrávání není dostupné.'});
 const voice=locale==='en-GB'?'en-GB-SoniaNeural':'en-US-JennyNeural';
 try{
  const response=await fetch(`https://${region}.tts.speech.microsoft.com/cognitiveservices/v1`,{method:'POST',signal:AbortSignal.timeout(18000),headers:{'Ocp-Apim-Subscription-Key':key,'Content-Type':'application/ssml+xml','X-Microsoft-OutputFormat':'audio-24khz-48kbitrate-mono-mp3'},body:`<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="${locale}"><voice name="${voice}"><prosody rate="-8%">${escapeXml(text)}</prosody></voice></speak>`});
  if(!response.ok)return res.status(503).json({error:'Vzor se teď nepodařilo připravit.'});
  const bytes=Buffer.from(await response.arrayBuffer());res.setHeader('Content-Type','audio/mpeg');res.setHeader('Cache-Control','public, max-age=86400');return res.status(200).send(bytes);
 }catch{return res.status(503).json({error:'Vzor se teď nepodařilo připravit.'})}
}
export const config={maxDuration:25};
