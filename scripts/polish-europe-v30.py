"""Readable public wording and precise age / provenance distinctions for v30."""
import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1];path=root/'data/catalog.json';d=json.loads(path.read_text())
assert d['completeness_audit']['version']==30
ids=set(d['completeness_audit']['new_ids']);pids=set(d['completeness_audit']['new_profiles']);sids=set(d['completeness_audit']['new_school_ids'])
substitutions={
 'PlanèteSciences':'Planète Sciences','WestSideRobotLab':'West Side Robot Lab','WorldChampionship':'World Championship','EurobotJunior':'Eurobot Junior','HauntedSTEAMLab':'Haunted STEAM Lab',
 'SwissChallenge':'Swiss Challenge','SwissExplore':'Swiss Explore','SwissStarter':'Swiss Starter','Swisslocal':'Swiss local','Swissregional':'Swiss regional','Swissfinal':'Swiss final',
 'RoboBasic6':'RoboBasic 6','LEGOComputationalThinking&AI':'LEGO Computational Thinking & AI','ComputationalThinking&AI':'Computational Thinking & AI',
 'Challenge9':'Challenge 9','Challenge10':'Challenge 10','Elementary8':'Elementary 8','Explore6':'Explore 6','Juniorrobotics':'Junior robotics','SeniorVEX':'Senior VEX',
 'Engineeringnotebook':'Engineering notebook','DesignNotebookAward':'Design Notebook Award','InnovateAward':'Innovate Award','SigmaBots':'Sigma Bots','RoboSparks':'RoboSparks',
 'AlpineRoboGames':'Alpine Robo Games','OffensivePowerRating':'Offensive Power Rating','SchoolHub':'School Hub','AfterSchoolHub':'After School Hub',
 'schoolreport':'school report','Schoolreport':'School report','IBContinuum':'IB Continuum','InternationalSchool':'International School','StageOne':'Stage One','FiraGranVia':'Fira Gran Via',
 'rueClaudePouillet':'rue Claude Pouillet','LeMillénaire':'Le Millénaire','LaRoche-sur-Yon':'La Roche-sur-Yon','AuvergneRhôneAlpes':'Auvergne Rhône-Alpes',
 'schooltuition':'school tuition','currentregistration':'current registration','currentseason':'current season','FutureEdition':'Future Edition','FoundersEdition':'Founders Edition',
 'Classpack':'Classpack','familybooking':'семейная запись','familycamp':'семейный лагерь','familyregistration':'семейная регистрация','technicalworkshop':'технический мастер-класс',
 'worldquota':'мировая квота','worldqualification':'мировой отбор','worldfinal':'мировой финал','worldprize':'мировая награда','worldaward':'мировая награда',
 'foreigneligibility':'допуск иностранной команды','foreignteam':'иностранная команда','foreigndelegation':'иностранная делегация','foreignadmission':'иностранный приём',
 'nationalfinal':'национальный финал','localqualifier':'местный отбор','nationalquota':'национальная квота','internationalroute':'международный маршрут',
 'roboticscourse':'курс робототехники','juniorcoach':'наставник младших','teamplace':'место в команде','teamcode':'код команды','gradeplacement':'определение класса',
 'ниодного':'ни одного','ещёне':'ещё не','неустановлен':'не установлен','неустановлена':'не установлена','неустановлены':'не установлены','неполучен':'не получен','неполучена':'не получена','неполучены':'не получены',
 'неподтверждён':'не подтверждён','неподтверждена':'не подтверждена','неподтверждены':'не подтверждены','необещан':'не обещан','необъявлен':'не объявлен','непереносить':'не переносить','неперенесён':'не перенесён',
 'поage':'по возрасту','поgrade':'по классу','поschool':'по school','потаблице':'по таблице','вописании':'в описании','вформе':'в форме','для6':'для 6','для9':'для 9',
 'оба6':'оба 6','обоимпо':'обоим по','лучшихшкол':'лучших школ','schoolclaims':'сообщения школ','sourceproof':'источник',
 'Robotfiloguidé':'Управляемый проводной робот','robotfiloguidé':'управляемый проводной робот','Teledriven':'Управляемый','non-compact':'кроме готовых компактных роботов',
 'robot/travel':'робот / поездка','robot/trip':'робот / поездка','robot/travel/internationalfee':'робот / поездка / международный взнос',
}
def readable(x):
 if isinstance(x,str):
  if x.startswith(('http','C9','L2','E1','S02')) and ' ' not in x:return x
  for a,b in substitutions.items():x=x.replace(a,b)
  x=re.sub(r'([А-Яа-яЁё])([A-Za-z0-9])',r'\1 \2',x)
  x=re.sub(r'([A-Za-z0-9])([А-Яа-яЁё])',r'\1 \2',x)
  x=re.sub(r'(?<=\d)(?=[A-Za-z][a-z])',' ',x)
  x=re.sub(r'([a-z])([A-Z][a-z])',r'\1 \2',x)
  x=re.sub(r'(?<=[,;:])(?=\S)',' ',x)
  x=x.replace('≠',' ≠ ').replace('→',' → ').replace(' /',' /').replace(' +',' +')
  return re.sub(r' +',' ',x)
 if isinstance(x,list):return [readable(v) for v in x]
 if isinstance(x,dict):return {k:(v if k in ['url','source','id','entity_id','team_id','profile_ids','event_ids','school_ids','new_ids'] else readable(v)) for k,v in x.items()}
 return x
