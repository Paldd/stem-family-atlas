"""Primary-source camp and children's coding-event audit, preserving v18.

Dates identify the announced scope, not invented daily teaching schedules.
English lessons, English assistance and English-medium robotics are distinct.
"""
import copy, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / 'data/catalog.json'
d = json.loads(PATH.read_text()); DAY = '2026-10-01'
assert len(d['events']) == 1135 and d['completeness_audit']['version'] == 18
baseline = copy.deepcopy(d['completeness_audit']['counts'])
byid = {e['id']: e for e in d['events']}; added = []; updated = []
carried = list(d['completeness_audit']['new_ids'])
regions = {'Швейцария':'Европа','Финляндия':'Европа','Германия':'Европа','Испания':'Европа',
    'Великобритания':'Европа','Сингапур':'Азия','Гонконг':'Азия','Малайзия':'Азия',
    'Таиланд':'Азия','Южная Корея':'Азия','Коста-Рика':'Центральная Америка','Кения':'Африка',
    'Мир':'Глобально'}

def source(url, title, proof):
    row = next((s for s in d['sources'] if s['url'] == url), None)
    if row: row.update(checked=DAY, evidence=proof)
    else: d['sources'].append(dict(url=url,title=title,checked=DAY,evidence=proof))

def add(id, title, country, city, url, **kw):
    assert id not in byid
    e = dict(id=id,block='Лагеря',title=title,country=country,region=regions[country],city=city,
        source=url,checked=DAY,start='',end='',deadline='',period='Следующий набор / даты не объявлены',
        date_status='Не объявлено',age='Возраст конкретной группы уточнить',
        mat='Условно — новый набор, язык и иностранный приём подтвердить',
        osc='Условно — новый набор, язык и иностранный приём подтвердить',
        format='Дневная каникулярная программа',participation='day_camp',admission_kind='program',
        entry='Выбрать опубликованный трек и группу; подтвердить возраст, язык, иностранный приём и места.',
        gear='Оборудование и темы выбранной программы',cost='Следующий тариф / доступность мест не подтверждены',
        language='Язык технических занятий EN / ES не подтверждён',languages=[],support_languages=[],
        language_mode='unconfirmed',language_certainty='Язык страницы не доказывает язык преподавания.',
        scope='local',level='Учебная программа; конкурсная мировая квалификация не заявлена',
        importance_reason='Редакционная оценка по содержанию и доступности семейного маршрута; не официальный мировой рейтинг.',
        reward='Учебный проект / опыт; сертификат лагеря не является победой в международной лиге',
        priority='P2 — поездка после подтверждения',status='Идея',
        action='Проверить следующий набор, группу, язык технического блока и конкретные дни занятий.',
        themes=['robotics','coding','technology'],evidence_level='program',references=[],related_ids=[],
        registration_status='Семья не зарегистрирована; опубликованное предложение не подтверждает наличие места.',
        note='Точные дни рождения и школьные классы неизвестны. Указан возрастной кандидат, а не принятый допуск.',
        proof='Прочитана программа организатора.',provider=title.split(' · ')[0])
    e.update(kw)
    if e['start']: e['date_status']='Подтверждено'
    d['events'].append(e);byid[id]=e;added.append(id);source(url,title,e['proof']);return e

def ref(e,url,label,proof):
    e.setdefault('references',[]).append(dict(url=url,label=label));source(url,label,proof)

def en(**kw):
    return dict(language='Английский — язык технического курса',languages=['EN'],language_mode='primary',
        language_certainty='Язык курса прямо заявлен организатором.',**kw)

def past(e, start, end):
    e['historical_editions']=[dict(start=start,end=end,status='Прошедшая смена; будущие даты не перенесены')]

# Europe: boarding eligibility is checked separately from the school's day camp.
stg='https://www.stgeorges.ch/fr/camps/summer-camps'
for id,mode,label in [('L166','residential','пансион'),('L167','day_camp','дневной формат')]:
    e=add(id,'St George’s · Junior STEAM · '+label,'Швейцария','Montreux / Clarens',stg,
        **en(),provider='St George’s International School',age='Junior 8–12; STEAM option в общем каталоге 8–16',
        mat='Да по опубликованному возрасту; новый Junior набор подтвердить',osc='Нет — Junior STEAM начинается с 8 лет',
        participation=mode,format='Двухнедельная смена с проживанием' if mode=='residential' else 'Дневной лагерь; конкретные часы Junior подтвердить',
        scope='international',gear='Программирование роботов, 3D-печать, stop-motion, прототипирование',
        cost='Последний тариф 2026: CHF 7570 / 2 недели пансиона' if mode=='residential' else 'Последний тариф 2026: CHF 3920 / 2 недели дневного Junior',
        entry='Выбрать именно STEAM как академическую опцию Junior, а не язык / public speaking. Международная регистрация предусматривает паспорт и medical information.',
        proof='Прочитана официальная FR страница: Junior8–12, STEAM8–16, English как основной язык; пансион / day8–16, младшие Nano / Mega только day.',
        note='2026 смены закончились: 28 июня–11 июля, 12–25 июля, 26 июля–8 августа. Даты 2027 не опубликованы. Для Оскара Mega6–7 — дневная альтернатива, но робототехническая программа этой группы не подтверждена. Возможные встречи CERN / EPFL не гарантированы каждой смене.')
    past(e,'2026-06-28','2026-08-08')

bm='https://summer.brillantmont.ch/mornings/tech-academy'
for id,start,end in [('L168','2027-07-03','2027-07-17'),('L169','2027-07-17','2027-07-31')]:
    e=add(id,'Brillantmont · Tech Academy 2027 · '+start[8:]+'.07–'+end[8:]+'.07','Швейцария','Lausanne',bm,
        **en(),provider='Brillantmont',start=start,end=end,date_scope='camp_window',period='',
        age='10–16; начинающий английский не подходит Tech Academy',mat='Условно — должен исполниться возраст 10 лет к прибытию',osc='Нет — минимум 10 лет',
        participation='residential',format='Пансион: фиксированная двухнедельная программа',scope='international',
        gear='Неделя AI, затем сборка / автономное программирование собственного робота; свой ноутбук',
        cost='CHF 7000 за 2 недели 2027, включая робота; пансион / питание / присмотр / трансферы перечислены в Fees',
        entry='Официальный приём международных учащихся 10–16; Tech Academy доступна только в двух опубликованных двухнедельных сменах. Заявка / medical form и подтверждение места отдельно.',
        proof='Прочитаны Tech Academy, Apply/Dates, Fees и Questions: текущие Fees явно указывают оба интервала 2027; техника преподаётся на English.',
        note='В описании Tech Academy сохранились старые даты 4–18 июля / 18 июля–1 августа. Для календаря использована явно датированная Fees2027. Французский доступен в среде лагеря, но технический курс идёт на EN. Родителям пансион не предоставляется; birthday Матвея важен. Окно включает дни приезда / отъезда, не ежедневные уроки.')
    for suffix,label in [('apply-dates','Даты / начало смен 2027'),('apply-fees','Тариф и точные интервалы 2027'),('apply/questions','Пансион и иностранные участники')]:
        ref(e,'https://summer.brillantmont.ch/'+suffix,label,'Прочитана официальная страница; 2027 начинается 3 / 17 июля, минимум 2 недели; родители не проживают в школе.')

