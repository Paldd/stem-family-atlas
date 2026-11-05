"""Primary 2027 Swiss tariff matrices and dated Malta technical camp options."""
from copy import deepcopy
from datetime import date,datetime,timedelta
from zoneinfo import ZoneInfo
CHECKED='2026-11-04'
SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
PREF='https://www.prefleuricamps.ch/'
SUMMER=PREF+'en/summer/'
FEES=PREF+'en/summer-fees/'
TERMS=PREF+'en/general-terms-and-conditions/'
BOARD=PREF+'wp-content/uploads/2026/10/PREFLEURI-SUMMER-CAMPS-PRICELIST-FINAL-2027-ENG-PRINT.pdf'
DAY=PREF+'wp-content/uploads/2026/10/PREFLEURI-SUMMER-CAMPS-PRICELIST-DAYSTUDENTS-2027-ENG-EXTERNAL-PRINT.pdf'
BROCHURE=PREF+'wp-content/uploads/2026/10/Brochure-summer-camps-2027-EN-HD.pdf'
TCTC='https://www.tctcmalta.com/en/private-courses/courses/720/christmas-camp.htm'
TCTC_TERMS='https://www.tctcmalta.com/en/terms-conditions.htm'
NUEJOS='https://www.nuejos.com/holiday-camps'
NUEJOS_POLICY='https://www.nuejos.com/_files/ugd/a1036d_1854ea51a9f24cc885811da4c3bba6cd.pdf'
FRILINGUE='https://www.frilingue.ch/en/juniors/learn-languages-switzerland-youth/liddes-saint-bernard/alps-winter-camp'
PREF_LANG=T('С 6 лет можно выбрать English / French language course или учебную поддержку; PDF указывает 15 часов в неделю. EN подтверждён для языкового курса, язык всего дня и каждой выездной опции отдельно уточнить.',
 'Desde 6 se puede elegir English / French language course o apoyo académico; PDF indica 15 horas semanales. EN confirmado para curso de idioma; confirmar idioma de día completo y cada opción de excursión.')
PREF_DEPOSIT=T('PDF 2027: аванс CHF 1000 на ребёнка входит в цену, остаток за 60 дней до приезда / начала. General terms одновременно говорят о full payment и подтверждении с deposit; точное условие брони согласовать. Summer отмена за 60–45 дней — удержание 1000, менее 45 — вся цена; более ранний срок и границы не разъяснены. При подтверждённых особых обстоятельствах описан перенос оплаты, не обещан cash refund. Условия не принимались.',
 'PDF 2027: anticipo CHF 1000 por niño incluido en precio, saldo 60 días antes de llegada / inicio. General terms menciona a la vez full payment y confirmación con deposit; acordar condición exacta de reserva. Cancelación Summer 60–45 días — retención 1000, menos de 45 — precio completo; plazo anterior y límites sin aclarar. Casos especiales acreditados describen traslado del pago, sin prometer cash refund. Sin aceptar condiciones.')
PREF_DISCOUNT=T('Скидка 10% от 4 недель уже включена. Скидка второму ребёнку 10% не суммируется: пансион исключает форму, страховку и налоги, day PDF перечисляет только форму. Базу скидки выбранного пакета подтвердить; семейная смета не уменьшена автоматически.',
 'Descuento 10% desde 4 semanas ya incluido. Descuento de segundo niño 10% no acumulable: residencia excluye uniforme, seguro e impuestos, PDF day enumera solo uniforme. Confirmar base de descuento del paquete elegido; presupuesto familiar no se reduce automáticamente.')
PREF_PLACE='Chesières · Chemin de Curnaux 32 · near Villars-sur-Ollon'
UNKNOWN_LANG=T('Язык конкретной программы EN/ES/RU ещё не подтверждён; английский сайт и список учебных предметов не доказывают язык занятий.',
 'Idioma EN/ES/RU del programa concreto aún sin confirmar; web inglesa y lista de asignaturas no acreditan idioma de clases.')

def source(title,url):return dict(title=title,url=url,checked=CHECKED)
def merge_sources(p,items):p['sources']=list({s['url']:s for s in p['sources']+items}.values())
def weekdays(start,end):
    a=date.fromisoformat(start);b=date.fromisoformat(end);return [(a+timedelta(days=i)).isoformat() for i in range((b-a).days+1) if (a+timedelta(days=i)).weekday()<5]
def lesson(day,start,end,zone,topic):
    z=ZoneInfo(zone)
    def utc(t):return datetime.fromisoformat(day+'T'+t).replace(tzinfo=z).astimezone(ZoneInfo('UTC')).isoformat().replace('+00:00','Z')
    return dict(date=day,start_time=start,end_time=end,timezone=zone,topic=topic,ical_timed=True,start_utc=utc(start),end_utc=utc(end))
def base(ident,slug,provider,country,iso,place,formats,age):
    detail=T('Возрастная возможность — не подтверждение места; язык, группа и приём внешней семьи уточняются.',
             'Posibilidad por edad no confirma plaza; idioma, grupo y admisión de familia externa pendientes.')
    return dict(id=ident,slug=slug,provider=provider,country=country,iso=iso,place=place,themes=['general'],formats=formats,age=age,
        language=UNKNOWN_LANG,confirmed_instruction_languages=[],programme='',timing=dict(status='next_unannounced',label='',sessions=[],session_details=[]),
        price=dict(year=None,currency='',amount=None,unit='programme',label='',included='',extras='',deposit=''),accommodation='',
        family_fit={k:dict(status='conditional',detail=detail) for k in ['matvey','oscar']},editorial_reason=detail,shortlist=[],
        questions=[T('Подтвердить язык ведущего, возраст на начало, место и самостоятельный приём детей.','Confirmar idioma del instructor, edad al inicio, plaza y admisión individual de niños.'),
                   T('Получить окончательный счёт, включения, питание, технику, страхование, транспорт и правила отмены.','Obtener factura final, inclusiones, comida, equipo, seguro, transporte y cancelación.')],sources=[],checked=CHECKED)

