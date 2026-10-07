"""Primary programme and contract review: French junior boarding, Spain and Canada."""
from pathlib import Path
from collections import Counter
from camp_planning_v108 import offer

ROOT = Path(__file__).resolve().parents[1]
BASE = '030dd4687c8f67458979b87004d93af7aab318f4'
CHECKED = '2026-10-06'
ENJOY = 'https://www.enjoy-sejourslinguistiques.com/'
LBS = 'https://littlebritishschools.com/stages-de-vacances/summer/'
MAS = 'https://www.masdethau.com/'
AGORA = 'https://lledo.agorainternationalschool.es/'
BROCHURE = AGORA+'fs/resource-manager/view/e571fcaa-ef18-4f59-89b4-cdc81be61970'
RIDLEY = 'https://www.ridleycollege.com/camps-summer-programmes/'
DAY = RIDLEY+'summer-day-camps/'
NEW = ['enjoy-autumn-junior','enjoy-winter-junior','enjoy-spring-junior',
       'littlebritish-best','littlebritish-grammar-archive','masthau-family',
       'agora-lledo-super','agora-lledo-mini-science','agora-lledo-tech-young','agora-lledo-tech',
       'ridley-junior-science','ridley-dot-dash','ridley-spike-intermediate','ridley-spike-senior','ridley-board']
NEW_OFFERS = ['enjoy-autumn-both','littlebritish-best-oscar']
ASK = 'До выбора получить подтверждение места, приёма приезжей семьи, возрастной группы и окончательного счёта. Заявки, сообщения и оплаты не выполнялись.'

