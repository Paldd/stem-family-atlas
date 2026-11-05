"""Current Maker Faire editions; visitor access and workshops remain distinct."""
CHECKED='2026-11-04'
SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
NETWORK='https://makerfaire.com/upcoming-faires/'
BILBAO='https://bilbao.makerfaire.com/'
BILBAO_PROGRAMME=BILBAO+'programa-2026/'
SHENZHEN='https://www.shenzhenmakerfaire.com/'
ALPHA=SHENZHEN+'2026/11/04/alpha-camp-two-days-of-hands-on-discovery-at-maker-faire-shenzhen-2026/'
ALPHA_SHOP='https://www.seeedstudio.com/Maker-Faire-Shenzhen-2026-Alpha-Camp-Early-Bird-2-Day-Pass-with-Limited-NFC-Badge.html'
MONTERREY='https://luma.com/i5cz5p70'
ORLANDO='https://www.makerfaireorlando.com/'
UNKNOWN_LANG=T('Язык ведущего конкретной мастерской EN/ES/RU не подтверждён. Английская или испанская страница сама по себе не доказывает язык занятий.',
 'Idioma EN/ES/RU del instructor del taller concreto sin confirmar. Una página inglesa o española por sí sola no acredita el idioma de las actividades.')
UNKNOWN_FIT=T('Условно: подтвердить вход ребёнка, сопровождение и возраст выбранной активности.',
 'Condicional: confirmar entrada infantil, acompañamiento y edad de actividad elegida.')
FAMILY_FIT=T('Да для семейного посещения; возраст и запись на мастерские отдельно.',
 'Sí para visita familiar; edades y reserva de talleres aparte.')
UNPRICED=T('Цена выпуска ещё не подтверждена; прежние тарифы не перенесены.',
 'Precio de esta edición aún sin confirmar; tarifas anteriores no se trasladan.')
MAKER_NOTE=T('Фестиваль проектов и makers; это не полный каталог мировых компаний и не мировой финал робототехники.',
 'Festival de proyectos y makers; no es un catálogo completo de empresas mundiales ni una final mundial de robótica.')

def refs(*items):return [dict(label=label,url=url) for label,url in items]
def expo(e,policy='confirm_children'):
    e.update(exhibition_tier='family_alternative',visitor_policy=policy,
        visitor_policy_note=FAMILY_FIT if policy=='family' else UNKNOWN_FIT,
        highlights=[T('Проекты makers','Proyectos maker'),T('Изобретения и прототипы','Inventos y prototipos'),T('Мастерские: правила отдельно','Talleres: reglas aparte')],
        exhibitor_note=MAKER_NOTE,exhibitor_directory_url=e['source'],adult_entry=e['entry'])
    return e

def new_event(ident,title,country,iso,city,start,end,url,family=False):
    fit=FAMILY_FIT if family else UNKNOWN_FIT
    e=dict(id=ident,block='События',title=title,country=country,iso=[iso],region='Северная Америка' if iso=='USA' else 'Европа' if iso in ['ITA','ESP'] else 'Азия',
        city=city,start=start,end=end,deadline='',period='',date_status='Подтверждено',date_scope='festival_window',
        age=T('Семейный фестиваль; пределы отдельных мастерских уточнить.','Festival familiar; confirmar límites de cada taller.') if family else T('Детские правила этого выпуска ещё не опубликованы / не подтверждены.','Reglas infantiles de esta edición aún sin publicar / confirmar.'),
        mat=fit,osc=fit,format=T('Посещение фестиваля; самостоятельная заявка makers и мастерские отдельно.','Visita al festival; propuesta maker y talleres aparte.'),
        entry=T('Проверить билет посетителя и запись на выбранную активность; заявка экспонента не даёт семейный билет.','Comprobar entrada de visitante y reserva de actividad elegida; propuesta expositora no concede entrada familiar.'),
        gear=MAKER_NOTE,language=UNKNOWN_LANG,languages=[],language_mode='unconfirmed',language_certainty=UNKNOWN_LANG,cost=UNPRICED,
        level=T('Семейный / региональный maker-фестиваль','Festival maker familiar / regional'),reward=T('Посещение и учебный проект; соревновательная награда не обещана.','Visita y proyecto educativo; sin prometer premio competitivo.'),
        scope='regional',importance_reason=T('Редакционная оценка по практической программе и доступу семьи; независимый мировой рейтинг не установлен.','Valoración editorial por programa práctico y acceso familiar; clasificación mundial independiente sin acreditar.'),
        priority='P2 — '+T('после проверки семейного билета и программы','tras comprobar entrada familiar y programa') if family else 'P3 — '+T('условия семьи ещё уточняются','condiciones familiares pendientes'),
        action=T('Выбрать подходящую по возрасту активность, подтвердить язык, билет и наличие мест до поездки.','Elegir actividad de edad adecuada y confirmar idioma, entrada y plazas antes del viaje.'),
        source=url,references=refs((T('Официальный календарь сети','Calendario oficial de la red'),NETWORK)),
        proof=T('Дата прочитана в официальном календаре; локальная страница проверена отдельно, различия сезонов сохранены.','Fecha leída en calendario oficial; página local comprobada aparte, diferencias entre temporadas conservadas.'),
        checked=CHECKED,status='Идея',note='',themes=['makers','technology'],participation='visitor',admission_kind='open_application',evidence_level='event_page')
    return expo(e,'family' if family else 'confirm_children')

