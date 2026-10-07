"""Selected Asian primary programme clauses, exact winter dates and Taiwan 2027."""
import re
CHECKED='2026-10-05'
DUL='https://www.dulwich.org/world/camps'
YC='https://www.ycyw-edu.com/en/2026-ycyw-summer-programme-primary-programme'
YCI='https://www.ycyw-edu.com/en/summer-programme-2026'
MI='https://www.mandarininn.cn/chinese-summer-camp-shanghai'
TC='https://www.tinycode.hk/in-home-camps/'
TCT='https://www.tinycode.hk/terms-and-conditions/'
AO='https://aisloutdoor.com/products/'
POL='https://aisloutdoor.com/pages/policies-and-guidelines'
JG='https://www.jgroup.com.tw/'
JGEN=JG+'summer-back-in-taiwan/'
JC=JG+'%E5%A4%8F%E4%BB%A4%E7%87%9F/'
CITY='https://tctimewalk.com/'
NEW=['dulwich-ai-film','dulwich-lita-festive','dulwich-finland-winter',
     'ycis-shanghai-english','ycis-beijing-vex','ywies-beijing-vexiq','ywies-tongxiang-vex',
     'mandarininn-shanghai','tinycode-scratch','tinycode-robot','tinycode-games','tinycode-ai',
     'harrow-hk-ecobot','harrow-hk-sleigh','harrow-guangzhou-auto','harrow-myoko-ski',
     'tc-city-ambassador','jasmine-build','jasmine-shop','jasmine-discovery','jasmine-micro','jasmine-nola','jasmine-winter-block']

