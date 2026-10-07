"""Own-site curriculum and admission clauses; no invented future offers."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='1f46cbbc5175edb4aec7098f4dad113ba30c8256'
CHECKED='2026-10-05'
X='https://xclcamps.com/'
A='https://www.americanvillage.fr/'
NEW=['xcl-stem-juniors','xcl-engineering-explorers','xcl-junior-coding','xcl-future-engineers','xcl-vr','xcl-minecraft-one','xcl-minecraft-two','xcl-roblox','xcl-generative-ai','xcl-design-thinking','xcl-technopreneurship','xcl-entrepreneurship-101','xcl-aviation-drones','xcl-steam-explorers','xcl-science-explorers','xcl-multi-young','xcl-multi-adventure','xcl-eal','american-manga-ayrolle','american-british-damian']
UPDATED=['xcl','american-village']
TERMS='Полная оплата за3 рабочих дня после брони. Договор: после оплаты отмены/возврата нет, включая поздний приезд/ранний отъезд. Перенос ≥10 дней внутри того же сезона Summer/Winter по наличию; более дорогой курс с доплатой. FAQ допускает рассмотрение возврата при болезни всей недели и справке, но договор этого не обещает: противоречие надо разрешить до покупки. Закрытие властями может дать годовой кредит вместо возврата.'
EXTRAS='SGD120/неделю/ребёнок за автобус по FAQ, маршрут при ≥6 пассажирах. Собственная medical/accident страховка обязательна: XWA не покрывает незачисленных школьников/родителей/гостей. Жильё семьи/перелёт/дорога отдельно. Онлайн Stripe +3%, условная комиссия способа оплаты. 10% earlybird до15мая2026 истёк; скидка второму ребёнку не подтверждена.'
LANG='FAQ допускает низкий уровень английского, но не устанавливает язык преподавания именно этого курса. Английский сайт не доказательство EN-инструктора; EN/ES/RU поток согласовать.'

def add_asia_europe_v109(add,src,fit,profiles):
 def emit(*a,role=None,**kw):
  add(*a,**kw);p=profiles[-1];p['checked']=CHECKED
  for s in p['sources']:s['checked']=CHECKED
  if role:p['language_evidence_role']=role
  return p
 common=[src('Календарь: expired earlybird15May2026',X+'camps-schedule/'),src('FAQ: транспорт/English level/болезнь',X+'about-us/faqs/'),src('Договор: оплата/отмена/страховка',X+'terms-and-conditions/')]
 questions=['Подтвердить реальные зимние2026/27 или летние2027 даты/цену/место, язык своего инструктора и индивидуальный иностранный приём; возраст на первый день неизвестен.','Полный счёт с автобусом/условной3%комиссией/страховкой и действующий возврат. По FAQ самостоятельный туалет и экстренный контакт взрослого. Заявки/оплаты/согласия не отправлялись.']
 m=('conditional','Матвей9–10 в2027 подходит по возрасту; будущая смена/язык пока неизвестны.')
 o=('conditional','Оскар6–7 в2027 подходит по возрасту; будущая смена/язык пока неизвестны.')
 o7=('conditional','Оскар только после7-летия в2027; в6лет ниже минимума.')
 m10=('conditional','Матвей только после10-летия в2027; в9лет ниже минимума.')
 ol=('later','Оскар2020 максимум7 в2027, младше минимального возраста.')
 game='Перекус, обед, футболка, ноутбук и login account во время курса; ноутбук не подарок.'
 rows=[
 (0,'STEM Juniors','4–7','science,engineering,coding','Материалы/причина и следствие: домики с ростками, магнитные лабиринты, кристаллы, физические блоки команд. Вводная научная игра, не подготовка к международному финалу.','29июня–3июля без года; календарь2026 в эту неделю показывает другой STEAM6–9. Juniors заезд/год не установлен.',720,None,('not_eligible','Матвей старше максимума7.'),o,'the-scholar/stem-juniors/',None),
 (1,'Engineering Explorers','6–8 и9–11','engineering,robotics','WittyMitty: механическая рука, ползающая/шагающая модель, RCмашина и marble run. Сделанные игрушки прямо разрешено забрать домой. Это инженерный курс, не доказанный соревновательный тренинг VEX/WRO.','Summer2026 без точных дат.',760,2026,m,o,'the-techie/engineering-explorers/',None),
 (2,'Junior Coding','6–8','coding,games','Matata/Scratch: блоки, условия, анимации и игры. Сравнить начальный уровень с навыками детей.','Summer2026 без точных дат.',710,2026,('not_eligible','Матвей9–10 старше максимума8.'),o,'the-techie/code-academy/',None),
 (3,'Future Engineers · Build Code Compete','Собственный блок10–15; календарь7–15; общий CodeAcademy6–14 — противоречие','robotics,coding,engineering','Micro:bit, VEX и применение дронов, системы, проектные итерации и командная работа. Учебное competition не означает зачисление в мировую лигу или международную медаль.','6–10июля совпадает с календарём2026; нижний возраст расходится7vs10.',760,2026,m10,('later','Собственный блок10+: Оскар2020 не подходит2027. Календарь7–15 не даёт одобрения младшему.'),'the-techie/code-academy/',None),
 (4,'Virtual Reality','9–14','coding,games,technology','CoSpacesEdu: свои3Dокружения/VRпроекты, цифровая грамотность и работа вместе. Экспорт и сохранение доступа к проектам уточнить.','Summer2026 без точных дат.',750,2026,m,ol,'the-techie/code-academy/',None),
 (5,'Minecraft Level1','7–9','games,coding,engineering','Blueprint, pixel art,3Dмир, системное мышление и дизайн среды. Общая страница не требует опыта.','13–17июля в календаре2026.',760,2026,('conditional','Матвей только пока9, после10-летия выше максимума9.'),o7,'the-techie/game-design/',game),
 (6,'Minecraft Level2','7–14','games,coding,engineering','Redstone/электрические схемы, автоматические двери и SmartSchool. Рекомендован проходившимLevel1; обязательный тест/пререквизит не установлен.','Даты TBC.',750,None,m,o7,'the-techie/game-design/',game),
 (7,'Roblox Game Design','7–10','games,coding','Создание/тестирование3Dигр, скрипты/debugging и итерации по обратной связи. Аккаунты/сохранение проектов уточнить.','27–31июля в календаре2026.',760,2026,m,o7,'the-techie/game-design/',game),
 (8,'Generative AI','10–14','ai,art,coding','ChatGPT/Suno/MidJourney: история/аудио/визуальный проект, ответственноеAI. Детский workflow через преподавателя, аккаунты и родительские согласия не описаны; аккаунты не создавались.','13–17июля без года; в общем календаре отдельныйAIблок не найден. Не датируем по соседнему Minecraft.',760,None,m10,ol,'the-techie/game-design/',game),
 (9,'Design Thinking & Innovation','8–12','entrepreneurship,engineering','Эмпатия/проблема/идеи/прототип/тест: физические модели, настольная игра и pitch. Прежний опыт по общей странице не нужен.','Даты TBC.',760,None,m,ol,'the-all-rounder/kids-entrepreneurship/',None),
 (10,'Technopreneurship','10–14','entrepreneurship,coding','Проблема пользователя→wireframe→мобильный прототип, block-based coding,UX/UI,pitch/marketing. Запуск бизнеса/доход не обещан.','Summer2026 без точных дат.',760,2026,m10,ol,'the-all-rounder/kids-entrepreneurship/',None),
 (11,'Entrepreneurship101','8–12','entrepreneurship,general','Потребности пользователей,branding/marketing, разработка продукта и pitch решения. Не заявленный международный хакатон с жюри.','6–10июля без года; отдельный блок в календаре не найден.',760,None,m,ol,'the-all-rounder/kids-entrepreneurship/',None),
 (12,'Aviation & Drones','6–12','engineering,technology,science','Аэродинамика/история полёта, мини-дроны/симулятор, бумажные самолёты, эффектMagnus и ракета с давлением. Не доказанныйFPVгоночный интенсив.','Страница20–24июля, календарь2026 дополнительно22–26июня; июль совпадает, июнь отдельно на странице курса не установлен.',760,2026,m,o,'the-techie/aviation-and-drones/',None),
 (13,'STEAM Explorers','6–9','science,engineering,art','TerraMinds: междисциплинарные опыты, исторические цивилизации, космос/симметрия. Не переносим детали отдельногоSTEMJuniors.','Страница22–26июня/13–17июля2026; календарь29июня–3июля/13–17июля. Первые недели расходятся, июль совпадает.',720,2026,('conditional','Матвей только до10-летия: максимум9.'),o,'the-scholar/steam-explorers/','Общий календарь заявляет meals/materials; конкретный блок полный пакет не перечисляет. Обед/футболку и takehome сверить.'),
 (14,'Science Explorers','Блок7–11, описание7–12 — расхождение','science,engineering,general','Простые машины/химические реакции/физика/биология/астрономия, научный метод и командные задачи. Take-home projects прямо заявлены.','Даты TBC.',720,None,m,o7,'the-scholar/science-explorers/',None),
 (15,'Multi-Activities · younger','Конкретный блок5–8; header3–8, общий текст3–5/6–8/9–14','general,sport,art,science,coding','Спорт/драма/творчество/плавание. Опыты и beginnercoding могут входить: занятия прямо зависят от наличия инструкторов, инженерные часы не гарантированы.','Страница6–10/20–24/27–31июля; календарь2026 только последние две недели.',720,2026,('not_eligible','Матвей9–10 старше конкретного младшего5–8 курса.'),o,'the-all-rounder/multi-activity/',None),
 (16,'Multi-Adventure','9–14','general,sport,nature,science','Спортивные игры/сокровища, первая помощь, фильтрация воды, навыки в бассейне, мини-походYishunPark/outdoor cooking. Дневной курс, не ночёвка в лесу.','6–10июля без года; отдельный блок в календаре не найден.',730,None,m,ol,'the-all-rounder/multi-activity/',None),
 (17,'EAL English','7–12; в календаре группы7–9/10–12','languages,general','Speaking/listening/reading/writing и грамотность. Дети уже владеютEN: оценить подходящую группу и пользу относительно инженерного курса.','6–10/20–24июля в календаре2026.',720,2026,m,o7,'the-scholar/eal-camp/',None),
 ]
 for i,name,age,themes,content,dates,fee,year,mat,osc,path,included in rows:
  p=emit(NEW[i],'XCL Singapore · '+name,'Сингапур','SGP','XCL World Academy · Yishun',themes,'day',age,
   LANG if i!=17 else 'EAL прямо развивает английские навыки. ЭтоENязыковой курс, не доказательство английского преподавания технических программ XCL.',content,
   dates+' Зима2026/27 и лето2027 этого курса не опубликованы; BookNow не подтверждает будущий заезд/места.',
   dict(year=year,label=f'SGD{fee}/5-дневный курс на ребёнка'+(' — архив2026, не цена2027.' if year else '; год тарифа не установлен, не цена2027.'),included=included or 'Перекус, обед, футболка и материалы в собственном блоке; техника домой не обещана, кроме явно описанных игрушек EngineeringExplorers.',extras=EXTRAS,deposit=TERMS),
   'Дневной Mon–Fri09:00–15:00,2YishunStreet42,Singapore768039. Пансиона нет; жильё семьи отдельно.',fit(*mat),fit(*osc),
   'Кандидат для сравнения конкретного проекта/возраста/языка; программа одного оператора, не независимый мировой топ и не обещание международных наград.',questions,
   [src('Собственный блок курса: возраст/содержание/прайс',X+path)]+common,status='published_2026' if year else 'next_unannounced',confirmed=['EN'] if i==17 else [],role='english_course' if i==17 else 'english_level_policy')
  if i==1:p['price']['included']='Общий календарь meals/materials; свой Engineeringблок не перечисляет еду/футболку. Игрушки домой прямо подтверждены; полный пакет согласовать.'
  if i in [1,12]:p['shortlist']=['both','technical']
  elif i in [2,3,4,8,9,10]:p['shortlist']=['technical']
  elif i in [0,15,16]:p['shortlist']=['general']
 insurance='Packassurance60EUR отдельно: assistance/rapatriement,annulation,volbagages; обязательность и полнота покрытия не установлены. Парижский/провинциальный транспорт, еда в дороге, карманные расходы исключены. Провинциальный участок может быть без сопровождающего: встречаHopways в Париже не сопровождение всего пути.'
 fq=['Собственные2027 даты/цена/foreignintake/возраст и отмена пока неизвестны. Старые кнопкиRéserver/общие слова о последнем месте не доказывают доступность закрытого заезда.','Formulesheader7–17 против конкретных индивидуальных формул8+. ClasseDécouverteCE2–4ème для школьных групп, не индивидуальная семейная смена.']
 emit(NEW[18],'American Village · Manga Mania · Moulin de l’Ayrolle','Франция','FRA','Saint-Félix-de-Pallières · Gard','general,languages,art','boarding','10–14',
  'Прямо100%EN лагерная жизнь; native/bilingual сотрудники,10чEN за6дней.',
  'Командные mangaмиссии,истории/творчество/cosplay. ENгруппы около15 по уровню;ratio1:5 — заявлениеоператора. Символические диплом/повязка не международная соревновательная награда.',
  'JF2:12–17июля2026,6дней/5ночей,Complet/больше недоступен. Даты и цена2027 не опубликованы.',
  dict(year=2026,label='ОтEUR779/ребёнок/6дней,архив2026; зависит от города отправления, не2027.',included='5ночей/fullboard,10чEN,активности/сопровождение. Montpellierвокзал–центр без доплаты по резервированию.',extras=insurance,deposit='2027аванс/отмена неизвестны. Oney3/4платежа — услуга с условиями, не скидка.'),
  'Moulin de l’Ayrolle: комнаты4–6 с душем,полный пансион.',fit(*m10),fit(*ol),'Матвею после10 как английская творческая самостоятельность; Оскару не2027. Не робототехнический интенсив.',fq,
  [src('Собственная формула',A+'formule/manga-mania'),src('JF2/12–17July2026/779/пакет',A+'sejour/manga-mania'),src('Возрастная таблица/школьные группы',A+'formules')],status='published_2026',confirmed=['EN'],priority=['general','boarding'],role='camp_life_and_english_lessons')
 emit(NEW[19],'British Village · Domaine de Damian','Франция','FRA','Vesc · Drôme','general,languages,sport,art','boarding','КонкретныйDamian11–15; общийBritish8–15/11–15 зависит от центра',
  'Прямо100%ENлагерь;10чEN/неделю,английские активности/вечера.',
  'Британская культура/игры/спорт/творчество/бассейн,DrWho-style занятия. Accrobranche только13дневнымзаездам. Ratio1:5 — заявлениеоператора. Общая языковая смена, неAI/roboticsинтенсив.',
  'Все6заездов2026 закрыты:28июня–10июля и12–24июля(13дней);28июня–3июля/5–10июля/12–17июля/19–24июля(6дней). 2027необъявлен.',
  dict(year=2026,label='Архив2026:отEUR749/6дней или1469/13дней на ребёнка; зависит от города отправления.',included='5или12ночей/fullboard,10или20чEN,активности/сопровождение. Valenceвокзал–центр бесплатно по резервированию.',extras=insurance,deposit='2027договор/аванс/отмена неизвестны; закрытые заезды не бронировались.'),
  'DomaineDamian:полный пансион5или12ночей.',fit('later','Матвей2017 максимум10в2027; конкретный центр только после11-летия в2028.'),fit(*ol),'Будущий подростковыйENмаршрут; минимум8другого центра не применяем кDamian11+.',fq,
  [src('Общая формула с разными возрастами',A+'formules/british-village'),src('6закрытыхзаездов/749/1469/11+',A+'sejour/domaine-de-damian-summer'),src('Возрастная таблица',A+'formules')],status='published_2026',confirmed=['EN'],role='camp_life_and_english_lessons')
 for p in profiles:
  if p['slug']=='xcl':
   p['checked']=CHECKED;p['language']=LANG;p['confirmed_instruction_languages']=[];p['language_evidence_role']='english_level_policy';p['price']['extras']=EXTRAS;p['price']['deposit']=TERMS
   p['timing']['label']+=' Календарь связан сearlybird15мая2026; новых2026/27зимних или2027летнихзаездов не подтверждено.'
   p['questions'].append('FAQболезнь vs строгийдоговор; свой ENтехническийинструктор/foreignintake/страховка ещё не подтверждены.')
   for title,url in common:
    if url not in {s['url'] for s in p['sources']}:p['sources'].append(dict(title=title,url=url,checked=CHECKED))
  elif p['slug']=='american-village':
   p['checked']=CHECKED;p['age']+=' Formulesheader7–17 против индивидуальныхформул8+: минимум7 не установлен.'
   p['questions'].append('ClasseDécouverteCE2–4ème для школьныхгрупп, не индивидуальная смена. Oscar2020 не8в2027. Damian11+,Manga10+.')
   if A+'formules' not in {s['url'] for s in p['sources']}:p['sources'].append(dict(title='Таблица возрастов и школьные группы',url=A+'formules',checked=CHECKED))

def extend_report_v109(r):
 r['shortlist'].extend([
  dict(label='Сингапур · два инженерных возраста на одном кампусе',slugs=NEW[:3],reason='Engineering6–8/9–11 для разных уровней,игрушки домой. Juniors4–7/Coding6–8 толькоОскару. Все2027смены/ENинструктор неизвестны;dayформат/жильё/страховка отдельно.'),
  dict(label='Матвей · инженерия → проект → предпринимательство',slugs=[NEW[i] for i in [3,9,10,8]],reason='DesignThinking8–12 по возрасту;FutureEngineers/Technopreneur/AI после10. Calendar7vsdetail10 расходится. Проектные курсы одногооператора, не обещание мировых наград;нет2027дат.'),
  dict(label='Франция · английский пансион и маршрут взросления',slugs=['american-wizard',NEW[18],NEW[19]],reason='Wizard8+ужеесть;MangaМатвею после10,конкретныйDamian11+только2028+. Oscarmax7в2027 не8+. Цены2026архивные,общийheadline7–17 ограничения не меняет.')])
 r['gaps'].extend([
  dict(country='Сингапур',iso='SGP',provider='v109 · XCL даты и возраст курсов',detail='FutureEngineers7–15calendar vs10–15detail;Science7–11vs7–12;STEAMJune22vsJune29. Juniors тойже недели не тотжеSTEAM. TBC/BookNow/разрозненныеJulyдаты не2027.',next_action='Единый будущий календарь курса/возраста/прайса иреальные места;истёкшийearlybirdMay15 2026 не переносить.',url=X+'camps-schedule/'),
  dict(country='Сингапур',iso='SGP',provider='v109 · XCL договор/страховка/язык',detail='FAQmedicalrefundconsideredvsTermsno-refundafterpay;3workingdayspay/10dayschange/sameseason. Ownmedical/accidentдлянеучениковXWA,автобус120/week≥6riders. LowEnglishwelcome неENtechnicalteacher;EAL толькоязыковойкурс.',next_action='Разрешить возвраты/подтвердить ENинструктора/foreignintake иinvoice+жильё/дорогу/страховку.',url=X+'terms-and-conditions/'),
  dict(country='Франция',iso='FRA',provider='v109 · AmericanVillage7header vs конкретные8+',detail='Formules7–17,индивидуальныеформулы8+. Manga10+,конкретныйDamian11+. ClasseDécouverteCE2–4ème школьнойгруппе. JF2от779/12–17July2026 и6Damian749/1469заездов закрыты;2027нет.',next_action='Конкретныйцентр/договор/foreignintake;Oscarmax7в2027,MatMangaпосле10/Damianпосле11в2028. Операторские отзывы не независимый рейтинг.',url=A+'formules'),
  dict(country='Испания',iso='ESP',provider='v109 · Respira UrbanTech — групповое предложение',detail='LEGO/Scratch/Unity/Blender/3D/VR;FAQгруппы3–14/минимум50. €78/90/102за1неделю с4/5/6часами в день не счётдлядвух и не подтверждённая2027смена. Период Christmas2026–27 указан, но конкретные venue/дни/ESинструктор/индивидуальныйприём неизвестны.',next_action='Открытые индивидуальные смены и полный пакет до семейной рекомендации.',url='https://respiraocio.com/campamentos-urbanos/campamentos-urbanos-tecnologicos/'),
  dict(country='Испания / Тайвань / Европа / мир',iso='ESP',provider='v109 · повторная проверка без дублей',detail='EnglishSummerTech8–15/€905/15чEN+15чtech ужеесть:годтарифа/ENроботики неизвестны. KeikoChristmas2026/27/FAISL2026/STEAMSquad/Grove/Wenzao2027 уже отдельные досье. FAISLPDFзагружен повторно,новой визуальнойпроверки109нет. 0полностьюаудированныхстран.',next_action='ПродолжатьCHE/FRA/ESP/Europe/TWN/SGP/KOR/JPN/USA/CAN/CRI/MEX/LatAm:общие/технические/тематические лагеря/пансионы,школы/результаты5–10лет,соревнования/лиги/выставки/семейные маршруты. Мировую цель не сужать.',url='https://www.englishsummer.com/campamentos-de-verano-ingles/tematicos-deportivos/tecnologico/')])

def correct_catalog_v109(catalog):
    e=next(q for q in catalog['events'] if q['id']=='L183')
    assert e['source']==X+'the-techie/robotics/' and not e['start']
    e.update(checked=CHECKED,language=LANG,languages=[],language_mode='unconfirmed',language_certainty=LANG,
        mat='Условно:9–10 в2027; конкретный заезд/язык и возраст на первый день подтвердить.',
        osc='Условно только после7-летия в2027; в6лет младше минимума.')
    e['note']='Архивное расписание2026 прошло; новых зимних2026/27 или летних2027 дат нет. '+TERMS+' '+EXTRAS
    if X+'terms-and-conditions/' not in {r['url'] for r in e['references']}:
        e['references'].append(dict(url=X+'terms-and-conditions/',label='Договор:отмена/оплата/страховка'))
