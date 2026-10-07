"""Asian winter/spring programmes and a family-friendly Australian summer option."""
from copy import deepcopy
import re
from camp_americas_v90 import clean_profile, readable

CHECKED = '2026-10-05'
GUNG = 'https://getgungho.com/'
TEAM = 'https://app.teamlinkt.com/register/go/getgungho/'
UG = 'https://u-gaku.jp/'
IM = 'https://www.imagineeducation.com.au/'
BC = 'https://www.britishcouncil.kr/en/kinder-plus-all-day-programme-aged-6%E2%80%937'
CT = 'https://www.camptaiwan.com.tw/'
GC_PDF = IM+'_files/ugd/66f0a3_5f67e11eb2104fdeab442c6b6df597ad.pdf'
BNE_PDF = IM+'_files/ugd/66f0a3_cd65e2bff6f84d9ebc857bf870365065.pdf'
GC_HOME = IM+'_files/ugd/66f0a3_a2c9913bcbd14a7da925a1566e173010.pdf'
BNE_HOME = IM+'_files/ugd/66f0a3_df495b179a1e4d088dc0058180664a01.pdf'
IM_REFUND = IM+'_files/ugd/66f0a3_f5b6f8abb6334ea59805c199861e9d41.pdf'
NOTICE = 'https://drive.google.com/file/d/1XPmUl76jQm7HKBq62Se3KbZ4p8SWV9Y9/view?usp=sharing'

def polish(s):
    replacements={
        'Englishcore subjects':'уроки английского', 'afternoonart':'творчество после обеда',
        'STEMblock':'блок STEM', 'publicholiday':'государственный праздник', 'безуроков':'без уроков',
        'optionalfamilytrip':'необязательная семейная поездка', 'schoolingweek':'неделя посещения школы',
        'schoolvisit':'посещение школы', 'sampleweek':'пример недели', 'безжилья':'без жилья',
        'offenrolmentfee':'скидка на регистрационный сбор', 'feecomponents':'части цены',
        'parenttuition':'обучение родителей', 'camp-specificприменимость':'применимость к выбранному лагерю',
        'camp-specific':'именно для лагеря', 'enrolment/placementневозвратны':'регистрация/подбор жилья невозвратны',
        'afterstartобычнонетrefund':'после начала обычно нет возврата', 'materialsrefund':'возврат за материалы',
        'waivedenrolmentfee':'без регистрационного сбора', 'freecourse':'бесплатный курс',
        'soloпансион':'самостоятельный пансион', 'fullservice':'полное сопровождение',
        'familyminimum':'минимальный семейный срок', 'housing/parentcourse/fullinvoice':'жильё/курс родителей/полный счёт',
        'foreignstaff':'иностранные сотрудники', 'foreignteachers':'иностранные преподаватели',
        'Englishgroupwork':'групповые задания на английском', 'naturehunt':'поиск природных объектов',
        'STEAMteamproject':'командный проект STEAM', 'Englishpresentation':'презентация на английском',
        'Springvenue':'Весенняя площадка', 'наоба':'на оба', 'OISTcampustour':'экскурсия по кампусу OIST',
        'businesswork/visit':'бизнес-проект/посещение', 'Операторпишет':'Оператор пишет',
        'Englishlevelany':'любой уровень английского', 'groupclasses':'групповые занятия',
        'individualhours':'индивидуальные часы', 'перенесеныиз':'перенесены из', 'вновьне суммируетсядля':'не добавляется повторно для',
        'tax/fullforeigninvoice':'налоги/полный счёт для иностранцев', 'ещёуточнить':'ещё уточнить',
        'Fee обоихсезоновиз':'Тариф обоих сезонов из', 'ownprogramme':'собственная программа',
        'ownoperatorwinterarticle':'собственная статья оператора о зиме', 'winterfee':'зимний тариф',
        'springfee':'весенний тариф', 'Cebuairportreturntransfer':'трансфер Cebu airport туда/обратно',
        'неповторенов':'не повторено в', 'feeinclude list':'перечень включений',
        'fullpackageconfirm':'полный пакет подтвердить', 'initialcontract':'первичный контракт',
        'airportpickup':'встреча в аэропорту', 'same-genderfriends/siblings':'друзья/братья/сёстры одного пола',
        'послеdeadline':'после срока акции', 'roomshare':'совместная комната',
        'политикаотмены':'политика отмены', 'Общаяполитика':'Общая политика',
        'послеapplication':'после заявки', 'отменабезfee':'отмена без сбора',
        'общегоservice':'всего обслуживания', 'впервые5':'в первые 5',
        'Japanese staffадминистративно':'административное сопровождение японских сотрудников',
        'currentstudentspriority':'приоритет нынешних учеников', 'foreignintake':'приём иностранцев',
        'Englishdevelopment':'развитие английского', 'schoolmonthlyfee':'месячная цена школы',
        'monthlyregular':'ежемесячный регулярный тариф', 'неcurrentinvoice':'не текущий счёт',
        'campteachinglanguage':'язык преподавания лагеря', 'summerchildren':'дети летнего лагеря',
        'Notyetopen':'Набор ещё не открыт', 'семейнаясмета':'семейная смета',
        'Familyweekends':'Семейные выходные', 'campbuses':'автобусы лагеря',
        'ноbusfee':'но сбор за автобус', 'неподменять':'не подменять',
        'fees2027':'тарифы 2027', 'foreignadmission':'приём иностранцев',
        'Noexternalactions':'Без внешних действий', '30min':'30 минут',
        'half-day':'полдня', 'weeklystarts':'еженедельные даты начала',
    }
    for a,z in replacements.items():s=s.replace(a,z)
    return re.sub(r'\b(SGD|AUD|JPY|KRW)(?=\d)',r'\1 ',s)

def polish_profile(p):
    for k in ['age','language','programme','accommodation','editorial_reason','place']:p[k]=polish(p[k])
    p['timing']['label']=polish(p['timing']['label'])
    for k in ['label','included','extras','deposit']:p['price'][k]=polish(p['price'][k])
    p['questions']=[polish(q) for q in p['questions']]
    for q in p['family_fit'].values():q['detail']=polish(q['detail'])
    for q in p.get('timing',{}).get('session_details',[]):
        for k in ['label','price','place','proof','entry']:
            if k in q:q[k]=polish(q[k])


