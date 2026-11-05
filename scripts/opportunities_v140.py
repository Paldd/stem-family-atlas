"""Primary-source refresh, 4 November 2026. Applied after historical enrichers."""
from copy import deepcopy
import re

CHECKED='2026-11-04'
SPANISH={}
def T(ru,es):
    es=re.sub(r'\b(en|de|del|el|al|y|para|solo|máximo|total|edad|edades|desde|días|semanas|exige|cumple|registro|clasificatorias|finales|premios|supera)(?=\d)',r'\1 ',es)
    SPANISH[ru]=es
    return ru

WAICY='https://www.waicy.org/waicy-2026/'
GUIDE='https://waicy-cdn.wholeren.cn/wp-content/uploads/2026/10/WAICY-2026-Guidebook-2.pdf'
TIMTOS='https://cloudcdn.taiwantradeshows.com.tw/2027/timtos/kit-en/application-kit-en.pdf'

COMMON_MAKEX=T('Даты дисциплины проверены 04.11.2026 по её странице. Тарифные справки магазина относятся к 06.10.2026. Заявка, свободные места и итоговый счёт семьи не подтверждены.',
    'Fechas verificadas el04.11.2026 en la página de la disciplina. Referencias de precios de tienda del06.10.2026. Solicitud, plazas e importe final familiar sin confirmar.')
FIRST_BLOCK=T('27 ноября: регистрация 09:00–12:00, отбор 13:00–19:30. 28 ноября: финалы 09:00–12:30, награждение 12:30–13:30. Часовой пояс America/Mexico_City.',
    '27 de noviembre: registro09:00–12:00, clasificatorias13:00–19:30. 28 de noviembre: finales09:00–12:30, premios12:30–13:30. Zona America/Mexico_City.')
SECOND_BLOCK=T('28 ноября: регистрация 09:00–12:30, отбор 15:00–19:30. 29 ноября: финалы 09:00–14:00, награждение 14:30–15:30. Часовой пояс America/Mexico_City.',
    '28 de noviembre: registro09:00–12:30, clasificatorias15:00–19:30. 29 de noviembre: finales09:00–14:00, premios14:30–15:30. Zona America/Mexico_City.')
WAICY_NOTE=T('Текущее октябрьское руководство исправляет Showcase: дедлайн 29.11.2026 17:00 ET. Главная, обложка, расписание и подробный Showcase указывают 4–6 декабря; во вводном абзаце PDF осталось 5–7 декабря. Индивидуальный слот сообщают после отбора; сам факт подачи не означает приглашение в финал.',
    'La guía de octubre corrige Showcase: plazo29.11.2026 17:00 ET. Web, portada, calendario y sección detallada Showcase indican4–6 de diciembre; el párrafo introductorio PDF aún dice5–7. El horario individual depende de la selección; enviar no confirma invitación a la final.')
WAICY_DEADLINE=T('29.11.2026 17:00 ET = 22:00 UTC = 16:00 Коста-Рика. Дедлайн повторён в разделах четырёх треков октябрьского руководства.',
    '29.11.2026 17:00 ET =22:00 UTC =16:00 Costa Rica. El plazo figura en los cuatro apartados de la guía de octubre.')