def build_profiles():
    result=[]
    common=T('Утром язык или учебная поддержка, затем спорт, природа, творчество и экскурсии по возрасту. Это общий международный лагерь, самостоятельный курс робототехники не заявлен.',
             'Por la mañana idioma o apoyo académico, después deporte, naturaleza, creatividad y excursiones por edad. Campamento internacional general, sin curso independiente de robótica anunciado.')
    for ident,slug,boarding,rates in [
      ('CP1164','prefleuri-summer-board-2027',True,{2:6150,3:8950,4:10750,5:13300,6:15750}),
      ('CP1165','prefleuri-summer-day-2027',False,{2:3575,3:5250,4:6800,5:8400,6:9900})]:
        p=base(ident,slug,T('Préfleuri · лето 2027 · пансион 5–14','Préfleuri · verano 2027 · residencia 5–14') if boarding else T('Préfleuri · лето 2027 · дневной 5–14','Préfleuri · verano 2027 · diurno 5–14'),
            'Швейцария','CHE',PREF_PLACE,['boarding'] if boarding else ['day'],T('5–14; в 2027 обоим подходит общий возраст, дети распределяются по разным группам. English lessons с 6 лет.',
               '5–14; en 2027 ambos cumplen edad general, se asignan a grupos distintos. English lessons desde 6.'))
        p.update(themes=['general','languages','sport'],programme=common,language=PREF_LANG,confirmed_instruction_languages=['EN'],language_evidence_role='language_lessons')
        p['family_fit']={k:dict(status='candidate',detail=T('В 2027 возраст соответствует 5–14 и языковым занятиям с 6. Ночёвки / выбранная группа и места подтверждаются отдельно.',
            'En 2027 edad compatible con 5–14 y clases de idioma desde 6. Pernocta / grupo elegido y plazas se confirman aparte.')) for k in ['matvey','oscar']}
        included=T('Пансион, полное питание, туристический налог, ежедневная стирка, форма, medical/accident insurance, язык и основные спорт / поездки по PDF 2027. PDF указывает 3 T-shirts, сайт 2: точный комплект формы уточнить.',
            'Residencia, pensión completa, tasa turística, lavandería diaria, uniforme, medical/accident insurance, idioma y deporte / excursiones básicos según PDF 2027. PDF indica 3 T-shirts, web 2: confirmar uniforme exacto.') if boarding else T('PDF: форма 2 T-shirts + sweater, местный minibus Villars–Chesières в 09:00 / 18:00, язык, спорт / поездки. Обед в списке day включений не выделен — подтвердить. Страховку обеспечивают родители; выходных нет.',
            'PDF: uniforme 2 T-shirts + sweater, minibus local Villars–Chesières 09:00 / 18:00, idioma, deporte / excursiones. Almuerzo no separado en inclusiones day — confirmar. Padres cubren seguro; sin fines de semana.')
        p['price'].update(year=2027,currency='CHF',amount=rates[2],unit='child_two_weeks',label=T('2027, возраст 5–14: ','2027, edad 5–14: ')+('2 / 3 / 4 / 5 / 6 '+T('недель: ','semanas: '))+' / '.join(str(rates[w]) for w in range(2,7))+' CHF. '+PREF_DISCOUNT,
            included=included,extras=T('За пределами основного тарифа: выбранные тематические недели и верховая езда. Group Geneva UM CHF 250 за ребёнка / направление по субботам в опубликованные часы; individual taxi CHF 600 / trip. Перелёты и полный счёт отдельно.',
                'Fuera de tarifa base: semanas temáticas elegidas y equitación. Group Geneva UM CHF 250 por niño / trayecto los sábados en horarios publicados; individual taxi CHF 600 / trip. Vuelos y factura completa aparte.') if boarding else T('Страхование детей родителями, питание по подтверждённому day-пакету, тематические опции, семейное жильё и дорога отдельно. Местный minibus включён; не добавлять его повторно.',
                'Seguro infantil por padres, comida según paquete day confirmado, opciones temáticas, alojamiento familiar y viaje aparte. Minibus local incluido; no sumarlo otra vez.'),deposit=PREF_DEPOSIT)
        p['accommodation']=T('Пансион; минимальный оплачиваемый заезд 2 недели, приезд и выезд по субботам. Наличие места / комната и готовность к ночёвкам отдельно.',
            'Residencia; estancia mínima pagada 2 semanas, llegada y salida los sábados. Plaza / habitación y preparación para pernoctar aparte.') if boarding else T('Дневной лагерь Пн–Пт 09:00–18:00, минимум 2 недели. Родители обеспечивают проживание и выходные.',
            'Campamento diurno Lu–Vi 09:00–18:00, mínimo 2 semanas. Padres organizan alojamiento y fines de semana.')
        p['timing'].update(status='published_2027',label=T('Матрица 2027 прямо разрешает пять дат начала и длительности 2–6 недель. Даты окончания рассчитаны по таблице; наличие места не подтверждено.',
            'Matriz 2027 autoriza cinco inicios y duraciones 2–6 semanas. Fechas finales calculadas según tabla; plazas sin confirmar.'))
        for i in range(5):
            first=date(2027,6,26)+timedelta(days=i*7+(0 if boarding else 2))
            for weeks in range(2,7-i):
                end=first+timedelta(days=7*weeks-(0 if boarding else 3));a=first.isoformat();b=end.isoformat()
                rule=T('Начало разрешено таблицей 2027; пансион Сб–Сб, длительность в полных неделях, последний выезд 7 августа.',
                    'Inicio autorizado por tabla 2027; residencia Sá–Sá, duración en semanas completas, última salida 7 de agosto.') if boarding else T('Начало разрешено таблицей 2027; дневные Пн–Пт, последние занятия 6 августа; выходные не учебные дни.',
                    'Inicio autorizado por tabla 2027; diurno Lu–Vi, últimas clases 6 de agosto; fines de semana no lectivos.')
                v=dict(start=a,end=b,label=str(weeks)+' '+T('недели · пансион','semanas · residencia') if boarding else str(weeks)+' '+T('недели · дневной Пн–Пт','semanas · diurno Lu–Vi'),price=str(rates[weeks])+' CHF '+T('на ребёнка за весь выбранный период; аванс внутри цены','por niño por periodo elegido completo; anticipo dentro de precio'),source=BOARD if boarding else DAY,
                    date_precision='published_rule',date_rule=rule,date_status='Опубликованное правило · даты рассчитаны',date_scope='camp_session' if boarding else 'session_days')
                if not boarding:v['sessions']=[lesson(day,'09:00','18:00','Europe/Zurich',T('Дневной лагерь · выбранная программа','Campamento diurno · programa elegido')) for day in weekdays(a,b)]
                p['timing']['sessions'].append([a,b]);p['timing']['session_details'].append(v)
        p['sources']=[source(T('Прайс пансиона 2027 · визуально сверенная таблица','Tarifa residencia 2027 · tabla comprobada visualmente'),BOARD),source(T('Прайс day 2027 и учебные дни','Tarifa day 2027 y días lectivos'),DAY),source(T('Текущие цены, опции и возрастные группы','Precios actuales, opciones y grupos de edad'),FEES),source(T('Содержание лагеря и языковые курсы','Contenido del campamento y cursos de idioma'),SUMMER),source(T('Общие условия оплаты и отмены','Condiciones generales de pago y cancelación'),TERMS)]
        p['editorial_reason']=T('Практичный кандидат для общего отдыха обоих детей с опубликованным прайсом 2027; разные возрастные группы и language lessons не означают общий робототехнический курс.',
            'Candidato práctico para vacaciones generales de ambos niños con tarifa 2027 publicada; grupos por edad y language lessons no equivalen a curso robótico compartido.')
        result.append(p)
    options=[
      ('CP1166','prefleuri-element-2027','Element Rangers','2027-07-03','2027-07-09',400,8,T('Зиплайн, вода и подземные маршруты; максимум 15 участников.','Tirolina, agua y rutas subterráneas; máximo 15 participantes.')),
      ('CP1167','prefleuri-expedition-2027','Expedition','2027-07-10','2027-07-16',600,10,T('Четыре дня пешком между горными хижинами с ночёвками в горах; максимум 15 участников.','Cuatro días a pie entre refugios con pernocta en montaña; máximo 15 participantes.')),
      ('CP1168','prefleuri-extreme-2027','Extreme Adventure','2027-07-17','2027-07-23',650,10,T('Рафтинг, скалолазание, каньонинг, zip-line, mountain carting и RealFly; максимум 15 участников.','Rafting, escalada, barranquismo, zip-line, mountain carting y RealFly; máximo 15 participantes.')),
      ('CP1169','prefleuri-tour-2027','Swiss Tour','2027-07-24','2027-07-30',950,10,T('Поездки по Швейцарии с завершением в Europa-Park, Германия; максимум 15 участников.','Viajes por Suiza con final en Europa-Park, Alemania; máximo 15 participantes.'))]
    for ident,slug,name,a,b,amount,minimum,content in options:
        p=base(ident,slug,'Préfleuri · '+name+' · '+T('опция общего лагеря','opción de campamento general'),'Швейцария','CHE',PREF_PLACE,['day','boarding'],T('От ','Desde ')+str(minimum)+' '+T('лет по странице программы.','años según página del programa.'))
        if ident=='CP1168':p['age']=T('Конфликт: страница программы и fee page от 10, оба PDF 2027 от 8. Для ребёнка младше 10 допуск не подтверждён.',
            'Discrepancia: página de programa y tarifas desde 10, ambos PDF 2027 desde 8. Admisión de menor de 10 sin confirmar.')
        p.update(themes=['general','sport'],requires_parent_programme_ids=['CP1164','CP1165'],programme=content+' '+T('Это платная опция внутри минимум двухнедельного общего лагеря, не самостоятельная недельная смена. Дневным участникам разрешены excursion weeks, но их конкретные дни и часы выездов уточнить.',
            'Opción pagada dentro de campamento general mínimo de dos semanas, no sesión semanal independiente. Alumnos diurnos pueden participar en excursion weeks; confirmar días y horas concretos.'))
        p['timing'].update(status='published_2027',label=T('Опубликованное окно тематической опции; день за днём программа и участие day отдельно подтверждаются.',
            'Periodo publicado de opción temática; confirmar programa diario y participación day.'),sessions=[[a,b]],session_details=[dict(start=a,end=b,label=T('Тематическая опция · не отдельный лагерь','Opción temática · no campamento separado'),source=SUMMER,price=str(amount)+' CHF '+T('доплата к общему лагерю','suplemento del campamento general'),date_scope='camp_window')])
        p['price'].update(year=2027,currency='CHF',amount=amount,unit='option_week_supplement',label=str(amount)+' CHF '+T('сверх оплаченного общего лагеря; это не полная цена поездки или проживания.','además del campamento general pagado; no es precio completo de viaje ni alojamiento.'),included=content,extras=T('Основной day / boarding пакет минимум 2 недели, личные расходы и дорога отдельно. Возможную замену языковых уроков выездной программой уточнить.',
            'Paquete base day / boarding mínimo 2 semanas, gastos personales y viaje aparte. Confirmar posible sustitución de clases de idioma por excursiones.'),deposit=PREF_DEPOSIT)
        p['accommodation']=T('Размещение только по выбранному основному лагерю; в Expedition ночёвки в горных хижинах. Day не превращается автоматически в оплаченный пансион.',
            'Alojamiento según campamento base elegido; Expedition pernocta en refugios de montaña. Day no se convierte automáticamente en residencia pagada.')
        p['family_fit']['matvey']=dict(status='candidate' if minimum==8 else 'conditional',detail=T('Возраст 9–10 летом 2027: минимум 8 проходит; минимум 10 только после дня рождения. Противоречия конкретной опции согласовать.',
            'Edad 9–10 en verano 2027: mínimo 8 compatible; mínimo 10 solo tras cumpleaños. Acordar discrepancias de opción concreta.'))
        p['family_fit']['oscar']=dict(status='later',detail=T('В 2027 только 6–7: младше любого указанного минимума 8 / 10. Может рассмотреть общий лагерь своей группы, не эту опцию.',
            'En 2027 solo 6–7: menor de cualquier mínimo indicado 8 / 10. Puede considerar campamento general de su grupo, no esta opción.'))
        p['sources']=[source(T('Даты, содержание и возраст опции','Fechas, contenido y edad de opción'),SUMMER),source(T('Доплата и альтернативный возраст в PDF','Suplemento y edad alternativa en PDF'),BOARD),source(T('Опции для day и их условия','Opciones day y condiciones'),DAY),source(T('Fee page: текущий минимум и цена','Fee page: mínimo y precio actuales'),FEES)]
        result.append(p)
    p=base('CP1170','tctc-christmas-2026-27','TCTC Malta · Christmas Tech Camp','Мальта','MLT','Malta · Naxxar / Paola',['day'],T('7–11 к началу курса 28 декабря 2026; отдельные январские дни как самостоятельный набор не объявлены.',
        '7–11 al inicio 28 de diciembre de 2026; días de enero separados no anunciados como convocatoria independiente.'))
    p.update(themes=['robotics','ai','coding','games','makers'],language=T('Общая политика TCTC: занятия на английском, нужны понимание, письмо и обсуждение на EN. Maltese возможен только по согласию всех учеников и преподавателя; сохранить английскую группу до записи.',
        'Política general TCTC: clases en inglés, requieren comprensión, escritura y debate EN. Maltese solo por acuerdo de todos los alumnos y profesor; asegurar grupo inglés antes de inscripción.'),confirmed_instruction_languages=['EN'],
        programme=T('Basic: 3D printing, Creative AI через демонстрации преподавателя, Robotics and Coding. Full добавляет Creating Games утром. Начальный творческий курс; конкретный робот, компьютер на ребёнка и сложность для опытного участника уточнить.',
            'Basic: 3D printing, Creative AI con demostraciones del profesor, Robotics and Coding. Full añade Creating Games por la mañana. Curso creativo inicial; confirmar robot, ordenador por niño y dificultad para participante experimentado.'))
    p['family_fit']['matvey']=dict(status='candidate',detail=T('На старте возраст 8–9, внутри 7–11. Английская группа и место отдельно, опыт может превышать вводный уровень.',
        'Al inicio edad 8–9, dentro de 7–11. Grupo inglés y plaza aparte, experiencia puede superar nivel introductorio.'))
    p['family_fit']['oscar']=dict(status='later',detail=T('На 28 декабря 2026 ребёнку 2020 года рождения не более 6, ниже 7. Более поздний день рождения в январе не даёт автоматический доступ к полному курсу.',
        'El 28 de diciembre de 2026 niño nacido en 2020 tiene como máximo 6, menor de 7. Cumpleaños posterior en enero no permite automáticamente curso completo.'))
    p['price'].update(year=2026,currency='EUR',amount=200,unit='five_day_programme',label=T('Basic EUR 200 за весь пятидневный курс 09:00–12:30; Full EUR 225 за весь курс 08:00–12:30. Добавление Games увеличивает общий тариф на 25, не на 225. Налог / возможные обязательные доплаты подтвердить.',
        'Basic EUR 200 por curso completo de cinco días 09:00–12:30; Full EUR 225 por curso completo 08:00–12:30. Añadir Games aumenta total en 25, no en 225. Confirmar impuesto / posibles suplementos obligatorios.'),
        included=T('По general terms включаются базовые материалы / заметки, где применимо. Ровно какой компьютер, robot kit и распечатанный проект получит ребёнок, не установлено.',
            'General terms incluye materiales / apuntes básicos cuando procede. Ordenador, robot kit y proyecto impreso concretos que recibe niño sin determinar.'),
        extras=T('Проживание семьи, поездка и питание отдельно. Общая политика запрещает еду в классе; условия перерывов и перекуса уточнить.',
            'Alojamiento familiar, viaje y comida aparte. Política general prohíbe comer en aula; confirmar descansos y merienda.'),
        deposit=T('General terms: обычный аванс EUR 100, но может отличаться по курсу; остаток к началу. При отмене учеником cash refund не обещан, credit note на 3 месяца с возможным продлением на 3 по усмотрению школы. При отмене школой описан возврат отменённой части. Применимость и платёж не подтверждены; условия не принимались.',
            'General terms: anticipo habitual EUR 100, puede variar por curso; saldo al inicio. Cancelación por alumno sin prometer cash refund, credit note de 3 meses con posible extensión de 3 por decisión de escuela. Cancelación por escuela describe reembolso de parte cancelada. Aplicación y pago sin confirmar; condiciones no aceptadas.'))
    p['accommodation']=T('Только дневные занятия; ночёвки, утренний присмотр до выбранного времени и обед не заявлены.',
        'Solo clases diurnas; pernocta, cuidado previo a hora elegida y almuerzo sin anunciar.')
    p['timing'].update(status='published_2026_27',label=T('Пять учебных дней: 28 / 29 / 30 декабря 2026 и 4 / 5 января 2027. Рождественский перерыв не добавлен как ежедневный лагерь.',
        'Cinco días lectivos: 28 / 29 / 30 de diciembre de 2026 y 4 / 5 de enero de 2027. Pausa navideña no se añade como campamento diario.'),variant_keyed=True)
    days=['2026-12-28','2026-12-29','2026-12-30','2027-01-04','2027-01-05']
    for venue,number in [('Naxxar',7115),('Paola',7116)]:
        url='https://www.tctcmalta.com/viewer/'+str(number)+'/download.pdf'
        for package,start,amount in [('Basic','09:00',200),('Full','08:00',225)]:
            place='Naxxar · TCTC Business & Education Centre · 151 Labour Avenue' if venue=='Naxxar' else T('Paola · точный корпус уточнить','Paola · edificio exacto por confirmar')
            v=dict(start=days[0],end=days[-1],label=venue+' · '+package,variant_key=venue.lower()+'-'+package.lower(),price=str(amount)+' EUR '+T('за 5 дней целиком','por 5 días completos'),source=url,
                place=place,date_scope='session_days',sessions=[lesson(day,start,'12:30','Europe/Malta',package+' · Christmas Tech Camp') for day in days],
                proof=T('Даты и Basic 09:00–12:30 сверены по отдельному PDF этого центра; Full 08:00–12:30 и цена по общей странице курса. Свободные места не подтверждены.',
                    'Fechas y Basic 09:00–12:30 contrastados con PDF propio del centro; Full 08:00–12:30 y precio según página general del curso. Plazas libres sin confirmar.'))
            p['timing']['sessions'].append([days[0],days[-1]]);p['timing']['session_details'].append(v)
    p['sources']=[source(T('Программа, цена Basic / Full и возраст','Programa, precio Basic / Full y edad'),TCTC),source(T('Язык, overseas applications, материалы и отмена','Idioma, overseas applications, materiales y cancelación'),TCTC_TERMS),source('Naxxar · Christmas timetable','https://www.tctcmalta.com/viewer/7115/download.pdf'),source('Paola · Christmas timetable','https://www.tctcmalta.com/viewer/7116/download.pdf'),source(T('Официальные центры и адрес Naxxar','Centros oficiales y dirección Naxxar'),'https://www.tctcmalta.com/en/tctc-centres.htm')]
    result.append(p)
    for ident,slug,academic in [('CP1171','nuejos-adventure-2026-27',False),('CP1172','nuejos-academics-watch',True)]:
        p=base(ident,slug,'NUEJOS · '+('Academics Camp' if academic else 'Adventure / Multi-activity Camp'),'Швейцария','CHE','Baar · Sihlbruggstrasse 3a',['day'],
            T('6–12 в описании Academics; общий заголовок Education 5–12 не снижает минимум этой программы.',
              '6–12 en descripción Academics; cabecera Education 5–12 no reduce mínimo de este programa.') if academic else T('2–12 по описанию Adventure; точная группа детей подтверждается отдельно.','2–12 según Adventure; confirmar grupo infantil concreto.'))
        p['themes']=['general','robotics','science'] if academic else ['general','sport']
        p['programme']=T('Утром экскурсии; после — Mathematics, English, German, French, Italian, Art, Robotics и STEM из общего предложения. Часы робототехники и язык её преподавания не установлены; это не обещание недельного robotics-only курса.',
            'Excursiones por la mañana; después Mathematics, English, German, French, Italian, Art, Robotics y STEM de oferta general. Horas de robótica e idioma sin determinar; no promete curso semanal exclusivo de robótica.') if academic else T('Общие экскурсии утром и занятия / игры по возрасту после; братья могут быть в разных учебных группах. Adventure объявлен all year round; спортивная программа и Teen исключают зиму, Fishing только весна / лето.',
            'Excursiones comunes por la mañana y actividades / juegos por edad después; hermanos pueden estar en grupos distintos. Adventure se anuncia all year round; programa deportivo y Teen excluyen invierno, Fishing solo primavera / verano.')
        amount=880 if academic else 680
        p['price'].update(currency='CHF',amount=amount,unit='child_week',label=(T('Текущая недатированная ставка ','Tarifa actual sin fecha ')+str(amount)+' CHF '+T('за полную неделю до опубликованных 8.10% MWST; для выбранной смены подтвердить.','por semana completa antes de 8.10% MWST publicados; confirmar para sesión elegida.')),
            included=T('Заявленная программа и экскурсии; что именно из питания / материалов включено, запросить полным счётом.',
                'Programa y excursiones anunciados; solicitar factura completa para inclusiones de comida / materiales.'),
            extras=T('CHF 50 разовая membership для новых учеников; единицу для семьи и налогообложение подтвердить. Bus в неделю: Zug 85 / Zürich Affoltern 100 / Luzern 125; ранний drop-off 15 в день на ребёнка. Скидка 10% для siblings / extra weeks только за полную неделю, база и суммирование не определены. Не вычитать её автоматически.',
                'CHF 50 membership única para alumnos nuevos; confirmar unidad familiar e impuesto. Bus semanal: Zug 85 / Zürich Affoltern 100 / Luzern 125; drop-off temprano 15 al día por niño. Descuento 10% para siblings / extra weeks solo semana completa, base y acumulación sin definir. No restarlo automáticamente.'),
            deposit=T('Camp Policy: после подтверждения регистрации отмена / возврат и компенсация пропусков не предусмотрены. Уведомить об аллергиях; еду с собой запрещают, состав и стоимость питания уточнить. Место и условия не приняты.',
                'Camp Policy: tras confirmar registro no contempla cancelación / reembolso ni compensación por ausencias. Informar alergias; prohíbe comida propia, confirmar menú y coste. Plaza y condiciones sin aceptar.'))
        p['accommodation']=T('Дневной: привезти 08:30–09:00, забрать до 18:00; morning до 14:00. Внешнее жильё семьи не входит. Точные часы выбранного пакета отдельно.',
            'Diurno: llegada 08:30–09:00, salida hasta 18:00; morning hasta 14:00. Alojamiento familiar externo no incluido. Horario exacto de paquete elegido aparte.')
        if academic:
            p['timing'].update(status='next_unannounced',label=T('Общий календарь оператора не подтверждает конкретный запуск Academics в каждую неделю. Тематические даты пока не добавлены в подтверждённый календарь.',
                'Calendario general del operador no confirma Academics cada semana. Fechas temáticas aún no añadidas al calendario confirmado.'))
        else:
            p['timing'].update(status='published_2026_27',label=T('Опубликованные окна Festive / Winter / Spring для общего Adventure; дневные посещения и полную неделю выбирают отдельно. Летние даты 2027 ещё Soon.',
                'Periodos Festive / Winter / Spring publicados para Adventure general; días sueltos y semana completa se eligen aparte. Fechas verano 2027 aún Soon.'))
            for a,b in [('2026-12-18','2026-12-22'),('2027-02-08','2027-02-12'),('2027-02-15','2027-02-19'),('2027-02-22','2027-02-26'),('2027-03-29','2027-04-02'),('2027-04-05','2027-04-09'),('2027-04-19','2027-04-23'),('2027-04-26','2027-04-30')]:
                p['timing']['sessions'].append([a,b]);p['timing']['session_details'].append(dict(start=a,end=b,label=T('Окно выбора дня / недели','Periodo para elegir día / semana'),price=p['price']['label'],source=NUEJOS,date_scope='camp_window',entry=T('Выбрать конкретные дни и пакет. Окно 18–22 декабря включает выходные; фактические даты посещения / итоговую цену не выводить из недельного тарифа.',
                    'Elegir días concretos y paquete. Periodo 18–22 de diciembre incluye fin de semana; no deducir asistencia / precio final de tarifa semanal.')))
        p['family_fit']={k:dict(status='conditional',detail=T('Возраст общего предложения выглядит подходящим; проверить дату, школьную группу, фактический EN/ES и индивидуальный приём. Для Academics 6+ нужен уже исполненный возраст.',
            'Edad de oferta general parece compatible; confirmar fecha, grupo escolar, EN/ES real y admisión individual. Academics 6+ requiere edad cumplida.')) for k in ['matvey','oscar']}
        p['sources']=[source(T('Календарь, программа и опубликованные тарифы','Calendario, programa y tarifas publicadas'),NUEJOS),source(T('Настоящая Camp Policy из кнопки Read Policy','Camp Policy real desde botón Read Policy'),NUEJOS_POLICY)]
        result.append(p)
    return result

