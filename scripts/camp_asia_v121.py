"""Selected new Asian programme dossiers; no accepted intake or global ranking claim."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='a3550580bcc331e37778ea6836e35a947a040d56'
CHECKED='2026-10-06'
R='https://roboto.sg/'
M='https://www.malverncollegetokyo.jp/summer-programme-2026/'
BC='https://www.malverncollegetokyo.jp/wp-content/uploads/2026/04/BritishCouncilSummerEnglishCourse_E.pdf'
T='https://tka.com.tw/zh_tw/theme-camps/'
O='https://www.onestepinitiative.com/'
C='https://www.cognitivesystems.academy/holiday-workshop-singapore'
J='https://www.connectedu.com/magazine-post/jeju-global-it-camp-_-ru'
JEN='https://www.connectedu.com/magazine-post/jejuglobalitcamponlineseminar_eng'
FIVE=[['2026-11-23','2026-11-27'],['2026-11-30','2026-12-04'],['2026-12-07','2026-12-11'],['2026-12-14','2026-12-18']]
THREE=[['2026-11-23','2026-11-25'],['2026-11-30','2026-12-02'],['2026-12-07','2026-12-09'],['2026-12-14','2026-12-16']]
TWO=[['2026-11-26','2026-11-27'],['2026-12-03','2026-12-04'],['2026-12-10','2026-12-11'],['2026-12-17','2026-12-18']]
ROBOTO=[
 ('junior-developer','Junior AI Developer','7–8','09:00–12:00',FIVE,450,390,'15 часов / 5 полудней','robotics,coding,ai,science','Игровая логика, VR-миры, программирование робота с датчиком близости, Minecraft Education и генеративные истории.'),
 ('junior-inventor','Junior AI Inventor','7–8','13:00–16:00',FIVE,450,390,'15 часов / 5 полудней','robotics,coding,ai,science','Dash, механизмы LEGO, Minecraft, игры в Roblox Studio и короткий фильм с генеративным ИИ.'),
 ('junior-coder','Junior Coder','7–8','09:00–16:00',THREE,600,540,'21 час / 3 дня','robotics,coding,science','По дневному плану: игровая логика, VR, Dash, сборка LEGO, робот с датчиком близости и Minecraft. Отдельное занятие ИИ в расписании не выделено.'),
 ('junior-futurist','Junior AI Futurist','7–8','09:00–16:00',FIVE,950,890,'35 часов / 5 дней','robotics,coding,ai,science','Роботы, VR, Minecraft, Roblox, игровая логика, генеративные истории и создание фильма.'),
 ('junior-creator','Junior AI Creator','7–8','09:00–16:00',TWO,420,360,'14 часов / 2 дня','coding,ai,art','Minecraft Education, Roblox Studio, генеративные истории и фильм. Физическая робототехника в этом двухдневном треке не заявлена.'),
 ('young-developer','Young AI Developer','9–12','09:00–12:00',FIVE,450,390,'15 часов / 5 полудней','robotics,coding,ai,science','Scratch, сборка LEGO SPIKE Prime с датчиками/моторами, генеративные материалы, Minecraft и Roblox Studio.'),
 ('young-inventor','Young AI Inventor','9–12','13:00–16:00',FIVE,450,390,'15 часов / 5 полудней','robotics,coding,ai,science','mBot: линия/препятствия, мобильные приложения, Roblox Studio, Minecraft Education и генеративные медиа.'),
 ('young-coder','Young AI Coder','9–12','09:00–16:00',THREE,600,540,'21 час / 3 дня','robotics,coding,ai,science','Scratch, mBot, LEGO SPIKE Prime, мобильные приложения, генеративные материалы и Roblox Studio.'),
 ('young-futurist','Young AI Futurist','9–12','09:00–16:00',FIVE,950,890,'35 часов / 5 дней','robotics,coding,ai,science','Scratch, mBot, LEGO SPIKE Prime, мобильные приложения, ИИ, Roblox и Minecraft Education.'),
 ('young-creator','Young AI Creator','9–12','09:00–16:00',TWO,420,360,'14 часов / 2 дня','coding,ai,art','Minecraft Education, игровые миры и программируемые агенты, Roblox Studio и генеративные медиа. Физический робот не заявлен.')]
NEW=['roboto-'+q[0] for q in ROBOTO]+['taipei-kids-theme-camps','one-step-maker','malvern-tokyo-arts','malvern-tokyo-orchestra','malvern-tokyo-musical','malvern-tokyo-british-council','csa-space-challenge','connected-jeju-global-it']
ASK='Уточнить новый набор, возраст/класс на начало, индивидуальный иностранный приём, язык группы, итоговый счёт, оборудование, страховку и отмену. Заявки не отправлялись.'

def add_asia_v121(add,src,fit,profiles):
 def emit(*a,**kw):
  add(*a,**kw);p=profiles[-1];p['checked']=CHECKED
  for s in p['sources']:s['checked']=CHECKED
  return p
 both=fit('conditional','Оба подходят по годам рождения; новый сезон, возрастная группа и иностранный приём ещё не подтверждены.')
 for key,name,age,hours,sessions,normal,early,duration,themes,programme in ROBOTO:
  junior=key.startswith('junior');full=hours=='09:00–16:00';url=R+'holiday-camp-'+key
  p=emit('roboto-'+key,'Roboto · '+name,'Сингапур','SGP','Novena · Goldhill Centre или Tampines · напротив Tampines Hub: выбрать один центр',themes,'day',age+' лет, именно holiday track',
   'Прочитано английское описание, но прямое обещание языка преподавания для этого заезда не найдено. EN пока не подтверждён.',
   programme+' '+duration+'; '+hours+'. На странице курса соотношение ведущих 1:4–6; это обзорный дневной курс.',
   'Четыре опубликованных варианта ноября–декабря 2026; каждый предлагается в Novena и Tampines. В календаре одна запись курса/недели с выбором центра, не удвоение числа лагерей. Набор 2027 ещё не опубликован.',
   dict(year=2026,label=f'$ {normal} обычный / $ {early} early bird за ребёнка и трек. Код валюты и срок скидки не установлен; скидка не гарантирована.',included='Занятия. '+('Обед прямо включён на странице курса.' if full else 'Обед для этого полудневного пакета не обещан.'),extras='Ноутбук/аренда, налоги, транспорт, страховка и владение наборами уточнить; полный счёт неизвестен.',deposit='Условия оплаты и отмены именно holiday camp пока не установлены.'),
   'День, без ночёвок; родители организуют жильё и доставку.',
   fit('conditional','В ноябре–декабре 2026 Матвею 8–9: '+('Junior допустим только пока ему 8; после 9-летия нужен Young 9–12. В 2027 Junior уже младше его возраста.' if junior else 'Young допустим после 9-летия; до него нужен Junior 7–8.')),
   fit('not_eligible','Оскару 5–6 в ноябре–декабре 2026, ниже минимума 7. Общий FAQ о детях с 5 лет не разрешение на этот лагерь; будущий набор отдельно.'),
   'Сравнивать по длительности, содержанию и возрасту; английский, индивидуальный допуск и места ещё проверить. Учебный проект не международная победа.',
   [ASK,'FAQ о еженедельных занятиях требует свой ноутбук и обещает иной instructor ratio; условия holiday track не переносить автоматически.'],
   [src('Именно этот курс: программа, цена и смены',url),src('Выбор holiday tracks',R+'holiday-camp'),src('FAQ: отдельные условия weekly courses',R+'faq')],status='published_2026',sessions=sessions)
  p['timing']['session_details']=[dict(start=a,end=b,label=name+' · выбрать Novena или Tampines',place=p['place'],price=p['price']['label'],source=url,date_scope='camp_session',date_precision='published_session',proof='Точные даты на собственной странице курса прочитаны через первичный web reader; прямой HTTP вернул 406. Наличие места и английский не подтверждены.') for a,b in sessions]
 p=emit(NEW[10],'Taipei Kids Academy · Summer / Winter Theme Camps','Тайвань','TWN','520 Ren’ai Road, Section4 · 1–2F · Xinyi, Taipei',
  'general,languages,science,art,culture','day','3–12; максимум 16, один англоязычный и один китайскоязычный преподаватель',
  'Основные занятия на EN; около 20% специальных художественных занятий на китайском. Это двуязычная программа, не весь день на английском.',
  'Тематические недели: природа, вода, загадки, путешествия и творчество. Есть экскурсии и дополнительные elective занятия; робототехника как отдельный курс не подтверждена. Полный день 08:00–16:30, присмотр до 18:00; half-day08:00–12:30.',
  'Собственная страница: зима 21.01–03.02.2026, лето июль–август 2026. Всё в прошлом; зимой/летом 2027 новых точных дат ещё нет.',
  dict(year=2026,label='Основной тариф не установлен в прочитанных первичных материалах.',included='Экскурсии входят в структуру/расчёт курса; полный состав питания уточнить.',extras='Electives и поздний pickup отдельно; стоимость не установлена.',deposit='Отмена: невозвратные NT$1 000; внутри месяца ещё NT$1 200 за смену для экскурсий. Остаток по местным правилам; отсутствие не денежный возврат.'),
  'Дневной формат; семейное жильё отдельно.',both,both,'Возраст обоим подходит; основной английский подтверждён, китайский художественного блока требует решения.',[ASK],
  [src('Текущая первичная страница: язык, возраст и правила',T),src('Летние темы 2026: первичный reader, прямойURL404','https://tka.com.tw/en/summer-camp-2026/')],status='archive_next_unannounced',priority=['both','general'],confirmed=['EN','ZH'])
 p['language_evidence_role']='bilingual'
 p=emit(NEW[11],'One Step Initiative · Maker × STEAM','Тайвань','TWN','Taipei · точный venue не установлен','science,coding,art','day','12–16',
  'Оператор прямо описывает среду Chinese/English bilingual; постоянную персональную английскую помощь подтвердить.',
  'Dragon Habitat: модель, свет и электронные цепи; Pocket Game: 3D-моделирование/печать и механика; Paper Circuits: LED и интерактивная бумага. Проект можно забрать. Небольшие поддерживающие группы с разным темпом обучения.',
  'Пилот июля 2026:7–9,14–16 и выходные 11–12/18–19,13:00–16:00. Архив, не новый набор 2027.',
  dict(year=2026,label='Бесплатный ограниченный пилот 2026; будущая бесплатность не обещана.',included='Описанные занятия и собственная готовая поделка.',extras='Поездка/жильё/доплаты нового сезона неизвестны.',deposit='Форма/опрос о потребностях, индивидуальное подтверждение; согласие на съёмку отдельно.'),
  'Короткие дневные занятия; пансион не заявлен.',fit('later','Матвею ещё нет 12.'),fit('later','Оскару ещё нет 12.'),
  'Технический вариант на будущий возраст, не текущая рекомендация обоим.',[ASK],[src('Возраст, bilingual, curriculum и бесплатный пилот',O)],status='archive_next_unannounced',confirmed=['EN','ZH'])
 p['language_evidence_role']='bilingual'
 arts=[
  (NEW[12],'Prep Summer Arts','5–11 · Prep 1–6','13–17 июля 2026',88000,'5 дней','Музыка, танец, театр и визуальное искусство, совместный итоговый показ.',both,both,'https://cdnm.heyzine.com/files/uploaded/v3/d984a19c99c2768ae07e7d669587b55bd19b7da0-2.pdf'),
  (NEW[13],'Orchestra','8–12 · Prep 4–FY1','20–24 июля 2026',88000,'5 дней','Оркестровые/секционные репетиции, индивидуальная работа и итоговый концерт.',fit('conditional','Возраст Матвея подходит; Prep 4–FY1, инструмент и уровень отдельно.'),fit('later','Оскару ещё нет 8; учебная ступень тоже ограничена.'),'https://cdnm.heyzine.com/files/uploaded/v3/bc3b47a5d6601e75e0b69f16bdd71d6b6c2dd9e6.pdf'),
  (NEW[14],'Musical Academy','10–18 · Prep 6 и старше','20–31 июля 2026',176000,'2 недели','Актёрская игра, пение, танец, декорации/костюмы и совместный музыкальный спектакль.',fit('conditional','Матвею только после 10-летия и при соответствии Prep 6; возраст сам по себе не даёт допуск.'),fit('later','Оскару ещё нет 10.'),'https://cdnm.heyzine.com/files/uploaded/v3/af69653dd27b73af54c16778503d1249d7128304.pdf')]
 for slug,name,age,dates,fee,unit,programme,mat,osc,pdf in arts:
  emit(slug,'Malvern College Tokyo · '+name,'Япония','JPN','3–2–1 Josuiminamicho · Kodaira · Tokyo','general,art,languages','day',age,
   'Брошюра ставит целью развитие коммуникации на английском, но язык каждого занятия прямо не гарантирован; EN-only ещё уточнить.',
   programme+' Будни 09:00–15:00; техническая программа UK Malvern сюда не перенесена.',
   dates+'; собственная страница помечает Full. Прошедший закрытый набор; даты/места 2027 не объявлены.',
   dict(year=2026,label=f'JPY {fee:,} за {unit}; внешний registration fee JPY 12 100 отдельной строкой, единица семья/ребёнок требует уточнения. Налог 10% включён.',included='Обучение выбранного курса.',extras='Обед JPY5 500/неделю либо lunchbox. Инструмент/материалы/поездка/страховка и жильё отдельно проверить.',deposit='Дедлайн 06.05.2026; полный возврат до 07.05.2026, затем нет. Частичное посещение без скидки. Новый 2027 договор неизвестен.'),
   'День, родители организуют ночёвки.',mat,osc,'Кандидат на художественный отдых после нового анонса, не робототехнический интенсив.',[ASK],
   [src('Школьный обзор с отметкой Full',M),src('Собственная брошюра: программа/возраст/цена/отмена',pdf)],status='archive_next_unannounced')
 p=emit(NEW[15],'British Council × Malvern College Tokyo · English + Clubs','Япония','JPN','Malvern College Tokyo · Kodaira','general,languages,science,art','day','6–9: Primary Plus 2 6–7 / Plus 3 8–9;12–16 детей в группе',
  'Утренний английский British Council и дневные science/craft/roleplay Clubs прямо на EN.',
  'Истории и разговорные задачи утром; затем творческие клубы, научные опыты и командные задания.09:30–15:30; уровни чтения/письма описаны отдельно. Родители могут наблюдать последнюю часть финального дня.',
  '21–24 июля 2026 — четыре дня;27–31 июля 2026 — пять. Архив; календарь 2027 пока неизвестен.',
  dict(year=2026,label='Внешние non-MCT pupils: JPY75 600/4 дня или 92 000/5 дней, с налогом. Школьные 65 600/82 000 не тариф нашей семьи.',included='Уроки и English Clubs.',extras='Lunchbox или school lunch JPY4 400/4 дня и 5 500/5 дней; жильё/дорога/страховка отдельно.',deposit='После подтверждения: отмена до 14.05.2026 0%,15.05–14.06 30%,15–30.06 70%, с 01.07 100%. При незапуске группы полный возврат; не договор 2027.'),
  'День; ночёвки не заявлены.',fit('conditional','Матвей 9–10 в 2027: если предел 6–9 сохранится, только до 10-летия; новый возрастной набор и уровень ещё нужны.'),fit('conditional','Оскар 6–7 в 2027: предварительно младшая группа, новый сезон и письменный уровень ещё проверить.'),
  'Прозрачный архив английской программы; не нужно покупать начальный язык, если уровень детям слишком простой.',[ASK],
  [src('Программа и группы',M),src('Возраст, внешний тариф, уровни и отмена',BC)],status='archive_next_unannounced',confirmed=['EN'])
 p['language_evidence_role']='language_lessons'
 emit(NEW[16],'Cognitive Systems Academy · Space Challenge Season','Сингапур','SGP','Singapore · точный venue декабрьской группы не установлен','robotics,coding,science','day','Декабрьская страница 7–12; приложенный PDF май–июнь 7–18 относится к другому набору',
  'Английский сайт/брошюра есть; прямого обещания языка декабрьских занятий не найдено.',
  'Space Robotics:2 дня/240 минут; Rocket Flight:3 дня/360 минут, роботизированный запуск и бумажная ракета; combined5 дней/600 минут. Это короткие занятия, не полный день присмотра. Сезонные баллы/медали внутренние, не мировая лига.',
  'Страница: декабрь 2026, без точных недель. Прикреплённый SpacePDF: май–июнь 2026; его даты/возраст не подставлять в декабрь.',
  dict(year=2026,label='$299/2 дня, $416/3 дня; combined $554 для первых 20 вместо$715. Код валюты, доступность скидки и итог не подтверждены.',included='Описанные mission workshops.',extras='Наборы в собственность, питание, venue, дорога/страховка отдельно уточнить.',deposit='Опубликованный refund policy относится к цифровым курсам; не принят как договор очного лагеря.'),
  'Дневные короткие занятия; ночёвки не заявлены.',fit('conditional','Матвей 8–9 осенью 2026 укладывается 7–12; группа/язык/даты неизвестны.'),fit('not_eligible','Оскар 5–6 в 2026 ниже 7; общие обещания не расширяют декабрьский возраст.'),
  'Технический вариант с явным конфликтом старой брошюры и нового анонса. DSA/FLL/MIT/NASA маркетинг не подтверждение отбора, партнёрства или мирового результата.',[ASK],
  [src('Декабрьский анонс/цены',C),src('Прикреплённый архив Space Season May/June2026','https://www.cognitivesystems.academy/_files/ugd/93d899_0e2c241fc7884a72b4be5aadf08c4bb2.pdf'),src('Digital-only refund policy','https://www.cognitivesystems.academy/refundpolicy')],status='partial_2026')
 p=emit(NEW[17],'Connected · Jeju Global IT Camp · семейная программа','Южная Корея','KOR','Jeju Shinhwa World · остров Чеджу','general,languages,coding,science,art,culture','family','5–12; родитель обязательно сопровождает',
  'Оператор прямо заявляет 100% английские занятия, группы по возрасту/уровню. Русский текст — язык описания, не русское преподавание.',
  'Природа/геология/экология Чеджу, английский STEAM, digital art, coding,3D-дизайн, культурные активности. Выбор 1–3 недель; семейные гостиницы или апартаменты. Собственное описание международного состава не независимый рейтинг.',
  'Только 13–19.07,20–26.07,27.07–02.08.2025 опубликованы. Новый 2026–27 набор не подтверждён; текущая категория сайта не новый календарь.',
  dict(year=2025,label='Тариф обучения/семейного проживания не установлен;2027 счёта нет.',included='Пакет и меню выбранного отеля ещё уточнить.',extras='Перелёт, трансфер, стоимость родителей/второго ребёнка, страховка и ноутбук неизвестны.',deposit='Договор отмены нового набора не установлен.'),
  'Родитель живёт с детьми; не самостоятельный пансион.',both,both,'Возраст и семейный формат перспективны; пока архив для наблюдения за новым анонсом.',[ASK],
  [src('Собственное русское описание 2025',J),src('Собственное английское подтверждение даты/возраста/venue',JEN)],status='archive_next_unannounced',confirmed=['EN'])
 p['language_evidence_role']='camp_life'
 assert [p['slug'] for p in profiles[-len(NEW):]]==NEW

def extend_report_v121(r):
 r['version']=121
 r['shortlist'] += [
  dict(label='Сингапур · ближайшие технические дни',slugs=['roboto-young-coder','roboto-young-futurist','roboto-junior-coder','csa-space-challenge'],reason='Roboto:40 вариантов курса/недели ноября–декабря 2026, два центра на выбор. Матвей Junior пока 8/Young после 9, Оскару ещё рано. EN/валюту/место подтвердить. CSA только месяц; старыйPDF не декабрьский календарь.'),
  dict(label='Тайвань · английский общий лагерь и будущий maker',slugs=['taipei-kids-theme-camps','one-step-maker'],reason='TKA3–12 подходит обоим по возрасту, основные занятияEN, художественная частьZH. Новый 2027 набор/цены неизвестны. OneStep12–16 обоим позже, бесплатным был только пилот 2026.'),
  dict(label='Япония · художественные и английские каникулы',slugs=['malvern-tokyo-arts','malvern-tokyo-orchestra','malvern-tokyo-musical','malvern-tokyo-british-council'],reason='Четыре различных курса одного кампуса. Arts5–11 обоим; Orchestra8–12 плюсPrep 4; Musical после 10 плюсPrep 6. BC6–9: Матвею только пока 9. Лето 2026 архив, первые три Full; цены 2027 неизвестны.'),
  dict(label='Южная Корея · английский IT с родителями',slugs=['connected-jeju-global-it','smis-jeju-winter','gamja-jeju-winter'],reason='Новый семейный кандидат Connected5–12 пока подтверждён только 2025; не смешивать с отдельными зимними программами SMIS/Gamja и их возрастами/контрактами.')]
 for iso,country,provider,detail,url in [
  ('SGP','Сингапур','Roboto holiday vs weekly','Полные текущие own-course reader clauses доступны, directHTTP406. Camp ratio1:4–6 vs FAQ1:3/ownlaptop для weekly не переносить без проверки. Валюта/EN/срок скидки/holidayrefund/иностранный приём/места неизвестны.',R+'holiday-camp'),
  ('TWN','Тайвань','Taipei Kids Academy','Текущая ownZHстраница прочитана, oldENsummerURL404 но readerbody есть. Возраст/EN+ZH установлены; новый 2027 календарь, основной тариф/питание/иностранный приём неизвестны.',T),
  ('JPN','Япония','Malvern Tokyo четыре программы','Возраст и школьная ступень независимы. OwnTokyoBCPDF исправляет weekdayошибки family-directory; четыре/пять дней разныецены. Arts registration fee unit семья/ребёнок не установлен,2027 язык/цены/места/внешний приём проверить.',M),
  ('SGP','Сингапур','CSA календарь и договор','December7–12 страница vs SpacePDFMayJune7–18; дополнительныеPDFworkshop7–14 имеют 1–2 часа и другиевозраста, не расширяют December. Digitalrefundpolicy не договор очного camp. Месяц не точнаясмена; DSA/внутренниемедали не мировойотбор.',C),
  ('KOR','Южная Корея','Connected Jeju Global IT новый сезон','Собственное EN/RU описание 2025,5–12,родитель,ENITпрочитано. Нет актуального 2026–27 прайса/дат/контракта. Русская страница не русскоязычная группа.',J),
  ('TWN','Тайвань','HappyKids seasonal camp','Ownmainpage/regularDay/ASLA не достаточное подтверждение отдельного summer/winter camp. Пока нет нового campдосье; testimonialSpanishClub не испаноязычный лагерь.', 'https://happykids.taipei/')]:
  r['gaps'].append(dict(iso=iso,country=country,provider='v121 · '+provider,detail=detail,next_action='Продолжить первичную проверку нового набора и индивидуального допуска; неизвестные условия сохранять явно.',url=url))
