"""Current Mexican competitions and Costa Rican holiday courses, 4 November 2026."""
from copy import deepcopy
from datetime import date, timedelta

CHECKED = '2026-11-04'
SPANISH = {}


def T(ru, es):
    SPANISH[ru] = es
    return ru


BEBRAS = 'https://bebras.mx/'
BEBRAS_RULES = 'https://bebras.mx/wp-content/uploads/2026/08/Bebras-Otono-2026-%C2%B7-Convocatoria-Detalle.pdf'
ROBOJAM = 'https://www.robojam.live/mexico'
CHALLENGES = 'https://www.robojam.live/challenges'
FOD_ARTICLE = 'https://fod.ac.cr/noticias/mas-alla-de-las-pantallas-por-que-es-importante-que-ninas-ninos-y-adolescentes-aprendan-a-crear-con-tecnologia/'
FOD_FORM = 'https://survey.zohopublic.com/zs/SjzWbS'
TEAM = T('До 3 участников + взрослый наставник; минимальный размер команды отдельно не указан.',
         'Hasta 3 participantes + asesor adulto; el tamaño mínimo del equipo no se indica por separado.')
RJ_COST = T('Опубликованы тарифы: до 11.12.2026 — 450 MXN / 25 USD / 80000 COP; до 15.01.2027 — 630 MXN / 35 USD / 112000 COP; до 26.02.2027 — 900 MXN / 50 USD / 160000 COP. Единицу оплаты и несколько дисциплин подтвердить; робот, дорога и жильё отдельно.',
            'Tarifas publicadas: hasta 11.12.2026 — 450 MXN / 25 USD / 80000 COP; hasta 15.01.2027 — 630 MXN / 35 USD / 112000 COP; hasta 26.02.2027 — 900 MXN / 50 USD / 160000 COP. Confirmar unidad de pago y varias disciplinas; robot, transporte y alojamiento aparte.')
RJ_ENTRY = T('Очный этап ASFM открыт командам любой страны; регистрация с 02.11.2026. Дисциплина проводится при минимум 5 командах; максимум 5 регистраций одного клуба в одном испытании. Это заявка на конкретный этап, без автоматического мирового отбора.',
             'Etapa presencial ASFM abierta a equipos de cualquier país; registro desde 02.11.2026. Cada reto requiere mínimo 5 equipos; máximo 5 inscripciones de un club por reto. Solicitud a esta etapa, sin clasificación mundial automática.')
RJ_NOTE = T('Прочитаны связанные испанские PDF редакции 25.06.2026. Местные изменения разрешены организатором: до оплаты сверить редакцию 2027 и возрастную отсечку. На странице указано 20:00, но строка часового пояса сочетает -6 GMT и PDT; UTC не назначен. Разрешение на данные и изображение указано до 14 марта. Регистрацию, согласия и оплату семьи не оформляли.',
            'Leídos los PDF españoles enlazados, edición 25.06.2026. Se permiten cambios locales: antes del pago confirmar edición 2027 y corte de edad. La página indica 20:00, pero mezcla -6 GMT y PDT; no se asigna UTC. Autorización de datos e imagen indicada antes del 14 de marzo. Sin registro, consentimiento ni pago familiar.')
RJ_AWARD = T('Первые 3 места: аккредитации на одно событие ROBOJAM по регламенту; остальные могут запросить сертификат участия. Конкретное следующее событие и дополнительные призы не названы; сертификат участия не равен призовому месту.',
             'Primeros 3 puestos: acreditaciones para un evento ROBOJAM según reglamento; los demás pueden solicitar certificado de participación. Próximo evento y premios adicionales sin identificar; certificado distinto de puesto premiado.')
RJ_LANGUAGE = T('Регламенты ES прочитаны; краткая страница двуязычная. Язык судейства и помощь на EN отдельно не подтверждены.',
                'Reglamentos ES leídos; web breve bilingüe. Idioma de jueces y asistencia EN sin confirmar por separado.')
RJ_GATE = T('Условно: верхний возраст подходит; нижний порог, отсечку, самостоятельность и местный допуск подтвердить.',
            'Condicional: cumple edad máxima; confirmar mínimo, corte, autonomía y admisión local.')


