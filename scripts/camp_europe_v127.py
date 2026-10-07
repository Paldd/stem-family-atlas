"""European junior holidays, English boarding and current versus archived prices."""
from pathlib import Path
import re
from camp_planning_v108 import offer
ROOT=Path(__file__).resolve().parents[1]
BASE='5b7d54972ba462ba7cf20dc84749f12743ae3f4d'
CHECKED='2026-10-06'
H='https://www.hoplaboum.fr/camp-de-jour-educatif-bilingue-grenoble'
HP='https://www.hoplaboum.fr/_files/ugd/a1f5ce_1e97094824074869bbab6277d9d5dc8b.pdf'
L='https://littlebritishschools.com/stages-de-vacances/'
V='https://campthevillage.com/'
VF=V+'en/frequently-asked-questions/'
VP=V+'media/com_vistas/documentos/dossier.pdf'
HI='https://hif.ch/camps/winter-camp-2027/'
FC='https://www.anglais-in-france.fr/'
FCP=FC+'tarifs/19-tarifs-stages-et-formations/76-colonies-de-vacances'
FCT=FC+'tarifs/20-reservation/84-cgv'
C='https://cienciayrobotica.es/actividad/campamento-tecnologico-de-verano-2023-liceo-sorolla'
CP='https://cienciayrobotica.es/wp-content/uploads/2026/05/FOLLETO-camp-2026.pdf'
NEW=['hopla-autumn','hopla-winter','hopla-spring','hopla-world','hopla-outdoors','hopla-art','hopla-games',
     'littlebritish-winter-fairy','littlebritish-winter-boost','littlebritish-spring-london','littlebritish-spring-boost',
     'village-kids','village-teens','hif-winter-2027','french-colo-summer','ciencia-sorolla-camp']
NEW_IDS=['hopla-world-both','littlebritish-winter-boost-matvey']
def readable(v):
    from camp_latam_v123 import readable as base_readable
    if isinstance(v,str):return re.sub(r'(?<=\d), (?=\d)',',',base_readable(v))
    if isinstance(v,list):return [readable(x) for x in v]
    if isinstance(v,dict):return {k:(x if k in ['url','source','status','date_precision','date_scope','start','end','admission_kind'] else readable(x)) for k,x in v.items()}
    return v
ASK='До записи подтвердить свободные места, точную возрастную группу, приём приезжей семьи и полный счёт. Заявки и оплаты не выполнялись.'
HREF='Полная оплата и заполненный dossier; смена открывается при минимум 6 детях, максимум 12 по holiday PDF. Отмена семьёй ≥15 дней: полный возврат; за 14–7 дней удерживают 50%; менее 7 дней/неявка — 100%, исключения по решению школы. Пропуски не возвращают; если школа отменяет из-за группы менее 6, полный возврат. Это правила Holiday Camp, не кружка по средам.'