def enrich_v140(d):
    events={e['id']:e for e in d['events']}
    for ident in ['C608','C610','C611','C612','C616','C617','C609','C614','C615','C618']:
        e=events[ident];first=ident in ['C608','C610','C611','C612','C616','C617']
        e.update(start='2026-11-27' if first else '2026-11-28',end='2026-11-28' if first else '2026-11-29',
                 date_scope='festival_window',checked=CHECKED,registration_status=COMMON_MAKEX,
                 proof=T('Прочитана новая официальная страница дисциплины с отдельным расписанием; общие три дня фестиваля сужены до её двух дней.',
                     'Leída la página oficial renovada con horario propio; los tres días del festival se acotan a los dos de esta disciplina.'))
        old=e.get('note','')
        old=old.replace('Даты 27–29.11 — общее окно фестиваля; точный день этой дисциплины не найден.','')
        block=FIRST_BLOCK if first else SECOND_BLOCK
        e['note']=old.strip() if block in old else old.strip()+' '+block
    # This course is explicitly marked as a future call, not one of the two blocks.
    e=events['C613']
    e.update(start='',end='',deadline='',checked=CHECKED,
        period=T('Soccer / CK World Cup: следующая convocatoria пока не объявлена; даты общего MakeX не являются датами этой дисциплины.',
                 'Soccer / CK World Cup: próxima convocatoria sin anunciar; las fechas generales MakeX no son fechas de esta disciplina.'),
        date_status=T('Ожидается новая convocatoria','Próxima convocatoria pendiente'),
        registration_status=T('Текущая страница показывает Próxima convocatoria; открытый приём и соревнование 27–29 ноября не подтверждены.',
            'La página muestra Próxima convocatoria; no confirma inscripción abierta ni competición del27–29 de noviembre.'),
        proof=T('Повторно прочитана отдельная Soccer page; приём отделён от действующих ноябрьских дисциплин.',
            'Releída la página Soccer; convocatoria separada de las disciplinas vigentes de noviembre.'),
        priority=T('P2 — следить за новой convocatoria','P2 — seguir la próxima convocatoria'),
        action=T('Дождаться дат и правил Soccer; для ноября выбирать только дисциплины с опубликованным расписанием.',
            'Esperar fechas y reglas Soccer; para noviembre elegir disciplinas con horario publicado.'))
    events['C020'].update(checked=CHECKED,registration_status=COMMON_MAKEX,
        proof=T('Проверены основная страница и расписания 11 категорий. Soccer пока без convocatoria. PDF mTiny, Codey, Inspire и Starter повторно скачаны и прочитаны.',
            'Verificadas la web principal y las11 categorías. Soccer sin convocatoria. Descargados y releídos los PDF mTiny, Codey, Inspire y Starter.'),
        note=T('Первый блок 27–28 ноября: mTiny, Sumo, RoverX, линия, Intermediate, Explorer. Второй 28–29: Codey, Inspire, Signal Rise и Challenge. Soccer без даты. Возрастная отсечка 01.01.2026 у mTiny/Codey сохранена; у Inspire/Starter другие интервалы рождения. Мировая квота не подтверждена.',
            'Primer bloque27–28 de noviembre: mTiny, Sumo, RoverX, línea, Intermediate, Explorer. Segundo28–29: Codey, Inspire, Signal Rise y Challenge. Soccer sin fecha. Se conserva el corte01.01.2026 de mTiny/Codey; Inspire/Starter usan otros intervalos de nacimiento. Cupo mundial sin confirmar.'))
    events['C608']['action']=T('Оскар: подтвердить mTiny и coach на 27–28 ноября. Матвей не проходит возраст mTiny. Уточнить полный счёт до покупки техники.',
        'Oscar: confirmar mTiny y coach para27–28 de noviembre. Matvey supera la edad mTiny. Pedir importe completo antes de comprar equipo.')
    events['C609']['action']=T('Матвей: подтвердить Codey и coach на 28–29 ноября. Для Оскара минимум 6 лет на 01.01.2026 требует рождения именно 01.01.2020; без точной даты допуск не обещать.',
        'Matvey: confirmar Codey y coach para28–29 de noviembre. Para Oscar, tener mínimo6 años al01.01.2026 exige nacimiento el01.01.2020; sin fecha exacta no confirmar admisión.')
    for ident in ['C608','C609','C614','C615']:
        events[ident]['proof']=T('Страница с расписанием и связанный PDF повторно прочитаны 04.11.2026. Возрастные ограничения прежних правил сохранены.',
            'Releídos página con horario y PDF enlazado el04.11.2026. Se conservan los límites de edad del reglamento anterior.')
    for ident in ['C037','C1152','C1153','C1154']:
        e=events[ident]
        e.update(checked=CHECKED,deadline='2026-11-29',deadline_utc='2026-11-29T22:00:00Z',deadline_note=WAICY_DEADLINE,
            deadline_label=T('Подача проекта','Entrega del proyecto'),
            proof=T('Проверены обновлённая страница WAICY и октябрьский Guidebook-2: возраст/команда, сроки каждого трека и расписание финала.',
                'Verificadas web WAICY renovada y Guidebook-2 de octubre: edad/equipo, plazos por modalidad y calendario final.'),
            registration_status=T('Официальная подача проектов объявлена; регистрацию семьи и принятие проекта не проверяли.',
                'Entrega oficial anunciada; inscripción familiar y aceptación del proyecto sin verificar.'))
        e['references']=[r for r in e.get('references',[]) if '/2026/09/WAICY' not in r['url']]
        if not any(r['url']==GUIDE for r in e['references']):
            e['references'].append(dict(label=T('Октябрьское руководство 2026','Guía de octubre2026'),url=GUIDE))
        if ident=='C037':
            e.update(start='',end='',
                period=T('Объявлен финал 4–6 декабря 2026; вводный абзац PDF всё ещё содержит 5–7 декабря. Конкретный слот после отбора уточнить.',
                    'Final anunciada4–6 de diciembre2026; el párrafo introductorio PDF aún indica5–7. Confirmar horario individual tras la selección.'),
                date_status=T('Конфликт дат финала; дедлайн подтверждён','Fechas finales contradictorias; plazo confirmado'),note=WAICY_NOTE,
                action=T('Подготовить самостоятельный AI-проект и EN-материалы к 29 ноября 16:00 Коста-Рика; индивидуальный слот финала проверить после отбора 2 декабря.',
                    'Preparar proyecto AI propio y materiales EN antes del29 de noviembre16:00 Costa Rica; comprobar horario final tras la selección del2 de diciembre.'))
        else:
            e['source']=GUIDE
            e['note']=T('Дедлайн этого трека подтверждён новым руководством. Общие дни WAICY не превращаем в обязательную защиту каждого Art/Video/LLM проекта. Собственный вклад ребёнка и условия AI-инструментов обязательны; сертификат участия не равен призу.',
                'Plazo de esta modalidad confirmado en la guía nueva. No se asigna presentación obligatoria de cada proyecto Art/Video/LLM a todo el periodo WAICY. Exigir autoría infantil y condiciones de herramientas AI; certificado de participación distinto de premio.')
    events['C038'].update(checked=CHECKED,
        proof=T('Официальная главная Codeavour 8.0 заново прочитана: приём без фиксированного закрытия, 7–18 лет, 1–3 ученика с mentor, два тарифных этапа. Дата финала не установлена.',
            'Releída la web oficial Codeavour8.0: inscripción sin cierre fijo, edades7–18, 1–3 alumnos con mentor y dos fases tarifarias. Final sin fecha establecida.'))
    for ident in ['C846','C847']:
        events[ident].update(checked=CHECKED,
            registration_status=T('Регистрация Global Appathon 2027 открыта с 29.10.2026; семья не зарегистрирована этим исследованием.',
                'Inscripción Global Appathon2027 abierta desde29.10.2026; esta investigación no registra a la familia.'),
            proof=T('Повторно прочитаны главная и FAQ сезона 2026–27. Junior, сроки AOE, английские материалы и различие award/contribution certificate проверены.',
                'Releídos web y FAQ de la temporada2026–27: Junior, plazos AOE, materiales en inglés y distinción award/contribution certificate.'))
    guide=next(p for p in d['league_guide']['profiles'] if p['id']=='waicy')
    guide['nuances'][0]=WAICY_NOTE;guide['checked']=CHECKED
    guide['sources']=[s for s in guide['sources'] if '/2026/09/WAICY' not in s['url']]
    for s in guide['sources']:
        if s['url']==WAICY:s['checked']=CHECKED
    if not any(s['url']==GUIDE for s in guide['sources']):
        guide['sources'].append(dict(title=T('Октябрьское руководство 2026','Guía de octubre2026'),url=GUIDE,checked=CHECKED))
    d['league_guide'].update(version=140,checked=CHECKED)
    nearby=d['family_strategy'].get('nearby_participation_v118')
    if nearby:
        old=nearby.get('archived_items',[])+[i for i in nearby['items'] if i['id'] not in ['C608','C609','C614','C615','C082']]
        nearby['archived_items']=list({i['id']:i for i in old}.values())
        nearby['items']=[i for i in nearby['items'] if i['id'] in ['C608','C609','C614','C615','C082']]
        nearby.update(checked=CHECKED,version=140,
            scope=T('Текущие ноябрьские возможности и будущие маршруты; октябрьские старты перенесены в архив этой подборки. Мировой охват неполный.',
                'Oportunidades actuales de noviembre y rutas futuras; eventos de octubre archivados en esta selección. Cobertura mundial parcial.'),
            conclusion=T('Оскару — mTiny 27–28 ноября; Матвею — Codey 28–29 ноября, после подтверждения заявки. Вместе можно рассмотреть Starter, но DOB-правило не подтверждает места, готовность и итоговую стоимость.',
                'Oscar: mTiny27–28 de noviembre; Matvey: Codey28–29, previa confirmación de inscripción. Starter puede evaluarse juntos, pero cumplir DOB no confirma plazas, preparación ni coste final.'))
        for item in nearby['items']:
            if item['id']=='C608':item['step']=events['C608']['action']
            if item['id']=='C609':item['step']=events['C609']['action']
        nearby['next_steps']=[T('Выбрать дисциплины и подтвердить места, возраст, роботов и полный счёт; не опираться на прошедшие октябрьские предложения.',
            'Elegir disciplinas y confirmar plazas, edad, robots e importe total; no usar ofertas vencidas de octubre.'),
            T('Для WAICY подготовить собственный проект к 29 ноября 16:00 Коста-Рика. Для Appathon сейчас открыта регистрация; подача начнётся 2 декабря.',
            'Para WAICY preparar proyecto propio antes del29 de noviembre16:00 Costa Rica. Appathon ya admite registro; entrega desde el2 de diciembre.')]
    if 'E201' not in events:
        base=deepcopy(events['E010'])
        base.update(id='E201',title="TIMTOS 2027 · Taipei Int'l Machine Tool Show",country='Тайвань',region='Азия',iso=['TWN'],
            city=T('Taipei · TaiNEX 1, TaiNEX 2 и TWTC Hall 1','Taipei · TaiNEX1, TaiNEX2 y TWTC Hall1'),
            venue='Taipei Nangang Exhibition Center / TWTC',start='2027-03-02',end='2027-03-06',deadline='',deadline_label='',deadline_note='',
            period='',date_status='Подтверждено',checked=CHECKED,source=TIMTOS,
            age=T('Посетители 12+; детям младше 12 вход запрещён','Visitantes12+; acceso prohibido a menores de12'),
            mat=T('Нет: в 2027 Матвею 9–10, требуется 12+','No: en2027 Matvey tendrá9–10; exige12+'),
            osc=T('Нет: в 2027 Оскару 6–7, требуется 12+','No: en2027 Oscar tendrá6–7; exige12+'),
            cost=T('Тариф посетителя не подтверждён; стоимость стенда из exhibitor kit не является входным билетом.',
                'Tarifa de visitante sin confirmar; el precio de stand del exhibitor kit no es una entrada.'),
            entry=T('Только взрослый маршрут родителей; проверить регистрацию посетителя на официальном сайте. Не брать детей на основании общего отраслевого интереса.',
                'Ruta solo para adultos de la familia; verificar registro de visitante en la web oficial. El interés tecnológico no da acceso infantil.'),
            action=T('Рассматривать отдельную поездку взрослых; детям нужен иной семейный ивент.',
                'Considerar visita separada de adultos; elegir otro evento familiar para los niños.'),
            language=T('Официальный fact sheet EN; язык конкретного форума уточнить','Fact sheet oficial EN; confirmar idioma de cada foro'),
            language_certainty=T('EN подтверждён для документа, не для всех докладов','EN confirmado para el documento, no para todas las ponencias'),
            languages=[],support_languages=['EN'],language_mode='materials',participation='visitor',admission_kind='visitor',
            scope='international',level=T('Международная промышленная выставка','Exposición industrial internacional'),
            priority=T('P4 — только взрослые','P4 — solo adultos'),status='Идея',
            reward=T('Посещение выставки; не конкурсная награда','Visita a exposición; sin premio competitivo'),
            note=T('Дни показа 2–6 марта; 7–9 марта — демонтаж, не дополнительные дни посещения. Детский запрет подтверждён официальным fact sheet.',
                'Exposición2–6 de marzo;7–9 de marzo es desmontaje, sin días adicionales de visita. Prohibición infantil confirmada en el fact sheet oficial.'),
            proof=T('Официальный TIMTOS 2027 exhibitor kit: визуально проверена страница fact sheet и расписание монтажа/показа/демонтажа.',
                'Kit oficial TIMTOS2027: revisados visualmente fact sheet y calendario de montaje/exposición/desmontaje.'),
            registration_status=T('Регистрацию посетителя и билеты семьи не оформляли','Registro de visitantes y entradas familiares no tramitados'),
            themes=['robotics','ai','technology'],exhibition_tier='global',visitor_policy='adults_only',
            visitor_policy_note=T('Официально запрещён вход младше 12 лет; Матвей и Оскар не подходят по возрасту.',
                'Acceso oficialmente prohibido a menores de12; Matvey y Oscar no cumplen la edad.'),
            adult_entry=T('Проверить требования и тариф взрослого посетителя; правила экспонента не заменяют visitor registration.',
                'Verificar requisitos y tarifa del visitante adulto; reglas de expositor distintas de visitor registration.'),
            importance_reason=T('Промышленная автоматизация, робототехника и Industrial AI; редакционный приоритет взрослого знакомства с отраслью.',
                'Automatización industrial, robótica e Industrial AI; prioridad editorial para visita sectorial adulta.'),
            highlights=[T('Robotics & Automation и Industrial AI входят в официальный профиль','Robotics & Automation e Industrial AI figuran en el perfil oficial')],
            exhibitor_note=T('Список компаний и программа докладов отдельно не проверены','Lista de empresas y programa de ponencias sin verificar por separado'),
            exhibitor_directory_url='',exhibitors=[],references=[dict(label=T('Официальный сайт TIMTOS','Web oficial TIMTOS'),url='https://www.timtos.com.tw/en/index.html')])
        for k in ['sessions','public_days','public_start','public_end','deadline_utc','historical_editions']:base.pop(k,None)
        d['events'].append(base)
    urls={s['url'] for s in d['sources']}
    for url,title in [(GUIDE,T('WAICY · октябрьское руководство','WAICY · guía de octubre')),(TIMTOS,'TIMTOS 2027 fact sheet')]:
        if url not in urls:
            d['sources'].append(dict(url=url,title=title,checked=CHECKED,evidence=T('Первичный документ прочитан; ограничения сохранены','Documento primario leído; restricciones conservadas')))
    d['asof']=max(d['asof'],CHECKED)