# Preserve schema identifiers, enums and URLs; polish only human-readable fields.
event_fields=['title','city','age','mat','osc','entry','gear','language','cost','level','reward','priority','action','proof','note','period','format','visitor_note','company_scope','registration_status']
for e in d['events']:
 if e['id'] in ids:
  for k in event_fields:
   if k in e:e[k]=readable(e[k])
  for r in e.get('references',[]):r['label']=readable(r['label'])
for p in d['league_guide']['profiles']:
 if p['id'] in pids:
  for k in ['name','age_summary','summary','categories','route','hardware','language','importance','strengths','requirements','nuances','cost','award','sources','evidence']:p[k]=readable(p[k])
for s in d['schools']:
 if s['id'] in sids:
  for k in ['name','city','curriculum','ages','language_note','fit','boarding_note','programme','labs','ai','results','admissions','cost','questions','sources','verification']:s[k]=readable(s[k])
f=d['europe_focus'];f=readable(f);d['europe_focus']=f
f['family']='Матвей — 2017 год, Оскар — 2020 год. Оба могут учиться весь день на английском и испанском; русский тоже подходит. Точные классы и дни рождения неизвестны.'
f['conclusion']='Для европейской учебной базы первым проверял бы Испанию: язык уже знаком обоим, есть независимые команды WRO и младшие категории FIRST LEGO League. Швейцарию рассматривал бы как английскую школьную базу после проверки наставника младших и полной сметы. Францию — для конкретных двуязычных каникул; постоянный соревновательный маршрут требует французского или подтверждённой команды на английском.'
f['limitations']='Это моя рекомендация по возрасту, языкам и прочитанным программам, а не официальный рейтинг стран или школ. Места, приём иностранцев, национальные квоты, полный бюджет и все местные операторы ещё не проверены. Три страны исследованы частично.'
updates={
 'ESP':dict(verdict='Первый кандидат европейской базы',reason='Испанский доступен обоим. WRO разрешает независимые нешкольные команды; RoboBasic начинается с 6 лет. В FIRST LEGO League две редакции с разным оборудованием.',mat='WRO Elementary — 8–12 лет. FLL Future K8 — 8–16, подходит по возрастному диапазону уже сейчас. Founders Challenge — 10–16; для сезона 2027 нужно подтвердить контрольную дату возраста.',osc='WRO RoboBasic — 6–12. FLL Explore — 6–9, K5 — 5–7. Explore и K5 дают признание проекта, а не победу в конкурентном турнире.',camp='NATUK / HES прямо предлагает Robotics на английском для 6–16 лет. Есть проживание в отеле и дневной формат; даты нового набора 2027 пока не опубликованы.',school='Brains La Moraleja и St PETER’S Barcelona — кандидаты. Проверить действующую младшую команду и наставника. В последнем PDF St PETER’S Robotics только для Y1–Y2, для Y3–Y5 указана Virtual Reality.',risk='Независимая команда ещё не означает право на испанскую мировую квоту. Для K8 нужны 4–10 детей и два новых робота. Перед покупкой выбрать редакцию и подтвердить местный этап.'),
 'CHE':dict(verdict='Английская школьная база с возрастными условиями',reason='WRO Starter — 6–10, Elementary — 8–12. FLL Explore — 6–10, Challenge — 9–16. У International School Basel описан путь робототехники по классам.',mat='WRO Elementary или FLL Challenge с 9 лет. В Basel младшая робототехника описана для Grades 3–5; точный класс Матвея нужно определить.',osc='WRO Starter и FLL Explore — 6–10. Приём шестилетнего ребёнка в школу не подтверждает робототехническую группу ниже Grade 3.',camp='Helvetic опубликовал таблицы курсов и летних смен 2027, но английский именно в робототехнике не доказан. Brillantmont Tech с 10 лет — будущий кандидат для Матвея после проверки дня рождения и группы.',school='International School Basel и Aiglon. У Basel подтверждены сообщения о национальных результатах старших и квалификации на Worlds; мировая награда младшей команды не установлена.',risk='Starter не заявлен как категория мирового финала. Иностранный допуск, даты местных FLL-площадок и язык лагерей ещё уточняются. Студенческий билет Swiss Robotics Day относится к PhD / MSc / BSc, не к детям.'),
 'FRA':dict(verdict='Двуязычные каникулы; школьный путь с языковой проверкой',reason='Есть конкретные STEAM-смены ABI на английском и французском. Planète Sciences опубликовал три региональных отбора Junior 2027. Общий FLL Challenge указан для 9–16 лет.',mat='Coupe Junior — 8–18 лет по странице участия; три отбора в феврале–апреле 2027. FLL Challenge Founders с 9 лет условно. Язык интервью и иностранную регистрацию нужно подтвердить.',osc='ABI Haunted STEAM Lab: группа Explorer 5–8 лет. В Junior минимальный возраст 8 по текущей странице участия; старое описание с 7 лет также не допускает шестилетнего.',camp='ABI: 19–23 и 26–30 октября, 21–23 декабря 2026. Только Haunted прямо публикует группы 5–8 и 9–12. Tinker предлагает EN / ES через принимающий центр; открытой семейной смены не подтверждено.',school='Ermitage и ABI: двуязычные младшие программы. Доказательства мирового лидерства роботокоманд не установлены. Пансион Ermitage с 11 лет пока не подходит обоим детям.',risk='Французские материалы ещё не означают возможность судейства на английском. В Junior расходится минимум 7 / 8 лет. Доступные окна Tinker — предложение центрам. Общие даты фестиваля 5–8 мая не выданы за точное расписание Junior final.')}