def add_europe_canada_v130(add,src,fit,profiles):
    names={'FRA':'Франция','ESP':'Испания','CAN':'Канада'}
    def emit(i,name,iso,place,themes,formats,age,language,programme,timing,price,housing,mf,of,sources,
             status='next_unannounced',confirmed=None,role=None,sessions=None):
        add(NEW[i],name,names[iso],iso,place,themes,formats,age,language,programme,timing,price,housing,mf,of,
            'Редакционный кандидат по опубликованному syllabus, возрастам и условиям. Международный или мировой рейтинг качества этой программы не установлен.',
            [ASK],sources,status=status,confirmed=confirmed,sessions=sessions)
        p=profiles[-1];p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
        if role:p['language_evidence_role']=role
        return p
    both=fit('conditional','Группа 6–10 предварительно подходит обоим. Для Матвея верхняя граница на дату смены и приём детей без французского отдельно; место не подтверждено.')
    ey='Младшая группа билингвальная FR/EN, постепенно увеличивает английский. Полная English-only политика относится к 11–17, не переносится на 6–10. Для уже свободно говорящих детей проверить уровень и поддержку без французского.'
    ep='Утром игровые языковые занятия, после обеда спорт, творчество и кулинарные workshops; младший проект отдельно от подросткового. Это общий языковой пансион с digital detox, не robotics/AI intensive. PDF запрещает личные подключённые устройства; звонки семье через телефон лагеря. Полный педагогический проект выдают после регистрации, он ещё не прочитан.'
    es=[src('Ближайшие наборы, младшие 6–10',ENJOY+'prochains-sejours'),src('Младший билингвальный проект, транспорт и питание',ENJOY+'faq'),src('Текущий общий прайс: 820 TTC, транспорт отдельно',ENJOY+'tarif'),src('Формы: для зимы/весны пока soon',ENJOY+'formulaires')]
    p=emit(0,'Enjoy! · Vers l’immersion · осень 2026','FRA','Tourville-sur-Pont-Audemer, Eure; ближайшая станция Bernay','general,languages,sport','boarding','6–10; отдельная группа от 11–17',ey,ep,
        '19–24 октября 2026, понедельник 10:30 — суббота 16:30 по конкретной странице. Общий FAQ ещё пишет окончание в пятницу; приоритет отдаётся конкретному заезду, часы перед поездкой подтвердить.',
        dict(year=2026,label='EUR 820 TTC / ребёнок, шесть дней; двое EUR 1 640 базового лагерного пакета.',included='Проживание, питание, языковые занятия и активности. FAQ перечисляет четыре приёма пищи в день; общий тариф младших указывает 15 часов языкового курса.',
             extras='Дорога не включена. Возможна navette к Bernay, тариф/включение не установлены. VACAF/Pass Colo не применены к международной семье автоматически; семейная скидка не доказана.',
             deposit='Опубликованный пустой dossier требует аванс 50%, EUR 410 на ребёнка, в счёт цены; это не дополнительный сбор. Действующие правила отмены/возврата и страхования не найдены в прочитанном dossier.'),
        'Детский пансион на кампусе Lycée Agricole Privé; родители там не проживают. Максимум 30 детей и 5–6 специалистов — собственное заявление конкретной страницы.',both,both,
        [src('Конкретная осенняя смена и TTC',ENJOY+'19-24-octobre-2026'),src('Пустой dossier октября 2026: аванс/младший проект/digital detox',ENJOY+'_files/ugd/040825_d1aabdd841554689b2bd8d6beae12345.pdf')]+es,
        status='published_2026',confirmed=['EN','FR'],role='bilingual_camp_life',sessions=[['2026-10-19','2026-10-24']])
    p['timing']['session_details']=[dict(start='2026-10-19',end='2026-10-24',label='Vers l’immersion · 6–10',source=ENJOY+'19-24-octobre-2026',place=p['place'],price=p['price']['label'],date_scope='boarding_session',date_precision='published_session',proof='Конкретная страница и PDF прямо повторяют 19–24 октября 2026; weekday соответствует календарю. Общий FAQ Friday отмечен отдельно.')]
    for i,title,url,label,price_label in [
        (1,'Enjoy! · младший зимний набор 2027','1-6-mars-2027','Upcoming пишет 1–6 марта 2027, но detail-page и формы озаглавлены FÉVRIER 2027. Точный месяц/даты конфликтуют; сессия и ICS не создаются.','EUR 820 all-inclusive на detail-page; 2027 итог и действующий dossier ещё нужны.'),
        (2,'Enjoy! · младший весенний набор 2027','avril-2027','Заголовок 19–24 апреля 2027 (Пн–Сб), описание говорит Вс–Пт. До письменного исправления точный заезд и ICS не создаются.','EUR 750 на странице апреля против EUR 820 TTC в общем тарифе младших. Цена 2027 не установлена; расхождение не усредняется.')]:
        p=emit(i,title,'FRA','Tourville-sur-Pont-Audemer, Eure','general,languages,sport','boarding','6–10; проверить верхнюю границу на дату',ey,ep,label,
            dict(year=2027,label=price_label,included='Страницы обещают жильё, питание, языковые занятия и активности; точный новый пакет требует подтверждения.',extras='Транспорт отдельно. Тариф трансфера, страхование, международный приём, возврат и состав цены нового сезона ещё неизвестны.',deposit='Новые dossier в forms обозначены bientôt disponible. Октябрьский аванс EUR 410 не перенесён на новый прайс; заявку не отправляли.'),
            'Проживание детей на кампусе; тип комнаты и ночной присмотр выбранного 2027 заезда отдельно.',both,both,[src('Страница конкретного сезона с противоречием',ENJOY+url)]+es,
            status='partial_2027',confirmed=['EN','FR'],role='bilingual_camp_life')
        p['questions'] += ['Получить исправленные единые даты, цену и новый договор: сейчас страница набора расходится с другими первичными страницами.']
    p=emit(3,'Little British Schools · Best of LBS 2027','FRA','Paris 6/7/16/17 и Meudon: один курс в пяти школах','general,languages,science,art','day','3–6 в опубликованном расписании; не CE1–CM2',
        'На странице прямо сказано, что занятия полностью на английском.',
        'Общий тематический курс: STEM-опыты, музыка, британская культура, роли и творчество. 2,5 часа в день; это не полный дневной лагерь и не обещанный курс роботов.',
        '23–27 августа 2027, пять будних дней. На каждой площадке утро 09:30–12:00 либо день 14:00–16:30; выбирать одну группу.',
        dict(year=2027,label='EUR 300 / ребёнок за пять полудней, 12,5 часа.',included='Короткие английские занятия и тематические активности.',extras='Проживание семьи, транспорт, питание и care вне 2,5 часа не включены в опубликованный тариф; отдельный полный день не рассчитан.',deposit='Публичная карточка не устанавливает оплату/отмену/возврат; нужен договор выбранной школы.'),
        'Дневное пребывание 2,5 часа; родители организуют жильё и остальной день.',
        fit('not_eligible','Матвей старше группы 3–6.'),fit('conditional','Оскару только пока он ещё 6 на дату курса; после 7-летия эта группа не подходит.'),
        [src('Конкретный курс 2027: даты, возраст, язык, расписание и цена',LBS+'the-best-of-little-british-2027/')],
        status='published_2027',confirmed=['EN'],role='general_instruction',sessions=[['2027-08-23','2027-08-27']])
    p['timing']['session_details']=[dict(start='2027-08-23',end='2027-08-27',label='Best of LBS · выбранная школа и половина дня',place=p['place'],source=LBS+'the-best-of-little-british-2027/',price=p['price']['label'],date_scope='day_camp_window',date_precision='published_session',proof='Одна тематическая программа с пятью альтернативными адресами, не пять независимых операторов. Конкретный campus/утро/день ещё выбираются.')]
    emit(4,'Little British Schools · Grammar Boot Camp · архив','FRA','Paris 6/7/17; список других школ в footer не подтверждает открытый набор','languages,general','day','Collège: 6e–3e; класс, а не возраст всей сети',
        '100% англоязычный учебный курс по карточке.',
        'Интенсив устной/письменной речи, грамматики, словаря и произношения; самостоятельные сезонные модули. К техническому STEM-потоку младших не относится.',
        'Точный архив 24–28 августа 2026; группы complet. Ссылки footer на зиму/весну 2027 не устанавливают новый летний заезд.',
        dict(year=2026,label='Архив EUR 250 / 12,5 часа; не цена нового набора 2027.',included='Пять занятий по 2,5 часа.',extras='Жильё, дорога, остальной день отдельно.',deposit='Условия нового сезона не подтверждены. Прошлое complet не объявляет будущий набор закрытым.'),
        'Полудневный курс, без пансиона.',fit('later','Потребуется реальный класс Collège; Матвей сейчас младше школьной категории.'),fit('later','Оскар пока младше Collège.'),
        [src('Текущая ссылка из Best of ведёт на архив 2026, Collège',LBS+'grammar-boot-camp-summer-3/')],status='archive_next_unannounced',confirmed=['EN'],role='language_instruction')
    emit(5,'Mas de Thau · семейная программа с Kids’ Club','FRA','Languedoc / Occitanie, рядом с Mèze и Thau','general,nature,art,sport','family','Kids’ Club 3 месяца–12 лет; 12+ отдельный teen sport',
        'Команда детей прямо названа native English nannies либо bilingual animation team. Это подтверждённая поддержка EN, не обещание исключительно английского всех активностей.',
        'Природа, поисковые игры, строительство, животные, drawing/junk art, кулинария и водные игры. Родители живут вместе с детьми. Самостоятельная robotics/AI программа не заявлена.',
        'High season июль/август без явно указанного года; mid-season прямо апрель–сентябрь 2026. Даты/места/цена 2027 не опубликованы. Kids’ Club Пн–Пт 09:30–12:30 и 14–17, среда high season 09:30–16.',
        dict(year=2026,label='Публично от EUR 5 285 / неделю за семью из четырёх в high season; от 3 493 mid-season 2026; год high-season тарифа не указан. Не цена за каждого ребёнка и не подтверждённый прайс 2027.',
             included='High-season пакет: семейное жильё, half board, Kids’ Club, snacks, одна babysitting evening, домашняя уборка Пн–Пт и одна выбранная off-site activity ребёнку.',
             extras='Остальные приёмы пищи и дополнительные off-site активности отдельно. Self catering от EUR 235/ночь, минимум 4 ночи, включает только утренний club; afternoon/meals/babysitting отдельно. Налоги, сезонный полный quote и отмена неизвестны.',
             deposit='Размер/возврат залога и договор не установлены на прочитанных страницах; booking engine не использовали.'),
        'Семейный курорт с дневной детской программой, не отдельный детский пансион. Зимняя работа Kids’ Club не доказана.',
        fit('conditional','До 12 лет подходит по общему возрасту; EN support и выбранный сезон подтвердить.'),fit('conditional','До 12 лет подходит; программа совместного отдыха с родителями, не зачисление в самостоятельный пансион.'),
        [src('Kids’ Club: EN/bilingual команда, возраст, часы и занятия',MAS+'family-holidays-kids-club-babysitting-south-france/'),src('Состав high/mid/self-catering пакетов и цены',MAS+'prices-and-services/'),src('Родительские опции и babysitting',MAS+'relaxing-holidays-for-parents-in-south-france/')],
        confirmed=['EN'],role='camp_life_support')
    ap=dict(year=2026,label='Архив 2026: общая таблица EUR 385/452 за fortnight (09–14:30/16:30), 731/859 за две, 1060/1248 за три; полный сезон 1175/1376. Применимость к конкретной Technology/Mini Science отдельно, 2027 не объявлен.',
            included='Обед; длинный день также snack. Care 07:30–09 и 16:30–17 включён по общей таблице.',
            extras='Bus routes по Castellón без опубликованной здесь цены. Скидки не суммируются; early/student скидки прямо исключают Technology Campus. EUR 180/221 относится только к 22/23/25/26 июня, не универсальной неделе.',
            deposit='EUR 100 невозвратный reservation payment; остаток до начала. Не установлено, аванс это в составе tuition или добавочный fee: итог не увеличен автоматически. Разрешены три instalments; полный cancellation contract не прочитан.')
    af=fit('conditional','Архивная группа по рождению включает ребёнка; 2027 возрастные группы, дата и приём внешних детей ещё нужны.')
    an=fit('not_eligible','Годы рождения опубликованной группы исключают ребёнка; общий возраст всей сети не заменяет конкретный brochure cutoff.')
    for i,name,age,prog,mf,of,label in [
        (6,'Agora Lledó · Super Summer','Web 6–12, но brochure 2026: рождение 2014–2019; Оскар2020 не входит.','Семь общих тем: динозавры, океан, международное приключение, ecology, talent show, CSI и sport. Английский, swimming и creative activities.',af,an,'Архив 22 июня–7 августа 2026; новый 2027 не объявлен.'),
        (7,'Agora Lledó · Mini Science','Brochure 2026: рождение 2017/2018/2019/2020; младший science, не общий Tech3–14.','Знакомство с наукой и инженерией через практические опыты; каждый день новая тема. Подробный ежедневный syllabus не опубликован.',af,af,'Архив: Mini Science пишет 22–27 июня 2026, общая таблица оплачивает 22/23/25/26. Границу/выходные не исправляем предположением; 2027 ещё не объявлен.'),
        (8,'Agora Lledó · младшая Technology','Brochure 2026: рождение 2020–2022; не группа 2014–2019.','LEGO Education, первые задания конструирования и роботов. Более сложная программная/3D/VR часть страницы относится к старшей группе.',an,af,'Архив 30 июня–10 июля 2026. Новый набор 2027 и новые годы рождения пока не опубликованы.'),
        (9,'Agora Lledó · Technology','Brochure 2026: рождение 2014–2019. Web общий диапазон3–14 не отменяет отдельную младшую группу.','Роботы, программирование, drawing on computer, создание игр, 3D printing, AR/VR и эксперименты по STEAM; платформы/часы каждого модуля и оборудование в собственность не установлены.',af,an,'Архив 30 июня–10 июля 2026. Новый 2027 не объявлен.')]:
        emit(i,name,'ESP','Camino Caminàs 175, Castellón de la Plana', 'general,languages,sport' if i==6 else 'science,general' if i==7 else 'robotics,coding,technology', 'day',age,
             'Конкретная программа brochure прямо 100% English; это относится к названному потоку, а не выводится из языка сайта.',prog,label,dict(ap),
             'Дневная программа с обедом, без пансиона. Swimming только в длинном 09–16:30 Technology варианте.',mf,of,
             [src('Программы, внешний приём и общие диапазоны',AGORA+'en/school-life/summer-camp'),src('Первичный brochure2026: группы, английский, содержание, таблица fees',BROCHURE)],
             status='archive_next_unannounced',confirmed=['EN'],role='technical_instruction' if i>=8 else 'general_instruction')
    rp=dict(year=2026,label='Архив $450 / недельный day camp; $360 для опубликованных четырёхдневных недель. Валюта/налог итогового счёта отдельно; это не прайс 2027.',
            included='Дневные занятия. Hot lunch описан в overview, но далее указан lunch option: включение и цена требуют quote.',
            extras='Before care $30, after care $30, вместе $50 за неделю по overview. Два nut-free snack и вода свои. Late pickup после17:30 $25. Транспорт и жильё семьи отдельно; техника выдаётся для занятий, переход в собственность не доказан.',
            deposit='Day refund: >4 недели до старта удерживают10%, за2–4 недели50%, менее2 недель возврата нет. Отсутствия/неиспользованные meals не возвращают. Это правила day, не boarding.')
    rm=fit('conditional','Матвей в 2027 будет9–10; год/группа/верхняя возрастная граница и технический EN ещё подтвердить. Архив2026 не даёт места2027.')
    ro=fit('conditional','Младшая ступень7+ только после7-летия Оскара. Пока6 — отдельный Junior Science, не Dot/Dash или SPIKE7–10.')
    rn=fit('not_eligible','Ребёнок старше Junior4–7, нужен другой поток.')
    for i,name,age,programme,mf,of,url in [
        (10,'Ridley College · Junior Science','4–7','Научный метод через игровые эксперименты и наблюдение; не обещаны программирование роботов или AI.',rn,fit('conditional','Оскар6–7 предварительно младшей группы; exact cutoff на будущий сезон отдельно.'),DAY+'junior-camps-ages-4-to-7-'),
        (11,'Ridley College · Dot & Dash','7–10','Программирование Dot/Dash: движение, свет, задания, решение задач, коммуникация и командная работа. Курс вводный; для опытного Матвея проверить уровень.',rm,ro,DAY+'intermediate-camps-ages-7-to-10-'),
        (12,'Ridley College · SPIKE Prime · intermediate','7–10','LEGO SPIKE Prime: конструирование с моторами/датчиками, код, challenges и внутренние robot games. Последние не международная награда.',rm,ro,DAY+'intermediate-camps-ages-7-to-10-'),
        (13,'Ridley College · SPIKE Prime · senior','10–13','Более сложный SPIKE Prime: управление роботами, engineering, препятствия, новые missions и внутренние robot games. Конкретный часовой syllabus и соревновательный уровень требуют подтверждения.',fit('conditional','Матвею только после10-летия; уровень и новые даты отдельно.'),fit('later','Оскар пока младше10, младший курс не снимает senior minimum.'),DAY+'senior-camps-ages-10-to-13-')]:
        emit(i,name,'CAN','2 Ridley Road, St. Catharines, Ontario','science,general' if i==10 else 'robotics,coding','day',age,
             'Прочитанные страницы EN не содержат однозначной гарантии английского именно camp/robotics instruction. EN школы и язык сайта не выданы за такую гарантию.',programme,
             'Прочитаны конкретные летние недели2026; все уже прошли. У SPIKE intermediate только короткие недели29.06–03.07 и04–07.08 с исключёнными праздниками. Набор2027 не объявлен.',dict(rp),
             'Дневной camp09–15:30, drop/pickup08:30–16; parents не допускаются в campus buildings по опубликованным правилам. Жильё семьи отдельно.',mf,of,
             [src('Конкретный syllabus, возраст, недели и цена2026',url),src('Общие часы, holidays, meals/care и day refund',DAY+'summer-day-camps-overview')],status='archive_next_unannounced')
    emit(14,'Ridley College · Day Camp Boarding','CAN','2 Ridley Road, St. Catharines, Ontario','general,robotics,coding,sport,art','boarding','Конкретный Day Camp Boarding10–16; общий header10–17 и отдельный ESL12–17 не расширяют этот поток.',
         'Международный приём прямо указан. Но EN технических выбранных дневных занятий ещё требуется подтвердить.',
         'Днём выбирают доступный поток вместе с местными детьми; вечером/на выходных культурные trips, Niagara/Toronto/Canada’s Wonderland. Robotics option не означает непрерывную техническую смену. CustomSTEM+ESL для группы минимум10 — отдельный продукт, не индивидуальная заявка братьев.',
         'Архив2026:28.06–11.07,12–25.07,26.07–08.08,09–22.08; четырёхнедельные варианты. Новые2027 dates/fees ещё не объявлены.',
         dict(year=2026,label='Архив $3 995 / две недели или $7 695 / четыре; tax included по конкретному Day Camp Boarding. Валюту подтвердить; не новый прайс2027.',
              included='Sharedboarding accommodation, три meals и snacks, доступные day programmes, evening/weekend excursions и24-hourstaffcare по странице.',
              extras='Airport transfer/medical insurance и отдельные camp upgrades не перечислены здесь как включённые. Внешний международный приём не подтверждает персональное зачисление.',
              deposit='Только архив boarding2026: до01.05 удерживают10%,01.05–01.06 —50%, после01.06 возврата нет. Visa-refund имеет собственные сроки подачи/уведомления2026, не перенесён на2027. Day cancellation4/2недели к boarding не применяется.'),
         'Детский пансион со sharedrooms и supervisedlife, родители отдельно.',
         fit('conditional','Матвею только после10-летия; camp track и новый сезон отдельно.'),fit('later','Оскар пока младше boarding10+.'),
         [src('Прямой international admission, жильё, пакет и отдельные правила boarding2026',RIDLEY+'summer-boarding')],status='archive_next_unannounced')