def camp_profiles_v140():
    """Four distinct programmes; campus/date combinations are not fabricated."""
    from datetime import date,timedelta
    graphite='https://graphiteacademy.com/holiday-camps-november-holiday-camp/'
    worklab='https://www.worklab.com.sg/minecraft-coding-camp'
    schedule='https://www.worklab.com.sg/_files/ugd/4223d1_8b1592ea2e724f0d8f61cdfdc611bbab.pdf'
    place=T('Elias Mall #02-306 / Canberra Plaza #03-10,11; точную площадку выбранной смены подтвердить',
        'Elias Mall#02-306 / Canberra Plaza#03-10,11; confirmar sede concreta de la sesión elegida')
    unknown_language=T('Язык преподавания не указан. Английская страница не подтверждает EN; язык объяснений и поддержки нужно получить от оператора.',
        'Idioma de enseñanza sin indicar. Una web en inglés no confirma EN; pedir al operador idioma de explicación y apoyo.')
    programmes=[
      ('CP1120','graphite-heroverse-2026','Graphite Academy · Heroverse',['coding','games'],[['2026-11-23','2026-11-25']],
       T('Pixel Art, MakeCode Arcade и Delightex: собственная ретро-игра и 3D-мир, брелок из бусин. 3 дня по 2,5 часа, всего 7,5 часов; максимум 8 детей.',
         'Pixel Art, MakeCode Arcade y Delightex: juego retro propio y mundo3D, llavero de cuentas.3 días de2,5 horas, total7,5 horas; máximo8 niños.'),
       T('$328 early bird / $398 обычный тариф; валюта, GST, единица оплаты и срок скидки не раскрыты.',
         '$328 early bird / $398 tarifa normal; moneda, GST, unidad de pago y plazo del descuento sin detallar.')),
      ('CP1121','graphite-pokemon-2026','Graphite Academy · Pokémon Coding Adventure',['coding','games'],[['2026-11-30','2026-12-02']],
       T('Pixel Art, Scratch и Minecraft Education: собственная игра и 3D-мир. 3 дня по 2,5 часа, всего 7,5 часов; максимум 8 детей.',
         'Pixel Art, Scratch y Minecraft Education: juego propio y mundo3D.3 días de2,5 horas, total7,5 horas; máximo8 niños.'),
       T('$328 early bird / $398 обычный тариф; валюта, GST, единица оплаты и срок скидки не раскрыты.',
         '$328 early bird / $398 tarifa normal; moneda, GST, unidad de pago y plazo del descuento sin detallar.')),
      ('CP1122','graphite-ai-lego-2026','Graphite Academy · AI LEGO Robotics',['robotics','ai'],[['2026-11-26','2026-11-27'],['2026-12-03','2026-12-04']],
       T('Построить LEGO-машину, испытать движение и препятствия, познакомиться с AI и автономным транспортом. 2 дня по 2,5 часа, всего 5 часов; максимум 8 детей. Реальное обучение модели и версия набора не описаны.',
         'Construir vehículo LEGO, probar movimiento y obstáculos e introducir AI y transporte autónomo.2 días de2,5 horas, total5 horas; máximo8 niños. No se detalla entrenamiento de modelos ni versión del equipo.'),
       T('$248 early bird / $298 обычный тариф; валюта, GST, единица оплаты и срок скидки не раскрыты.',
         '$248 early bird / $298 tarifa normal; moneda, GST, unidad de pago y plazo del descuento sin detallar.')),
    ]
    out=[]
    for ident,slug,provider,themes,sessions,programme,price in programmes:
        out.append(dict(id=ident,slug=slug,provider=provider,country='Сингапур',iso='SGP',place=place,themes=themes,formats=['day'],
            age=T('6–13 лет; возраст на начало и исключения отдельно не описаны','6–13 años; fecha de corte y excepciones sin detallar'),
            language=unknown_language,confirmed_instruction_languages=[],programme=programme,
            timing=dict(status='published_2026',label=T('Ноябрь–декабрь 2026; занятия 09:30–12:00. Даты опубликованы, свободные места и выбранный кампус не подтверждены.',
                'Noviembre–diciembre2026;09:30–12:00. Fechas publicadas; plazas y campus elegido sin confirmar.'),sessions=sessions,precision='published_sessions'),
            price=dict(year=2026,label=price,
                included=T('Содержание проекта описано; включение устройства, аккаунтов и расходников в цену уточнить.',
                    'Contenido del proyecto descrito; confirmar si dispositivo, cuentas y materiales están incluidos.'),
                extras=T('Проживание семьи, дорога и питание отдельно; технику домой не обещают.',
                    'Alojamiento familiar, transporte y comida aparte; no se promete equipo para llevar a casa.'),
                deposit=T('Аванс, отмена и возврат выбранной смены не опубликованы в прочитанной странице.',
                    'Anticipo, cancelación y reembolso de la sesión elegida no publicados en la página consultada.')),
            accommodation=T('Дневные утренние занятия; проживание не предлагается','Sesiones de mañana; sin alojamiento'),
            family_fit=dict(matvey=dict(status='conditional',detail=T('Год рождения 2017 подходит диапазону; язык, внешний приём и сложность после трёх лет опыта уточнить.',
                'Nacimiento2017 dentro del rango; confirmar idioma, admisión externa y nivel tras tres años de experiencia.')),
                oscar=dict(status='conditional',detail=T('Нужны исполненные 6 лет на начало; день рождения и правило отсечения неизвестны. Язык не подтверждён.',
                    'Debe haber cumplido6 al empezar; cumpleaños y regla de corte desconocidos. Idioma sin confirmar.'))),
            editorial_reason=T('Новый короткий технический вариант; неизвестный язык не включён в подтверждённые EN-программы.',
                'Nueva opción técnica breve; idioma desconocido excluido de programas EN confirmados.'),shortlist=[],
            questions=[T('Подтвердить язык преподавания, площадку и места выбранных дат.',
                'Confirmar idioma docente, sede y plazas en las fechas elegidas.'),
                T('Получить полный счёт с валютой, GST, техникой и условиями отмены; приём приезжих не установлен.',
                    'Pedir importe completo con moneda, GST, equipo y cancelación; admisión de visitantes sin establecer.')],
            sources=[dict(title=T('Точные программы, даты и рекламные тарифы','Programas, fechas y tarifas anunciadas'),url=graphite,checked=CHECKED)],checked=CHECKED))
    sessions=[[s,(date.fromisoformat(s)+timedelta(days=3)).isoformat()] for s in ['2026-11-23','2026-11-30','2026-12-07','2026-12-14','2026-12-21','2026-12-28','2027-01-04']]
    programme=T('Minecraft Education и блочное программирование: логика, последовательности, тестирование и отладка собственной работы. PDF показывает 4 полудня 09:30–12:00, то есть 10 часов пребывания с ежедневным перерывом 15 минут. Упоминание Java/2 полных дней на общей странице расходится с этим расписанием.',
        'Minecraft Education y bloques: lógica, secuencias, pruebas y depuración de trabajo propio. PDF:4 medias jornadas09:30–12:00, 10 horas de estancia con pausa diaria de15 minutos. La mención Java/2 días completos en la web general discrepa de este horario.')
    fit=dict(matvey=dict(status='candidate',detail=T('Матвей 2017 года рождения старше 8 лет во все эти смены. Уровень и внешний приём подтвердить.',
        'Matvey, nacido en2017, supera8 años en todas estas sesiones. Confirmar nivel y admisión externa.')),
        oscar=dict(status='later',detail=T('Оскару 2020 года рождения ещё нет 8 лет ни в одной указанной смене.',
            'Oscar, nacido en2020, aún no cumple8 en ninguna sesión indicada.')))
    details=[]
    for start,end in sessions:
        days=[]
        for offset in range(4):
            day=(date.fromisoformat(start)+timedelta(days=offset)).isoformat()
            days.append(dict(date=day,start_time='09:30',end_time='12:00',timezone='Asia/Singapore',
                topic='Minecraft Education',time_note=T('Время местное; 15 минут перерыва входят в пребывание','Hora local;15 minutos de pausa incluidos en la estancia')))
        details.append(dict(start=start,end=end,label='Forum · Minecraft Coding',source=schedule,
            price=T('$449 за выбранные 4 полудня; валюта и GST в PDF не указаны',
                '$449 por las4 medias jornadas elegidas; moneda y GST sin indicar en PDF'),
            date_scope='session_days',sessions=days,family_fit=fit,
            place='Forum The Shopping Mall · #02-01/02 · 583 Orchard Road',
            proof=T('Дни, часы, возраст, место и цена перепроверены по текущему PDF Year-End 2026–27.',
                'Días, horas, edad, sede y precio verificados en el PDF actual Year-End2026–27.')))
    out.append(dict(id='CP1123',slug='worklab-minecraft-coding-2026-27',provider="Children’s Worklab · Minecraft Coding",country='Сингапур',iso='SGP',
        place='Forum The Shopping Mall · #02-01/02 · 583 Orchard Road',themes=['coding','games'],formats=['day'],
        age=T('8+ по дню рождения на первый день; класс не заменяет возраст','8+ cumplidos al primer día; curso escolar no sustituye edad'),
        language=T('Оператор прямо подтверждает все занятия на английском; речь не только об английском сайте.',
            'El operador confirma expresamente todas las clases en inglés; no se deduce del idioma web.'),confirmed_instruction_languages=['EN'],
        programme=programme,timing=dict(status='published_2026_27',label=T('Семь недель 23.11.2026–07.01.2027; только понедельник–четверг, 09:30–12:00. Подробный PDF имеет приоритет над общим старым описанием.',
            'Siete semanas23.11.2026–07.01.2027; solo lunes–jueves,09:30–12:00. El PDF detallado prevalece sobre la descripción general antigua.'),sessions=sessions,session_details=details,precision='published_sessions'),
        price=dict(year=2026,season='2026/27',label=T('$449 за неделю из 4 полудней. Валюта и GST не напечатаны; не считать автоматически USD. Скидка группы требует минимум 3 детей.',
            '$449 por semana de4 medias jornadas. Moneda y GST sin imprimir; no asumir USD. Descuento de grupo exige mínimo3 niños.'),
            included=T('Учебный курс; ноутбук и аккаунт Minecraft отдельно подтвердить. Выдача техники домой не заявлена.',
                'Curso; confirmar portátil y cuenta Minecraft por separado. Sin promesa de equipo para llevar.'),
            extras=T('Обеда нет; перекус и напиток свои. Дорога и жильё семьи отдельно. Два брата не дают групповую скидку для 3 детей.',
                'Sin almuerzo; traer merienda y bebida. Transporte y alojamiento familiar aparte. Dos hermanos no cumplen descuento para3 niños.'),
            deposit=T('Оплату и отмену выбранной недели подтвердить; рассылку и заявку семьи не оформляли.',
                'Confirmar pago y cancelación de la semana elegida; sin suscripción ni solicitud familiar.')),
        accommodation=T('Только дневной формат; родители отвечают за доставку и время после 12:00.',
            'Solo de día; familia responsable del transporte y del tiempo posterior a12:00.'),family_fit=fit,
        editorial_reason=T('Подтверждённый EN игровой coding-интенсив для Матвея; Оскару нужен другой младший курс.',
            'Intensivo coding de videojuegos EN confirmado para Matvey; Oscar necesita otro curso infantil.'),shortlist=[],
        questions=[T('Подтвердить место, валюту, GST, устройство и аккаунт; не переносить старые условия полного дня.',
            'Confirmar plaza, moneda, GST, dispositivo y cuenta; no trasladar condiciones antiguas de jornada completa.'),
            T('Уточнить реальную платформу: Minecraft Education с блоками или Java-моды; приём приезжих и возврат неизвестны.',
                'Confirmar plataforma real: Minecraft Education con bloques o mods Java; admisión extranjera y reembolso desconocidos.')],
        sources=[dict(title=T('Явный английский язык и возраст 8+','Enseñanza en inglés explícita y edad8+'),url=worklab,checked=CHECKED),
            dict(title=T('Текущий PDF: семь недель, Forum, 09:30–12:00 и $449',
                'PDF actual: siete semanas, Forum,09:30–12:00 y $449'),url=schedule,checked=CHECKED)],checked=CHECKED))
    return out