for c in f['countries']:c.update(updates[c['iso']])
f['steps']=[
 dict(title='Осень 2026 · выбрать одну действующую команду',detail='До покупки набора FLL выбрать редакцию и площадку. Испанская K8 допускает диапазон 8–16 лет, но требует 4–10 участников. Оскару отдельно рассмотреть Explore / K5 или RoboBasic. В швейцарском Challenge указан срок регистрации 31 октября 2026; проверить конкретную площадку и иностранный допуск.'),
 dict(title='Каникулы · проверить технический уровень',detail='Из найденных датированных смен с английским и возрастными группами для обоих — ABI Haunted STEAM Lab 26–30 октября 2026: цепи, механизмы и код, группы 5–8 / 9–12. Это учебная программа. При трёх годах опыта нужно заранее согласовать сложность и собственный проект детей.'),
 dict(title='2027–2029 · инженерная лига и собственный продукт',detail='Матвею: WRO Elementary с автономным роботом или выбранная редакция FLL. Оскару: RoboBasic либо проект Explore, затем Elementary после 8 лет по национальным правилам. Добавить Python, механику, журнал экспериментов, объяснение на EN / ES и проект для реального пользователя. Одна–две лиги помогут сохранить глубину работы.'),
 dict(title='К 10–12 годам · отбор и доказательства вклада',detail='Наставник, регулярные тренировки, свой код и инженерный журнал → местный результат → национальная квота → мировой этап. Различать оценённую награду, результат матчей и участие. Решение о переезде принимать после пробного триместра и знакомства с работой действующей команды.')]
