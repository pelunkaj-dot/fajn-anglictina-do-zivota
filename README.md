# FajnAngličtina do života

Plný situační kurz A1–B2 a adaptivní trenér slovní zásoby. Buildless HTML + ES modules; původní `mluvme_en.html` se nemění.

- 12 tematických okruhů × 4 úrovně = 48 misí, 288 autorských komunikačních zadání.
- 744 položek trenéru (384 slov/spojení + 288 původních vět + 48 obměn + 24 základních spojení), filtrování úrovně/tématu/typu/paměťového stavu.
- Výběr, psaní, poslech a kartičky. Chyby se vracejí do aktuální série, další termín opakování se ukládá. Intervaly 5 minut / 1 / 3 / 7 / 14 / 30 dnů. Sebehodnocení kartiček je důvěra v uživatele.
- Mise: skládání, výběr nebo psaní z ověřených variant. Volný text nemá AI sémantické hodnocení; nerozpoznanou formulaci aplikace neprohlašuje za jazykovou chybu.
- Nápověda a vzor pouze na vyžádání. Britské i americké schválené varianty jsou přijímány.
- Výslovnost: vyžádané nahrávání, automatický limit 14 s, ukončení tlačítkem, zastavení mikrofonu při odchodu, konverze mono PCM16 WAV 16 kHz, stávající `fdc-gateway/api/pronunciation` s `phoneticAssessment=true`. Shoda slov a výslovnost jsou oddělené. Nedostupnost služby nikdy neznamená úspěch ani chybu uživatele.
- Poslech přes nový nezávislý endpoint `/api/life-tts` s pevnými britskými/americkými hlasy a mezipamětí v paměti stránky. Při nedostupnosti použije přesný dostupný hlas `en-GB`/`en-US` v zařízení. Když daný hlas chybí, aplikace to oznámí a neslibuje jiný přízvuk.
- Světlý, tmavý, fialový vzhled; vypnutí města, animací a zvuku; respektování omezení pohybu.
- Výsledky lokálně v prohlížeči; export/import JSON zálohy. Bez centrálních uživatelských účtů. Při kontrole hlasu audio zpracuje stávající externí služba; aplikace nahrávky neukládá.

## Vývoj a kontroly

`python3 build-content.py` sestaví data z editovatelných zdrojů. `npm test` provede obsahové a logické testy. CI navíc kontroluje všechny mise přes UI, čtyři režimy trenéru, mobilní šířku, persistenci a simulovanou hlasovou odpověď. Tato simulace ověřuje integraci, ne přesnost hodnocení skutečného lidského hlasu. Živý mikrofon a dostupnost hlasů vyžadují ověření v cílovém zařízení.

GitHub Pages workflow nasazuje pouze po úspěšných kontrolách. Pokud nastavení Pages nelze automaticky zapnout, v Settings → Pages vyberte Source: GitHub Actions.

## Obsah

A1: krátké konkrétní potřeby; A2: běžné detaily; B1: řešení problémů a zdůvodnění; B2: nuance, vyjednávání, argumentace. Úrovně jsou didaktické zařazení autorského materiálu, nikoli certifikace CEFR. Město přijímá první dokončení mise jako odměnu; opakování téže mise nepřidává dalších 30 XP. Vzor/nápověda se evidují jako opora, přeskočený mikrofon se neeviduje jako ověřená výslovnost.

## Ověření první verze

Obsahové testy prošly pro všech 48 misí a 744 položek. Prohlížečové testy dokončily všech 48 misí přes UI, kontrolovaly všechny režimy, ověřené alternativy, nápovědu na vyžádání, uložení rozepsaného vstupu, rekurenci chyb, zálohy, hlasový požadavek a mobilní rozložení. Snímky byly vizuálně zkontrolovány. Živá služba vrátila britský i americký zvuk a skutečné hodnocení hlásek; nejde o náhradu kontroly lidského hlasu na cílovém zařízení.

## Opory a didaktický průchod

Každá původní i obměněná situace má autorský český význam repliky, významová spojení a možnost poslechu. A1 začíná od nuly; A2–B2 si mohou připomenout nižší základy přímo v situaci. Opory se otevírají pouze na vyžádání. Překlad otázky, zopakování ani zpomalení neoznačují odpověď jako podpořenou. Vodítko a vzor se evidují jako opora, otevřená spojení se uloží k upevnění bez zvýšení počtu chyb. Po použití opory se na konci mise objeví obměněná situace. Samostatné použití vyžaduje ověřenou obměnu bez opory a neúspěšného pokusu; pouhé přečtení vzoru nestačí.

Můj pokrok rozlišuje prošel / s oporou / použil samostatně, přehled úrovní a témat, chybové a zapomenuté položky, splatné opakování a zvlášť výslovnost. Slabá místa lze otevřít rovnou k procvičení, včetně zapomenutých základů z nižší úrovně. Původní výsledky a preference zůstávají zachované. Staré dokončené mise nejsou zpětně vydávány za ověřené samostatné obměny.

Při prvním neúspěchu zůstává zápis nebo nabídka zachována. Další pokus nabídne otevření vodítka, ale sám odpověď neodkryje. Psanou neznámou formulaci aplikace stále neumí sémanticky ověřit; nepovažuje ji automaticky za jazykovou chybu.
