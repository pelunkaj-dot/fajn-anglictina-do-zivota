"""Generate a separate static taste: no speech service, microphone or remote fonts."""
import json,pathlib,re
root=pathlib.Path(__file__).parent
assets=root/'assets'
full=json.loads((assets/'course.json').read_text())
topics={'restaurant','travel','shopping'}
missions=[]
for mission in full['missions']:
 if mission['topic'] in topics:
  mission=dict(mission);mission['turns']=mission['turns'][:3];missions.append(mission)
phrase_ids={'phrase-'+turn['id'] for m in missions for turn in [*m['turns'],m['transfer']]}
foundations=[f for level in full['levels'] for f in [x for x in full['foundations'] if x['level']==level][:2]]
foundation_ids={'foundation-'+f['id'] for f in foundations}
words=[v for topic in topics for level in full['levels'] for v in [x for x in full['vocabulary'] if x['kind']=='word' and x['topic']==topic and x['level']==level][:4]]
word_ids={v['id'] for v in words}
data={**full,'topics':[t for t in full['topics'] if t['id'] in topics],'missions':missions,'foundations':foundations,'vocabulary':[v for v in full['vocabulary'] if v['id'] in phrase_ids|word_ids|foundation_ids]}
(assets/'demo-course.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
html=(root/'index.html').read_text().replace('<title>FajnAngličtina do života</title>','<title>Ochutnávka · FajnAngličtina do života</title>')
html=html.replace('<meta name="description" content="FajnAngličtina do života: situační mise A1–B2, chytrý trenér slovní zásoby a britská i americká výslovnost.">','<meta name="description" content="Vyzkoušej Angličtinu do života: krátké situace A1–B2, přirozené odpovědi a trenér slovní zásoby.">')
html=html.replace('<meta name="viewport"', '<meta http-equiv="Content-Security-Policy" content="default-src \'self\'; connect-src \'self\'; script-src \'self\'; style-src \'self\' \'unsafe-inline\'; img-src \'self\' data:; font-src \'self\'; media-src \'none\'; object-src \'none\'; base-uri \'self\'; frame-src \'none\'; form-action \'none\'"><meta name="viewport"')
html=html.replace('<body data-theme="light">','<body data-theme="light" data-demo="true">')
html=html.replace('href="assets/style.css"','href="assets/demo-style.css"').replace('src="assets/app.js"','src="assets/demo-app.js"')
html=html.replace('<label><span>Výslovnost</span>','<label hidden><span>Výslovnost</span>')
banner='<section class="demo-banner" aria-label="Ochutnávka"><div><strong>Ochutnávka · Angličtina do života</strong><span>3 témata · A1–B2 · krátké mise a trenér slovní zásoby. Bez poslechu a kontroly výslovnosti.</span></div><a class="primary" href="https://fajndoucko.cz/fajncvicebna/" target="_blank" rel="noopener">Chci plnou verzi ↗</a></section>'
html=html.replace('<main id="app">',banner+'<main id="app">')
(root/'demo.html').write_text(html)
style=(assets/'style.css').read_text();style=re.sub(r"^@import[^\n]*\n",'',style)
style+='''\n.demo-banner{max-width:1440px;margin:20px auto 0;padding:20px 28px;background:var(--tint);border:1px solid var(--accent);border-radius:18px;display:flex;align-items:center;justify-content:space-between;gap:18px}.demo-banner strong{display:block;font-size:1.15rem}.demo-banner span{display:block;color:var(--muted);margin-top:5px;font-size:.9rem}.demo-banner a{flex-shrink:0;text-align:center}.demo-speaking{padding:20px;background:var(--warm);border-radius:16px;margin-top:24px}.demo-speaking h3{font-family:Georgia,serif;font-size:1.35rem}.demo-speaking p:last-child{margin-bottom:0}.demo-full-note{padding:16px;background:var(--tint);border-radius:12px}.demo-full-note a{text-decoration:underline}.demo-banner [hidden]{display:none}@media(max-width:600px){.demo-banner{margin:14px 16px 0;padding:16px;display:block}.demo-banner a{display:block;margin-top:12px}.demo-speaking{padding:16px}}\n'''
(assets/'demo-style.css').write_text(style)
app=(assets/'app.js').read_text().replace("from './speech.js'","from './demo-speech.js'").replace("from './guide.js'","from './demo-guide.js'").replace("from './city.js'","from './demo-city.js'").replace("const KEY='fajn-anglictina-do-zivota-v1'","const KEY='fajn-anglictina-do-zivota-demo-v1'").replace("fetch('assets/course.json')","fetch('assets/demo-course.json')")
app=app.replace(',levelGuidance,',',levelGuidance as fullLevelGuidance,',1)
app=app.replace("const KEY=","const levelGuidance={...fullLevelGuidance,A1:'Začínáš od nuly? Přečti otázku. Když nerozumíš, otevři Co říká? Pak si můžeš nechat vysvětlit části odpovědi a sestavit ji ze slov.'};\nconst KEY=",1)
app=app.replace('Každá mise je šest kroků do skutečného života.','Každá ukázková mise má tři situace. Plná verze rozvíjí všech 12 témat.')
app=app.replace('POSLECHNI A ZOPAKUJ','PŘEČTI A ZOPAKUJ').replace('Nejdřív si ji poslechni a zopakuj vlastními ústy. Potom sestav svou odpověď.','Přečti si ji a zkus ji vyslovit nahlas. Potom sestav svou odpověď.')
app=app.replace('<div class="listen-action">','<div class="listen-action" hidden>').replace('>Přehrát znovu</button>',' hidden>Přehrát znovu</button>').replace('>Přehrát pomaleji</button>',' hidden>Přehrát pomaleji</button>')
app=app.replace('<small>▷ Poslechnout spojení</small>','<small>Význam spojení</small>')
app=app.replace('<button class="secondary" id="model-listen">','<button class="secondary" id="model-listen" hidden>').replace('<button class="secondary" id="foundation-listen">','<button class="secondary" id="foundation-listen" hidden>')
app=app.replace("['listening','Poslech','Poslechni angličtinu a vyber význam'],",'')
app=app.replace('Po odpovědi ji můžeš přečíst nahlas a zkontrolovat výslovnost.','Po odpovědi ji zkus přečíst nahlas. Kontrola výslovnosti je součástí plné verze.')
app=app.replace('Britské i americké varianty jsou v pořádku. Po odpovědi si můžeš procvičit výslovnost.','Krátká odpověď může být úplně správná. Důležité je předat zamýšlený význam.')
app=app.replace('Zaměř se na označená slova.','Zkus větu znovu nahlas.')
app=app.replace('${spoken}/${a.turns.length}', '—').replace('ověřených výslovností','kontrola výslovnosti v plné verzi')
start=app.index('<section class="progress-card"><h2>Výslovnost zvlášť</h2>')
end=app.index('</section></div><section class="progress-card"><h2>Co potřebuje upevnit?',start)
app=app[:start]+'''<section class="progress-card"><h2>Co přidává plná verze?</h2><p>Všech 12 témat, 48 úplných misí, 336 situací a bohatší trenér slovní zásoby. Navíc poslech v britské i americké angličtině a dobrovolná kontrola výslovnosti.</p><a class="primary" href="https://fajndoucko.cz/fajncvicebna/" target="_blank" rel="noopener">Chci plnou verzi ↗</a>'''+app[end:]
app=app.replace("if(matchMedia('(prefers-reduced-motion: reduce)').matches)","if(state.vocabFilters.mode==='listening')state.vocabFilters.mode='choice';if(state.active?.kind==='vocab'&&state.active.mode==='listening')state.active.mode='choice';if(matchMedia('(prefers-reduced-motion: reduce)').matches)")
app=app.replace("Výslovnostní nahrávka se posílá pouze při vyžádané kontrole. Modul ji neukládá mezi výsledky.","Ochutnávka nepracuje s mikrofonem ani hlasovými službami. Výsledky ukládá jen v tomto prohlížeči, odděleně od plné verze.")
(assets/'demo-app.js').write_text(app)
guide=(assets/'guide.js').read_text().replace("['Poslechni',", "['Přečti',")
(assets/'demo-guide.js').write_text(guide)
city=(assets/'city.js').read_text().replace('/ 48 misí','/ 12 ukázkových misí').replace('/48 misí','/12 ukázkových misí')
(assets/'demo-city.js').write_text(city)
print(f'Demo: {len(missions)} short missions, {sum(len(m["turns"]) for m in missions)} base situations, {len(data["vocabulary"])} vocabulary entries')