lyceum='https://www.lyceum-alpinum.ch/wp-content/uploads/2025/09/Flyer-Summer-Camp-2026.pdf'
for id,label,age,gear in [('L170','Arduino Robotics','10–17','Arduino, проектирование / сборка / программирование робота'),
    ('L171','Python Game Design','10–17','Python / вводный Scratch и дизайн компьютерной игры'),
    ('L172','AI и machine learning','AI track12–15; общий летний пансион10–17','Классификаторы, обучение модели, dataset и AI-проект')]:
    e=add(id,'Lyceum Alpinum Zuoz · '+label+' · следующий сезон','Швейцария','Zuoz',lyceum,
        **en(support_languages=['DE','FR']),provider='Lyceum Alpinum Zuoz',age=age,participation='residential',format='Пансион; утренний Digital Skills как выбранная опция',scope='international',
        mat='Нет сейчас — AI track минимум 12 лет' if id=='L172' else 'Условно — будущая смена после 10-летия',osc='Нет — минимум '+('12' if id=='L172' else '10')+' лет',
        gear=gear,cost='Последний flyer2026: CHF5800 / 2 недели; новый тариф неизвестен',
        proof='Прочитан flyer2026 и Digital Skills factsheet: пансион10–17; цифровые модули на English, вопросы возможны DE/FR; AI12–15.',
        note='Прошедшие смены 5–17 и 19–31 июля2026, будущие даты не подтверждены. Junior Day6–9 предлагает языки и outdoor — не доказанный robotics camp. Factsheet описывает 9×3.5 часа, flyer2026 29 Digital hours; часы следующего набора уточнить.')
    ref(e,'https://www.lyceum-alpinum.ch/wp-content/uploads/2024/10/Factsheet-Digital-Skills.pdf','Digital Skills · язык и содержание','Курс на EN, поддержка вопросов DE/FR; AI12–15. Фактический поток / распределение часов сверить с новым набором.')
    past(e,'2026-07-05','2026-07-31')

aalto='https://www.aalto.fi/en/aalto-university-junior/camps'
for id,label,grade,gear,themes in [('L173','Scientist camp in English','Заканчивающие 1–3-й школьный класс','Водные / лабораторные эксперименты и STEM',['science','technology']),
    ('L174','Robotics camp in English','Заканчивающие 4–6-й школьный класс','Сборка и программирование роботов',['robotics','coding'])]:
    e=add(id,'Aalto Junior · '+label+' · следующий набор','Финляндия','Espoo · Otaniemi',aalto,
        **en(),provider='Aalto University Junior',age=grade+' по потоку2026; возраст в годах не заменяет класс',
        gear=gear,themes=themes,format='Дневная смена Mon–Fri 09:00–15:00; 5 дней',cost='Последний тариф2026: €150 / 5 дней, обед включён',
        evidence_level='historical_program',entry='В2026 места распределяли жеребьёвкой после подачи2–8марта. Сейчас2026 закрыт / all full; новый набор и эквивалент зарубежного класса согласовать.',
        proof='Прочитана официальная Camps page: два English лагеря8–12июня2026 с разными классами; другие потоки Finnish, closed/full.',
        note='Смена2026 прошла; даты2027 не назначены. EnglishScientist — научный STEM, не робототехника. EN не перенесён на остальные Finnish лагеря. Классы обоих детей неизвестны.')
    past(e,'2026-06-08','2026-06-12')

for id,suffix,label,age,mat,osc in [('L175','robotics-junior/','Robotics Junior','5–7','Нет — старше7','Да по возрасту; возможность EN поддержки подтвердить'),
    ('L176','lego-robotics-foundations/','LEGO Robotics & AI Foundations','German grades1–3, примерно6–9','Условно — класс1–3 и новая группа','Условно — класс1–3 и новая группа')]:
    e=add(id,'Train the Future · '+label+' · DE + EN помощь','Германия','Berlin · Mitte','https://trainthefuture.de/en/kurse/'+suffix,
        provider='Train the Future',age=age,mat=mat,osc=osc,participation='regular',format='Регулярный курс: 10 месяцев, одно60-минутное занятие / неделю',
        language='Немецкий — основной; прямо заявлена помощь на английском',languages=['DE'],support_languages=['EN'],language_mode='support',
        language_certainty='English support указана в поле Language конкретного регулярного курса; полного EN курса не обещано.',
        gear='Robotics Junior: modular kit, моторы, датчики, block coding' if id=='L175' else 'LEGO Education, алгоритмы, датчики, простая классификация AI',
        proof='Прочитана отдельная course page: возраст / grade, регулярный10-month формат и German with support in English.',
        note='Курс не является каникулярным лагерем. Уточнить, достаточна ли EN помощь ребёнку без немецкого и возможен ли короткий визит. Эта языковая поддержка не перенесена на holiday camp того же оператора.')
robotcamp='https://trainthefuture.de/en/camps/robotics/'
add('L177','Train the Future · Robotics holiday camp · EN уточнить','Германия','Berlin · Mitte / Prenzlauer Berg',robotcamp,
    provider='Train the Future',age='8–16',mat='Условно — возраст подходит, EN support лагеря не подтверждена',osc='Нет — минимум8',
    format='Пять дневных каникулярных дней; следующие даты не объявлены',language='Немецкий; English support именно camp не заявлена',languages=['DE'],
    gear='mBot2 / mBlock5, датчики, машинное обучение / Teachable Machine',
    proof='Отдельная camp page прямо указывает German; пятидневный curriculum и8–16. EN support регулярных курсов является отдельным предложением.',
    note='Не считать этот camp полностью английским или bilingual по языку EN страницы. В regular курсах того же провайдера помощь EN заявлена; для лагеря нужно отдельное подтверждение.')

club='https://theenglishclub.es/fun-weeks-2026/'
e=add('L178','The English Club · Fun Weeks, английский + robotics','Испания','Valladolid · Parquesol / Arroyo',club,
    **en(),provider='The English Club Valladolid',age='3–13 по2026 programme',mat='Да по прошлому возрасту; следующий набор подтвердить',osc='Да по прошлому возрасту; следующий набор подтвердить',
    format='Дневной10:00–14:00; продление08:30 /14:30 по2026',gear='Короткие robotics/coding проекты1–2 дня в неделю; другие дни English / спорт / piscina',
    cost='Последнее предложение2026: от€145 / неделю; сроки скидки прошли',
    proof='Прочитана Fun Weeks2026: English vehicular language, первые robot projects in English, расписание называет robotics/programming bilingual1–2 раза в неделю.',
    note='2026:29июня–31июля. Новый сезон неизвестен. Билингвальность технического блока заявлена, но пара языков прямо не названа; основной EN подтверждён, ES помощь уточняется. Это смешанный языковой лагерь с техническими днями, не ежедневный robotics intensive.')