def extend_report_v130(r):
    r['version']=130;r['asof']=CHECKED
    r['shortlist'] += [dict(label='Франция · младший языковой пансион и семейный отдых',slugs=NEW[:6],reason='Enjoy 6–10 билингвальный: осень EUR 820 TTC, даты и цена 2027 расходятся. Best of LBS 3–6 лет: 23–27 августа 2027, EUR 300 только Оскару до 7-летия. Mas de Thau — совместный отдых с родителями и английской поддержкой; робототехника не заявлена.'),
        dict(label='Испания · английская программа и группы по рождению',slugs=NEW[6:10],reason='Брошюра Agora Lledó 2026 прямо подтверждает английский технических занятий. Mini Science и две группы Technology разделены. Общий диапазон сайта 3–14 не заменяет конкретные годы рождения; новые условия 2027 ещё нужны.'),
        dict(label='Канада · школьная инженерия и будущий пансион',slugs=NEW[10:],reason='Ridley: Science 4–7, Dot/Dash 7–10, SPIKE 7–10 и 10–13; пансион 10–16 с международным приёмом. Пока архив 2026; английский робототехники не подтверждён языком сайта. У дневного лагеря и пансиона разные правила отмены.')]
    gaps=[('FRA','Enjoy · зимние/весенние даты и цена',ENJOY+'prochains-sejours','Зима: 1–6 марта против February в заголовке и формах. Апрель: 19–24 Пн–Сб против Вс–Пт, EUR 750 против общего EUR 820 TTC. Точные сессии 2027 и ICS до исправления не создаются.'),
        ('FRA','Enjoy · приём детей без французского и возврат',ENJOY+'faq','Младшие FR/EN; полностью EN только 11–17. Педагогический проект после регистрации. Иностранный приём, отмена и страхование ещё не доказаны; VACAF/Pass Colo семье автоматически не назначены.'),
        ('FRA','Mas de Thau · семейный договор 2027',MAS+'prices-and-services/','Год high-season прайса не указан; mid-season прямо 2026. Half board и self catering — разные пакеты. Цена семье из четырёх; налоги, договор, даты 2027 и английский всех активностей ещё нужны.'),
        ('ESP','Agora Lledó · новые группы и полный технический тариф',BROCHURE,'Архив 2026: Super 2014–19 исключает Оскара2020; младшая Technology 2020–22, старшая 2014–19. Общая таблица EUR 385/452 за две недели не подтверждает цену Technology. Ранние/школьные скидки исключают Technology. Mini Science 22–27 июня против четырёх дней в прайсе; новый сезон отдельно.'),
        ('CAN','Ridley · следующий набор, язык и цена',DAY+'summer-day-camps-overview','Архив 2026: новые даты, возрастные группы и счёт 2027, технический английский и включение обеда ещё нужны. Дневная отмена по 4/2 неделям отличается от календарных сроков пансиона2026.'),
        ('CAN','Concordia · public source retrieval', 'https://www.concordia.ca/camps/science-engineering.html','Две обычные прямыеHTTP попытки к science/generalpages остановлены certificate validation. ENcamp-language/новыйseason не подтверждены; досье и календарь не добавлены. TLSverification не отключалось.')]
    names={'FRA':'Франция','ESP':'Испания','CAN':'Канада'}
    r['gaps'] += [dict(iso=iso,country=names[iso],provider='v130 · '+title,url=url,detail=detail,next_action='Продолжить первичную проверку новых наборов и всех приоритетных стран; ни одна страна не признана полностью изученной.') for iso,title,url,detail in gaps]
    additions=[
        ('camp-suisse-board','general,boarding','Сравнить общий английский пансион после 7-летия Оскара.','CHF 4 400 за две недели включает пансион, трансферы и оборудование. Условия2018 не являются новым договором2027; Оскар в6 лет младше минимума.'),
        ('camp-suisse-day','general','Обоим дневная английская альпийская программа с отдельным жильём семьи.','Дневной лагерь 5+ отличается от пансиона 7+. Пансионные тариф, страхование и трансфер на дневной формат не переносятся.'),
        ('chantemerle-junior-board','general,boarding','Младший пансион 6–11 и языковые занятия обоим.','Английские уроки подтверждены; язык лагерной жизни и техники отдельно. Летнее окно2027 не непрерывная35-дневная смена. Медстраховка CHF8/день и регистрационный платёж в окончательном счёте.'),
        ('helvetic-zug-summer','technical','Швейцарская дневная робототехника 4–12 с опубликованными неделями2027.','EN/DE и группа выбранного класса отдельно; семейное жильё вне тарифа. В подробной карточке12–16 июля, в обзоре13–16: расхождение уже отмечено.'),
        (NEW[0],'general,boarding','Короткий младший французский пансион обоим осенью.','6–10 билингвальный FR/EN; полностью английская политика относится к11–17. Базовый пакет EUR1640TTC на двоих; дорога, возврат и места отдельно.'),
        (NEW[3],'general','Короткий английский курс науки и творчества Оскару в Париже.','3–6 только до7-летия;23–27 августа2027, EUR300 за12,5часа. Матвей старше; полный день и жильё не обещаны.'),
        (NEW[5],'general','Семейное жильё и детский клуб с английской поддержкой во Франции.','Родители с детьми; общий курорт, английский всех модулей не установлен. Прайс и лето2027 ещё не подтверждены.'),
        (NEW[7],'general,technical','Сравнить английскую младшую науку в Испании.','Брошюра2026 включает рождение2017–2020; группы, даты и цена2027 ещё нужны. Короткая июньская неделя указана неоднозначно.'),
        (NEW[11],'technical','Канадская вводная робототехника, для Оскара после7-летия.','7–10, Dot/Dash и архив2026. Технический английский и набор2027 ещё нужны; опытному Матвею уровень может быть простым.')]
    profiles={p['slug']:p for p in r['profiles']}
    review=r['family_review'];existing={q['slug'] for q in review['entries']}
    review['entries'] += [dict(slug=s,goals=g.split(','),reason=why,key_limit=limit,dossier_checked=profiles[s]['checked']) for s,g,why,limit in additions if s not in existing]
    review.update(version=130,asof=CHECKED)
    review['coverage']=dict(candidates=len(review['entries']),countries=len({profiles[q['slug']]['iso'] for q in review['entries']}),fully_audited_countries=0)
    r['counts']=dict(dossiers=len(r['profiles']),countries=len({p['iso'] for p in r['profiles']}),swiss=sum(p['iso']=='CHE' for p in r['profiles']),by_status=dict(Counter(p['timing']['status'] for p in r['profiles'])),source_urls=len({s['url'] for p in r['profiles'] for s in p['sources']}))
    from camp_europe_v127 import readable
    # Later passes append profiles before report extensions run. Normalise the
    # profiles owned by this pass, not whichever dossiers happen to be last.
    r['profiles']=[readable(p) if p['slug'] in NEW else p for p in r['profiles']]
    r['shortlist'][-3:]=readable(r['shortlist'][-3:]);r['gaps'][-6:]=readable(r['gaps'][-6:]);r['family_review']=readable(review)