for p in d['league_guide']['profiles']:
 if p['id'] in pids:
  p['language']='Язык технического интервью и местного этапа подтвердить; англоязычный сайт не доказывает судейство на английском.'
  p['importance']='Национальный маршрут внутри международного семейства; не отдельная новая мировая лига.'
  p['hardware']='Оборудование зависит от категории и редакции; не покупать до выбора местного этапа.'
  p['cost']='Взнос, робот и поездка считаются отдельно; опубликованные тарифы конкретного года не гарантируют цену следующего сезона.'
  p['award']='Награда конкретного этапа по протоколу. Учебное признание, квалификация и мировая победа различаются.'
  p['evidence']='Прочитаны первичные страницы. Неизвестные условия следующего сезона и иностранного допуска отмечены отдельно.'
byid={e['id']:e for e in d['events']}
for id in ['L217','L219']:
 byid[id]['mat']='Условно: в 2027 Матвею исполняется 10; для группы 6–9 нужна точная дата рождения и правило оператора'
for id in ['C908','C909','C912','C913','C914','C915','C916']:
 byid[id]['entry']=readable(byid[id]['entry'])
byid['E017']['period']='1–4 марта 2027 · Fira Gran Via'
for e in d['events']:
 if e['id'] in ids:
  for k in event_fields:
   if k in e:e[k]=re.sub(r'(\d): (\d)',r'\1:\2',e[k])
for id in ['E140','E141','E142']:
 e=byid[id];e.update(visitor_policy_note=e['visitor_note'],adult_entry='Профессиональная регистрация у организатора; билет и действующие условия подтвердить.',exhibitor_note='Компании и исследовательские организации по перечню конкретного издания. Все мировые производители не обещаны.')
 e.update(highlights=['Робототехника и автоматизация','ИИ и технологические проекты','Компании, исследовательские организации и демонстрации'],exhibitor_directory_url=e['source'])
for id in ['C906','C907']:
 byid[id]['entry']='Команда из 2–3 детей и наставник 18+. Подтвердить календарь, таблицу года рождения нового сезона и допуск иностранной семьи у WRO Switzerland.'
 byid[id]['note']='Прочитаны правила 2026; приём до 15 марта 2026 закрыт. Даты 2027 ещё не опубликованы. Starter — бесплатный младший местный путь. Главная страница связывает мировой отбор с RoboMission / Future Innovators, но не со Starter. Возрастной диапазон не подтверждает право иностранной команды на швейцарскую квоту.'
for id in ['C910','C911']:
 byid[id]['entry']='Команда из 2–3 детей и наставник. FAQ разрешает независимые нешкольные команды. Подтвердить иностранный допуск, выбрать местный турнир с нужной категорией и проверить право на национальную квоту.'
 byid[id]['note']='Не каждый местный турнир предлагает все категории. Приём закрывается за 15 дней до даты или раньше при заполнении; точных дат следующего сезона пока нет. Местный этап ведёт в национальный финал. Мировой отбор зависит от категории и национального допуска; RoboBasic не заявлен как категория мирового финала.'
