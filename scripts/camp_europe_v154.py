"""Explicit Swiss day-camp weeks, current Zuoz terms, and separate family budgets."""
from camp_europe_v148 import lesson,weekdays

CHECKED='2026-11-05'
SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
SD='https://www.campsuisse.com/day-camp-dates-prices/'
SA='https://www.campsuisse.com/summer-day-camp/'
SF='https://www.campsuisse.com/crm/form.php'
SL='https://www.campsuisse.com/activities/languages-at-camp-suisse/'
SB='https://www.campsuisse.com/register-online/dates-and-prices/'
ST='https://www.campsuisse.com/wp-content/uploads/2017/11/Terms-updated-for-2018.pdf'
J='https://www.lyceum-alpinum.ch/en/summer-camps/junior-day-camp/'
B='https://www.lyceum-alpinum.ch/en/summer-camps/boarding-camp/'
I='https://www.lyceum-alpinum.ch/wp-content/uploads/2026/10/Cancellation-Insurance-International-Summer-Camp-2027.pdf'
JL='https://www.lyceum-alpinum.ch/wp-content/uploads/2024/11/Junior-Day-Camp-language-course-factsheet.pdf'
DS='https://www.lyceum-alpinum.ch/wp-content/uploads/2026/09/Factsheet-Digital-Skills.pdf'
AV='https://www.americanvillage.fr/sejour/printemps'
JOBS='https://www.job-americanvillage.com/en/dates-locations-vacation-camps'
SWEEKS=[('2027-06-21','2027-06-25'),('2027-06-28','2027-07-02'),('2027-07-05','2027-07-09'),('2027-07-12','2027-07-16'),
        ('2027-07-19','2027-07-23'),('2027-07-26','2027-07-30'),('2027-08-02','2027-08-06'),('2027-08-09','2027-08-13')]
ZUOZ_CANCEL=T('Текущая страница 2027: отмена за 60 и более дней без расходов; за 59–30 дней возвращают 50%; за 29 дней и меньше возврата нет, включая поздний приезд / no-show. После одобрения заявки выставляют полный счёт со сроком оплаты 15 дней; аванс не нужен, место резервируется после полной оплаты. Это не фиксированный дедлайн регистрации. Условия не принимались.',
 'Página actual de 2027: cancelación con 60 o más días sin cargo; con 59–30 días se devuelve 50%; con 29 días o menos sin devolución, incluidos llegada tardía / no-show. Tras aprobar solicitud emiten factura completa pagadera en 15 días; no exige anticipo, plaza reservada tras pago íntegro. No es plazo fijo de inscripción. Sin aceptar condiciones.')
ZUOZ_INS=T('Отдельная страховка отмены 2027: CHF 160 за две недели International либо CHF 30 за одну неделю Junior на участника. Действует от окончательной брони только до начала лагеря; во время смены уже недействительна. Названы болезнь / травма, события с близкими, забастовки и иные перечисленные риски; предвидимые / уже начавшиеся события исключены. Это не медицинское покрытие во время лагеря и не безусловный возврат; применимость полной страховки семье подтвердить.',
 'Seguro de cancelación de 2027 separado: CHF 160 por dos semanas International o CHF 30 por una semana Junior y participante. Desde reserva definitiva solo hasta inicio del campamento; deja de ser válido durante sesión. Incluye enfermedad / accidente, sucesos con allegados, huelgas y otros riesgos enumerados; excluye hechos previsibles / iniciados. No cubre salud durante campamento ni garantiza devolución incondicional; confirmar póliza completa para familia.')
JUNIOR_GATE=T('Junior 6–9: Матвей допускается только пока ещё 9, после десятилетия нужен другой поток. Оскар в 2027 имеет подходящие 6–7. Но связанный школой language factsheet адресован НЕ носителям выбранного языка и уровню beginner–intermediate: языковую пригодность обоих и применимость к 2027 подтвердить. Возможность учиться весь день на EN не устанавливает уровень языкового курса. Страница сезона предлагает EN / DE; французский из старого factsheet не добавлен как поток 2027.',
 'Junior 6–9: Matvey solo mientras tenga 9; tras cumplir diez necesita otro programa. Oscar en 2027 cumple edad de 6–7. Pero language factsheet enlazado por escuela se dirige a NO nativos del idioma elegido y nivel beginner–intermediate: confirmar adecuación de ambos y vigencia para 2027. Poder estudiar todo el día en EN no acredita nivel del curso lingüístico. Página de temporada ofrece EN / DE; francés del factsheet antiguo no se añade como opción 2027.')