def add_europe_v127(add,src,fit,profiles):
    names={'FRA':'Франция','ESP':'Испания','CHE':'Швейцария'}
    both=fit('conditional','Минимум 5 лет подходит обоим; верхнюю границу/группу и открытый приём ещё подтвердить. Английский предварительно не требуется, среда билингвальная FR/EN.')
    grade=fit('unknown','Требуется фактический класс CE1–CM2; год рождения не подтверждает эту школьную категорию.')
    osc_small=fit('conditional','Группа 3–6: Оскару в 2027 будет 6–7, подходит только до 7-летия на дату курса. Место и возрастной cutoff подтвердить.')
    mat_big=fit('not_eligible','Матвей старше максимума 6 этой группы; опыт не отменяет возрастную границу.')
    def emit(i,name,iso,place,themes,formats,age,language,programme,label,price,housing,mf,of,sources,
             status='next_unannounced',confirmed=None,role=None,sessions=None):
        add(NEW[i],name,names[iso],iso,place,themes,formats,age,language,programme,label,price,housing,mf,of,
            'Редакционный кандидат по собственному syllabus и условиям, с отдельным возрастным и языковым допуском. Независимый мировой рейтинг качества не установлен.',
            [ASK],sources,status=status,confirmed=confirmed,sessions=sessions)
        p=profiles[-1];p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
        if role:p['language_evidence_role']=role
        return p
    def dated(p,url,scope='day_camp_window'):
        p['timing']['session_details']=[dict(start=a,end=b,label='Опубликованная смена',place=p['place'],source=url,
            price=p['price']['label'],date_scope=scope,date_precision='published_session',proof='Даты прямо опубликованы оператором; наличие места и персональный допуск отдельно.') for a,b in p['timing']['sessions']]
    # Seven seasonal curricula of one bilingual school; not seven unrelated camp operators.
    hopla=[
      ('2026-10-19','2026-10-23','Autumn · colours and tastes','general,art,science','Цвета, вкусы, приготовление еды, творческие опыты, физические и кооперативные игры; финальный Grand Banquet. Предварительного английского не требуют.'),
      ('2027-02-15','2027-02-19','Winter Holiday Camp','general,languages','В PDF опубликована зимняя смена. Общий проект включает искусство, сенсорные/научные опыты, кулинарию, спорт и сотрудничество; конкретная зимняя тема и ежедневный syllabus пока не названы.'),
      ('2027-04-12','2027-04-16','Spring Holiday Camp','general,languages','Точная весенняя смена указана в PDF. Билингвальное практическое обучение; собственный весенний тематический план ещё нужен. Робототехника не заявлена.'),
      ('2027-07-05','2027-07-09','Trip Around the World','general,art,languages','Культуры, искусство и кулинария разных стран, создание проектов и общение на FR/EN. Общая международная тема, не зарубежная поездка детей.'),
      ('2027-07-12','2027-07-16','Outdoor Week','nature,science,general','Природа, сад и научные наблюдения; планируется посещение Arboretum Robert Ruffier-Lanche при UGA. 14 июля выходной: занятия только 12, 13, 15, 16 июля; не пять дней.'),
      ('2027-07-19','2027-07-23','Art in all its Forms','art,music,general','Музыка, танец, театр, изобразительное искусство и планируемое музейное посещение; проекты и общение в FR/EN.'),
      ('2027-08-23','2027-08-27','All About Games','games,general,languages','Настольные, традиционные, кооперативные и подвижные игры; стратегии, логика, создание правил. Это не заявленный курс разработки видеоигр.')]
    for i,(a,b,title,themes,programme) in enumerate(hopla):
        price=dict(year=2026 if i==0 else 2027,label='EUR 290 за ребёнка / полную пятидневную неделю; для двоих EUR 580. Наличие места и итоговый счёт отдельно.',
            included='Дневные занятия 09–16:30, билингвальная команда и материалы по программе.',
            extras='Обед и оба перекуса приносит семья. Care 08:30–09 и 16:30–18: EUR 2,50 за полчаса. Полные 2 часа care × 5 дней × 2 ребёнка = EUR 100, расчёт по тарифу; жильё и дорога отдельно.',deposit=HREF)
        if i==4:
            price['label']='Тариф EUR 290 относится к пятидневной неделе. Для четырёх дней 12–16 июля отдельная цена не опубликована; пропорциональный скидочный расчёт не сделан.'
            price['extras']='14 июля школа не работает; тариф care EUR 2,50/полчаса известен, цена выбранной четырёхдневной смены требует счёта. Lunchbox, жильё и дорога семьи отдельно.'
        p=emit(i,'HoplaBoum · '+title,'FRA','École Internationale HoplaBoum · 3 rue de la Condamine, Gières / Grenoble',themes,'day',
            'Полный день с 5 лет; верхняя граница holiday-группы не названа. PDF также содержит отдельные утренние группы 3–4.',
            'Holiday PDF прямо устанавливает билингвальную французско-английскую среду и команду, без требований к предварительному английскому. Это не английский как единственный язык всех занятий.',
            programme,a+' – '+b+'; 09–16:30, пансиона нет.',price,'Дневной лагерь; питание приносит семья, родители организуют отдельное жильё.',both,both,
            [src('Темы лета, осень и выходной 14 июля',H),src('Holiday PDF: даты, язык, группа, цена и отмена',HP)],
            status='published_2026' if i==0 else 'published_2027',confirmed=['EN'],role='bilingual',sessions=[[a,b]])
        dated(p,HP)
        if i==4:
            v=p['timing']['session_details'][0];v['date_scope']='session_days'
            v['sessions']=[dict(date='2027-07-'+d,start_time='09:00',end_time='16:30',timezone='Europe/Paris',ical_timed=True,topic='Outdoor Week · занятия; 14 июля выходной') for d in ['12','13','15','16']]
    # Five explicit venue schedules, with identical dates, represented by keyed variants.
    locations=['Paris 6','Paris 7','Paris 16','Paris 17','Meudon']
    for i,path,title,age,a,b,programme,mf,of in [
      (7,'winter/fantastic-fairytales/','Winter · Fantastic Fairytales','3–6','2027-02-08','2027-02-12','Английские сказки: Rumpelstiltskin, Красная Шапочка, Три поросёнка и Goldilocks; творчество, научные опыты, phonics, песни и игры полностью на английском.',mat_big,osc_small),
      (8,'winter/english-boost-camp-2027/','Winter · English Boost','CE1–CM2, школьный класс','2027-02-08','2027-02-12','Чтение, письмо, слушание, речь, vocabulary/grammar, ролевые игры и культура. Сезонные темы обновляются; это языковой курс, не технический интенсив.',grade,grade),
      (9,'spring/i-love-london/','Spring · I Love London','3–6','2027-04-05','2027-04-09','Big Ben, Tower Bridge, автобусы и Buckingham Palace через phonics, конструирование и tea time. Тематическая неделя в Париже/Meudon, не поездка в Лондон.',mat_big,osc_small),
      (10,'spring/english-boost-camp-2027-2/','Spring · English Boost','CE1–CM2, школьный класс','2027-04-05','2027-04-09','Новый самостоятельный сезонный цикл английского: четыре языковых навыка, выступления, vocabulary/grammar, игры и культурные темы.',grade,grade)]:
        u=L+path
        p=emit(i,'Little British Schools · '+title,'FRA','Paris 6 / 7 / 16 / 17 и Meudon','languages,art,science' if i==7 else 'languages,art,technology' if i==9 else 'languages,general','day',age,
            'В собственной карточке занятия прямо описаны как полностью английские; language lessons, не робототехника.',programme,
            a+' – '+b+'; 2,5 часа в день, 12,5 часа за пять дней.',dict(year=2027,label='EUR 300 за ребёнка / неделю из пяти занятий по 2,5 часа; не полный дневной уход.',
                included='Заявленный тематический или языковой курс. Обед, care и полный день не заявлены.',extras='Другой временной слот не считается бесплатным вторым курсом; жильё, дорога, питание семьи отдельно.',
                deposit='Публичный договор курса, аванс и шкала отмены в выбранных страницах не найдены; нужно письменное подтверждение до оплаты.'),
            'Без пансиона. У младших страницы показывают AM 09:30–12 или PM 14–16:30; Meudon только AM. Boost во всех пяти расписаниях 14–16:30. Выбирают один слот.',mf,of,
            [src('Конкретный syllabus, дата, пять расписаний и тариф',u)],status='published_2027',confirmed=['EN'],role='language_lessons',sessions=[[a,b]]*5)
        p['timing']['variant_keyed']=True
        p['timing']['session_details']=[dict(start=a,end=b,label=loc,place=loc,variant_key=loc.lower().replace(' ','-'),source=u,price=p['price']['label'],date_scope='day_camp_window',date_precision='published_session',proof='Пять школьных расписаний явно показаны на собственной странице; место/слот подтверждается при записи.') for loc in locations]
    for i,age,path in [(11,'8–12','en/international-summer-camp-in-spain/'),(12,'13–17','en/summer-camp-in-spain/')]:
        mf=fit('conditional','Матвей входит в Kids 8–12; новый заезд 2027 и места пока не опубликованы.') if i==11 else fit('later','Для Teens минимальный возраст 13; пока будущий маршрут.')
        of=fit('later','Оскар младше Kids 8; в 2027 ему 6–7. Семейная смета двух участников сюда пока неприменима.') if i==11 else fit('later','До 13 лет этот подростковый трек недоступен.')
        p=emit(i,'the Village · '+('Kids' if i==11 else 'Teens'),'ESP','Corvera de Asturias · URH Zen Balagares Hotel; San Fernando International College / Avilés','general,languages,sport,art,technology','boarding',age,
            'Основная среда и проекты прямо на английском. Spanish School для международных участников — дополнительная языковая опция, не основной испанский поток. Реальную взаимную совместимость академий подтвердить.',
            'Английская среда, спорт, Chef, Broadway и Media: сценарий, съёмка, монтаж. Выбирают академии, общий лагерь не обещает программирование робота. Сайт заявляет 1 coach на 5, FAQ около 85% носителей; это собственные утверждения, не независимая проверка.',
            'Опубликованные смены только 2026: 28.06–11.07 и 12–25.07; уже прошли. Новый 2027 не объявлен; прошлое Sold Out не означает закрытый будущий набор.',
            dict(year=2026,label='Архив 2026: EUR 2 290 / две недели или EUR 4 460 / четыре; 10% VAT включён. Это не цена 2027.',
                included='Полный пансион в double/triple ensuite, базовые академии, ограниченная прачечная, liability/accident/medical assistance по оператору.',
                extras='Архив 2026: Surf 280, Sailing 405; Madrid coach return 88, Tordesillas/Benavente 78. Скидка второму брату 120 не применена к возрастно неподходящему Оскару. FAQ требует собственные ракетки/обувь/mesh laundry bags; surfing kit предоставляет школа.',
                deposit='FAQ: provisional reservation семь дней, затем первый платёж; точные refund deadlines и суммы находятся в высылаемом договоре/личном кабинете. Не стали бесплатной отменой; аккаунт и заявку не создавали.'),
            'Детский пансион, родитель не живёт в camp. Комнаты/этажи и расписания разделены по возрасту и полу, staff rooms между детскими. Laundry каждые четыре дня только часть одежды; towels/куртки не включены. Family Day отсутствует.',mf,of,
            [src('Возрастная программа, язык, архивные даты и цена',V+path),src('FAQ: staff, оснащение, ночёвки, laundry и договор',VF),src('Полная брошюра, явно сезон 2026',VP)],confirmed=['EN'],role='camp_life')
    emit(13,'HIF Swiss International School · Winter Camp 2027','CHE','HIF boarding campus · Ftan, Lower Engadin','general,sport,science','boarding','10–16',
        'English прямо в карточке зимней смены; beginner to advanced относится к snow-sports, не доказанный языковой placement.',
        'Ski/snowboard по уровню, прикладная физика снега/погоды/сил/снаряжения, карты и принятие решений, первая помощь и mountain awareness. Зимний трек не обещает летний модуль AI/robotics.',
        '10–20 февраля 2027; 11 дней / 10 ночей.',dict(year=2027,label='CHF 4 586 за участника / 11 дней, 10 ночей.',
            included='Residential programme, основные snow-sports/учебные активности и питание по описанию. Specialist equipment предоставляется, но winter gear может потребовать местной аренды: точный перечень/включение ski pass и проката подтвердить.',
            extras='Zurich Airport pick-up CHF 300: не доказан бесплатный обратный трансфер. Single/shared bathroom +500; single ensuite +1 000; pocket money 50–100. Travel/medical outdoor insurance и winter gear rental отдельно по выбранному пакету.',
            deposit='Публичная шкала аванса/отмены в прочитанной зимней странице не найдена; применимость summer terms не переносится автоматически.'),
        'Пансион: twin ensuite, возрастные группы, staff днём и ночью по оператору. Телефон хранится днём, контакт в установленное вечернее время. UM airport сопровождение описано, конкретный тариф и flight windows подтвердить.',
        fit('conditional','Матвей достигает 10 в 2027; на 10 февраля должен уже быть 10. До дня рождения минимальному возрасту не соответствует.'),
        fit('later','Оскару 6–7 в 2027, ниже минимального возраста 10.'),[src('Winter 2027: возраст, язык, программа, цена, пансион и equipment',HI)],
        status='published_2027',confirmed=['EN'],role='camp_life',sessions=[['2027-02-10','2027-02-20']])
    dated(profiles[-1],HI,'camp_session')
    p=emit(14,'Anglais in France · The French Colo Summer','FRA','Vazerac, near Toulouse / Montauban; optional riding at Molières','general,languages,sport','boarding',
        'Конфликт одной страницы: новые даты 10–16, подробный admission 11–16 и дети после collège; для 10-летнего допуск не доказан.',
        'Английский — уроки, вечерняя и общая среда. Riding на английском только с Galop 3; новичкам riding по-французски. EN не назначен автоматически всей конной опции.',
        '10 часов английского в мини-группе, водные/общие активности, вечерняя английская среда; Premium ещё 10 часов английского ИЛИ riding. 1 native leader / максимум 6 по собственному тарифу.',
        'Сезон 4 июля – 27 августа 2027, каждую неделю воскресенье 17:00 – пятница 17:00. Сохранено как сезонное окно, без выдуманного фиксированного двухмесячного пансиона.',
        dict(year=None,label='Текущий недатированный тариф: Standard EUR 765 / шесть дней, Premium EUR 910 / шесть дней. Применимость к конкретной неделе 2027 подтвердить.',
            included='10 часов английского, проживание, питание и обычные активности; Premium +10h английского или riding. Тип комнаты/число соседей не названо.',
            extras='Montauban train transfer 25 за направление / 50 return; другие поездки семьи отдельно. Insurance cancellation/assistance не включена; 2024 insurance prices не стали тарифом 2027.',
            deposit='Общие публичные CGV: аванс ≥33%, остаток за 30 дней; изменение 35. Отмена: >60 дней удерживают10% (мин50),60–31д20% (мин100),30–21д50%,20–8д75%,7–3д90%,<3д100%. Точный договор выбранной French Colo 2027 должен подтвердить применимость этих общих правил.'),
        'Residential в языковом центре; свой собственный формат комнат и ночное сопровождение уточнить. Это не автоматически host-family one-to-one, описанный в общих CGV.',
        fit('unknown','Матвею 9–10 в 2027; прямой конфликт 10–16 / 11–16 и collège не позволяет подтвердить допуск даже после 10-летия.'),fit('later','Оскар ниже обеих названных нижних границ 10/11.'),
        [src('Сезон 2027, два разных возрастных описания и syllabus',FC+'immersion/7-the-french-colo/42-colo-ete'),src('Тарифы, питание, часы и transfers',FCP),src('Общие CGV: оплатa и отмена',FCT),src('Транспорт: семье выбрать маршрут',FC+'tarifs/20-reservation/82-transport'),src('Insurance: отдельное покрытие',FC+'tarifs/20-reservation/107-assurances-sejour-linguistique')],
        status='partial_2027',confirmed=['EN'],role='camp_life',sessions=[['2027-07-04','2027-08-27']])
    p['timing']['precision']='season_window';p['timing']['session_details']=[dict(start='2027-07-04',end='2027-08-27',label='Окно недельных French Colo',place=p['place'],price=p['price']['label'],date_scope='season_window',date_precision='season_window',source=FC+'immersion/7-the-french-colo/42-colo-ete',proof='Сезон и правило воскресенье–пятница опубликованы; индивидуальные места и admission не подтверждены.')]
    emit(15,'Ciencia y Robótica · Liceo Sorolla summer camp','ESP','Liceo Sorolla, Pozuelo de Alarcón, Madrid; webpage Bularas 2 versus PDF Avda Bularas 4','robotics,coding,ai,games,technology','day',
        'Web 6–18; PDF классы Primaria/ESO и годы рождения 2010–2019. Oscar 2020 не включён в таблицу 2026; новое правило 2027 нужно отдельно.',
        'EN/ES преподавание прямо не установлено в прочитанных странице/PDF; испанский язык документа не является обещанием языка ведущего.',
        'Роботы по возрасту WeDo/EV3/Makeblock, Microbit, электроника и drones; Scratch/Alice/Kodu/RPG Maker, Roblox/Minecraft, 3D design/printing. AI только ESO. PDF описывает один компьютер и один робот/электронный kit на ученика, не покупку набора домой.',
        'Точный архив 22 июня – 17 июля 2026; уже прошёл. Смены и программа 2027 пока не опубликованы.',
        dict(year=2026,label='Архив EUR 234 / неделю; 439 за две,614 за три,789 за четыре. Web 62 / отдельный день. Не цена 2027.',
            included='В архиве lunch/snack, оборудование на занятиях, программа и school accident/liability insurance. AI syllabus для младшего школьника не гарантирован.',
            extras='2026: дополнительный час 26/нед,два часа42/нед;сibling5%/after-school5% не складываются. Приборы на сайте магазина не являются обязательной покупкой для camp.',
            deposit='PDF требует аванс170 и остаток за неделю; раздел возврата содержит 22 мая2023 в брошюре2026. Такой конфликт не принят как актуальный договор 2026/2027.'),
        'Дневной 08:50–15 в PDF /09–15 web, optional до17; пансиона нет. Точный адрес и pickup часы различаются: сверить до поездки.',
        fit('conditional','Матвей2017 есть в группе 3–4 Primaria архива2026; новый класс, смену, язык и правило2027 подтвердить.'),fit('unknown','Web6–18 и PDF только2010–2019 расходятся для Oscar2020; возрастная таблица нового года ещё нужна.'),
        [src('Собственная карточка: точный сезон2026 и общий возраст',C),src('PDF: kits, программа, классы, еда, цены и конфликт возврата',CP)])
    profiles[-len(NEW):]=readable(profiles[-len(NEW):])

