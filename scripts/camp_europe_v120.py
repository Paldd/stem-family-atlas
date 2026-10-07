"""Selected French and Spanish programmes, distinct ages, formats and fee scopes."""
from pathlib import Path
from camp_planning_v108 import offer
ROOT=Path(__file__).resolve().parents[1]
BASE='1be283ffca9dfd95a1f5f2802b996b9536ddcbe5'
CHECKED='2026-10-06'
NEW=['country-kids-family','pari-convention','pari-ranelagh','etopia-junior','etopia-middle','etopia-advanced','playcode-ulpgc']
K='https://www.country-kids.fr/'
P='https://pari-grandir.com/'
PC=P+'centres/convention/'
PR=P+'centres/ranelagh/'
PF=P+'wp-content/uploads/2022/05/convention-toussaint-26.pdf'
RF=P+'wp-content/uploads/2022/05/ranelagh-toussaint-26.pdf'
H='https://www.fundacionhiberus.com/'
E=H+'vocaciones-steam/etopia-kids/'
U='https://eii.ulpgc.es/es/noticia/La-ULPGC-acoge-el-Campus-Tecnologico-de-Verano-Aventura-STEM-Viaje-en-el-Tiempo-de-Play'
PLAY='https://playcodeacademy.com/campus-tecnologico-ulpgc-las-palmas-de-gran-canaria/'
EN='https://download.enforex.com/pdf/enforex-summercamps.pdf'
ASK='Подтвердить возраст на первый день, индивидуальный приём приезжающих иностранных детей, язык группы, место, полный счёт, страховку и условия отмены. Запросы, заявки и оплаты не отправлялись.'
UNKNOWN_LANG='Программа описана на испанском, но язык преподавателя и постоянная EN/ES/RU помощь группе прямо не обещаны. Английский интерфейс не доказательство английских занятий.'
AUTUMN=[['2026-10-19','2026-10-23'],['2026-10-26','2026-10-30']]

