"""Selected English holiday weeks, Spain curricula and French residential learning."""
from collections import Counter
from pathlib import Path
from camp_planning_v108 import offer

ROOT=Path(__file__).resolve().parents[1]
BASE='7c537ae25a4d7c212b958f08436ac6762eb06896'
CHECKED='2026-10-06'
KIDS='https://www.kidsandus.fr/fr/ecoles-anglais-enfants/'
BAR='https://www.kidsandus.es/es/academias-ingles/kidsus-eixample-dreta/halloween-fun-weeks-ya-estan-aqui'
PARIS5=KIDS+'kidsus-paris-5/stages-toussaint-2026'
PARIS11='https://kidsandus.fr/fr/ecoles-anglais-enfants/kidsus-paris-11/halloween-fun-weeks-sont-retour'
ANGERS=KIDS+'kidsus-angers-centre/halloween-funweeks-2026'
RUEIL=KIDS+'kidsus-rueil-malmaison/stage-vacances-toussaint-0'
CODE='https://codelearn.es/'
SILC='https://silc.fr/'
NORM=SILC+'sejours-linguistiques/destinations/france/immersion-anglaise-en-normandie/'
ONE=SILC+'sejours-linguistiques/destinations/france/one-to-one-10-cours-par-semaine-france/'
TERMS=SILC+'conditions-particulieres-de-vente/'
TOLEDO='https://www.colegiosanpatriciotoledo.com/en/summer-camps'
PDFROOT='https://d24d7vsshzrslo.cloudfront.net/sites/school6/files/2025-12/1211565312853162_-_summer_camps_2026_phase_1_timetable_san_patricio_toledo_'
COOLEST='https://coolestprojectsspain.org/'
EVENT_ID='E190'
NEW=['kidsus-barcelona-autumn','kidsus-paris5-autumn','kidsus-paris11-autumn','kidsus-angers-autumn','kidsus-rueil-english','kidsus-rueil-english-art',
     'codelearn-sixseven','codelearn-roboball','codelearn-godot','silc-normandy-english','silc-one-to-one-france',
     'sanpatricio-mega-day','sanpatricio-robotics-day','sanpatricio-robotics-board']
ASK='Подтвердить конкретное место, возраст на начало, приём приезжей семьи, выбранный языковой поток и полный счёт/отмену. Заявки, сообщения и оплаты не выполнялись.'
SILC_CANCEL='Прочитаны детские CPV 2026, не договор 2027: €600 аванс, включая €100 dossier; эти €100 невозвратны при обычном отказе. Удержания >60 дней 10%, 60–31 день 30%, 30–16 дней 50%, 15–8 дней 75%, менее 8 дней 100%, с исключёнными из базы fees/insurance. Страница курса пишет цену без dossier, CPV — с dossier: итоговое включение €100 расходится. Не складывать автоматически €1150 + €100 как окончательный счёт. Optional cancellation insurance 3,75% с отдельными основаниями; не автоматический полный возврат.'