def extend_report_v127(r):
    r['version']=127
    r['methodology'].append('v127: выбранные европейские junior holidays и пансионы проверены по собственным страницам и полным PDF. Пять школьных площадок LBS имеют keyed variants;14июляHopla исключено. Архив2026/общий договор/английская camp-life и язык технического курса разделены. Мировой аудит не завершён.')
    r['shortlist'] += [dict(label='Франция · оба младших в билингвальном полном дне',slugs=NEW[:7],reason='Hopla: семь точных смен,5+,FR/EN,290 за пять дней,свой lunchbox,minimum6/maximum12 по Holiday PDF. Outdoor в июле четыре дня, отдельный quote нужен.'),
        dict(label='Париж · короткие тематические и языковые курсы2027',slugs=NEW[7:11],reason='Fairytales/London3–6 только Оскару до7-летия;BoostCE1–CM2 зависит от класса.300 за12,5часа,не полный дневной лагерь;каждый campus свой вариант.'),
        dict(label='Европа · английский пансион и технический архив',slugs=NEW[11:],reason='VillageKids8–12 сMedia,2027TBC;HIFwinter10–16/Feb10–20/4586CHF дляМатвея только после10-летия;FrenchColo конфликт10/11минимум;SorollaAIтолькоESO иархив2026,новый2027ещё нужен.')]
    gaps=[('FRA','Hopla · четыре дня и возрастная группа',H,'14июлявыходной;пятидневная290 не пересчитана автоматически на четыре дня. PDFHolidaymax12/min6 отличается отWednesdaymax20;upperageHolidayне назван. Нижняядетская morningграница3–4/11:45 versus price12:00 не влияет на6/9лет,но оставлена как отличие.'),
      ('FRA','LBS · класс, слот и договор',L+'winter/fantastic-fairytales/','Новые четыре зимне-весенних курса: пять явно показанных площадок каждый. CE1–CM2не выведен из рождения;3–6до7-летия.300только2,5h×5,безобеда/пансиона. Saturdayworkshopsимеютразнуюдлительность,не превратились в camp. ПубличныйCGCввыбранныхстраницахне найден.'),
      ('ESP','Village · следующий год и договор',VF,'Все цены/смены брошюры2026. MainEN,Spanishoptionalнеосновнойпоток,Mediaне робототехника. Laundryограничен,FamilyDayнет,coach1:5собственноеутверждение. Refunddeadlineвысылаетсявprivatearea,не полученчерезсозданиеаккаунта.2027ещёне подтверждён.'),
      ('CHE','HIF · зимний quote и equipment',HI,'Смена10–20Feb2027/10–16/EN/4586,новыйwinterне summerAIrobotics. 300pick-upнеавтоматическиreturn;specialistequipmentversuswintergearrentalразделены. Составski-pass/rental/договоротменыиageна10Febещёнужен.'),
      ('FRA','French Colo · минимум10 или11',FC+'immersion/7-the-french-colo/42-colo-ete','Однастраница10–16рядомс2027и11–16/послеcollègeподробнее. CampseasonJuly4–Aug27снедельнымправилом,нефиксированнаядвухмесячнаясмена.765/910недатированы;CGVобщиедляhost-familyтоже,неавтоматическийcampagreement. RidingENтолькоGalop3.'),
      ('ESP','Sorolla · архив, год возврата и язык',CP,'2026syllabusииндивидуальныйkit+PCназанятияпрочитаны;неkitдомойинеAIвсеммладшим. Web6–18противPDF2010–2019,адрес2против4,refund2023вPDF2026,дат2027нет. ESдокументне explicitteacherlanguage. Досьеархивное,не новый доступныйлетнийcamp.'),
      ('TUR','Space Camp Türkiye · текущий первичный syllabus ещё нужен','https://www.spacecampturkey.com/en','ДваurllibTLSissuererrors;systemcurlcпроверкойTLS получил200,ноNextlandingне содержитпрочитанногополногоprogramme. Старыеcached9–18/12–15сcolarshipне перенесенына2027. Не добавлены выдуманные даты/цены/победы;турецкийлагерьостаётсяследующиммаршрутомпроверки.')]
    names={'CHE':'Швейцария','FRA':'Франция','ESP':'Испания','TUR':'Турция'}
    for iso,title,url,detail in gaps:r['gaps'].append(readable(dict(iso=iso,country=names[iso],provider='v127 · '+title,url=url,detail=detail,next_action='Продолжить первичную проверку следующего набора и всех приоритетных стран. Ни одна страна не признана полностью изученной.')))
    r['shortlist'][-3:]=readable(r['shortlist'][-3:])

