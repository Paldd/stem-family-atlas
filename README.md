# STEM Family Atlas

## Языковые версии

Русский сайт: https://paldd.github.io/stem-family-atlas/
Испанский сайт: https://paldd.github.io/stem-family-atlas/es/

Переключатель RU / ES сохраняет раздел и параметры ссылки. Обе версии используют одни и те же ID записей и локальные планы браузера. Язык сайта не меняет язык обучения или судейства, указанный в карточке.

Испанская версия включает все записи, досье, разделы, региональные подразделы и публичные выгрузки. Это перевод существующей базы, а не новый аудит дат организаторов. Большой корпус переведён локальными моделями; интерфейс и ключевые термины имеют отдельный редакционный словарь. Полная ручная лингвистическая проверка каждого длинного досье не заявляется. Неизвестные условия источников остаются неизвестными.

Переводы хранятся в `data/i18n/es.json`, редакционные уточнения — в `data/i18n/es-reviewed.json`. `ui-source-tokens.json` фиксирует переводимые JavaScript-токены и хеши оригинальных файлов. При изменении русского материала нужно обновить переводы и токены. Сборка блокируется, если фрагмент не переведён; автоматическая публикация не обращается к платным API или моделям.

После основной сборки выполните:

```sh
python3 scripts/build-spanish.py
python3 scripts/verify-spanish.py
```

Проверка сравнивает состав разделов, все ID, даты, цифры, технические знаки, URLs и полные JSON/SQLite выгрузки. Остатки русских имён файлов в ссылках сохранены намеренно: имена файлов и официальные URLs не переименовываются при переводе.

Для локального перевода использованы Helsinki-NLP/OPUS-MT ru-es (Apache-2.0) и Meta NLLB-200 distilled 600M (CC-BY-NC-4.0), с последующей редактурой и проверками; модели не включены в репозиторий. Проект предназначен для семейного некоммерческого планирования. Ссылки на модели и метод находятся в `data/i18n/translation-method.json`.