def add_europe_v133(add,src,fit,profiles):
    def emit(i,name,iso,place,themes,formats,age,lang,programme,dates,price,housing,mf,of,sources,status='next_unannounced',confirmed=None,role=None,variants=None):
        add(NEW[i],name,{'FRA':'Франция','ESP':'Испания'}[iso],iso,place,themes,formats,age,lang,programme,dates,price,housing,mf,of,
            'Редакционный кандидат по собственной программе и условиям. Включение в атлас не является мировым рейтингом или подтверждением зачисления.',[ASK],sources,
            status=status,confirmed=confirmed,sessions=[[v['start'],v['end']] for v in variants] if variants else [])
        p=profiles[-1];p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
        if role:p['language_evidence_role']=role
        if variants:
            for v in variants:
                v.setdefault('place',place)
                v.setdefault('source',p['sources'][0]['url'])
            p['timing']['session_details']=variants
            if len({(v['start'],v['end']) for v in variants})<len(variants):p['timing']['variant_keyed']=True
        return p
    def variant(start,end,key,label,age='3–10',mf=None,of=None,price='Прайс не опубликован.',housing='Дневной лагерь; семейное жильё отдельно.'):
        v=dict(start=start,end=end,variant_key=key,label=label,age=age,price=price,accommodation=housing,date_scope='day_camp_window')
        if mf is not None:v['family_fit']=dict(matvey=dict(status=mf[0],detail=mf[1]),oscar=dict(status=of[0],detail=of[1]))
        return v
    both=fit('conditional','В октябре 2026 возраст 8–9 / 5–6 входит в эту общую группу; индивидуальное место, выбранный формат и приём приезжих отдельно.')
    unknown=dict(year=2026,label='Прайс конкретного центра/смены не опубликован.',included='Тематические английские игры и занятия; включение питания/материалов в неизвестную оплату отдельно.',extras='Транспорт, питание, дополнительные часы присмотра и жильё семьи отдельно уточнить.',deposit='Аванс, договор и возврат неизвестны; booking forms не использовались.')
    en='Прямо опубликовано 100% English для этих FunWeeks; общий языковой лагерь, не робототехническая или AI программа.'
    emit(0,'Kids&Us Eixample Dreta · Halloween FunWeek','ESP','Barcelona · Eixample Dreta','general,languages,art','day','3–10',en,
        'Storytime, театральные игры, песни, творчество и Halloween. Группы до 10 на преподавателя; принимают учеников сети и детей извне.',
        '26–30 октября 2026. Точные часы этого центра неизвестны; общие сетевые 09–13 не перенесены как обещание. Зима/лето 2027 ещё не объявлены.',dict(unknown),
        'Дневной формат; пансион не заявлен.',both,both,[src('Собственное объявление 28.09.2026: даты, 3–10, 100% EN',BAR),src('Общий формат FunWeeks и сезонность, не часы Barcelona','https://www.kidsandus.es/es/actividades-ingles-ni%C3%B1os/campamentos/tematicos')],
        status='published_2026',confirmed=['EN'],variants=[variant('2026-10-26','2026-10-30','barcelona','Halloween · часы уточнить')])
    emit(1,'Kids&Us Paris 5 · Toussaint FunWeeks','FRA','Paris 5 · конкретный кабинет уточнить','general,languages,art','day','3–10',en,
        'Творческие темы Magic/Halloween; группы 3–4, 5–6, 7–10 по 8–10 детей. Есть утро, после обеда и полный день; цены/точные часы находятся в неполученной брошюре, не придуманы.',
        '19–23 и 26–30 октября 2026; конкретные часы и формат внутри недели уточнить.',dict(unknown),'Дневной формат, не пансион.',both,both,[src('Собственное объявление 30.09.2026: две недели и EN',PARIS5)],
        status='published_2026',confirmed=['EN'],variants=[variant('2026-10-19','2026-10-23','paris5-one','Toussaint · формат/часы уточнить'),variant('2026-10-26','2026-10-30','paris5-two','Halloween · формат/часы уточнить')])
    full8=fit('conditional','Полный день только 5–8. Матвей 2017 в октябре 2026 имеет 8–9: подходит только до девятого дня рождения; утренний 3–10 шире.')
    fullosc=fit('conditional','В октябре 2026 имеет 5–6 и входит в 5–8; место/приём отдельно.')
    emit(2,'Kids&Us Paris 11 · утро и полный день с разным возрастом','FRA','Paris 11 · Kids&Us','general,languages,art','day','Утро 3–10; после обеда/полный день 5–8',en,
        'Secret Agents первая неделя, Swamp Life вторая; English games, stories, songs и творчество. Неученики принимаются; максимум 10 в группе. На второй неделе опубликовано только утро.',
        '19–23 октября 2026: утро 09–12:30 (3–10), после обеда 13:30–16:30 и полный день 09–16:30 (5–8). 26–30 октября: только 09–12:30 (3–10).',dict(unknown),
        'Дневной лагерь. Полный день не означает пансион; питание не установлено.',both,both,[src('Объявление 25.09.2026: недели, часы и отдельные возрастные группы',PARIS11)],
        status='published_2026',confirmed=['EN'],variants=[
            variant('2026-10-19','2026-10-23','morning-one','Secret Agents · 09–12:30'),
            variant('2026-10-19','2026-10-23','full-one','Secret Agents · 09–16:30','5–8',full8,fullosc,housing='Полный дневной формат 09–16:30, только 5–8; питание/перерыв уточнить.'),
            variant('2026-10-26','2026-10-30','morning-two','Swamp Life · только 09–12:30')])
    full10=fit('conditional','В октябре 2026 входит в 5–10; для полного дня нужен собственный picnic и два перекуса, место/приём отдельно.')
    emit(3,'Kids&Us Angers · Centre и Nord · Halloween','FRA','Angers · Centre/Place Imbach и Nord/Terra Botanica','general,languages,art,nature','day','Утро 3–10; полный день Centre 5–10',en,
        'Тематические английские игры утром. В Centre первой недели творческие дни: парк, fresco, magic potions, treasure hunt, кулинария. Игровая science-тема не полноценная robotics/AI лаборатория.',
        'Centre 19–23 октября 2026: 09–12:30 или полный день с послеобеденным 14–16:30. Nord 26–30 октября: 09–12:30. Care 08:30–09 /12:30–13; для Centre послеобеденного формата до 17, цена care неизвестна.',
        dict(unknown,included='Английские тематические занятия, максимум 10 детей. Для полного дня собственные picnic и morning/afternoon snacks.',extras='Еда полного дня семьи; стоимость optional care и материалов не опубликована.'),
        'Два центра — разные площадки и недели; без пансиона.',both,both,[src('Объявление 16.09.2026: centres, часы, ages, picnic',ANGERS)],
        status='published_2026',confirmed=['EN'],variants=[
            variant('2026-10-19','2026-10-23','centre-morning','Centre/Imbach · 09–12:30'),
            variant('2026-10-19','2026-10-23','centre-full','Centre/Imbach · утро + 14–16:30','5–10',full10,full10,housing='Полный день Centre; свой picnic и два перекуса; начало/конец и care отдельно.'),
            variant('2026-10-26','2026-10-30','nord-morning','Nord/Terra Botanica · 09–12:30')])
    rprice=dict(year=2026,label='EUR 285 / ребёнок / неделю за утренний English 09–13; две опубликованные tuition дают EUR 570, не весь семейный отдых.',
        included='Пять утренних English FunWeek дней; полное включение meals/materials не установлено.',extras='Жильё родителей/детей, питание, транспорт, возможные fees отдельно; afternoon ART не входит в €285.',deposit='Аванс и возврат не опубликованы.')
    emit(4,'Kids&Us Rueil-Malmaison · утренний English','FRA','8 Passage Schneider, 92500 Rueil-Malmaison','general,languages,art','day','3–12',en,
        'Игровой English FunWeek 09–13, ученики и неученики, группы до 8. Эта карточка относится только к английскому утру, не к художественной второй половине дня.',
        '19–23 октября 2026, 09–13.',rprice,'Дневное утро; семейное жильё отдельно.',both,both,[src('Объявление 19.09.2026: часы, 3–12 и €285/€495/ART',RUEIL)],
        status='published_2026',confirmed=['EN'],variants=[variant('2026-10-19','2026-10-23','morning','English · 09–13','3–12',price='EUR 285 / ребёнок / неделю')])
    artlang='EN прямо подтверждён утром 09–13. Язык послеобеденного AMK’ART 14–17 не установлен: это English lessons + art, не подтверждённый полностью английский день.'
    emit(5,'Kids&Us Rueil-Malmaison + AMK’ART · полный смешанный день','FRA','8 Passage Schneider, 92500 Rueil-Malmaison','general,languages,art','day','3–12',artlang,
        'Утренний English FunWeek и послеобеденная живопись AMK’ART. Отдельный afternoon €215/week; combined €495/week. Материалы ART €30/week — единицу per child/group нужно согласовать.',
        '19–23 октября 2026, полный день 09–17; English 09–13, Art 14–17, lunch gap уточнить.',
        dict(year=2026,label='EUR 495 / ребёнок / неделю combined + ART materials EUR 30/week, единица начисления материалов не установлена. Не итоговая цена двух детей.',included='English утром и художественные занятия после обеда.',extras='Материалы, lunch supervision/еда, транспорт и жильё отдельно уточнить.',deposit='Аванс/возврат и язык ART неизвестны.'),
        'Дневной mixed programme без пансиона.',fit('conditional','Входит в 3–12, но язык ART/перерыва и индивидуальный приём ещё нужны.'),fit('conditional','Входит в 3–12, но язык ART/перерыва и индивидуальный приём ещё нужны.'),
        [src('Собственное объявление: combined price и разные части дня',RUEIL)],status='published_2026',confirmed=['EN'],role='language_lessons',
        variants=[variant('2026-10-19','2026-10-23','mixed','English + ART · 09–17','3–12',price='EUR 495 tuition + EUR 30/week ART materials, единицу уточнить')])
    cllang='Язык преподавания прямо не опубликован. Испанский текст сайта не подтверждает ES и не исключает каталонский; EN/ES поток конкретного центра отдельно.'
    cm=fit('conditional','Общая сеть camp 7–18 охватывает возраст Матвея, но минимум/уровень именно этого курса ещё неизвестен.')
    co=fit('conditional','Оскару сейчас 5–6, ниже сетевого 7. В 2027 — только после 7-летия и подтверждения минимума конкретного курса; название 6–7 не возраст.')
    cprice=dict(year=None,label='Тариф конкретного курса не опубликован.',included='Учебная программа описана; использование техники не обещает take-home kit.',extras='Жильё семьи, питание, материалы/оборудование и camp-specific fees уточнить.',deposit='Даты, договор/возврат и величина возможной sibling/student discount не установлены.')
    for i,name,path,programme,dates in [
        (6,'Codelearn · Campus 6–7 · игры и робототехника','cursos/campus-6-7-de-programacion-y-robotica/',
         'Создание игр, сборка/программирование робота и off-screen logic. Компьютеры, роботы и материалы предоставляются для работы; домашняя выдача не заявлена. Опыт не требуется. «6–7» — мем/название, не напечатанный возраст 6–7 лет.',
         'Курс без точных дат/года, возраста и fees. Общая сеть говорит 7–18, но это не минимум каждого track. Новые сессии 2026–2027 не создаются.'),
        (7,'Codelearn · Robobol · конструкция Futbots','cursos/campus-robobol/',
         'Построить механический/электронный Futbot, запрограммировать joystick control, испытать и сыграть мини-матч. Объявлен follow-on Robobol в феврале без года/rules/награды: это не установленная международная лига.',
         'Mataró: 22, 23, 24 декабря без явно указанного года; отдельный February tournament тоже без года. Точные календарные даты не выведены из сезона.'),
        (8,'Codelearn · Devcamp Godot · 2D/3D game creation','cursos/devcamp-videojuegos-con-godot/',
         'Godot, GDScript, nodes/scenes, variables/functions/conditions; 2D sprites, physics/collision; 3D axes/models/cameras/lighting, signals. GDScript похож на Python, но этот syllabus не является курсом Python. Возраст/предпосылки отдельно.',
         'Course syllabus опубликован, конкретный центр, dates/year/цена неизвестны. Нет придуманных смен 2027.')]:
        emit(i,name,'ESP','Испанские центры Codelearn · выбранный кампус уточнить','robotics,coding,games' if i!=8 else 'coding,games','day',
             'Общий campus 7–18; возраст конкретного курса неизвестен',cllang,programme,dates,dict(cprice),'Дневное обучение; пансион не заявлен.',cm,co,
             [src('Собственный syllabus, не подтверждённая смена',CODE+path),src('Общие кампусы 7–18, сезонность и centres',CODE+'campus-tecnologicos/')])
    future=fit('conditional','Матвею в июле 2027 9–10: группа 10+ только после десятого дня рождения; место/приём не подтверждены.')
    olater=fit('later','10+; Оскару 2020 в 2027 только 6–7, сейчас не подходит.')
    norm=emit(9,'SILC · English Immersion in Normandy · пансион','FRA','English Manor House · примерно 10 км от Avranches','general,languages,nature,sport','boarding','10–15',
        'Англоязычная команда и English activities 100% VO прямо описаны. Это immersion through activities; десять индивидуальных уроков относятся к другой One-to-One программе.',
        'Спорт, природа, кулинария/творчество и английские игры; 4 полудня на территории, одна full-day excursion Mont-Saint-Michel или Saint-Malo и evenings. Общий ratio 1:12, language activities 1:13–14.',
        'Выбранная собственная вариация: 18–23 июля 2027. Онлайн-покупка недоступна: is_in_stock=false; причина (нет мест/ещё не открыто) не установлена.',
        dict(year=2027,label='Вариация 18–23.07.2027 EUR 1 150 с Paris route. Текст без транспорта €855 и listing €995 не равны выбранной цене; включение dossier €100 расходится с CPV.',
             included='Пансион/full board, программа, местный транспорт и сопровождаемый поезд из Парижа у выбранной transport option.',extras='Доезд до Paris, dossier/insurance и полный quote отдельно. Не применять общие авиадоплаты к французскому поезду.',deposit=SILC_CANCEL),
        'Пансион: комнаты 4–8 с общими санузлами, полное питание, территория 30 га. Родительское проживание не включено.',future,olater,
        [src('Выбранная вариация 2027, availability, содержание/проживание',NORM),src('Детские CPV 2026: fee и cancel tiers, не договор 2027',TERMS)],
        status='published_2027',confirmed=['EN'],variants=[dict(start='2027-07-18',end='2027-07-23',variant_key='normandy',label='English immersion · 2027 · онлайн недоступно',
            price='EUR 1 150 transport variation; dossier conflict/полный quote отдельно',availability=dict(status='unconfirmed',label='Онлайн-покупка недоступна · причину уточнить'),date_scope='camp_session')])
    norm['programme_type']='general_residential_camp'
    norm['availability']=dict(status='unconfirmed',label='Онлайн-покупка недоступна · причину уточнить')
    emit(10,'SILC · One-to-One English во Франции · homestay','FRA','Англоязычные host families · преимущественно сельская Nouvelle-Aquitaine','general,languages','boarding','10–17; минимум English A1/A2',
        '10 индивидуальных English lessons по 55 минут в неделю и англоязычная host family. Это не общая FR-speaking colony и не Robotics camp.',
        'One-to-One уроки, 3 культурные half-day family activities/week и свободное время. Нужны мотивация/самостоятельность; ребёнок занимает себя в свободные часы. Один francophone/host family, возможен другой nationality student. Размещение двух братьев вместе не гарантировано.',
        'Year-round по запросу, 1–4 недели, arrival Sunday/departure Saturday. Доступные host families и конкретные 2026–2027 weeks не опубликованы: правило weekdays не стало точными сессиями.',
        dict(year=None,label='От EUR 1 130 / week без dossier на текущей странице; сезон/полный тариф 2027 не указан.',included='10×55 минут English/week, full board у семьи, 3 культурные полудня/week.',extras='Дорога и transfers отдельно; цена семьи/города/сезона и dossier требуют quote.',deposit=SILC_CANCEL),
        'Homestay с full board, не школьный boarding house и не постоянный 24/7 лагерный counsellor. Родители живут отдельно.',future,olater,
        [src('10–17, A1/A2, частные уроки и автономность homestay',ONE),src('CPV 2026 и конфликт dossier',TERMS)],confirmed=['EN'])
    toledotiming='Current title 2026/2027, но body dates без года, приложенные robotics/mega timetables прямо 2026. Main 28.06–11.07 /12–25.07, Mega 22.06–17.07: не подтверждённые сессии 2027. Следующий набор/price отдельно.'
    toledofees='В Prices per session: Main day €1180/2weeks, boarding €1925/2weeks; ниже day range €1180–1700 зависит от pathways. Это не binding robotics invoice. Hero/overview и нижняя таблица имеют расхождения. Договор refund/deposit и новый прайс 2027 ещё неизвестны.'
    mega=fit('conditional','Mega 6–9: возраст на выбранную неделю и группа отдельно. Матвей в 2027 после 10-летия выходит из Mega; Оскар подходит лишь после 6-летия.')
    emit(11,'San Patricio Toledo · Mega day · младшие 6–9','ESP','Juan de Vergara 1, La Legua, 45005 Toledo','general,languages,sport,art,robotics,engineering','day','Mega 6–9; Nano 3–5 отдельная группа',
        'Для Nano/Mega прямо English immersion; квалифицированные EN/ES-speaking staff. Школьная bilingual среда не обещает Robotics Main младшей группе.',
        'Спорт, swimming, arts и thematic weekly workshops. Приложенный Mega timetable (имя файла 2026) показывает Tuesday11–12 STEAM (VR/robotics/light/science) и Thursday11–12 engineering basics. Это короткие активности общего лагеря, не Main robotics/game-design10–16. Non-students welcome по FAQ, индивидуальный допуск отдельно.',
        toledotiming,
        dict(year=None,label='Fees Nano/Mega: 1 week €280; при 2/3/4weeks €275/270/265 за каждую неделю. Overview €265 half-day против Fees €265 multi-week — тариф half-day не подтверждён.',
             included='Учебные активности, staff, accident insurance; lunch/snacks заявлены общим Fees, конкретный half/full пакет отдельно.',extras='Транспорт и жильё семьи отдельно. Hours/питание half-day и применимый тариф требует quote.',deposit=toledofees),
        'Nano/Mega Day Camp Only. Приложенный Mega timetable: arrival08:45, programme09–16, lunch13–13:45; half-day hours и новый сезон отдельно. Общий FAQ09–19 не перенесён на Mega.',mega,mega,
        [src('Live Overview/Activities/Fees/FAQ: возраст, English, day only',TOLEDO),src('Ссылка текущего сайта на Mega timetable прямо 2026',PDFROOT+'mega_v2.pdf')],confirmed=['EN'])
    main=fit('conditional','Main 10–16: для Матвея 2017 летом 2027 только после 10-летия; readiness и языковый поток подтвердить.')
    tl='Robotics & Computing прямо в bilingual English/Spanish environment; FAQ выбор EN или ES. Это подтверждённая bilingual поддержка; расписание/состав конкретного потока отдельно.'
    tp='Robotics, sensors/microcontrollers, 3D modelling/printing, Godot и MakeCode Arcade; Aseprite/Piskel pixel art, собственная идея/story/coding/testing videogame. Уровень beginners допускается описанием; выдача robot/laptop домой не заявлена. Optional language или speciality sports после обеда.'
    for i,fmt in [(12,'day'),(13,'boarding')]:
        emit(i,'San Patricio Toledo · Robotics & Computing · '+('дневной' if fmt=='day' else 'пансион'),'ESP','Juan de Vergara 1, La Legua, 45005 Toledo',
             'robotics,coding,games,art','day' if fmt=='day' else 'boarding','Main 10–16',tl,tp,toledotiming,
             dict(year=None,label=('Main day table EUR 1 180 /2weeks; pathway range EUR 1 180–1 700, robotics-specific quote неизвестен.' if fmt=='day' else 'Main residential table EUR 1 925 /2weeks; robotics-specific invoice и новый сезон 2027 отдельно.'),
                  included='Staff/программа, accident/liability cover; meals и scheduled activities. Пансион дополнительно full board и laundry. Техника для занятий, не take-home комплект.',
                  extras='Madrid transfer return €380/oneway €200; standard window Sun arrival/Sat departure 08–16, вне окна higher private quote. Personal travel/health insurance и pocket money отдельно. Inclusion day excursions расходится между Fees и FAQ.',deposit=toledofees),
             ('Дневной Main: общий FAQ 09–19. Проживание семьи отдельно; формат младшего Mega этим временем не определяется.' if fmt=='day' else 'School boarding house, quadruple ensuite комнаты, 24/7staff, weekly laundry. Monitor 1:10 evening/excursions; teaching 1:12; language max15, не max16 из Overview. Комнаты распределяет оператор.'),
             main,olater,[src('Live Activities/Stay/Safety/Fees/FAQ: syllabus, EN/ES, rooms и insurance',TOLEDO),src('Ссылка сайта на Robotics Computing timetable прямо 2026',PDFROOT+'robotics_computing_v2.pdf')],confirmed=['EN','ES'],role='bilingual')