def extend_planning_v127(d):
    m=d['camp_planning'];m['offers']=[q for q in m['offers'] if q['id'] not in NEW_IDS]
    m['offers'] += [offer(NEW_IDS[0],NEW[3],'Hopla · оба ребёнка ·5–9 июля2027',290,currency='EUR',format='day',checked=CHECKED,sessions=[['2027-07-05','2027-07-09']],sources=[H,HP],
        optional=[dict(id='fullcare',label='Care08:30–09и16:30–18 ·два ребёнка ×5дней ×4получаса ×2,50',amount=100)],
        unknown_required=[dict(id='food',label='Lunchboxиобаsnacksдлядвухдетей ·семейнаястоимость',unit='amount',rate=1,min=0)],
        gate='Полныйдень5+,верхнююгруппуиоткрытыйприёмподтвердить. FR/ENбилингвально;minimum6детейдляоткрытия.290за5днейнецена4дневнойOutdoorнедели.',
        included='09–16:30,билингвальныезанятия;обед/перекусыиздома.',deposit_note=HREF,scope='EUR580заоба5-дневныхкурса;собоимиполнымиcare680. Питание,жильёиродительскаядорогаещёнеоценены,неполныйtravelquote.'),
      offer(NEW_IDS[1],NEW[8],'LBS winter Boost ·толькоМатвей ·8–12февраля2027',300,currency='EUR',children=['matvey'],base_by_child=dict(matvey=300),format='day',checked=CHECKED,sessions=[['2027-02-08','2027-02-12']],sources=[L+'winter/english-boost-camp-2027/'],
        gate='CE1–CM2,классМатвеянеустановлен. Только14–16:30,одинвыбранныйcampus;это2,5h/day,неполныйdaycare. Оскаротдельно,неincluded.',
        included='Пятьанглоязычныхзанятий/12,5часа.',deposit_note='Аванс/шкалаотменыпубличноввыбраннойкарточкенераскрыты;письменныйдоговорещёнужен.',scope='300EURтолькоодинребёнок/12,5hприподтверждённомклассе. Жильё,еда,careвнеэтихчасовиОскаротдельно.')]
    m.update(version=127,asof=CHECKED)
    m['offers'][-2:]=readable(m['offers'][-2:])