def competition_rows():
    bebras = dict(id='C1170', block='Соревнования', title='Bebras México · Otoño 2026 · N1–N6',
        country='Мексика', region='Северная Америка', city=T('Онлайн из дома или школы; участие из Коста-Рики подтвердить', 'En línea desde casa o escuela; confirmar participación desde Costa Rica'),
        start='2026-11-09', end='2026-11-30', deadline='2026-11-30', period='', date_status='Подтверждено',
        age=T('6–18 лет, 1 класс primaria — конец bachillerato. N1: 1–2 классы; N2: 3–4; N3: 5–6. Категория определяется реальным классом.',
              '6–18 años, 1 de primaria — fin de bachillerato. N1: cursos 1–2; N2: 3–4; N3: 5–6. Categoría según curso escolar real.'),
        mat=T('Да по возрасту; подтвердить класс и участие из Коста-Рики.', 'Sí por edad; confirmar curso y participación desde Costa Rica.'),
        osc=T('Условно: исполненные 6 лет и минимум 1 класс; день рождения и класс неизвестны.', 'Condicional: 6 cumplidos y mínimo curso 1; cumpleaños y curso desconocidos.'),
        format=T('Индивидуально: одна непрерывная сессия 50 минут; семейная учётная запись управляет отдельными доступами детей.',
                 'Individual: una sesión continua de 50 minutos; cuenta familiar administra accesos separados de los hijos.'),
        entry=T('Родитель может вести семейную / homeschool учётную запись; школа не обязательна. Для детей в семейной записи CURP и email необязательны; самостоятельная запись ребёнка имеет другие требования. Ключи могут готовиться до 72 часов; рекомендуют зарегистрироваться до 9 ноября.',
                'Un progenitor puede administrar cuenta familiar / homeschool; escuela no obligatoria. CURP y email infantiles opcionales en modalidad familiar; registro independiente tiene otros requisitos. Claves pueden tardar hasta 72 horas; recomiendan registrarse antes del 9 de noviembre.'),
        gear=T('Устройство с интернетом на одного участника; компьютер, планшет или телефон. Робот и платная техника не нужны.',
               'Dispositivo con internet por participante; ordenador, tableta o teléfono. Sin robot ni equipo de pago.'),
        language=T('Испанский прямо указан в convocatoria.', 'Español indicado expresamente en la convocatoria.'), languages=['ES'], language_mode='primary',
        cost=T('Бесплатно: convocatoria объявляет 100% gratuita.', 'Gratis: convocatoria indica 100% gratuita.'),
        level=T('C — национальная редакция международного Bebras', 'C — edición nacional de Bebras internacional'),
        reward=T('Цифровые результаты и признание; ориентир публикации около 7 декабря ещё не подтверждён. Это не мировой финал робототехники.',
                 'Resultados y reconocimientos digitales; publicación hacia el 7 de diciembre aún sin confirmar. No es final mundial de robótica.'),
        priority=T('P0 — бесплатный ближайший онлайн-вариант', 'P0 — opción próxima gratuita en línea'),
        action=T('Проверить класс, день рождения Оскара и дистанционный допуск семьи из CR; затем родителю самостоятельно выбрать семейный маршрут. Доступы готовить заранее, не в последний день.',
                 'Comprobar curso, cumpleaños de Oscar y admisión familiar desde CR; después el progenitor elige la modalidad familiar. Preparar claves con antelación.'),
        source=BEBRAS, proof=T('Прочитаны convocatoria на 3 страницах, главная и описание семейного участия; даты, бесплатность, ES и данные учётной записи проверены.',
                              'Leídas convocatoria de 3 páginas, portada y modalidad familiar; verificadas fechas, gratuidad, ES y datos de cuenta.'),
        checked=CHECKED, status='Идея',
        note=T('Регистрация открыта с 19 октября и продолжается до 30 ноября; 9 ноября — рекомендуемый срок, не обязательный дедлайн. Официальная схема позволяет домашнюю сдачу, но проживание вне Мексики отдельно не оговорено. Никакой учётной записи семьи не создавали.',
               'Registro desde el 19 de octubre hasta el 30 de noviembre; 9 de noviembre es recomendación, no plazo obligatorio. Se permite realizar desde casa, pero residencia fuera de México sin regular por separado. No se creó cuenta familiar.'),
        deadline_note=T('Последний день регистрации 30.11.2026; час и UTC не опубликованы. До 72 часов на ключи; не планировать регистрацию и сдачу в последний день.',
                        'Último día de registro 30.11.2026; hora y UTC no publicados. Hasta 72 horas para claves; evitar registro y prueba el último día.'),
        themes=['coding'], scope='national', participation='individual', admission_kind='open_application', evidence_level='rules', date_scope='assessment_window',
        references=[dict(label=T('Официальная convocatoria 2026','Convocatoria oficial 2026'),url=BEBRAS_RULES),dict(label=T('Семейный маршрут','Modalidad familiar'),url='https://bebras.mx/participa/')])
    base = dict(block='Соревнования',country='Мексика',region='Северная Америка',city='ASFM · Av. Dr. Ignacio Morones Prieto 1500 · Santa Catarina, Nuevo León',
        start='2027-04-17',end='2027-04-17',deadline='2027-02-26',period='',date_status='Подтверждено',
        format=TEAM,entry=RJ_ENTRY,language=RJ_LANGUAGE,languages=[],support_languages=['ES','EN'],language_mode='unconfirmed',cost=RJ_COST,
        level=T('B — международный Open на уровне отдельного этапа','B — Open internacional de una etapa concreta'),reward=RJ_AWARD,
        priority=T('P1 — открытый мексиканский этап; допуск отдельно','P1 — etapa mexicana abierta; admisión aparte'),
        action=T('Выбрать испытание и взрослого наставника; подтвердить возрастную отсечку, минимальную команду, места, единицу оплаты и редакцию правил до подготовки поездки.',
                 'Elegir reto y asesor adulto; confirmar corte de edad, equipo mínimo, plazas, unidad de pago y edición de reglas antes del viaje.'),
        source=ROBOJAM,proof=T('Мексиканская страница и 8 связанных испанских регламентов прочитаны; дата этапа, иностранный вход, возраст, команда и робот проверены раздельно.',
                            'Leídas web mexicana y 8 reglamentos españoles enlazados; verificados por separado fecha, entrada extranjera, edad, equipo y robot.'),
        checked=CHECKED,status='Идея',note=RJ_NOTE,themes=['robotics','coding'],scope='international',participation='team',admission_kind='open_application',evidence_level='rules',date_scope='festival_window',
        deadline_note=T('26.02.2027 20:00 по странице; противоречивое обозначение часового пояса требует уточнения, точный UTC не рассчитан.',
                        '26.02.2027 20:00 según web; zona horaria contradictoria pendiente, sin UTC exacto.'),
        references=[dict(label=T('Описание испытаний','Descripción de retos'),url=CHALLENGES)])
    parent=deepcopy(base);parent.update(id='C1171',title='RoboJam MX Norestense · ASFM · 2027',
        age=T('По испытанию: Bristle Race максимум 9; Path Attack Junior максимум 12; CrossBot максимум 15; остальные объявлены для любого возраста.',
              'Por reto: Bristle Race máximo 9; Path Attack Junior máximo 12; CrossBot máximo 15; restantes para cualquier edad.'),
        mat=RJ_GATE,osc=RJ_GATE,gear=T('Робот и поле зависят от выбранного испытания; Bristlebot, автономная программа и teleoperado имеют разные требования.',
                                     'Robot y pista según reto; Bristlebot, programa autónomo y teleoperado tienen requisitos distintos.'))
    rows=[bebras,parent]
    specs=[
      ('C1172','Bristle Race',0,9,T('Bristlebot 10 × 10 см, максимум 1 мотор и 9 V; щетинки вместо колёс/гусениц; дистанционный запуск запрещён. Дистанция 150 см.',
                               'Bristlebot 10 × 10 cm, máximo 1 motor y 9 V; cerdas en lugar de ruedas/orugas; inicio remoto prohibido. Distancia 150 cm.')),
      ('C1173','Path Attack Junior',4,12,T('Автономный робот 15 × 15 см на 10 шестиугольников. Без внешних датчиков; встроенные encoders, gyroscope и accelerometer допускаются. Во время официальной попытки нельзя программировать или дистанционно запускать.',
                                      'Robot autónomo 15 × 15 cm para 10 hexágonos. Sin sensores externos; encoders, gyroscope y accelerometer integrados permitidos. Sin programación ni inicio remoto durante intento oficial.')),
      ('C1174','CrossBot',2,15,T('Автономный робот 20 × 20 см; минимум 1 датчик распознавания цвета; одна программа для выбора зоны по цвету.',
                               'Robot autónomo 20 × 20 cm; mínimo 1 sensor para reconocer color; un programa para elegir zona según color.')),
      ('C1175','Skill Drive',6,None,T('Робот teleoperado 20 × 20 см, без датчиков наведения. Толкать предмет, не захватывать его; направляющие максимум 3.5 см. Раунд 120 секунд.',
                                   'Robot teleoperado 20 × 20 cm, sin sensores de guía. Empujar objeto sin agarrarlo; guías máximo 3.5 cm. Ronda 120 segundos.')),
      ('C1176','Stack.IN',7,None,T('Робот teleoperado 30 × 30 см, без датчиков наведения; предмет можно толкать или захватывать. Раунд 120 секунд.',
                                'Robot teleoperado 30 × 30 cm, sin sensores de guía; se puede empujar o agarrar objeto. Ronda 120 segundos.')),
      ('C1177','BumperBot Evolution',1,None,T('Автономный робот 20 × 20 см; одна программа независимо от старта. Удалить 10 препятствий за 120 секунд.',
                                           'Robot autónomo 20 × 20 cm; un programa independiente de la salida. Retirar 10 obstáculos en 120 segundos.')),
      ('C1178','Path Attack Pro',5,None,T('Робот teleoperado 15 × 15 см; без датчиков наведения; 5 шестиугольников и 5 препятствий. Pro здесь не означает автономный режим.',
                                       'Robot teleoperado 15 × 15 cm; sin sensores de guía; 5 hexágonos y 5 obstáculos. Pro no implica modo autónomo.')),
      ('C1179','Disk Derby',3,None,T('Робот teleoperado 20 × 20 см; без датчиков наведения; захватывать диски и доставлять в свою зону. Раунд 120 секунд.',
                                   'Robot teleoperado 20 × 20 cm; sin sensores de guía; agarrar discos y llevar a zona propia. Ronda 120 segundos.')),
    ]
    ids=['1kZnAbk3euwqJe8TvVFEnRGvJbJpslGKu','1_bsjNHppKRGpBd8IyGWnmNwP4Z85PFdY','1bSv88FAoh5xHH539hr9IiGAYu4_awKXY','1rianC2YLngELwIx_npHOLOV46dwE_X2t','1fyX_eHjw7JjtGsxRiBj7Zc_hl5wmltpl','1wfKwvELYUCqNaKoIPOB4PsOf98gP8Ui7','1s48BOFoZxwxQhjWFzUsQgYmqWCnrjwki','1z_9FW_6gRtcHLJ7V4J1qkM6Qce96YTqo']
    for ident,name,index,limit,gear in specs:
        e=deepcopy(base);rule='https://drive.google.com/file/d/'+ids[index]+'/view'
        age=T(f'Максимум {limit} лет по PDF; контрольная дата и нижняя граница не указаны.',f'Máximo {limit} años según PDF; fecha de corte y mínimo sin indicar.') if limit else T('Любой возраст по PDF; для несовершеннолетних нужен взрослый наставник.','Cualquier edad según PDF; menores necesitan asesor adulto.')
        e.update(id=ident,title='RoboJam MX Norestense · '+name+' · 2027',age=age,mat=RJ_GATE,osc=RJ_GATE,gear=gear,related_ids=['C1171'])
        e['references'].append(dict(label=T('Прочитанный регламент ES · 25.06.2026','Reglamento ES leído · 25.06.2026'),url=rule))
        if ident=='C1172':
            e['mat']=T('Условно: максимум 9 лет; на 17.04.2027 проходит только при рождении после 17.04.2017, если отсечка в день турнира. Правило отсечения подтвердить.',
                       'Condicional: máximo 9 años; al 17.04.2027 cumple solo si nació después del 17.04.2017, suponiendo corte el día del torneo. Confirmar regla de corte.')
            e['osc']=T('По верхнему возрасту подходит: в апреле 2027 будет 6–7; минимум и допуск подтвердить.','Cumple edad máxima: en abril 2027 tendrá 6–7; confirmar mínimo y admisión.')
            e['themes']=['robotics','makers']
        rows.append(e)
    for row in rows:
        row['language_certainty']=row['language']
        row['importance_reason']=T('Национальная редакция или отдельный открытый этап международной сети; место в мировом рейтинге не заявляется.',
                                   'Edición nacional o etapa abierta concreta de red internacional; sin puesto declarado en ranking mundial.')
    return rows