def refresh_existing(report):
    p=next(p for p in report['profiles'] if p['id']=='CP003');p['checked']=CHECKED
    p['timing'].update(status='published_2027',label=T('Лето 26 июня–7 августа 2027 подтверждено текущей страницей и прайсами. Это общий обзор; конкретные day / boarding варианты вынесены в отдельные досье.',
        'Verano 26 de junio–7 de agosto de 2027 confirmado por página actual y tarifas. Es resumen general; variantes day / boarding concretas en fichas separadas.'))
    p['language']=PREF_LANG;p['language_evidence_role']='language_lessons';p['confirmed_instruction_languages']=['EN']
    p['price'].update(year=2027,label=T('2027, 5–14 лет: boarding 2 / 3 / 4 / 5 / 6 недель CHF 6150 / 8950 / 10750 / 13300 / 15750; day 3575 / 5250 / 6800 / 8400 / 9900. Тарифы 2026 заменены текущими. ',
        '2027, 5–14 años: boarding 2 / 3 / 4 / 5 / 6 semanas CHF 6150 / 8950 / 10750 / 13300 / 15750; day 3575 / 5250 / 6800 / 8400 / 9900. Tarifas 2026 sustituidas por actuales. ')+PREF_DISCOUNT,
        included=T('Пансион: проживание, полное питание, туристический налог, стирка, форма, medical/accident insurance, язык / занятия / поездки. Day: форма, minibus Villars–Chesières, язык / занятия / поездки; питание уточнить, страховка родителей.',
            'Residencia: alojamiento, pensión completa, tasa turística, lavandería, uniforme, medical/accident insurance, idioma / actividades / excursiones. Day: uniforme, minibus Villars–Chesières, idioma / actividades / excursiones; confirmar comida, seguro por padres.'),
        extras=T('2027: Element Rangers 400 CHF, Expedition 600, Extreme Adventure 650, Swiss Tour 950 сверх основного лагеря. Extreme: PDF от 8, сайт от 10 — конфликт. Horse riding 300 за неделю. Geneva group UM 250 за ребёнка / направление в субботу; taxi 600 за trip. Возраст опции, место и полный счёт отдельно.',
            '2027: Element Rangers 400 CHF, Expedition 600, Extreme Adventure 650, Swiss Tour 950 además del campamento base. Extreme: PDF desde 8, web desde 10 — discrepancia. Horse riding 300 semanal. Geneva group UM 250 por niño / trayecto sábado; taxi 600 por trip. Edad de opción, plaza y factura completa aparte.'),deposit=PREF_DEPOSIT)
    merge_sources(p,[source(T('Новый boarding прайс 2027','Tarifa boarding nueva 2027'),BOARD),source(T('Новый day прайс 2027','Tarifa day nueva 2027'),DAY),source(T('Текущая программа 2027','Programa actual 2027'),SUMMER),source(T('Текущая fee page 2027','Fee page actual 2027'),FEES),source(T('Условия оплаты и отмены','Condiciones de pago y cancelación'),TERMS)])
    p=next(p for p in report['profiles'] if p['id']=='CP866');p['checked']=CHECKED
    p['price']['included']=T('Полный пансион, языковой курс и основные активности / экскурсии. Sunday Geneva group transfer включён: прилёт 10:00–16:00, вылет 12:00–18:00. Страница заявляет 24-hour supervision; договор не обещает непрерывное индивидуальное наблюдение за каждым подростком.',
        'Pensión completa, curso de idioma y actividades / excursiones básicas. Sunday Geneva group transfer incluido: llegada 10:00–16:00, salida 12:00–18:00. Página anuncia 24-hour supervision; contrato no promete observación individual continua de cada adolescente.')
    p['price']['extras']=T('Geneva в воскресенье вне опубликованных часов 400 CHF / направление, Пн–Сб 500. UM service 100 / направление плюс правила / сбор авиакомпании. Комнаты: 100 / 200 / 275 / 300 CHF в неделю; Hotel Gd 400 / 450 / 500 по типу. Некоторые комнаты отдельно, 10 минут пешком. Прокат лыж 150 или premium 300 в неделю; страховка 50 в неделю, если нет своей. Стирка 40 и специальное питание 100 — единицу начисления подтвердить. Дополнительный день Verbier 150 включает дорогу, ski pass, перекус и сопровождение, только intermediate / advanced. Полный счёт уточнить.',
        'Geneva domingo fuera de horas publicadas 400 CHF / trayecto, Lu–Sá 500. UM service 100 / trayecto más reglas / cargo de aerolínea. Habitaciones: 100 / 200 / 275 / 300 CHF semanales; Hotel Gd 400 / 450 / 500 según tipo. Algunas habitaciones separadas, 10 minutos a pie. Alquiler de esquí 150 o premium 300 semanal; seguro 50 semanal si no tiene propio. Lavandería 40 y dieta especial 100 — confirmar unidad de cobro. Día extra Verbier 150 incluye viaje, ski pass, merienda y supervisión, solo intermediate / advanced. Confirmar factura completa.')
    for v in p['timing']['session_details']:
        v['place']='Liddes · Relais de Dranse' if v['start']<'2027-01-31' else 'La Fouly · Maison Dolent' if v['start']=='2027-02-14' else 'Bourg-Saint-Pierre · Petit Vélan'
    merge_sources(p,[source(T('Текущие адреса по неделям и трансферы','Sedes actuales por semana y traslados'),FRILINGUE),source(T('Условия оплаты и отмены','Condiciones de pago y cancelación'),'https://www.frilingue.ch/en/language-camps-switzerland/terms-conditions')])
    # Remove old price-unpublished claims from the visible summaries as well.
    for item in report['family_review']['entries']:
        if item['slug']=='prefleuri':
            item['key_limit']=T('Прайсы 2027 опубликованы: пансион минимум две недели, day по будням; форматы и доплаты раздельно. Языковой урок не подтверждает английский всех активностей. Конкретная группа, полный счёт и готовность к ночёвкам отдельно.',
                'Tarifas 2027 publicadas: residencia mínimo dos semanas, day entre semana; formatos y suplementos separados. Clase de idioma no confirma inglés de todas las actividades. Grupo concreto, factura completa y preparación para pernoctar aparte.')
            item['dossier_checked']=CHECKED
    for item in report['shortlist']:
        if item.get('reason','').endswith('Préfleuri подходит младшим, но price2026 и cancellation summer/winter разные; ENlanguageclasses не full ENcamp.'):
            item['reason']=item['reason'].split('Préfleuri подходит младшим')[0]+T('Préfleuri теперь публикует прайсы 2027 для младших: day и пансион раздельно; условия summer/winter различаются. EN language classes не подтверждают весь день на английском.',
                'Préfleuri publica ahora tarifas 2027 para menores: day y residencia por separado; condiciones summer/winter distintas. EN language classes no confirma todo el día en inglés.')
    for item in report['gaps']:
        old='Préfleuri2026 fee/reductions не 2027; summer/Ski60–45/minus1000 vswinter60 boundary, cashrefund не обещан.'
        if isinstance(item,dict) and old in item.get('detail',''):
            item['detail']=item['detail'].replace(old,T('Préfleuri: старые тарифы заменены прайсами 2027 в текущих досье. Условия скидок day / boarding различаются; договор summer / winter и cash refund отдельно уточнить.',
                'Préfleuri: tarifas anteriores sustituidas por precios 2027 en fichas actuales. Condiciones de descuento day / boarding distintas; aclarar contrato summer / winter y cash refund aparte.'))