def add_asia_v92(add, src, fit, P):
    start = len(P)
    def fee(year, label, included, extras, terms):
        return dict(year=year, label=label, included=included, extras=extras, deposit=terms)
    def variants(p, rows):
        p['timing'].update(sessions=[[r['start'],r['end']] for r in rows], session_details=rows, variant_keyed=True)
    def row(a, z, key, label, price, source, place, **kw):
        return dict(start=a, end=z, variant_key=key, label=label, price=price, source=source, place=place, **kw)
    language_unknown = 'Язык преподавания и сопровождения конкретной смены EN/ES/RU пока не указан. Английский сайт и перевод регистрационной формы не доказывают английские занятия.'
    g_sources = [src('Собственные возрастные/тематические программы',GUNG+'sentosa-kids-camps'),src('FAQ: группы, еда, отмена',GUNG+'camp-gungho-sentosa-faqs'),src('Активности и сопровождение',GUNG+'camper-safety-%26-wellbeing'),src('Собственные правила оплаты/возврата',GUNG+'camp-terms-and-conditions')]
    g_terms = 'Полная оплата подтверждает запись. Отмена участником/неявка обычно без возврата/переноса; документированная травма или переезд из Сингапура: возврат за вычетом транзакционных и понесённых расходов. Недобор: FAQ обещает полный возврат, terms уведомление ≥5 дней. COVID-закрытие: кредит 12 месяцев, переносимый между братьями, без cash refund. Фото/видео и live streaming разрешаются terms; условия не приняты.'
    g_extras = 'Горячий обед — платная опция, сумма не видна; иначе свой lunch/snacks. Card handling 3%; PayNow предлагают после обращения, оплата не выполнена. Жильё, перелёт, EZ-Link, страховка и возможный shuttle отдельно; точная сумма GST, скидок и билетов на экскурсии не раскрыта.'
    g_housing = 'Дневной формат 09–16, Sentosa Monorail / VivoCity H&M как места выдачи/приёма. Не пансион. По FAQ возрастные группы, максимум 1 взрослый на 10 детей (заявление оператора). Совместная группа друзей/братьев требует разницы DOB ≤12 месяцев: для братьев 2017/2020 совместную группу не обещают.'
    g_questions = ['Подтвердить EN занятий, действующие места, возраст по точному DOB, all-in invoice с GST/lunch/3%/shuttle/excursions/insurance, отдельные возрастные группы и текущую отмену.']
    both = fit('conditional','Возраст в диапазоне 5–12; visitors прямо допускаются, но язык, место, активность и окончательный DOB gate подтвердить.')
    add('gungho-general','Camp GungHo · Beach / Wilderness / Christmas','Сингапур','SGP','Sentosa; pick-up Monorail или VivoCity','general,sport,art,science','day',
        'Основные программы 5–12; Christmas Cracker: заголовок формы 5–10, body 5–12 и DOB range расходятся',language_unknown,
        'Beach: игры и Adventure Cove; Wilderness: узлы, укрытия, Morse code, солнечная готовка и outdoor; Christmas/Xtra: творчество и командные задания. Это общий отдых, не курс робототехники. Visitors разрешены собственной страницей. Kayaking только 10+, Hydrodash требует уверенного плавания; не каждый аттракцион доступен каждому возрасту.',
        'Четыре конкретные дневные смены осень/зима 2026; 2027 ещё не опубликован.',
        fee(2026,'Beach 12–16 Oct: SGD 660 (early 600 закончился 27 Sep). Wilderness 30 Nov–4 Dec и Christmas 14–18 Dec: 620 early / 660 regular. Xtra 21–23 Dec: 408 early / 430 regular. Это tuition, не полный счёт.',
            'Описанные занятия и поездки; перечень оплаченных admission tickets и meal package подтвердить. Размер автоматической sibling скидки не раскрыт; friends 3+ 8% HANGOUT не складывать автоматически.',g_extras,g_terms),g_housing,both,both,
        'Новый кандидат обоим в Сингапуре с явным visitor intake и разными возрастными группами; преподавание EN ещё не доказано.',g_questions,
        g_sources+[src('Beach live price/calendar',TEAM+'197251'),src('Wilderness live price/calendar',TEAM+'199975/'),src('Christmas age conflict / tariff',TEAM+'199973/'),src('Xtra 3-day tariff',TEAM+'199971/')],status='published_2026',priority=['both','general'])
    variants(P[-1],[
        row('2026-10-12','2026-10-16','beach','Beach Games · 09–16','SGD 660; ранний тариф 600 истёк 27.09',TEAM+'197251','Sentosa'),
        row('2026-11-30','2026-12-04','wilderness','Wilderness Survivors · 09–16','SGD 620 до 08.11 / 660 обычный тариф',TEAM+'199975/','Sentosa'),
        row('2026-12-14','2026-12-18','christmas','Christmas Cracker · 09–16','SGD 620 до 22.11 / 660 обычный тариф',TEAM+'199973/','Sentosa',age='Заголовок формы 5–10; описание 5–12, годы рождения 2013–2021: расхождение'),
        row('2026-12-21','2026-12-23','xtra','Xmas Xtra · 3 дня 09–16','SGD 408 до 29.11 / 430 обычный тариф; регистрация до 18.12, 23:55 по местному времени',TEAM+'199971/','Sentosa',deadline='2026-12-18')])
    add('gungho-santa-steam','Camp GungHo · Crunch Labs / Santa STEAM','Сингапур','SGP','Sentosa','general,science,engineering,art','day','5–12; DOB range формы2013–2021 не полностью согласован с возрастной надписью',language_unknown,
        'Наука, инженерные эксперименты, snow machine, slime/chemistry, tower challenges и творчество, затем Adventure Cove. Crunch Labs в названии формы не доказывает партнёрство с компанией/выдачу брендового набора. Робототехника, code и AI в этой программе не обещаны.',
        '7–11 December2026,09–16. Регистрационная карточка видимо прочитана без заполнения; места/допуск ещё не подтверждены.',
        fee(2026,'SGD 620 early до15.11.2026 /660 regular за5дней. Для двух детей без скидки 1 240/1 320 плюс доплаты; sibling discount неизвестна.',
            'Описанные научные/творческие активности; equipment ownership и admission tickets ещё уточнить.',g_extras,g_terms),g_housing,both,both,
        'Тематический общий STEAM для обоих; научный опыт, а не международная победа или продвинутый robotics intensive.',g_questions,g_sources+[src('Видимая собственная booking card: даты/тариф',TEAM+'199974/')],status='published_2026',priority=['both','technical'],sessions=[['2026-12-07','2026-12-11']])
    add('gungho-treasure','Camp GungHo · Treasure Island','Сингапур','SGP','Sentosa','general,art,sport','day','Сайт и выбранный заголовок формы5–8; body5–12, birth range21Nov2013–20Nov2021: конфликт',language_unknown,
        'Пиратский квест, craft, командные задачи и beach, финальный Adventure Cove. Visitors разрешены. Форма имеет реально видимый конфликт возраста, не исправленный автоматически из широкого DOB range.',
        '23–27 November2026,09–16. Next2027 dates неизвестны.',fee(2026,'SGD 620 early до01.11 /660 regular за5дней. Максимум3siblings можно регистрировать вместе; точная скидка неизвестна.',
            'Описанный дневной programme; детали invoice/tickets подтвердить.',g_extras,g_terms),g_housing,
        fit('unknown','В2026 будет8–9: header5–8 противbody5–12. Требуется точный DOB и подтверждение фактической группы; широкий form gate не принят за решение.'),
        fit('conditional','В2026 будет5–6: по обоим возрастным текстам подходит; язык/места/активности уточнить.'),
        'Младший общий вариант Оскару; Матвею возрастная группа пока не установлена.',g_questions,g_sources+[src('Видимая форма:5–8 противbody5–12',TEAM+'199976/')],status='published_2026',priority=['general'],sessions=[['2026-11-23','2026-11-27']])
    add('gungho-adventure','Camp GungHo · Adventure9–14','Сингапур','SGP','Sentosa','general,sport','day','9–14; формаDOB23Nov2011–22Nov2017',language_unknown,
        'Go-karts, Mega Zip, Hydrodash, beach, командные задачи и Adventure Cove; возраст/рост/плавание каждого аттракциона уточнить. Даты прочитаны в собственной карточке оператора, не взяты из общего баннера.',
        '23–27November2026,09–16.',fee(2026,'SGD640 early до01.11 /690regular за5дней.', 'Описанная adventure programme; все билеты/страховку подтвердить.',g_extras,g_terms),g_housing,
        fit('conditional','Форма требуетDOB≤22Nov2017. Если родился позже, в смене ещё8 и диапазон9–14 не выполняется; точный DOB неизвестен.'),fit('later','В2026 будет5–6, ниже9.'),
        'Вариант самостоятельности Матвею после9-летия; младший Treasure Island расположен в ту же неделю, совместную группу не обещают.',g_questions,g_sources+[src('Own dates/price/exact DOB gate',TEAM+'199977/')],status='published_2026',priority=['general'],sessions=[['2026-11-23','2026-11-27']])

    # Camp price and programme are distinct from the all-year monthly Kinder Plus course.
    add('british-council-korea-winter-kinder','British Council Korea · Kinder Plus Winter Camp','Южная Корея','KOR','Seoul · Seocho / City Hall centres','general,languages,art','day','Опубликованный course intake: рождённые2020/2021; camp-specific visitor exception неизвестно',
        'Программа развивает английский через immersion/Timmy/IEYC/phonics. Подтверждены языковые занятия EN; язык всего дня и camp-specific syllabus ещё неизвестны.',
        'Двухнедельный Winter Camp в учебном календаре Kinder Plus, приоритет current students. Общий IEYC/Timmy/phonics относится к круглогодичному курсу, не подтверждает40minphonics ежедневно именно в camp. Для уже уверенного EN Оскара проверить уровень/насыщенность; robotics здесь не заявлена.',
        '11–22January2027: строкаWinterCamp в semesterSep2026–Feb2027. Не Session10(25Jan–26Feb) и не регулярные10месяцев. Конкретное расписание лагерного дня уточнить.',
        fee(2027,'Отдельная стоимость Winter Camp неизвестна. KRW1 516 200Seocho /1 020 300CityHall — месячная tuition регулярного курса, не цена2недельcamp.',
            'Camp meals/materials/transport и полный invoice неизвестны.', 'Жильё/перелёт/семейное сопровождение отдельно; school monthlyfee не суммируется какmandatorycampcharge.', 'Priority currentstudents; external/foreign registration иcamprefund неизвестны. Generalcourse first-come enquiry/SMS не равно принятойcampзаявке.'),
        'Дневные центры; panсион не предложен.09:15–15:00 опубликовано для общего курса, часы зимнего camp ещё подтвердить.',
        fit('later','Матвей2017 не входит в intake2020/2021.'),fit('conditional','Oscar2020 в опубликованном intake; currentstudentspriority/foreignvisitor/уровень иместа подтвердить.'),
        'Зимний кандидат младшему, но уровень English development может быть начальным и сборы/внешнийприём ещё неизвестны.',
        ['Подтвердить внешнюю иностранную запись в WinterCamp, Oscar2020/ENlevel, camp-specificsyllabus/hours/food/fee/refund.'],[src('Own course/calendar: WinterCamp отдельно отmonthlyfee',BC)],status='published_2027',priority=['general'],confirmed=['EN'],sessions=[['2027-01-11','2027-01-22']])
    P[-1]['language_evidence_role']='language_lessons'
    variants(P[-1],[row('2027-01-11','2027-01-22','winter','Две недели · priority current students','Campfee неизвестна, не monthlycourse tuition',BC,P[-1]['place'],date_scope='day_camp_window',attendance_weekdays=['MO','TU','WE','TH','FR'])])

    # Same international operator, different campuses. Optional Saturdays are not tuition days.
    for slug,name,place,pdf,home,transport in [('imagine-gold-coast-junior','Gold Coast','9LawsonSt,Southport4215 · Gold Coast',GC_PDF,GC_HOME,'schooltransport2026 AUD100/нед.; airportGoldCoastprivate180/basic90 eachway'),('imagine-brisbane-junior','Brisbane','170LeichhardtSt,SpringHill4000 · Brisbane',BNE_PDF,BNE_HOME,'schooltransport2026 AUD120/нед.; Brisbaneprivateairport180eachway')]:
        add(slug,'Imagine Education · Junior Camp '+name,'Австралия','AUS',place,'general,languages,science,art','day,family','Junior6–11 /Senior12–16; ENelementary–intermediate',
            'English programme с практикой вclassroom/outdoor; EnglishOnly применяется в определённых activities. Это не обещание всехчасов наEN и не advancedtechnicalcourse.',
            'Культура/животные/еда/города/природа, Englishcore subjects, afternoonart/sport/excursions и единичныйSTEMblock. Samples09–15:30; publicholiday26January безуроков, Saturday optionalfamilytrip/TBC. Web30hoursExplore нельзя считать30часамиEnglish илиrobotics. GoldCoast schoolingweek требуетweek4, ноsampleweek5 остаётся обычным: schoolvisit/ages/fee ещё не установлены.',
            'Официальные flyer2027:11January–12February, выбирать1–5недель. Enrol prior11December2026; timetable приблизительный, weeklySaturday лишь optionaltrip.',
            fee(2027,'AUD250enrolment +800tuition/нед. +150materials/нед. =1 200одна /2 150две /5 000пять недель за ребёнка, безжилья/дороги. Sibling50%offenrolmentfee, неtuition; scopeскидки обоим/второму подтвердить.',
                'Tuition иmaterials поfeecomponents; hat/orientation, feedback/certificate. Lunch вsample не подтверждает включение питания.',
                'Familyhomestay иairport дополнительно. Реальный housingPDF только2026:2parents+2children placement660 +1 310/нед.;1parent+2children600 +1 100/нед., триеды/internet. '+transport+'. Прайсыhomestay/transfer2027, страховка иparenttuition неизвестны; не складывать2026жильё с 2027 camp какcurrentinvoice.',
                'Запись только послеpayment. Собственная общаяrefundpolicyv4.9:≥4 неделиwrittennotice возвратtuition;позжеcharge4недели;enrolment/placementневозвратны;afterstartобычнонетrefund. Homestayдоarrival≥8недельfullrefund иначе2неделиrent;camp-specificприменимость к1–5неделям иmaterials ещё подтвердить.'),
            'Familyhomestay option, parentsGeneralEnglish втомжеcampus(waivedenrolmentfee, неfreecourse). Учебноеsolo+homestay2026fullservice только8–17; дляОскара6–7 soloпансион не подтверждён. Individualhomestay2026minimum2нед., familyminimum/rooms/supervision2027unknown.',
            fit('conditional','Junior6–11 подходит; ENужеуверенный, сверить academicchallenge вместо повторения начальногоEnglish.'),fit('conditional','На11Jan2027 уже6–7, Junior6–11 подходит; ссемьёй предпочтительно, самостоятельныйhomestayнеподтверждён.'),
            'Семейная англоязычная программа зимой2027 с проверяемой формулойtuition; разныекампусы/трансферы, ане2оператора. Дляroboticsвыбирать отдельныйtechnicaltrack.',
            ['Подтвердить ENlevel/challenge, действующие места/weeklystarts/holidayhours, campcontract/materialsrefund/lunch, schoolingweekусловия, foreigndocuments, housing/parentcourse/fullinvoice2027.'],
            [src('Own Junior2027 programme/familyoption',IM+'junior-english-program'),src('Own campusflyer2027, обе страницы видимо проверены',pdf),src('Own feespage: housing ещё2026',IM+'fees'),src('Own homestay2026, неprice2027',home),src('Общаяrefundpolicy, campcontractуточнить',IM_REFUND)],status='published_2027',priority=['both','general'],confirmed=['EN'])
        P[-1]['language_evidence_role']='language_lessons'
        variants(P[-1],[row('2027-01-11','2027-02-12','summer-window','Выбор 1–5 недель; 26 января занятий нет','AUD 250 + 950 за каждую неделю; без жилья/трансфера',pdf,place,date_scope='day_camp_window',attendance_weekdays=['MO','TU','WE','TH','FR'],proof='Официальное окно 2027; примерное расписание. Субботние семейные поездки необязательны; 26 января уроков нет. Даты выбранных недель и условия посещения школы уточнить. Организатор просит записаться до 11 декабря 2026; точная включённая граница не установлена.')])

    ug_sources=[src('Краткиеcampdates/программы, общийindexнеполныйаудит',UG+'english-camps/'),src('Политика несовершеннолетних:foreignintakeуточнить',UG+'company/minor-policy'),src('Owncancellation90/60/45days',UG+'company/cancel-policy'),src('Refundguarantee требует≥4недель',UG+'company/refund-policy')]
    ug_terms='ПервичныйcontractfeeJPY30 000;repeatбезнего. Общаяполитика:раньше90дней ив первые5днейпослеapplication отменабезfee, далееcontractfee;с90/60/45дней50%/70%/100%общегоservice+relatedcosts. Точные включённые границы90дней перекрываются;campcontractполучить. Послеstartвозвратнет. Fullrefundguarantee требует≥4недель/заявку≤3дней/attendance:не автоматический возврат5/7-дневногоcamp. Медицинские/дорожные расходы родителей, никакихзаявок/согласий не отправлено.'
    gradefit=fit('unknown','Требуются фактический школьный класс/эквивалентelementaryилиmiddle, точныйDOB, иностранный приём и административная/medicalподдержкаEN. Годрожденияне заменяеткласс.')
    for slug,name,iso,country,place,base,cap,content in [
        ('ugaku-nasu','Nasu / Nasu Kashi','JPN','Япония','Winter: Nasu Grand Garden, Tochigi; spring: National Nasu Kashi Youth Nature House, Nishigo,Fukushima',159800,15,'Зимойcamp-life сforeignstaff, nature/craft/Englishgroupwork. Spring2027: naturehunt/orienteering/craft, STEAMteamproject/BBQ иEnglishpresentation. SpringvenueFukushima отличается отwinterTochigi;meetingJRShinShirakawa11:00наобаends.'),
        ('ugaku-okinawa','Okinawa · English & Business','JPN','Япония','Winter:3-110Miyagi,Chatan; spring:PensionThreePeace,Onna (exclusive)',139800,20,'Совместная жизнь сforeignteachers/Englishgroupwork. Spring2027: создать свой магазин наEN, OISTcampustour, aquarium/Ryukyumura/sea/cooking/BBQ иfinalpresentation. Этоbusinesswork/visit, не лабораторная стажировкаOIST. SummaryпредпочитаетENintermediate+, brochureдля начинающих проверить.'),
        ('ugaku-cebu','Cebu · One-to-One English','PHL','Филиппины','28EmilioOsmeñaSt,CebuCity;Mactan-Cebuairportmeeting',139800,10,'Spring2027:14часовone-to-oneEN +groupclasses, islandhop/NGOvisit/market/cooking/presentation. Зимойindividualhoursне перенесеныизspring. ОператорпишетEnglishlevelany, Japanese24hstaff — ENmedical/adminsupportпроверить.')]:
        url=UG+'english-camps/'+slug.removeprefix('ugaku-')+'/'
        add(slug,'U-GAKU · English Camp '+name,country,iso,place,'general,languages,science,art'+(',entrepreneurship' if iso=='JPN' and slug.endswith('okinawa') else ''),'boarding','Elementary/middle-school children; числовойageне замещаеткласс',
            'Ownprogramme прямоEnglishсforeignteachersвобщении/питании/активностях; Japanese staffадминистративно. ЭтоENcamp-life +языковая практика, языкформ/medicalпомощи для иностранной семьи уточнить.',content,
            'Зима 26–30 декабря 2026 / 4 ночи; весна 28 марта–3 апреля 2027 / 6 ночей. '+str(cap)+' мест весной. '+('Cebu: 20 зимой / 10 весной. ' if iso=='PHL' else 'Okinawa: верхний блок страницы 10 мест, подробный 20 — расхождение сохранено. ' if slug.endswith('okinawa') else '')+'Площадки и даты различаются по сезону.',
            fee(2027,'WinterJPY'+f'{base:,}'+' +initial30 000 ='+f'{base+30000:,}'+';Spring199 800 +30 000 =229 800. Contractfeeвновьне суммируетсядляrepeat;tax/fullforeigninvoiceещёуточнить. '+('Nasu winterfeeизownoperatorwinterarticle, springfeeизownprogramme.' if slug=='ugaku-nasu' else 'Feeобоихсезоновизownprogramme.'),
                ('Cebuairportreturntransfer, lessons/materials/activities/3meals/support; roomназван, ноhousingнеповтореновfeeinclude list:полныйpackageconfirm.' if iso=='PHL' else 'Housing/meals/lessons/materials/activities/support;поFAQобычно3meals,first/lastdayмогутотличаться.'),
                'Flights/pocketmoney/initialcontract/insurance/medicalиз политики отдельно. '+('Airporttransferназван включённым;foreignpassport/childentrydocumentsпроверить по официальным правилам;supportне равно полученному разрешению.' if iso=='PHL' else 'Airport/stationtransferoptionплатно, прайсаещёнет;дляNasuвеснойmeetingstationнеairportpickup.'),ug_terms),
            'ResidentialEnglishCamp;foreignteachers+Japanesestaff. Springrooms2–4поакциидо31Octсоsame-genderfriends/siblings;roomshareнеguaranteeпослеdeadline. Языковые иforeignadmissionусловия для семьи неизвестны.',gradefit,gradefit,
            'КороткийENпансион/проектысownseasonfees. ДлясемьиEN/ES/RUбезJapaneseнужныclass-equivalenceиEnglishadministration, независимыйtoprankнеприсвоен.',
            ['Проверить фактическиеclasses, foreignchildEN/admin/medicalsupport, campcontract/cancelboundaries/tax/insurance, pickup/room и availability; дляCebuforeignentry отдельно.'],
            [src('Ownseasonprogramme/fee/venue',url),src('Ownwinterrelease:3точныхcampместа',UG+'news/2026-winter-english-camp/')]+([src('Ownoperatorarticle: только свойNasu wintertariff,неrank другихоператоров',UG+'media/kokunai/english-camp/winter_english_camp/')] if slug=='ugaku-nasu' else [])+ug_sources,status='published_2026_27',priority=['general','boarding'],confirmed=['EN'])
        P[-1]['language_evidence_role']='camp_life'
        winterplace=place.split(';')[0];springplace=place.split(';')[-1]
        variants(P[-1],[row('2026-12-26','2026-12-30','winter','4ночи/5дней',f'JPY{base:,} +30 000initialcontract',url,winterplace),row('2027-03-28','2027-04-03','spring','6ночей/7дней', 'JPY199 800 +30 000initialcontract',url,springplace)])

    ct=next(p for p in P if p['slug']=='camp-taiwan')
    ct['checked']=CHECKED
    ct['timing'].update(status='published_2027',label='Own2027summer page:5–10/12–17/19–24/26–31July,2–7/16–21August. Все6смен Not yet open;9–14Augustнепридуманыизweeklymarketing.',sessions=[['2027-07-05','2027-07-10'],['2027-07-12','2027-07-17'],['2027-07-19','2027-07-24'],['2027-07-26','2027-07-31'],['2027-08-02','2027-08-07'],['2027-08-16','2027-08-21']])
    ct['availability']=dict(status='not_open_yet',label='Набор ещё не открыт',checked=CHECKED)
    ct['timing']['session_details']=[dict(start=a,end=z,label='Summer2027 · набор ещё не открыт',price='Текущая страница: YouthNT$24 000/группа2–5по23 000; invoice2027ещёподтвердить',source=CT+'summer-camp',place=ct['place'],entry='Набор2027 ещё не открыт; дождаться объявления и подтвердить точный DOB/иностранный приём.',availability=deepcopy(ct['availability'])) for a,z in ct['timing']['sessions']]
    ct['price']['year']=2027
    ct['price']['label']='Текущая страница с календарём 2027: Youth 7–12 лет NT$24 000 за 6 дней / 5 ночей; группа 2–5 детей по 23 000, 6–10 по 22 000, 11+ по 21 000. Teen 13–16 лет 26 000, групповые тарифы 25 000 / 24 000 / 23 000. У цен нет отдельного годового штампа: финальный счёт 2027 ещё подтвердить. Набор ещё не открыт.'
    ct['price']['included']='Уведомление разделяет общий тариф на регистрацию NT$1 000, обязательный автобус NT$1 000 и оставшееся обучение. Первые две суммы уже входят в общий тариф, их не добавляют повторно. FAQ и памятка описывают палатки и три приёма пищи в день. Автобусы из Тайбэя; трансфер аэропорта отдельно. Окончательный состав счёта 2027 подтвердить.'
    ct['price']['extras']='По уведомлению за международную оплату PayPal/картой добавляется 5%; этот сбор невозвратный даже при возврате основной цены. Перелёт, трансфер аэропорта, страховка и семейные выходные отдельно. Памятка предусматривает иностранных участников, но приём именно этих детей ещё не подтверждён.'
    ct['price']['deposit']='Недатированное уведомление: оплатить в течение 14 дней после регистрации. Регистрационные NT$1 000 невозвратны. При расхождении официальна английская версия: за 30 / 21–29 / 11–20 / 4–10 / 1–3 дня возвращают 100 / 90 / 70 / 50 / 30% обучения и транспорта; в день старта 0. В китайской версии за 21–29 / 11–20 / 4–10 дней транспорт возвращают полностью, за 1–3 дня — 50%; сохранён приоритет английской версии. Срок более 30 дней и точную границу уточнить. При болезни/тайфуне после полного лагерного дня — пропорциональный возврат за обучение; отмена оператором даёт кредит либо возврат по той же таблице, 100% деньгами не гарантированы. Хотя бы один опекун должен находиться на Тайване и забрать заболевшего ребёнка. Актуальность договора для 2027 подтвердить.'
    ct['accommodation'] += ' По уведомлению хотя бы один родитель/опекун должен находиться на Тайване во время лагеря, чтобы забрать ребёнка при болезни или травме.'
    ct['questions']=['Подтвердить открытие шести смен 2027, достижение Оскаром 7 лет к началу, иностранный приём и полный счёт со страховкой. Учесть опекуна на Тайване; получить актуальные условия 2027 и точную границу возврата за 30 дней. Семейные выходные — отдельная программа: октябрьские даты 16–18 против 17–18 не согласованы.']
    for s in ct['sources']:s['checked']=CHECKED
    ct['sources'] += [dict(title='Ownsummerhandbook:bus/meals/communication',url=CT+'parent-handbook-getting-ready-for-camp',checked=CHECKED),dict(title='LinkedCAMPnotice,actualseasoncontractещёпроверить',url=NOTICE,checked=CHECKED)]
    # Reader-facing copy uses plain Russian; evidence URLs and structured dates stay exact.
    for p in P[start:]:
        if p['slug'].startswith('gungho-'):
            p['price']['extras']='Горячий обед оплачивается отдельно, цена не видна; можно приносить свой обед и перекусы. При оплате картой сбор 3%. PayNow предлагается после обращения. Жильё, перелёт, EZ-Link, страховка и возможный шаттл отдельно. Полный счёт с GST, скидками и входными билетами пока неизвестен.'
            p['price']['deposit']='Полная оплата подтверждает запись. Отмена участником или неявка обычно без возврата и переноса. При документированной травме либо переезде из Сингапура возможен возврат за вычетом транзакционных и понесённых расходов. При недоборе FAQ обещает полный возврат, условия — уведомление минимум за 5 дней. При COVID-закрытии кредит на 12 месяцев, переносимый между братьями; возврат деньгами не обещан. Условия включают разрешение на фото, видео и прямые трансляции; от имени семьи они не приняты.'
            p['accommodation']='Дневной лагерь 09:00–16:00; точки приёма и выдачи — Sentosa Monorail либо VivoCity у H&M. Пансиона нет. По FAQ максимум 10 детей на взрослого; независимой проверки этого соотношения нет. Друзья и братья в одной группе должны различаться по дате рождения не более чем на 12 месяцев: общую группу для детей 2017 и 2020 годов не обещают.'
            p['questions']=['Подтвердить английский преподавания, места, возраст по точной дате рождения и ограничения аттракционов. Получить полный счёт с GST, обедом, сбором карты, шаттлом, билетами, страховкой, скидкой братьям и действующими условиями отмены.']
        if p['slug'].startswith('imagine-'):
            p['age']='Junior 6–11 лет; Senior 12–16. Английский начального и среднего уровня.'
            p['language']='Подтверждены занятия английским и его практическое использование. Правило English Only действует в отдельных активностях; весь день только на английском и язык технического блока не подтверждены.'
            p['programme']='Уроки английского, знакомство с культурой, животными, едой, городом и природой; после обеда творчество, спорт и экскурсии, отдельный блок STEM. Это языковая программа с общими активностями. Пример дня 09:00–15:30; субботние семейные поездки необязательны, 26 января уроков нет. Указанные на сайте 30 часов Explore не означают 30 часов английского или робототехники. Для школьной недели Gold Coast просят посещать неделю 4, но пример недели 5 обычный: возраст, состав и доплату посещения школы ещё уточнить.'
            p['timing']['label']='11 января–12 февраля 2027; выбрать 1–5 недель. В буклете просят записаться до 11 декабря 2026, точную включённую границу подтвердить. Расписание примерное, субботние поездки — по выбору.'
            p['price']['label']='AUD 250 регистрация + 800 обучение/нед. + 150 материалы/нед. = 1 200 за одну, 2 150 за две, 5 000 за пять недель на ребёнка. Жильё и дорога отдельно. Скидка братьям 50% только на регистрацию; применение ко второму или обоим детям уточнить.'
            p['price']['included']='Обучение и материалы по указанной формуле; шляпа, вводная встреча, обратная связь и сертификат. Обед в расписании не доказывает включённое питание.'
            p['price']['extras']='Семейное жильё и аэропорт оплачиваются отдельно. Прайс жилья только 2026: 2 родителя + 2 ребёнка AUD 660 подбор + 1 310/нед.; 1 родитель + 2 ребёнка 600 + 1 100/нед., с тремя приёмами пищи и интернетом. '+('Gold Coast: доставка в школу 100/нед., аэропорт 180 частный / 90 основной за направление.' if p['slug']=='imagine-gold-coast-junior' else 'Brisbane: доставка в школу 120/нед., частный аэропорт 180 за направление.')+' Это тарифы 2026, жильё и транспорт 2027 пока неизвестны. Страховка и обучение родителей отдельно; итоговый счёт 2027 нельзя получить сложением разных годов.'
            p['price']['deposit']='Место подтверждается после оплаты. Общая политика возврата v4.9: письменное уведомление минимум за 4 недели даёт возврат обучения, позднее удерживают 4 недели; регистрация и подбор жилья невозвратны, после начала возврата обычно нет. За жильё до приезда при уведомлении минимум за 8 недель полный возврат, позднее удерживают 2 недели аренды. Применение к лагерю на 1–5 недель и возврат за материалы ещё подтвердить.'
            p['accommodation']='Возможен семейный homestay. Родителям предлагают General English в том же кампусе без регистрационного сбора; сам курс платный. Самостоятельное обучение с полным сопровождением и проживанием в прайсе 2026 — только 8–17 лет: Оскару 6–7 лет пансион без родителей не подтверждён. Минимальный индивидуальный срок 2026 — 2 недели; семейный минимум, комнаты и надзор 2027 неизвестны.'
            p['editorial_reason']='Семейный зимний вариант с проверяемым тарифом обучения. Это два кампуса одного оператора. Детям, уже владеющим английским, проверить сложность; для робототехники нужен отдельный технический курс.'
            p['questions']=['Подтвердить уровень и сложность, места, даты выбранных недель и часы в праздники. Получить договор лагеря, правила возврата за материалы, обед, условия посещения школы и полный счёт 2027 на жильё, транспорт и курс родителей.']
        if p['slug'].startswith('ugaku-'):
            p['age']='Дети начальной и средней школы; нужен фактический класс или его признанный эквивалент.'
            p['language']='Английский используется с иностранными преподавателями в жизни лагеря, за едой и в активностях; есть языковые занятия. Административное сопровождение японских сотрудников. Поддержка иностранной семьи и медицинское общение на английском пока не подтверждены.'
            winter_base=159800 if p['slug']=='ugaku-nasu' else 139800
            p['price']['label']=f'Зима JPY {winter_base:,} + 30 000 первичный контракт = {winter_base+30000:,}; весна 199 800 + 30 000 = 229 800. При повторном посещении контракт не добавляется. Зимний Nasu в собственной статье обозначен с налогом; налоги и полный счёт остальных вариантов подтвердить.'.replace(',',' ')
            p['programme']={
                'ugaku-nasu':'Зимой совместная жизнь с иностранными сотрудниками, природа, творчество и групповые задания на английском. Весной поиск природных объектов, ориентирование, творчество, командный проект STEAM, барбекю и презентация на английском. Зимняя площадка Nasu Grand Garden в Tochigi; весенняя National Nasu Kashi Youth Nature House в Nishigo, Fukushima. Весенняя встреча и выдача у JR Shin-Shirakawa в 11:00, аэропорт не обещан.',
                'ugaku-okinawa':'Совместная жизнь и групповые задания с иностранными преподавателями. Весной дети создают собственный магазин на английском, посещают кампус OIST, океанариум и Ryukyu Mura, готовят, участвуют в морских активностях и итоговой презентации. Посещение OIST — экскурсия, лабораторная стажировка не заявлена. На странице предпочтителен средний уровень английского и выше; младшую/начальную группу уточнить.',
                'ugaku-cebu':'Весной 14 часов индивидуального английского плюс групповые уроки, поездка по островам, посещение NGO, рынок, готовка и презентация. 14 индивидуальных часов не перенесены на зиму. Оператор пишет о любом уровне английского и японских сотрудниках 24 часа; медицинскую и административную помощь английским иностранной семье подтвердить.'
            }[p['slug']]
            p['price']['deposit']='Первичный контракт JPY 30 000; повторно он не добавляется. Общие условия отмены: раньше 90 дней и в первые 5 дней после заявки без сбора, позже — сбор контракта; с 90 / 60 / 45 дней удерживают 50 / 70 / 100% обслуживания и связанные расходы. Формулировки точной границы 90 дней перекрываются — нужен договор смены. После начала возврата обычно нет. Гарантия полного возврата требует минимум 4 недели, обращения в первые 3 дня и соблюдения условий посещаемости: на лагерь 5 или 7 дней автоматически не распространяется.'
            p['accommodation']='Пансион с иностранными преподавателями и японскими сотрудниками. Весной предлагаются комнаты на 2–4 человека. Акция совместной комнаты друзьям/братьям одного пола действует до 31 октября; после неё размещение вместе не гарантировано. Иностранный приём и административную поддержку английским подтвердить.'
            p['editorial_reason']='Короткий пансион с английским и проектами, опубликованными сезонными тарифами. Для вашей семьи проверить признание классов, иностранный приём и поддержку на английском; мировой рейтинг независимо не установлен.'
            p['questions']=['Подтвердить фактические классы, иностранный приём, административную и медицинскую поддержку на английском, свободные места и размещение. Получить договор конкретной смены, полный счёт с налогами, страховкой и трансферами. Для Cebu отдельно проверить официальные правила въезда иностранного ребёнка.']
            for f in p['family_fit'].values():f['detail']='Нужны фактический школьный класс или его признанный эквивалент, точная дата рождения, иностранный приём и поддержка на английском. Год рождения не заменяет класс.'
        if p['slug']=='british-council-korea-winter-kinder':
            p['age']='Опубликованный приём курса: дети 2020 и 2021 годов рождения. Исключения для иностранных участников лагеря неизвестны.'
            p['programme']='Зимний двухнедельный лагерь в календаре Kinder Plus, приоритет нынешних учеников. IEYC, Timmy и ежедневные 40 минут фонетики описаны для круглогодичного курса; содержание конкретного лагеря ещё неизвестно. Программа развивает английский. Для Оскара, уже владеющего языком, проверить уровень и сложность; робототехника не заявлена.'
            p['timing']['label']='11–22 января 2027 в календаре учебного полугодия сентябрь 2026–февраль 2027. Это отдельный Winter Camp, расписание его дня уточнить.'
            p['price']['label']='Цена Winter Camp неизвестна. KRW 1 516 200 Seocho / 1 020 300 City Hall — месячная цена обычного курса; это не цена двух недель лагеря.'
            p['price']['included']='Питание, материалы, транспорт лагеря и полный счёт неизвестны.'
            p['price']['extras']='Жильё, перелёт и семейное сопровождение отдельно. Месячную цену курса не добавляют как обязательный лагерный сбор.'
            p['price']['deposit']='Приоритет нынешних учеников. Приём внешних/иностранных детей и возврат оплаты лагеря неизвестны. Форма интереса и SMS по обычному курсу не означают принятую заявку в лагерь.'
            p['accommodation']='Дневные центры Seocho / City Hall, пансион не предложен. Часы 09:15–15:00 относятся к обычному курсу; для лагеря уточнить.'
            p['editorial_reason']='Зимний языковой кандидат Оскару. Для уверенного английского программа может оказаться начальной; внешний приём и лагерные сборы ещё неизвестны.'
            p['questions']=['Подтвердить внешний иностранный приём Оскара 2020 года, уровень и сложность, содержание именно Winter Camp, часы, питание, цену и отмену.']
    ct['timing']['label']='Лето 2027: 5–10, 12–17, 19–24, 26–31 июля; 2–7 и 16–21 августа. Шесть смен, набор ещё не открыт. 9–14 августа в расписании нет.'
    for v in ct['timing']['session_details']:
        v['label']='Лето 2027 · набор ещё не открыт'
        v['price']='Текущая страница: Youth NT$24 000; группа 2–5 по 23 000. Финальный счёт 2027 подтвердить.'
        v['entry']='Набор 2027 ещё не открыт; дождаться объявления и подтвердить точную дату рождения и иностранный приём.'
    for p in P[start:]+[ct]:
        p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
        clean_profile(p)
        polish_profile(p)


