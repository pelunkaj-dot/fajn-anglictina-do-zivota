import {normalise,matches} from './engine.js';
const ARTICLES=new Set(['a','an','the']);
const protectedNext=new Set(['few','little','lot','couple','number','great','good','more','less','most','least','same','other']);
const notes={
 indefinite:{title:'Neurčitý člen',impact:'Drobný nedostatek — sdělení je srozumitelné.',short:'Vynechaný člen nebrání domluvě. V běžné angličtině ho sem doplníme.',why:'Před počitatelným podstatným jménem v jednotném čísle potřebujeme člen nebo jiné určení. Když mluvíme o jednom blíže neurčeném předmětu, osobě či místě, používáme a nebo an. An patří před samohláskovou výslovnost, a před souhláskovou.'},
 definite:{title:'Určitý člen',impact:'Drobný nedostatek — sdělení je v této situaci srozumitelné.',short:'Partner ti rozumí. Člen the pomáhá označit konkrétní věc.',why:'The používáme, když je z kontextu jasné, kterou věc, osobu či místo myslíme. Tady vynechání členu domluvu neblokuje; doplněním bude věta přirozenější.'},
 agreement:{title:'Tvar slovesa',impact:'Drobný nedostatek — význam zůstává jasný.',short:'Osoba i sdělení jsou jasné. Upravíme jen tvar slovesa.',why:'V přítomném čase má sloveso po I a you základní tvar, například I live nebo you have. Ve třetí osobě jednotného čísla se obvykle přidává -s. U spojení there is / there are rozhoduje, zda mluvíme o jedné věci, nebo o více věcech.'}
};
// Specific reviewed collocations only; never interchange directions such as to/from.
const prepositions=[
 {canonical:/\bin cash\b/g,variants:['with cash','by cash'],why:'Pro placení hotově používáme spojení in cash. With cash je srozumitelné; ustálená podoba je in cash.'},
 {canonical:/\bby card\b/g,variants:['with card','on card'],why:'Pro platbu kartou používáme by card. With a card je také běžná správná formulace, když mluvíš o použití konkrétní karty.'},
 {canonical:/\bon (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b/gi,variants:['in $1','at $1'],why:'Před názvy dnů používáme on, například on Monday. Den z tvé odpovědi je jasný; upravujeme jen předložku.'},
 {canonical:/\bin the (morning|afternoon|evening)\b/gi,variants:['at the $1','on the $1'],why:'Pro části dne používáme in the morning, in the afternoon a in the evening. Výjimkou je at night. V této větě zůstává část dne srozumitelná.'},
 {canonical:/\bat (\d+(?::\d+)?(?:\s*(?:am|pm|o’clock|o'clock))?)\b/gi,variants:['in $1','on $1'],why:'Před konkrétním časem používáme at. Časový údaj v tvé větě se nezměnil, takže domluvě tato nepřesnost nebrání.'},
 {canonical:/\blive in (a|an|the) (flat|apartment|house|small flat|small house|small apartment)\b/gi,variants:['live at $1 $2'],why:'Když říkáme, v jakém typu bydlení žijeme, používáme live in. At se běžně používá s konkrétní adresou. Tady je typ bydlení jasný i s nepřesnou předložkou.'}
];
function articleMatch(value,reference){
 const input=normalise(value).split(' '),target=normalise(reference).split(' '),corrections=[];let i=0;
 for(let j=0;j<target.length;j++){
  const word=target[j];if(input[i]===word){i++;continue}
  if(ARTICLES.has(word)&&!protectedNext.has(target[j+1])){
   if((word==='a'||word==='an')&&(input[i]==='a'||input[i]==='an')){corrections.push(notes.indefinite);i++;continue}
   corrections.push(word==='the'?notes.definite:notes.indefinite);continue;
  }
  return null;
 }
 return i===input.length&&corrections.length?corrections:null;
}
export function assessCommunication(value,turn){
 if(matches(value,turn.accepted))return{status:'exact',model:turn.answer,corrections:[]};
 for(const model of turn.accepted){
  const variants=[{text:model,corrections:[]}];
  for(const rule of prepositions)for(const replacement of rule.variants){const text=model.replace(rule.canonical,replacement);if(text!==model)variants.push({text,corrections:[{title:'Předložka',impact:'Drobný nedostatek — význam v této situaci zůstává jasný.',short:'Domluvil by ses. Přirozenější je ustálené spojení ve vzoru.',why:rule.why}]})}
  for(const [pattern,replacement] of [[/\bI live\b/g,'I lives'],[/\bI have\b/g,'I has'],[/\byou have\b/gi,'you has'],[/\bthere are (two|three|four|five|six|seven|eight|nine|ten|\d+)\b/gi,'there is $1']]){const text=model.replace(pattern,replacement);if(text!==model)variants.push({text,corrections:[notes.agreement]})}
  for(const variant of variants){const articles=articleMatch(value,variant.text);if(matches(value,[variant.text])&&variant.corrections.length||articles){const corrections=[...variant.corrections,...(articles||[])].filter((c,i,a)=>a.findIndex(v=>v.title===c.title)===i);return{status:'communicated',model,corrections}}}
 }
 const n=normalise(value),numbers=n.match(/\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\b/g)||[];
 const negation=s=>/\b(?:not|cannot|never|no)\b/.test(s);
 const stripped=s=>s.replace(/\b(?:not|cannot|never|no|\d+|one|two|three|four|five|six|seven|eight|nine|ten)\b/g,'').replace(/\s+/g,' ').trim();
 for(const model of turn.accepted){const expected=normalise(model);if(n.replace(/\bcannot\b/g,'can')===expected.replace(/\bcannot\b/g,'can')&&n!==expected)return{status:'meaning',message:'Pozor, can a cannot (can’t) říkají opak: můžu a nemůžu. Zkus vyjádřit zamýšlený význam.'};if(n.replace(/\b(?:to|from)\b/g,'DIRECTION')===expected.replace(/\b(?:to|from)\b/g,'DIRECTION')&&n!==expected)return{status:'meaning',message:'Tady se mění směr: to znamená do nebo k, from znamená z nebo od. Partner by dostal jinou informaci. Zkus větu upravit.'};if(stripped(n)===stripped(expected)&&n!==expected){if(negation(n)!==negation(expected))return{status:'meaning',message:'Pozor, zápor mění sdělení. Partner by mohl pochopit opak toho, co chceš říct. Zkus větu upravit.'};const expectedNumbers=expected.match(/\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\b/g)||[];if(numbers.join('|')!==expectedNumbers.join('|'))return{status:'meaning',message:'Tady se mění počet nebo časový údaj. Partner by dostal jinou informaci. Porovnej údaj se zadáním a zkus to znovu.'}}}
 return{status:'unrecognised',message:'Tuhle formulaci zatím neumím spolehlivě posoudit. Nemusí být chybná. Zkus ji upravit, nebo si na vyžádání porovnej běžnou podobu.'};
}