past(e,'2026-06-29','2026-07-31')
asv='https://asvalencia.org/summerprogram/steam-summerland/'
e=add('L179','American School Valencia · STEAM Summerland','Испания','Valencia · Puçol',asv,
    **en(),provider='American School of Valencia',age='Возраст / класс STEAM Summerland на прочитанной странице не указан',
    format='Дневной09:30–16:30 по2026;2 или4 недели',gear='Робототехника, кодинг, engineering и STEAM-проекты по недельной теме',
    entry='Программа требует минимум intermediate English; внешняя семейная заявка, возрастную группу и2/4-недельный формат подтвердить.',
    proof='Прочитана STEAM page и новость школы о полном English summer programme2026; intermediate English обязателен для STEAM.',
    note='2026:29июня–24июля, дедлайн19июня прошёл. Следующая дата / min-age не подтверждены; EN готовность семьи не устанавливает нужный класс или campus admission.')
ref(e,'https://asvalencia.org/es/programas-verano-asv-2026-matricula-abierta/','Летние программы ASV2026 · язык','Все взаимодействия summer programme на English; STEAM min intermediate English; прошлые даты / срок.')
past(e,'2026-06-29','2026-07-24')
life='https://lifeschool.es/es/tech-summer-camp/'
e=add('L180','LIFE International School · VEX EXP Tech Summer','Испания','Madrid region · Tres Cantos',life,
    **en(),provider='LIFE International School',age='10–14',mat='Условно — следующий набор после10-летия',osc='Нет — минимум10',
    format='Дневной09:00–16:00; недельные смены',gear='VEX EXP STEM Labs: сборка / кодинг роботов, лабиринт, инженерные задачи',
    cost='Тариф2026: €280 / неделю, обед и snack; новый тариф неизвестен',
    entry='Официально допускаются дети вне LIFE school; максимум16 детей в неделю. Следующий набор и возраст на старт подтвердить.',
    proof='Отдельная Tech Summer2026 page:10–14, полная English immersion / robotics in English, VEX EXP, недельные смены и приём внешних детей.',
    note='Смены22–26июня,29июня–3июля,6–10июля2026 прошли. На2027 точных дат нет; не переносить старые автоматически.')
past(e,'2026-06-22','2026-07-10')
e=add('L181','EDUCAROBOT · Robotics / STEAM campus Plasencia','Испания','Plasencia','https://campamentoderobotica.es/',
    provider='EDUCAROBOT',age='5–16; группа / часы по возрасту уточняются',mat='Да по прошлому возрасту; следующий поток и язык подтвердить',osc='Да по прошлому возрасту; следующий поток и язык подтвердить',
    format='Дневной:FULL09–14,FLEX10–14,MINI10:30–13:30',gear='LEGO Mindstorms / WeDo, mBot, VEX; coding, CAD, электроника и maker',
    cost='Последний2026 прайс:от€59.95 MINI / неделю; другие форматы дороже',
    proof='Прочитана primary2026 page:5–16, робототехника / coding / maker, только дневные часы. Учитель имеет English qualification; это не обещание английского camp.',
    note='2026 лето объявлено с22июня; окончание и следующий набор не подтверждены. Страница ES и English квалификация преподавателя не доказали технический язык; пока не входит в подтверждённый EN/ES курс.')

techfaq='https://www.techcamp.org.uk/info/faqs'
e=add('L182','TechCamp · Winchester residential engineering / technology','Великобритания','Winchester',
    'https://www.techcamp.org.uk/info/residential-camps',**en(),provider='TechCamp UK',age='9–17 по календарному году; некоторые advanced courses11+ /13+',
    mat='Да по общему возрасту; выбрать курс9+ и смену',osc='Нет — должен исполниться9 в календарном году',
    participation='residential',format='Пансион: приездSunday / выездFriday; weekend stay отдельно',scope='international',
    gear='Выбранный инженерный / coding / AI course; robotics availability зависит от текущего меню',
    entry='Международные участники допускаются; instructionEnglish, рекомендуетсяB1 устного и письменного. Выбрать реальный residential course и трансфер, а не только город.',
    proof='Прочитаны Residential, Overseas Campers и FAQ: Winchester, foreign campers, весь instruction наEnglish,B1 recommendation, minimum9calendar-year.',
    note='Нет подтверждённой будущей даты конкретного курса. Девятилетний общий camp gate не открывает advanced AI11+/13+. ПоFAQ8-летний допускается лишь если9 исполнится в тот же календарный год.')
ref(e,'https://www.techcamp.org.uk/info/overseas-campers','Международные участники / EnglishB1','All instruction English; B1 written/oral рекомендуется.')
ref(e,techfaq,'FAQ · возраст и курсы','Минимум9 по календарному году; advanced11+/13+ отдельно.')

# Asia: no residential eligibility is inferred from a separate teen programme.
xclfaq='https://xclcamps.com/about-us/faqs/'
for id,suffix,label,age,mat,osc,gear,themes in [
    ('L183','the-techie/robotics/','Robotics','7–10','Да по последнему возрасту; следующий поток подтвердить','Нет сейчас — минимум7','LEGO robot и block coding',['robotics','coding']),
    ('L184','the-techie/code-academy/','Junior Coding','6–8 для Junior Coding, не весь Code Academy6–14','Нет сейчас — старше8 для Junior Coding','Да по последнему возрасту; следующий поток подтвердить','Основы программирования для младшей группы',['coding','games']),
    ('L185','the-scholar/stem-juniors/','STEM Juniors','4–7 по текущей странице STEM Juniors','Нет сейчас — старше7','Да по последнему возрасту; следующий поток подтвердить','Эксперименты, engineering и STEAM; robotics этой группы не обещана',['science','technology'])]:
    e=add(id,'XCL Camps · '+label+' · следующий сезон','Сингапур','XCL World Academy / выбранный camp campus','https://xclcamps.com/'+suffix,
        provider='XCL Camps',age=age,mat=mat,osc=osc,gear=gear,themes=themes,format='ДневнойMon–Fri09:00–15:00 по2026',
        language='Английская среда предполагается по FAQ; язык технического трека прямо не подтверждён',languages=['EN'],
        language_certainty='FAQ обсуждает English readiness и допускает низкий English level; это основание EN-кандидата, не прямое обещание whole-course instruction.',
        proof='Прочитаны отдельная programme page, summer2026 schedule и FAQ; возраст выбранного трека отделён от общего camp range.',
        note='Расписание June–August2026 прошло; новые даты не назначены. Старый brochure4–6 не заменяет текущий STEM Juniors4–7. Иностранную короткую заявку, группу и language support подтвердить.')
    ref(e,xclfaq,'FAQ · English readiness / booking','УровеньEnglish обсуждается при выборе camp, но язык каждого урока не заявлен.')
    ref(e,'https://xclcamps.com/camps-schedule/','Опубликованное summer2026 расписание','Все прочитанные смены прошедшие; не перенесены на2027.')