def add_asia_v102(add,src,fit,profiles):
    def emit(*args,variants=None,role=None,support=None,**kw):
        add(*args,**kw);p=profiles[-1];p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
        if role:p['language_evidence_role']=role
        if support:p['confirmed_support_languages']=support
        if variants:
            for v in variants:v.setdefault('place',p['place'])
            p['timing'].update(session_details=variants,variant_keyed=True,sessions=[[v['start'],v['end']] for v in variants])
        def prose(value):
            if isinstance(value,dict):return {k:prose(v) for k,v in value.items()}
            if isinstance(value,list):return [prose(v) for v in value]
            if not isinstance(value,str):return value
            # Human prose only: identifiers, dates and source URLs are untouched.
            value=re.sub(r'(?<=[А-Яа-яЁё])(?=[A-Za-z0-9])|(?<=[A-Za-z0-9])(?=[А-Яа-яЁё])',' ',value)
            value=re.sub(r'\b(RMB|HKD|NT|Grade|G|Y)(?=\d)',r'\1 ',value)
            value=re.sub(r'(?<=[a-z])(?=[A-Z])',' ',value)
            value=re.sub(r'([,;])(?=\S)',r'\1 ',value)
            substitutions={'необещаем':'не обещаем ', 'неизвестны':'не известны', 'неустановлены':'не установлены',
                           'нужноподтвердить':'нужно подтвердить', 'точныедаты':'точные даты', 'всемейной':'в семейной',
                           'полнаяоплата':'полная оплата', 'всчёт':'в счёт', 'дооплаты':'до оплаты', 'согласоватьDOB':'согласовать DOB',
                           'неполная':'не полная', 'неанглийский':'не английский', 'неперенесён':'не перенесён',
                           'неточно':'не точно', 'навыбранные':'на выбранные', 'толькопосле':'только после ',
                           'одинchange':'один change', 'НЕдобавлятьещё':'НЕ добавлять ещё ', 'ПолныйEN':'Полный EN',
                           'НАдатурегистрации':'на дату регистрации', 'НАдатуРЕГИСТРАЦИИ':'на дату регистрации'}
            for a,b in substitutions.items():value=value.replace(a,b)
            return value.strip()
        for k in ['provider','place','age','language','programme','price','accommodation','family_fit','editorial_reason','questions']:
            p[k]=prose(p[k])
        return p
    unknown='Полный договор, иностранный индивидуальный приём, медицинская страховка, места и окончательный счёт требуют подтверждения. Заявки не подавались.'
    emit('dulwich-ai-film','EIMx / Dulwich · AI Movie Creation',
         'Китай','CHN','Beijing / Shanghai / Xi’an · Dulwich или Dehong; распределение дат по кампусам уточнить',
         'ai,art,coding','day','Y5–Y7 / G4–G6; классы детей неизвестны',
         'Прямо English; внешним non-EiM нужны доказательства английского или короткое интервью. EN/ES способности семьи не заменяют школьный порог.',
         'Команда создаёт короткий фильм: story/storyboard → AI visuals, voice, music → editing/post-production → показ и объяснение решений. Каждый из форматов3/5дней проходит весь цикл. Максимум30 в классе. Финальный AI Film Festival — внутренний показ лагеря, не международная кинонаграда.',
         '3–5 и3–7 октября2026 уже начались; на дату проверки5октября нельзя обещать поздний вход. Нового набора2027 нет. Текущий частично прошедший курс не добавлен как новая будущая смена.',
         dict(year=2026,label='Стандарт RMB6500/3дня или10800/5дней. EiM5500/9180; early bird5225/8721 истёк14сентября. Это не тариф2027.',included='Учебная программа; состав питания/материалов/страховки не раскрыт.',extras='Жильё семьи, дорога, устройства, платные AI accounts/API и дополнительные сборы неизвестны.',deposit=unknown),
         'Дневной; пансиона и проживания семьи в кампусе не заявлено.',
         fit('unknown','Нужен фактический классY5–7/G4–6, не выводим его из2017года.'),fit('unknown','Класс не установлен; младший возраст сам по себе не разрешает вход вG4–6.'),
         'Полезный пример реального AI production курса в Китае; пока архив начавшегося набора и школьная категория, а не готовый маршрут обоим.',
         [unknown,'Точный campus/новый сезон, класс/EN interview, devices/accounts и часы практики.'],[src('Собственная AI programme: сроки, G4–6, EN, цены, max30',DUL)],status='archive_next_unannounced',confirmed=['EN'],role='instruction')

    vv=[dict(start=a,end=b,variant_key=k,label='LITA festive /6дней',price='RMB14800 standard;12850 EiM',source=DUL,
             proof='Собственная зимняя таблица2026; даты не распределены отдельно поBeijing/Shanghai.',date_scope='day_camp_window') for a,b,k in [('2026-12-19','2026-12-24','dec19'),('2026-12-26','2026-12-31','dec26')]]
    emit('dulwich-lita-festive','EIMx / LITA · West End in a Week · Festive',
         'Китай','CHN','Beijing / Shanghai · конкретный campus выбранной недели уточнить',
         'general,art,languages','day','11–17',
         'Entirely English: песни, scripts, rehearsal и tutor feedback; нужен хороший EN comprehension/communication. Профессиональный сценический опыт не обязателен.',
         'Шесть дней как театральная компания: acting/voice/choreography → сцены → репетиции → live musical production. LITA сообщает опыт West End своих tutors; это собственное описание, не независимый мировой рейтинг лагеря. Indicative09–17; окончательный репертуар определяется командой.',
         '19–24 или26–31 декабря2026,6дней. Две даты не умножены на два города без campus allocation.',
         dict(year=2026,label='RMB14800 стандарт;12850 EiM student /6дней.',included='Театральное обучение; питание/материалы/страховка не установлены.',extras='Дорога, жильё родителей, гардероб и дополнительные сборы неизвестны.',deposit=unknown),
         'Day camp, ориентировочно09–17; собственного летнего/зимнего пансиона нет.',
         fit('later','Минимум11; Матвею8–9 вдекабре2026.'),fit('later','Минимум11; Оскару5–6 вдекабре2026.'),
         'Сильный тематический английский творческий вариант на будущий возраст; не отправляем в текущий семейный ICS.',
         [unknown,'Точный campus/день итогового показа и состав fee.'],[src('LITA возраст/даты/EN/стоимость/indicative hours',DUL)],status='published_2026',confirmed=['EN'],variants=vv)

    vv=[dict(start=a,end=b,variant_key=k,label='Parent-child /10дней9ночей',formats=['family'],price='IndicativeRMB40800; единица тарифа/цена семьи неизвестны',source=DUL,
             proof='Собственная зимняя таблица2026/27. Family format, не автономный детский пансион с6лет.') for a,b,k in [('2026-12-22','2026-12-31','dec22'),('2027-01-26','2027-02-04','jan26'),('2027-02-11','2027-02-20','feb11')]]
    emit('dulwich-finland-winter','EIMx / Funlink · Finland Winter Wonderland',
         'Финляндия','FIN','Helsinki → Rovaniemi → Northern Finland; оператор EIMx/Dulwich',
         'general,science,culture,sport,languages','family','6–17, преимущественно вместе с родителями',
         'English — основной язык, Chinese-speaking team support. Это прямое programme statement, не предположение по сайту.',
         'Heureka Science Centre, Design Museum/Design District, Oodi и посещениеUniversity of Helsinki → Arktikum/Arctic ecology → youth camp, huskies/reindeer, skiing/ice fishing/snowshoeing/Sámi culture. Университетский визит не означает академический курс университета. Погода/снег могут менять itinerary; родители и дети имеют отдельные элементы опыта.',
         '22–31 декабря2026;26января–4февраля и11–20февраля2027.10дней/9ночей; student-only только по отдельному согласованию.',
         dict(year=2027,season='2026/27',label='IndicativeRMB40800: единица тарифа не указана. Не умножаем на4 и не называем ценой всей семьи.',
              included='Проживание в программе, local transport, занятия и только meals, указанные itinerary.',extras='International И domestic Finnish flights и visa fees исключены. Северный переезд overnight train OR domestic flight, финальная логистика неизвестна: не считать авиаперелёт включённым вlocal transport. Страховка, winter clothes и дополнительные meals неизвестны.',deposit=unknown),
         '4-star hotel вHelsinki и youth camp на севере; тип комнаты/семейное размещение/ratio ещё не раскрыты. Родительский формат не равен independent boarding.',
         fit('candidate','Возраст подходит, в сопровождении родителей; подтвердить snow activity gates.'),fit('conditional','Для декабрьского выезда только после6лет; в2027 будет6–7. Зимняя одежда, snow activities и full family invoice отдельно.'),
         'Реальные зимние EN даты для семейного научно-культурного путешествия; полезный альтернативный трек к робототехнике, с непрозрачной пока единицей цены.',
         [unknown,'Цена на ребёнка/взрослого/семью, северный перелёт/поезд, комнаты/программа6лет, отказ при погодных изменениях.'],[src('Actual Finland winter schedule, main EN, family format и exclusions',DUL)],status='partial_2026_27',priority=['both','general'],confirmed=['EN'],variants=vv,role='camp_life',support=['ZH'])

    emit('ycis-shanghai-english','YCIS Shanghai · English Enrichment / STEAM',
         'Китай','CHN','Puxi/Hongqiao6–14 Y1–8; Pudong/Regency Park8–10 Y4–6',
         'general,languages,science,art','day','Puxi6–14 иY1–8; Pudong8–10 иY4–6; оба порога проверять',
         'English Enrichment/PBL literacy, поддержкаEAL и extension сильнымEN. Сеть описывает bilingual environment. Английские занятия подтверждены; язык каждого digital/STEAM блока и всей лагерной жизни отдельно не установлен.',
         'Language-focused project learning с art/music, digital technology/STEAM и service learning; обе двухнедельные сессии имеют похожее содержание. Это не отдельный подтверждённый robotics intensive. Общая network page разрешает всем детям2–18; не отменяет возраст/класс выбранного курса и не доказывает иностранный паспортный допуск.',
         'Архив22июня–3июля и6–17июля2026,09–14:30; deadline29мая прошёл.2027 не опубликован.',
         dict(year=2026,label='RMB10800/2недели /ребёнок; двое21600 при допуске вPuxi. Цена2027 неизвестна.',included='EN/PBL programme; meals/transport/insurance в этой карточке не раскрыты.',extras='Жильё семьи, поездка, bus/material fee и sibling discount уточнить.',deposit=unknown),
         'Только дневной; Pudong не младшая заменаPuxi.',fit('conditional','Подходящий возраст, но фактическийY1–8 либоY4–6 неизвестен.'),fit('unknown','Puxi минимум6 иY1–8; до6лет не проходит, класс неизвестен. Pudong8+ не подходит.'),
         'EN general/STEAM день при семейной поездке вShanghai; новый2027 набор и предметный язык ещё нужны.',
         [unknown,'Новый сезон/класс, teaching language STEAM, full invoice и daily lunch.'],[src('Две реальных Shanghai programme cards',YC),src('Network bilingual/open-to-all statement не заменяет course gate',YCI)],status='archive_next_unannounced',confirmed=['EN'],role='language_lessons')

    for slug,name,place,age,date,fee,programme in [
      ('ycis-beijing-vex','YCIS Beijing · VEX Robot Olympics & Sports','YCIS Beijing','8–13 иY4–9','22июня–1июля2026','RMB9500','VEX/robotics/coding вместе со sport; точная платформа и учебные часы не раскрыты.'),
      ('ywies-beijing-vexiq','YWIES Beijing · VEX IQ Summer Camp','YWIES Beijing','8–13 иG4–9','6–12июля2026','RMB13800/7дней','Пластиковые конструкции, robot building и software programming;08:30–15:30. Internal1000 и early1000 до30апреля архивны, суммирование скидок не доказано.'),
      ('ywies-tongxiang-vex','YWIES Tongxiang · VEX Competition Preparation','Tongxiang · Zhejiang','G4–12; возраст ночёвки не опубликован','28июня–5июля2026','Primary10960day/12100board; Secondary14660day/15280board RMB','Competition rules analysis → initial robot build → foundation programming к новомуVEX сезону. Описано1week, опубликованный период8календарных дней; дни занятий/приезда уточнить. Не обещает qualification вworld finals.')]:
        board=slug.endswith('tongxiang-vex')
        emit(slug,name,'Китай','CHN',place,'robotics,coding,engineering','day,boarding' if board else 'day',age,
             'Язык VEX-преподавания не назван в course card. English website и bilingual network не доказывают EN robotics; не входит в фильтр EN instruction.',
             programme,'Архив:'+date+'. Новый2027 набор/даты не объявлены; не перенесены в будущий календарь.',
             dict(year=2026,label=fee+'; тариф2027 неизвестен.',included='УчебнаяVEX программа. Tongxiang прямо external students same price; полный состав питания/boarding package не указан.' if board else 'УчебныйVEX курс; питание/материалы/insurance ещё уточнить.',extras='Дорога, жильё семьи/трансфер, устройства и личная экипировка не оценены.',deposit=unknown),
             'Day или школьный boarding; минимум ночёвки/rooms/night ratio не раскрыты.' if board else 'Дневной; летний школьный пансион не заявлен.',
             fit('unknown','Требуется конкретный школьныйY/G4+, возраст не заменяет класс.'),fit('unknown','G/Y4+ требует подтверждения; не считаем младшего допущенным по бренду.'),
             'СодержательнаяVEX возможность и путь подготовки к сезону; без установленного языка/класса и нового набора не готовая рекомендация обоим.',
             [unknown,'Actual VEX teaching language, класс/минимумboarding, hardware/ratio/2027dates.'],[src('Actual VEX programme/fee/grade cards',YC),src('Сеть bilingual: предметный язык отдельно',YCI)],status='archive_next_unannounced')

    emit('mandarininn-shanghai','Mandarin Inn · Bilingual Shanghai Culture Camp',
         'Китай','CHN','1280 Huaihai Middle Road · Xuhui · Shanghai',
         'general,languages,culture,art','day','8–12',
         'Fully bilingual English & Mandarin прямо в programme. Это культурно-языковой день, не английская робототехника.',
         'HSK2 beginners: городскойmap/orienteering, cooking/order food, festivals/craft/museum, Mandarin vlog/scrapbook/interview. Max12/week; weeklyThursday outing с bilingual staff1:6 и заявленной travel insurance. Friday showcase14:30–16. Website говорит4weeks total, но form перечисляет8недель внутри22июня–14августа; не выдаём их за новое2027 расписание.',
         'Архив22июня–14августа2026,09–16Пн–Пт;2027 не объявлен.',
         dict(year=2026,label='RMB3800/нед;7220/2,10260/3,12920/4. Второму5%, комбинация со скидками неизвестна; ранняя10% до3апреля истекла.',included='Материалы/workshops, weekly outing transport/entry, certificate/souvenir booklet; travel insurance outings поFAQ.',extras='Lunch не включён: cold packed lunch свой. Drop-off/pickup родителей, семейное жильё/дорога. Referral500course-credit не cash discount; missed days не переносятся.',deposit='Отмена/возврат/оплата не раскрыты в прочитанныхFAQ; новый договор2027 неизвестен.'),
         'Только дневной, lunch/drop-off родителей.',fit('candidate','8–10 в2026–27 входит8–12, нужен новый набор.'),fit('later','Минимум8, Оскару5–7 пока рано.'),
         'Билингвальная культурная неделя Матвею вShanghai; честно показаны обед и возрастная разница.',
         ['Новый2027 invoice/dates, конфликт4weeks/8weeks, отмена/состав страховки и иностранный intake.'],[src('Own bilingual8–12, fee, gear, lunch и outing rules',MI)],status='archive_next_unannounced',confirmed=['EN'],role='bilingual')

    for slug,name,age,programme,mat,osc in [
      ('tinycode-scratch','Scratch Game Design','6–8','Scratch game: loops/events/conditionals + Google Teachable Machine; итог playable game.',fit('conditional','Только пока8, после9 верхний порог нарушен; actualDOB/новыйсезон.'),fit('conditional','После6лет входит6–8; для2027 новый сезон не объявлен.')),
      ('tinycode-robot','AI & Robotics Lab','7–11','micro:bit CreateAI gesture model + mBot2 navigation/commands. Всё robot hardware приносит instructor, не обещано как подарок.',fit('candidate','Возраст входит7–11; новый сезон/предметный уровень уточнить.'),fit('conditional','Только после7-летия в2027; до него7+ не выполнено.')),
      ('tinycode-games','Roblox / Minecraft Game Coding','Body8–12; FAQ8–10 — верхний порог конфликтует','Два альтернативных курса: Roblox Studio Obby/scripts + AI Code Assist, ИЛИ Minecraft Education/MakeCode quest сNPC/events/AIagents. Один10h пакет не означает оба курса.',fit('candidate','8–10 находится внутри обоих возрастных вариантов.'),fit('later','Минимум8; Оскару6–7 рано.')),
      ('tinycode-ai','Python & AI / AI Vibe Coding','10+','Два альтернативных курса: Python variables/functions/loops/data + ChatGPT API/chatbot/data project; ИЛИ Replit/Lovable prompts/debug/refine/published application. Это применениеAI, не обучение собственнойLLM.',fit('conditional','После10-летия в2027; пока9 минимум10 не выполнен.'),fit('later','Минимум10.'))]:
        emit(slug,'Tiny Code Hong Kong · '+name,'Гонконг','HKG','At your home · Hong Kong; временное жильё/район согласовать',
             'coding,ai,robotics' if slug=='tinycode-robot' else 'coding,ai,games','day',age,
             'English Instruction прямо в10h schedule. Частный преподаватель1:1, либо до3детей одного согласованного курса.',
             programme+'5дней×2h; project + parent report + completion certificate +16-class roadmap. Roadmap не включает16бесплатных занятий и certificate не международная награда.',
             'Архив:любаяПн–Пт неделя15июня–28августа2026, family-coordinated hours. Новый2027 календарь не объявлен; не создаём вымышленных weeklyICS.',
             dict(year=2026,label='HKD5280/1ребёнок10h;3432 EACH при2–3детях вобщей сессии, двое6864. Согласовать разный возраст/курс; два индивидуальных курса10560.',
                  included='10h English private instruction; толькоRoboticsLab all hardware предоставляется. Итог project/report/certificate/roadmap.',extras='СвойMac/Windows иChrome; Roblox Studio/Minecraft Education для соответствующего курса. Лицензии/API/AI subscription иtemporary home visit/insurance не оценены.15%referral не совмещено автоматически со35%group.',
                  deposit='Own termsApril2026:полная оплата; послеenrolment/full payment refunds/transfers нет. Reschedule7days notice/emergency approval, максимум1class/month; T8/Black Rainin-home переносится. Новые2027 terms отдельно.'),
             'У семьи дома2h/день, без supervised full day/питания/пансиона; условия допуска вhotel/rental проверить.',mat,osc,
             'Точный частныйEN технический формат для семейной поездки; разные возрастные предметы и полный день не смешаны.',
             ['2027 schedule/full fee, точнаягруппа/возраст, нужныйlaptop/accounts/AI paidusage, временныйадрес/insurance/contract.'],
             [src('Actual ages/curriculum/hardware/English10h/each fee',TC),src('OwnApril2026 refund/weather/payment terms',TCT)],status='archive_next_unannounced',confirmed=['EN'],role='instruction')

    camps=[
      ('harrow-hk-ecobot','EcoBot Patrol · Mission Green City','Гонконг','HKG','AISL Harrow Hong Kong ·38 Tsing Ying Rd,Tuen Mun','6–8',8980,'2026-12-24','ecobot-patrol-mission-green-city',
       '4дня:motors/gears/sensors/pulleys, tablet blockcoding → waste sorting/wildlife/cleaning/transport missions → build/test/debug/present. Exact number completed зависит отpace; namedrobotkit и gift не заявлены.',fit('conditional','Только если ещё8 на выбранные дни; после9 максимум8 не выполнен.'),fit('conditional','Нужно6лет на21декабря; по2020году exactDOB неизвестен.')),
      ('harrow-hk-sleigh','Santa’s Sleigh Lab','Гонконг','HKG','AISL Harrow Hong Kong ·38 Tsing Ying Rd,Tuen Mun','9–12',8980,'2026-12-24','santa-s-sleigh-lab',
       '4дня:force/friction/balance/stability/energy → прототип deliveryvehicle → design/test/improve → внутренняяReindeer Racing Challenge и presentation. Platform/coding module не назван, это engineering, не автоматическиAI/VEX.',fit('conditional','После9лет подходит; basicEN followinstructions нужен.'),fit('later','Минимум9.')),
      ('harrow-guangzhou-auto','Future Automotive Construction Academy','Китай','CHN','AISL Harrow Guangzhou ·23 Huanxin North Rd,Huangpu','8–13',12500,'2026-12-26','future-automotive-construction-academy',
       '5.5дняresidential:assemble electric kart/chassis/steering/battery/motor → trial/improve → F1-inspired sponsor/brand/teamroles/business strategy → ConstructorsGrandPrix. Это внутренний challenge, неofficialF1 partnership или worldroboticsqualification.',fit('candidate','8–9 вдекабре2026 входит8–13.'),fit('later','Минимум8.')),
      ('harrow-myoko-ski','Myoko Ski Winter Camp','Япония','JPN','Myoko ·Suginohara/Akakura Kanko ·Youth Nature House','10–16',23800,'2026-12-26','myoko-ski-winter-camp',
       '6дней/5ночей (detail5.5day):four mornings2.5–3h ski/snowboard lessons byMyokoSnowSports, snowadventures/Jigokudani monkey ecology/culture. WMA-based6–8h firstaid workshop; заявленныйBasicFirstAid/CPR certificate толькопослеassessment, issuer/recognition отдельно. Staffratio1:5 заявлен оператором, не independentinspection.',fit('later','Вдекабре2026 максимум9, минимум10 ещёне выполнен.'),fit('later','Минимум10.'))]
    for slug,name,country,iso,place,age,fee,end,key,programme,mat,osc in camps:
        boarding=iso=='CHN' or iso=='JPN';ski=iso=='JPN';u=AO+key
        cancellation=('Overseasprogramme:с1октября2026fees non-refundable, bookingchanges не предлагаются.' if ski else 'HK/Mainland:1–31октября2026 возврат40% с4%processing deduction, с1ноябряnon-refundable; одинchange до1ноября втомжепериоде/subjectavailability. База4%deduction требуетinvoice, не выводим автоматически36%или38.4%.')
        emit(slug,'AISL Outdoor / Harrow · '+name,country,iso,place,
             'general,sport,culture' if ski else 'engineering,entrepreneurship' if boarding else 'robotics,coding,engineering' if 'ecobot' in slug else 'engineering,science',
             'boarding' if boarding else 'day',age,
             'Camp Details прямо English. Sleigh требуетbasicEN. Это language statement курса; свобода мест/иностранный индивидуальный приём отдельно.',
             programme,
             '21–'+end[-2:]+'декабря2026. Structured offer InStock/variantavailable=true на дату проверки; текстовыйSoldout входит в шаблон. Это не гарантия принятой заявки/остатка мест.',
             dict(year=2026,label='HKD'+str(fee)+' за указаннуюсмену,tax included. '+('Два разныхдневныхкурсаEcoBot/Sleigh суммарно17960 до семейнойдороги/жилья.' if not boarding else ''),
                  included=('5ночей/fullmeals,4ski/snowboard sessions,lifts,rentalboots/skis/poles/helmet,afternoon/eveningprogramme,monkeyexcursion,returnNarita/Hanedatransfer/Tokyoescort,firstaid/materials.' if ski else 'Materials,allactivities/excursions,performance report/certificate,school accommodation,3meals/snacks иPublicLiabilityInsurance.' if boarding else 'Materials,allactivities/excursions,performance report/certificate,lunches/snacks.'),
                  extras=('Flights,personal travel/wintersports/medicalinsurance,skiwear/thermals/gloves/goggles,extra meals,pocketmoney,visas,medical/evacuationcosts. Fullclothingbuy/rentbudgetнеизвестен.' if ski else 'Трансферклагерю/flights/visa/personaltravelinsurance исключены. Familylodgingдляday отдельно; boarding rooms/medical cover/gear extras неизвестны.'),
                  deposit='Полнаяоплатаприenrolment,non-transferablebooking.7daycooling-off закончился30сентября2026; не обещаемего5октября. '+cancellation+' Приотменеоператоромнедоборагруппыfullrefund; погодная/force-majeure отменапоpolicyбезrefund. Localemergencyphone обязателен.'),
             'YouthNatureHouse5ночей,rooms/gender/nightcareподробностинеизвестны;Staff1:5ownclaim.' if ski else 'HarrowGuangzhouпансион,nightrooms/ratioнеустановлены.' if boarding else 'Day09–16; семейное жильё/дневнойdropoff отдельно.',
             mat,osc,
             'Точный зимнийEN технический/тематический курс с реальным пакетом и строгой отменой; '+('будущийвозрастобоим, исключёнтекущийfamilyICS.' if ski else 'дляразныхдетейразныеминимумы икампусы.'),
             ['Иностранный intake/DOB/места/localemergencyphone/окончательныйinvoice,contractexceptions,gear/insurance/ratio/rooms; booking не создан.'],
             [src('Actualwinterprogramme dates/language/fee/package/ownpublicstock',u),src('Actualwinter2026refund/change/emergency policy',POL)],status='published_2026',confirmed=['EN'],
             variants=[dict(start='2026-12-21',end=end,variant_key='winter',label=name,price='HKD'+str(fee),source=u,
                           availability=dict(status='listed_available',label='Ownpublicvariantavailable=true; зачисление/места отдельно'),
                           date_scope='camp_session' if boarding else 'day_camp_window',proof='Own2026product card/date/age/English/inclusions; dates not2027.')])

    emit('tc-city-ambassador','TC Time Walk · Junior City Ambassador',
         'Тайвань','TWN','Taichung old town ·5дней4ночи','general,culture,languages,entrepreneurship','boarding','9–15; incomingGrade3–incomingGrade10, эквивалент класса уточнить',
         'EN & Mandarin bilingual, прямо НЕfull-Englishcourse. Observation/interviews/foreigntravellerguiding вEN; уровень групп определяется английским. ДлябезMandarinchildren критическое сопровождение ещё нужно уточнить.',
         'Observeoldarchitecture → market/cooking/ESG → fieldinterviews/camera → storytelling/speechbodylanguage → ребёнокведётродителейпоучасткумаршрута. Own2026staffforeignguide1:7task идругой1:1task неoverallratio. Publictourismbureauguidance не independentcampqualityranking. Internalbadge/certificate не международная победа.',
         '2027 pre-booking объявлен, точныедаты/полныйfeeпокаНЕобъявлены. Архив22–26августа2026неперенесёнв2027ICS.',
         dict(year=2026,label='АрхивstandardNT20900,early18999до1августа,two-person17500EACH,subsidy12000толькоподокументам.2027ценыunknown;необещаемстаруюскидку.',included='Архив4youthhostelnights,4meals/day,materials/craft/localtransport,accident/travelinsurance,programme/record/certificate.',extras='ПоездкадоTaichung,insuranceextent/gear/new2027inclusionsнеустановлены.',deposit='2027NT1000holddeposit; послеобъявленияцены7днейнаотказсfullrefund. Поздняяотмена/остаток/входитлидепозитвfeeнепоказаны;депозитНЕполнаястоимость.'),
         'Архивyouthhostel4ночи;campnightrooms/ratio/nightstaff2027неизвестны.',
         fit('conditional','9–10в2027подходитвозраст;actualincominggrade/Chinesecomprehension/boardingготовностьещёнеизвестны.'),fit('later','Минимум9;Оскару6–7рано.'),
         'ТайваньскийкультурныйпредпринимательскийтрекМатвею;покаdeposit-only2027иEN/ZH,неанглийскийroboticsпансион.',
         ['Actual2027dates/invoice/gradeequivalence/Englishcriticalsupport/hostel/refund/foreignindividualintake.'],
         [src('OwnENoverview9–15/5days4nights',CITY+'en'),src('Actual2027announcement/refundable1000deposit',CITY+'blog/junior-city-ambassador-camp-taichung'),src('Archive2026curriculum/fullfee/package/age',CITY+'pro-courses/summercamp')],status='partial_2027',confirmed=['EN'],role='bilingual')

    rows=[
      ('jasmine-build','AXC · Block Builders Academy · Build It!','2–4','2027-07-05','2027-07-09',JG+'%E9%BA%A5%E5%A1%8A%E7%87%9F/%E5%86%92%E9%9A%AA%E5%AD%B8%E9%99%A2/',
       'engineering,art,games','Paper/recycledmaterial/wood/tape:build wearable/room-scaleMinecraft-inspiredobjects,prototype/test/improve. Не Minecraft coding;computer/gameexperience ненужны. Миниобществоjobs/campcurrency,physicalgames/quiettime.',
       'English-ledtasks,foreignTAиChinese-speakingteachers; детиестественноEN/ZH. Правилаобъясняюттак,чтобыкаждыйпонял. КритическаяEN-onlyподдержканаплощадкетребуетпроверки.'),
      ('jasmine-shop','AXC · Jasmine Shop Opens!','4–7','2027-07-12','2027-07-16',JG+'%E5%B7%A5%E4%BD%9C%E4%B8%96%E7%95%8C/',
       'entrepreneurship,maths,art','Товары/pricing/inventory/cashier/queues/service/accounts:настоящиепокупатели—детидругойсмены,непубличныеродители. Personalwagesиshoprevenueразные,итограспределяютсовместно. Не roboticsкурс.',
       'OwncourseFAQНЕall-English:контрфразынаEN,сложныеpricing/inventory/problemsобъясняютсянаChinese. ОбщийheadlineEnglish-ledнеобещаетENвсейбизнесдискуссии.'),
      ('jasmine-discovery','AXC · Discovery · Field & Studio','4–7','2027-07-19','2027-07-23',JG+'%E7%99%BC%E7%8F%BE%E5%AE%B6/',
       'engineering,science,art','NTUEstudio/NTUcampusfield:наблюдатьobject/users/materials → proposal →prototype →датьдругомупроверить →переделать. Основныематериалыбесплатны;minisocietyjobs/currency. Own3foreignteachers/classplusbilingualstaff,не24/7boardingratio.',
       'OwnFAQ:corequestions/taskinstructions/toolsнаEN;правила,meetings/conflicts/dailyreflectionнаChinese. НеполныйENprogramme;поддержкасемьеENподтверждена.'),
      ('jasmine-micro','AXC · Microverse Research Station','2–4','2027-08-02','2027-08-06',JG+'%E9%A1%AF%E5%BE%AE%E7%87%9F/',
       'science,engineering','Пятьднейодинresearchquestion:collectwater →ownmicroscope/focus/wetslide →справедливоесравнение/count →test/report. Ownmicroscopeкаждому,5детейнаworktable;этонеoverallstaffratio. Нельзяизтакогонаблюдениязаключатьwaterdrinkingsafety. Нужныrepeatableevidence/limitations.',
       'Microscopeinstructions/comparisonphrasesнаEN;criticalrules/faircountdecision/reflectionнаChinese. НикакогообещанияполностьюENнаучныхдискуссий;ownfamilyENsupportесть.')]
    for slug,name,grade,start,end,u,themes,programme,language in rows:
        p=emit(slug,'Jasmine Garden · '+name,'Тайвань','TWN','National Taipei University of Education ·Da’an,Taipei; boardingnearTaipei101',
             themes,'day,boarding','Currentgrade'+grade+' НАДАТУРЕГИСТРАЦИИ, не risinggrade/возраст; эквивалентшколысогласовать',
             language+' ENregistration/briefing/emergencyparentcontactесть;китайскийнеизвестенсемье.',programme,
             start+'–'+end+',5дней09–17;check-in08–09.2027registrationopenowncalendar; отдельныеpageостатки«ценавоктябре/waitlist»противновойтаблицы—меставсёравнонеподтверждены.',
             dict(year=2027,label='NT13800day; +4nightsNT6000 =19800 сboarding, неfullboard. ФормакамповыходеждаNT300/штукаотдельно.',
                  included='Lunch/materials/insuranceпоcoursepages. Пакетoptionalhostel4nightsвключаетbreakfast, НЕdinner.',
                  extras='Campclothes300/item (ownoldshirtmayreuse);latepickup17–18:30NT1000/wholecamp,ad-hoc400/occasionfirstfree. Dinner/pocketmoney/travel/airports/dailytransportещёнеоценены. Двеодинаковыепрограммыдвоим27600dayили39600boardдоclothes/ужинов; допускобоимнеустановлен.',
                  deposit='NT800offсо2сменытогожеребёнка,discountsнеstack/earlybirddatesнеобъявлены. Refund/paymentcontractвsharedformнепрочитан/непринят;служебныйостатокwaitlistнеобъявленрешённым.'),
             'Dayилиoptional4nightsbackpackhostelnearTaipei101,before/afterhandover/rooms/nightstaffнеизвестны. Campusуниверситетанеозначаетuniversitycampoperator.',
             fit('conditional','НуженactualcurrentGrade'+grade+';невыводимклассиз2017года. Chineseсложныхобсуждений/возможностьENпереводасогласовать.'),
             fit('unknown','Currentgrade'+grade+'неизвестен;2017/2020годнеподтверждаетшкольныйкласс. Необещаемэтотпансионмладшему.'),
             'Точные2027даты/базоваяцена ипрактическийтрек;ENчастично,Chineseвсложныхблоках,grade/ужиныограничиваютготовностьрекомендации.',
             ['Currentgradeequivalence/полноеENсопровождениекитайскихобсуждений,foreignpassportintake/rooms/nightcare/страховка/refund/fullinvoice/места.'],
             [src('Course-specific2027curriculum/language/lunch/gear',u),src('Actual9sessioncalendar/fees/grades/boarding',JC),src('OverseasENsupport/teacher-vs-peerlanguage/2027table',JGEN)],
             status='partial_2027',confirmed=['EN'],role='partial_bilingual',support=['EN'],variants=[dict(start=start,end=end,variant_key='summer',label=name,price='NT13800day /19800board beforeextras',source=JC,date_scope='day_camp_window',attendance_weekdays=['MO','TU','WE','TH','FR'],proof='Own2027tableandcoursepage. Currentgradeatregistration,English-ledpartswithChinesediscussion;optionalboardingnotfullboard.')])

    vv=[]
    for start,end,k,label,grade,price,formats in [
      ('2027-07-05','2027-07-09','time','JourneyThroughTime','3–6','NT14800day /20800optionalboard',['day','boarding']),
      ('2027-07-12','2027-07-16','campus','WildLivingCampus','2–4','NT15800 includes1night',['day','boarding']),
      ('2027-07-19','2027-07-23','water','InvisibleCityWater','2–6','NT19800 includes4nights, lunch/dinner/transitextra',['boarding']),
      ('2027-07-26','2027-07-30','rail','FiveDaysByRail','3–7','NT16800includes1night;optional3nights4500,total21300',['day','boarding']),
      ('2027-08-02','2027-08-06','wild','WildLivingBackcountry','4–7','NT19800includes4nights,packageallincluded claim,confirmmealcover',['boarding'])]:
        vv.append(dict(start=start,end=end,variant_key=k,label=label,age='Currentgrade'+grade+'atregistration',price=price,formats=formats,source=JC,
                       family_fit=dict(matvey=dict(status='unknown',detail='Grade'+grade+'иMandarin comprehensionнеизвестны.'),oscar=dict(status='unknown',detail='Grade'+grade+'иMandarin comprehensionнеизвестны.')),
                       proof='Own2027ENandZHtables,explicitnotfullEnglish;includednightsnotchargedtwice. Условияmeal/transportvarybysession.'))
    emit('jasmine-nola','Jasmine Garden · NOLA Real-World Adventure',
         'Тайвань','TWN','Taipei/NTUEmeetup;PinglinHuliaotan/railTaipei–Ruifang; actualcampvenuevaries',
         'general,culture,science,sport','day,boarding','CurrentGrade2–7, отдельныегруппы2–4/2–6/3–6/3–7/4–7',
         'Mandarin-first. ENessentialsupport:designatedcontacteverysession иparentemergencyENline. Это EN SUPPORT, неанглийскоепреподавание; требуетсяbasicMandarinпониматьобычныйразговор/безопасность.',
         'Пятьразныхприключенческихвыборов:archaeology/history/city/Hsinchusciencepark;campus→outdoorfire/living;urbanwaterinvestigation;railwayplanning/tickets/independence;four-nightwildcamp. Неroboticsкурс. NOLA24minimumforminggroup,overalluppercapнеустановлен,ownleadersabout1:6–8. Самостоятельностьсогласовать.',
         'Пятьточных2027смен5дней;дваодновременныхкурсаодномуребёнкунельзясовмещать. Boardingнеуровеньсложности.',
         dict(year=2027,label='NT14800–19800activity. Time+6000board=20800;Rail16800+4500=21300;Water19800already4nights—НЕдобавлятьещё6000.',
              included='Campus1night;Rail1nightRuifang;Water4nightFormosa101hostel/breakfast;Wild4nightHuliaotan/packageallincluded claim. Питание/дорогазависятоткурса.',
              extras='Cityhostelbreakfastincluded,dinnerexcluded;Waterlunch+dinnerизpocketmoney,publictransitEasyCardсамостоятельно (2dayscoachincluded). Railmeals/faresуточнить. Gear/rainwear/campclothes/airportsдополнительно. Wildnightroomtypesunknown.',
              deposit='NT800samechildadditionalcamp,nostacking/earlybirdunannounced. Срокиоплаты/отмена/страховка/весьcontractнеизвестны.'),
         'Частьdayсвключённой1ночью;часть4nightboarding. Дополнительныеcitynightsschoolhostelнешкольныйпансион. Handover/nightcare/roomsнеустановлены.',
         fit('unknown','Фактическийcurrentgrade/Mandarinнеизвестны;EN/ES/RUсемьиненазываемMandarinprepared.'),fit('unknown','Currentgrade2+иbasicMandarinнеустановлены;необещаемдопускмладшему.'),
         'РеальныеобщиетематическиеТайваньскиесмены;поканеосновнойENмаршрутдлясемьи,ноEnglishsupportвыделенотдельно.',
         ['BasicMandarin/gradeequivalence/foreignintake/independence,nightcare/gear/insurance/refund/mealtransportcompletebudget.'],
         [src('Actual2027ninecourses/currentgrades/format/fees/mealextras',JC),src('TeacherMandarinvsessentialEnglishsupport/overseasintake',JGEN)],status='published_2027',support=['EN'],role='support_only',variants=vv)

    u=JG+'%E9%BA%A5%E5%A1%8A%E7%87%9F/%E5%AF%A6%E9%AB%94%E5%B7%A5%E5%9D%8A/'
    emit('jasmine-winter-block','Jasmine Garden · AXC Minecraft Physical Workshop · Winter',
         'Тайвань','TWN','National Taipei University of Education ·Da’an,Taipei',
         'engineering,art,games','day','CurrentGrade1–5 на дату регистрации; классы детей неизвестны',
         'English-led tasks с foreign teachers/TA и Chinese-speaking staff; среда EN/ZH. Правила должны быть понятны каждому. EN-only сопровождение китайских объяснений ещё нужно подтвердить.',
         'Два дня физических Minecraft-inspired построек: бумага/коробки/дерево → вырезать/собрать → проверить размеры входа/инструмента → изменить общий сценический мир. Кодирование не преподают; компьютер/планшет и Minecraft опыт не нужны. Game, quiet time, physical activity и миниобщество дополняют workshop. Max30 — размер смены, не staff ratio.',
         '21–22 января2027, четверг/пятница09–17, приём08–09. Регистрация объявлена открытой; early bird до16октября2026 — срок скидки, не последний срок регистрации.',
         dict(year=2027,label='NT6800/2дня; earlyNT6300 до16октября2026. Двоим13600/12600 до одежды и при подтверждённом допуске.',
              included='Workshop; lunch и insurance прямо включены. Материалы предоставляет программа; полный состав страхового покрытия уточнить.',
              extras='Camp shirtNT300/штука, прежнюю можно использовать. Если каждому нужна одна новая:14200standard/13200early семье, до дороги/жилья. Latepickup17–18:30 ad-hocNT400, первый случай в смене бесплатно; двухдневныйwholecamp lateplan не продаётся. Пансиона не заявлено.',
              deposit='SamechildsecondsessionNT800off, скидки не суммируются. Договор отмены/аванс/оплата не прочитаны в форме; earlybird не reservation.'),
         'Только дневной; родительские pickup/ночное жильё отдельно.',
         fit('conditional','Нужен фактическийcurrentGrade1–5; возраст2017 не заменяет школьный класс. Язык сложных объяснений уточнить.'),
         fit('unknown','МинимумGrade1 на дату регистрации; класс не известен. Не утверждаем допуск по2020году.'),
         'Конкретная младшая зимняя maker-смена с новым2027 прайсом; интересный старт при семейной поездке, после проверки класса и EN поддержки.',
         ['Классы/DOB/EN critical explanations/иностранный intake/места, полный invoice/insurance/refund/одежда/родительский pickup.'],
         [src('ActualJan2027two-day physicalbuilding/Grade1–5/6800early6300/lunchinsurance/gear',u),src('Overseasfamily English support',JGEN)],
         status='partial_2027',confirmed=['EN'],support=['EN'],role='partial_bilingual',
         variants=[dict(start='2027-01-21',end='2027-01-22',variant_key='winter',label='PhysicalWorkshop /2дня',price='NT6800;early6300до16October2026;shirt300extra',source=u,
                        date_scope='day_camp_window',attendance_weekdays=['TH','FR'],proof='OwnJan21–22/Grade1–5/fee/English-led+Chinese support. EarlybirdOct16notregistrationdeadline.')])

