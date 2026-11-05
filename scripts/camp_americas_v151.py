"""Public 2026/27 technical day camps and carefully gated weekly programmes."""
from datetime import date,timedelta
from camp_europe_v148 import lesson,weekdays

CHECKED='2026-11-05'
SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
AI='https://aialabs.org/'
AIC=AI+'camps'
AIR=AI+'refund-policy'
AIW=AI+'waiver-policy'
HB='https://hollandbloorview.ca/services/programs-services/firstr-robotics-program-winter-2026'
HBD='https://hollandbloorview.ca/services/programs-services/robotics-holland-bloorview/program-description'
HOF='https://www.hofstra.edu/academics/ce/summer-camp/'
UNKNOWN=T('Основной язык занятий EN/ES/RU прямо не установлен. Англоязычный сайт и местонахождение в США / Канаде сами по себе не доказывают язык преподавания; закрепить английскую группу до брони.',
          'Idioma principal EN/ES/RU de clases sin establecer expresamente. Web inglesa y ubicación en EEUU / Canadá no acreditan por sí solas idioma de enseñanza; asegurar grupo en inglés antes de reservar.')
AI_REFUND=T('Camp / one-off: отмена за 14 и более дней — возврат за вычетом 6%; внутри 14 дней до начала — account credit. После начала возврата нет, за непосещённые сессии возможен credit; отдельные пропущенные дни не возвращают. Credit действует 2 года внутри семьи, не равен cash refund. При отмене оператором — полный refund без сбора или credit по выбору; внешние закрытия / погода — make-up либо credit. Действует версия договора при зачислении; договор не принимался.',
            'Camp / one-off: cancelación con 14 o más días — devolución menos 6%; dentro de 14 días antes del inicio — account credit. Después de empezar sin devolución, sesiones no asistidas pueden generar credit; días individuales perdidos no se reembolsan. Credit vale 2 años dentro de familia, no equivale a cash refund. Cancelación del operador: refund íntegro sin cargo o credit a elección; cierres externos / clima: make-up o credit. Rige versión del contrato al inscribirse; sin aceptar contrato.')
AI_CONFLICT=T('Карточки holiday и их публичные данные показывают USD 519 даже за один день; FAQ отдельно называет 159 / 259 / 349 / 499 за 1 / 2 / 3 / 5 дней. Care в карточке 65 / 160, FAQ 13 / 32 в день. Эти значения расходятся для коротких смен: нужен письменный счёт, меньшую цифру не выдаём за подтверждённую цену.',
              'Fichas holiday y sus datos públicos muestran USD 519 incluso por un día; FAQ indica aparte 159 / 259 / 349 / 499 por 1 / 2 / 3 / 5 días. Care en ficha 65 / 160, FAQ 13 / 32 diarios. Valores discrepan en sesiones cortas: se necesita factura escrita, sin presentar cifra menor como precio confirmado.')
AI_PROMO=T('Текущая ранняя цена указана до 31 декабря 2026. Четыре дня: USD 359 сейчас, regular 419 с 1 апреля; пять дней: 449 сейчас, regular 519 с 1 апреля. Промежуточные цены января–марта не выдумываем. 10% sibling заявлены на дополнительного ребёнка, но суммирование скидок действует лишь в объёме, который применит checkout. В смете раннюю цену не уменьшаем автоматически ещё на 10%.',
           'Precio anticipado actual hasta 31 de diciembre de 2026. Cuatro días: USD 359 ahora, regular 419 desde 1 de abril; cinco días: 449 ahora, regular 519 desde 1 de abril. Sin inventar precios intermedios de enero–marzo. 10% sibling anunciado para niño adicional, pero descuentos combinados solo según checkout. Presupuesto anticipado no se reduce automáticamente otro 10%.')
HB_GATE=T('Это рекреационная программа Holland Bloorview со специальным приёмом: до старта нужен formal diagnosis, возможна собственная поддержка 1:1; состояние семьи не предполагаем. Возраст проверяется на 31 декабря, год отсечения в описании не уточнён. Требуется индивидуальное решение о пригодности группы и приёме семьи из-за рубежа. Название FIRST не означает регистрацию команды в соревновании.',
          'Programa recreativo de Holland Bloorview con admisión especial: requiere formal diagnosis antes de empezar, posible apoyo propio 1:1; sin suponer situación de la familia. Edad a 31 de diciembre, año de corte sin precisar en descripción. Requiere decisión individual sobre adecuación al grupo y admisión familiar extranjera. Nombre FIRST no implica registrar equipo en competición.')