for id,country,city,title,url,age,cost,gear in [
    ('L186','Сингапур','Bukit Timah / Joo Chiat / Goldhill / Mohamed Sultan','Newtonshow · Jolly-Mix Winter2026/27',
        'https://www.newtonshowcamp.com/winter-camp','3–14','Общий прайсSGD730 / неделю; акции и выбранный трек уточнить','Science + maker / engineering / robotics + art / cooking'),
    ('L188','Гонконг','Wan Chai / Kowloon Bay / Wong Chuk Hang / Shek Mun','Newtonshow · Winter Robotics & Maker2026/27',
        'https://www.newtonshow.hk/winter-camp','3–12','ОтHK$657; длительность услуги за этот тариф прямо не указана','Robotics, engineering, конструкция / design и тестирование'),
    ('L189','Малайзия','Kuala Lumpur: Bangsar / Bukit Bintang; Johor Bahru / Penang','Newtonshow · Jolly-Mix Winter2026/27',
        'https://newtonshow.my/winter-camp','3–12','ОтRM600 / неделю; площадку / дни и трек подтвердить','Maker / motorized projects / Robo-Olympics внутри смешанного STEM / art camp')]:
    faq='https://www.newtonshowcamp.com/more-information-about-camp' if country=='Сингапур' else 'https://www.newtonshow.hk/faq' if country=='Гонконг' else 'https://newtonshow.my/faq'
    e=add(id,title,country,city,url,provider='Newtonshow',start='2026-11-23',end='2027-01-29',period='',date_scope='camp_window',
        age=age,mat='Да по опубликованному возрасту; группу и место подтвердить',osc='Да по опубликованному возрасту; группу и место подтвердить',
        format='ДневнойMon–Fri09:00–16:00; можно день / несколько дней / неделю',cost=cost,gear=gear,
        language='FAQ заявляет native English teachers; полный язык каждого трека подтвердить',languages=['EN'],
        language_certainty='Прочитан FAQ именно этой страны (HK/MY: public FAQ structured answers): nativeEnglishteachers. EN-кандидат по персоналу, без прямого whole-course обещания.',
        proof='Прочитана локальная winter page:23Nov2026–29Jan2027, возраст, дневные часы, содержание и площадки; локальныйFAQ подтверждает English-native staff.',
        note='Даты — общее окно предложений. Конкретные рабочие / праздничные дни, доступность темы в кампусе и место подтверждаются при выборе недели; это не непрерывная смена68дней. Jolly-Mix включает роботов лишь как часть программы; Robo-Olympics camp games не являются мировой лигой.')
    ref(e,faq,'ЛокальныйFAQ · преподаватели / организация','English-native staff указан именно локальным FAQ, не перенесён из другой страны.')
e=add('L187','Newtonshow Singapore · отдельный Robotics camp, даты уточнить','Сингапур','Singapore · выбрать доступный campus',
    'https://www.newtonshowcamp.com/robotics-camp',provider='Newtonshow',age='На одной странице5–12 и5–13; верхнюю границу подтвердить',
    mat='Да по обоим опубликованным возрастным диапазонам; набор подтвердить',osc='Да по обоим опубликованным возрастным диапазонам; набор подтвердить',
    format='Дневной robotics programme;5 дней09:00–16:00',gear='LEGO Education, моторы / датчики, сборка / программирование',
    language='NativeEnglishteachers по общему FAQ; instruction выбранной robotics группы подтвердить',languages=['EN'],
    language_certainty='FAQ staff EN, но устаревший Robotics schedule не подтверждает новую смену.',
    proof='Прочитана отдельная Robotics page и FAQ: робототехнический programme; диапазоны5–12/13 расходятся; даты autumn/christmas не имеют года.',
    note='На robotics page есть Sep4–Nov10 /Nov20–Jan12 без года; они не использованы как будущие даты. Новое winter2026/27 окно относится к смешанному / maker offer, не доказывает доступность этой чистой LEGO смены.')
ref(e,'https://www.newtonshowcamp.com/more-information-about-camp','NewtonshowSGFAQ','NativeEnglishteachers; родитель не остаётся в классе.')

uwc='https://www.uwcthailand.ac.th/beyond-the-classroom/summer-camps-2026'
e=add('L190','UWC Thailand / TEEMS · Sports & Technology day camp','Таиланд','Phuket',uwc,
    provider='UWC Thailand / TEEMS',age='ДневнойSports & Technology4–14',mat='Да по2026 возрасту; следующий поток и технический язык подтвердить',osc='Да по2026 возрасту; следующий поток и технический язык подтвердить',
    format='Дневной недельный camp; boarding12–18 отдельно',gear='Coding, robotics, animation и STEAM плюс sport / outdoor',
    language='English immersion урок15:00–16:00 — дополнительная опция; язык robotics блока не заявлен',languages=[],support_languages=['EN'],language_mode='language_lessons',
    language_certainty='Опция English class доказана; она не доказывает EN instruction всех технологий.',
    cost='Тариф2026 dayTHB18950 / неделю; English option THB7500 дополнительно',
    entry='Программа открыта внешним семьям Phuket; выбрать дневной Technology вариант и проверить язык, возраст и следующий набор.',
    proof='Прочитана Summer2026 page:day4–14,Technology coding/robots; отдельныйboarding только12–18; English tuition optional15–16.',
    note='2026:22июня–17июля; следующая дата неизвестна. Boarding12–18 не подходит обоим и не перенесён на дневной4–14 programme.')
past(e,'2026-06-22','2026-07-17')
berlitz='https://www.berlitztaiwan.com/pages/berlitz-study-abroad-korea'
add('L191','Berlitz · Seoul English camp + STEM workshops','Южная Корея','Seoul',berlitz,
    provider='Berlitz',age='8–18',mat='Да по опубликованному возрасту; текущий набор подтвердить',osc='Нет — минимум8',
    participation='residential',format='Проживание / полный пакет; даты конкретной смены не указаны',scope='international',
    gear='English lessons + hands-on robots / AI / biotechnology workshops и культурные занятия',
    language='English уроки и English-speaking accommodation environment; язык каждого STEM workshop уточнить',languages=[],support_languages=['EN'],language_mode='language_lessons',
    language_certainty='Прямо описана English-speaking среда / уроки; нет явного whole-STEM English teaching обещания.',
    proof='Прочитана BerlitzTaiwan page именно о Korea:8–18, accommodation / meals / airport transfers и STEM workshops robots/AI.',
    note='Это программа вКорее, хотя источникTaiwan. Страница не называет год / будущие даты / актуальную цену. Наличие13завтраков не превращено в придуманную точную14-дневную смену.')

