import json,pathlib,re
root=pathlib.Path(__file__).parent
source=json.loads((root/'assets/course-source.json').read_text())
translations={};lines=(root/'assets/prompt-translations.txt').read_text().splitlines()
for i in range(0,len(lines),7):
 topic,level=lines[i].split('|');translations[(topic,level)]=lines[i+1:i+7]
assert len(translations)==48
foundations=json.loads((root/'assets/foundations.json').read_text())
glossary=json.loads((root/'assets/chunk-glossary.json').read_text())
# A1 presents full forms first. Heard contractions stay accepted and are explained on request.
def full_a1(text):
 pairs={"I'd":"I would","I'm":"I am","I'll":"I will","I've":"I have","It's":"It is","What's":"What is","isn't":"is not","don't":"do not","can't":"cannot","you're":"you are","we're":"we are","that's":"that is"}
 for short,full in pairs.items():
  text=re.sub(r'\b'+re.escape(short)+r'\b',full,text,flags=re.I)
 return text
for key,value in list(glossary.items()):
 expanded=full_a1(key)
 if expanded!=key:glossary.setdefault(expanded,value)
def chunks(answer,topic,level):
 import re
 result=[];occupied=set();lower=answer.lower()
 for en,cz in sorted(glossary.items(),key=lambda p:len(p[0]),reverse=True):
  for match in re.finditer(r'(?<![a-z])'+re.escape(en.lower())+r'(?![a-z])',lower):
   positions=set(range(match.start(),match.end()))
   if not positions&occupied:
    result.append((match.start(),{'en':answer[match.start():match.end()],'cz':cz}));occupied|=positions
 return [v for _,v in sorted(result)]
transferTranslations={
'Where would you like to go?':'Kam byste chtěli jet?', 'Can you still reach your destination?':'Můžete se ještě dostat do cíle?', 'Why did you miss your flight?':'Proč jste zmeškali let?', 'Would you like to change rooms?':'Chcete vyměnit pokoj?', 'What did your reservation include?':'Co bylo zahrnuto v rezervaci?', 'Does it fit?':'Sedí vám to?', 'What would you prefer?':'Čemu byste dali přednost?', 'Can we change the deadline?':'Můžeme změnit termín?', "Which costs haven't been considered?":'Které náklady nebyly zohledněny?', 'When do you feel worse?':'Kdy se cítíte hůř?', 'How have you felt since starting the medication?':'Jak se cítíte od zahájení užívání léků?', 'What time shall we meet?':'V kolik se sejdeme?', 'Is Wednesday convenient?':'Vyhovuje středa?', 'Would you like to invite anyone else?':'Chcete pozvat ještě někoho?', 'When did the problem start?':'Kdy problém začal?', 'Which conditions would you like clarified?':'Které podmínky si chcete nechat upřesnit?', 'Which days are you available?':'Které dny máte čas?', 'What would you like to improve?':'Co byste chtěli zlepšit?', 'What kind of feedback would you prefer?':'Jaké zpětné vazbě byste dali přednost?', 'What message would you like to leave?':'Jakou zprávu chcete zanechat?', 'When did the connection stop working?':'Kdy připojení přestalo fungovat?', 'Which charge are you questioning?':'Který poplatek zpochybňujete?', 'When do you need to be back?':'Kdy musíte být zpět?', 'What does the forecast say?':'Co říká předpověď?', 'How can we reduce waste?':'Jak můžeme omezit odpad?', 'Have you read the novel?':'Četli jste ten román?', 'What helped create suspense?':'Co pomohlo vytvořit napětí?', 'The dish contains several ingredients.':'Jídlo obsahuje několik přísad.'}
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
   turns.append({'id':f'{topic}-{level}-{j}','prompt':r[0],'intent':r[1],'answer':r[2],'translation':r[3],'accepted':[r[2],*r[4:]],'hint':hint(r[2]),'promptCz':translations[(topic,level)][j],'chunks':chunks(r[2],topic,level)})
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
promptMap={t['prompt']:t['promptCz'] for m in missions for t in m['turns']}
for line in (root/'assets/transfer-source.txt').read_text().splitlines():
 topic,level,prompt,intent,answer,translation,*accepted=line.split('|')
 m=next(m for m in missions if m['topic']==topic and m['level']==level)
 cz=transferTranslations.get(prompt,promptMap.get(prompt))
 assert cz,prompt
 m['transfer']={'id':m['id']+'-transfer','prompt':prompt,'promptCz':cz,'intent':intent,'answer':answer,'translation':translation,'accepted':[answer,*accepted],'hint':hint(answer),'chunks':chunks(answer,topic,level),'transfer':True}