def programme(ident,slug,provider,country,iso,place,start,end,url):
    detail=T('Возраст, сопровождение и язык выбранной мастерской ещё подтвердить; место не забронировано.',
             'Confirmar edad, acompañamiento e idioma del taller elegido; plaza sin reservar.')
    return dict(id=ident,slug=slug,provider=provider,country=country,iso=iso,place=place,themes=['makers','technology'],formats=['day'],
        catalog_participation='holiday_workshop',age=T('Минимальный возраст не опубликован.','Edad mínima sin publicar.'),language=UNKNOWN_LANG,confirmed_instruction_languages=[],
        programme='',timing=dict(status='published_2026',label=T('Опубликовано окно мастерских, не смена детского лагеря.','Periodo de talleres publicado, no sesión de campamento infantil.'),sessions=[[start,end]],
            session_details=[dict(start=start,end=end,label=T('Мастерские фестиваля','Talleres del festival'),date_scope='workshop_window',date_precision='published_window',entry=detail,source=url,price=UNPRICED)]),
        price=dict(year=2026,currency='',amount=None,unit='programme',label=UNPRICED,included=T('Включения выбранной активности уточнить.','Confirmar inclusiones de actividad elegida.'),
            extras=T('Поездка, сопровождение, техника и материалы: итоговые обязательные расходы ещё не установлены.','Viaje, acompañamiento, equipo y materiales: gastos obligatorios finales aún sin determinar.'),
            deposit=T('Оплата и отмена по письменным условиям выбранного предложения; запись не выполнена.','Pago y cancelación según condiciones escritas de oferta elegida; sin inscripción realizada.')),
        accommodation=T('Короткая очная мастерская; проживание и присмотр без родителей не заявлены.','Taller presencial breve; alojamiento y cuidado sin padres no anunciados.'),
        family_fit={k:dict(status='conditional',detail=detail) for k in ['matvey','oscar']},editorial_reason=detail,shortlist=[],
        questions=[detail,T('Получить окончательный прайс, требования к технике, время, материалы и правила отмены.','Obtener precio final, requisitos de equipo, horario, materiales y cancelación.')],
        sources=[dict(title=provider,url=url,checked=CHECKED)],checked=CHECKED)