def add_europe_v120(add,src,fit,profiles):
 def emit(*a,**kw):
  add(*a,**kw);p=profiles[-1];p['checked']=CHECKED
  for s in p['sources']:s['checked']=CHECKED
  return p
 both=fit('conditional','Возраст подходит по годам рождения; точный возраст, конкретная смена, иностранный приём и места отдельно.')
 p=emit(NEW[0],'Country Kids · семейная английская программа','Франция','FRA','Le Mas Pandit · Octon 34800, Hérault / Occitanie','general,languages,sport,art,culture','family','Crèche с 3 месяцев; Kids Club до 12 лет; подросткам отдельная гибкая программа',
  'Оператор прямо называет англоязычную команду Crèche и Kids Club. Это язык детского сопровождения и активностей, не расписание академических уроков английского.',
  'Семейное проживание и детский outdoor club: ферма/животные, походы, поиски насекомых, творчество, садоводство, танцы, плавание и кулинария. Семь семей за неделю; общий заезд по субботам, только недельные Sat–Sat поездки. Родители живут вместе с детьми; обычный самостоятельный детский пансион не заявлен. Робототехника и ИИ не входят в прочитанную программу. Собственные награды и эпитеты «best» не независимый рейтинг.',
  'Сезон заявлен с апреля до первой недели сентября без годовых точных смен. Даты, доступность и тариф 2027 пока не установлены; зимой эту программу не обещать.',
  dict(year=None,label='От EUR 7 490 за семью из четырёх за неделю, год тарифа не указан. Это цена семейного проживания, а не 7 490 за каждого ребёнка.',included='Семейные апартаменты, питание/напитки по пакету, уборка/прачечная, детский club, две babysitting вечера, основные активности, две выездные активности на человека и spa treatment по описанию.',extras='FAQ исключает субботний обед и ресторанные ужины родителей по вторникам/четвергам; вечернее детское питание требует надзора родителей. Дорога и обязательная страховка отдельно. Дополнительный гость от EUR 1 000; применимость к возрасту и новый сезон подтвердить.',deposit='Текущий договор опубликован 10.12.2024: 30% при брони, остаток за 8 недель. Ранее 9 недель возврат только при перепродаже недели минус €300 и возможная разница цены; внутри 9 недель весь счёт остаётся обязательным. Применимость к выбранной поездке уточнить.'),
  'Семейные апартаменты, родители на месте и сохраняют ответственность. Договор требует сопровождающего взрослого для несовершеннолетних; соотношение drop-off club и участия родителя в отдельных активностях уточнить. Полная holiday insurance обязательна, запрашивается доказательство покрытия.',both,both,
  'Кандидат для общего английского семейного отдыха обоим; опубликованная цена семьи и возраст клуба понятны. Полного тарифа и календаря 2027 ещё нет.',
  [ASK,'Получить семейный состав пакета, точную неделю, цены ресторанов/дороги/страховки и границы родительского надзора.'],
  [src('Пакет и семейная цена',K+'packages-holidays-to-south-of-france/'),src('Англоязычная команда / возраст / активности',K+'for-the-kids-child-friendly-holidays-in-south-of-france/'),src('FAQ: недельный формат и исключения питания',K+'faq-family-farm-holidays-france/'),src('Депозит / отмена / взрослый / обязательная страховка',K+'terms-and-conditions-of-sale/')],priority=['both','general'],confirmed=['EN'])
 p['language_evidence_role']='camp_life'
 for slug,name,url,pdf,age,base,second,lunch,mfit,ofit in [
  (NEW[1],'Pari-Grandir · Paris Convention',PC,PF,'3–10; до 27 детей',450,337,'Обед Ekilibre и snack включены.',both,both),
  (NEW[2],'Pari-Grandir · Paris Ranelagh',PR,RF,'3–6; до 16 детей',395,296,'Lunchbox приносят родители; snack включён.',fit('not_eligible','Матвею 8–9 в 2026 и 9–10 в 2027, выше максимума именно Ranelagh 3–6. Общий виджет3–10 не расширяет допуск этого центра.'),fit('conditional','Оскару 5–6 в 2026: возраст подходит. В 2027 6–7 — Ranelagh только пока ему 6; после 7-летия выбрать Convention 3–10.'))]:
  p=emit(slug,name,'Франция','FRA','11 rue du Clos Feuquières, Paris15' if slug==NEW[1] else '49 rue du Ranelagh, Paris16 · помещения At Montessori',
   'general,languages,science,art,sport,culture','day',age,
   'Активности прямо на FR и EN, English Club с англоязычными ведущими; группы по возрасту и уровню. Это двуязычная программа, не полностью английский учебный день.',
   'Общие каникулы с English Club, культурой, творчеством, театром, парком/спортом и простыми научными опытами. Осенью первая тема — мировые чудеса, вторая — Haunted Manor. PDF содержит дневной план; 08:15–19:00, понедельник–пятница. Экскурсии зависят от возраста и подтверждения; программа может меняться. Робототехника/ИИ и международный соревновательный результат не заявлены.',
   'Именно этот центр публикует 19–23 и 26–30 октября 2026. Сеть также объявляет 21–24 декабря 2026, 15–26 февраля, 12–23 апреля, 5–30 июля и 23–27 августа 2027, но доступность зависит от центра: не переносить эти окна в точные смены каждого филиала.',
   dict(year=2026,season='2026–2027',label=f'Полная неделя: € {base} первый  / € {second} второй ребёнок по напечатанной таблице. '+('Четыре дня: €360 / €270; один день: €105 / €79.' if slug==NEW[1] else 'Четыре дня: €316 / €237; один день: €89 / €67. Скидки учащихся At Montessori внешней семье не подставлять.'),included='Материалы/занятия/выходы и snack. '+lunch,extras='Поездка, жильё родителей и страхование отдельно. Цены до налогового кредита; льготу50% семье-туристу автоматически не применять. Летние multi-day скидки и совместимость со sibling price требуют отдельного расчёта.',deposit='Регистрация закрепляется оплатой/подтверждением списания. Возврат отсутствий — по медсправке; без неё услуга оплачивается. Годовой контракт afterschool и его трёхмесячное уведомление не подменяют holiday cancellation.'),
   'Дневной лагерь; семье отдельное жильё и ежедневный pickup. '+lunch,mfit,ofit,
   'Convention — ближайший двуязычный дневной кандидат обоим.' if slug==NEW[1] else 'Ranelagh — отдельный младший вариант Оскару; Матвею в этом центре места по возрасту нет.',
   [ASK,'Подтвердить выбранный holiday centre, доступность позже осени, аллергию/обед и отмену до первого дня.'],
   [src('Возраст именно центра / язык / питание',url),src('Осень и тариф2026–27',pdf),src('Календарь сети: центры открываются по-разному',P+'bonne-rentree-a-tous/')],status='published_2026_27',sessions=AUTUMN,priority=['both','general'] if slug==NEW[1] else ['general'],confirmed=['EN','FR'])
  p['language_evidence_role']='bilingual'
  p['timing']['session_details']=[dict(start=a,end=b,label=label,price=f'€ {base}/ребёнок/неделя; второй{second} при соблюдении условий',place=p['place'],source=pdf,date_scope='day_camp_window',entry='Индивидуальная holiday registration; возраст/место и иностранный приём отдельно.',programme=p['programme']) for (a,b),label in zip(AUTUMN,['Wonders of the World','Haunted Manor'])]
 groups=[
  (NEW[3],'Etopia Kids · junior robotics / animation','6–8','robotics,coding,art',
   'ExploraBOTS: собрать/программировать робота, датчики и данные; Universo Animado: цифровые персонажи/истории/анимация.',
   fit('not_eligible','В новом 2027 сезоне Матвею9–10, выше junior6–8. В архивном 2026 мог подходить только пока ему8.'),fit('conditional','В 2027 Оскару6–7: возрастной кандидат junior6–8, но новый набор и язык ещё неизвестны.')),
  (NEW[4],'Etopia Kids · games / space / science','8–11','coding,games,robotics,science',
   'SectorGAME: персонажи, правила и игровые уровни; MisiónÓRBITA: спутники и управление космическими роботами; CienciaLand: эксперименты.',both,fit('later','Оскару в 2027 максимум7; минимум 8. Не включать в треки8–11.')),
  (NEW[5],'Etopia Kids · autonomous robotics / AI / cybersecurity','10–13','robotics,coding,ai,engineering',
   'Escuadrón Robótico: механика/датчики, блочное и текстовое мышление, автономные задачи, follows-line/robotarms. AgenciaSecreta: защита информации/код/криптография. FrecuencIALAB: ИИ/голос/музыка/звук.',fit('conditional','Матвею в 2027 9–10: эта ступень только после 10-летия; не старые8–11 тарифы/задания.'),fit('later','Оскару в 2027 6–7, минимум 10; это будущая ступень.'))]
 for slug,name,age,themes,content,mfit,ofit in groups:
  p=emit(slug,name,'Испания','ESP','Etopia · Av. Ciudad de Soria8, Zaragoza / Delicias',themes,'day',age,UNKNOWN_LANG,
   content+' Десять тематических itineraries всей сети с возрастами6–8/8–11/10–13/12–15; ChampionsTech и NúcleoCÓDIGO с12 лет не подходят обоим сейчас. Один трек длится неделю; при повторе того же itinerary содержание повторяется, поэтому оператор не советует повторять его несколько недель. 09:00–14:00, приём08:50–09:00; ранний час08:00–09:00 и обед14:00–15:00 отдельно. Предварительных знаний не требуется. Команда/помещения фонда и Academia de Inventores не академические университетские кредиты.',
   'Архив 2026: 22–26 июня, 29 июня–3 июля, 6–10, 13–17 и 20–24 июля, 31 августа–4 сентября. Эти смены завершились; новые даты2027 не опубликованы и не сдвигаются автоматически.',
   dict(year=2026,label='€130/неделя2026; ранний час€5/неделя, обед€27 за 5 дней. Это архивные цены, не смета2027.',included='Недельный тематический itinerary; полный список материалов/оборудования и ownership не опубликован.',extras='Вода/snack свои; email перед стартом перечисляет вещи, в том числе pendrive. Конкретные kits, loan/buy/забрать модель и язык техники неизвестны. Обед и early отдельно.',deposit='Ранний10% до 3 мая 2026 истёк. Поздний10% sibling code выдавали после первой отдельной покупки; не скидка автоматически на обе первые заявки. Возврат/страховка/2027 invoice не установлены.'),
   'Дневной формат в Сарагосе; детские ночёвки не заявлены, жильё семьи отдельно.',mfit,ofit,
   'Подробно описанная техническая ступень под возраст; пока наблюдение за новым набором, а не готовая2027 поездка с подтверждённым английским.',
   [ASK,'Получить новый 2027 itinerary, язык учителя/safety, иностранный индивидуальный вход, kit/часы и refund.'],
   [src('Десять itineraries / возраст / даты / цены2026',E),src('Подробная продвинутая робототехника10–13',H+'itinerarios/escuadron-robotico/'),src('Участие Academia de Inventores / City Zaragoza',H+'politica-de-privacidad-etopia-kids/')],status='archive_next_unannounced',priority=['technical'])
 p=emit(NEW[6],'PlayCode Academy · ULPGC Aventura STEM','Испания','ESP','Escuela de Ingeniería Informática · ULPGC Campus Tafira, Las Palmas de Gran Canaria','robotics,coding,engineering,science,games','day','6–16; задания по возрасту/уровню',UNKNOWN_LANG,
  'Первичный сайт университета описывает time-travel STEM: drones для археологических карт, robots-painters и prehistoric alert systems. Названы LEGO, Arduino, Micro:Bit, Edison, drones, Delightex, design/3D printing; распределение по младшему возрасту и право забрать hardware не установлены. 09:00–14:00 в помещениях школы информатики; ограниченные места. Страница сети PlayCode перечисляет другие университетские площадки, но некоторые карточки2024/finished: это не единая открытая смена2027 и не поступление в университет.',
  'Анонс университета от 5 июня 2026: первая смена 22, 23, 25, 26 июня — четыре дня без 24 июня; затем 29 июня–3 июля и 6–10 июля 2026. Архив, новый 2027 календарь не установлен.',
  dict(year=2026,label='€135 внешнему участнику /115 сотруднику ULPGC в анонсе2026; sibling discount без величины. Длительность, к которой относится цена, требует проверки — не сумма за все три смены.',included='Практические STEM workshops и технологические инструменты по объявлению; полный пакет не перечислен.',extras='Питание, материалы на вынос, собственный компьютер, страховка, early/late pickup и трансфер неизвестны.',deposit='Прямой HTTP обоих PlayCode URLs завершился DNS ошибкой; университетская полная программа прочитана. Условия брони/возврата и места2027 не подтверждены.'),
  'Дневной campus, ночёвок детям и родителям не обещает. Жильё семьи на Gran Canaria отдельно.',both,both,
  'Технический кандидат обоим с университетским первичным описанием и названным hardware. Свежий операторский набор, язык и полный тариф ещё нужны.',
  [ASK,'Проверить новый сезон, единицу тарифа, младшую группу, язык и договор оператора; место проведения не университетский диплом.'],
  [src('Полный первичный анонс ULPGC / возраст / hardware / цена',U),src('Операторская страница: прямая загрузка недоступна',PLAY)],status='archive_next_unannounced',priority=['both','technical'])