embassy='https://embassy.camp/ai-future-camp/'
add('L192','Embassy · AI Future Camp2027 · пансион','Малайзия','Kuala Lumpur',embassy,
    provider='Embassy Camps',start='2027-07-04',end='2027-07-24',period='',date_scope='camp_window',age='9–19',
    mat='Да по минимальному возрасту; конкретную AI группу и допуск подтвердить',osc='Нет — минимум9',
    participation='residential',format='Три недели с hotel accommodation / полным питанием',scope='international',
    gear='10AI platforms, prompt skills, touch typing и прикладные проекты; этоAI, не подтверждённая робототехника',themes=['ai','coding','technology'],
    language='Организатор заявляет English-speaking immersion; язык и адаптацию технических заданий младшей группы подтвердить',languages=['EN'],language_mode='unconfirmed',
    language_certainty='English-speaking immersion заявлена как цель; полный язык каждого AI workshop прямо не определён.',
    cost='Пакет$2890 twin /$2590 triple with shared bathroom; страница не называет валюту символа$',
    entry='Официальное международное предложение9–19; подтвердить наставника / группу9–10, язык задания и доступные младшим инструменты до заявки.',
    proof='Прочитана официальная AI Future page:July4–24,2027,KualaLumpur,9–19,hotel package и10AI platforms. Отдельный Smart Skills2027 не содержит обещанной некоторыми каталогамиrobotics.',
    note='AI Future отличается от Smart Skills. Публикация цены / registrationbutton не означает место или заявку. Даты включают общее окно пакета, точные workshopдни не опубликованы.')

wonder='https://www.lifeprojecteducation.org/wondercamp-july-2026'
e=add('L193','Life Project Education · WONDER Camp, engineering + Spanish','Коста-Рика','Ojochal',wonder,
    provider='Life Project Education',age='Общий заголовок6–15, FAQгруппы3–5 /6–12; для братьев общий диапазон6–12',
    mat='Да по6–12 группе; новый набор подтвердить',osc='Да по6–12 группе; новый набор подтвердить',
    format='ДневнойMon–Fri09:00–14:00; lunch не включён',themes=['technology','science','makers'],
    gear='Бамбуковая инженерия, architecture / geometry и командные проекты; robots / AI / coding не заявлены',
    language='Испанская immersion прямо заявлена; заголовок называет bilingual camp, объём EN поддержки неизвестен',languages=['ES'],language_mode='primary',
    language_certainty='Spanish immersion заявлена организатором; EN не добавлен как подтверждённая поддержка только из bilingual заголовка.',
    cost='Последний2026 прайс:$222 / неделя за1ребёнка,2недели$400; валюта символа$ на странице не определена',
    entry='Организатор прямо приглашает visiting families; выбрать новую смену и6–12группу, подтвердить место / язык.',
    proof='Прочитана отдельная July2026camp page:Spanishimmersion,visitingfamilies,6–12группа,engineering/nature,circus,day09–14.',
    note='2026:20–24 /27–31июля прошли. Это местная engineering / STEM альтернатива, не робототехнический лагерь. Заголовок6–15 против6–12FAQ сохранён; новый сезон не датирован.')
past(e,'2026-07-20','2026-07-31')

iron='https://ironscholars.com/upcoming-events/'
add('L194','Iron Scholars · Children’s Day Build Zone2026','Сингапур','Kidz Amaze · SAFRA Jurong',iron,
    provider='Iron Scholars',start='2026-10-03',end='2026-10-04',period='',date_scope='workshop_window',age='Build Zone6–12',
    mat='Да по возрасту; места и язык уточнить',osc='Да по возрасту; места и язык уточнить',participation='holiday_workshop',
    format='Одночасовой workshop:2варианта в каждый день14–15 /17:15–18:15 Singapore time',
    gear='Групповая сборка и design robot car',cost='Guest$41 /session; разные member rates$33/35, валюту и adult entry подтвердить',
    priority='P3 — небольшой местный workshop при поездке',entry='На primarypage естьGuestrate и registrationlink; подтвердить места, язык и сопровождающего. Это неGlobalRoboticsGameshackathon.',
    proof='CurrentUpcomingEvents явно объявляет3–4October2026,BuildZone6–12 и два одночасовых слота; нижнийNov14–15hackathon относится к gallery2025 и registrationclosed.',
    note='Не крупный международный фестиваль: местный детский тематический день. Октябрьские дни — окно выбора1часа, не48-часовой лагерь. Старый Novemberhackathon не выдан за новый2026.')

# Project contests and a virtual robot task test: different results and gates.
penang='https://penangmathplatform.com/event/icode-math-hackathon/'
add('C840','iCode Math Hackathon · Penang2026 Blockly Junior Final','Малайзия','IPG Kampus Pulau Pinang',penang,
    block='Соревнования',start='2026-10-10',end='2026-10-10',period='',age='Blockly Junior7–9; другие уровни10–12 /13–15 /16–19',
    mat='Условно по7–9возрасту; без пройденного отбора финал недоступен',osc='Нет — минимум7',participation='individual',format='30virtualrobot missions за60минут; финал08:30–11:30',
    admission_kind='qualifier',scope='regional',priority='P4 — новый вход в финал без отбора не подтверждён',
    gear='Blockly / virtualrobot challenges',entry='Top25каждой категории после предварительных18июня,15июля,12августа,18сентября. Отборы прошли; latefamily entry не объявлен.',
    reward='Протокол virtualtask competition; Top3получают invitation InternationaliCodeChina, дата / место / расходы отдельно',
    level='Местный отбор и финал; не открытый международный projecthackathon',
    proof='Прочитана primaryeventpage:7–9BlocklyJunior,60min/30tasks,четыре прошлых qualifiers,Top25final10October иTop3invitationChina.',
    note='НазваниеHackathon не меняет формат: задания на виртуального робота, не свободный проект48часов. ENpage не подтверждает язык инструкций. У семьи нет подтверждённого квалификационного результата.')