HOF_LIMIT=T('Описание программы проверено, точные смены и тарифы выбранного трека пока не удалось подтвердить. Опубликован общий сезон кампуса, но конкретные даты заезда и наличие мест ещё нужно получить у оператора.',
            'Descripción del programa verificada, sesiones y tarifas exactas del curso elegido aún sin confirmar. Temporada general del campus publicada, pero faltan fechas concretas y plazas por confirmar con operador.')

def src(title,url):return dict(title=title,url=url,checked=CHECKED)
def fit(status,ru,es):return dict(status=status,detail=T(ru,es))
def base(ident,slug,provider,country,iso,place,age,themes,formats):
    return dict(id=ident,slug=slug,provider=provider,country=country,iso=iso,place=place,age=age,
                themes=themes,formats=formats,language=UNKNOWN,confirmed_instruction_languages=[],
                programme='',timing=dict(status='partial_2027',label='',sessions=[],session_details=[]),
                price=dict(year=None,currency='',amount=None,unit='programme',label='',included='',extras='',deposit=''),
                accommodation='',family_fit={},editorial_reason='',shortlist=[],questions=[],sources=[],checked=CHECKED)

def ai_profile(ident,slug,provider,themes):
    p=base(ident,slug,provider,'США','USA','Magnolia · 3121 W Government Way Apt 1 · Seattle, WA 98199',
        '5–12',themes,['day'])
    p['family_fit']=dict(matvey=fit('candidate','Подходит 5–12; в 2027 старший поток 9–12. Реальный уровень после трёх лет соревнований, язык и место ещё согласовать.',
                                 'Compatible con 5–12; en 2027 grupo mayor 9–12. Acordar nivel real tras tres años compitiendo, idioma y plaza.'),
                         oscar=fit('candidate','Подходит 5–12; летом 2027 младший поток 5–8. Не обещаем одинаковую сложность проекта с Матвеем.',
                                   'Compatible con 5–12; verano 2027 grupo menor 5–8. Sin prometer misma complejidad de proyecto que Matvey.'))
    p['accommodation']=T('Дневной 09:00–15:00, без ночёвок. Magnolia — конкретная площадка; даты Bellevue не копируем из Seattle. До / после занятий и на выходных семья обеспечивает проживание и уход.',
                         'Diurno 09:00–15:00, sin pernocta. Magnolia es recinto concreto; fechas Bellevue no copiadas de Seattle. Familia organiza alojamiento y cuidado fuera de clases y fines de semana.')
    p['price'].update(currency='USD',deposit=AI_REFUND)
    p['shortlist']=['technical']
    p['questions']=[T('Подтвердить английский язык, иностранный самостоятельный приём, возрастную группу, сложность и места. Местный учебный турнир / showcase не международная медаль.',
                     'Confirmar inglés, admisión extranjera individual, grupo de edad, complejidad y plazas. Torneo educativo local / showcase no es medalla internacional.'),
                    T('Получить полный счёт: тариф именно выбранных дней, питание, care, taxes, страховка, применение sibling / ранней цены и условия отмены.',
                      'Obtener factura completa: tarifa de días elegidos, comida, care, taxes, seguro, aplicación de sibling / precio anticipado y cancelación.')]
    p['sources']=[src(T('Календарь 2026/27 и Summer 2027 · разные блоки', 'Calendario 2026/27 y Summer 2027 · bloques distintos'),AIC),
                  src(T('Refund / credit / скидки', 'Refund / credit / descuentos'),AIR),
                  src(T('Условия участия · только чтение', 'Condiciones de participación · solo lectura'),AIW)]
    return p

HOLIDAYS=[
 ('hero-tech-robotics-1111','2026-11-11','2026-11-11','Hero Tech Robotics',
  T('Спасательный робот с лебёдкой / подъёмником, движение по поисковому маршруту.', 'Robot de rescate con cabrestante / brazo elevador y ruta de búsqueda.')),
 ('battlebots-mini-tournament-1123','2026-11-23','2026-11-25','BattleBots Mini-Tournament',
  T('Конструирование арены и роботов для внутреннего мини-турнира, управление и стратегия. Это не отбор международной лиги.', 'Construcción de arena y robots para minitorneo interno, control y estrategia. No clasificatorio de liga internacional.')),
 ('winter-wonderland-robotics-1221','2026-12-21','2026-12-23','Winter Wonderland Robotics',
  T('Автоматический снегоочиститель, механические зимние модели, сенсоры и световые последовательности.', 'Quitanieves automático, modelos mecánicos de invierno, sensores y secuencias de luz.')),
 ('scrap-to-bot-challenge-1228','2026-12-28','2026-12-30','Scrap to Bot Challenge',
  T('Безопасные вторичные материалы, макетные платы и электроника для работающего робота.', 'Materiales reutilizados seguros, placas de prototipos y electrónica para robot funcional.')),
 ('future-city-innovators-0128','2027-01-28','2027-01-28','Future City Innovators',
  T('Городские инженерные задачи, прототипы и кодирование решений.', 'Problemas de ingeniería urbana, prototipos y programación de soluciones.'))]
