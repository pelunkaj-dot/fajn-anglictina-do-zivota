import json,pathlib
root=pathlib.Path(__file__).parent
source=json.loads((root/'assets/course-source.json').read_text())
levels=['A1','A2','B1','B2'];topics=[];missions=[];vocab=[]
def hint(answer):
 lower=answer.lower()
 guides=[('could','Zdvořilou žádost můžeš začít pomocí Could…'),('would','Zdvořilou otázku můžeš začít pomocí Would…'),("i'd prefer",'Vyjádři svou preferenci pomocí I would prefer…'),("i'd like",'Vyjádři přání pomocí I would like…'),("i've",'Zkušenost nebo dosavadní stav vyjádři pomocí I have…'),('if ','Použij podmínku začínající If…'),('is there','Na existenci něčeho se ptej pomocí Is there…'),('how','Začni otázkou How… a upřesni, na co se ptáš.'),('what','Začni otázkou What…'),('where','Na místo se ptej pomocí Where…'),('when','Na čas se ptej pomocí When…'),('do you','Použij otázku Do you…'),('i am','Začni podmětem I a slovesem am.'),("i'm",'Začni podmětem I a slovesem am, zkráceně I am → I’m.')]
 guide=next((msg for prefix,msg in guides if lower.startswith(prefix)),'Použij začátek níže a dokonči požadovaný význam.')
 return guide+' Začátek vzoru: '+ ' '.join(answer.split()[:min(3,len(answer.split())-1 or 1)])+'…'
for topic,t in source.items():
 topics.append({'id':topic,**{k:t[k] for k in ['title','place','colour','icon']}})
 for level,rows in t['levels'].items():
  turns=[]
  for j,r in enumerate(rows):
   turns.append({'id':f'{topic}-{level}-{j}','prompt':r[0],'intent':r[1],'answer':r[2],'translation':r[3],'accepted':[r[2],*r[4:]],'hint':hint(r[2])})
   vocab.append({'id':f'phrase-{topic}-{level}-{j}','topic':topic,'level':level,'en':r[2],'cz':r[3],'accepted':[r[2],*r[4:]],'kind':'phrase'})
  missions.append({'id':f'{topic}-{level}','topic':topic,'level':level,'title':t['title'],'turns':turns})
for line in (root/'assets/vocabulary-source.txt').read_text().splitlines():
 topic,level,items=line.split('|')
 for j,pair in enumerate(items.split(';')):
  en,cz=pair.split('=');vocab.append({'id':f'word-{topic}-{level}-{j}','topic':topic,'level':level,'en':en,'cz':cz,'accepted':[en],'kind':'word'})
# British/American variants are accepted, not penalised.
variants={'bill':'check','lift':'elevator','flat':'apartment','cinema':'movie theater','return ticket':'round-trip ticket','single ticket':'one-way ticket','tap':'faucet','neighbour':'neighbor','colour':'color','kilometre':'kilometer','authorise':'authorize','interval':'intermission','toilet':'restroom','film':'movie','post':'mail','changing room':'fitting room'}
for v in vocab:
 if v['en'] in variants:v['accepted'].append(variants[v['en']])
out={'levels':levels,'topics':topics,'missions':missions,'vocabulary':vocab}
(root/'assets/course.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(f'{len(topics)} topics, {len(missions)} missions, {sum(len(m["turns"]) for m in missions)} turns, {len(vocab)} vocabulary entries')