def extend_report_v120(r):
 r['shortlist'] += [
  dict(label='Франция · семья и ближайшие двуязычные каникулы',slugs=NEW[:3],reason='Country Kids: родители живут вместе с детьми, англоязычная команда и семейная цена от7490 без года. Convention 3–10 подходит обоим; Ranelagh 3–6 только Оскару, затем другой центр. Два точных осенних дневных блока и отдельные тарифы/питание.'),
  dict(label='Испания · технические ступени Etopia / ULPGC',slugs=NEW[3:],reason='Архив 2026 отдельно от будущего2027. Etopia6–8 Оскару;8–11 Матвею;10–13 только после 10-летия. ULPGC6–16 обоим с конкретным hardware. Язык преподавания и новый иностранный набор пока неизвестны.')]
 for iso,country,provider,detail,url in [
  ('FRA','Франция','Country Kids семейный пакет','Англоязычный club и pricefrom7490/family4/week установлены. Нет годового2027 тарифа/смен и полномочия сдавать детей в самостоятельный пансион; guardian/club границы и включения ужинов уточнить.',K+'terms-and-conditions-of-sale/'),
  ('FRA','Франция','Pari-Grandir network vs venue','Общая страница публикует winter/spring/summer2027 по центрам. Точный календарь конкретного venue после осени и внешний иностранный приём ещё проверить. Ranelagh 3–6 не общий3–10; Convention450/337 с lunch не395/296 с lunchbox.',PC),
  ('ESP','Испания','Etopia Kids новый сезон и язык','Подробные2026 itineraries/возраста не новый 2027 набор;10% ранний срок истёк. EN/ESучитель,safety,foreignintake,полныйinvoice/kit и cancellation неизвестны.',E),
  ('ESP','Испания','PlayCode ULPGC','Первичный университетский анонс2026 прочитан, оба прямых PlayCode URLs DNSerror. Сетевые campus-карточки смешивают2024/2026. Новые2027 даты/язык/единица цены и операторский договор ещё нужны.',PLAY)]:
  r['gaps'].append(dict(iso=iso,country=country,provider='v120 · '+provider,detail=detail,next_action='Продолжить первичную проверку выбранного нового сезона и индивидуального допуска; неизвестные цены/язык/места не считать подтверждёнными.',url=url))