def extend_planning_v130(d):
    m=d['camp_planning'];m['offers']=[q for q in m['offers'] if q['id'] not in NEW_OFFERS]
    m['offers'] += [offer(NEW_OFFERS[0],NEW[0],'Enjoy · оба ·19–24 октября2026',820,currency='EUR',price_year=2026,format='boarding',checked=CHECKED,
        sessions=[['2026-10-19','2026-10-24']],sources=[ENJOY+'19-24-octobre-2026',ENJOY+'tarif',ENJOY+'faq'],
        included='Базовый пансион, питание, языковые занятия и активности: EUR 1 640 TTC на двоих.',
        gate='Младшая группа6–10 FR/EN; приём свободно говорящих на EN без FR, верхняя граница Матвея и места отдельно. Это осень2026, не прайс2027.',
        unknown_required=['Navette к Bernay, если требуется: цена/включение не установлены.','Действующие страховка, отмена, договор и итоговый счёт ещё нужны.'],
        deposit_note='50% / EUR410 каждому — аванс в составе820, не прибавлен повторно. VACAF/Pass Colo и скидка брату не применены.'),
      offer(NEW_OFFERS[1],NEW[3],'Best of LBS · толькоОскар ·23–27 августа2027',300,currency='EUR',children=['oscar'],base_by_child=dict(oscar=300),format='day',checked=CHECKED,
        sessions=[['2027-08-23','2027-08-27']],sources=[LBS+'the-best-of-little-british-2027/'],
        included='Пять английских полудней по2,5часа в выбранной школе.',gate='Только пока Оскару6; после7-летия не подходит. Матвей исключён. Место и приём отдельно.',
        unknown_required=['Договор, отмена, питание/уход вне2,5часа и окончательный счёт ещё нужны.'],
        deposit_note='EUR300 за12,5часа, не полный день. Семейное жильё и дорога добавляются отдельно.')]
    from camp_europe_v127 import readable
    m['offers'][-2:]=readable(m['offers'][-2:]);m.update(version=130,asof=CHECKED)