def extend_report_v133(r):
    r.update(version=133,asof=CHECKED)
    r['shortlist'] += [
        dict(label='Франция и Barcelona · ближайшие English FunWeeks',slugs=NEW[:6],reason='Октябрь 2026: general English, без robotics обещаний. Paris 11 full-day только 5–8; Rueil Art language неизвестен; центры/варианты считаются отдельно от числа операторов.'),
        dict(label='Испания · технические syllabus и будущий школьный robotics',slugs=NEW[6:9]+NEW[11:],reason='Codelearn без дат/языкового подтверждения; 6–7 название не возраст. San Patricio EN/ES Robotics 10–16 и Mega general 6–9; текущие PDF 2026, новый 2027 сезон ещё нужен.'),
        dict(label='Франция · English пансион и homestay с 10 лет',slugs=NEW[9:11],reason='Normandy вариация 18–23 июля 2027, онлайн-покупка недоступна. One-to-One host family требует autonomy/A1–A2. Оскар младше 10; Матвею после 10-летия.')]
    gaps=[('FRA','Kids&Us · fees, иностранный приём и язык Art',RUEIL,'Rueil EN утром подтверждён, Art after lunch язык неизвестен; €30/week materials единица ещё нужна. У Paris5/11 и Angers цены/возврат не опубликованы; non-student welcome не персональное принятие приезжих.'),
          ('FRA','Paris 11 · разные возрастные пределы',PARIS11,'Утро 3–10, полный день первой недели 5–8. Матвей 2017 подходит к полному дню только пока ему8; вторая неделя morning-only. Не переносить сетевой максимум10 на полный день.'),
          ('ESP','Kids&Us Barcelona · hours/price и 2027',BAR,'26–30Oct2026 опубликованы, но часы/price/refund нет. Общие сетевые часы и чужие centre fees не обещания для Barcelona. Next winter/summer2027 отдельно.'),
          ('ESP','Codelearn · age/language и Robobol year',CODE+'cursos/campus-6-7-de-programacion-y-robotica/','6–7 meme не age range. Сетевые7–18 не минимум каждого курса. December22–24 и February без year не точные смены/лига. ES web page не подтверждает преподавание; нельзя путать GDScript с Python.'),
          ('FRA','SILC · 2027 availability и детский договор',NORM,'July18–23 variation2027 есть, is_in_stock=false: причина неизвестна. Programme says excluding €100 dossier, CPV2026 says includes; refund tiers2026 не договор2027. Homestay не 24/7 colony.'),
          ('ESP','San Patricio · новый сезон и тариф/возраст',TOLEDO,'Title2026/27, current timetablePDF2026; no2027 exact rows. Main Robotics10–16 не Mega6–9; day range/half-day overview/multiweek fees/excursion inclusion расходятся. Нужны pathway invoice, refund и реальные места.'),
          ('ESP','Coolest Projects / Codeathlon · участник и семейный посетитель',COOLEST,'Own organizer24Oct2026Gavà12–18, free visitor/showcase; family stands11:30–13:30. Братья ниже12 для project submission, visitorусловиядлямладших отдельно. Jurymentions/diplomas/Pico kit и raffle не worldchampion title. Codeathlon platform points/clans не international school leaderboard.')]
    r['gaps'] += [dict(iso=iso,country={'FRA':'Франция','ESP':'Испания'}[iso],provider='v133 · '+title,url=url,detail=detail,next_action='Продолжить первичные programme/contract проверки всех мировых приоритетов; полностью изученных стран0.') for iso,title,url,detail in gaps]
    ps={p['slug']:p for p in r['profiles']};review=r['family_review']
    for slug,goals,reason,limit in [
        ('kidsus-barcelona-autumn',['general','languages'],'Barcelona 26–30 октября: общий English кандидат обоим.','Точные hours/fees/refund и приём приезжих ещё неизвестны; не robotics track.'),
        ('kidsus-paris5-autumn',['general','languages'],'Paris 5 две English недели октября для3–10.','Half/full-day hours и tuition не опубликованы; brochure form не отправлялась.'),
        ('kidsus-angers-autumn',['general','languages'],'Centre первая неделя даёт full day5–10, Nord следующая morning3–10.','Своя еда full day, цена/care/foreign intake отдельно; не technical intensive.'),
        ('kidsus-rueil-english',['general','languages'],'Точный утренний EN тариф €285/child/week и неделя19–23Oct.','Only09–13; полный ART день имеет непроверенный язык. €570 длядвух не полный отпуск.')]:
        assert not any(q['slug']==slug for q in review['entries'])
        review['entries'].append(dict(slug=slug,goals=goals,reason=reason,key_limit=limit,dossier_checked=CHECKED))
    review.update(version=133,asof=CHECKED)
    review['coverage']=dict(candidates=len(review['entries']),countries=len({ps[q['slug']]['iso'] for q in review['entries']}),fully_audited_countries=0)
    r['counts']=dict(dossiers=len(r['profiles']),countries=len({p['iso'] for p in r['profiles']}),swiss=sum(p['iso']=='CHE' for p in r['profiles']),by_status=dict(Counter(p['timing']['status'] for p in r['profiles'])),source_urls=len({s['url'] for p in r['profiles'] for s in p['sources']}))