SUISSE_TERMS=T('Сайт по-прежнему ссылается на Terms updated for 2018, код BA-DF-04-18-1.0. В таблице при отмене более чем за 56 дней удерживают deposit; за 56–43 / 42–29 / 28–15 / 14 и меньше дней — 60% / 70% / 80% / 100% общей цены. Это опубликованный связанный документ, не обещание отдельного договора 2027; применимость к day и актуальную редакцию получить до оплаты. Бронирование, acknowledgement и Confirmation Invoice в нём различаются. Согласие не давалось.',
 'Web sigue enlazando Terms updated for 2018, código BA-DF-04-18-1.0. Tabla retiene deposit al cancelar con más de 56 días; con 56–43 / 42–29 / 28–15 / 14 días o menos cobra 60% / 70% / 80% / 100% del total. Documento publicado enlazado, no promesa de contrato separado de 2027; obtener aplicación a day y versión vigente antes de pagar. Distingue reserva, acknowledgement y Confirmation Invoice. Sin dar consentimiento.')

def src(label,url):return dict(title=label,url=url,checked=CHECKED)
def merge(p,items):p['sources']=list({s['url']:s for s in p['sources']+items}.values())
def update_report(r):
    profiles={p['id']:p for p in r['profiles']}
    p=profiles['CP158']
    p['timing'].update(status='published_2027',label=T('Восемь опубликованных пятидневных вариантов 21 июня–13 августа 2027, каждый Пн–Пт 08:30–17:30. Форма перечисляет также 40 отдельных дней; выходные не включены. Это общий альпийский лагерь, не робототехнический интенсив.',
        'Ocho opciones publicadas de cinco días del 21 de junio al 13 de agosto de 2027, cada una lunes–viernes 08:30–17:30. Formulario enumera también 40 días individuales; sin fines de semana. Campamento alpino general, no intensivo de robótica.'),
        sessions=[list(s) for s in SWEEKS],session_details=[])
    p['language_evidence_role']='camp_life'
    p['price']['label']=T('CHF 200 за один день или CHF 1000 за конкретные пять будних дней. Для двух детей CHF 2000; с return minibus обоим на пять дней CHF 2200. Это не стоимость всего летнего сезона.',
        'CHF 200 por un día o CHF 1000 por cinco días laborables concretos. Dos niños CHF 2000; con return minibus de ambos cinco días CHF 2200. No es precio de toda temporada estival.')
    p['price']['deposit']=SUISSE_TERMS
    for n,(a,b) in enumerate(SWEEKS,1):
        p['timing']['session_details'].append(dict(start=a,end=b,label=T('Дневная неделя ','Semana diurna ')+str(n),
            price=T('CHF 1000 на ребёнка / пять дней; минибус CHF 20 за день туда-обратно на ребёнка отдельно.',
                    'CHF 1000 por niño / cinco días; minibus CHF 20 diarios de ida y vuelta por niño aparte.'),
            source=SF,formats=['day'],date_scope='session_days',
            sessions=[lesson(day,'08:30','17:30','Europe/Zurich',T('Альпийский дневной лагерь, обед и активности; язык camp life EN.',
                       'Campamento alpino diurno, almuerzo y actividades; idioma camp life EN.')) for day in weekdays(a,b)],
            proof=T('Неделя прямо перечислена в публичной форме 2027; часы и цена подтверждены отдельной Day Dates & Prices. Это чтение вариантов, не поданная заявка.',
                    'Semana enumerada expresamente en formulario público de 2027; horario y precio confirmados en Day Dates & Prices. Lectura de opciones, no solicitud enviada.')))
    merge(p,[src(T('2027 · точные недели и индивидуальные дни','2027 · semanas exactas y días individuales'),SF),
             src(T('Дневная цена и часы','Precio y horario diurnos'),SD),src(T('Дневной возраст и минибус','Edad diurna y minibus'),SA),
             src(T('English camp life; языковые уроки отдельно','English camp life; clases de idioma aparte'),SL),
             src(T('Связанный договор 2018 · не принят','Contrato enlazado de 2018 · sin aceptar'),ST)])
    p=profiles['CP157'];p['language_evidence_role']='camp_life'
    p['timing']['label']=T('Четыре основные двухнедельные смены 2027 сохранены. Для custom dates форма дополнительно публикует CHF 2200 за семь ночей Saturday–Saturday либо CHF 320 за ночь; конкретная custom-бронь и место требуют подтверждения.',
        'Conservadas cuatro sesiones principales de dos semanas de 2027. Para custom dates formulario publica además CHF 2200 por siete noches Saturday–Saturday o CHF 320 por noche; reserva custom y plaza requieren confirmación.')
    p['price']['label']=T('CHF 4400 / две недели. Форма: custom seven nights Saturday–Saturday CHF 2200, иные extra nights CHF 320. Custom-прайс не создаёт автоматически подтверждённые однодневные / недельные смены.',
        'CHF 4400 / dos semanas. Formulario: custom seven nights Saturday–Saturday CHF 2200, otras extra nights CHF 320. Precio custom no crea automáticamente sesiones diarias / semanales confirmadas.')
    p['price']['deposit']=T('FAQ: невозвратный аванс CHF 500 на участника входит в тариф, остаток за четыре недели. ',
                           'FAQ: anticipo no reembolsable de CHF 500 por participante incluido en tarifa, saldo cuatro semanas antes. ')+SUISSE_TERMS
    transfer=T('Публичная форма: детский Geneva transfer в предпочитаемые субботние часы включён; вне них CHF 250 за одно направление. Не выдавать это за цену трансфера родителей.',
        'Formulario público: Geneva transfer infantil incluido en horario preferido de sábado; fuera de él CHF 250 por trayecto. No presentar como tarifa de padres.')
    if transfer not in p['price']['extras']:p['price']['extras']+=' '+transfer
    merge(p,[src(T('2027 · custom nights и airport slots','2027 · custom nights y airport slots'),SF),
             src(T('Основные две недели и включения','Dos semanas principales e inclusiones'),SB),
             src(T('English camp life','English camp life'),SL),src(T('Связанный договор 2018','Contrato enlazado de 2018'),ST)])
    for ident in ['CP129','CP130']:
        p=profiles[ident];p['price']['deposit']=ZUOZ_CANCEL+' '+ZUOZ_INS
        if ZUOZ_INS not in p['price']['extras']:p['price']['extras']+=' '+ZUOZ_INS
        for v in p['timing']['session_details']:v['deposit']=p['price']['deposit'];v['extras']=p['price']['extras']
        merge(p,[src(T('Текущая страница 2027 · отмена 60 дней и оплата без аванса','Página actual de 2027 · cancelación 60 días y pago sin anticipo'),B if ident=='CP129' else J),
                 src(T('Отдельная страховка отмены именно 2027','Seguro de cancelación específico de 2027'),I)])
    p=profiles['CP129']
    p['timing']['label']=T('4–16 и 18–30 июля 2027, либо оба лагеря. Утренний Digital Skills выбирается отдельно от языков; открытую страницу регистрации не считать принятым местом.',
        '4–16 y 18–30 de julio de 2027, o ambos campamentos. Digital Skills matinal se elige aparte de idiomas; página de inscripción abierta no equivale a plaza aceptada.')
    merge(p,[src(T('Digital Skills 2027 · EN, оценка уровня и свой ноутбук','Digital Skills 2027 · EN, evaluación y portátil propio'),DS)])
    p=profiles['CP130'];p['language_evidence_role']='language_lessons'
    p['price']['included']=T('16 языковых уроков за неделю, обед, материалы, дневные активности и присмотр 08:30–16:00. Текущая страница включает местный pick-up / drop-off по запросу до St. Moritz / Madulain; аэропорт и жильё семьи не включены.',
        '16 clases de idioma por semana, almuerzo, materiales, actividades diurnas y supervisión 08:30–16:00. Página actual incluye pick-up / drop-off local bajo solicitud hasta St. Moritz / Madulain; aeropuerto y alojamiento familiar no incluidos.')
    p['language']=T('На 2027 подтверждён языковой курс EN или DE: 16 уроков в неделю и поощрение практики весь день. Это не Digital Skills и не техническое преподавание на EN. Связанный factsheet требует не-родной выбранный язык и beginner–intermediate; применимость и группу согласовать.',
        'Para 2027 confirmado curso de idioma EN o DE: 16 clases semanales y fomento de práctica todo el día. No es Digital Skills ni enseñanza técnica en EN. Factsheet enlazado exige idioma elegido no nativo y beginner–intermediate; acordar aplicación y grupo.')
    p['family_fit']['matvey']=dict(status='conditional',detail=JUNIOR_GATE)
    p['family_fit']['oscar']=dict(status='conditional',detail=JUNIOR_GATE)
    for v in p['timing']['session_details']:
        v['date_scope']='session_days'
        v['sessions']=[lesson(day,'08:30','16:00','Europe/Zurich',T('Junior: языковой курс, обед и дневные активности; не технический интенсив.',
            'Junior: curso de idioma, almuerzo y actividades diurnas; no intensivo técnico.')) for day in weekdays(v['start'],v['end'])]
    p['questions']=[JUNIOR_GATE]+[q for q in p['questions'] if q!=JUNIOR_GATE]
    merge(p,[src(T('Language factsheet · не-носители и уровень; дата файла старая, ссылка действующая','Language factsheet · no nativos y nivel; archivo antiguo, enlace vigente'),JL)])
    p=profiles['CP268']
    p['price']['label']=T('От EUR 779 за 11–16 апреля 2027, шесть дней / пять ночей. Окончательная цена зависит от выбранного города / транспорта; семейный счёт не выставлен.',
        'Desde EUR 779 por 11–16 de abril de 2027, seis días / cinco noches. Precio final depende de ciudad / transporte elegidos; sin factura familiar emitida.')
    staff=T('Клиентская карточка: 11–16 апреля; 9–16 апреля на job-сайте включают подготовку персонала. Летние job-периоды 2027 не являются подтверждёнными детскими сменами.',
        'Ficha de cliente: 11–16 de abril; 9–16 de abril en web job incluye preparación de personal. Periodos job estivales de 2027 no son sesiones infantiles confirmadas.')
    if staff not in p['questions']:p['questions'].append(staff)
    merge(p,[src(T('Клиентская смена · даты, возраст и от 779','Sesión de cliente · fechas, edad y desde 779'),AV)])
    for ident in ['CP129','CP130','CP157','CP158','CP268']:profiles[ident]['checked']=CHECKED
    r['counts']['source_urls']=len({s['url'] for p in r['profiles'] for s in p['sources']})
    r.update(version=154,asof=CHECKED)

