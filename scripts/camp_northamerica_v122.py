"""Selected North American primary programme clauses; worldwide work remains active."""
from pathlib import Path
from datetime import date,timedelta
import re
ROOT=Path(__file__).resolve().parents[1]
BASE='bdf0ae927bee969913ee1377d5c63e51d2a087a6'
CHECKED='2026-10-06'
C='https://canaqua.ca/'
K='https://www.kandalore.com/'
I='https://www.interlochen.org/'
Y='https://campcayuga.com/'
W='https://www.campwatitoh.com/'
NEW=['canaqua-shortstay','canaqua-intro','canaqua-two-weeks','canaqua-four-weeks','canaqua-day','canaqua-film','canaqua-family','canaqua-parent-child','kandalore-one-week','kandalore-prep-junior','kandalore-summer-family','kandalore-winter-family','interlochen-junior-exploration','interlochen-junior-visual','interlochen-arts-discovery','cayuga-junior-2027','watitoh-2027']
LANG='Английский сайт и иностранные участники установлены, но прямое обещание языка всех занятий этого заезда пока не найдено; EN/ES/RU не подтверждены.'
ASK='Подтвердить язык конкретной группы, иностранный приём, места, возраст/класс на нужную дату, валюту, налоги, итоговый счёт и договор отмены. Заявки не отправлялись.'
CANPOL='В цене уже есть невозвратные $200 membership, не добавлять второй раз. Депозит на ребёнка:1 неделя650/2 недели900/4 недели1250; остаток до1 мая. Карта только для депозита,+2%. Кроме Family Camps: ещё штраф125 до1 февраля/200 в феврале/250 в марте/300 в апреле; с1 мая возврата нет. Это опубликованная политика, не согласованный договор.'
def add_northamerica_v122(add,src,fit,profiles):
 both=fit('conditional','В 2027 Матвею9–10/Оскару6–7; возраст подходит этому треку, язык, иностранный приём и готовность к формату ещё проверить.')
 def emit(idx,name,iso,place,themes,formats,age,programme,rows,price,housing,mat=both,osc=both,sources=None,questions=None,language=LANG):
  slug=NEW[idx]; country='Канада' if iso=='CAN' else 'США'
  add(slug,name,country,iso,place,themes,formats,age,language,programme,
   'Опубликованные варианты 2027; точные смены ниже. Дата не означает свободное место.',price,housing,mat,osc,
   'Редакционный кандидат по возрасту, содержанию и формату; независимый мировой рейтинг не установлен. Общий/художественный лагерь не техническая лига.',
   questions or [ASK],sources or [],status='published_2027',sessions=[[r[0],r[1]] for r in rows])
  p=profiles[-1];p['checked']=CHECKED
  for s in p['sources']:s['checked']=CHECKED
  p['timing']['session_details']=[dict(start=a,end=b,label=label,place=place,price=fee,source=p['sources'][0]['url'],date_scope='camp_session',date_precision='published_session',proof='Выбранные условия собственной страницы прочитаны; индивидуальный допуск и свободное место не подтверждены.') for a,b,label,fee in rows]
  if formats=='family':
   for v in p['timing']['session_details']:v.update(formats=['family','boarding'],accommodation=housing)
  return p
 def canprice(label):return dict(year=2027,label=label+' +налог; код валюты/ставка налога пока не установлены.',included='Программа и пансион по описанию; membership200 уже в тарифе.',extras='Транспорт/аэропорт, налоги и личные расходы отдельно. Нельзя считать неизвестные суммы нулём.',deposit=CANPOL)
 place='503 Beaver Lake Drive · Cardiff, Ontario; Oakville/Ottawa — офисы, не площадки смен'
 one=C+'programs/1-week-traditional-overnight-summer-camps/'
 trad=C+'programs/2-4-week-traditional-overnight-summer-camps/'
 fam=C+'programs/family-weekend-camps/'
 faq=C+'the-experience/faqs/'
 ss=[('2027-06-27','2027-07-02','1A ·5–15','$1695')]+[(a,b,label+' ·5–11','$1950') for a,b,label in [('2027-07-04','2027-07-10','1B'),('2027-07-10','2027-07-16','1C'),('2027-07-18','2027-07-24','2A'),('2027-07-24','2027-07-30','2B'),('2027-08-01','2027-08-07','3A'),('2027-08-07','2027-08-13','3B'),('2027-08-15','2027-08-21','4A'),('2027-08-21','2027-08-27','4B')]]
 p=emit(0,'Camp Can-Aqua · Short-stay','CAN',place,'general,sport,art','boarding','1A5–15; остальные конкретные смены5–11, несмотря на общий заголовок5–12',
  'Выбор land/water/arts, часть дня по домику, часть elective. Короткий первый пансион, а не робототехника. По FAQ до8 детей в домике, Counselor и Junior Counselor; круглосуточный присмотр. Разница возраста братьев больше1 года — совместный домик не гарантирован.',ss,canprice('1A $1695 / остальные $1950 за ребёнка'),
  'Возрастные домики; питание и ночная организация описаны в FAQ.',sources=[src('Конкретные короткие смены, цены и отмена',one),src('Ночёвки, питание, международный транспорт',faq)])
 p['timing']['session_details'][0]['age']='5–15'
 for r in p['timing']['session_details'][1:]:r['age']='5–11'
 emit(1,'Camp Can-Aqua · Session5 / Intro','CAN',place,'general,sport,art','boarding','8–15 в таблице именно Session5; общий текст5–15 конфликтует',
  'Короткий вводный пансион с выбором занятий и общими активностями. Для допуска использовать8–15 в таблице выбранного заезда.',
  [('2027-08-29','2027-09-03','Session5 / Intro ·8–15','$1695 / $1625: условия второго тарифа неизвестны')],canprice('$1695 / $1625, назначение второго тарифа уточнить'),
  'Домики по возрасту.',osc=fit('later','Оскару6–7 в 2027; ниже минимума8 конкретной таблицы, общий текст5+ не разрешение.'),sources=[src('Session5: возраст, даты и два тарифа',one),src('Присмотр',faq)])
 two=[('2027-07-04','2027-07-16','Session1','$3625'),('2027-07-18','2027-07-30','Session2','$3625'),('2027-08-01','2027-08-13','Session3','$3625'),('2027-08-15','2027-08-27','Session4','$3475')]
 emit(2,'Camp Can-Aqua · Two-week traditional','CAN',place,'general,sport,art','boarding','6–14 в конкретных четырёх строках; общий текст6–15 шире',
  'Ежедневно общая активность и четыре elective. Молодшим школьникам короткий canoe outtrip описан как опциональный; требование для старших отличается. Точное размещение/поход подтвердить.',two,canprice('$3625 для1–3 / $3475 для4 за ребёнка'),
  'Пансион, домики по возрасту; короткие походы зависят от класса.',sources=[src('Точные2/4-week таблицы',trad),src('Присмотр/питание',faq)])
 emit(3,'Camp Can-Aqua · Four-week traditional','CAN',place,'general,sport,art','boarding','9–14 в конкретных строках; общий текст9–15 шире',
  'Длительный общий пансион с выбором спорта, искусства и outdoor. Четырёхнедельная цена не тариф короткого заезда.',
  [('2027-07-04','2027-07-30','Session1&2','$6175'),('2027-08-01','2027-08-27','Session3&4','$6175')],canprice('$6175 за ребёнка'),
  'Возрастные домики и походы по классу.',osc=fit('later','Оскару6–7 в 2027; минимум9.'),sources=[src('Конкретный4-week тариф и возраст',trad),src('Присмотр',faq)])
 dayrows=[('2027-07-05','2027-07-09','5 дней ·09:00–16:30','$565'),('2027-07-12','2027-07-15','4 дня ·09:00–16:30','$495'),('2027-08-16','2027-08-20','5 дней ·09:00–16:30','$565'),('2027-08-23','2027-08-26','4 дня ·09:00–16:30','$495')]
 price=canprice('$565/5 дней или $495/4 дня');price['included']='Дневная программа и обед прямо включены.';price['extras']+=' Скидка sibling к day camp не применяется.';price['deposit']='Дневной депозит не установлен; опубликованные650/900/1250 относятся к неделям пансиона. Политику отмены дневного договора уточнить.'
 emit(4,'Camp Can-Aqua · Day Camp','CAN',place,'general,sport,art','day','5–11',
  'Две общие ротации и два elective ежедневно: спорт, вода, творчество.09:00–16:30; опубликованы отдельные4/5-дневные даты. Упоминание ещё week5 в тексте без точной даты не добавлено.',dayrows,price,'Без ночёвок; семейное жильё/доставка отдельно.',sources=[src('Дневные даты, часы, обед и цены',one)])
 film=C+'programs/film-camp/'
 emit(5,'Can-Aqua × Northern Ontario Film Academy · Film Camp','CAN',place,'art,coding','boarding','9–15',
  'Актёрская работа, съёмка, монтаж, свет, фотография и короткий фильм/reel. Три периода film production и один общий elective в день. Программирование и физическая робототехника не заявлены.',
  [('2027-08-21','2027-08-27','Film Camp','$1950')],canprice('$1950 за ребёнка'), 'Полный residential camp по описанию.',osc=fit('later','Минимум9; Оскару6–7 в 2027.'),sources=[src('NOFA: содержание, возраст, цена и смена',film),src('Пансионный FAQ',faq)])
 profiles[-1]['themes']=['art']
 price=dict(year=2027,label='$895+налог за семью до5 одного household в июне; $1195+налог в сентябре. Это не цена на каждого ребёнка.',included='Семейный weekend и возрастные активности; полный перечень питания/белья подтвердить.',extras='Сверх5: ребёнок115 в июне/150 в сентябре+налог; валюту/налог/дорогу уточнить.',deposit='Family Camps прямо исключены из общей шкалы отмены. Отдельный депозит/семейный возврат не установлен.')
 emit(6,'Camp Can-Aqua · Family Weekend','CAN',place,'general,sport,art','family','Все возраста; до5 одного household в семейном тарифе',
  'Семейные land/water/arts: программы для малышей, детей, подростков и взрослых. Родители участвуют; не самостоятельный детский пансион.',
  [('2027-06-04','2027-06-06','Weekend1','$895/семья'),('2027-06-11','2027-06-13','Weekend2','$895/семья'),('2027-06-18','2027-06-20','Weekend3','$895/семья'),('2027-09-03','2027-09-06','Weekend4','$1195/семья')],price,'Семейное проживание на территории; конкретный домик/питание уточнить.',sources=[src('Семейная единица цены и смены',fam)])
 price=dict(year=2027,label='$395+налог за пару один взрослый+один ребёнок, не вся семья. Код валюты не установлен.',included='Доступ к программам Family Camp.',extras='Две пары для двух детей требуют отдельных взрослых/подтверждения счёта; дорога отдельно.',deposit='Отдельная семейная отмена не установлена; общий no-refund May1 не переносить.')
 emit(7,'Camp Can-Aqua · One-on-One Weekend','CAN',place,'general,sport,art','family','Ребёнок5–15 + один взрослый на пару',
  'Знакомство с лагерем вместе с родителем; off-grid Summit Village. Третий заезд содержит конфликтJune18–Sept20,2027 и не создан как трёхмесячная смена.',
  [('2027-06-04','2027-06-06','One-on-One1','$395/пара'),('2027-06-11','2027-06-13','One-on-One2','$395/пара')],price,'Off-grid семейное размещение в Summit Village, отличается от обычного family package.',sources=[src('Тариф пары и конфликт третьей даты',fam)])
 kp=K+'rates-and-dates/';kf=K+'outside-programs/';kplace='1143 Kandalore Road · Algonquin Highlands, Ontario; Toronto — офис'
 price=dict(year=2027,label='$2390 International / $2200 Domestic за неделю до налогов. Domestic только Canada/USA; семья из Коста-Рики не получает его автоматически.',included='Пансионный пакет; точный состав international тарифа ещё проверить.',extras='Валюта, налоги, airport/UM, одежда/походы, оборудование и итоговый счёт не установлены.',deposit='Собственная страница сообщает отдельные2027 refund/payment policies; выбранный договор пока не прочитан. Открытие регистрации15.10.2026 12:00EDT, не запись семьи.')
 emit(8,'Kandalore · One-week young campers','CAN',kplace,'general,sport','boarding','Рождённые2017–2021 по таблице2027, не устаревшее правило6–9',
  'Общий outdoor-пансион младшего возраста. Правила/походы из старых handbook2017/2018/2023 не перенесены в договор2027.',
  [('2027-07-03','2027-07-09','JulyWK1','$2390 International / $2200 Domestic'),('2027-07-10','2027-07-16','JulyWK2','$2390 International / $2200 Domestic')],price,'Лагерные домики; размер группы2027 подтвердить.',sources=[src('2027: годы рождения, тарифы и смены',kp),src('Открытие регистрации',K)])
 price=dict(price,label='$5830 International / $4225 Domestic за2 недели; $8650 / $7150 за4 недели, до налогов.')
 emit(9,'Kandalore · Prep Junior 2/4 weeks','CAN',kplace,'general,sport','boarding','Prep Junior рождённые2016–2020 по таблице2027',
  'Общий outdoor-пансион: длительность выбирать отдельно от возраста. Inter2014–15/Senior2011–13/Leadership2010–11 — другие ступени, не наша младшая группа.',
  [('2027-07-03','2027-07-16','A1 ·2 недели','$5830 International / $4225 Domestic'),('2027-07-17','2027-07-30','A2 ·2 недели','$5830 / $4225'),('2027-08-03','2027-08-16','B1 ·2 недели','$5830 / $4225'),('2027-08-17','2027-08-30','B2 ·2 недели','$5830 / $4225'),('2027-07-03','2027-07-30','A ·4 недели','$8650 / $7150'),('2027-08-03','2027-08-30','B ·4 недели','$8650 / $7150')],price,'Младшие лагерные домики; иностранный договор отдельно.',sources=[src('PrepJunior2016–2020 и international цены',kp)])
 price=dict(year=2027,label='$410 за взрослого / $330 за ребёнка +HST; таблица domestic, международный семейный тариф не установлен.',included='Private family cabin, питание и активности прямо описаны.',extras='Код валюты/ставкаHST, международная надбавка/транспорт уточнить.',deposit='Семейный договор оплаты/отмены пока не установлен.')
 emit(10,'Kandalore · Summer Family Camp','CAN',kplace,'general,sport','family','Семейный формат; отдельные возрастные ограничения занятий проверить',
  'Общая семейная outdoor программа с отдельным домиком и организованными активностями.',[('2027-09-03','2027-09-05','Summer Family','$410 adult / $330 child +HST')],price,'Private family cabin; родители с детьми.',sources=[src('Семейное проживание, питание, дата и цена',kf),src('Domestic колонка',kp)])
 price=dict(year=2027,label='2027 цена TBA для взрослых и детей; не подставлять летний тариф.',included='3 дня:1 ski day pass;5 дней:2 ski day passes. Семейный отапливаемый домик.',extras='Ski/snowboard rentals не включены. Валюта, питание, трансфер/страховка иHST уточнить.',deposit='Новый семейный зимний договор не установлен.')
 emit(11,'Kandalore · Winter Family Camp','CAN',kplace,'general,sport','family','Семейный формат; возраст/уровень для зимних активностей отдельно',
  'Лыжи SirSam’s, снегоступы, cross-country, broomball и другие зимние активности. Ночуют с родителями, не детский ski boarding по старому2020PDF.',
  [('2027-03-15','2027-03-17','3 дня · вариант1','TBA'),('2027-03-17','2027-03-19','3 дня · вариант2','TBA'),('2027-03-15','2027-03-19','5 дней','TBA')],price,'Private heated winterized family cabin.',sources=[src('Актуальные зимние смены и включённые ski passes',kf),src('2027: ценыTBA',kp)])
 ip=I+'camp-students-and-families/preparing-for-camp/';international=I+'summer-camp/admission/international-students-camp'
 intfaq=ip+'camp-international-faqs';tuition=I+'summer-camp/admission/tuition-and-financial-aid'
 rows=[('2027-06-27','2027-07-10','Session1','$5300'),('2027-07-11','2027-07-24','Session2','$5300'),('2027-07-25','2027-08-07','Session3','$5300')]
 price=dict(year=2027,label='$5300/2 недели +$65 невозвратная application fee. Код валюты на прочитанных страницах не установлен.',included='По pre-arrivalFAQ:room/board, classes, групповые и обязательные private lessons, recreation/performance access.',extras='ТранспортTVC/UM, материалы/инструмент по курсу и личные расходы отдельно. Airportpickup толькоTVC, неDetroit/Chicago.',deposit='Tuition до1 мая; отмену/депозит проверить отдельно. Priority15.01.2027; после — по местам/финансированию. Финансовая помощь не гарантирована.')
 for idx,name,url,programme in [(12,'Arts Exploration',I+'interdisciplinary-arts/camp-programs/grades-3-6','Театр/движение, творческое письмо, инструменты, visual art и экология. Междисциплинарная двухнедельная программа с чтениями/показами.'),(13,'Visual Arts',I+'visual-arts/camp-programs/grades-3-6/visual-arts','Четыре часа studio в день:рисунок/живопись, керамика, материалы. Итоговая выставка работ. Portfolio для этого младшего курса не требуется, first-come intake.')]:
  emit(idx,'Interlochen · Junior '+name,'USA','4000 J Maddy Parkway · Interlochen, Michigan','art,science' if idx==12 else 'art','boarding','Grades3–6 именно ДО лагеря; это не класс следующего сентября',programme,rows,price,'Пансионные cabins; родителям отдельное жильё. Посещение cabin детей не обещано.',
   mat=fit('conditional','Возраст9–10 совместим с младшими школьниками, но требуется фактический класс3–6 перед летом2027; год рождения не заменяет класс.'),osc=fit('later','Оскару6–7; стандартно раньше Grades3–6. Если фактический класс необычно высокий, индивидуальный допуск всё равно подтвердить.'),
   sources=[src('Именно Junior программа, даты/цена/приём',url),src('Иностранная application fee',international),src('2027 tuition/deadlines',tuition),src('Правила международного участника',intfaq),src('Включения, связь и техника',ip+'camp-pre-arrival-faqs')],
   questions=[ASK,'Оператор в ownFAQ пишет о student-status/I-20 и не допускаетB1/B2 для ArtsCamp. Для имеющегося/планируемого статусаE-2 семьи нужен индивидуальный ответ по выбранной программе; это не юридическое заключение. Academy ESL и школьный рейтинг не доказательство campEN/robotics. Junior laptops по общемуFAQ не разрешены.'])
 day=I+'day-camp';dr=[]
 for n in range(7):
  a=date(2027,6,21)+timedelta(days=7*n);b=a+timedelta(days=4);dr.append((a.isoformat(),b.isoformat(),'Неделя'+str(n+1)+' · тема2027TBA','$425/неделя в snapshot, цену2027 подтвердить'))
 price=dict(year=2027,label='Snapshot$425/неделя,$100deposit; ниже на странице остаются темы2026. Окончательную цену/договор2027 подтвердить.',included='Обед, лёгкий завтрак, перекус,T-shirt/lanyard и familyperformancepass описаны; состав2027 подтвердить.',extras='Опциональный busTraverseCity$50/неделя, семейное жильё/дорога отдельно.',deposit='Deposit100 невозвратный; опубликован refundдо1 июняминусdeposit, после нет. При смешанном2026/27 содержании не считать подписанным2027договором.')
 p=emit(14,'Interlochen · Arts Discovery Day Camp','USA','Interlochen Community Center · Michigan','general,art,science','day','7–12 и текущий2026–27 класс1–6, оба условия',
  'Недельный arts/outdoor day09:00–16:00, dropoff08:45–09:00/pickup16:00–16:15. Темы ниже страницы2026 не названы темами2027. Семейный performancepass — не гарантированное участие в платном концерте.',dr,price,'Без ночёвок; родители организуют жильё.',
  mat=fit('conditional','В диапазоне7–12; реальный класс1–6, иностранный приём/язык проверить.'),osc=fit('conditional','Только после7-летия и при классе1–6; до7 не соответствует минимуму. Нужна проверка на конкретную неделю.'),sources=[src('Snapshot2027 с оставшимися архивными темами2026',day)])
 for v in p['timing']['session_details']:
  v.update(date_precision='published_rule',date_rule='Собственный2027snapshot:7 недель, понедельник–пятница с21 июня по6 августа2027; семь недельных вариантов рассчитаны по этому правилу.',proof='2027snapshot и Mon–Fri rule; недельные темы2027 ещёTBA.',attendance_weekdays=['MO','TU','WE','TH','FR'])
 yr=Y+'enrollment-information/dates-fees.html'
 price=dict(year=2027,label='Две недели:$4200 normal; показаны скидки3250/3700/3400/2800 по сменам +обязательныйcanteen120. Условия скидки/валюта не установлены.',included='Пансионный tuition;canteen отдельно включаетT-shirt,стирку,перекусы.',extras='Linen rental35/2weeks;NYbus140/one-way;AVP70/EWR140/JFK180 one-way плюс внеофициальные даты;перелёты/UM отдельно.',deposit='Balance1мая; отмена250 до/на30апреля и500 после, но ownтекст опечатан. First-time proratedtuition guarantee требует условийpaperapplication;canteen не proratedrefund.')
 emit(15,'Camp Cayuga · Junior Campus / short sessions','USA','321 Niles Pond Road · Honesdale, Pennsylvania; PeapackNJ — winter office','general,sport,art','boarding','Camp6–16;JuniorCampus до13 и enteringGrades1–8. JuniorDivision:9 или младше/enteringGrades1–4',
  'Младшим структурированная ротация с counsellor, swiminstruction, спорт и creativearts. Старшим campus — иной free-choice режим. Матвей10/класс5 не автоматическиJuniorDivision, хотяJuniorCampus возможен. Робототехника не обещана.',
  [('2027-06-27','2027-07-10','Mini1','$4200 normal / $3250 displayed discount +$120'),('2027-07-11','2027-07-24','Mini2','$4200 / $3700 +$120'),('2027-07-25','2027-08-07','Mini3','$4200 / $3400 +$120'),('2027-08-08','2027-08-21','Mini4','$4200 / $2800 +$120')],price,
  'JuniorCampus с cabins; совместный домик требует одного enteringgrade, братьям не гарантирован.',sources=[src('2027 mini dates/rates +mandatorycanteen',yr),src('JuniorCampus и школьные классы',Y+'programs/junior-campus.html'),src('9-and-younger structuredJuniorDivision',Y+'programs/junior-division-activities.html'),src('Опциональные услуги',Y+'enrollment-information/optional-services.html'),src('First-time guarantee:границы',Y+'enrollment-information/first-time-camper-guarantee.html')])
 profiles[-1]['questions'] += ['First6weeks напечатаноSundayJune26,2027, хотя26июнясуббота и opening27июня. Этот спорный вариант не добавлен точнойсменой. Скидкаsibling100 дляmini не используется без подтверждения итогового счёта.']
 wf=W+'about-watitoh/dates-fees-faqs/'
 price=dict(year=2027,label='$14950/fullseason или$11500/first4weeks;кодвалюты не установлен.',included='Опубликованы стандартныеdeparture-pointtransports,canteen,sundries,laundry,scheduledtrips кромеSeniorovernights;пансионное питание описано.',extras='Golf/riding/tennisplus по500;специальнаяодежда/UM/перелёты/Seniortripsотдельно.',deposit='Earlycreditдо01.10.2026 уже истёк на дату проверки06.10; размер/депозит/отмена не установлены.')
 unknown=fit('unknown','Минимальный возраст на прочитанной собственной странице не установлен; иностранные участники не подтверждают зачисление этого ребёнка.')
 emit(16,'Camp Watitoh · Full Season / First Month','USA','1885 Main Street · Becket, Massachusetts;MaplewoodNJ — winteroffice','general,sport,art','boarding','Минимум/максимум возраста не установлен;4weeks только enteringGrade5 или ниже осеньюПОСЛЕ лагеря',
  'Общий co-edsleepaway:спорт,вода,приключения,creative/performancearts;cabingroup+choice. Internet-enableddevices не допускаются;это неcodingcamp. Первый звонокдиректорародителям в48часов,типичнаясвязьраз7–10дней;letters3разанеделю.',
  [('2027-06-26','2027-08-13','FullSeason','$14950'),('2027-06-26','2027-07-25','FirstMonth ·enteringGrade≤5','$11500')],price,'Традиционный пансион;посещение17.07.2027,безобещаниясемейногопроживания.',mat=unknown,osc=unknown,
  sources=[src('2027fees,grades,extras,communication',wf),src('Программа',W+'about-watitoh/program/'),src('First-timecampers',W+'about-watitoh/first-time-campers/')])
 # Readable spacing for new editorial prose, without modifying identifiers, URLs or old dossiers.
 def prose(v):
  if isinstance(v,str):
   v=re.sub(r'([А-Яа-яЁё])([A-Za-z0-9])|([A-Za-z0-9])([А-Яа-яЁё])',lambda m:' '.join(x for x in m.groups() if x),v)
   return re.sub(r'([,;])(?=\S)',r'\1 ',v)
  if isinstance(v,list):return [prose(x) for x in v]
  if isinstance(v,dict):return {k:(x if k in ['url','source','status','date_precision','date_scope','start','end'] else prose(x)) for k,x in v.items()}
  return v
 for p in profiles[-len(NEW):]:
  for k in ['provider','place','age','language','programme','price','accommodation','family_fit','editorial_reason','questions','sources']:
   p[k]=prose(p[k])
  p['timing']['label']=prose(p['timing']['label']);p['timing']['session_details']=prose(p['timing']['session_details'])