GAMES=[
 ('game-design-world-builders-0215','2027-02-15','2027-02-19','World Builders Game Design',
  T('Игровые миры и логика для 6–12; пятилетним предложено механическое LEGO. Оскару 6–7 в 2027, конкретную цифровую группу подтвердить.', 'Mundos y lógica de juegos para 6–12; a niños de cinco se ofrece LEGO mecánico. Oscar 6–7 en 2027; confirmar grupo digital concreto.')),
 ('ultimate-game-design-ai-0412','2027-04-12','2027-04-16','Ultimate Game Design & AI',
  T('Старшие создают цифровые миры и компьютерных персонажей; младшим механическая инженерия. Возраст старшего AI-потока не установлен числом, Оскару AI-курс не обещан.', 'Mayores crean mundos digitales y personajes controlados por ordenador; menores ingeniería mecánica. Edad del grupo mayor de AI sin cifra, sin prometer curso AI para Oscar.'))]
SUMMER=[
 ('steam-launchpad-0622','2027-06-22','2027-06-25','STEAM Launchpad: The Innovator’s Bootcamp',359,
  ['engineering','coding','science'],T('Четыре дня: механика, кодирование, 3D-дизайн и науки; общий технический sampler.', 'Cuatro días: mecánica, programación, diseño 3D y ciencias; sampler técnico general.')),
 ('robo-olympics-0628','2027-06-28','2027-07-02','Robo-Olympics: Mechanics, Motors & Torque',449,
  ['robotics','engineering'],T('Моторы, передачи, баланс и робототехнические состязания внутри лагеря.', 'Motores, engranajes, equilibrio y retos robóticos internos del campamento.')),
 ('eco-tech-ocean-explorers-0706','2027-07-06','2027-07-09','Eco-Tech & Ocean Explorers',359,
  ['engineering','science'],T('Четырёхдневная инженерия и исследования экосистем; конкретный итоговый проект по возрасту.', 'Ingeniería de cuatro días y exploración de ecosistemas; proyecto final según edad.')),
 ('arcade-studio-0712','2027-07-12','2027-07-16','Arcade Studio: Retro & 2D Game Design',449,
  ['games','coding'],T('Ретро-игры, 2D-проектирование и игровая логика.', 'Juegos retro, diseño 2D y lógica de videojuegos.')),
 ('mad-scientist-flight-lab-0719','2027-07-19','2027-07-23','The Mad Scientist & Physics of Flight Lab',449,
  ['science','engineering'],T('Научные опыты и физика полёта с возрастными инженерными задачами.', 'Experimentos científicos y física del vuelo con retos de ingeniería por edad.')),
 ('tech-art-design-studio-0726','2027-07-26','2027-07-30','Tech-Art & 3D Print Design Studio',449,
  ['art','engineering'],T('Техническое творчество, 3D-дизайн и печать; личный готовый принтер в цену не заявлен.', 'Creatividad técnica, diseño e impresión 3D; sin impresora personal incluida en precio.')),
 ('masterminds-math-codes-0802','2027-08-02','2027-08-06','Masterminds: Math, Codes & Tech Escape Rooms',449,
  ['coding','science'],T('Математика, шифры и технологические задачи escape room.', 'Matemáticas, códigos y retos tecnológicos de escape room.')),
 ('smart-cities-ai-sensors-0809','2027-08-09','2027-08-13','Smart Cities, AI & Autonomous Sensors',449,
  ['ai','coding','engineering'],T('Модели умных городов, AI и автономные датчики; задания младшей и старшей групп отличаются.', 'Modelos de ciudades inteligentes, AI y sensores autónomos; retos distintos para grupos menor y mayor.')),
 ('worlds-game-creators-0816','2027-08-16','2027-08-20','3D Worlds & Game Creators',None,
  ['games','coding'],T('Программа и даты анонсированы; карточка прямо говорит registration opens soon, тариф отсутствует.', 'Programa y fechas anunciados; ficha dice expresamente registration opens soon, sin tarifa.')),
 ('maker-expo-capstone-0823','2027-08-23','2027-08-27','Magnolia Maker Expo: The Young Entrepreneur & Capstone',449,
  ['engineering','entrepreneurship'],T('Итоговый проект и презентация идеи / предпринимательства; внутренний showcase лагеря, не мировая технологическая выставка.', 'Proyecto final y presentación de idea / emprendimiento; showcase interno del campamento, no feria tecnológica mundial.'))]