NEW_IDS=['enforex-madrid-two-day','enforex-madrid-two-board','enforex-elviria-two-day','enforex-elviria-two-board','enforex-salamanca-two-day','enforex-salamanca-two-board','pari-convention-autumn-week','pari-ranelagh-oscar-week']
def build_offers():
 out=[]
 for city,title,base,starts in [('madrid','Madrid',2495,['2027-07-04','2027-07-18','2027-08-01']),('elviria','Marbella Elviria',2095,['2027-07-04','2027-07-18','2027-08-01','2027-08-15']),('salamanca','Salamanca',2095,['2027-07-04','2027-07-18'])]:
  import datetime as dt
  shift=lambda s,n:(dt.date.fromisoformat(s)+dt.timedelta(days=n)).isoformat()
  for fmt in ['day','board']:
   slug='enforex-'+('marbella-elviria' if city=='elviria' else city)+'-'+fmt
   sessions=[[shift(s,1),shift(s,12)] if fmt=='day' else [s,shift(s,13)] for s in starts]
   options=[dict(id='local_roundtrip',label='Местный аэропорт/станция туда-обратно · 95 × 2 × 2 ребёнка · маршрут подтвердить',amount=380),dict(id='cancellation_guarantee',label='Cancellation guarantee · 300 × 2 недели × 2 ребёнка · условия отдельно',amount=1200)]
   if city!='salamanca' and fmt=='day':options.append(dict(id='daily_bus',label='Bus-stop transfer на2 недели · 250 × 2 ребёнка · маршрут подтвердить',amount=500))
   if city=='salamanca':
    options=[q for q in options if q['id']!='local_roundtrip']
    options.append(dict(id='madrid_shuttle',label='Madrid↔Camp shuttle · 220 × 2 ребёнка · маршрут подтвердить',amount=440))
   out.append(offer('enforex-'+city+'-two-'+fmt,slug,f'Enforex {title} · оба · 2 недели · '+('день' if fmt=='day' else 'пансион'),1200 if fmt=='day' else base,currency='EUR',price_year=2027,checked=CHECKED,format='day' if fmt=='day' else 'boarding',sessions=sessions,sources=[EN],
    required=[dict(id='application',label='Регистрация · 35 × 2 ребёнка · если ещё не оплачена в текущие12 месяцев',amount=70)],
    unknown_required=[dict(id='invoice_extras',label='Оставшиеся обязательные доплаты / достаточность страховки обоих · подтвердить',unit='amount',rate=1,min=0)],optional=options,
    gate='Именно Madrid/Elviria/Salamanca International5–18: оба по годам рождения подходят, нужны возрастная группа, languageplacement и место. Это детский лагерь, не Young Adults 16–21 с50% сопровождение. '+('Посещение пн–пт09:00–20:00: показаны реальные будние границы, а не воскресный заезд пансиона. Выходные отдельно.' if fmt=='day' else 'Пансион: воскресный заезд и субботний выезд, заявлено100% сопровождение; распределение младших комнат/ночной уход уточнить.')+' В Madrid нет смены 15–28 августа; в Salamanca нет смен в августе. Семейное размещение с 14 лет не подходит обоим.',
    included='20 уроков EN или ES по45 минут в неделю (=15 часов), study materials, workshop/sport/excursions. '+('Lunch, будние активности; жильё не входит.' if fmt=='day' else 'Sharedroom, питание икруглосуточное сопровождение.')+' P33 обещает travelhealthinsurance; p35 описывает ограничения и своё дополнительное покрытие — применимость к семье/формату ещё проверить. Язык уроков не обещание полностью английских sport/activities. Сертификат посещения не международная победа.',
    deposit_note='Summer-specific: при брони менее 4 недель весь счёт сразу; штраф €850 внутри 4 недель; внутри 2 недель и после старта возврата нет. Общие условия содержат €250 невозвратный депозит и другие удержания: применимость к детскому договору подтвердить, депозит не прибавляется к базе. Optional guarantee не обещает возврат всей поездки/доплат, есть основания и административные удержания.',
    scope='Опубликованная часть цены двоих за2 недели плюс регистрация70, если fee ещё не оплачен. Тариф35 действует12 месяцев, не пожизненно. Перелёт/жильё родителей и неизвестные обязательные расходы отдельно. Местный transfer95 не маршрутMadrid→Salamanca; shuttle220 альтернативный, не выбирать оба для одной дороги.'))
 out.append(offer(NEW_IDS[6],NEW[1],'Pari Convention · оба · 1 осенняя неделя',450,currency='EUR',price_year=2026,checked=CHECKED,format='day',sessions=AUTUMN,base_by_child=dict(matvey=450,oscar=337),sources=[PC,PF],
  unknown_required=[dict(id='insurance_extras',label='Страхование и прочие обязательные доплаты обоих · подтвердить',unit='amount',rate=1,min=0)],
  gate='Convention 3–10, оба подходят по годам; уточнить точный возраст и иностранный приём. EN/FR bilingual, 08:15–19:00, будни. Не тариф Ranelagh 3–6.',included='Занятия/материалы/выходы, обед Ekilibre и snack.',deposit_note='Место закрепляется оплатой; медицинская справка требуется для возврата отсутствия. Отмена до старта ещё уточнить. Налоговый кредит50% не применён.',scope='€787 = 450 + 337 по напечатанному таблице для второго ребёнка, без округления450 × 0,75 и без второй скидки. Это одна осенняя неделя2026; зимние/летние даты конкретного центра отдельно.'))
 out.append(offer(NEW_IDS[7],NEW[2],'Pari Ranelagh · только Оскар · 1 осенняя неделя',395,currency='EUR',price_year=2026,checked=CHECKED,format='day',sessions=AUTUMN,children=['oscar'],base_by_child=dict(oscar=395),sources=[PR,RF],
  unknown_required=[dict(id='lunch_cover',label='Lunchbox и страхование Оскара · семейная стоимость',unit='amount',rate=1,min=0)],
  gate='Строго Ranelagh 3–6: Оскар5–6 осенью2026 кандидат, Матвей старше максимума. В 2027 Оскар только до 7-летия; цена не подтверждает место.',included='Двуязычные занятия/материалы/выходы и snack; обед приносят родители.',deposit_note='Оплата закрепляет регистрацию; возврат отсутствий по медсправке. Школьный At Montessoridiscount к внешней семье не применён.',scope='€395 — только Оскар за одну неделю, а не два ребёнка. Другой лагерь/уход и расходы Матвея в сумме отсутствуют. Обед/семейное жильё/поездка отдельно.'))
 assert [q['id'] for q in out]==NEW_IDS
 return out

def extend_planning_v120(d):
 m=d['camp_planning'];out=build_offers();existing={q['id'] for q in m['offers']};byid={q['id']:q for q in out}
 m['offers']=[byid.get(q['id'],q) for q in m['offers']]+[q for q in out if q['id'] not in existing]
 m.update(version=120,asof=CHECKED)