def enrich_v154(d):
    offers=d['camp_planning']['offers'];o=next(o for o in offers if o['id']=='suisse-day-five')
    o.update(checked=CHECKED,sessions=[list(s) for s in SWEEKS],deposit_note=SUISSE_TERMS)
    o['sources']=list(dict.fromkeys(o['sources']+[SF,ST]))
    o=next(o for o in offers if o['id']=='lyceum-junior-week')
    o.update(checked=CHECKED,gate=JUNIOR_GATE,deposit_note=ZUOZ_CANCEL+' '+ZUOZ_INS,
             included=next(p for p in d['camp_programmes']['profiles'] if p['id']=='CP130')['price']['included'],
             optional=[dict(id='cancel_both',label=T('Страховка отмены обоим · 30 × 2 за одну неделю','Seguro de cancelación de ambos · 30 × 2 por una semana'),amount=60)])
    o['sources']=list(dict.fromkeys(o['sources']+[I,JL]))
    for ident in ['suisse-board-matvey','suisse-board-both-seven']:
        o=next(o for o in offers if o['id']==ident);o['deposit_note']=T('CHF 500 аванса на ребёнка входит в базу, не дополнительный платёж. ',
            'CHF 500 de anticipo por niño incluido en base, no pago adicional. ')+SUISSE_TERMS;o['checked']=CHECKED
    p=next(p for p in d['camp_programmes']['profiles'] if p['id']=='CP129')
    new=[dict(id='lyceum-digital-matvey-2027',slug=p['slug'],label=T('Zuoz Digital Skills · Матвею · один пансионный лагерь','Zuoz Digital Skills · Matvey · una sesión residencial'),
        currency='CHF',price_year=2027,format='boarding',children=['matvey'],base_by_child=dict(matvey=6200),discount_second=0,required=[],
        unknown_required=[dict(id='health_accident_liability',label=T('Медицинская, accident и liability страховка Матвея','Seguro médico, accident y liability de Matvey'),unit='amount',rate=1,min=0),
                          dict(id='own_laptop',label=T('Ноутбук, зарядка и адаптер · 0 только если уже есть подходящие','Portátil, cargador y adaptador · 0 solo si ya dispone de equipo adecuado'),unit='amount',rate=1,min=0)],
        optional=[dict(id='cancel',label=T('Отмена до начала · отдельная страховка на две недели','Cancelación antes de inicio · seguro separado de dos semanas'),amount=160),
                  dict(id='golf_kit',label=T('Golf bag / trolley только при выборе дневного Golf','Golf bag / trolley solo si elige Golf por la tarde'),amount=450)],
        unknown_trip=['travel','lodging','misc'],sessions=[['2027-07-04','2027-07-16'],['2027-07-18','2027-07-30']],sources=[B,DS,I],checked=CHECKED,
        gate=T('Только после 10-летия к заезду. В 2027 Матвею 9–10; конкретный трек, уровень и место подтвердить. Оскар ниже 10 и не включён в этот счёт; его Junior — отдельная программа.',
               'Solo tras cumplir 10 antes de llegada. En 2027 Matvey tiene 9–10; confirmar curso, nivel y plaza. Oscar menor de 10 y no incluido en presupuesto; su Junior es programa separado.'),
        deposit_note=ZUOZ_CANCEL+' '+ZUOZ_INS,included=p['price']['included'],
        scope=T('База CHF 6200 за одного ребёнка с пансионом; с выбранной страховкой отмены 6360. Семья обеспечивает отдельный уход Оскару и жильё взрослых. Четырёхнедельный тариф / выходные сюда не подставлены; это ещё не окончательный полный счёт.',
                'Base CHF 6200 por un niño con residencia; con seguro de cancelación elegido 6360. Familia organiza cuidado separado de Oscar y alojamiento adulto. No incorpora tarifa de cuatro semanas / fin de semana; aún no es factura completa final.'))]
    p=next(p for p in d['camp_programmes']['profiles'] if p['id']=='CP268')
    new.append(dict(id='american-village-spring-matvey-2027',slug=p['slug'],label=T('American Village · весна · только Матвей · минимальный тариф','American Village · primavera · solo Matvey · tarifa mínima'),
        currency='EUR',price_year=2027,price_basis='from',format='boarding',children=['matvey'],base_by_child=dict(matvey=779),discount_second=0,required=[],
        unknown_required=[dict(id='route_quote',label=T('Нужная доплата выбранного маршрута / города · по счёту','Suplemento necesario de ruta / ciudad elegida · según factura'),unit='amount',rate=1,min=0)],
        optional=[dict(id='insurance',label=T('Описанный страховой пакет · условия и применимость подтвердить','Paquete de seguro descrito · confirmar condiciones y aplicación'),amount=60)],
        unknown_trip=['travel','lodging','misc'],sessions=[['2027-04-11','2027-04-16']],sources=[AV],checked=CHECKED,
        gate=T('8–15: Матвею по возрасту подходит; индивидуальный иностранный приём и место неизвестны. Оскар ниже 8 и требует отдельной программы / ухода.',
               '8–15: Matvey cumple edad; admisión extranjera individual y plaza desconocidas. Oscar menor de 8 requiere programa / cuidado separado.'),
        deposit_note=p['price']['deposit'],included=p['price']['included'],
        scope=T('От EUR 779, с выбранным пакетом 60 база 839 до маршрута и поездки. Это английский общий лагерь и The Original 10 занятий по часу, не курс робототехники. 9 апреля — начало работы персонала, не заезд ребёнка.',
                'Desde EUR 779, con paquete elegido de 60 base 839 antes de ruta y viaje. Campamento general inglés y The Original de 10 clases de una hora, no curso de robótica. El 9 de abril empieza personal, no llegada infantil.')))
    index={o['id']:o for o in new};old={o['id'] for o in offers}
    d['camp_planning']['offers']=[index.get(o['id'],o) for o in offers]+[o for o in new if o['id'] not in old]
    d['camp_planning'].update(version=154,asof=CHECKED)
    rows={e['id']:e for e in d['events']}
    for ident,name in [('L170','Arduino Robotics'),('L171','Python Game Design'),('L172','AI / machine learning')]:
        e=rows[ident];archive=ident=='L172'
        e.update(checked=CHECKED,
            title='Lyceum Alpinum Zuoz · '+name+(' · '+T('модуль 2026 и новый курс 2027','módulo de 2026 y curso nuevo de 2027') if archive else ' · '+T('выбор курса 2027','elección de curso de 2027')),
            source=DS,related_ids=['CP129-20270704-20270716','CP129-20270718-20270730'],
            cost=T('Лагерь 2027: CHF 6200 / один заезд, Digital Skills выбирается в основном пакете. Нужен свой ноутбук и достаточная страховка; старые CHF 5800 относятся к 2026.',
                   'Campamento 2027: CHF 6200 / una sesión, Digital Skills se elige dentro de paquete principal. Requiere portátil propio y seguro adecuado; antiguos CHF 5800 corresponden a 2026.'),
            period=T('Общие лагеря 4–16 и 18–30 июля 2027; наличие конкретного курса и место в группе подтверждаются отдельно. Даты заездов в связанных карточках CP129.',
                     'Campamentos generales 4–16 y 18–30 de julio de 2027; confirmar curso concreto y plaza de grupo aparte. Fechas de estancia en fichas CP129 enlazadas.'),
            proof=T('Новый factsheet International Summer Camp 2027 прочитан; цифровые курсы taught in English, преподаватели EN / FR. Старые сведения 2026 отделены от нового предложения.',
                    'Leído nuevo factsheet International Summer Camp 2027; cursos digitales taught in English, instructores EN / FR. Información antigua de 2026 separada de nueva oferta.'))
        e['references']=list({r['url']:r for r in e.get('references',[])+[dict(url=DS,label=T('Digital Skills 2027 · четыре трека','Digital Skills 2027 · cuatro cursos')),dict(url=B,label=T('Возраст, даты пансиона и новые условия 2027','Edad, fechas residenciales y condiciones nuevas de 2027'))]}.values())
        if archive:
            e['note']=T('Исторический AI / machine learning 2026 был отдельным модулем 12–15. В 2027 опубликован другой AI & Innovation / Lean Startup внутри общего лагеря 10–17, не обещание того же курса ML. Для Матвея новый вариант только после 10-летия, Оскар ниже 10. Сравнить актуальное досье CP129; старая возрастная отметка описывала прежний модуль.',
                'AI / machine learning histórico de 2026 era módulo separado de 12–15. Para 2027 se publica otro AI & Innovation / Lean Startup en campamento general de 10–17, no promesa de mismo curso ML. Opción nueva de Matvey solo tras cumplir 10; Oscar menor de 10. Comparar ficha vigente CP129; marca de edad antigua describía módulo anterior.')
        else:
            e.update(age=T('Общий пансион 2027: 10–17; отдельного нового ограничения этого Digital Skills-трека не найдено, допуск подтвердить.',
                           'Residencia general de 2027: 10–17; sin encontrar nuevo límite separado de este curso Digital Skills, confirmar admisión.'),
                     mat=T('Условно: только после 10-летия к приезду и решения о группе.',
                           'Condicional: solo tras cumplir 10 antes de llegada y decisión de grupo.'),osc=T('Нет: младше 10 лет.', 'No: menor de 10 años.'),
                     note=T('Выбирается один утренний курс на заезд: эта карточка описывает трек, а не дополнительную независимую смену. 9 утренних занятий по 3.25 часа, брошюра округляет до 29 часов. Точные девять учебных дат не опубликованы; в календарь не внесены выдуманные ежедневные уроки.',
                            'Se elige un curso matinal por sesión: ficha de curso, no estancia independiente adicional. 9 clases matinales de 3.25 horas, folleto redondea a 29 horas. Nueve fechas lectivas exactas sin publicar; calendario no incorpora clases diarias inventadas.'))