def extend_report_v102(report):
    report['shortlist'] += [
      dict(label='Зима2026 · технические курсы Гонконга / Гуанчжоу',slugs=['harrow-hk-ecobot','harrow-hk-sleigh','harrow-guangzhou-auto'],reason='EcoBot6–8 иSleigh9–12одновременно21–24декабря,одинHKcampus/EN/lunch/snacks;согласоватьDOB. Guangzhou8–13engineering+businessboard21–26декабряМатвею. Это семейныйредакционныйвыбор, невнешнийрейтинг/гарантиямест.'),
      dict(label='Тайвань2027 · английские задания, научный/предпринимательский трек',slugs=['jasmine-winter-block','jasmine-build','jasmine-micro','jasmine-discovery','jasmine-shop'],reason='Зима21–22Jan:physical makerG1–5/6800early6300доOct16 плюсshirt300. Четыре2027летниенедели13800day/19800hostelдоextras. Grade2–4/4–7НАдатурегистрации;Chineseвчастисложныхобсуждений/правил. Необещаемall-EnglishилидопускОскара;полныйENсопровождениемладшимнеустановлен.'),
      dict(label='Гонконг · частная английская техника в семейной поездке',slugs=['tinycode-robot','tinycode-scratch','tinycode-games','tinycode-ai'],reason='Robotics7–11/Scratch6–8/gamesbody8–12vsFAQ8–10/PythonAI10+.10hathome,неfulldayпансион. Цены5280single/3432EACH2–3kids, hardwareonlyRoboticsprovided. Покаархив2026иоченьстрогийrefund.'),
      dict(label='Зимнее семейное путешествие / культура на будущий возраст',slugs=['dulwich-finland-winter','tc-city-ambassador','harrow-myoko-ski','dulwich-lita-festive'],reason='Finland6–17primarilyparent-childтри2026–27окнаEN,но40800единицанеясна. Taiwan9–15bilingualdeposit-only2027. Myoko10–16иLITA11–17позжеобоим. Культура/sport/artдополняютtechnicaltrack,сертификатнеworldaward.')]
    report['gaps'] += [
      dict(country='Китай / Гонконг',iso='CHN',provider='v102 · предметный язык / фактический зимний прайс',detail='ПервыйdossiercoverageMainlandChinaиHK. YCIS/YWIESVEXarchive2026G/Y4+,teachlanguageunknown;Englishsite/bilingualnetworkнеENrobotics. HarrowwinterstockstructuredInStock/varianttrue,hiddenSoldouttemplatelabelнефактclosed. ОбщийwinterpolicycoolingoffendedSep30,HKMainlandOct40%refundminus4%fee,overseasOctnonrefundable.',next_action='Foreignpassportindividualintake/DOB/grades/stock/fullinvoice/rooms/gear/currentcontract,новые2027VEXseasons.',url=POL),
      dict(country='Тайвань',iso='TWN',provider='v102 · AXC/NOLA реальные2027 программы',detail='Ownactual2027fees13800–19800и9датпрочитаны. AXCENtaskcommands,ноshops/design/sciencecomplexdiscussionчастоChinese;NOLAMandarin-first+ENessentialcontact. Currentgradeatregistrationнеrisinggrade. Water4night19800alreadyincludeslodging,butlunch/dinner/transitextra;Railextra3night4500not4night6000. Некоторыеcoursepagelegacywaitlist/price-inOctoberостаткипротивtableopen.',next_action='ЧестныйENcriticalsupport/gradeequivalence/foreignintake/rooms/insurance/refund/invoice/stock; неprepayбезfinalfacts. TCcity1000depositnotfull2027fee/calendar.',url=JGEN),
      dict(country='Япония / Южная Корея / Тайвань',iso='JPN',provider='v102 · LTL2027 ограничения языкового трека',detail='Триcountryownpages2027bookingsopen7–17:KidsDay7–11withparents,Residence11–17,Homestay12–17,HalfDay7–17. ОсновныеклассыJapanese/Korean/Mandarin,Englishinterface/EnglishdoctorsнеproofENteachingorstaffsupport. GenericinclusionlistcopyдажеHalfDayconflictsnoafternoon/weekendprose. Noexact2027dates/fullpricefromselectedbody. НеaddedasENcampилиindependentboarding7+.',next_action='Countryactualweeklydates/fees/Englishstaffsupport/halfdaypackage/11+nightcare/insurance. Не переноситьlanguageclaimsмеждустранами.',url='https://ltl-school.com/summer-camps/'),
      dict(country='Сингапур',iso='SGP',provider='v102 · Kids DiscoveryWorks: содержание есть, даты/язык пока неполные',detail='OwnpublicportalBishanscheduleheadlineSep/Oct2026/fullandhalfday/lunchsnacksfull;LEGOSpikePrime/ScratchBattlebotsиRescueRoverscontent. Parsedbodynotactualdatedfee/sessiontable,Englishinstructionexplicitnotfound. Privateportal/login/cartнеиспользованы;20%deadlineAug31архив.',next_action='Собственныеdatedsessionprice/grade/ENteaching/invoice/gear/contracts;notnewbooking/calendarfrommarketingheadline.',url='https://parentportal.kidsdiscoveryworks.com/camp_program'),
      dict(country='Китай',iso='CHN',provider='v102 · ASEEDER CTD: поисковая карточка не полный сайт',detail='SearchprimarycachedCTDShanghaiJuly13–24/G1–9/English+bilingualTA; обеdirectEnglishиChineseURLsHTTP404/noactualbody. Неaddedfullprogrammeаудит/fee/2027датыизcachedsnippet;eligibilitypercentilesиoptionalhotelнужныactualcurrentcontract.',next_action='Рабочаяofficialcanonicalprogramme/CTDpartnership/currentcourses/admissiontest/fullfee/2027dates,неделатьзаявку.',url='https://www.seedasdan.com/en/ctd-offline-en/')]