def age_fit(year, minimum, maximum, start):
    day=date.fromisoformat(start)
    ages=[day.year-born.year-((day.month,day.day)<(born.month,born.day)) for born in [date(year,1,1),date(year,12,31)]]
    low,high=min(ages),max(ages)
    status='later' if high<minimum else 'not_eligible' if low>maximum else 'conditional'
    detail=T(f'На начало возможны {low}–{high} лет; курс {minimum}–{maximum}. Точная дата рождения и правило отсечения неизвестны; язык, уровень и зачисление отдельно.',
             f'Al inicio puede tener {low}–{high} años; curso {minimum}–{maximum}. Cumpleaños exacto y corte desconocidos; idioma, nivel y admisión aparte.')
    return dict(status=status,detail=detail)


def camp_profiles_v141():
    # Date/year context is the form title: December 2026 and January 2027.
    programmes=[
      ('juguemos-robots','Juguemos a crear Robots',6,8,['robotics','coding'],[('2026-12-07','08:00','12:00'),('2027-01-11','08:00','12:00'),('2027-01-25','08:00','12:00')]),
      ('historias-animadas','Mis Historias Animadas',6,8,['coding','arts'],[('2027-01-18','08:00','12:00')]),
      ('creatividad-7-9','Creatividad y diseño con robótica · 7–9',7,9,['robotics','makers'],[('2027-01-25','08:00','12:00')]),
      ('robotica-nivel-1','Nivel 1 · Principios de construcción y programación',9,12,['robotics','coding'],[('2026-12-07','08:00','12:00'),('2027-01-11','08:00','12:00')]),
      ('robotica-nivel-2','Nivel 2 · Sistemas inteligentes: sensores y engranajes',9,12,['robotics','coding'],[('2027-01-18','08:00','12:00')]),
      ('robotica-nivel-3','Nivel 3 · Grados de libertad, sincronización y publicación',9,12,['robotics','coding'],[('2027-01-25','13:00','17:00')]),
      ('robotica-nivel-4','Nivel 4 · Líneas de procesamiento y acciones de datos',9,16,['robotics','coding'],[('2027-01-11','13:00','17:00')]),
      ('creatividad-10-12','Creatividad y diseño con robótica · 10–12',10,12,['robotics','makers'],[('2027-01-18','08:00','12:00')]),
      ('edificaciones-3d-nivel-1','Nivel 1 · Edificaciones en 3D',12,16,['technology','makers'],[('2026-12-07','08:00','12:00'),('2027-01-11','13:00','17:00'),('2027-01-18','08:00','12:00')]),
      ('edificaciones-3d-nivel-2','Nivel 2 · Edificaciones en 3D',12,16,['technology','makers'],[('2027-01-25','08:00','12:00')]),
      ('microplacas-nivel-1','Nivel 1 · Makers, Microplacas programables',12,16,['coding','makers'],[('2027-01-18','13:00','17:00')]),
      ('microplacas-nivel-2','Nivel 2 · Makers, Microplacas programables',12,16,['coding','makers'],[('2027-01-25','13:00','17:00')]),
    ]
    place='Fundación Omar Dengo · San José · Avenidas 10 y 12, Calle 25-A, Barrio Francisco Peralta'
    language=T('Публичная заявка и описание на ES; язык устного преподавания, поддержка EN и языковые требования отдельно не указаны.',
               'Solicitud pública y descripción en ES; idioma docente oral, apoyo EN y requisitos lingüísticos sin indicar por separado.')
    programme=T('В форме опубликованы название курса, возраст, даты и часы. Детальная программа, версия робототехники / устройства, размер группы и учебные результаты не раскрыты. 5 дней по 4 часа = 20 часов пребывания; перерывы отдельно не описаны.',
                'Formulario publica nombre, edad, fechas y horario. Temario detallado, versión del equipo / dispositivo, tamaño de grupo y resultados docentes sin detallar. 5 días de 4 horas = 20 horas de estancia; pausas sin describir.')
    price=T('60000 CRC за выбранный курс, IVAI включён. Проживание, дорога, питание и выдача техники домой не заявлены включёнными.',
            '60000 CRC por curso elegido, IVAI incluido. Alojamiento, transporte, comida y equipo para llevar no constan incluidos.')
    deposit=T('100% стоимости до курса. Нет возврата за неявку или прекращение участия; перенос даты участником не разрешён. Открытие зависит от минимального набора, число не указано; отмена оператором и её возврат отдельно не описаны.',
              '100% del precio antes del curso. Sin reembolso por inasistencia o abandono; sin cambio de fecha por participante. Apertura sujeta a mínimo de alumnos no especificado; cancelación del operador y su reembolso sin detallar.')
    questions=[T('Подтвердить язык преподавания, вход с паспортом / DIMEX, свободное место, точную возрастную отсечку и уровень.',
                 'Confirmar idioma docente, admisión con pasaporte / DIMEX, plaza, corte de edad y nivel.'),
               T('Уточнить робот, устройство, материалы, питание и полную сумму; для старших уровней проверить предварительную подготовку.',
                 'Aclarar robot, dispositivo, materiales, comida e importe total; comprobar preparación para niveles superiores.'),
               T('Родителям самостоятельно проверить условия оплаты, отмены и выбор согласия на изображение; эту форму не заполняли и не отправляли.',
                 'La familia revisa pago, cancelación y elección de consentimiento de imagen; formulario no completado ni enviado.')]
    out=[]
    for i,(slug,name,lo,hi,themes,starts) in enumerate(programmes,1124):
        details=[]
        for start,begin,finish in starts:
            end=(date.fromisoformat(start)+timedelta(days=4)).isoformat()
            fit={key:age_fit(year,lo,hi,start) for key,year in [('matvey',2017),('oscar',2020)]}
            details.append(dict(start=start,end=end,label=name,source=FOD_FORM,price=price,age=T(f'{lo}–{hi} лет по выбранному пункту формы',f'{lo}–{hi} años según opción del formulario'),
                family_fit=fit,date_scope='session_days',
                sessions=[dict(date=(date.fromisoformat(start)+timedelta(days=n)).isoformat(),start_time=begin,end_time=finish,timezone='America/Costa_Rica',topic=name,
                    time_note=T('Местное время; перерывы внутри блока не описаны','Hora local; pausas dentro del bloque sin describir')) for n in range(5)],
                proof=T('Публично прочитаны варианты курса в форме оператора: диапазон возраста, точные даты и часы. Поля семьи не вводили, отправку не выполняли.',
                        'Leídas opciones públicas del formulario del operador: edad, fechas y horas exactas. Sin datos familiares ni envío.')))
        fit={}
        for child in ['matvey','oscar']:
            states={v['family_fit'][child]['status'] for v in details}
            status=next(iter(states)) if len(states)==1 else 'conditional'
            fit[child]=dict(status=status,detail=T('Посменный допуск указан в расписании: возраст декабря и января может различаться. Язык, уровень и зачисление подтвердить.',
                                                 'Admisión por sesión en calendario: edad de diciembre y enero puede variar. Confirmar idioma, nivel y aceptación.'))
        out.append(dict(id=f'CP{i}',slug='fod-'+slug+'-2026-27',provider='FOD Líderes del Futuro · '+name,country='Коста-Рика',iso='CRI',place=place,themes=themes,formats=['day'],
            age=T(f'{lo}–{hi} лет; контрольную дату подтвердить, класс не заменяет возраст',f'{lo}–{hi} años; confirmar corte, curso escolar no sustituye edad'),
            language=language,confirmed_instruction_languages=[],programme=programme,
            timing=dict(status='published_2026_27',label=T('Декабрь 2026 — январь 2027; конкретные 5-дневные курсы по опубликованному расписанию.','Diciembre 2026 — enero 2027; cursos concretos de 5 días según horario publicado.'),
                sessions=[[v['start'],v['end']] for v in details],session_details=details,precision='published_sessions'),
            price=dict(year=2026,season='2026/27',currency='CRC',amount=60000,tax_included=True,unit='course',label=price,
                included=T('Объявленная цена курса с налогом; состав комплекта и предоставление устройства уточнить.','Precio de curso con impuesto; confirmar contenido del kit y préstamo de dispositivo.'),
                extras=T('Жильё и транспорт семьи отдельно; еда, расходники и устройство не детализированы.','Alojamiento y transporte familiar aparte; comida, materiales y dispositivo sin detallar.'),deposit=deposit),
            accommodation=T('Дневной курс в центральном офисе FOD; ночное проживание не предлагается.','Curso diurno en sede central FOD; sin alojamiento nocturno.'),
            family_fit=fit,editorial_reason=T('Близкий вариант с точным расписанием и ценой; это учебный курс, а не международная награда или доказанный мировой рейтинг лагерей.',
                                            'Opción próxima con horario y precio concretos; curso educativo, sin premio internacional ni ranking mundial demostrado.'),
            shortlist=[],questions=questions,sources=[dict(title=T('Официальное объявление сезона','Anuncio oficial de temporada'),url=FOD_ARTICLE,checked=CHECKED),
                dict(title=T('Публичная программа, даты и условия стоимости','Programa público, fechas y condiciones de precio'),url=FOD_FORM,checked=CHECKED)],checked=CHECKED))
    return out