lsc='https://www.lsc-challenge.org/lsc2026'
guide='https://www.lsc-challenge.org/_files/ugd/d9f7f5_14a1e38fd76a46d3a2cb48932af66feb.pdf'
for id,label,age,mat,osc in [('C841','U8 Explorer','7–8','Нет — старше8','Нет в2026 — младше7'),
    ('C842','U10 Builder','9–10','Да по опубликованному возрасту; cutoff / иностранный приём подтвердить','Нет — младше9')]:
    e=add(id,'LSC Challenge2026 · '+label,'Сингапур','Online submission platform / местное присутствие уточнить',lsc,
        block='Соревнования',start='2026-12-02',end='2026-12-02',period='',date_scope='activity_start',
        age=age,mat=mat,osc=osc,participation='individual',format='СвежийScratchпроект в назначенные120минут',
        admission_kind='open_application',scope='national',priority='P4 — возраст обеим детям не подходит' if id=='C841' else 'P2 — участие после подтвержденияforeignentry',
        gear='Scratch;U12отдельноPython11–12',cost='S$40 standardregistration поcompetitionguide',
        entry='Подача online через сайт; foreign / дистанционный допуск изCostaRica, cutoffи точный120-минутныйслот не установлены. Registrationopens17August,optionalworkshops2November.',
        reward='Сертификат участников; showcase / награды лучшим. Не мировая квалификационная лига.',level='Singapore creativecodingcompetition; мировой охват не доказан',
        proof='ПрочитаныLSC2026pageи4-pageofficialCompetitionGuide:7–8/9–10/11–12,120минут,S$40,старт2December /results21December.',
        note='2декабря — объявленное начало соревнования, не подтверждённый день именно вашей сессии. Конец периода не назначен21декабря: этоresultsday. GuideпланируетawardвторуюнеделюJanuary2027,websiteточныйденьнеуказывает. AItools,готовыйкод /cheatsheets запрещены; ребёнок пишет сам, родители дают лишь общую подготовительную помощь.')
    ref(e,guide,'ОфициальныйCompetitionGuide2026','Проверены возраст,120min,AI/prewrittenban,стоимость и разныефазы; exactsession/foreignentry неописаны.')

ikcc='https://www.ikcc.info/en/rules-pag3'
for id,name,start,category in [('C843','World Game Coding2027','2027-01-03','Game'),('C844','World Scratch Coding2027','2027-09-01','Open')]:
    e=add(id,'IKCC · '+name+' · начало','Мир','Online · international',ikcc,block='Соревнования',
        start=start,end=start,period='',date_scope='activity_start',age='Общие правила7–8 /9–10 /11–12 /13–14; категории конкретного2027издания ещё подтвердить; возраст на первыйденьрегистрации',
        mat='Условно —9/10возраст подходит общим правилам; категория2027подтверждается при анонсе',
        osc='Условно — должен уже быть7лет на первыйденьрегистрации и категория7–8 должнабытьобъявлена',
        participation='individual',admission_kind='open_application',scope='international',priority='P1 — онлайнпроект после открытияприёма',
        format='ИндивидуальныйScratch3.0проект; родителиguide, но без общейteamзаявки',gear='Scratch3.0;Game' if category=='Game' else 'Scratch3.0;story/animation/game/mixedOpen',
        themes=['coding','games'],cost='Бесплатно поRules; accountиentryразные действия',
        entry='Независимые дети / codingclubs допускаются, ноschooldocument обязательно содержитимя,школу/город/страну,класс,DOB; нуженadultguide /parentapproval. Общийcountrylimitможетизменяться; текущаялимитнаясписокBangladesh/Cambodia/India/Indonesia.',
        reward='Победителям1/2/3 дипломместа; остальнымparticipationcertificate. Физическиетрофеи/медалиinternationalwinnersнерассылаются.',
        level='Международныйонлайнконкурссамостоятельныхпроектов; неrobotleagueи неочныйhackathon',
        language='ПравилаEnglish; языкпроекта /Zoomавторстваконкретногоcontestуточнить. ENобязателенгодовойBestProjectsselection.',languages=['EN'],language_mode='unconfirmed',
        language_certainty='ENправилапрочитаны; обязательныйENдляBestProjectsнеперенесённакаждыйopencontest.',
        proof='ПрочитаныRules,Calendarиcurrenthome:ComingSoonявноуказывает3Jan2027/1Sep2027. GenericcalendarJan1 /Jan30неиспользованкакточный2027deadline.',
        note='Вкалендарепоказаноднодневноеначало,неполноеокноподачи. Конечныйсрок2027неподтверждён. Аккаунт,школьныедокументы,публикацияданныхипроекта /Zoomпроверкаавторстваотносятсякправиламорганизатора;никакихаккаунтовизаявоксайтсемьи несоздаёт. Старый2026приём1–30Septemberзакрыт.')
    ref(e,'https://www.ikcc.info/','ТекущиеComingSoon2027анонсы','Дваявныхstart2027,безпридуманногоenddate.')
    ref(e,'https://www.ikcc.info/en/calendar-pag18','Общийкалендарьиправилогодовоговыбора','ОбщийJanuary1расходитсясcurrentJan3для2027; yearlessendнеиспользован.')

add('C845','CodeYetu · National Young Innovators Hackathon · следующий сезон','Кения','Nairobi / выбраннаяплощадкауточнить',
    'https://hackathon.codeyetu.org/',block='Соревнования',provider='CodeYetu',age='Scratch6–12 /Game6–18;Robotics10–18,AI12–18',
    mat='Условно —Scratch/Gameвозрастподходит;national/foreignentryподтвердить',osc='Условно —Scratch/Gameвозрастподходит;national/foreignentryподтвердить',
    participation='team',admission_kind='open_application',scope='national',format='Командныйпроект→разработка→подача→защита',
    gear='ScratchилиGameDevelopmentдля6/9;Robot10+/AI12+неподходятобоимсейчас',themes=['coding','games'],
    level='НациональныйKenyaпроектныйhackathon;международнаяоткрытостьнеобъявлена',reward='Призы /сертификатыпорезультатукатегории;неworldtitle',
    entry='Страницапредлагаетсоздатьилиприсоединитьсяккоманде;deadline6June2026прошёл. Новыйсезон,teamrulesиforeignonline/onsitegateнеподтверждены.',
    proof='Прочитанаprimary2026page:realproject/teamworkflow,возрасткаждогоInnovationTrackи6Junecloseddeadline.',
    note='Дополнительныйглобальныйпримердетскогоhackathon,за пределамтрёхзапрошенныхрегионов. WebsiteENнеподтверждаетсудействоEN;непредставленкакдоступнаясейчасfamilyзаявка.')

# Refresh existing records without promoting language lessons to robotics EN.
byid['L006'].update(language_mode='language_lessons',languages=[],support_languages=['EN'],checked=DAY,
    language_certainty='English15h/weekподтверждены;язык15htechnologyотдельнонеуказан.',proof='ПовторнопрочитанофициальныйTechnologyCamp:8–15,15hEnglish+15htechnology;техническийязыкнеобещан.')
updated.append('L006')
byid['L003'].update(source='https://camptecnologico.com/les-alojamiento/',checked=DAY,age='9–11 /12–17 поLes2026programme',
    mat='Да по прошломувозрасту9–11;новыйнабор/языкподтвердить',osc='Нет —минимум9',language='ЯзыкroboticsEN/ESпрямонеподтверждён;primaryописаниенаES',languages=[],support_languages=[],language_mode='unconfirmed',
    cost='Тариф2026:€960/weekбезPC;+€50PCrental;transferотдельно',gear='Выборrobotics/coding/creative-techтрековпоagegroup',
    proof='ПрочитанаcurrentLes2026primarypage:9–11/12–17,5–12 /12–19July2026,€960,нообещаниеES/ENteachingотсутствует.',
    note='Смены2026прошли;новыедатынеобъявлены. Верхнееописаниеjaima/нижнееbungalowsрасходится:типжильяподтвердить. ESсайтнеподменяетпрямойlanguageoffer.',
    historical_editions=[dict(start='2026-07-05',end='2026-07-19')])