def add_ai_session(p,key,a,b,title,programme,price,themes=None):
    url=AI+'camps/magnolia-'+key+'-full'
    v=dict(start=a,end=b,label=title,place=p['place'],source=url,formats=['day'],date_scope='session_days',
           price=price,programme=programme,sessions=[lesson(day,'09:00','15:00','America/Los_Angeles',title) for day in weekdays(a,b)])
    if themes:v['themes']=themes
    p['timing']['sessions'].append([a,b]);p['timing']['session_details'].append(v)
    p['sources'].append(src(title+' · '+T('даты, программа и публичный тариф','fechas, programa y tarifa pública'),url))
    return v

def build_profiles():
    result=[]
    p=ai_profile('CP1174','aiara-holiday-robotics-2026-27','AI & Robotics Academy · Magnolia Holiday Robotics',['robotics','coding','engineering'])
    p['timing'].update(status='published_2026_27',label=T('Пять отдельных наборов ноября 2026–января 2027, от одного до трёх дней. Даты взяты с конкретных публичных карточек, не со школьного календаря по догадке.',
        'Cinco convocatorias separadas de noviembre de 2026 a enero de 2027, de uno a tres días. Fechas de fichas públicas concretas, sin deducirlas de calendario escolar.'))
    p['programme']=T('Практические роботы, электроника и инженерия 09–15. Группы holiday 5–7 / 8–12; материалы, учебные роботы и ноутбуки заявлены оператором. Сертификат / внутренний мини-турнир не международный результат.',
        'Robots prácticos, electrónica e ingeniería 09–15. Grupos holiday 5–7 / 8–12; materiales, robots educativos y portátiles declarados por operador. Certificado / minitorneo interno no es resultado internacional.')
    p['price'].update(year=2026,label=AI_CONFLICT,included=T('Материалы, учебные киты / ноутбуки, футболка, pizza и snacks. Свежий FAQ уточняет: pizza / snacks не обязательно полноценный обед, lunchbox при необходимости свой.',
        'Materiales, kits educativos / portátiles, camiseta, pizza y snacks. FAQ actual precisa: pizza / snacks no son necesariamente comida completa, lunchbox propio si hace falta.'),extras=T('Family travel, жильё, полноценный обед, taxes / страховка и корректная цена care отдельно. After-school transport за 160 / месяц не цена доставки на каникулы.',
        'Family travel, alojamiento, comida completa, taxes / seguro y precio correcto de care aparte. After-school transport de 160 / mes no es precio de transporte de vacaciones.'))
    for key,a,b,title,programme in HOLIDAYS:add_ai_session(p,key,a,b,title,programme,AI_CONFLICT)
    p['editorial_reason']=T('Ближайшие роботы обоим по возрасту; язык и конфликт цены не закрыты, готовую бронь или мировой рейтинг не заявляем.',
        'Robótica próxima compatible por edad con ambos; idioma y conflicto de precio pendientes, sin afirmar reserva lista ni ranking mundial.')
    result.append(p)
    p=ai_profile('CP1175','aiara-game-ai-breaks-2027','AI & Robotics Academy · Magnolia Game Design / AI Breaks',['games','coding','ai'])
    p['timing'].update(status='published_2027',label=T('Две разные пятидневные недели 15–19 февраля и 12–16 апреля 2027, 09–15. Не один непрерывный февраль–апрельский лагерь.',
        'Dos semanas distintas de cinco días 15–19 de febrero y 12–16 de abril de 2027, 09–15. No campamento continuo de febrero a abril.'))
    p['programme']=T('Игровая логика / создание миров и отдельная весенняя тема AI. Старший и младший проекты различаются, точный цифровой допуск Оскара и язык подтвердить.',
        'Lógica de juegos / creación de mundos y tema separado de AI en primavera. Proyectos mayor y menor distintos; confirmar admisión digital exacta de Oscar e idioma.')
    p['price'].update(year=2027,label=AI_CONFLICT,included=result[0]['price']['included'],extras=result[0]['price']['extras'])
    for key,a,b,title,programme in GAMES:add_ai_session(p,key,a,b,title,programme,AI_CONFLICT)
    p['editorial_reason']=T('Кандидат по возрасту обоим с разделением реального игрового / AI содержания младшей и старшей групп.',
        'Candidato por edad para ambos, distinguiendo contenido real de videojuegos / AI de grupos menor y mayor.')
    result.append(p)
    p=ai_profile('CP1176','aiara-summer-magnolia-2027','AI & Robotics Academy · Magnolia Summer 2027',['robotics','coding','ai','games','engineering','science'])
    p['timing'].update(status='published_2027',label=T('Десять отдельных недель 22 июня–27 августа 2027: 22–25 июня и 6–9 июля по 4 дня; остальные по 5. Все 48 дней 09–15, без выходных и без 5 июля. Неделя 16–20 августа объявлена, регистрация ещё не открыта.',
        'Diez semanas separadas 22 de junio–27 de agosto de 2027: 22–25 de junio y 6–9 de julio de 4 días; demás de 5. Los 48 días 09–15, sin fines de semana ni 5 de julio. Semana 16–20 de agosto anunciada, inscripción aún sin abrir.'))
    p['programme']=T('Утро 09–12: отдельные потоки 5–8 / 9–12; 12–13 перерыв, 13–15 общий lab. Каждая неделя самостоятельна. Robot Olympics и Maker Expo — внутренние учебные форматы, не отбор на чемпионат или публичная мировая выставка.',
        'Mañana 09–12: grupos separados 5–8 / 9–12; pausa 12–13, lab compartido 13–15. Cada semana independiente. Robot Olympics y Maker Expo son formatos educativos internos, no clasificatorio mundial ni feria mundial pública.')
    p['price'].update(year=2027,label=AI_PROMO,included=T('Учебные материалы, киты и футболка; показ проектов в пятницу. Питание summer отдельно согласуется до начала; зимнее обещание pizza не переносим автоматически.',
        'Materiales, kits y camiseta; presentación de proyectos el viernes. Comida summer se acuerda aparte antes del inicio; sin trasladar automáticamente pizza de invierno.'),extras=T('Care 4 дня: 52 утром / 128 после, 5 дней: 65 / 160 на ребёнка по конкретным карточкам. Laptop, питание, taxes / страховка и семейная поездка отдельно подтвердить. На 16–20 августа опубликованной цены нет.',
        'Care de 4 días: 52 por mañana / 128 por tarde, de 5 días: 65 / 160 por niño según fichas concretas. Confirmar laptop, comida, taxes / seguro y viaje familiar aparte. Sin precio publicado del 16–20 de agosto.'))
    for key,a,b,title,amount,themes,programme in SUMMER:
        tariff=T('Цена ещё не опубликована; не подставляем соседнюю неделю.', 'Precio aún sin publicar; sin asignar tarifa de semana vecina.') if amount is None else 'USD '+str(amount)+' '+T('ранний тариф до 31 декабря 2026; дальнейшие ступени уточнить','tarifa anticipada hasta 31 de diciembre de 2026; confirmar escalones posteriores')
        v=add_ai_session(p,key,a,b,title,programme,tariff,themes)
        if amount is None:v['entry']=T('Даты опубликованы, registration opens soon. Оформление записи пока не подтверждено открытым.', 'Fechas publicadas, registration opens soon. Inscripción aún sin confirmar abierta.')
    p['editorial_reason']=T('Сезонная техническая база для обоих с двумя возрастными потоками; цены привязаны к конкретным неделям и периоду раннего тарифа, язык ещё уточняется.',
        'Base técnica estacional para ambos con dos grupos de edad; precios vinculados a semanas concretas y periodo anticipado, idioma aún por confirmar.')
    result.append(p)

    tracks=[
      ('CP1177','hb-science-winter-2027','Holland Bloorview · Science Club','6–14','2027-01-19','2027-02-23',1,'18:00','19:30',['science'],['day'],'regular',
       T('Шесть вторников: опыты, наблюдение, измерение и совместная работа. Snow make-up 2 марта только при необходимости, не очередное обязательное занятие.',
         'Seis martes: experimentos, observación, medición y colaboración. Snow make-up 2 de marzo solo si hace falta, no otra clase obligatoria.')),
      ('CP1178','hb-junior-robotics-winter-2027','Holland Bloorview · Junior Robotics','6–10','2027-01-20','2027-02-24',2,'18:00','19:30',['robotics','coding'],['day'],'regular',
       T('Шесть сред, LEGO SPIKE Essential: моторы, световая матрица, цветовой датчик, icon / word blocks. Snow make-up 3 марта только при необходимости.',
         'Seis miércoles, LEGO SPIKE Essential: motores, matriz de luz, sensor de color, bloques con iconos / palabras. Snow make-up 3 de marzo solo si hace falta.')),
      ('CP1179','hb-coding-online-winter-2027','Holland Bloorview · Coding 101 Online',T('Winter 9–14; общее описание 8–14','Winter 9–14; descripción general 8–14'),'2027-01-21','2027-02-25',3,'18:00','19:00',['coding','games'],['online'],'online',
       T('Шесть четвергов онлайн, Scratch и собственная 2D-игра. Возраст расходится: Winter 9–14, общее описание 8–14; применяем конкретный Winter минимум 9, исключение только по решению оператора.',
         'Seis jueves online, Scratch y videojuego 2D propio. Edad discrepa: Winter 9–14, descripción general 8–14; usar mínimo Winter de 9, excepción solo por decisión del operador.')),
      ('CP1180','hb-intermediate-robotics-winter-2027','Holland Bloorview · Intermediate Robotics','10–14','2027-01-17','2027-02-28',6,'10:00','12:00',['robotics','coding'],['day'],'regular',
       T('Шесть воскресений, LEGO SPIKE Prime, Scratch-based coding и задачи Maze / Mars Rover / SumoBots. 14 февраля занятия нет. Snow make-up на странице ошибочно 7 марта 2026, не добавляем как подтверждённый день 2027.',
         'Seis domingos, LEGO SPIKE Prime, Scratch-based coding y retos Maze / Mars Rover / SumoBots. Sin clase 14 de febrero. Snow make-up dice erróneamente 7 de marzo de 2026; sin añadirlo como día confirmado de 2027.'))]
    for ident,slug,name,age,a,b,dow,start,end,themes,formats,participation,programme in tracks:
        p=base(ident,slug,name,'Канада','CAN','Holland Bloorview · 150 Kilgour Road · Toronto, Ontario',age,themes,formats)
        p['catalog_participation']=participation
        days=[];d=date.fromisoformat(a)
        while d<=date.fromisoformat(b):
            if d.weekday()==dow and d.isoformat()!='2027-02-14':days.append(d.isoformat())
            d+=timedelta(days=1)
        assert len(days)==6
        v=dict(start=a,end=b,label=name,source=HB,date_scope='session_days',formats=formats,
               sessions=[lesson(day,start,end,'America/Toronto',name) for day in days],
               price=T('Тариф не опубликован в прочитанной карточке.', 'Tarifa sin publicar en ficha leída.'),
               admission_kind='organization_route',entry=HB_GATE)
        p['programme']=programme+' '+HB_GATE
        p['timing'].update(status='published_2027',label=T('Регулярный шестинедельный курс: шесть отдельных занятий, не шестинедельный дневной лагерь. Резервные снежные даты не включены автоматически.',
            'Curso regular de seis semanas: seis clases separadas, no campamento diurno de seis semanas. Fechas de reserva por nieve no incluidas automáticamente.'),sessions=[[a,b]],session_details=[v])
        p['price'].update(year=2027,label=v['price'],included=T('Учебные занятия по выбранному треку; выдачу / возврат наборов и домашнюю технику согласовать.',
            'Clases del programa elegido; acordar entrega / devolución de kits y equipo doméstico.'),extras=T('Транспорт, проживание семьи, технические средства коммуникации / поддержка 1:1 при необходимости отдельно. Это не услуга полного дня или пансион.',
            'Transporte, alojamiento familiar, ayudas de comunicación / apoyo 1:1 si hace falta aparte. No servicio de día completo ni residencia.'),deposit=T('Оплата, страхование, резидентские условия и отмена не прочитаны в сезонной карточке; CampBrain не заполнялся.',
            'Pago, seguro, residencia y cancelación no constan en ficha de temporada; sin completar CampBrain.'))
        p['accommodation']=T('Онлайн с домашним сопровождением по необходимости; время Toronto, не местное время Коста-Рики.',
            'Online con apoyo doméstico si hace falta; hora Toronto, no hora local de Costa Rica.') if participation=='online' else T('Очные вечерние / воскресные занятия в Toronto, без проживания и полного дневного ухода.',
            'Clases presenciales nocturnas / dominicales en Toronto, sin alojamiento ni cuidado de día completo.')
        p['family_fit']=dict(matvey=fit('conditional','Возрастной диапазон / дату отсечения, formal diagnosis, язык и индивидуальный приём подтвердить; медицинское состояние детей неизвестно.',
            'Confirmar rango / fecha de corte de edad, formal diagnosis, idioma y admisión individual; situación médica infantil desconocida.'),oscar=fit('conditional','По младшему возрасту возможен только подходящий трек; formal diagnosis и решение о приёме обязательны, право семьи на участие не доказано.',
            'Por edad menor solo puede encajar curso adecuado; formal diagnosis y decisión de admisión obligatorios, sin acreditar derecho familiar a participar.'))
        if ident in ['CP1179','CP1180']:
            p['family_fit']['oscar']=fit('later','Минимум выбранного Winter-трека 9 / 10; Оскар в 2027 только 6–7. Специальные условия приёма это правило не отменяют.',
                'Mínimo del curso Winter elegido 9 / 10; Oscar en 2027 solo 6–7. Condiciones especiales de admisión no eliminan la regla.')
        p['editorial_reason']=T('Специальная рекреационная программа в мировом справочнике; не объявлена готовым семейным вариантом или квалификацией FIRST.',
            'Programa recreativo especializado en directorio mundial; sin presentarlo como opción familiar lista ni clasificación FIRST.')
        p['questions']=[T('Подтвердить конкретную категорию formal diagnosis, критерии приёма нерезидента, год возрастного отсечения 31 декабря и собственную поддержку при необходимости.',
            'Confirmar categoría concreta de formal diagnosis, admisión de no residentes, año de corte al 31 de diciembre y apoyo propio si hace falta.'),
            T('Уточнить английский, цену, материалы / домашний компьютер, отмену и фактический резервный день.',
              'Aclarar inglés, precio, materiales / ordenador doméstico, cancelación y día de reserva real.')]
        p['sources']=[src(T('Winter 2027 · действующий текст по старому URL', 'Winter 2027 · texto vigente en URL antigua'),HB),
                      src(T('Критерии приёма, диагноз, возраст и поддержка', 'Criterios de admisión, diagnóstico, edad y apoyo'),HBD)]
        result.append(p)

    for ident,slug,name,path,themes in [
      ('CP1181','hofstra-lego-sphero-2027-watch','Hofstra · LEGO & Sphero Robotics','specialty_robotics.html',['robotics','coding']),
      ('CP1182','hofstra-gba-2027-watch','Hofstra · Game Builders Academy','specialty_game_builders_academy_camp_long_island.html',['games','coding','ai','engineering'])]:
        p=base(ident,slug,name,'США','USA','Hofstra University · Long Island, New York',
               T('Entering Grades 2–10, отдельные потоки 2–5 / 6–10; это классы, не возраст 2–10 лет.',
                 'Entering Grades 2–10, grupos separados 2–5 / 6–10; son grados escolares, no edades de 2–10 años.'),themes,['day'])
        p['programme']=T('Младшие Grades 2–5: техническое занятие утром, recreation / swim после; старшие Grades 6–10 наоборот. LEGO Mindstorms / Sphero для robotics, coding / games / arts в GBA. Доплата Makerspace 515 относится только к Grades 6–10 и двухнедельной программе, не всем детям 6–10 лет.',
            'Menores Grades 2–5: especialidad técnica por la mañana, recreation / swim después; mayores Grades 6–10 al revés. LEGO Mindstorms / Sphero para robotics, coding / games / arts en GBA. Makerspace extra 515 solo para Grades 6–10 y programa de dos semanas, no todos los niños de 6–10 años.')
        p['timing'].update(status='partial_2027',label=HOF_LIMIT)
        p['price'].update(currency='USD',label=T('Общая текущая GBA-страница: Early Tuition 2350 за 2 недели, 1355 за 1 неделю; отдельную смену и применимость тарифа именно Robotics подтвердить. Дата окончания ранней цены не указана.',
            'Página GBA general actual: Early Tuition 2350 por 2 semanas, 1355 por 1 semana; confirmar sesión concreta y aplicación exacta a Robotics. Sin fecha de fin del precio anticipado.'),included=T('GBA Logistics: 09:00–16:00, lunch и transportation включены. Маршрут транспорта / конкретный адрес, нужный семье, отдельно согласовать.',
            'GBA Logistics: 09:00–16:00, lunch y transportation incluidos. Acordar ruta de transporte / dirección concreta que necesita la familia.'),extras=T('Makerspace 515 — опция Grades 6–10. Проживание родителей, перелёты, страхование и дополнительные часы отдельно; нет детского пансиона.',
            'Makerspace 515 es opción de Grades 6–10. Alojamiento de padres, vuelos, seguro y horas extra aparte; sin residencia infantil.'),deposit=T('Точные условия оплаты / возврата и доступность выбранной смены через текущий checkout не проверены. Старая анкета 2026 не договор на 2027.',
            'Sin verificar pago / devolución ni disponibilidad de sesión elegida en checkout actual. Formulario antiguo de 2026 no es contrato de 2027.'))
        p['accommodation']=T('Дневной кампусный формат; полный день включает рекреацию / плавание, техническая специализация по умолчанию часть дня.',
            'Formato diurno de campus; día completo incluye recreación / natación, especialidad técnica normalmente parte del día.')
        p['family_fit']={k:fit('conditional','Нужен фактический входящий класс по системе US и английский приём; год рождения не подтверждает Grades 2–5. Место не забронировано.',
            'Se necesita grado escolar de ingreso real según sistema US y admisión inglesa; año de nacimiento no acredita Grades 2–5. Plaza sin reservar.') for k in ['matvey','oscar']}
        p['editorial_reason']=T('Проверяемый университетский технический кандидат с честным разделением половины дня / Makerspace и школьного класса; даты пока watch.',
            'Candidato técnico universitario verificable, distinguiendo medio día / Makerspace y grado escolar; fechas siguen watch.')
        p['shortlist']=['technical']
        p['questions']=[T('Получить официальные даты, цену и письменные условия конкретного трека 2027; сверить входящий класс каждого ребёнка, английский и иностранный приём.',
            'Obtener fechas, precio y condiciones escritas del curso 2027 concreto; comprobar grado de ingreso de cada niño, inglés y admisión extranjera.'),
            T('Выяснить, в какой половине дня техника, какие приборы выдаются и возвращаются, маршрут bus, питание и отмена. Получить полный прайс до оплаты.',
              'Aclarar mitad del día técnica, equipos prestados y devueltos, ruta bus, comida y cancelación. Obtener precio completo antes de pagar.')]
        p['sources']=[src(name+' · '+T('программа и классы', 'programa y grados'),HOF+path),
                      src('Game Builders Academy · logistics / Early Tuition / Makerspace',HOF+'specialty_game_builders_academy_camp_long_island.html'),
                      src(T('Смены · точные строки не загрузились', 'Sesiones · filas exactas sin cargar'),HOF+'long-island-summer-camps-by-session.html')]
        p['sources']=list({s['url']:s for s in p['sources']}.values())
        result.append(p)
    return result