def extend_planning_v133(d):
    planning=d['camp_planning'];ident='kidsus-rueil-english-both'
    q=offer(ident,'kidsus-rueil-english','Rueil-Malmaison · английское утро · 19–23 октября 2026',285,currency='EUR',price_year=2026,format='day',sessions=[['2026-10-19','2026-10-23']],sources=[RUEIL],checked=CHECKED,
        unknown_required=[dict(id='meals_total',label='Питание/другие обязательные доплаты обоих · включение и цену подтвердить',unit='amount',rate=1,min=0)],
        gate='3–12 включает возраст обоих в октябре 2026. Подтверждено английское утро 09–13. Индивидуальный приём приезжих и места неизвестны.',
        included='English FunWeek mornings: опубликованная стоимость занятий €285 × 2 = €570. Семейная скидка не подтверждена.',
        deposit_note='Аванс/отмена не опубликованы; никакая сумма не оплачена.',
        scope='Опубликованная стоимость занятий двух детей. Жильё, транспорт, питание и неизвестные обязательные доплаты требуют отдельного счёта.')
    planning['offers']=[o for o in planning['offers'] if o['id']!=ident]+[q];planning.update(version=133,asof=CHECKED)

def enrich_v133(d):
    gate='Посетитель с родителями: собственная страница разрешает семьям и посетителям осматривать стенды бесплатно. Отдельный допуск детей младше 12 и часы входа уточнить. Возраст участников проектов 12–18; братья в 2026 младше.'
    e=dict(id=EVENT_ID,block='События',title='Coolest Projects Spain 2026 · семейное посещение проектов',country='Испания',region='Европа',city='Gavà · La Casa Gran',
        start='2026-10-24',end='2026-10-24',period='09–14; публичные стенды проектов 11:30–13:30',date_status='Подтверждено',deadline='',
        age='Участники проектов 12–18; возраст посетителей рассматривается отдельно',mat=gate,osc=gate,format='Семейное посещение; проекты участников индивидуально или в команде',
        entry='Посещение бесплатно. Проекты участников 12–18 принимают до 8 октября 2026; за младших 13 заявку подаёт взрослый. Этот срок не относится к братьям-посетителям. Места и правила входа детей уточнить.',
        gear='Scratch, игры, сайты, приложения, hardware, продвинутый код и AI. Участники могут показать незаконченный проект. Посетителю робот не требуется.',
        language='Страница доступна на ES/CA; язык выступлений и мастерских, поддержка EN не установлены.',languages=[],language_mode='unconfirmed',language_certainty='Язык сайта не язык занятия или защиты.',
        cost='Подача проектов и посещение бесплатны по FAQ; дорога, жильё и питание отдельно.',level='C — местный показ проектов в международной сети',
        reward='Тематические упоминания жюри, дипломы участникам, Pico kit за участие и призы розыгрыша. Это признание проектов, не мировой турнирный титул. Посетитель не получает автоматически подарки и дипломы участников.',
        priority='P2 — семейное посещение после проверки входа',action='Подтвердить вход младших посетителей и окно стендов 11:30–13:30; возраст для заявки проекта начинается с 12 лет.',
        source=COOLEST,references=[dict(label='Объявление партнёра Codelearn',url=CODE+'blog/participa-coolest-projects-spain/')],
        proof='Прочитаны собственные FAQ, программа и критерии жюри; HTTP-снимок сохранён. Приём семьи и текущая вместимость не подтверждены.',checked=CHECKED,status='Идея',
        note='Carrer Major 37, 08850 Gavà. Защита перед жюри 5–8 минут: творчество, техническая сложность с учётом уровня, оформление и польза. Награды для участников проектов 12–18; это местный показ работ.',
        iso=['ESP'],themes=['robotics','ai','coding','games'],scope='local',importance_reason='Местный показ детских проектов в сети Coolest Projects и EU Code Week 2026. Не относится к крупным выставкам технологических компаний.',
        participation='visitor',admission_kind='visitor',evidence_level='event_page',event_type='youth_project_showcase',venue='La Casa Gran · Carrer Major 37, 08850 Gavà',
        exhibitor_deadline='2026-10-08',exhibitor_age='12–18',visitor_age_status='under12_admission_not_explicitly_confirmed')
    existing=[x for x in d['events'] if x['id']!=EVENT_ID]
    assert not any(x['source']==COOLEST and x['start']==e['start'] for x in existing)
    d['events']=existing+[e]
    guide=d['league_guide'];p=next(p for p in guide['profiles'] if p['id']=='coolest')
    if EVENT_ID not in p['event_ids']:p['event_ids'].append(EVENT_ID)
    category=dict(name='Spain 2026 · Gavà · показ проектов',age='12–18 для показа проекта; семьи и посетители отдельно',team='Индивидуально или команда; за младших 13 заявку подаёт взрослый',hardware='Scratch, games, web, apps, hardware, advanced code, AI',
        age_rule='Местный минимум 12 не изменяет возрастные правила Online и других стран.',event_id=EVENT_ID,entry='Проекты до 8 октября 2026; бесплатное посещение 24 октября; вход младших 12 уточнить.',language='Язык защиты не подтверждён',
        note='Упоминания жюри, дипломы, Pico kit и розыгрыш отличаются от мирового турнирного титула. Братья могут рассмотреть посещение; для проектов они младше минимума.',source=COOLEST,checked=CHECKED)
    p['categories']=[q for q in p['categories'] if q.get('event_id')!=EVENT_ID]+[category]
    nuance='v133 · Spain/Gavà 24 октября 2026: участники проектов 12–18, индивидуально или команда, бесплатно; срок 8 октября только для заявок проектов. Семьи посещают стенды 11:30–13:30; вход младших детей отдельно. Местные упоминания жюри не титул чемпиона мира.'
    if nuance not in p['nuances']:p['nuances'].append(nuance)
    if not any(q['url']==COOLEST for q in p['sources']):p['sources'].append(dict(title='Own Spain2026 FAQ/agenda/jury',url=COOLEST,checked=CHECKED))
    guide.update(version=133,checked=CHECKED)
    if not any(q['url']==COOLEST for q in d['sources']):d['sources'].append(dict(title='CoolestProjectsSpain2026 · ownFAQ/agenda',url=COOLEST,checked=CHECKED,evidence='Youthshowcasevisitor/presenterandjudgementdistinguished.'))