for id in ['C912','C913','C914','C915']:
 byid[id]['entry']='Регистрация BIOGLOW 2026/27 у Ingeniera.soy открыта для школ, академий, ассоциаций и независимых групп. Подтвердить конкретный этап, иностранный допуск и контрольную дату возраста.'
 byid[id]['note']='В сезоне две аппаратно разные редакции. K8 — соревновательная для 8–16 лет, с 4–10 участниками и двумя новыми роботами; Матвей попадает в диапазон, но братьев вдвоём недостаточно. Explore и K5 не соревновательные. Discover прямо недоступен в регистрации 2026/27. Общий Classpack не даёт место на событии: нужен соответствующий вариант регистрации.'
for id in ['C917','C918','C919','C920']:
 byid[id]['age']='8–18 лет по текущей странице участия; старое описание 7–18 противоречит'
 byid[id]['entry']='Команда через Planète Sciences и местную делегацию. Национальный финал после местного отбора. Иностранную регистрацию, принимающую организацию и язык интервью подтвердить.'
 byid[id]['note']='Текущая страница участия указывает 8–18 лет, старое описание — 7–18. Оскар младше обоих порогов. Новые региональные даты 2027 опубликованы; старый срок 31 декабря 2025 и финал мая 2026 не перенесены на новый сезон. Местный призовой результат ведёт к национальному финалу, затем к Eurobot Junior по правилам отбора. Дата международного финала 2027 неизвестна.'+(' Общий фестиваль назначен на 5–8 мая 2027; точные дни Junior final ещё не получены, поле даты оставлено пустым.' if id=='C920' else '')
for id in ['L229','L230','L231']:
 byid[id]['entry']='Дневная смена на английском и французском. Подтвердить места и приём ребёнка из приезжей семьи, согласовать возрастную группу и технический уровень.'
byid['L230']['age']='Explorer — 5–8; Inventor — 9–12 лет, прямо в форме этой смены'
for id in ['L232','L233','L234','L235']:
 byid[id]['note']='Это предложение поставщика для образовательных и молодёжных центров. Даты — доступные окна заказа, а не подтверждённые открытые смены для семьи. Осень 2026 распродана. В летней таблице под заголовком 2027 остались строки 2026; даты не исправлены предположением. Предложения P4 не включены в семейный календарь.'
profile_text={
 'wro-switzerland':dict(route='Младшие занятия Starter и местный конкурс → самостоятельная команда Elementary → региональный и национальный отбор → международная квота при выполнении правил страны.',requirements=['Команда из 2–3 детей; взрослый не считается участником вместо ребёнка.','Возраст определяется годом рождения, а не только днём турнира.','Календарь и иностранный допуск нового сезона ещё неизвестны.'],nuances=['Starter не заявлен как категория мирового финала.','Бесплатные занятия для начинающих могут быть слишком простыми после трёх лет опыта; проверить сложность и наставника.']),
 'wro-spain':dict(name='WRO Spain · RoboBasic с 6 лет / Elementary',route='Независимая команда и подходящая категория → местный турнир → национальный финал → международный этап по правилам категории и национальной квоты.',requirements=['EUR60 за команду не включает оборудование, поездку и международный взнос.','Местный приём закрывается за 15 дней до турнира или раньше при заполнении.','Иностранный допуск не установлен.'],nuances=['Каждый местный организатор выбирает доступные категории.','RoboBasic — младший инженерный конкурс; он не заявлен как категория мирового финала.']),
 'fll-europe-three':dict(summary='Матвей: Challenge с 9 лет в Швейцарии или соревновательная K8 с 8 лет в Испании. Оскар: Explore 6–10 в Швейцарии, Explore 6–9 или K5 5–7 в Испании. Французский Challenge указан с 9 лет; английское судейство ещё не подтверждено.',route='Выбрать страну, редакцию и оборудование → зарегистрировать команду на нужный этап → собственный проект и техническое интервью → отбор на следующий этап по квоте страны и редакции.',requirements=['Признание в Explore / K5 отличается от победы в конкурентном турнире.','Испанская K8 требует минимум 4 детей и два новых робота; братьев вдвоём недостаточно.','В Swiss Challenge указан срок 31 октября 2026; конкретные местные даты ещё проверяются.'],nuances=['Founders и Future используют разное оборудование.','Англоязычный сайт не подтверждает английское судейство.','Международный слот нового сезона проверяется отдельно.']),
 'eurobot-junior-fr':dict(route='Собственный инженерный проект в течение 6–8 месяцев → местный отбор → призовой результат на национальном финале → Eurobot Junior по действующим правилам.',requirements=['Членство принимающей организации EUR50; робот и поездка оплачиваются отдельно.','Срок регистрации 2027 не получен; прежнее 31 декабря 2025 не перенесено на новый сезон.','Язык судейства и иностранную делегацию нужно согласовать.'],nuances=['Управляемый робот Junior отличается от автономного Senior Eurobot.','Общие даты 5–8 мая 2027 не подтверждают точные дни Junior final.'])}