def extend_report_v92(report):
    ss=len(report['shortlist']); gs=len(report['gaps'])
    report['shortlist'].extend([
        dict(label='Тайвань · шесть летних смен 2027, набор ещё не открыт',slugs=['camp-taiwan','camp-taiwan-family','typa','tas'],reason='Camp Taiwan опубликовал шесть смен; Оскару только после 7-летия. Текущая цена Youth NT$24 000, группа 2–5 по 23 000; финальный счёт 2027 уточнить. Регистрация и автобус уже входят в цену, международная карта +5%. Хотя бы один опекун остаётся на Тайване. Летний английский подтверждён; язык семейных выходных и октябрьские даты 16–18 против 17–18 ещё неизвестны.'),
        dict(label='Сингапур · общие каникулы обоим, отдельно робототехника Матвею',slugs=['gungho-general','gungho-santa-steam','gungho-treasure','gungho-adventure','computhink-lego'],reason='GungHoпрямодопускаетvisitors,прочитаныspecificprices620/660и3-day408/430, ENteachingunknown. AgeTreasure5–8vsbody5–12, AdventureDOB≤22Nov2017. Разныеagegroupsбратьев, lunch+3%cardextras. Computhink7–12/367SGD/9hостаётсяcandidateМатвею, ENещёуточнить;черновикURL404неиспользован.'),
        dict(label='ЮжнаяКорея · короткий языковой кандидат Оскару',slugs=['british-council-korea-winter-kinder','camp-sfs','dwight-seoul-junior'],reason='KinderPlusWinter11–22Jan2027приоритетcurrentstudents,intake2020/2021. Oscarусловно;Matvey2017неподходит. Monthlytuitionнеcampprice, ENlanguagelearning/actualcampcontentиforeignintakeпроверить.'),
        dict(label='Япония/Филиппины · зима2026 и весна2027 наEN',slugs=['ugaku-nasu','ugaku-okinawa','ugaku-cebu','english-adventure-winter','evergreen-hakuba-winter'],reason='U-GAKUownactualspring28Mar–3Apr2027,199800+initial30000JPY, разныеwinter/springvenues. NasuSTEAM, Okinawabusiness/OISTtour,Cebu14hone-to-oneтольковесной. Elementary/middlegradeэквивалент не выводим изDOB. Japaneseadmin/foreignintake/cancel90/60/45tiersещёсогласовать;4-weekguaranteeнепокрывает5/7daysавтоматически.'),
        dict(label='Австралия · семейное обучение в январе–феврале2027',slugs=['imagine-gold-coast-junior','imagine-brisbane-junior'],reason='Junior6–11оба,Englishlevelbeginner/intermediate:для уже уверенногоENтребуется более интересныйlevel. Own2027flyer250+800/wk+150/wk, familyhomestayопция имеет только2026price. Parentsнеполучаютfreecourse;Oscarstandalonesoloнеподтверждён. Saturdayoptional/26Janholiday иschoolingweekнепревращеныв30hEnglish/robotics.')
    ])
    report['gaps'].extend([
        dict(country='Тайвань',iso='TWN',provider='v92 · новый сезон Camp Taiwan',detail='Шесть смен 2027: набор ещё не открыт. Текущая цена Youth NT$24 000 / группа 2–5 по 23 000, Teen 26 000; финальный счёт сезона не подтверждён. По недатированному уведомлению регистрация 1 000 и обязательный автобус 1 000 — части цены; международная карта +5%, сбор невозвратный. Опекун должен оставаться на Тайване. Английская версия возврата имеет официальный приоритет, транспортные проценты расходятся с китайской. Летний EN, помощь на Mandarin, палатки и питание проверены; семейный EN, цена и октябрьские даты 16–18 против 17–18 неизвестны. Смена 9–14 августа не опубликована и не добавлена.',next_action='Проверить открытие набора, договор 2027, полный счёт/страховку, иностранный приём и 7-летие Оскара; продолжить другие тайваньские школьные и технические программы.',url=CT+'summer-camp'),
        dict(country='Сингапур',iso='SGP',provider='v92 · GungHo visitors, цены и конфликт DOB',detail='Actualprogrammeforms620/660,Adventure640/690,Xtra408/430 и3%cardhandling;earlyBeach600истёк27Sep. Treasuryheader5–8/body5–12 иChristmas5–10/body5–12 +широкиеDOBgatesне исправлены автоматически. Genericrestricted/waitlistHTMLtemplatesнеозначаютblocked/soldout:видимоформы Santa/Treasureпоказывают обычнуюstep1. ENunknown, lunch/shuttle/tickets/GSTнеall-in,95/2023archiveнеперенесены. Computhinkdraft404;canonicalсохраняет4ранее проверенныхdates367/9h, nopaddingnewoperator.',next_action='EN/age/availability иполныйfamilyquote;остальныеSingaporetechnical иgeneraloperators/2027не полностью аудированы.',url=GUNG+'sentosa-kids-camps'),
        dict(country='ЮжнаяКорея',iso='KOR',provider='v92 · KinderPlus противстарших ICI',detail='OwnWinter11–22Jan2027 вacademicSep2026–Feb2027, intake2020/2021/currentstudentspriority. Campfeeнеmonthlyregular1,516,200/1,020,300KRW. ДвеdirectHTTPtimeout попытки не выданы какdirectsuccess;primaryweb+раскрытыйbrowsercalendarпрочитаны. ICIwinter2026–27толькомiddle/high/university:невыданкак6/9camp, EN/KOusageнеполноеENinstruction.',next_action='ForeignexternalOscarintake/level/contract,другиеKoreayoungEnglishprogrammes иboardingпослеprimaryverification.',url=BC),
        dict(country='Япония / Филиппины',iso='JPN',provider='v92 · U-GAKU новые springdates и несовершеннолетние',detail='Spring28Mar–3Apr2027ownpages,199800+30000JPY. Nasu winterTochigi/springFukushimaNationalCentre, OkinawawinterChatan/springOnna, Cebuairportreturntransferexplicit. Okinawa10topvs20detailedcapacity,ENintermediate+,gradeequivalence/foreignadminunknown. Cancellation50/70/100%service+costsна90/60/45;generalrefundguarantee≥4weeksне5/7-daypromise;Cebuofficialforeignentryrequirementsещё не исследованы.',next_action='Действующийchildcontract/fullinvoice/gradeequivalence/ENmedicaladmin/foreignadmission, потомпрочиеJapan/Asia/camps2027.',url=UG+'english-camps/'),
        dict(country='Австралия',iso='AUS',provider='v92 · Imagine family option и разные годы прайса',detail='Own2027campusflyers6–11/12–16,11Jan–12Feb1–5weeks;250enrol+800tuition+150materialsweek. Website30hExploreне30hEnglish;Saturdayfamilyoptional/26Janholiday. GoldCoastschoolingweekneedsweek4бездоказанногоschoolvisitfee/age. Homestay2026 2parents2children660placement+1310week,transport100GC/120BNE;2027housingunknown. Solofullservice2026minimum8неOscar6. Generalrefundv4.9неcamp-specificcontract.',next_action='Exact2027familyinvoice/lunch/room/parentcourse/hours/level/contract;страна одна из мирового списка, не завершённый полныйAUSaudit.',url=IM+'junior-english-program')
    ])

    for q in report['shortlist'][ss:]:
        for k in ['label','reason']:q[k]=polish(readable(q[k]))
    for q in report['gaps'][gs:]:
        for k in ['provider','detail','next_action']:q[k]=polish(readable(q[k]))