for m in missions:
 t=m['transfer'];vocab.append({'id':'phrase-'+t['id'],'topic':m['topic'],'level':m['level'],'en':t['answer'],'cz':t['translation'],'accepted':t['accepted'],'kind':'phrase'})
for f in foundations:
 vocab.append({'id':'foundation-'+f['id'],'topic':'basics','level':f['level'],'en':f['en'],'cz':f['cz'],'accepted':[f['en']],'kind':'word','note':f['note']})
for m in missions:
 if m['level']=='A1':
  for t in [*m['turns'],m['transfer']]:
   original=t['answer'];t['answer']=full_a1(original);t['prompt']=full_a1(t['prompt'])
   if t['answer'] not in t['accepted']:t['accepted'].insert(0,t['answer'])
   t['hint']=hint(t['answer']);t['chunks']=chunks(t['answer'],m['topic'],'A1')
   if original!=t['answer']:t['contraction']={'short':original,'full':t['answer'],'note':'Stažený tvar znamená totéž jako plná podoba. Na A1 začínáme plnou podobou; zkrácenou můžeš používat také.'}
for v in vocab:
 if v['level']=='A1':
  v['en']=full_a1(v['en'])
  if v['en'] not in v['accepted']:v['accepted'].insert(0,v['en'])
# Every situation is individually reviewed for natural, context-complete responses.
context_lines=(root/'assets/contextual-responses.txt').read_text().splitlines()
assert len(context_lines)==48*8
reviewed=set()
# In beginner dialogue, teach the short reply first where the context supplies the rest.
short_primary={
 'restaurant-A1-1':'Jídelní lístek, prosím.','restaurant-A1-2':'Kuřecí polévku, prosím.','restaurant-A1-5':'Účet, prosím.',
 'travel-A1-0':'Do Londýna, prosím.','travel-A1-transfer':'Do Oxfordu, prosím.',
 'hotel-A1-1':'Alex Novák.','hotel-A1-transfer':'Sam Green.',
 'shopping-A1-0':'Tričko, prosím.','shopping-A1-2':'Velikost M, prosím.','shopping-A1-transfer':'Bundu, prosím.',
 'work-A1-0':'Sam.','work-A1-1':'Učitel.','work-A1-2':'Ve škole.','work-A1-3':'V osm.','work-A1-transfer':'Lékař.',
 'health-A1-1':'Bolest hlavy.','health-A1-transfer':'Bolest v krku.',
 'social-A1-0':'Anna.','social-A1-1':'Česká republika.','social-A1-2':'Brno.','social-A1-3':'Hudbu.','social-A1-4':'Trochu.','social-A1-transfer':'Tom.',
 'study-A1-0':'Angličtinu, prosím.','study-A1-transfer':'Španělštinu, prosím.',
 'outdoors-A1-1':'Do parku.','outdoors-A1-2':'Slunečno.','outdoors-A1-3':'Ne, je teplo.','outdoors-A1-5':'Připraven.','outdoors-A1-transfer':'Zima.',
 'culture-A1-0':'Filmy.','culture-A1-transfer':'Hudbu.'
}
for i in range(0,len(context_lines),8):
 topic,level=context_lines[i].split('|')
 mission=next(m for m in missions if m['id']==topic+'-'+level)
 for turn,line in zip([*mission['turns'],mission['transfer']],context_lines[i+1:i+8]):
  variants=line.split('|');assert all(variants),turn['id']
  turn['accepted']=list(dict.fromkeys([*turn['accepted'],*variants]));turn['contextReviewed']=True
  if turn['id'] in short_primary:
   turn['answer']=full_a1(variants[0]);turn['translation']=short_primary[turn['id']];turn['hint']=hint(turn['answer']);turn['chunks']=chunks(turn['answer'],topic,level)
   if not turn['chunks']:turn['chunks']=[{'en':turn['answer'],'cz':turn['translation']}]
  turn['accepted']=list(dict.fromkeys([turn['answer'],*turn['accepted']]))
  entry=next(v for v in vocab if v['id']=='phrase-'+turn['id']);entry['accepted']=turn['accepted'];entry['en']=turn['answer'];entry['cz']=turn['translation']
  reviewed.add(turn['id'])
assert len(reviewed)==336
out={'foundations':foundations,'levels' :levels,'topics':topics,'missions':missions,'vocabulary':vocab}
(root/'assets/course.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(f'{len(topics)} topics, {len(missions)} missions, {sum(len(m["turns"]) for m in missions)} turns, {len(vocab)} vocabulary entries')