[Открыть сайт](https://paldd.github.io/stem-family-atlas/) · [Статус публикации](https://github.com/Paldd/stem-family-atlas/actions/workflows/pages.yml)

Интерактивный семейный атлас соревнований, лиг, выставок, лагерей, постоянных школ и образовательных маршрутов. Текущая версия оформления — **139**: 13 цветовых направлений, интерактивные фильтры, карты и календарь. В исходной базе 3 847 записи, 1 119 досье программ лагерей/обучения, 144 профиля лиг/программ и 62 школьных досье. Это продолжающееся исследование: охват мира и проверки местного допуска пока неполные.

## Как обновляется сайт

Репозиторий `Paldd/stem-family-atlas`, ветка `main`, — основное место дальнейшей работы. После каждого push в `main` GitHub Actions собирает полные данные, проверяет источники и выгрузки и публикует `dist/` через GitHub Pages. При ошибке проверки новая версия не публикуется. PR проходят проверку без публикации.

Отредактированное локально изменение появляется на общей ссылке **после commit, push и успешной публикации**. Данные мероприятий не исследуются заново автоматически при push: для новых дат, цен и условий нужен отдельный аудит официальных источников. Дата последней проверки указана в досье. Файл `release.json` на опубликованном сайте показывает точный исходный коммит и время сборки; это не дата нового аудита мероприятий.

## Работа с исходниками

`data/catalog.json` — основной источник данных. Подробный справочник лагерей и его интеграция находятся в `data/camp-programmes-deep-2026-2027.json` и `scripts/`. Не восстанавливайте данные из исходного архива сентября: это потеряет последующие проверки.

```sh
git clone https://github.com/Paldd/stem-family-atlas.git
cd stem-family-atlas
python3 scripts/build-database.py
python3 scripts/build-spanish.py
python3 scripts/verify-site.py
python3 scripts/verify-spanish.py
python3 -m http.server 8772 --directory dist --bind 127.0.0.1
```

Локальный просмотр: `http://127.0.0.1:8772/`. После проверки изменения можно отправить обычным commit/push в `main`; затем проверить Actions и общую ссылку. Сборке нужны Python 3.10+ и стандартная библиотека; для проверки синтаксиса браузерного JavaScript нужен Node.js. Установки npm и внешнего серверного API не требуется.

## Структура

- `dist/`: сайт, календарь, карты, отчёты и полные выгрузки; автоматически публикуется.
- `data/`: исходные записи, доказательства проверок и незавершённый план исследования.
- `scripts/`: сборка, интеграция данных и проверки.
- `.github/workflows/pages.yml`: автоматическая проверка и публикация.
- `AGENTS.md`: правила дальнейшей работы с этим репозиторием.

Для скачивания полных баз используйте ZIP SQLite/JSON на сайте. Они сохраняют все записи; цена, старая программа, неподтверждённый язык, отсутствие мест и предварительный возрастной подбор отмечаются отдельно.

Сайт открывается на телефонах и компьютерах по общей ссылке. Избранное и личные отметки маршрута хранятся в браузере; обмен ссылкой передаёт условия подбора, а не автоматически всё избранное. Регистрации, оплаты и сообщения организаторам сайт не отправляет.

GitHub содержит новый исходный снимок последней версии. Предыдущая локальная история сохранена отдельно на ветке `sites-local-v137`; данные старого Sites-проекта в `.openai/` не публикуются. Прежняя ссылка ChatGPT Site этим репозиторием не обновляется.

Правила [публикации через GitHub Actions](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## История исследования и оформления до переноса

Motion v53 (2026-10-02) adds an interactive four-stage engineering diagram with a one-shot animated cycle, cursor-following eyes on the existing robot, animated personal progress, subtle card tilt/light, regional route animation, staggered entry and expandable age-stage motion. Controls support keyboard and touch. Global pause is browser-local; system reduced motion takes precedence. The route animation stops offscreen and in hidden documents. Scene controls never change completion marks, favorites, eligibility or research. Research and downloads remain byte-identical to v52. Authored files: `dist/assets/motion.js` / `.css`.

Experience v52 (2026-10-02) improves presentation while preserving research v51 byte for byte: 1,794 cards, 140 league profiles, 62 schools and 152 school-history results. `#journey` adds a family track with child, goal, topic, geography, a personal target, six proposed 90-day steps and each child's existing age/league progression. Local marks are separate for each track combination; they do not establish admission, applications, payments or awards. A JSON export/import transfers the track and favorites without replacing existing favorites. A shared URL transfers only track settings, without the personal target or completion marks. `#destinations` groups the ten existing country guides and derives geographic counts from their actual focus data. The grouped sidebar, mobile navigation, regional section jumps, global search, working browser history, vector diagrams and motion preferences are implemented in `dist/assets/experience.js` / `.css`. Those authored UI files and `dist/index.html` are not regenerated by the database builder. The dataset and all previous downloads remain unchanged; worldwide coverage is still partial (80 of 249 countries/territories have records, none is fully audited).


Southeast Asia v37 (sources checked 2026-10-01): Malaysia / Indonesia / Vietnam / Philippines now have a dedicated `#southeastasia` comparison. Adds 42 records: 27 competition categories / pathways, 9 camp or learning candidates and 6 exhibitions, plus 6 national profiles. The database has 1,535 records, 114 profiles and 32 unchanged school dossiers. Engage 12U is inclusive age 12 on May 6, 2027; Remote needs an invitation and the Hanoi scrimmage is Middle School only. Vietnam Open explicitly describes international teams; world spots remain separate. KodingNext explicitly teaches Indonesian / English; HEC describes English engineering but formal ages and future camp dates are unknown. Soleh Camp starts at 7 and DRABOT is online for primary ages 10–12. PhilSA Kibo requires Filipino citizenship. ITEX exhibition days are May 27–28, 2027; May 29 is its awards ceremony. Three Indonesian B2B shows prohibit under-18 visitors. All 1,119 prior family calendar entries remain identical; the new family calendar has 1,129 entries and the separate exhibition calendar has 82. All prior Europe comparisons, 116 school-history records and 23 top picks remain. Exports: `STEM_Southeast_Asia.json` / `.md`. Worldwide research stays active and partial.


Europe v30 (2026-10-01): Switzerland / Spain / France have a dedicated `#europe` comparison, 37 new records (19 learning cards from four operators, 15 competition pathways / editions / qualifiers, three professional exhibitions), four national profiles and three school dossiers. The catalogue now has 1,297 records, 91 profiles and 25 schools. All earlier records except the explicit MWC2027 date update, all earlier schools, 116 history entries and 23 top picks are preserved. Spanish FLL K8 age8–16, classic Challenge10–16, hardware / team differences and noncompetitive categories are traced to actual2026/27registration. Swiss Starter6–10 and French Junior age7/8conflict remain separate from foreign world qualification. ABI public forms establish2026dates and bilingual technical teaching; Helvetic language/year conflicts and Tinker B2B windows remain explicit. Family ICS retains981previousUIDs and adds19; major expoICS retains65 and adds4. No school world-prize claim or global completeness is inferred.

Oceania / Pacific v29 (2026-10-01): adds ten records, including Fiji's tourist-oriented 6–16 day camp, four actual STEAM-ED October workshop days, the host's strict 7–12 BrainPlay Code Club, two Australian national game / video pathways, an online results showcase, and the closed French Polynesian CM1 / CM2 robotics season. A primary-school route in RoboCupJunior Australia explicitly accepts international teams and national equal-placement awards, while excluding foreign qualification through Australia for the world championship. Separate profiles explain these gates. Website-only EN tags were removed from BrainPlay and the NZ VIQRC national record; the latter's published birth cutoff and dates are corroborated by KiwiBots. All 23 existing best recommendations, schools, results history and family strategy are preserved. The new camps remain candidates with unconfirmed instruction language; no new worldwide quality ranking or completeness is claimed.

The `/#catalog` view renders every matching record without pagination, including excluded and undated records by default. The reset button restores the full database; country, topic, age and admission filters still apply. A festival may have several linked discipline records (`parent_event_id`); card counts are not counts of independent festivals. `date_scope=festival_window` identifies a published festival window whose exact discipline day is unknown.

The v6 primary-source audit is in `data/audit-v6.json`. It retains unconfirmed foreign admission, language, currency and local-rule conflicts instead of treating registrations or training certificates as international wins.

The v7 audit is `data/audit-v7.json`. Published score-submission periods use `date_scope=submission_window`; they are not month-long in-person events. The complete downloadable ICS is now regenerated by the same database builder and includes upcoming, non-excluded event windows and distinct deadlines. Undated programs and past-only events are not assigned future calendar dates.

The v8 audit is `data/audit-v8.json`. It distinguishes network-directory exhibition dates from corroborated host rules, English-language camp instruction from an English website, and weekly programs from holiday camps. Different age tracks and real sessions have separate records; unannounced campus/theme/time combinations are not invented. Worldwide coverage remains unfinished.

The latest completeness inventory is `data/audit-v51.json`, also available interactively in `/#about`. Its counts are regenerated from the database: six continental inventories, league-to-event links, and major exhibition editions. It preserves the unfinished country coverage and source conflicts. The v13 pass adds sixteen dated holiday shifts, an undated LEGO Junior course, six gaming exhibition editions, the EU Code Week activity window, and the UK-residency-gated BAFTA YGD route. Eight existing gaming shows are now included in the major-exhibition view. No country is represented as fully audited.

The v14 pass adds three TechEx city editions, Tech Show London, HRIE, SIEAR, SIA and CHITEC with separate child admission, future-date conflicts and historical-only claims. ExpoCENFO visitor access and its university-only VisionRover contest are separate records. CENFOTEC Makers has exact December days but starts at age 10; Mexican holiday candidates lack confirmed teaching language and daily dates. No unknown dates were inserted into calendars.


Taiwan v15 (2026-10-01): 37 local cards (22 competition categories / pathways, 9 events, 6 learning programmes), 17 additions. Two explicit English winter2027 camps; grade / foreign entry gates and conflicting TIRT / GRG rules remain visible. Direct route overview: `#taiwan`; full local export: `downloads/STEM_Taiwan.json` / `.md`. New camp calendars use actual teaching days; weekends are excluded. Worldwide coverage remains unfinished.

Local v16 (2026-10-01): 1081 records / 806 competition cards / 129 events / 146 learning programmes. Added 11 dated Mexican FTC regionals and their national final, two younger on-site TecPro disciplines, and four undated virtual Match 2 categories. FTC currently excludes both children as competitors; spectator access remains unconfirmed. Codey Rocky uses Jan 1 eligibility, not current age. Two camp ES tags were removed because teaching language is unpublished. Local route overview: `#local`; export: `downloads/STEM_CostaRica_Mexico.json` / `.md`. All 1063 previous IDs, 62 profiles, 46 routes, and the 37 Taiwan cards remain. Both children can learn full-day on EN / ES; exact birthdays and school grades remain unknown.

The browser family ICS now applies the same future-date cutoff as the static family ICS. Direct hash navigation between `#local`, `#taiwan`, and the existing views rerenders without requiring a reload.

South America v17 (2026-10-01): primary local LNR calendars add all 10 visible future zonal / PRE SEDE / final records, with an independently read league and team rule guide. Chile OPEN relocation and Puerto Montt dates are resolved with visible conflicts. Programable has two age tracks and 30 actual teaching days each; Troonic has two announced 4-day windows with schedule conflicts. Historical or sold-out Colombia / Peru programmes remain distinct. Website-only ES tags were removed from two existing camps; the explicit ES Umake programme is historical. Direct overview: `#southamerica`; exports: `downloads/STEM_South_America.json` / `.md`. All prior 1081 cards, 62 profiles, 46 routes, Taiwan and CR/MX focus and family EN / ES context remain. Worldwide research remains unfinished.


South America v18 adds 33 primary-source records for Brazil, Uruguay, Paraguay and Bolivia and four league profiles. Visitor admission, closed championship entries, school-grade rules, and new camp cohorts remain distinct. This work is carried forward into the v19 publication.

Camps v19 (2026-10-01): 1170 catalog records, including 194 learning / camp / workshop records (29 additions), 845 competition records (6 additions), and 131 events. There are 67 league profiles, 46 legacy routes and 78 curated major-exhibition / family-alternative cards. The new `#camps` view includes day / boarding filters, primary technical language vs second-language assistance vs language lessons, six family routes, nine curated project / hackathon records, and explicit research gaps. Course language roles are freshly classified for only part of the inventory; legacy EN / ES tags do not automatically establish English-medium instruction.

Published camp windows and announced contest starts are distinct from daily teaching or submission deadlines. `date_scope=activity_start` exports a one-day reminder for an announced beginning; the unknown full period remains explicit. Winter windows do not promise every holiday / weekend or every track at every campus. The regenerated family ICS contains 939 upcoming, non-excluded dates / deadlines; static and browser UID / date values are matched. Public source retrieval receipts are in `data/camps-source-receipts-v19.json`; HTTP 200 alone does not establish relevant content, instruction language or family admission. The focused guide and exports are `data/camps-audit-v19.json` and `downloads/STEM_camps.json` / `.md`. No worldwide completeness is claimed and no registration, communication or payment is performed.

Schools v20 (2026-10-01): a separate `schools` collection and `#schools` view add 16 permanent-school profiles across 13 countries / six continents. Five public, eleven private / industry-network schools; three boarding providers with separate minimums; five profiles with literally stated world-stage results, two backed by FIRST organizer records. Fourteen result entries distinguish divisions, judged awards, national placements and participation. Seven programme-only candidates have no established wins. IB candidates, school-reported authorisation and read IB registry records remain distinct. The English language of a website or of Diploma does not establish junior / team instruction. Day age candidates are not admissions approval or competition-team acceptance.

School exports: `STEM_schools.json`, `.csv`, `.md`, `STEM_school_country_coverage.csv`, and separate `schools`, `school_results`, `school_sources` tables in the full SQLite database. The country directory has 249 explicit school-coverage statuses; zero countries are fully audited. Public retrieval receipts are in `data/schools-source-receipts-v20.json` and are distinct from browser-read evidence and admissions confirmation. All 1170 event objects, 67 profiles, 46 routes, family context, camp/local/Taiwan/South America data and calendar UID/date values are preserved.

The project research plan includes permanent schools and the competition retrospective. A fresh native Goal receipt on 2026-10-01 shows active. The original worldwide objective continues; this bounded research pass does not complete it.

School retrospective v21 (2026-10-01): `school_history` stores 116 award entries and 87 school / community / mixed / unresolved entities. All 44 FRC Championship Winner entries and 11 main Chairman / Impact winners from the 11 played Championship venue events in 2017–2019 / 2022–2026 were read from FIRST. The counts are distinct winning seasons inside FRC: Madera 4 (recent five: 3), Bellarmine 3 (1), Atascadero 2 (0), Burlingame 2 (1). Two Championship venues in 2017–2019 are literal venue titles; Festival of Champions 2017 is outside this series. COVID 2020 / 2021 match cancellations and the 2021 awards-only format remain distinct.

WRO adds 28 exact first places across seven selected RM / FI / FE categories for 2022–2025; RoboSports, all medals and school affiliations are incomplete. VEX, FLL and WAICY have sourced recent cases, with protocol / participant-report provenance. Worlds divisions, national / state awards, qualifications and unclassified marketing titles do not inflate the match-win count. FLL, FTC, RoboCupJunior and all-age VEX / early WRO archives remain partial. No global commercial school ranking is asserted.

School catalogue: 21 dossiers in 14 countries; additions Madera, Atascadero, Burlingame, AST Taichung and Misk Schools. Retrospective UI in `#schools`: five / ten year switch, repeat-FRC timeline, league / entity / award / query filters, source-linked results, coverage matrix and age-specific family routes. Export `STEM_school_history.json`, `.csv`, `.md`; SQLite `history_entities` and `history_results` preserve source and school foreign keys. Hash receipts document 15 organizer pages, independently of participant reports. Existing 1170 event records, league / route / family / camp data and calendar dates / UIDs remain unchanged.

Junior projects v22 (2026-10-01): 1177 event records / 70 league and programme profiles. Seven additions comprise two milestones of the same Global Appathon, G4C Student Challenge, two self-paced Astro Pi educational tasks, facilitator Game Jam resources and general FOSDEM 2027 dates. 197 camp / learning records include self-paced resources and are not 197 bookable holiday camps. New family project panel on #leagues distinguishes age candidates, conditional elementary / foreign entry, geographic exclusion and educational certificates. EN submission requirements are explicit for Appathon; ES video requires EN captions. Adult authorship must be declared; current Adult / All-Ages and technical judging conflicts remain visible. March 30 G4C listing is not a labelled deadline; old awards are not projected onto new elementary rules. FOSDEM Junior 2027 is unannounced.

Exports STEM_junior_projects.json / .md and project_focus SQLite metadata share catalog.json. registration_open and submission_open are one-day calendar reminders; Appathon deadline April 2 23:59 AOE is April 3 11:59 UTC / 05:59 Costa Rica. Family ICS now has 943 dates / deadlines, including four additions; Astro Pi P4 is excluded. The 1170 prior event objects, 21 school dossiers and 116 history entries remain. No country is fully audited.

Family strategy v23 (2026-10-01): seven conditional bases (Taiwan, Mexico, Panama, USA, Costa Rica, Brazil, Russia), two child-specific routes, three learning tracks, four horizons and a 90-day decision sequence. Recommendations are editorial and distinct from official programme / admission facts. Added ISP Panama S022 as a programme candidate; grades 3–12 VEX is not extended to Oscar without eligibility. 22 school dossiers in 15 countries; no additional event cards or historical medals. Existing 1177 events, 70 league profiles and 116 historical results preserved. Public strategy omits specific family migration statuses. #strategy supports child / country / horizon switches and source-linked school dossiers. Export STEM_family_strategy.md / .json and SQLite metadata. FIRST K–8 transition from 2027 and conditional sibling WRO 2028–29 calculation remain explicit. School / team places, budgets, exact grades and migration eligibility unresolved.

Asia v24 (2026-10-01): 27 additions, 1204 event records / 71 profiles. Five dated Japanese EN camp cohorts (four TCC day shifts5–12, Harrow Appi residential9–13), two Coding Lab regular EN tracks; current Avishkaar2026 categories / rules and eight zonals; provisional Delhi finale stays undated; seven FLL India2027 host windows visually read from organiser images. Avishkaar deadline / current-page conflicts and FLL Sept30 closure remain explicit; no foreign admission is assumed. Explora2026 programmes remain historical; Panama2027 / Korea junior EN camps not established. 22 schools, 116 historical results, seven family bases and prior event IDs preserved. Research stays active and incomplete; no applications or messages sent.

Family bases v25 (2026-10-01): refined comparison after mobility context; Mexico / Taiwan first, USA a current candidate when family business and a junior team align, Panama reserve, Costa Rica continuity, Brazil / Russia specialist routes. Three interactive scenarios and published 2026–27 two-child cost calculations for ASFM / TAS / ISP distinguish tuition, one-time fees and staged capital obligations. 2027–28 prices, places and individual migration eligibility remain unconfirmed. Exact family immigration statuses / passport combinations are omitted from the public site. Existing 1204 events, 71 profiles, 22 schools, 116 history entries and 969 family calendar items are preserved; worldwide research stays active.

Kazakhstan / Russian v26 (2026-10-01): Russian added to family language context and filters, with instruction evidence kept separate from Russian documents. 19 new cards (18 Kazakhstan, one Taipei RGT), 4 programme profiles; 1223 records / 75 profiles. Fresh RGT organiser announces Astana March 3–4 and Taipei May 29–30 2027; age rules still pending. WRO Elementary 8–12 and local Explore 6–10 / Challenge 10–16 are local-season evidence. RoboBalapan preschool gates, RoboLand junior/history distinction, KazRoboSport / Project and TechCup stale-source issues remain explicit. Kazakhstan overview on #leagues, table country shortcut, Markdown / JSON exports. Existing 1204 event objects, 22 schools, 116 results, 969 calendar items preserved; two announced RGT windows added. No RU instruction camp, foreign admission, school place or full national coverage inferred.

Family top picks v27 (2026-10-01): 23 evidence-linked editorial choices: 7 schools, 6 leagues, 6 camp programmes, 4 exhibitions. New #best supports category, child, horizon and search; badges and recommendation-only filters also appear in the full lists. Programme/age candidates are distinct from bookings and school/team admission; future secondary and 10+ camps stay separate. Existing 1223 events, 75 profiles, 22 school objects, 116 historical results and both calendar memberships preserved. No global rank or measured teaching quality claimed; research remains active. Export STEM_top_picks.json / .md and SQLite metadata.

World / Caribbean v28 (2026-10-01): 27 new records bring the catalog to 1250 (902 competition, 138 event, 210 camp / learning records), with 85 league / programme profiles and records in 70 countries. RoboNation 2027 dates remain older technical pathways; DOM local Explore 6–9 and Challenge 9–15 do not establish foreign-team acceptance. Barbados historical camps and stale CoderZ / iD Tech Global Academies pages retain unknown future dates and eligibility gates. CodeAI self-paced EN / ES materials have their own language-role filter and are not counted as live technical instruction. Prior 1223 event objects, 22 schools, 116 history records, 23 top picks and existing calendar entries are preserved; only three newly dated public online events join the family ICS (974 entries; major-exhibition ICS remains 65). Zero countries are fully audited.

South Asia v31 (2026-10-01): 20 primary-source additions bring the inventory to 1317 records (927 competition, 142 event, 248 camp / learning records), with 95 league / programme profiles and records in 75 countries. Four national profiles cover WRO India, WRO Pakistan, WRO Sri Lanka and Bangladesh Robot Olympiad. Junior grades, foreign applications, local-school eligibility, non-qualifying quizzes, archived summer dates and mixed Hindi / English instruction remain explicit. M.E.E.T.I.'s general foreign-student application differs from its government-school scholarship. BBT mechanical robotics starts at 6; its AI / entrepreneurship tracks start at 12. The only new exact future teaching day is the Grade4–12 Dhaka CAD workshop on October9, with an October6 deadline; foreign entry, English and the family's grade are unconfirmed. The family ICS has 1002 entries; the major-exhibition ICS remains69. All1297 prior event objects,91 prior profiles,25 school dossiers,116 history results,23 top picks, the Europe guide and prior calendar contents are preserved. Worldwide research stays active and incomplete; no applications, messages or payments were made.

Europe second pass v32 (2026-10-01): 29 new cards, one French junior profile, three school dossiers; 1,346 cards, 96 profiles, 28 schools. La Garenne camp windows are separate from its short 8–12 technical option; the six-year-old remains below that option in summer 2027. Swiss family workshops, Yverdon weekday conflict, EPFL 11–13, Spanish Start/Rookie versus nonofficial Training, French Discovery without ranking/world qualification, grade-gated AI and professional Advanced Factories access are explicit. Older world inventory is preserved except the documented L002 age correction and Spanish WRO profile expansion. School regional results are labelled separately from world awards. Current Europe view includes trial cities, prices/technical duration and the evidence needed to select a mentor. World research remains active and partial.

Northern Europe v34 (2026-10-01): 52 additions: 39 competition pathways / stages, seven learning programmes / sessions, six exhibitions / visits. The inventory is now 1,398 cards (970 competition,151 event,277 learning),102 profiles,29 schools in16 countries. The dedicated `#europe-north` guide compares Germany / Netherlands / Belgium and exports `STEM_Europe_DEU_NLD_BEL.json` / `.md`; the previous `#europe` guide remains unchanged. Fifteen published NL regional Challenge days and the Wageningen final, eight Belgian regional days and BeLux final, DACH final and German Junior Finale are separate from open foreign admission and world quotas. Future5+ has no official closing events this season and is classified as regular learning. English teaching / bilingual teaching / English assistance / English exhibit information stay distinct. ISD Düsseldorf is an English curriculum candidate with programme evidence, not an established world-winning school. German WRO final remains provisional and undated; unannounced2027camp cohorts are not assigned dates. Public gamescom2027dates are26–29August. Earlier event / profile / school / result / recommendation / CHE-ESP-FRA content is preserved except four explicit date / language refreshes; all1011 prior family calendar UIDs remain, with only three source-check dates refreshed. Family calendar total1051; major-expo calendar72. World coverage remains active and partial.

Europe junior third pass v35 (2026-10-01): 30 additions, one Swiss FIRST junior profile and one Paris school dossier; 1,428 records / 103 profiles / 30 schools. Swiss foreign event participation is distinct from domestic qualification; Alpine VEX explicitly excludes non-Swiss teams. Actual TechSpark Game Design dates are not transferred onto the general LEGO robotics course. TechLabs English assistance differs from bilingual teaching, with age and waiting-list conflicts visible. Ecolint has an October 19–23 robotics shift for younger children. Union Academy admits external pupils in English, with 45 / 90 minutes of coding inside broader Wednesday packages; no world-winning school result is inferred. ASTI secondary categories remain excluded for both boys. Smart City Expo child exceptions require confirmation; Coupe2027 contest dates do not establish public visitor days. Family ICS has1070 entries: one explicit national restriction removesC549, while1050 previous UIDs remain; C909 deadline text is corrected. Major exhibition ICS has73 entries. Prior29schools,116history records,23top picks and northern-Europe guide preserved. Mobile school route wrapping fixed. World coverage remains partial.


Version 36 adds a bounded Italy/Portugal pass: 65 cards, 5 league/programme profiles and 2 school dossiers. The new `#europe-south` comparison separates verified EN technical instruction from English lessons with Italian robotics, provisional junior eligibility from actual admission, and archived summer programmes from upcoming dates. The existing CHE/ESP/FRA and northern Europe views remain available. Worldwide coverage is partial.

Europe v38 (2026-10-02): deeper CHE / ESP / FRA adds 38 event/programme cards, 6 league/programme profiles, 4 primary-school dossiers and 2 precisely scoped school-reported awards. Country totals: Switzerland 74, Spain 47, France 50. Two global programme-transition cards have no local event dates. TechLabs four regular courses explicitly EN/DE, Oscar below their minimums; Nube7 teacher language ability remains support. La Miranda English mixed camp has age/birth-year conflicts. Eight dated Mini-Robots sessions belong to one operator; French technical EN/ES not established and excluded from family ICS. School results retain exact grade and stage, with explicit unresolved-stage and school-network labels. FLL 2026/27 final season and distinct LEGO / FIRST hardware plans shape the 2027–2029 route. No registration or world-completeness claim. Source receipts: data/europe-deep-source-receipts-v38.json. European comparison and downloads: #europe.

Europe decisions v39 (2026-10-02): three family scenarios (Spanish permanent team, Paris bilingual trial, Swiss EN/DE VEX), a five-year age forecast, and mentor-selection evidence in #europe and exported reports. Three additional French learning cards bring the catalog to1576 / CHE74 ESP47 FRA53. WRO Switzerland refundable general2026 fee versus free Starter claim is explicit, as is one-team-per-season participation. New French camp / club EN/ES remains unconfirmed and outside the family ICS. Existing world records,36 schools,118 history results and23 top picks preserved. Future age routes are forecasts, not tournament dates or confirmed admissions; world coverage remains partial.

Europe evidence v40 (2026-10-02): CHE / ESP / FRA now have 185 records (76 / 50 / 59), 16 regional school dossiers and five interactive evidence cards. Adds 7 regular programmes and 4 dated French camp sessions, TASIS and Marymount dossiers, and 8 bounded 2025/26 team results. RoboRAVE Craon Primary access is conditional on host school-stage/local rules, not age alone. Tech Kids EN regular courses remain distinct from its French-language holiday camp; TECNISTEM and Robo Matik age conflicts remain visible. Catalog: 1,587 records; 120 league profiles, 38 schools and 126 history results. Both prior calendars retain their UID sets (1,131 family / 87 major exhibition entries). Worldwide research remains active and partial.

Africa v41 (2026-10-02), carried into v42: 29 primary-source additions, five national/programme profiles, two school dossiers and five scoped results. The new #africa guide covers Kenya, Ghana, Nigeria, Rwanda, South Africa and Morocco. National placements and school-unresolved Ghana world awards stay distinct. English instruction is explicit for selected Rwanda courses, not inferred for Ghana camps or Kenyan schools. Nigeria 2027 professional expos retain unconfirmed child admission. Archived and broad holiday windows do not become future daily camps. Source receipts and partial country exports are preserved.

Europe family v42 (2026-10-02): nine additional learning records, St George Barcelona school dossier, two exact Swiss national placements and six refreshed competition/expo policies. CHE / ESP / FRA: 194 records (76 / 58 / 60), 17 school dossiers. Three interactive base comparisons separate each child's route, school evidence, conditional two-child costs and trial plans. Swiss Starter has no international quota; too-young local exceptions cannot qualify internationally. Spanish WRO permits independent 2–3-child teams, with local entry closing 15 days before or earlier at capacity. St George's English robotics camp is a 2026 archive; no 2027 dates are inferred. PetitUnivers February2027 English lessons do not establish English technical instruction. SIDO September15–16,2027 moves to Eurexpo and stays adult-only under the last published rules. Its date remains in the major-exhibition calendar and is removed from the family calendar.

Inventory: 1,625 records, 125 league/programme profiles, 41 schools, 133 historical results. Family calendar: 1,136 entries; four old entries expired at the October2 cutoff, SIDO was removed, ten Africa dates/deadlines were added. Major-exhibition calendar: 89 entries, retaining all 87 prior entries. Existing recommendations, previous regional guides and research objective are preserved. Source gaps, foreign/team admission, exact birthdays/grades and undisclosed 2027 cohorts remain explicit. Worldwide research stays active and partial; no country is labelled fully audited.


### Middle East primary-source pass · v43

Added33cards (20competition /9learning /4visit),4national profiles and2school dossiers for UAE,Oman,Qatar and Saudi Arabia. The four-country view is `#middleeast`; JSON /Markdown /SQLite exports include it. The inventory now has1658cards,129profiles,43schools and135bounded historical results. All earlier regional routes and records are retained except the four explicitly rechecked Gulf rows.

Qatar2026PDF amendments narrow junior ages and hardware relative to the broad overview. Qatar Discovery/Explore/FLL require at least half the team to be Qatari. OmanKids6–9 has no World Final qualification. UAE JIC is school-nominated and2026registration is closed. SISD English Primary STEAM is a school programme; Cheltenham Grade9national WRO award is not a world win or an elementary-family guarantee.

Current FunRobotics EN/AR, LaFolie staff language support and unconfirmed technical instruction are separated. Past2026summer/spring cohorts stay archived; no future dates inferred. WebSummit Qatar local18+ overrides a generic conditional youth clause until a Qatar exception is confirmed. LEAP published18+ is retained; Museum of the Future is a separate family alternative. The family ICS has1139entries and the major-exhibition ICS92; all previous family UID dates are preserved.

Read receipts: `data/middleeast-source-receipts-v43.json`; source migrations: `scripts/expand-middleeast-v43.py`, followed by `scripts/polish-middleeast-v43.py` and `scripts/build-database.py`. Anonymous browser checks cover33new/4updated dialogs, four national profiles, school/history links, language roles, visitor gates, downloads, prior regional views and mobile widths320/390. Query blur no longer rerenders school-history rows and discards the first click on age evidence. World coverage remains partial:80countries/territories with records,249in inventory,0fully audited.

Europe practical v44 (2026-10-02): CHE / ESP / FRA now have 202 cards (78 / 60 / 64) and 18 school dossiers. Eight additions distinguish actual EN primary-year groups in Pamplona, two 2027 Leysin residential candidates starting at age 10, two French workshops with unconfirmed technical EN / ES, and two Toulouse-area family events. ISL adds a precisely labelled national teen VEX Skills second place, school-reported Worlds participation without a world title, and a 2026/27 fee calculation; junior team access remains unconfirmed. Three league profiles are refreshed, including the FIRST K–8 transition after 2026/27. Previous other-region routes, schools, history and all calendar UID/date pairs are preserved; the two family events are the only calendar additions. Inventory: 1666 records / 129 profiles / 44 schools / 136 history results. Source receipts: data/europe-practical-source-receipts-v44.json. Worldwide coverage remains partial and active. No enrolment, external messages or payments.

Europe v45 (2026-10-02): the ninth bounded Switzerland / Spain / France pass adds 23 cards: 12 public Swiss FLL venue/division dates at seven locations, Jaén and three French 2027 stages, five learning/workshop candidates and two free family festivals. The catalogue contains 1,689 records, 130 league profiles, 46 school dossiers and 136 unchanged history results; the three-country comparison covers 225 cards and 20 schools. A dated season route is available in `#europe`. LIFE and public Ciudad de Nejapa in Tres Cantos have programme evidence, not verified junior world titles. LIFE uses an American Christian English curriculum; its archived English VEX EXP camp starts at age 10. Nantes locally requires FLL ages 11–16 despite the national 9–16 FAQ. Swiss judging/Starter languages, Explore age 6–9 versus 6–10, and Future 5+ hardware conflicts remain explicit. At Home placeholders are excluded; Jura Challenge and Yverdon Explore were full on the public snapshot. Exact birthdays/grades, current team admission and foreign world quotas remain unconfirmed. All unrelated prior records, school dossiers, history and regional routes are preserved. The family calendar has 1,164 entries and the exhibition calendar 96; language-unconfirmed French learning programmes do not become confirmed family camp dates. Worldwide research remains active and partial.


Europe family choices v46 (2026-10-02): 11 new cards, two school dossiers and one new world finalist. The three-country view now contains 236 records (CHE 97 / ESP 64 / FRA 75), 22 school dossiers and nine filterable family choices. Cosmo Nyon dates for 2027 retain unknown technical language and camp-specific age; TecnoCamp and Costa Blanca remain future candidates. ICS Paris Primary is English 6–11, while its FabLab is Grades 6–9 and AI Startup is Grades 6–12. ASV Valencia has verified English ASV+ and a conditional two-child 2026/27 cost example. FIRST now directly supports ROBOTECH Champion’s Award Winner 2026 and mindfactory Champion’s Award Finalist; their schools are unresolved. TechSpark LEGO Junior remains undated because it is absent from the dated menus. Inventory: 1700 cards / 130 profiles / 48 schools / 137 history results. All earlier calendar UID/date pairs, unrelated regions and family context are preserved. No applications, external messages or payments. Worldwide coverage remains active and partial.

Europe deeper v47 (2026-10-02): 12 new cards, EISB Cambridge Primary dossier, updated Aiglon junior language evidence, and 9 precisely scoped 2025/26 results. Database: 1,712 records, 130 profiles, 49 schools, 146 history results; CHE / ESP / FRA 102 / 68 / 78 cards and 23 schools. HIF has two real English residential sessions in July2027, minimum10 at the start; exact birthday remains a gate. Aiglon robotics minimum8 differs from overall daycamp7. EISB Science explicitly EN; Chess & Robotics language unknown, published summer birth2012–2019 excludes Oscar2020. Old2026 prices are not reused for2027. MJC8–11 workshop differs from its12+ competition team; official Occitanie March27,2027 overrides club April copy. FIRST2025 RobotPerformance2/3 are read from original HTML ordinals. ROBOTECH is an independent mixed-school team. AdvancedManufacturingMadrid requires over16, SwissAISummit generally18+; separate VivaTech June19,2027 publicday keeps child-ticket uncertainty, SIAMS April4–7,2028 also needs child-access confirmation. All older data and world scope are preserved except explicit E102 family-feed replacement by E184 and C918 source clarification. Worldwide coverage remains active and partial.


Singapore / Hong Kong v48 (2026-10-02): 43 new cards (18 competition tracks / stages, 22 learning cohorts / programmes and 3 exhibitions), four profiles, AIS Hong Kong and Singapore American School dossiers, and four exactly scoped results. The dedicated `#asia-english` guide has six filterable family choices, four season clusters and six evidence comparisons; JSON / Markdown / SQLite exports include it. Inventory: 1,755 cards, 134 profiles, 51 schools, 150 historical results. Singapore 94 cards, Hong Kong 27. Four actual October weeks × five Worklab tracks have explicit English instruction; Cobo language is also explicit. Computhink 22 existing November / December cohorts keep their dates but lose unverified English-instruction tags. FLL Singapore class gates, Overseas awards without Singapore World Festival qualification, separate NRC / WRO organisers, and Hong Kong remote school-grade / foreign-entry uncertainty are explicit. AIS regional / internal VEX GO is separate from world titles; SAS pipeline does not establish elementary world awards. GITEX AI Asia is strictly over18; ITAP child admission remains unconfirmed; InnoCarnival is a free family event. Current full school fees / places are unconfirmed. Migrations: `scripts/deepen-asia-english-v48.py`, then `scripts/polish-asia-english-v48.py`, then `scripts/build-database.py`. Source receipts: `data/asia-english-source-receipts-v48.json`. All previous regional guides, family strategy, schools, profiles, history and calendar UID/date pairs preserved. Family calendar 1,201 entries, major exhibition calendar 104. Worldwide research remains active and partial. No enrolment, applications, external messages or payments.

Europe family fit v49 (2026-10-02): the requested CHE/ESP/FRA follow-up adds four learning records and one Rosenberg Primary dossier. The Europe view switches between season-long competition, a two-child trial and English-school scenarios, with a 2026–2038 skills route. Rosenberg school EN / junior courses are verified after rendering; camp technical language, chosen weeks and junior boarding remain unconfirmed. Tech Kids 5–6 Niveau2 is bilingual,7–9 Niveau2 is FR-only. All earlier1755 cards,51 schools,134 profiles and150 results remain unchanged; no calendar dates are invented. Data totals1759 cards /52 schools, with world coverage still partial.

Mexico / Costa Rica junior family pass v50 (2026-10-02): adds 14 cards and three national / regional league dossiers. Local family choices, FLL formal teams and 2026/27 direct National exception, WRO junior calendar-year gates and LATI student-only pits are explicit. LATI 2026 Sumo limits conflict with the linked 2025 PDF; the first day is October 9, the new-team October 4 deadline is derived, and the second jornada is undated. Closed Robotifest competition registration leaves the family calendar; CENFOTEC10–12 remains excluded for both. Regular Ciberbots courses do not establish holiday ages or language. All1759 preceding records retained with13explicit updates;134 preceding profiles,52 schools,150 history results and European scenarios preserved. Totals1773 cards /137 profiles; world coverage remains partial.


East Asia v51 (2026-10-02): a bounded Japan / mainland China / Taiwan pass adds 21 cards (11 FIRST Japan stages / paths and 10 learning programmes), 3 programme profiles, 10 permanent-school dossiers and 2 precisely scoped school-reported YK Pao awards. The inventory is now 1,794 cards (1,143 competition / 188 event / 463 learning), 140 profiles, 62 schools and 152 history records. The new #eastasia guide has three family scenarios, eight filterable choices, country comparisons and a 2026–2038 development route; JSON and Markdown exports retain sources and conditions. EN instruction is distinguished from assistance, bilingual teaching and unconfirmed camp language. Past 2026 summer cohorts do not acquire invented 2027 dates. Harrow Appi school 11+ differs from winter camp 9+; Hengqin boarding 8+ is bilingual; Morrison dorm is a later high-school route with a prior-study requirement. Japan VEX National C537 requires genuine domestic team activity and has conflicting header/body dates; its dated calendar entry is removed pending confirmation. Family ICS has 1,218 entries (1,205 prior UID/date pairs preserved plus 13 new entries); the major-expo calendar remains 104. All prior 52 schools, 137 profiles, 150 results and seven regional guides are preserved. Shared scenario routing and narrow-screen link wrapping are verified at 390/320px. Worldwide coverage remains partial and active; no school enrolment, coach place, foreign admission or world-ranking claim is inferred. Source receipts: data/east-asia-source-receipts-v51.json.

Camp scope extension (2026-10-04): the active research plan now covers leading general and themed camps worldwide for all2026–2027holiday seasons, with a complete Switzerland discovery pass, day / residential tracks, programme-specific languages and age gates, evidence-based editorial comparisons and full per-child / family cost models. Requirements and discovery leads live in `data/camp-programme-expansion.json`; public snapshots are `STEM_camp_scope_2026_2027.json` and `STEM_research_plan.json`. The shared Swiss chat is discovery input, not verified rules; Camp Montana example was independently checked against three primary pages. No camp research completion, accepted application, vacancy or overall world ranking is inferred. Existing research records, all other downloads and planning / motion behavior are unchanged.


Camps v54 (2026-10-04): a separate detailed programme guide adds 50 operator/programme dossiers in 17 countries, including 13 Swiss operators and 78 unique official source URLs. The 2026/2027 season, exact 2027 dates, partially published 2027 programmes, 2026 history, and unannounced next cohorts are distinct. Programme content, technical versus general activity, age/class thresholds, language roles, day/boarding access, original-currency fees, extras, deposits and unanswered admissions questions are presented independently. Editorial shortlists express family suitability and disclosed programme content, not a global quality ranking or a guarantee of admission.

`data/camp-programmes-deep-2026-2027.json` is authored by `scripts/deepen-camp-programmes-v54.py`; matching JSON and a detailed Markdown report are published under `dist/downloads/STEM_camp_programmes_deep_2026_2027.*`. The independent `dist/assets/camp-programmes.js` / `.css` panel on `#camps` provides seven scoped filters, five family scenarios, up-to-four dossier comparisons, published-date overview and direct dossier URLs. It does not rewrite event objects, existing camp learning cards, school/history records, or calendar IDs. Legacy shared controls move into the collapsible previous camp inventory while this view is open and return above the catalogue in other views.

The dossier guide is not a complete worldwide camp directory. Brazil NR and UBC Geering Up could not be verified from current live programme bodies; Korea's internal school trips are not counted as public camps. Unpublished prices, English instruction, exact birthdays/classes, and availability remain explicit questions. No applications, payments or organiser messages have been made. Existing original catalog and camp exports are preserved. The worldwide research goal remains active.


Camp integration v55 (2026-10-04): the detailed guide now has 54 dossiers in 19 countries, including 14 Swiss dossiers and 88 unique official URLs. Village Camps Leysin (Junior versus STEM), Zell am See and Santa Cruz are individually sourced; the UBC Geering Up FAQ was read through the web reader while direct retrieval still returned the browser-verification wrapper. Its 2026 grade/curriculum rules and no-overnight policy are documented; 2027 dates, fees and EN remain unknown.

`scripts/camp_catalog_bridge.py` runs inside `build-database.py`. It embeds the detailed guide as `camp_programmes` in the canonical catalogue, browser data and portable full database, and adds relational SQLite tables `camp_programmes`, `camp_programme_sources`, `camp_programme_events`. An explicit whitelist links existing programme IDs; related operator/track links do not assert the same course or eligibility. There are 97 new published-session cards, seven reused legacy event IDs, and six broad season windows that produce no new session cards. General camp stays do not inherit robotics/coding/AI theme tags merely because a paid or age-restricted workshop is offered. Family Aviation is a parent-accompanied residential programme. The 1,794 original event objects, league profiles, routes, school/history data and family context stay unchanged. New dates join the shared calendar, catalogue, country map and exports.

The dossier guide uses the same embedded canonical data with a standalone JSON fallback, a country overview map with keyboard-accessible equivalent buttons, and direct links from catalogue cards and modals. The country map does not claim exact campus positions. The world-wide research goal stays active. Run the dossier authoring script before `build-database.py` when modifying dossiers.

Exact Swiss variants v55: Les Elfes has six summer sessions, nineteen separately published winter weeks and its May 2027 spring session, each with its base fee and correct seasonal content; My Family has two/three-week alternatives with explicit venue and age. Le Rosey homepage repeats contradictory My Family three-week prices (CHF 13,200 / 13,500); the programme page says CHF 13,200 including a non-refundable deposit. The conflict stays visible. These are base tariffs, not promised final totals or available places.

Swiss camps v56 (2026-10-04): three separate Régent tracks and JFK Swiss Outdoor Camp bring the guide to 58 programme dossiers in 19 countries, including 18 Swiss programme dossiers (not 18 distinct operators), and 96 official URLs. Régent Labs 8–14 is a Matvey candidate; Leadership 13–16 and Pre-University 15–17 remain future tracks. FAQ establishes English camp life while specific STEM instruction and 2027 financial conditions still need confirmation; enrolment cancellation dates are still 2026. Pocket money and the unresolved inclusion of the CHF 1,000 application fee are explicit.

JFK includes published 2027 day/boarding fees, exact November 2 registration opening, and 30 alternative one/two/three-week options computed from the public weekly rule. Day windows are labelled Monday–Friday and exclude weekends from attendance; boarding runs Sunday–Sunday. Current live PDF was downloaded, hashed and visually read on both pages: its tariffs match live HTML. An older web-reader extraction returned different prices/transfers/refund terms and was rejected for current values. Liability insurance still conflicts between admissions HTML and the current PDF; camp-specific EN and the security deposit amount remain unknown. No account, form, booking, message or payment was submitted. All 1,891 v55 event objects and previous calendar UID/date pairs are preserved.

France/Spain camp pass v57 (2026-10-04): 10 new detailed programme dossiers plus deeper ILC, American Village and Camp Tecnológico evidence bring the guide to 68 dossiers in 19 countries, with 122 official URLs. Ermitage and Wander offer future holiday dates; IH has nine dated autumn/winter/spring city-specific cards. Campuses on identical dates retain distinct stable IDs and the detailed calendar uses those variants. All 1,931 prior event objects and 1,315 prior family-calendar UID/date pairs are preserved; 21 added calendar entries yield 1,952 events and 1,336 family ICS entries. The 18 Swiss dossiers and prior competition/exhibition/school blocks remain intact.

Fresh-source conflicts remain explicit: IH live summer row is still 2026 despite academic2026/27 tariff headings and a conflicting cached2027 extraction; no new summer2027 event was inferred. Wander's spring2017 typo is excluded. ILC/TECS yearless tariff/date tables stay undated. SIS and King's title2026/2027 does not replace body2026 dates; age boundaries differ for day/boarding/STEAM. The Wizard School2026 card is closed. Rockbotic's unrelated blog spam was ignored; the clean official closed event card provides historical context only. No form, booking, message, account or payment was submitted. This is progress on an active worldwide goal, not complete world coverage or promised admission.

Asia camp pass v58 (2026-10-04): 10 new programme dossiers (four Camp Asia tracks, two separate Taiwanese operators/formats, two Japanese programmes and two LCCL junior tracks), plus refreshed Camp Taiwan and Camp SFS conditions. The detailed guide now has 78 dossiers in 19 countries, including 18 Swiss dossiers and 140 official URLs. Seventeen future dated entries bring the database to 1,969 records and family ICS to 1,353; all 1,952 earlier event objects and 1,336 earlier UID/date pairs remain intact. Camp Asia October robotics is only6–8, LCCL ages conflict with its portal, Camp Taiwan family dates conflict, Camping Taiwan requires completedGrade1, Hakuba means grades6–9 and English Adventure winter has an explicit 2020birthday cutoff. Unknown teaching language remains outside confirmed EN filters. Source receipts and bounded audit are downloadable; worldwide scope stays active and incomplete.

Americas camp pass v110 (2026-10-06): 17 new programme dossiers across seven operators and 28 dated camp rows bring the guide to 815 dossiers in 39 countries and the catalogue to 3,376 records. All 798 previous dossier objects and 3,348 previous event objects/IDs are retained unchanged. Five new two-child estimates join the nine existing estimates: Arca with/without food, Cacao, Houston and Perot. A sibling package total is a package, not a fabricated individual price; travel and unanswered mandatory charges remain unknown. The complete SQLite and JSON archives contain all records, with hashes and README; raw files exceeding the hosting file limit are omitted without truncating the databases.

Houston age groups/dated themes are separate, and all Explorer programmes are day/evening rather than boarding. KSC 2026 is sold out and its unpublished 2027 is not inferred. Arca's current October HTML overrides stale September search extracts; English, Christian content and the two-sibling package are explicit. Cacao's January dates conflict with its weekday copy; its calendar records an attendance-to-confirm range, not invented individual days. Berkana's winter year/duration and summer week/format prices require clarification. RF's January2026 course is archived; CPIC professional workshops and MountView school-group trips are not presumed open child camps. None of the countries or the world is claimed fully audited; permanent schools, competition history, leagues, exhibitions and family routes remain within the active worldwide objective.

Reproduce this data pass with `python3 scripts/deepen-camp-programmes-v54.py`, then `python3 scripts/build-database.py`, then `python3 scripts/finalize-americas-camps-v110.py`. Its independent verification is `python3 scripts/verify-americas-camps-v110.py`. Native publication, source snapshots, archived payload checks and the offline functional check are separate private receipts. No applications, consents, messages, accounts, bookings, payments or recurring schedules were created.
# Проверка европейских программ v111 · 6 октября 2026

Добавлены 12 досье программ пяти организаторов во Франции, Швейцарии,
Испании, Великобритании и Ирландии. Это возрастные и форматные варианты,
а не двенадцать независимых лагерей и не объективный мировой рейтинг.
Первичные страницы, три афиши и выбранные страницы двух PDF проверены.
Подтверждённые даты: 43 новых строки календаря; все 3376 прежних записей
и 815 прежних досье сохранены без изменений.

Обновлённый реестр: 827 досье в 39 странах, 3419 карточек, 17 семейных
смет. Новые сметы: Paris 15 — EUR640 за полдня или EUR1380 за полный день
на двоих за пять дней; Barcelona — EUR120 на двоих за один STEM день.
Полный счёт, страхование, языки отдельных блоков и приём приезжих остаются
вопросами к организаторам. В Швейцарии CHF210 для Flight Camp относится
только к одобренной субсидии. Его FAQ по ссылке «2027» визуально относится
к 2026; старые даты приезда в новый календарь не перенесены.

Неизвестный формат посещения теперь показан отдельно от дневного лагеря
и пансиона. Неподтверждённый язык не попадает в фильтр подтверждённого EN.
Полный мировой аудит остаётся активной целью; полностью проверенных стран
пока нет. Публикация подтверждается отдельной квитанцией Sites.

Воспроизведение: `python3 scripts/deepen-camp-programmes-v54.py`, затем
`python3 scripts/build-database.py`, `python3 scripts/finalize-europe-camps-v111.py`
и `python3 scripts/verify-europe-camps-v111.py`.

## Азия: первичные программы и документы, проход112

Добавлены12 досье у шести операторов: WINNING, Kidchen Club,
Young Engineers Singapore, Sunshine Kids Academy, Kspace и HAFS.
SMIS Jeju дополнен собственными материалами FutureLab/ESL/ночного присмотра.
Реестр содержит839 досье в39 странах и3421 карточку; все прежние ID
сохранены. Из прежних карточек изменены только две смены SMIS; остальные
3417 объектов сохранены точно. Все17 семейных смет сохранены без изменений.

Две новые точные смены2027: Cebu STEAM22января–3февраля с10 лет
(USD1900early/2200regular) и Singapore AIGC23января–1февраля с11 лет
(USD3900early,USD1000аванс внутри). Матвею Cebu доступен только после
10-летия к первому дню; Оскару пока рано. Родительский тариф не даёт
младшему допуск в STEAM. Семейный языковой WINNING6–10 отдельно,
без доказанных дат/прайса. Страна определяется площадкой: Cebu — Филиппины,
а не Тайвань, где опубликовано объявление и находится соорганизатор.

Kidchen указывает октябрьские недели без года. Young Engineers не публикует
новые даты/цену/язык технического учителя. Kspace подробно раскрывает
налоги, форму, обязательный screening и отмену для прошедших сезонов;
его зимний PDF относится к2025/26, летний — к2026. Эти документы
не создают календарь2027. Sunshine рекламирует конкретный курс2026
только для малышей до3лет; общая возрастная рамка до12 не заменяет
конкретную программу старших. HAFS требует Grade4+, а собственный FAQ
ограничивает обещание English-only. SMIS подтверждает английский для ESL;
язык AI/STEAM/humanities ещё не установлен.

Проверены39 прямых обращений к первичным источникам,35 ответов HTTP200,
четыре PDF и20 полностью просмотренных значимых страниц. HTTP202 без тела,
ошибки, старые поисковые описания и пустой notice не считаются новой
подтверждённой программой. Полный мировой аудит остаётся активным,
полностью проверенных стран пока нет. Публикация подтверждается отдельно.

Воспроизведение: `python3 scripts/deepen-camp-programmes-v54.py`, затем
`python3 scripts/build-database.py`, `python3 scripts/finalize-asia-camps-v112.py`
и `python3 scripts/verify-asia-camps-v112.py`.

## Америка: подробные программы и семейные сезоны, проход126

Локально подготовлены19 новых досье у пяти операторов: InnEd Academy,
Frost Valley YMCA, Explora Campamento, CodeREV Kids и отправляющее
отделение CISV México. Обновлено существующее EnvisionCP299 без дубля.
Реестр содержит999 досье в39 странах,3741 карточку и2943 семейные даты;
все3695 прежних карточек,979 остальных досье и48 бюджетов сохранены.
Досье и смены не означают столько же независимых лагерных организаций.

InnEd публикует два трёхдневных блока декабря2026. Frost разделён на
пансион, дневные maker-программы и родительские семейные заезды;
выбор2–6 зимних ночей остаётся сезонным окном. Даты2027 не превращают
старый дневной прайс2026 в новый счёт. Тариф за участника не подменяется
тарифом за ребёнка, комнату или весь lodge. Sugarloaf/Seedlings дают
коды заездов без выдуманных недельных границ. CodeREV syllabus явно2024;
Envision и Explora сохраняют конфликтующие/недатированные календари.
CISV Village11лет — будущий chapter-маршрут, не прямая покупка места
в любой стране. Неподтверждённый язык не попадает в EN-фильтр.

Выбранные условия прочитаны в64 первичных обращениях, включая пятьPDF;
два конкретных прайс-листа визуально проверены. HTTP200 может означать
home fallback или soft404. Raw HTML/PDF/изображения остаются вне repo.
Проверки сравнивают предыдущие объекты и полные SQLite/JSON/CSV/ICS,
отдельно проверяют фильтры, прямые карточки и мобильный интерфейс.

Версия126 ещё не опубликована. Свежие get_site вернули
«SitesConnectorError: Sites project not found», list_sites пуст;
последняя подтверждённая публикация —125. Локальная подготовка не
означает save/deploy. Мировая цель активна, полностью проверенных стран нет.

Воспроизведение: `python3 scripts/deepen-camp-programmes-v54.py`, затем
`python3 scripts/build-database.py`, `python3 scripts/finalize-americas-camps-v126.py`
и `python3 scripts/verify-americas-camps-v126.py`.

## Франция и Испания: ближайшие английские недели, проход 133

Локально добавлены 14 досье программ четырёх операторов: Kids&Us,
Codelearn, SILC и International School San Patricio Toledo. Реестр теперь
содержит 1 098 досье в 39 странах, 3 806 записей, 62 семейных варианта
и 56 частичных смет. Все 3 793 прежние события, 1 084 досье, 55 смет,
школы, результаты и маршруты сохранены. Досье не равны числу операторов.

Двенадцать датированных вариантов включают октябрьские English FunWeeks
и SILC Normandy 18–23 июля 2027. Paris 11: morning 3–10, full day 5–8;
Rueil: EN утром, язык ART неизвестен. €570 — только два утренних tuition.
Codelearn «6–7» — название-мем, не возраст; даты Robobol без года и язык
сайта не стали подтверждённой сменой или языком преподавания. Toledo Main
Robotics 10–16 отличается от коротких STEAM активностей Mega 6–9.
Приложенные timetable filenames 2026 не подтверждают точные смены 2027.
SILC online unavailable оставляет причину неизвестной; CPV 2026 с конфликтом
€100 dossier не представлены договором 2027.

E190 — местный Coolest Projects Spain: 24 октября, проекты 12–18,
семейное посещение отдельно. Срок подачи проектов 8 октября не дедлайн
младших братьев-посетителей; карточка не входит в major exhibition ICS.
Все 3 009 прежние VEVENT сохранены побайтно, новых 13; major ICS — 104.

25 сохранённых HTTP-ответов включают shell, source bundle и discovery
pages; условия Toledo отдельно прочитаны через native browser. Три PDF,
11 страниц извлечённого текста, две страницы расписаний визуально проверены.
Raw страницы и PDF вне репозитория. Проверены полные SQLite/JSON, исходные
объекты и 11 локальных desktop UI сценариев; нового mobile/production QA нет.

Воспроизведение: `scripts/deepen-camp-programmes-v54.py`, затем
`scripts/build-database.py`, `scripts/finalize-europe-camps-v133.py`
и `scripts/verify-europe-camps-v133.py` через Python с lxml/pypdf.
Версия 133 ещё не опубликована: свежий get_site того же проекта вернул
404 «Sites project not found». Последняя подтверждённая публикация 125.
Мировая цель активна; полностью изученных стран 0.

## Сингапур и уточнение Camp Ayla: проход 134

Добавлены четыре досье программ двух операторов: EDUTech Future и
CAMP CHALLENGE. Реестр содержит 1 102 досье в 39 странах, 3 808 записей,
64 семейных варианта и 57 частичных смет. Из прежних объектов полностью
сохранены 1 097 досье, 3 782 события, 56 смет, все 142 профиля лиг/программ,
школы, результаты и маршруты. Досье могут относиться к одному оператору;
количество не является рейтингом мировых лагерей.

EDUTech Industry 21–26 ноября 2026: полный лагерь 7–15 подходит Матвею
по возрасту; Оскару — только отдельный Family AI Ideathon 5–6 с родителем.
Точный день младшего компонента неизвестен: сохранено окно недели без
выдуманной смены. Цена $1 500 / диапазон S$200–1 500 ещё не определяют
семейный счёт; единица начисления неизвестна. Регистрация И оплата
полного лагеря до 15 ноября. Язык преподавания и допуск иностранцев к
специальным выездам ещё требуют подтверждения. Занятия AI for Tweens
9–14 по два часа на выходных отдельно; срок октябрьского набора прошёл.

Nature Quest 23–25 ноября, 5–10: общий дневной отдых для обоих. Три дня
$356 до GST: стандартный расчёт с 9% даёт 388,04 каждому / 776,08 за двоих.
SGD принят по местному контексту; валюта и округление требуют счёта.
Ранняя скидка в расчёт не включена. Неизвестные обязательные суммы и
семейная поездка остаются открытыми. Две площадки; конец 25 ноября
расходится в заголовке и плане: 20:00/20:30. Английский сайт не стал
подтверждением языка занятий ни для одной новой программы.

У Camp Ayla исправлены названия Prime 09–13 / Regular 09–15 /
Extended 09–17 / Super Extended 09–18. Числовые тарифы, даты, возраст и
языковые теги прежние; изменены 24 календарных подписи и дата проверки.
Семейный ICS содержит 3 025 записей: 2 998 прежних VEVENT сохранены
побайтно, у 24 Ayla прежние UID и даты, добавлены две смены и один
регистрационный срок. ICS 104 крупных выставок не изменён.

11 сохранённых первичных HTTP-ответов проверены по хешам. Выбранные
условия сопоставлены с досье; полные SQLite/JSON и прежние объекты
проверены отдельно. Raw HTML/text и снимки браузера вне repo.
Проверены локальные desktop фильтры, возраст/язык, карточки и смета;
нового mobile/production QA нет.

Воспроизведение: `scripts/deepen-camp-programmes-v54.py`, затем
`scripts/build-database.py`, `scripts/finalize-asia-camps-v134.py`
и `scripts/verify-asia-camps-v134.py` через Python. Проверка первичных
снимков требует приватного evidence-каталога вне репозитория.

Версия 134 локальная и ещё не опубликована: свежий get_site того же
проекта вернул 404 «Sites project not found». Последняя подтверждённая
публикация — 125. Полная мировая цель активна, полностью изученных стран 0.