for p in d['league_guide']['profiles']:
 if p['id'] in profile_text:
  p.update(profile_text[p['id']])
  for c in p['categories']:
   for k in c:c[k]=c[k].replace('Robo Basic','RoboBasic').replace('Future Innovators','Future Innovators')
  for s in p['sources']:s['title']=s['title'].replace('Swissages','Возраст в Швейцарии ').replace('Spainactual','Регистрация Испания ').replace('Currentparticipation','Текущие условия участия').replace('Presentationageconflict','Расхождение возраста в описании')
for e in d['events']:
 if e['id'] in ids:
  e['title']=e['title'].replace('Junior2027','Junior 2027').replace('BIOGLOW2026','BIOGLOW 2026').replace('Winter2027','Winter 2027').replace('Spring2027','Spring 2027').replace('Day2026','Day 2026').replace('Lyon2027','Lyon 2027').replace('Robo Basic','RoboBasic')
for s in d['schools']:
 if s['id'] in sids:
  s['verification']='Прочитаны первичные программы и сообщения школ. Приём детей, место в команде и доступные места не подтверждены.'
 if s['id']=='S023':
  s.update(curriculum='Англоязычная частная школа без распределения прибыли; IB PYP / MYP / DP по сообщению школы.',ages='Школа 3–18 лет. Junior Robotics: Grades 3–5; VEX IQ: Grades 7–8; VEX V5: старшая ступень. Классы детей нужно определить.',language_note='Школа прямо подтверждает английский язык. Язык конкретного младшего наставника уточнить.',programme='Grades 3–5: необязательные платные внешние занятия робототехникой. Grades 7–8: курс VEX IQ, соревновательная группа описана как план следующего года. Старшая VEX V5 команда имеет национальные результаты.',ai='В Junior описаны AI-enabled kits; полноценный курс ИИ для шестилетних не доказан.',admissions='Школа принимает в течение года при наличии места и выполнении требований. Проверить английский, определение класса, младшего тренера и вход в команду.',questions=['Кто ведёт Grades 3–5, сколько часов и какие результаты последних трёх сезонов?','Какие технические занятия доступны Оскару до Grade 3?','Почему обзор называет 2-е национальное место, а отдельный отчёт 4-е в общем зачёте и 2-е OPR? Нужен протокол организатора.'])
  s['fit']['note']='Оба — кандидаты по школьному возрасту. Для Матвея проверить Grade 3–5; для Оскара робототехническая группа ниже Grade 3 не подтверждена.'
  for r in s['results']:r.update(team='Sigma Bots / Limbo' if 'Alpine' in r['stage'] else 'Sigma Bots',team_id='',limit=r.pop('note',r.get('limit','')))
 if s['id']=='S024':
  s.update(curriculum='Англоязычная частная школа 1–18; IB PYP / MYP / DP по сообщению школы.',ages='Школа 1–18. PDF After School Hub 2025/26: Robotics только Y1–Y2, Virtual Reality Y3–Y5. Расписание 2026/27 нужно подтвердить.',programme='Платная Robotics Y1–Y2 в последнем прочитанном PDF. Участие RoboSparks в FLL в 2018 году — исторический факт; действующая сильная соревновательная команда и призовые места не доказаны.',language_note='Английский язык школы подтверждён; язык наставника Robotics отдельно уточнить.',questions=['Какая робототехническая группа для Матвея есть в 2026/27?','Есть ли действующая команда FLL, код команды, наставник и результаты?','Для Оскара: точный класс, язык, цена и наличие мест в Robotics?'])
  s['fit']['note']='Оба подходят по школьному возрасту условно. Robotics Y1–Y2 вероятнее для Оскара; для Матвея в Y3–Y5 описана Virtual Reality, робототехнический маршрут требует проверки.'
 if s['id']=='S025':
  s.update(curriculum='Двуязычная FR / EN школа для 2–12 лет; STEAM-проекты на каникулах. IB не подтверждён.',ages='Школа 2–12. Haunted STEAM Lab: группы 5–8 и 9–12.',programme='Двуязычная начальная школа с текущими проектами: электрические цепи, механизмы, код. Отборная соревновательная команда не установлена.',language_note='FR / EN подтверждён для школы и конкретного Haunted workshop. Полностью английский школьный день не обещан.',questions=['Какова доля английского в школьном дне и робототехнике?','Есть ли действующая FLL / WRO команда, наставник и результаты?','Как поддерживают детей 6 / 9 лет без французского?'])
  s['fit']['note']='Школьный возраст и группы Haunted подходят обоим по диапазону. Приём, оценивание и места не подтверждены.'