def extend_planning(d):
    common=dict(currency='CHF',price_year=2027,children=['matvey','oscar'],discount_second=0,required=[],unknown_trip=['travel','lodging','misc'],checked=CHECKED)
    board=dict(common,id='prefleuri-summer-2027-two-board',slug='prefleuri-summer-board-2027',label=T('Préfleuri · двое · пансион 26 июня–10 июля 2027','Préfleuri · dos niños · residencia 26 de junio–10 de julio de 2027'),format='boarding',base_by_child=dict(matvey=6150,oscar=6150),sessions=[['2027-06-26','2027-07-10']],
        unknown_required=[dict(id='invoice_extras',label=T('Другие обязательные суммы выбранного счёта · подтвердить','Otros importes obligatorios de factura elegida · confirmar'),unit='amount',rate=1,min=0)],
        optional=[dict(id='geneva-um-rt',label=T('Geneva UM туда-обратно двум детям · 250 × 2 × 2','Geneva UM ida y vuelta para dos niños · 250 × 2 × 2'),amount=1000),dict(id='element-matvey',label=T('Element Rangers 3–9 июля · только Матвей','Element Rangers 3–9 de julio · solo Matvey'),amount=400)],
        sources=[BOARD,FEES,SUMMER,TERMS],gate=T('Обоим подходит 5–14; языковые классы с 6. Разные возрастные группы, комната и English stream отдельно. Element Rangers только Матвею 8+; Оскару 6–7 рано.',
            'Ambos cumplen 5–14; clases de idioma desde 6. Grupos por edad distintos, habitación y English stream aparte. Element Rangers solo Matvey 8+; Oscar 6–7 aún menor.'),deposit_note=PREF_DEPOSIT,
        included=T('Опубликованная база двух 12300 CHF с питанием, формой, туристическим налогом и страховкой по PDF. Аванс 1000 каждому внутри базы, не добавлен повторно.',
            'Base publicada para dos 12300 CHF con comida, uniforme, tasa turística y seguro según PDF. Anticipo 1000 cada uno dentro de base, sin sumarlo otra vez.'),
        scope=T('При двух организованных UM-трансферах туда-обратно детям база с ними 13300 CHF. Это не полный счёт поездки: перелёты, UM авиакомпании, расходы взрослых / внешнее жильё отдельно. Неприменимая ко всем компонентам скидка не вычтена.',
            'Con traslados UM organizados ida y vuelta de ambos niños, base con ellos 13300 CHF. No es factura completa de viaje: vuelos, UM de aerolínea, gastos adultos / alojamiento externo aparte. Descuento no aplicable a todos los componentes sin restar.'))
    day=dict(common,id='prefleuri-summer-2027-two-day',slug='prefleuri-summer-day-2027',label=T('Préfleuri · двое · day 28 июня–9 июля 2027','Préfleuri · dos niños · day 28 de junio–9 de julio de 2027'),format='day',base_by_child=dict(matvey=3575,oscar=3575),sessions=[['2027-06-28','2027-07-09']],
        unknown_required=[dict(id='day_cover_meals',label=T('Страховка обоих и питание по day счёту · подтвердить','Seguro de ambos y comida según factura day · confirmar'),unit='amount',rate=1,min=0)],optional=[],sources=[DAY,FEES,SUMMER,TERMS],gate=board['gate'],deposit_note=PREF_DEPOSIT,
        included=T('База двух 7150 CHF за десять учебных дней Пн–Пт 09:00–18:00; форма и minibus Villars–Chesières включены. Проживания и weekend-care нет.',
            'Base de dos 7150 CHF por diez días lectivos Lu–Vi 09:00–18:00; uniforme y minibus Villars–Chesières incluidos. Sin alojamiento ni weekend-care.'),
        scope=T('Проживание всей семьи, дорога, личная страховка детей и включение питания не закрыты этой суммой. Семейная скидка не вычтена без разбивки условий.',
            'Alojamiento de familia, viaje, seguro personal infantil e inclusión de comida no resueltos por esta suma. Sin restar descuento familiar sin desglose de condiciones.'))
    malta=dict(id='tctc-matvey-basic-2026',slug='tctc-christmas-2026-27',label=T('TCTC Malta · только Матвей · Christmas Basic / Full','TCTC Malta · solo Matvey · Christmas Basic / Full'),currency='EUR',price_year=2026,children=['matvey'],base_by_child=dict(matvey=200),discount_second=0,required=[],
        unknown_required=[dict(id='camp_extra',label=T('Обязательные доплаты / техника, если требуются · подтвердить','Suplementos obligatorios / equipo, si procede · confirmar'),unit='amount',rate=1,min=0)],
        optional=[dict(id='games-early',label=T('Full: Games 08:00–09:00 все пять дней · доплата 25','Full: Games 08:00–09:00 los cinco días · suplemento 25'),amount=25)],sources=[TCTC,TCTC_TERMS],sessions=[['2026-12-28','2027-01-05']],
        gate=T('7–11 на 28 декабря; Матвей подходит, Оскар ниже 7. Выбрать Naxxar или Paola и закрепить английский язык по общей политике.',
            '7–11 el 28 de diciembre; Matvey compatible, Oscar menor de 7. Elegir Naxxar o Paola y asegurar inglés según política general.'),deposit_note=T('Обычный аванс 100 EUR по general terms может отличаться по курсу и входит в тариф; остаток до начала. Набор, отмена и письменный счёт отдельно.',
            'Anticipo habitual 100 EUR según general terms puede variar por curso y está incluido en tarifa; saldo antes de inicio. Convocatoria, cancelación y factura escrita aparte.'),
        included=T('200 EUR — Basic за пять реальных учебных дней, 225 — Full с ранним Games; это не дневная цена и не сумма за обоих братьев.',
            '200 EUR es Basic de cinco días lectivos reales, 225 Full con Games temprano; no precio diario ni importe de ambos hermanos.'),unknown_trip=['travel','lodging','misc'],scope=T('Учебный тариф только Матвея. Питание, семейная поездка и отдельная программа Оскара не включены.',
            'Tarifa educativa solo de Matvey. Comida, viaje familiar y programa separado de Oscar no incluidos.'),checked=CHECKED,format='day')
    authored=[board,day,malta];idx={o['id']:o for o in authored};old={o['id'] for o in d['camp_planning']['offers']}
    d['camp_planning']['offers']=[idx.get(o['id'],o) for o in d['camp_planning']['offers']]+[o for o in authored if o['id'] not in old]
    d['camp_planning'].update(version=148,asof=CHECKED)