def extend_planning(d):
    offers=[]
    for days,amount,ident,start,end,morning,afternoon in [(4,359,'four-day','2027-06-22','2027-06-25',52,128),
                                                       (5,449,'five-day','2027-06-28','2027-07-02',65,160)]:
        path='magnolia-'+('steam-launchpad-0622-full' if days==4 else 'robo-olympics-0628-full')
        o=dict(id='aiara-both-'+ident+'-early-2027',slug='aiara-summer-magnolia-2027',
            label='AI & Robotics Academy · '+T('двое · ', 'dos niños · ')+str(days)+T(' дн. · ранний тариф', ' días · tarifa anticipada'),
            currency='USD',price_year=2027,format='day',children=['matvey','oscar'],base_by_child=dict(matvey=amount,oscar=amount),discount_second=0,required=[],
            unknown_required=[dict(id='food_cover_taxes',label=T('Питание обоих, обязательные taxes / страховка если нужны', 'Comida de ambos, taxes / seguro obligatorios si procede'),unit='amount',rate=1,min=0)],
            optional=[dict(id='morning-both',label=T('Утренний care обоим на все дни', 'Care matinal de ambos todos los días'),amount=morning*2),
                      dict(id='afternoon-both',label=T('Послеобеденный care обоим на все дни', 'Care vespertino de ambos todos los días'),amount=afternoon*2)],
            unknown_trip=['travel','lodging','misc'],sessions=[[start,end]],sources=[AI+'camps/'+path,AIC,AIR],checked=CHECKED,
            gate=T('Оба соответствуют 5–12: разные утренние группы, общий afternoon lab. Английский, реальный уровень, наличие мест и приём приезжей семьи ещё подтвердить.',
                   'Ambos cumplen 5–12: grupos matinales distintos, afternoon lab compartido. Confirmar inglés, nivel real, plazas y admisión de familia visitante.'),
            deposit_note=AI_REFUND,included=T('Опубликованная ранняя база двух без дополнительного sibling-вычета; киты / материалы и футболки. Питание summer не подтверждено включённым.',
                'Base anticipada publicada para dos sin deducción sibling adicional; kits / materiales y camisetas. Comida summer sin confirmar incluida.'),
            scope=AI_PROMO+' '+T('Это цена занятий и выбранных care, не полный счёт поездки. Промо до 31 декабря не дедлайн регистрации и не обещание цены после этой даты.',
                'Precio de clases y care elegidos, no factura completa de viaje. Promoción hasta 31 de diciembre no es plazo de inscripción ni promesa de precio posterior.'))
        offers.append(o)
    idx={o['id']:o for o in offers};old={o['id'] for o in d['camp_planning']['offers']}
    d['camp_planning']['offers']=[idx.get(o['id'],o) for o in d['camp_planning']['offers']]+[o for o in offers if o['id'] not in old]
    d['camp_planning'].update(version=151,asof=CHECKED)

def enrich_v151(d):
    extend_planning(d)
    for e in d['events']:
        if e.get('camp_programme_id') in {'CP1174','CP1175','CP1176','CP1177','CP1178','CP1179','CP1180'}:
            e['priority']='P3 — '+T('язык, счёт и конкретный приём уточнить','confirmar idioma, factura y admisión concreta')
        if e.get('camp_programme_id')=='CP1176':
            variant=next(v for p in d['camp_programmes']['profiles'] if p['id']=='CP1176' for v in p['timing']['session_details'] if v['start']==e['start'])
            e['themes']=list(variant['themes'])
            if e['start']=='2027-08-16':
                e['registration_status']=T('Даты анонсированы; registration opens soon, открытая запись не подтверждена.',
                    'Fechas anunciadas; registration opens soon, inscripción abierta sin confirmar.')