source(byid['L003']['source'],'CampTecnológicoLes2026',byid['L003']['proof']);updated.append('L003')
byid['L013'].update(title='TechCamp · дневныеengineering/technologyкурсы',checked=DAY,language_mode='primary',languages=['EN'],
    language_certainty='OverseasCampersпрямоподтверждаетallinstructionEnglish;B1recommended.',age='Минимум9покалендарномугоду;advanced11+/13+отдельно',
    format='Дневнойcamp;residentialWinchesterвыделенвL182',participation='day_camp',related_ids=['L182'],
    proof='Повторнопрочитаныcurrentcourses,FAQиOverseasCampers;общийmin9неоткрываеткаждыйAIadvancedcourse.')
ref(byid['L013'],'https://www.techcamp.org.uk/info/overseas-campers','AllinstructionEnglish /B1','Языкподтверждёнпрямо;курсвыбираетсяпоagegroup.');updated.append('L013')
byid['L121'].update(checked=DAY,language_mode='language_lessons',support_languages=['EN'],
    language='EnglishdailylessonsиIA-bilingüeподтверждены;полныйroboticsязыкнеустановлен',
    note=byid['L121']['note']+' ВпланахFlexroboticsнет,Complete/Premiumroboticsвключают. IA-bilingüeвCompuInglésнеозначаетвесьArduino/roboticsблокнаEnglish.',
    proof='Повторнопрочитаныindex2026ипланы:27July–28August8–14,Englishdaily/IA-bilingüe,roboticsтольковComplete/Premium.')
ref(byid['L121'],'https://www.conversa.com.mx/planes_modalidades_verano','ПланыFlex/Complete/Premium','Flexнеимеетrobotics;прошлыесрокипланыпрочитаны.');updated.append('L121')
byid['C039'].update(checked=DAY,participation='individual_or_team',format='Индивидуальныйпроектилитеам;действующие2027teamrulesподтвердить',
    proof='Прочитанаofficialonlinehelp:молодыеcreators≤18извсегомира;2026закрыт,2027датыещёнет.',
    note=byid['C039']['note']+' 2027reopeningобъявленбезточныхдней;показпроектовнеобещаеткаждомумировуюмедаль.')
ref(byid['C039'],'https://online.coolestprojects.org/help','OnlineShowcaseHelp','Worldwide≤18;2026closed,next2027TBA.');updated.append('C039')

# Normalize only our new / refreshed editorial text, preserving source URLs.
def spaces(value):
    import re
    value=re.sub(r'([А-Яа-яЁё])([A-Za-z0-9])',r'\1 \2',value)
    value=re.sub(r'([A-Za-z0-9])([А-Яа-яЁё])',r'\1 \2',value)
    return value
for id in added+updated:
    e=byid[id]
    for key,value in list(e.items()):
        if isinstance(value,str) and key not in ['id','source','start','end','deadline','date_scope','language_mode','participation','scope','admission_kind','evidence_level','provider','registration_url']:
            e[key]=spaces(value)

issues=[
    dict(name='Brillantmont2027 / старыеTechAcademyдаты',status='Fees/Applyявно2027:3–17July/17–31July. Programmebodyсохранил4–18July/18July–1Augustстарогокалендаря;использован2027Fees.',official_alternative='https://summer.brillantmont.ch/apply-fees'),
    dict(name='Englishassistance / Englishlessons / courseEnglish',status='BerlinregularDE+ENsupportнеперенесённаGerman-onlycamp. EnglishSummer/UWC/ConversaурокиENнеприравненыкEnglishrobotics. NewtonFAQnativeENstaffиXCLEnglishreadinessдаюткандидата,неwhole-courseguarantee.',official_alternative=robotcamp),
    dict(name='Boardingminimumage',status='StGeorgeJuniorSTEAM8+,Brillantmont/Zuoz10+,TechCamp9calendar-year,Berlitz8+,Embassy9+. UWCday4–14неоткрываетboarding12–18. JuniorZuoz6–9языковой,неrobotics.',official_alternative=uwc),
    dict(name='NewtonshowfuturewindowvsoldRobotics',status='ЛокальныеWinter2026/27страницызадают23Nov–29Janкакпредложениеweek/day. PureRoboticsSGимеет5–12/13иyearlessстарыеdates;новоеконкретноеробоокноневыведено.',official_alternative='https://www.newtonshowcamp.com/robotics-camp'),
    dict(name='Детскиеhackathons / phase dates',status='Penangfinalзакрытбезqualifier. IronScholarsNovhackathonстарый2025closed,October2026workshopотдельно. LSCDec2начало,Dec21results;IKCC2027Jan3startрасходитсясgenericJan1,конецTBA.',official_alternative=lsc),
    dict(name='Историческиеиотклонённыекандидаты',status='Aalto2026closed/full;Lyceum2026PDF,Spain2026shifts,WONDER2026неперенесенына2027. EmbassySmartSkills2027неrobotics;YoungEngineersBerlinEnglishcampпокалишьагрегатор;PanamaOEI2021tenderнеfamilycamp.',official_alternative='https://embassy.camp/smart-skills-camp-in-malaysia/')]