def enrich_v148(d):
    extend_planning(d)
    p=d['camp_programmes'];parents={'CP1164','CP1165'}
    for e in d['events']:
        if e.get('camp_programme_id') in {'CP1166','CP1167','CP1168','CP1169'}:
            e['priority']='P2 — '+T('только с основным лагерем и подходящим возрастом','solo con campamento base y edad adecuada') if e['camp_programme_id']=='CP1166' else 'P3 — '+T('возраст и условия опции уточнить','confirmar edad y condiciones de opción')
            e['entry']=T('Оплатить и согласовать основной лагерь минимум 2 недели; затем отдельную доступную по возрасту опцию. Сама доплата не бронирует проживание или весь лагерь.',
                'Acordar y pagar campamento base mínimo 2 semanas; después opción separada disponible por edad. Suplemento por sí solo no reserva alojamiento ni campamento completo.')
            cover_start=(date.fromisoformat(e['start'])+timedelta(days=2)).isoformat()
            e['related_ids']=[x['id'] for x in d['events'] if x.get('camp_programme_id') in parents and x['start']<=(e['start'] if x['camp_programme_id']=='CP1164' else cover_start) and x['end']>=e['end']]
        if e.get('camp_programme_id') in {'CP1171','CP1172'}:e['priority']='P3 — '+T('язык и окончательный пакет уточнить','confirmar idioma y paquete final')