def programme_additions():
    alpha=programme('CP1161','shenzhen-alpha-maker-workshops-2026','ALPHA Camp · Maker Faire Shenzhen 2026','Китай','CHN','Shenzhen · Nanshan · Vanke Cloud Design Commune','2026-12-12','2026-12-13',ALPHA)
    alpha['programme']=T('Двухдневное maker-пространство; примерно 40 мастерских планируются, а не подтверждены расписанием. Роботы, ROS, ИИ на устройствах, электроника и цифровое производство перечислены как возможные темы. Это не объявленный детский лагерь: возраст, присмотр и фактический язык ведущих неизвестны.',
        'Espacio maker de dos días; se planean unos 40 talleres, sin horario confirmado. Robots, ROS, IA en dispositivos, electrónica y fabricación digital son temas posibles. No se anuncia como campamento infantil: edad, supervisión e idioma real de instructores desconocidos.')
    alpha['price'].update(currency='USD',amount=59.9,unit='person_two_day_pass',label=T('Ранний двухдневный пропуск 59.9 USD на человека до 20 ноября; обычный 89.9 USD. Изначально 100 ранних пропусков, не текущий остаток. Это цена ALPHA, не полный семейный бюджет.',
        'Pase anticipado de dos días 59.9 USD por persona hasta 20 de noviembre; ordinario 89.9 USD. Cupo inicial de 100 pases anticipados, no saldo actual. Precio ALPHA, no presupuesto familiar completo.'),
        included=T('Два дня ALPHA, NFC badge, обед в каждый день, maker passport и предварительное бронирование мастерских. Сертификат только после требований занятий / заданий; это не победа в международной лиге.',
            'Dos días ALPHA, NFC badge, almuerzo cada día, maker passport y reserva anticipada de talleres. Certificado solo tras requisitos de actividades / retos; no es victoria en liga internacional.'),
        extras=T('Индивидуальные мастерские ограничены местами и требуют резерва. Цены занятий и материалы будут публиковаться постепенно; их включение в пропуск и вход на весь Maker Faire не подтверждены. Налоги, сборы, взрослый сопровождающий и поездка отдельно уточняются.',
            'Talleres individuales con plazas limitadas y reserva. Precios y materiales se publicarán progresivamente; sin confirmar su inclusión en pase ni acceso a todo Maker Faire. Confirmar impuestos, cargos, adulto acompañante y viaje.'))
    alpha['editorial_reason']=T('Интересный опыт мастерской рядом с электроникой Shenzhen; возрастной допуск семьи и язык ещё не подтверждены, поэтому не проверенный топ детских лагерей.',
        'Experiencia de taller interesante junto a electrónica de Shenzhen; admisión familiar por edad e idioma aún sin confirmar, por ello no figura como mejor campamento infantil verificado.')
    alpha['sources'].append(dict(title=T('Официальный магазин: валюта USD и ранний пропуск','Tienda oficial: moneda USD y pase anticipado'),url=ALPHA_SHOP,checked=CHECKED))
    alpha['timing']['session_details'][0]['price']=alpha['price']['label']
    alpha['timing']['session_details'][0]['extras']=alpha['price']['extras']
    bilbao=programme('CP1162','bilbao-family-electronics-2026',T('Maker Faire Bilbao · семейная электроника','Maker Faire Bilbao · electrónica familiar'),'Испания','ESP','Bilbao · Zorrotzaurre · Fábrica Artiach, Ribera de Deusto 70','2026-11-21','2026-11-22',BILBAO_PROGRAMME)
    bilbao['age']=T('От 6 лет обязательно с взрослым. Оскару нужен уже исполненный шестой день рождения к занятию.','Desde 6 años obligatoriamente con adulto. Oscar debe haber celebrado su sexto cumpleaños antes de actividad.')
    bilbao['programme']=T('Семейная пайка и программирование; примеры изделий — шагающий робот, лампа и звуковой контур. Каждая семья забирает сделанное. Точный набор изделий, распределение по дням и часы ещё не объявлены.',
        'Soldadura y programación en familia; ejemplos de creaciones: robot caminante, lámpara y circuito sonoro. Cada familia se lleva su creación. Productos concretos, distribución por días y horas aún sin anunciar.')
    bilbao['timing']['label']=T('21–22 ноября 2026: окно семейных мастерских; часы и запись будут опубликованы. Это не двухдневная смена с присмотром.',
        '21–22 de noviembre de 2026: periodo de talleres familiares; horas y reserva pendientes de publicación. No es sesión de dos días con cuidado infantil.')
    bilbao['price'].update(currency='EUR',amount=0,unit='activity',label=T('Все мероприятия программы 2026 бесплатны. Места семейных мастерских ограничены; запись ещё должна открыться. Поездка и расходы семьи отдельно.',
        'Todas las actividades del programa 2026 son gratuitas. Plazas de talleres familiares limitadas; reserva aún por abrir. Viaje y gastos familiares aparte.'),
        included=T('Участие и изготовленный семьёй предмет; окончательный выбор мастерской и материалов ещё уточнить.','Participación y objeto creado por familia; confirmar selección final de taller y materiales.'))
    bilbao['family_fit']['matvey']=dict(status='candidate',detail=T('По возрасту подходит: от 6, обязательно с взрослым. Язык, место и запись ещё подтвердить.','Edad compatible: desde 6, obligatoriamente con adulto. Confirmar idioma, plaza y reserva.'))
    bilbao['family_fit']['oscar']=dict(status='conditional',detail=bilbao['age'])
    bilbao['sources'].append(dict(title=T('Главная страница: от 6 лет с взрослым','Página principal: desde 6 con adulto'),url=BILBAO,checked=CHECKED))
    bilbao['timing']['session_details'][0].update(age=bilbao['age'],price=bilbao['price']['label'],entry=T('Запись на сайте ещё должна открыться; взрослый участвует вместе с ребёнком.','Reserva en web aún por abrir; adulto participa junto con niño.'),availability=dict(status='not_yet_open',note=T('Места ограничены, запись анонсирована как предстоящая.','Plazas limitadas, reserva anunciada como próxima.')))
    robot=programme('CP1163','monterrey-talking-robots-2026','Maker Faire Monterrey · Talking Robots','Мексика','MEX','Monterrey · HUB de Innovación y Emprendimiento · Prototyping Lab','2026-11-12','2026-11-12',MONTERREY)
    robot['themes']=['robotics','ai','makers']
    robot['programme']=T('Talking Robots: управление физическими устройствами через разговорные инструкции ИИ. Описан отдельный мастер-класс 17:00–18:00, хотя общий билет Expo указан 09:00–17:00. Возраст детей и сопровождение к этой мастерской не установлены.',
        'Talking Robots: controlar dispositivos físicos con instrucciones conversacionales de IA. Taller separado 17:00–18:00, aunque entrada general Expo indica 09:00–17:00. Edad infantil y acompañamiento de este taller sin determinar.')
    robot['timing']['label']=T('12 ноября 2026, 17:00–18:00, America/Monterrey; отдельная мастерская после указанного конца общей Expo.','12 de noviembre de 2026, 17:00–18:00, America/Monterrey; taller separado tras final anunciado de Expo general.')
    robot['price'].update(currency='',amount=0,unit='workshop',label=T('Публичная конфигурация конкретного билета: type=free. Материалы, техника, возрастной допуск и подтверждение места отдельно; общий бесплатный билет не бронирует мастерскую.',
        'Configuración pública de entrada concreta: type=free. Materiales, equipo, admisión por edad y confirmación de plaza aparte; entrada general gratuita no reserva taller.'))
    robot['timing']['session_details'][0].update(price=robot['price']['label'],date_scope='session_days',sessions=[dict(date='2026-11-12',start_time='17:00',end_time='18:00',timezone='America/Monterrey',topic='Talking Robots',ical_timed=True,start_utc='2026-11-12T23:00:00Z',end_utc='2026-11-13T00:00:00Z')],
        entry=T('Отдельный тип билета. Текущая публичная конфигурация: require_approval=false; это не подтверждает принятие детей. Подтвердить возраст, взрослого и место; регистрация не выполнена.',
            'Tipo de entrada separado. Configuración pública actual: require_approval=false; no acredita admisión infantil. Confirmar edad, adulto y plaza; sin inscripción realizada.'))
    return [alpha,bilbao,robot]