focus=dict(version=19,checked=DAY,
    conclusion='Все лагеря мира не собраны. Добавлены новые первичные программы Европы и Азии, engineering-альтернатива в Коста-Рике и детские проектные соревнования. По странам сохраняются пробелы, по старым сменам — ожидание нового набора.',
    family='Матвей2017 /Оскар2020:оба могут учиться наEN/ES. Точные birthdays/grades неизвестны; пансионы /языковаяпомощь /foreignentryпроверяютсяотдельно.',
    added_ids=added,updated_ids=updated,carried_forward_ids=carried,
    hack_event_ids=['C039','C840','C841','C842','C843','C844','C845'],
    routes=[
        dict(name='Оба ребёнка · выбрать группы одного оператора',detail='NewtonshowSG/HK/MYопубликовалиWinter2026/27окно23ноября–29января. Возраст6/9подходит,ноязыкконкретнойrobotics/makerгруппыиплощадкуподтвердить. XCLимеетотдельноRobotics7–10дляМатвея,JuniorCoding6–8/STEAM4–7дляОскара;следующиеweekdaysTBA.',ids=['L186','L188','L189','L183','L184','L185']),
        dict(name='Европа · английский технический курс',detail='StGeorgeJuniorSTEAM8+:Матвейвозрастнойкандидат,Оскарпоканет. TechCamp9поyear/B1:Матвейпослевыборакурса9+,пансионWinchesterотдельно. FunWeeksValladolid3–13имеетENrobotics1–2днявнеделювсмешанномлагере;новыедатыпоканеобъявлены.',ids=['L166','L167','L182','L013','L178','L179']),
        dict(name='Меньше9 · помощьENилиESengineering',detail='BerlinRoboticsJunior5–7даётDEосновной+ENподдержку,неканикулы. FoundationsпоGermangrade1–3нужноподтвердить. WONDEROjochal6–12Spanishimmersion/engineeringпринимаетvisitingfamilies;следующийнаборTBA,роботы/AIнезаявлены.',ids=['L175','L176','L193']),
        dict(name='Пансионы2027 · возраст на приезд',detail='BrillantmontTech3–17или17–31июля2027,10–16,EN,CHF7000/2weeks:Матвейпосле10-летия,Оскарпоканет. EmbassyAIFuture4–24июля2027,9–19,hotelpackage:Матвейagecandidate,Englishimmersion/AIgroup9–10уточнить. ZuozDigital10–17:новыедатыTBA,AIмодуль12–15.',ids=['L168','L169','L192','L170','L171','L172']),
        dict(name='Хакатон / проект · действительное достижение',detail='CoolestProjects2027showcaseдляобоих≤18,датыпоканет. IKCC2027объявляетначало3января(Game)/1сентября(Open);7+напервыйденьрегистрации,individual,schooldocumentобязателен. LSCU10начинается2декабря2026,120minсамостоятельногоScratchбезAI;foreignremoteentryуточнить. Penang10Octoberfinalнедоступенбезпрошлогоотбора.',ids=['C039','C843','C844','C842','C840']),
        dict(name='Крупные тематические события',detail='Выставкиостаётсяотдельнымразделомссемейным/взрослымдопуском. EUCodeWeek—сетьlocalactivities,акаждыйshowcaseнеотборныйworldfinal. IronScholars3–4October—маленькийчасовойBuildZone,старыйGlobalGameshackathonclosedнеприписан2026. Составкрупныхeventsпроверяетсяпогороду,датамидетскимправилам.',ids=['L194','E130'])],
    gaps=[
        'ЛатинскаяАмерика:имеютсяместныеESкандидатыиArgentina/Peru2027программы,ноEnglish/Spanishinstructionневыводитсяизсайта. BrazilPortuguese/foreigngateикрупныеopenboardingrobotcampsCentralAmericaещёнедостаточноподтверждены.',
        'Европа:первичныесведенияновыхпрограммCH/GB/DE/ES/FIдобавлены;восточная/севернаяЕвропа,другиепансионыифактические2027cohortsпокапокрытычастично.',
        'Азия:Singapore/HongKong/Malaysia/Thailand/Koreaдобавлены;Taiwanпервичнаяпроверкасохранена. Japan/China/India/Vietnamиостальныестранытребуютновыхlocalholiday/foreign/ENsupportисточников.',
        'Детскиеinternationalhackathons6/9редкивпрочитанномнаборе;немалоанонсовдля12+/highschool/universityилипрошедшихсезонов. Открытаямеждународнаязаявкадля6-летнегонеустановленаоднимсловомkids.',
        'Необъявленныйсезон,наличиемест,языквсехуроков,возрастнадатуисоставтрансферадолжныбытьподтвержденыдооплаты;сайтсейчассобираетпланирование.'],
    source_issues=issues)
for key in ['family']:
    focus[key]=spaces(focus[key])
for row in focus['routes']:
    row['detail']=spaces(row['detail'])
focus['gaps']=[spaces(x) for x in focus['gaps']]
d['camp_focus']=focus
a=d['completeness_audit']
a.update(version=19,checked=DAY,baseline=baseline,new_ids=added,new_profiles=[],updated_ids=updated,
    conclusion='Мировой охват частичный. Все лагеря, соревнования и выставки по всем странам пока не собраны; неизвестные даты, языки и допуски отмечены явно.',
    scope='Первичная проверка дополнительных лагерей / пансионов / English поддержки в Европе и Азии; LatinAmericaengineeringальтернатива и обновлениеConversa; детскиеcoding-проекты / taskhackathon. Предыдущие33SouthAmericaкарточки сохранены.',
    camp_focus=focus)
a['source_issues']+=issues
a['caveats'] += ['Новыеcardcountsвключаютtracks/форматы/смены;неравнычислунезависимыхoperators/camps.',
    'EnglishnativeперсоналилиwebsiteнеприравненыкwholecourseEN;основнойязык/поддержка/языковыеурокиразделены.',
    'Датаactivity_startнапоминаетначалосоревнования/приёма,неполныйпериодконкурса;camp_windowнеежедневноеприсутствиевесьсезон.']
a['known_backlog'].append(dict(kind='Camps',name='Полноталетнихпансионов/ENилиESroboticsиchildhackathons',reason='; '.join(focus['gaps']),url='https://www.stgeorges.ch/fr/camps/summer-camps'))
d.update(asof=DAY,source_count=len(d['sources']))
d['expansion_log'].append(dict(version=19,date=DAY,scope='EuropeAsiaLATAMcampsandchildprojects',added_ids=added,updated_ids=updated,
    notes=['All1135baselineIDs/67profiles/46legacyroutes/family/Taiwan/local/SouthAmericafocuspreserved.',
        'Instruction/support/languagelessonsdistinct;pastcampdatesnotreused;boardingminseparate.',
        'Noaccounts/registrations/messages/paymentsperformed.']))
planpath=ROOT/'data/research-plan.json';plan=json.loads(planpath.read_text());plan.update(updated=DAY,completeness_audit='data/audit-v19.json')
for row in plan['requirements']:
    if row['id']=='camps':row['evidence']='v19:29additionalcamp/learningcards;EuropeCH/FI/DE/ES/UK,AsiaSG/HK/MY/TH/KR,CRIengineering;primary/support/Englishlessonsseparated,worldcoveragepartial.'
    if row['id']=='eligibility':row['evidence']='v19:boardingmin8/9/10vsday4–14;grade/birthdaycutoffs,individualschooldocument,germanEnglishsupport;foreignentryunknownvisible.'
plan['latest_validation']=dict(version='v19',status='pending',research_status='partial',carried_forward_version=18)
plan['next_research'].insert(0,'Лагеря / детские hackathons: '+'; '.join(focus['gaps']))
planpath.write_text(json.dumps(plan,ensure_ascii=False,indent=2));PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2))
(ROOT/'data/camps-audit-v19.json').write_text(json.dumps(focus,ensure_ascii=False,indent=2))
assert len(added)==35 and len(d['events'])==1170
print(json.dumps(dict(added=len(added),learning=sum(byid[x]['block']=='Лагеря' for x in added),total=len(d['events']),ids=added),ensure_ascii=False))