for k in ['conclusion','scope']:d['completeness_audit'][k]=readable(d['completeness_audit'][k])
for x in d['completeness_audit']['source_issues'][-5:]:
 for k in ['name','status']:x[k]=readable(x[k])
d['completeness_audit']['conclusion']='Частичный мировой каталог. v30: 37 новых карточек, 4 национальных профиля, 3 школы и отдельное сравнение Швейцарии, Испании и Франции. Возраст, язык, даты и уровень результатов проверены по конкретным программам; неизвестные условия видны в досье.'
d['completeness_audit']['scope']='Углублённая проверка Швейцарии, Испании и Франции: лагеря, возрастные маршруты соревнований, школы и профессиональные выставки. Мировое исследование продолжается.'
d['school_focus']['conclusion']='25 школьных досье. Добавлены International School Basel, St PETER’S Barcelona и ABI Paris. Школьный возраст, младшая робототехника, язык и результаты команды проверяются отдельно. Мировой школьный аудит частичный.'
d['school_focus']['routes'][-1]['detail']='Basel: путь по классам и национальные награды старших. St PETER’S: английский / IB, но Robotics в последнем PDF только Y1–Y2. ABI: двуязычная младшая школа и конкретные STEAM-смены; соревновательное лидерство не доказано. Возраст пансиона Aiglon и Ermitage проверяется отдельно.'
d['camp_focus']['conclusion']='Новые европейские кандидаты: датированные FR / EN проекты ABI; Robotics на EN у NATUK / HES без дат нового лета; Helvetic 2027 с уточнением языка именно робототехники; Tinker на EN / ES через принимающий центр. Это программы и смены четырёх операторов.'
for r in d['camp_focus']['routes'][-2:]:
 r['name']=readable(r['name']);r['detail']=readable(r['detail'])
for x in d['camp_focus']['source_issues'][-5:]:
 for k in ['name','status']:x[k]=readable(x[k])
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('v30 public wording / school provenance / 2027 age gates refined')