def enrich_v146(d):
    idx={e['id']:e for e in d['events']};new=[]
    e=new_event('E202','Maker Faire Lynchburg 2027','США','USA','Lynchburg · Randolph College','2027-03-14','2027-03-14','https://lynchburg.makerfaire.com/',True)
    e.update(cost=T('Посещение бесплатно; регистрация помогает планированию. Она также включает розыгрыш, который не является международной наградой.','Asistencia gratuita; registro ayuda a planificación. Incluye sorteo, que no constituye premio internacional.'),
        note=T('11:00–17:00. Отдельная форма спрашивает взрослых и детей; конкретные мастерские и расписание будут опубликованы.','11:00–17:00. Formulario separado pregunta por adultos y menores; talleres concretos y horario pendientes.'),
        references=refs((T('Бесплатный вход и семейная регистрация 2027','Entrada gratuita y registro familiar 2027'),'https://lynchburg.makerfaire.com/tickets/')));new.append(e)
    e=new_event('E203','Maker Faire Ulaanbaatar 2027','Монголия','MNG',T('Улан-Батор · точная площадка ещё не подтверждена','Ulán Bator · sede exacta aún sin confirmar'),'2027-05-08','2027-05-09',NETWORK)
    e.update(evidence_level='catalog',note=T('Дата из официальной сети. Локальная ссылка dudu.mn пока описывает семейную программу 2021 в Terelj; это не подтверждение площадки, языка, цены или лагеря 2027.','Fecha de red oficial. Enlace local dudu.mn aún describe programa familiar 2021 en Terelj; no acredita sede, idioma, precio ni campamento 2027.'),references=refs((T('Локальная ссылка: старый материал 2021','Enlace local: material antiguo 2021'),'https://dudu.mn/')));new.append(e)
    e=new_event('E204','Maker Faire Trieste 2027','Италия','ITA',T('Trieste · площадка 2027 уточняется','Trieste · sede 2027 pendiente'),'2027-05-22','2027-05-23','https://trieste.makerfaire.com/en/home-page/')
    e.update(evidence_level='catalog',note=T('Сеть объявляет 22–23 мая 2027. Локальная страница ещё про 9–10 мая 2026; её бесплатный вход и Piazza Unità d’Italia не перенесены в условия 2027.','Red anuncia 22–23 de mayo de 2027. Página local aún trata 9–10 de mayo de 2026; entrada gratuita y Piazza Unità d’Italia no se trasladan a condiciones 2027.'));new.append(e)
    e=new_event('E205','Southeast Minnesota Maker Faire 2027','США','USA','Owatonna · Minnesota','2027-06-12','2027-06-12','https://southeastminnesota.makerfaire.com/',True)
    e['note']=T('Город и дата прямо на локальной странице; конкретное здание, часы и тариф пока не установлены. Не путать с Rochester, New York.','Ciudad y fecha expresas en página local; edificio, horas y tarifa aún sin determinar. No confundir con Rochester, New York.');new.append(e)
    e=new_event('E206','Los Angeles Maker Faire 2027','США','USA','Los Angeles · Central Library','2027-07-31','2027-07-31','https://losangeles.makerfaire.com/')
    e['note']=T('Официальная сеть указывает 2027; локальный заголовок — July 31, 10:00–16:00 и Central Library без года. Меню экспонентов ещё 2026. Детский вход, билет и состав 2027 отдельно подтвердить.','Red oficial indica 2027; cabecera local July 31, 10:00–16:00 y Central Library sin año. Menú de expositores sigue 2026. Confirmar entrada infantil, billete y programa 2027.');new.append(e)
    e=new_event('E207','Long Island Maker Faire 2027','США','USA',T('Long Island · площадка 2027 уточняется','Long Island · sede 2027 pendiente'),'2027-09-19','2027-09-19','https://longisland.makerfaire.com/')
    e.update(evidence_level='catalog',note=T('Дата 19 сентября 2027 из сети. Локальная страница ещё про 6 июня 2026 в Stony Brook; эта площадка, тариф и список makers не объявлены для 2027.','Fecha 19 de septiembre de 2027 de red. Página local aún trata 6 de junio de 2026 en Stony Brook; sede, tarifa y lista maker no anunciadas para 2027.'));new.append(e)
    e=new_event('E208','Maker Faire Bay Area 2027','США','USA','California · Mare Island','2027-09-24','2027-09-26','https://makerfaire.com/bay-area/?2026')
    e.update(scope='international',note=T('Страница с параметром 2026 прямо объявляет возвращение 24–26 сентября 2027 на Mare Island. Дни общего семейного входа, пятничный школьный режим, билеты и мастерские 2027 ещё не установлены. Старые скидки и программа 2026 не перенесены.','Página con parámetro 2026 anuncia expresamente regreso 24–26 de septiembre de 2027 a Mare Island. Días de entrada familiar, régimen escolar del viernes, entradas y talleres 2027 aún sin determinar. Descuentos y programa 2026 no se trasladan.'));new.append(e)
    e=new_event('E209','Maker Faire Bilbao 2026','Испания','ESP','Bilbao · Zorrotzaurre; Meñaka · Bizkaia','2026-11-16','2026-11-22',BILBAO_PROGRAMME,True)
    e.update(cost=T('Все мероприятия программы 2026 бесплатны; ограниченные мастерские требуют записи, которая ещё должна открыться.','Todas las actividades del programa 2026 son gratuitas; talleres limitados requieren reserva aún por abrir.'),
        age=T('Семейная электроника 21–22 ноября — от 6 лет с взрослым; другие активности по собственным условиям.','Electrónica familiar 21–22 de noviembre — desde 6 con adulto; otras actividades con condiciones propias.'),
        note=T('Неделя в нескольких местах, а не ежедневная семейная выставка: учебные / профессиональные визиты по записи; семейные мастерские только 21–22. Открытая 3D-печать 21 ноября с 11:30, разговор 13:00. Язык конкретного ведущего не установлен.','Semana en varias sedes, no exposición familiar diaria: visitas educativas / profesionales con cita; talleres familiares solo 21–22. Impresión 3D abierta 21 de noviembre desde 11:30, charla 13:00. Idioma de instructor concreto sin determinar.'),
        references=refs((T('Возраст семейной электроники и будущая запись','Edad de electrónica familiar y reserva futura'),BILBAO)));new.append(e)
    e=new_event('E210',T('Maker Faire Orlando · Field Trip Day 2026 · набор закрыт','Maker Faire Orlando · Field Trip Day 2026 · convocatoria cerrada'),'США','USA','Orlando · Central Florida Expo Center & Fairgrounds','2026-11-06','2026-11-06',ORLANDO+'field-trip-day/')
    closed=T('Нет нового допуска: достигнута вместимость, принимают только уже записанных участников.','Sin admisión nueva: aforo completo, solo participantes ya inscritos.')
    e.update(priority='P4 — '+T('набор заполнен','convocatoria completa'),mat=closed,osc=closed,entry=closed,adult_entry=closed,
        cost=T('Бесплатно для допустимых школьных групп и подтверждённого homeschool / full-time virtual student плюс одного взрослого на ученика. Набор уже закрыт.','Gratis para grupos escolares admitidos y homeschool / full-time virtual student acreditado más un adulto por alumno. Convocatoria ya cerrada.'),
        availability=dict(status='closed',note=closed),registration_status=closed,
        note=T('6 ноября 10:00–15:00, только предварительно записанные школьные группы и подтверждённые homeschool / virtual families. Взрослый присмотр обязателен. Этот вход не действует на публичные 7–8 ноября; обычной семье нельзя приехать без подтверждения.','6 de noviembre 10:00–15:00, solo grupos escolares y homeschool / virtual families acreditadas e inscritas previamente. Supervisión adulta obligatoria. Esta entrada no vale para 7–8 de noviembre públicos; familia ordinaria no puede llegar sin confirmación.'),
        parent_event_id='E008')
    # A closed group preview is kept in the full catalogue, not promoted as a
    # public exhibition visit in the independent exhibition calendar.
    e.pop('exhibition_tier');new.append(e)
    for e in new:
        if e['id'] in idx:idx[e['id']].update(e)
        else:d['events'].append(e);idx[e['id']]=e
    idx['E210'].pop('exhibition_tier',None)
    for ident in ['E008','E070','E071','E072','E075','E076']:
        e=idx[ident];expo(e,'family' if ident in ['E008','E070','E075','E076'] else 'confirm_children');e['checked']=CHECKED
    orlando=idx['E008'];orlando.update(source=ORLANDO+'attend/',
        cost=T('USD: предпродажа один день adult 20 / youth-student 15, два дня 30 / 25; обычные один день 25 / 20, два дня 35 / 30. Возраст границы youth и финальные сборы ещё подтвердить. Нулевая строка Support the Maker Effect Foundation — пожертвование, не бесплатный билет.',
            'USD: anticipada un día adult 20 / youth-student 15, dos días 30 / 25; ordinaria un día 25 / 20, dos días 35 / 30. Confirmar corte youth y cargos finales. Línea cero Support the Maker Effect Foundation es donación, no entrada gratuita.'),
        note=T('7–8 ноября 10:00–17:00, бесплатная парковка. Билет включает просмотр Robot Ruckus, не соревновательное участие. Пятничный школьный Field Trip Day 6 ноября — отдельно и уже заполнен. Льготы EBT / educators / military требуют своих доказательств.','7–8 de noviembre 10:00–17:00, aparcamiento gratuito. Entrada incluye ver Robot Ruckus, no competir. Field Trip Day escolar del viernes 6 de noviembre es separado y ya completo. Descuentos EBT / educators / military exigen acreditación propia.'),
        references=refs((T('Официальный билет: тарифы USD','Entrada oficial: tarifas USD'),'https://events.humanitix.com/makerfaireorlando'),(T('Отдельный закрытый школьный день','Día escolar separado y cerrado'),ORLANDO+'field-trip-day/')),
        related_ids=['E210'])
    rochester=idx['E070'];rochester.update(cost=T('Не подтверждено для 2026. Attend содержит шапку 21 ноября 2026, но билет 2025 и старые $12/40, $15/50 с 15 ноября; новый TicketLeap не раскрыл тариф. Эти суммы не приняты как текущие.',
        'Sin confirmar para 2026. Attend tiene cabecera 21 de noviembre de 2026, pero entrada 2025 y antiguos $12/40, $15/50 con 15 de noviembre; TicketLeap nuevo no mostró tarifa. Esas cifras no se aceptan como actuales.'),
        note=T('21 ноября 09:00–17:00, RIT Gordon Field House. Страница пишет individual 5+, family 2 adults + 3 children 5–18 и до 4 бесплатно, но блок смешан с 2025: тариф и применимость условий детям подтвердить. Student STEAM Fest 20 ноября отдельно.','21 de noviembre 09:00–17:00, RIT Gordon Field House. Página dice individual 5+, family 2 adults + 3 children 5–18 y hasta 4 gratis, pero bloque mezclado con 2025: confirmar tarifa y condiciones infantiles. Student STEAM Fest 20 de noviembre separado.'),
        references=refs((T('Attend: свежая дата и старый билетный блок','Attend: fecha nueva y bloque de entradas antiguo'),'https://rochester.makerfaire.com/attend/'),(T('Билет 2026: тариф не удалось прочитать','Entrada 2026: tarifa sin poder leer'),'https://events.ticketleap.com/tickets/maker-faire-rochester/2026')))
    idx['E071'].update(source='https://www.iamas.ac.jp/ommf2026/',note=T('5 декабря 12:00–17:00, 6 декабря 10:00–16:00, Softopia Japan Center Building. Заявки makers закрыты; это не закрытие посещения. Детский вход, EN/ES и тариф не опубликованы. Суммы спонсорства не билеты.','5 de diciembre 12:00–17:00, 6 de diciembre 10:00–16:00, Softopia Japan Center Building. Propuestas maker cerradas; no implica cierre al público. Entrada infantil, EN/ES y tarifa sin publicar. Importes de patrocinio no son entradas.'))
    idx['E072'].update(start='2026-12-09',end='2026-12-09',evidence_level='catalog',references=refs((T('Текущая дата сети: 9 декабря','Fecha actual de red: 9 de diciembre'),NETWORK)),
        note=T('Сеть теперь указывает только 9 декабря 2026 вместо прежних 8–12. Локальная страница описывает makerspace, но не подтверждает площадку Faire, детский билет и язык. Бесплатный walk-around не равен входу на фестиваль.','Red ahora indica solo 9 de diciembre de 2026 en lugar de anteriores 8–12. Página local describe makerspace, sin acreditar sede Faire, entrada infantil ni idioma. Walk-around gratuito no equivale a entrada al festival.'))
    idx['E075']['note']=T('Локальный анонс Summer 2027, сеть — июнь 2027 без дня. Дата остаётся пустой; старый тариф и бесплатный возраст не объявлены условиями 2027.','Anuncio local Summer 2027, red junio de 2027 sin día. Fecha sigue vacía; tarifa y edad gratuita antiguas no se declaran condiciones 2027.')
    idx['E075']['cost']=UNPRICED
    idx['E076'].update(note=T('21 августа 10:00–18:00, 22 августа 10:00–17:00; Hannover Congress Centrum. Семейный формат прямо подтверждён. Прайс, конкретные мастерские и EN/ES 2027 ещё уточнить; каталог экспонентов и программа по ссылкам пока 2026.','21 de agosto 10:00–18:00, 22 de agosto 10:00–17:00; Hannover Congress Centrum. Formato familiar expresamente confirmado. Confirmar precios, talleres concretos y EN/ES 2027; enlaces de expositores y programa aún 2026.'))
    shenzhen=idx['E009'];shenzhen.update(checked=CHECKED,source=SHENZHEN,
        entry=T('Правила общего посетительского билета и детского входа 2026 ещё подтвердить. Заявка makers до 30 октября уже прошла; ALPHA — отдельный платный пропуск и резерв мастерских.','Confirmar reglas de entrada general e infantil 2026. Plazo de propuesta maker 30 de octubre ya pasado; ALPHA es pase pagado y reserva de talleres aparte.'),
        note=T('12–13 декабря, Vanke Design Commune, Nanshan. Новость 28 октября объявляет первые 98 стендов, не окончательное число компаний. У ALPHA возможны роботы / ИИ, но возраст и язык не подтверждены.','12–13 de diciembre, Vanke Design Commune, Nanshan. Noticia 28 de octubre anuncia primeros 98 puestos, no número final de empresas. ALPHA puede incluir robots / IA, pero edad e idioma sin confirmar.'),
        references=refs((T('ALPHA: отдельные мастерские и пропуск','ALPHA: talleres y pase separados'),ALPHA)))
    shenzhen['adult_entry']=shenzhen['entry']
    monterrey=idx['E066'];monterrey.update(title='Maker Faire Monterrey / ITERA TEC 2026',source=MONTERREY,checked=CHECKED,start='2026-11-12',end='2026-11-12',date_status='Подтверждено',date_scope='festival_window',
        city='Monterrey · HUB de Innovación y Emprendimiento Eduardo Garza T. · Av. Eugenio Garza Sada 2501 Sur',
        cost=T('General и Talking Robots имеют type=free в публичной конфигурации билетов. Материалы и другие обязательные расходы выбранной активности уточнить.','General y Talking Robots tienen type=free en configuración pública de entradas. Confirmar materiales y otros gastos obligatorios de actividad elegida.'),
        entry=T('Текущая ссылка официальной сети ведёт на событие Tec de Monterrey в Luma. Выбрать General и нужную мастерскую отдельно; проверить детский возраст и сопровождение. Регистрация не выполнялась.','Enlace actual de red oficial lleva a evento Tec de Monterrey en Luma. Elegir General y taller deseado por separado; comprobar edad infantil y acompañamiento. Sin registro realizado.'),
        note=T('Новая официальная ссылка и страница хозяина согласуются: четверг 12 ноября 2026. Старые 29–30 октября / 19–20 ноября больше не основной анонс. Общая Expo 09:00–17:00, Talking Robots отдельно 17:00–18:00. Возраст и EN/ES преподавание не подтверждены.','Enlace oficial nuevo y página anfitriona coinciden: jueves 12 de noviembre de 2026. Antiguos 29–30 de octubre / 19–20 de noviembre ya no son anuncio principal. Expo general 09:00–17:00, Talking Robots separado 17:00–18:00. Edad e instrucción EN/ES sin confirmar.'),
        proof=T('Прослежена свежая ссылка из официального календаря сети в Luma; прочитаны описание хозяина, дата, площадка и публичная конфигурация билетов. Противоречие старой ссылки устранено новым текущим анонсом.','Seguido enlace nuevo desde calendario oficial a Luma; leídos descripción anfitriona, fecha, sede y configuración pública de entradas. Conflicto antiguo resuelto por anuncio actual nuevo.'),references=refs((T('Официальная сеть с новой ссылкой Monterrey','Red oficial con enlace nuevo Monterrey'),NETWORK)))
    expo(monterrey)
    for pid,parent in [('CP1161','E009'),('CP1162','E209'),('CP1163','E066')]:
        for child in d['events']:
            if child.get('camp_programme_id')==pid:
                child['parent_event_id']=parent;child['priority']='P3 — '+T('возраст и язык мастерской уточнить','confirmar edad e idioma del taller')
                idx[parent]['related_ids']=list(dict.fromkeys(idx[parent].get('related_ids',[])+[child['id']]))
    for e in list(idx.values()):
        if e['id'] in {x['id'] for x in new}|{'E008','E009','E066','E070','E071','E072','E075','E076'}:
            e['adult_entry']=e['entry']
    urls={s['url'] for s in d['sources']}
    for e in list(idx.values()):
        if e.get('checked')!=CHECKED:continue
        for ref in [dict(label=e['title'],url=e['source'])]+e.get('references',[]):
            if ref['url'] not in urls:
                d['sources'].append(dict(url=ref['url'],title=ref['label'],evidence='official-primary',checked=CHECKED));urls.add(ref['url'])