def enrich_v141(d):
    index={e['id']:e for e in d['events']}
    for row in competition_rows():
        if row['id'] in index:index[row['id']].update(deepcopy(row))
        else:d['events'].append(row);index[row['id']]=row
    e=index['C064']
    e.update(checked=CHECKED,priority=T('P2 — приём завершён; проверить уже оформленную школьную заявку','P2 — registro terminado; comprobar inscripción escolar previa'),
        cost=T('4000 CRC за ученика, IVA включён, по официальному порталу Bebras Costa Rica.','4000 CRC por alumno, IVA incluido, según portal oficial Bebras Costa Rica.'),
        registration_status=T('Приём завершился 16.10.2026. Новая семейная заявка напрямую не допускается; позднее исключение не подтверждено.',
                              'Registro terminó el 16.10.2026. Sin solicitud familiar directa; excepción tardía no confirmada.'),
        action=T('Уточнить у школы, были ли дети зарегистрированы до 16 октября и в какой категории. Если нет, поздний допуск не обещан; рассмотреть отдельные правила Bebras México.',
                 'Comprobar con escuela si los hijos quedaron registrados antes del 16 de octubre y categoría. Sin registro previo no se promete admisión tardía; evaluar reglas propias de Bebras México.'),
        proof=T('Повторно прочитаны официальный JSON agenda/reglamento и публичный портал cuttle: сроки, школьный маршрут, 4000 CRC с IVA и награды. Расхождение по 2 классу не разрешено.',
                'Releídos JSON oficiales agenda/reglamento y portal cuttle: plazos, vía escolar, 4000 CRC con IVA y premios. Discrepancia sobre curso 2 sin resolver.'),
        reward=T('Электронный сертификат всем; лучшие 10% категории по стране получают почётную отметку и официальную публикацию. Это национальное признание, не мировой титул.',
                 'Certificado digital a todos; mejor 10% nacional de categoría recibe mención y publicación oficial. Reconocimiento nacional, sin título mundial.'))
    ref='https://costarica.cuttle.org/index.php?action=content&id=31'
    if not any(x['url']==ref for x in e['references']):e['references'].append(dict(label=T('Официальный портал: цена и школьная регистрация','Portal oficial: precio y registro escolar'),url=ref))
    index['C020']['osc']=T('По возрасту возможны mTiny, Inspire/Starter; Codey зависит от дня рождения. Soccer пока без новой convocatoria.',
                          'Por edad posibles mTiny, Inspire/Starter; Codey depende del cumpleaños. Soccer sigue sin convocatoria nueva.')
    e=index['C685'];e.update(checked=CHECKED,
        age=T('По связанным PDF: Bristle Race максимум 9; Path Attack Junior максимум 12; CrossBot максимум 15; остальные прочитанные очные категории любого возраста.',
              'Según PDF enlazados: Bristle Race máximo 9; Path Attack Junior máximo 12; CrossBot máximo 15; restantes categorías presenciales leídas sin límite de edad.'),
        format=TEAM,proof=T('Прочитаны 8 испанских регламентов 25.06.2026 и текущая мексиканская convocatoria 2027. Возрастные рамки и автономный / teleoperado режим уточнены по PDF.',
                            'Leídos 8 reglamentos españoles 25.06.2026 y convocatoria mexicana 2027 actual. Edades y modo autónomo / teleoperado precisados mediante PDF.'),
        note=T('Найден очный мексиканский этап 17.04.2027 и его 8 испытаний. Pixart и RandoMap в данном очном списке не объявлены; глобальная сеть не равна датированному мировому финалу.',
               'Encontrada etapa mexicana presencial 17.04.2027 con 8 retos. Pixart y RandoMap no anunciados en esta lista presencial; red global distinta de final mundial fechada.'))
    guide=next(g for g in d['league_guide']['profiles'] if g['id']=='robojam')
    guide['categories']=[g for g in guide['categories'] if g.get('event_id') not in {f'C{i}' for i in range(1172,1180)}]
    for category in guide['categories']:
        if category.get('event_id')=='C685':
            category.update(age=index['C685']['age'],team=TEAM,note=index['C685']['note'],checked=CHECKED)
    for i in range(1172,1180):
        e=index[f'C{i}'];guide['categories'].append(dict(name=e['title'],age=e['age'],team=e['format'],hardware=e['gear'],age_rule=RJ_NOTE,
            event_id=e['id'],entry=e['entry'],language=e['language'],note=e['note'],source=e['references'][-1]['url'],checked=CHECKED))
    guide.update(age_summary=index['C685']['age'],age_tags=['6','9','10-12','teen'],hardware=T('Bristlebot, автономный робот и teleoperado выбираются по категории; размеры 10 × 10, 15 × 15, 20 × 20 или 30 × 30 см.',
                    'Bristlebot, robot autónomo y teleoperado según categoría; dimensiones 10 × 10, 15 × 15, 20 × 20 o 30 × 30 cm.'),
        route=RJ_ENTRY,award=RJ_AWARD,nuances=[RJ_NOTE],checked=CHECKED)
    guide['event_ids']=list(dict.fromkeys(guide['event_ids']+[f'C{i}' for i in range(1171,1180)]))
    for url in [ROBOJAM,CHALLENGES]+[index[f'C{i}']['references'][-1]['url'] for i in range(1172,1180)]:
        if not any(s['url']==url for s in guide['sources']):guide['sources'].append(dict(title='RoboJam · ES',url=url,checked=CHECKED))
    bebras=next(g for g in d['league_guide']['profiles'] if g['id']=='bebras')
    bebras['categories']=[g for g in bebras['categories'] if g.get('event_id') not in ['C1170','C064']]
    for ident in ['C1170','C064']:
        e=index[ident];bebras['categories'].append(dict(name=e['title'],age=e['age'],team=e['format'],hardware=e['gear'],age_rule=e['age'],event_id=ident,
            entry=e['entry'],language=e['language'],note=e['note'],source=e['source'],checked=e['checked']))
    bebras['event_ids']=list(dict.fromkeys(bebras['event_ids']+['C1170','C064']))
    bebras['age_tags']=list(dict.fromkeys(bebras['age_tags']+['6','9','10-12','teen']))
    for url in [BEBRAS,BEBRAS_RULES,ref]:
        if not any(s['url']==url for s in bebras['sources']):bebras['sources'].append(dict(title='Bebras · ES',url=url,checked=CHECKED))
    bebras['nuances']=[n for n in bebras['nuances'] if not n.startswith('México 2026:')]
    bebras['nuances'].append(T('México 2026: бесплатно, семейный маршрут, 9–30 ноября. Costa Rica 2026: 4000 CRC, только школа, срок регистрации 16 октября. Правила одной страны не переносить в другую.',
                              'México 2026: gratis, modalidad familiar, 9–30 de noviembre. Costa Rica 2026: 4000 CRC, solo escuela, plazo de registro 16 de octubre. No trasladar reglas entre países.'))
    for e in d['events']:
        if e.get('camp_programme_id') in {f'CP{i}' for i in range(1124,1136)}:e['support_languages']=['ES']
    near=d['family_strategy']['nearby_participation_v118']
    additions=[dict(id='C1170',title='Bebras México · Otoño 2026',children=['matvey','oscar'],mode='check',gate=index['C1170']['age'],step=index['C1170']['action']),
        dict(id='C1173',title='RoboJam Monterrey · Path Attack Junior',children=['matvey','oscar'],mode='check',gate=index['C1173']['age'],step=index['C1173']['action'])]
    near['items']=[x for x in near['items'] if x['id'] not in ['C1170','C1173']]
    near['items']=additions+near['items'];near.update(version=141,checked=CHECKED,
        conclusion=T('Ближайший онлайн-вариант — Bebras México 9–30 ноября, после проверки класса и допуска из CR. Затем MakeX ноября по детским категориям. Локальные курсы FOD декабря/января дают подготовку; RoboJam Monterrey 17 апреля — отдельный открытый старт, без обещания мирового титула.',
                     'Opción próxima en línea: Bebras México 9–30 de noviembre, tras confirmar curso y admisión desde CR. Después MakeX de noviembre por categoría infantil. Cursos locales FOD de diciembre/enero sirven de preparación; RoboJam Monterrey el 17 de abril es etapa abierta propia, sin promesa de título mundial.'))
    d['league_guide'].update(version=141)
    existing_urls={s['url'] for s in d['sources']}
    for e in competition_rows():
        for url in [e['source']]+[r['url'] for r in e['references']]:
            if url not in existing_urls:d['sources'].append(dict(url=url,title='Bebras / RoboJam 2026–27',evidence='rules',checked=CHECKED));existing_urls.add(url)
    d['asof']=max(d['asof'],CHECKED)
