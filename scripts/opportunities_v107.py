"""Selected primary 2026–27 competition clauses; preserve the wider atlas."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED = '2026-10-05'
BASE = 'faad1e27121ecfc06854fbbd02f676c1726931f8'
W = 'https://worldrobotleague.net/'
G = 'https://waicy-cdn.wholeren.cn/wp-content/uploads/2026/09/WAICY-2026-Guidebook.pdf'
R = 'https://www.roboraveinternational.org/'
RF = 'https://www.robofest.net/images/2627/General2027.pdf'
HOST = 'https://www.kw.ac.kr/ko/life/newsletter.jsp?BoardMode=view&DUID=53144'
NEW_IDS = ['C'+str(i) for i in range(1145,1155)] + ['E189']
UPDATED = ['C037','C053','C082','C083','C087']

def ref(label,url): return dict(label=label,url=url)

def enrich(d):
    ev = {e['id']:e for e in d['events']}
    e = ev['C037']
    e.update(title='WAICY 2026 · AI Showcase · проект решения реальной проблемы',
      age='Сайт: 6–18; руководство: under 18. Все школьные классы; точный возраст на контрольную дату уточнить.',
      mat='Да по возрастной рамке; проект, класс и допуск отдельно',
      osc='Условно: должно исполниться 6 лет по контрольной дате; день рождения не задан',
      period='Глобальный срок руководства 29 ноября 2026, 17:00 ET; Showcase section содержит старый 2025 год. Финал 4–6 / 5–7 декабря расходится.',
      date_status='Конфликт дат / лет в источнике', source='https://www.waicy.org/waicy-2026/',checked=CHECKED,
      gear='Решение реальной проблемы с ИИ; описание проекта и AI usage до250 слов каждое; видео до6мин: презентация3мин + демонстрация3мин. Указать собственную работу детей.',
      proof='Прочитаны actual2026 page и текущее30-страничное руководство: выбранные разделы и визуальные страницы3/9/14/20/29. Global2026deadline и отдельные Art/Video/LLM2026 deadlines подтверждаются; Showcase subsection всё ещё2025.',
      note='AI Showcase, Art, Video и LLM/AI Agent — отдельные задания и карточки. Общий срок29.11.2026 17ET есть наp3, но Showcase p5 содержит29.11.2025; подтвердить применимость к Showcase. Финал p2 старый2025/p3 5–7декабря/p29 4–6декабря2026: точные дни не экспортируются. Сертификат участия не равен Gold/Silver/Bronze. Перевод во время презентации допускается, EN-материалы нужны; инструменты должны разрешать законное использование ребёнком с родителем.',
      references=[ref('Текущее руководство · отдельные требования и конфликты',G),ref('Rubrics','https://www.waicy.org/rubrics/')],
      related_ids=['C1152','C1153','C1154'])
    e = ev['C053']
    e.update(source=RF,checked=CHECKED,
      proof='Прочитаны current General2027 V1 от25.09.2026 (selected timeline/category clauses) и собственное сообщение KwangWoon: host объявил28–31мая2027 подтверждёнными, но международный PDF всё ещёTENTATIVE.',
      note=e['note']+' Университет-host в августе2026 сообщает официальный28–31мая2027; более новый международный V1 25сентября всё ещёTENTATIVE. Конфликт полномочий/версий не снят: поездку пока не считать подтверждённой.',
      references=[ref('Текущий календарь','https://www.robofest.net/index.php/current-competitions/main-page'),ref('Объявление университета-host',HOST),ref('International Directors','https://www.robofest.net/index.php/about/international-directors')])
    # Replacing each note with a stable literal keeps a repeat execution idempotent.
    e['note']='Определяющим является школьный класс весной2027, а не только возраст. Explorer1–4; Game/Exhibition Junior5–8, waiver отдельно и не гарантирован. Национальное представительство/квота отдельно. Университет-host в августе2026 сообщает официальный28–31мая2027; более новый международный V1 25сентября всё ещёTENTATIVE. Конфликт полномочий/версий не снят: поездку пока не считать подтверждённой.'
    for ident,slug in [('C082','roborave-puerto-vallarta-open-2027'),('C083','roborave-guanajuato-open-2027'),('C087','roborave-world-championship-houston-2027')]:
        e = ev[ident]
        e.update(source=R+'en/events/'+slug, checked=CHECKED,
          references=[ref('a-MAZE-ing:8–15лет,2–4участника',R+'en/programs/a-maze-ing'),ref('Текущий календарь сети',R+'en/events')],
          proof='Повторно прочитаны actualevent page и actuala-MAZE-ing:8–15лет,2–4students. Остальные категории и международная квота проверяются отдельно.')
    ev['C082']['format']='Команда2–4участника для a-MAZE-ing; остальные дисциплины по локальным правилам'
    ev['C083']['scope']='national'
    ev['C083']['note']='В заголовке International, в основном тексте NATIONAL2027. 21–22мая названо tentative: точные дни не экспортируются. RRID бесплатно, взнос отдельно. a-MAZE-ing8–15/2–4; младшие категории и зарубежный вход уточнить. Оскар2020 года рождения максимум7лет в2027: a-MAZE-ing не подходит.'
    ev['C087']['osc']='Нет для a-MAZE-ing8–15: Оскару 2020 г.р. будет максимум 7 лет в 2027. Другие дисциплины уточнить.'
    ev['C087']['note']='Мировой финал сети и Open имеют разный формат и допуск. Для a-MAZE-ing8–15 Оскар2020г.р. не достигает8лет ни в один день2027; это не исключает все остальные дисциплины. Точные5–7ноября опубликованы, площадка ещёPorconfirmar, актуальные взносы не опубликованы. SpaceCenter/NASA в программе — заявление организатора, не доказательство одобрения NASA или автоматического доступа/отбора.'

    def card(ident,title,source,**kw):
        e=dict(id=ident,block='Соревнования',title=title,country='Южная Корея',region='Азия',city='Площадка и город покаTBA',source=source,checked=CHECKED,
          start='',end='',deadline='',period='Февраль 2027; точные дни, город и регистрация пока не объявлены',date_status='Предварительно',
          age='По категории / класс и контрольная дата отдельно',mat='Условно: подтвердить свою категорию',osc='Условно: подтвердить свою категорию',
          format='Команда / индивидуальный формат по правилам категории',participation='team',admission_kind='open_registration',
          entry='WRL / IREA обещает регистрацию международных команд. Точные дни, площадка и окончательные правила 2027 года ещё не опубликованы.',
          gear='По конкретной категории',language='Правила опубликованы на английском и испанском. Язык судейства и наставника не установлен.',languages=[],
          language_certainty='EN/ES текст правил не означает EN/ES судейство или обучение.',cost='Взносы, способы оплаты и расходы на оборудование, проживание и транспорт ещё не опубликованы. Визовое приглашение не является одобренной визой.',
          scope='international',level='Международный открытый турнир · развивающаяся сеть',
          importance_reason='Масштаб по текущему собственному приглашению; словоWorld не доказывает сопоставимость с FIRST/VEX/WRO или независимое мировое лидерство.',
          reward='Заявлены Grand, Gold, Silver и Bronze по категории. Победу подтверждает официальный протокол; сертификат участия имеет другое значение.',
          priority='P2 — поездка после правил, допуска и полного бюджета',status='Идея',
          action='Дождаться точных дней, площадки и взносов; проверить класс, возраст и окончательные правила своего дивизиона. Затем решить о поездке.',
          proof='Прочитаны собственное приглашениеWRL 2027 и подробная страница правил. Февраль без точных дней не превращён в календарную смену.',
          note='WRL и RoboRAVE Korea проходят вместе; это не RoboRAVE WorldChampionship Houston. Девять стран относятся к прошлым мероприятиям, не подтверждённому roster2027. Английская регистрация/визовые приглашения обещаны, не оформлены.',
          references=[ref('Приглашение, расписание и иностранный вход',W)],themes=['robotics'],registration_status='Регистрация ещё не объявлена; заявка семьи не подана.')
        e.update(kw)
        e['iso'] = {'Южная Корея':['KOR'],'Китай':['CHN'],'Онлайн / США':[]}.get(e['country'],[])
        if ident in ev:
            idx=next(i for i,x in enumerate(d['events']) if x['id']==ident);d['events'][idx]=e
        else:d['events'].append(e)
        ev[ident]=e
        return e
    card('C1145','WRL 2027 · Robot Battle Othello Junior U12',W+'rules/othello/',
      age='Junior U12: 12 лет включительно и младше по регламенту. Минимальный возраст и контрольная дата не указаны.',
      format='Матчи 1:1 либо 2:2 с управлением роботами; формат может меняться по числу участников',participation='individual',
      gear='Собранный remotecontrol робот≤500g(+3g),25×25×25cm,≤11.7V; selfmade или один серийный комплект с разрешёнными исключениями. Матчи2мин/11двухцветных блоков.',
      note='Оба входят в верхнюю возрастную рамку, но минимальный возраст и контрольная дата не опубликованы. AI Othello Junior / Senior только анонсированы; для них будут отдельные правила. Текущий Othello с управлением роботом не является этим ИИ-треком.')
    card('C1146','WRL 2027 · MRC Soccer LEGO Junior5–13',W+'rules/mrc-soccer/',
      age='В обзоре WRL и правилах Thai MRC 2026: Junior 5–13 лет. Дивизион 2027 года и контрольную дату нужно подтвердить.',
      mat='Условно: входит в рамку 5–13 лет; окончательный дивизион 2027 и допуск отдельно',osc='Условно: входит в рамку 5–13 лет; минимальный возраст подходит, окончательный дивизион 2027 отдельно',
      format='2–3 участника, 2–4 робота; два тайма по 2 минуты',gear='AllLEGO≤1000g,20cmcube,расширение25×25cm. WRL перечисляетLEGO SpikeJr; ThaiMRC2026 допускает всеLEGOмоделиJunior.',
      references=[ref('WRL 2027 invitation',W),ref('Авторитетные ThaiMRC LEGO2026 правила','https://mrc.makerrobotics.co.th/futsal-lego/')],
      note='WRL summary не заменяет связанный ThaiMRC регламент. В собственном summary есть альтернативныеMRC/KRL модели; окончательные изменения обещаны≥50дней до турнира. ThaiMRC2026 roster20команд не перенесён на Korea2027. Оба входят5–13, но это ещё не приём семьи.')
    card('C1147','WRL 2027 · Humanoid Relay · будущая открытая категория',W+'rules/humanoid-relay/',
      age='По объявлению возраст и национальность не ограничены. Состав команды, требования к роботам и подсчёт баллов ещё не опубликованы',
      gear='Командные миссии гуманоидных роботов. Конкретная техника, задания и расходы ещё не опубликованы.',
      mat='Условно: возраст не ограничен; полные правила категории ещё не готовы',osc='Условно: возраст не ограничен; полные правила категории ещё не готовы',
      priority='P3 — наблюдать будущие правила; поездку не бронировать по этому анонсу',note='Открытый возраст не доказывает подходящую маленькому ребёнку задачу или доступную технику. Правилаcomingsoon; это ориентир будущего маршрута, не готовый детский чемпионат.')
    common=W+'rules/roborave/'
    for ident,title,age,gear,note in [
      ('C1148','SumoBot LEGO/VEXIQ ES','Elementary School (ES). Школьная контрольная дата и минимальный возраст не опубликованы.','Autonomous≤1kg;официальныеLEGO/VEXконтроллер,моторы,датчики;25×18cm. KoreaOpenring800mm,globalV6.2ring100cm: локальная поправка имеет приоритет.','Не переносить глобальный100cmring наKorea800mm. Для обеих детей подтвердитьESкласс и иностранныйroster; одно словоelementary не доказывает6летминимум.'),
      ('C1149','Line Following ES','Elementary School (ES). Возраст и школьная контрольная дата проверяются отдельно.','AutonomousLEGO/VEXIQ либоOpen;≤1500USDrobotcostlimit,65030cm³. 3мин,чёрнаялиния,доставка шариков; ES75–125точное число объявляют на событии.','1500USD — потолок стоимости робота, не взнос. Местный grade/minage иteamcount неизвестны; не подставлять изa-MAZE-ing.'),
      ('C1150','SoccerBot RC ES','Elementary School (ES). Минимальный возраст и контрольный класс проверяются отдельно.','2RCробота≤800g каждый/15cmcube;≤500USDeachteam по собственномуsummary (единицу уточнить). Два тайма90сек; безshooting/grabbingball.','Это RC, неautonomousMRCsoccer. 500USD — аппаратное ограничение вsummary, не билеты или семейнаяцена; формулировкуeachteam уточнить.'),
      ('C1151','a-MAZE-ing ES','Глобальное правило: 8–15 лет. Локальная категория ES, контрольная дата и исключения отдельно.','2–4students по глобальномуchallenge; autonomousone robot/maze2мин. Gyro/externalmazesensorsprohibited; wheelencodersallowed.','Оскару2020г.р. максимум7лет в2027: поglobal8–15 не подходит. Корейскийsummary даётES/MS безнижнегопорога: младшийoverride не опубликован; не считать допуск доказанным.')
    ]:
        card(ident,'RoboRAVE Korea Open 2027 · '+title,common,age=age,gear=gear,note=note)
    ev['C1151']['osc']='Нет по глобальному8–15; младшее локальное исключение не подтверждено'
    ev['C1151']['references'].append(ref('Globala-MAZE-ing8–15/2–4',R+'en/programs/a-maze-ing'))

    final_conflict='Точные даты защиты не установлены: currentPDFp2 содержит2025,p3 5–7декабря,p29 4–6декабря2026. В календарь добавлен только срок подачи. Сертификат участия не равен призу; инструменты и работа взрослого должны быть раскрыты.'
    for ident,title,gear,note in [
      ('C1152','AI Generated Art · The Future We Choose','Идея≥250слов,процесс/prompts≥250слов,≥2iterationimages,finalPNG/JPEG и2минpitch; показать собственные решения ребёнка.','Всеgrades. Оценивают идею/эволюцию/вклад автора, не только красивую генерацию.'),
      ('C1153','AI Generated Video · The Future We Choose','Finalvideo1–2мин ENилиENsubtitles;concept200–300слов,script/storyboard≥3keyscenes,workflow250–400слов,≥3sceneprocess descriptions; инструменты/источники раскрыть.','Всеgrades; Storytelling/visualdirection/humanediting обязательны, готовыеAIклипы без своей истории недостаточны.'),
      ('C1154','LLM & AI Agent · AI as a Service','Создать специализированного персонализированногоadviser;documentproblem/users/tools,testing,refinement,limits/ethics/citations.','Всеlevels welcome, но рассчитан наuppermiddle/highschool и безотдельныхвозрастныхгрупп; маленькие дети конкурируют со старшими. Это усложнённый проект, не основной стартовыймедальныймаршрут.')
    ]:
        card(ident,'WAICY 2026 · '+title,G,country='Онлайн / США',city='Удалённая подача; форматфинальнойзащиты уточнить',region='Онлайн / мир',
          age='Сайт: 6–18 лет; PDF: младше 18; все школьные классы. День рождения и контрольную дату уточнить.',mat='Условно: возраст подходит; самостоятельность проекта и правила отдельно',
          osc='Условно: должно исполниться 6 лет по контрольной дате; помощь взрослого раскрыть',format='Индивидуально или команда 1–5 участников по общему разделу руководства',participation='individual',
          entry='Подготовить пакет своегоtrack и подать черезофициальную2026форму; международныйremoteформат объявлен, заявка не отправлена.',
          deadline='2026-11-29',deadline_utc='2026-11-29T22:00:00Z',deadline_label='Подача WAICY Art / Video / LLM',
          deadline_note='29ноября2026,17:00EasternTime =22:00UTC/16:00Коста-Рика; отдельныеcurrenttracksections повторяют2026. Днифинала всёещёконфликтуют.',
          period='Подача29ноября2026 17:00ET; днифинала требуют уточнения',date_status='Подтверждён срок подачи; конфликт дней финала',
          gear=gear,language='Конкурсные материалы на английском; видео на английском либо с английскими субтитрами. Руководство допускает перевод во время живой презентации.',languages=['EN'],
          language_certainty='Английские материалы и субтитры прямо установлены руководством. Это конкурс, язык лагеря здесь не оценивался.',
          cost='Актуальнаяполнаяцена не опубликована; guidehistoryупоминаетfreeparticipation, это не отдельныйinvoice2026. AItools/network отдельно.',
          reward='Participationcertificate дляподавшихвовремя;Gold/Silver/Bronze оцениваются отдельно. Приз не гарантирован.',priority='P1 — ближайший удалённый проект после проверки правил',
          action='Выбрать один посильныйtrack, сделать самостоятельныйчерновик/дневникитераций и до29ноября проверитьвозраст/актуальностьформы/полныйпакет.',
          proof='Прочитано текущее30-страничное руководство: selectedArt/Video/LLMrequirements и2026deadline. Визуально сверены страницы3/9/14/20/29, сохраненыконфликтыгода/финала.',
          references=[ref('WAICY 2026 homepage','https://www.waicy.org/waicy-2026/')],themes=['ai','technology'],
          note=note+' '+final_conflict,related_ids=['C037'],registration_status='Официальная форма связана с руководством; это не подтверждает открытый набор. Заявка семьи не отправлена.')
    card('E189','Beijing2027 · Humanoid Robot Half Marathon · технологическое событие',
      'https://www.beijing.gov.cn/fuwu/lqfw/gggs/202608/t20260824_4833810.html',block='События',country='Китай',region='Азия',city='Пекин · Yizhuang',
      start='2027-04-18',end='2027-04-18',period='',date_status='Подтверждено',date_scope='festival_window',
      age='Командыразработчиковроботов/университеты/индустрия; минимальныйвозрастпосетителя не опубликован.',
      mat='Условно: только посещение после подтверждениядетскоговхода',osc='Условно: только посещение после подтверждениядетскоговхода',
      participation='visitor',admission_kind='visitor',visitor_policy='confirm_children',visitor_policy_note='Официальныйанонс не содержит семейныхбилетов/зон/условий несовершеннолетних.',
      format='Очная роботизированнаягонка; это не многопрофильнаявыставкакомпаний и не лагерь.',
      entry='Уточнить открытуюзонупосещения/билеты/детскийвход; семейноеучастиевроботгонке не подтверждено.',
      gear='Гуманоидныероботы на дистанцииполумарафона; публичнаяпрограмма/tickets ещёне опубликованы.',
      language='Языккомментариев/семейнойпрограммы неустановлен',languages=[],cost='Посещение/билеты/семейныезоны не опубликованы; инженерныйвзнос не равен цене посетителя.',
      level='Международноетехнологическоесобытие · объявление муниципалитета',priority='P3 — ознакомление приподходящейпоездке',
      reward='Посещение не даёт конкурснойнаграды',action='Передпоездкой проверить новый visitorанонс, детскийвход и реальныеплощадкинаблюдения.',
      proof='Прочитан собственныйmunicipalannouncement24августа2026: новаядата18апреля2027 и приглашениекомандразработчиков.',
      references=[],note='Дата 2027 года объявлена, но состав участников, билеты и детский вход не подтверждены. Гонка не включена в счёт крупнейших торговых выставок компаний.',themes=['robotics','technology'])

    categories=[]
    for ident in NEW_IDS[:7]:
        e=ev[ident];categories.append(dict(name=e['title'],age=e['age'],team=e['format'],hardware=e['gear'],age_rule='По конкретномуpublisheddivision; дата/gradeпроверяются отдельно',entry=e['entry'],event_id=ident))
    p=dict(id='world-robot-league',name='World Robot League / IREA · KoreaOpen',group='international',age_summary='Othello≤12;MRCSoccerJunior5–13;RoboRAVEES;HumanoidRelayallages. Февраль2027TBA.',age_tags=['6','9','10-12'],
      summary='Развивающаяся международнаяоткрытаяплощадкаКореи: выбирать категорию, не считатьWordWorld независимыммировымрейтингом.',categories=categories,event_ids=NEW_IDS[:7],legacy_ids=[],
      route=['Выбрать конкретныйвозрастной/gradeдивизион','Дождаться места/дней/полных2027правил ивзносов','Собратьteam иrobotсоответствующегокласса','Получить иностранныйдопуск и решитьопоездке','Сохранятьпротокол/рольребёнка/инженерныйдневник'],
      hardware='Othelloсамодельный/серийный≤500g;MRCAllLEGO;RoboRAVEкатегорииимеютразныеплатформы;HumanoidTBA.',
      language='EN/ESправила есть;Englishregistrationобещана. Язык судейства/обучения не установлен.',importance='Internationalopennetwork, не доказанныйtierFIRST/VEX/WRO и не мироваятаблица лидеров.',
      strengths='OthelloU12 иMRCSoccer5–13 дают младшиевозрастные кандидаты; иностранныйвход заявлен.',
      requirements=['Возраст/класс/cut-off отдельно','Техосмотр по окончательнойкатегории','Полныйбюджет/взнос/языксудейства ещёTBA'],
      nuances=['AI Othelloтолькоplanned, текущийOthelloremotecontrol','MRC/KRLсущественноразличаются; финальныеправила≥50днейдо турнира','RoboRAVEKorea не HoustonWorlds; слот/квотаавтоматически неследует','AllagesRelay покабезполныхправил'],
      cost='Текущие2027взносы/проезд/gear/ночлег не опубликованы.',award='ЗаявленыGrand/Gold/Silver/Bronze; достижение подтверждается отдельнымпротоколом.',
      sources=[dict(title=title,url=url,checked=CHECKED) for title,url in [('WRL 2027 invitation',W),('Othello',W+'rules/othello/'),('MRC',W+'rules/mrc-soccer/'),('Relay',W+'rules/humanoid-relay/'),('KoreaRoboRAVE',W+'rules/roborave/')]],
      evidence='Собственныеprimaryclauses прочитаны; независимое мировоелидерство/новыйroster/teacherlanguage не доказаны.',checked=CHECKED)
    profiles=d['league_guide']['profiles'];profiles[:]=[q for q in profiles if q['id']!=p['id']]+[p]
    waicy=next((p for p in profiles if any('C037'==x for x in p['event_ids'])),None)
    if waicy:
        waicy['event_ids']=list(dict.fromkeys(waicy['event_ids']+['C1152','C1153','C1154']))
    urls={e['source'] for e in d['events'] if e['id'] in NEW_IDS+UPDATED}
    urls.update(s['url'] for e in d['events'] if e['id'] in NEW_IDS+UPDATED for s in e.get('references',[]))
    present={s['url'] for s in d['sources']}
    for u in sorted(urls-present):d['sources'].append(dict(url=u,title='Selected2026–27 competition source',checked=CHECKED,evidence='Первичныйисточник; конкретныеконфликты/неизвестные условия указаны вкарточках.'))
    d['source_count']=len(d['sources'])
    return d

if __name__=='__main__':
    p=ROOT/'data/catalog.json';d=json.loads(p.read_text());enrich(d)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2))
    print(json.dumps(dict(new_competitions=10,new_visitor_event=1,updated_ids=UPDATED,new_league_profiles=1)))
