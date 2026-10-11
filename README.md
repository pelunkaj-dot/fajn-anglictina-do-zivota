# FajnAngličtina do života

Plný situační kurz A1–B2 a adaptivní trenér slovní zásoby. Buildless HTML + ES modules; původní `mluvme_en.html` se nemění.

- 12 tematických okruhů × 4 úrovně = 48 misí, 288 autorských komunikačních zadání.
- 672 položek trenéru (384 slov/spojení + 288 vět), filtrování úrovně/tématu/typu/paměťového stavu.
- Výběr, psaní, poslech a kartičky. Chyby se vracejí do aktuální série, další termín opakování se ukládá. Intervaly 5 minut / 1 / 3 / 7 / 14 / 30 dnů. Sebehodnocení kartiček je důvěra v uživatele.
- Mise: skládání, výběr nebo psaní z ověřených variant. Volný text nemá AI sémantické hodnocení; nerozpoznanou formulaci aplikace neprohlašuje za jazykovou chybu.
- Nápověda a vzor pouze na vyžádání. Britské i americké schválené varianty jsou přijímány.
- Výslovnost: vyžádané nahrávání, automatický limit 14 s, ukončení tlačítkem, zastavení mikrofonu při odchodu, konverze mono PCM16 WAV 16 kHz, stávající `fdc-gateway/api/pronunciation` s `phoneticAssessment=true`. Shoda slov a výslovnost jsou oddělené. Nedostupnost služby nikdy neznamená úspěch ani chybu uživatele.
- Poslech přes nový nezávislý endpoint `/api/life-tts` s britskými/americkými hlasovými instrukcemi a mezipamětí v paměti stránky. Při nedostupnosti použije přesný dostupný hlas `en-GB`/`en-US` v zařízení. Když daný hlas chybí, aplikace to oznámí a neslibuje jiný přízvuk.
- Světlý, tmavý, fialový vzhled; vypnutí města, animací a zvuku; respektování omezení pohybu.
- Výsledky lokálně v prohlížeči; export/import JSON zálohy. Bez centrálních uživatelských účtů. Při kontrole hlasu audio zpracuje stávající externí služba; aplikace nahrávky neukládá.

## Vývoj a kontroly

`python3 build-content.py` sestaví data z editovatelných zdrojů. `npm test` provede obsahové a logické testy. CI navíc kontroluje všechny mise přes UI, čtyři režimy trenéru, mobilní šířku, persistenci a simulovanou hlasovou odpověď. Tato simulace ověřuje integraci, ne přesnost hodnocení skutečného lidského hlasu. Živý mikrofon a dostupnost hlasů vyžadují ověření v cílovém zařízení.

GitHub Pages workflow nasazuje pouze po úspěšných kontrolách. Pokud nastavení Pages nelze automaticky zapnout, v Settings → Pages vyberte Source: GitHub Actions.

## Obsah

A1: krátké konkrétní potřeby; A2: běžné detaily; B1: řešení problémů a zdůvodnění; B2: nuance, vyjednávání, argumentace. Úrovně jsou didaktické zařazení autorského materiálu, nikoli certifikace CEFR. Město přijímá první dokončení mise jako odměnu; opakování téže mise nepřidává dalších 30 XP. Vzor/nápověda se evidují jako opora, přeskočený mikrofon se neeviduje jako ověřená výslovnost.