def extend_report_v122(r):
 r['shortlist'] += [dict(label='Канада · первая короткая ночёвка или family camp',slugs=['canaqua-shortstay','canaqua-day','canaqua-family','canaqua-parent-child','kandalore-one-week','kandalore-summer-family','kandalore-winter-family'],reason='УCan-Aqua конкретные5–11/5–15,семейнаяценадо5 и отдельнаяпара;уKandalore birthyear2017–2021. EN/валюту/допуск ещё подтвердить. Семейный формат может предшествовать самостоятельному пансиону.'),dict(label='Канада · тематический фильм и длительный пансион',slugs=['canaqua-film','canaqua-two-weeks','canaqua-four-weeks','kandalore-prep-junior'],reason='Film9–15 Матвеюкандидат,Оскарупозже;2wk6–14 обоим,4wk9–14 толькоМатвей. KandalorePrepJunior2016–2020 обоимпоyearofbirth,InternationaltariffнеDomestic.'),dict(label='США · arts и general с независимым школьным допуском',slugs=['interlochen-junior-exploration','interlochen-junior-visual','interlochen-arts-discovery','cayuga-junior-2027','watitoh-2027'],reason='InterlochenJuniorGrades3–6 ДОsummer,ArtsDiscovery7+иGrade1–6. CayugaJuniorCampusнеJuniorDivision;Watitoh4weeksкласс≤5ПОСЛЕsummer,ноminageнеустановлен. Это дополнительные творческие/generalпути,незаменаroboticsleague.')]
 for iso,name,url,detail in [('CAN','Can-Aqua',C,'Точные2027тарифы/даты,ноunknownвалюта/EN/налог/foreigncontract. Intro8–15/tablevs5–15text;short5–11vs5–12heading;2wk6–14vs6–15;4wk9–14vs9–15. Pair3June18–Sept20 неcalendar. Familycancelисключён,дневнойдепозитнеpanсионный.'),('CAN','Kandalore',K,'Direct4HTTP406;собственныеreader2027таблицыпрочитаны. Birthyears2017–2021/2016–2020;InternationalvsDomesticCanadaUSA. Новыеrefund/EN/currency/itineraryнепрочитаны;oldhandbooksне2027contract.'),('USA','Interlochen',I,'JuniorGrades3–6доsummer,неrisinggrade. Day7–12иcurrentgrade1–6;2027snapshotvs2026themes/pricingконтрактуточнить. OwnintFAQstudentstatusнеперсональноерешениедляE2;AcademyESLнеcampEN. Нетjuniorcollegecredit/rankingclaim.'),('USA','Cayuga',Y,'First6weeksJune26Sunday2027ошибка,неprecisecalendar. Normal/discount+mandatorycanteen;discounteligibility/currency/ENunknown. JuniorDivision9-and-younger/grade1–4vsJuniorCampus≤13/grades1–8. Guaranteeтолькоtuitionобычныеночныеcharges.'),('USA','Watitoh',W,'Минимальныйвозраст/EN/валюта/депозит/cancelunknown. Enteringgrade≤5дляfirstmonthпослеcamp. Earlycredit01.10ужеистёк. ТрадиционныеShabbatactivitiesoptionalдляnonJewishпоownFAQ.'),('USA','Camp Tamarack domain identity','https://www.camptamarack.com/','camptamarack.com ownbody говоритcentralOregonUSA;неOntarioCanada и неMichiganJewish t amarackcamps.com. Не создан слабыйканадскийcampprofile.'),('USA','Greeley/другие tech gaps','https://campgreeley.com/','DNSнеразрешён дляэтогоследа;неclaimprogrammeproof. НовыеNAgeneralпрограммынезакрываютrobotics/AI/CanadaLatAmпокрытие.')]:
  r['gaps'].append(dict(iso=iso,country='Канада' if iso=='CAN' else 'США',provider='v122 · '+name,url=url,detail=detail,next_action='Продолжить первичную проверку выбранных условий; весьмировойаудитостаётсяактивным.'))
