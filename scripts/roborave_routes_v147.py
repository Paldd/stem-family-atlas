"""RoboRAVE host, challenge and registration evidence; preserve local overrides."""
from copy import deepcopy
CHECKED='2026-11-04'
SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
ROOT='https://www.roboraveinternational.org/en/'
EVENTS=ROOT+'events'
VALLARTA=ROOT+'events/roborave-puerto-vallarta-open-2027'
GUIDE=ROOT+'guides/how-to-register-a-team'
GLOBAL_FLL='https://firstlegoleague.org/'
FLL_MX='https://www.firstlegoleagues.mx/preguntas-frecuentes/'
FEE=T('Страница события: 580 USD за каждого ученика и coach; список событий: 650 USD без единицы оплаты. Противоречие не разрешено. Минимум 2 ученика + 1 coach: базовый расчёт по первому тарифу 1740 USD за этих троих, не полный семейный счёт. Техника, дорога, взрослые и Оскар как гости, налоги, отмена и включение проживания ещё подтвердить.',
 'Página del evento: 580 USD por cada alumno y coach; lista de eventos: 650 USD sin unidad de pago. Discrepancia sin resolver. Mínimo 2 alumnos + 1 coach: cálculo base según primera tarifa 1740 USD para esas tres personas, no factura familiar completa. Confirmar equipo, viaje, adultos y Oscar como visitantes, impuestos, cancelación e inclusión de alojamiento.')
TEAM=T('2–4 ученика и не менее одного coach с RRID; один challenge на команду по странице Puerto Vallarta. Ограничение другого события может отличаться.',
 '2–4 alumnos y al menos un coach con RRID; un challenge por equipo según página Puerto Vallarta. Otro evento puede tener límites distintos.')
ENTRY=T('RRID каждого ученика и coach → событие → challenge → division → состав / RRTID → проверка суммы → подтверждение организатора. Бесплатный RRID, платёж и статус Confirmed различаются; заявка этой семьёй не выполнялась.',
 'RRID de cada alumno y coach → evento → challenge → division → integrantes / RRTID → revisión de importe → confirmación del organizador. RRID gratuito, pago y estado Confirmed son distintos; esta familia no ha realizado inscripción.')
LANG=T('Есть официальные EN/ES инструкции. Язык судейства, детского интервью и помощи на конкретном этапе ещё не подтверждён.',
 'Hay instrucciones oficiales EN/ES. Idioma de arbitraje, entrevista infantil y ayuda en etapa concreta aún sin confirmar.')
OSCAR=T('Нет по текущим минимальным рамкам: в 2027 исполнится только 7, а ES в таблице начинается с 8. Младшее исключение для этого challenge не опубликовано.',
 'No según mínimos actuales: en 2027 cumplirá solo 7 y tabla ES empieza en 8. Excepción menor para este challenge sin publicar.')
MAT_ES=T('Да по возрасту ES 8–11: в 2027 исполнится 10; нужен подходящий партнёр и подтверждение команды.',
 'Sí por edad ES 8–11: en 2027 cumplirá 10; necesita compañero adecuado y confirmación del equipo.')
MAT_CONFLICT=T('Условно: таблица ES 8–11 расходится с общим возрастом или текстом категории. Нужны действующая редакция и точная дата рождения; допуск не обещан.',
 'Condicional: tabla ES 8–11 discrepa de edad general o texto de categoría. Se requieren edición vigente y fecha exacta de nacimiento; admisión sin prometer.')
AGE8=T('Баннер от 8; ES 8–11, MS 11–14, HS 14–18. Возрастная отсечка и правило смешанной команды ещё уточняются.',
 'Cabecera desde 8; ES 8–11, MS 11–14, HS 14–18. Confirmar corte de edad y regla de equipo mixto.')
AGE10=T('Баннер 10–99, таблица ES 8–11: нижняя граница противоречива. В феврале 2027 Матвею 9–10; решение по редакции и дню рождения, не по одному тегу ES.',
 'Cabecera 10–99, tabla ES 8–11: mínimo contradictorio. En febrero de 2027 Matvey tendrá 9–10; decidir según edición y cumpleaños, no solo etiqueta ES.')
AGE12=T('Баннер 12–99; список MS 11–14 / HS / UP, но основной текст упоминает ES. Это противоречие, а не установленный младший допуск.',
 'Cabecera 12–99; lista MS 11–14 / HS / UP, pero texto principal menciona ES. Es discrepancia, no admisión infantil acreditada.')

def challenge_specs():
    return [
      ('a-maze-ing','a-MAZE-ing',T('Баннер 8–15; таблица ES 8–11 / MS 11–14 / HS 14–18 — общий верх тоже расходится. Для Матвея ES возраст возможен; локальную отсечку подтвердить.',
       'Cabecera 8–15; tabla ES 8–11 / MS 11–14 / HS 14–18 — máximo general también discrepante. Edad ES posible para Matvey; confirmar corte local.'),
       T('Автономный робот: минимум 2 колеса и свободное опорное колесо. Внешние датчики запрещены, энкодеры колёс разрешены. Робот идёт по приподнятому деревянному лабиринту. Объём напечатан как 65030 cm³; значение и формат уточнить, не исправлены догадкой.',
        'Robot autónomo: mínimo 2 ruedas y rueda de apoyo libre. Sensores externos prohibidos, encoders de rueda permitidos. Recorre laberinto elevado de madera. Volumen impreso como 65030 cm³; confirmar valor y formato, sin corregir por suposición.'),True),
      ('entrepreneurial','Entrepreneurial',AGE12,T('Рабочий робот / продукт с Input–Process–Output, демонстрация, одностраничный marketing flyer и Business Model Canvas; прототип до 3000 USD. Текст объединяет ES/MS, хотя metadata младший ES не предлагает. Награда и exhibition-only при малом числе команд различаются.',
       'Robot / producto funcional con Input–Process–Output, demostración, marketing flyer de una página y Business Model Canvas; prototipo hasta 3000 USD. Texto agrupa ES/MS, aunque metadata no ofrece ES menor. Premio y exhibition-only con pocos equipos son distintos.'),False),
      ('firefighting','Firefighting',AGE10,T('Автономное тушение 4 свечей за 3 минуты; робот до 1500 USD. Проверяется управление тушением датчиком; пропеллер до 12 cm с защитой. Подготовку с огнём и технические проверки проводит допустимая команда по правилам площадки.',
       'Extinción autónoma de 4 velas en 3 minutos; robot hasta 1500 USD. Se verifica control de extinción mediante sensor; hélice hasta 12 cm con protección. Equipo admitido realiza preparación con fuego y verificaciones técnicas según reglas de sede.'),False),
      ('alpine','AlpineBot',AGE12,T('Автономно подняться по крутому склону, выйти на стол и поставить флаг; заявлена оценка времени. Младшие divisions в разных блоках расходятся, а подробный раздел Check-In обрывается; полный действующий регламент запросить.',
       'Subir pendiente de forma autónoma, llegar a mesa y colocar bandera; se anuncia puntuación por tiempo. Divisions menores discrepan entre bloques y sección Check-In detallada queda incompleta; obtener reglamento vigente completo.'),False),
      ('sumolego','SumoLEGO',AGE8,T('Автономный LEGO, только детали LEGO; класс 1 kg, габариты 25 × 18 cm, высота не ограничена. Стоимость робота до 1500 USD. Кольцо 100 cm; это не автоматически те же размеры, что у прежнего турнира семьи или Korea Open.',
       'LEGO autónomo, solo piezas LEGO; clase 1 kg, dimensiones 25 × 18 cm, altura sin límite. Robot hasta 1500 USD. Ring de 100 cm; no equivale automáticamente a medidas del torneo anterior de familia o Korea Open.'),True),
      ('sumoopen','SumoOpen',AGE10,T('Автономный робот до 1500 USD; 25 × 18 cm без ограничения высоты. В таблице классы 1 kg / 3 kg, ES связан с 1 kg; точную локальную весовую категорию подтвердить. Нельзя намеренно разрушать соперника.',
       'Robot autónomo hasta 1500 USD; 25 × 18 cm sin límite de altura. Tabla con clases 1 kg / 3 kg, ES asociado a 1 kg; confirmar categoría de peso local exacta. Sin destrucción intencionada del rival.'),False),
      ('soccerbot','SoccerBot RC',AGE10,T('2 радиоуправляемых робота; таблица 800 g, габариты 15 × 15 × 15 cm. Лимит 500 USD в описании пары: единицу стоимости подтвердить. Батарейное питание, мячу нельзя перекрывать более 30% объёма; роботов между командами не делят.',
       '2 robots por radiocontrol; tabla 800 g, dimensiones 15 × 15 × 15 cm. Límite 500 USD en descripción de pareja: confirmar unidad de coste. Baterías, no encerrar más de 30% del balón; no compartir robots entre equipos.'),False),
      ('fastbot','FastBot',AGE8,T('Автономный line follower до 1500 USD с обязательным IR-датчиком и рабочим кодом линии при check-in. Число кругов и трассу задаёт division / директор; лимит попытки 3 минуты, касание завершает заезд.',
       'Line follower autónomo hasta 1500 USD con sensor IR obligatorio y código de línea funcional en check-in. Division / director fija vueltas y pista; límite de intento 3 minutos, tocar termina recorrido.'),True),
      ('roboethics','RoboEthics',T('Metadata предлагает ES 8–11 и баннер 10–99; основной текст — обычно HS/UP и ровно 2 участника вместо metadata 2–4. Возраст и состав противоречивы, младшее участие не подтверждено.',
       'Metadata ofrece ES 8–11 y cabecera 10–99; texto principal suele HS/UP y exactamente 2 integrantes frente a metadata 2–4. Edad y composición discrepantes, participación infantil sin confirmar.'),
       T('Тема 2027: аргументы за и против паузы развития ИИ. Требуется подготовить обе позиции; это дебаты, а не сборка робота. Четыре зарегистрированные команды нужны для официального challenge; иначе возможно объединение или показ.',
        'Tema 2027: argumentos a favor y contra pausa del desarrollo de IA. Preparar ambas posiciones; son debates, no construcción de robot. Cuatro equipos inscritos necesarios para challenge oficial; en otro caso posible fusión o exhibición.'),False),
    ]

def refs(*items):return [dict(label=label,url=url) for label,url in items]
def enrich_v147(d):
    idx={e['id']:e for e in d['events']}
    parent=idx['C082'];parent.update(checked=CHECKED,format=TEAM,entry=ENTRY,cost=FEE,language=LANG,languages=[],language_mode='unconfirmed',language_certainty=LANG,
        evidence_level='event_page',proof=T('Текущая страница события сверена с каталогом, всеми связанными challenge и руководством регистрации. Цена и возрастные противоречия сохранены явно.',
        'Página actual del evento contrastada con catálogo, todos los challenge enlazados y guía de registro. Discrepancias de precio y edad conservadas explícitamente.'),
        age=T('Девять challenge на странице события: младший ES в таблицах от 8, у части задач баннеры 10 / 12 и текст расходятся. Братьям нельзя автоматически заявиться одной младшей командой.',
              'Nueve challenge en página del evento: ES menor desde 8 en tablas, algunas tareas tienen cabeceras 10 / 12 y textos discrepantes. Hermanos no pueden inscribirse automáticamente como un equipo menor.'),
        mat=MAT_ES,osc=OSCAR,deadline='',date_scope='festival_window',
        registration_status=T('На странице регистрация открыта; 60 команд — объявленная вместимость, не остаток мест. Срок закрытия и окончательный счёт не опубликованы однозначно.',
             'Página indica registro abierto; 60 equipos es aforo anunciado, no plazas restantes. Cierre y factura final sin publicar inequívocamente.'),
        note=T('25–28 февраля 2027 — окно фестиваля, конкретный день каждого challenge неизвестен. Взнос за человека, не за всю команду. Проживание из соседней Ruta Científica не перенесено в робототехнический пакет. Houston — следующий отдельный допуск, не автоматическая награда за поездку.',
             '25–28 de febrero de 2027 es periodo del festival, día concreto de cada challenge desconocido. Cuota por persona, no por equipo completo. Alojamiento de Ruta Científica vecina no se traslada al paquete robótico. Houston requiere admisión siguiente separada, no premio automático por viajar.'),
        references=refs((T('Список событий: другой тариф 650 USD','Lista de eventos: otra tarifa 650 USD'),EVENTS),(T('Руководство регистрации и подтверждения','Guía de registro y confirmación'),GUIDE)))
    new_ids=[]
    for n,(slug,name,age,gear,clear) in enumerate(challenge_specs(),1199):
        ident='C'+str(n);e=deepcopy(parent)
        e.update(id=ident,title='RoboRAVE Puerto Vallarta 2027 · '+name,parent_event_id='C082',age=age,gear=gear,mat=MAT_ES if clear else MAT_CONFLICT,osc=OSCAR,
            source=ROOT+'challenges/'+slug,priority=('P2 — ' if clear else 'P3 — ')+T('после проверки challenge и состава','tras comprobar challenge e integrantes'),
            action=T('Подтвердить редакцию, возрастную отсечку, состав и итоговый тариф этого challenge. Матвею нужен партнёр подходящего возраста; Оскара не включать по одному тегу ES.',
                     'Confirmar edición, corte de edad, integrantes y tarifa final de este challenge. Matvey necesita compañero de edad adecuada; no incluir a Oscar solo por etiqueta ES.'),
            proof=T('Прочитаны карточка challenge, полный доступный текст, divisions и связь с конкретным Puerto Vallarta. Расхождения блоков сохранены явно.',
                    'Leídos ficha de challenge, texto completo disponible, divisions y enlace al Puerto Vallarta concreto. Discrepancias entre bloques conservadas explícitamente.'),
            references=refs((T('Событие и цена за человека','Evento y precio por persona'),VALLARTA),(T('Список с другим тарифом','Lista con otra tarifa'),EVENTS),(T('Порядок подтверждения регистрации','Proceso de confirmación de registro'),GUIDE)),
            themes=['robotics','ai'] if slug=='roboethics' else ['robotics','entrepreneurship'] if slug=='entrepreneurial' else ['robotics'],evidence_level='rules')
        e.pop('related_ids',None)
        if slug=='roboethics':e['format']=T('Metadata 2–4, основной текст ровно 2; применимый состав подтвердить. Coach отдельно.',
             'Metadata 2–4, texto principal exactamente 2; confirmar composición aplicable. Coach aparte.')
        else:e.update(team_min=2,team_max=4)
        if ident in idx:idx[ident].update(e)
        else:d['events'].append(e);idx[ident]=e
        new_ids.append(ident)
    parent['related_ids']=list(dict.fromkeys(parent.get('related_ids',[])+new_ids))
    overview=idx['C052'];overview.update(checked=CHECKED,source=EVENTS,entry=ENTRY,format=TEAM,age=parent['age'],cost=T('RRID бесплатен; способ оплаты и стоимость определяет конкретное событие. Puerto Vallarta: 580 USD за человека против 650 USD без единицы в списке; не переносить этот тариф на всю сеть.',
        'RRID gratuito; cada evento fija modalidad de pago y precio. Puerto Vallarta: 580 USD por persona frente a 650 USD sin unidad en lista; no trasladar esa tarifa a toda la red.'),
        references=refs((T('Текущий порядок регистрации','Proceso actual de registro'),GUIDE)),note=T('Глобальный challenge и локальная поправка имеют разные области действия. Печатный ES / возраст, grade и размер команды сверяются отдельно для каждого этапа.',
        'Challenge global y modificación local tienen ámbitos distintos. ES / edad, curso escolar y tamaño de equipo se comprueban por separado en cada etapa.'))
    overview['mat']=T('Условно: выбрать конкретное событие и подтверждённый challenge / division.','Condicional: elegir evento concreto y challenge / division confirmado.')
    overview['osc']=T('Условно только после проверки младшего локального пути; глобальный ES 8+ в 2027 ещё рано.','Condicional solo tras comprobar vía local menor; ES global 8+ aún temprano en 2027.')
    guanajuato=idx['C083'];guanajuato.update(checked=CHECKED,start='',end='',deadline='',date_status='Предварительные даты',scope='national',
        period=T('21–22 мая 2027 указаны как tentative; не включены в календарь подтверждённых дат.',
                 '21–22 de mayo de 2027 figuran como tentative; no incluidos en calendario de fechas confirmadas.'),
        planned_windows=[dict(start='2027-05-21',end='2027-05-22',status='tentative')],
        mat=T('Условно: местные challenge и возраст ещё не объявлены.','Condicional: challenge y edades locales aún sin anunciar.'),osc=T('Условно: младший путь с 6/7 лет не объявлен; глобальный ES начинается с 8.','Condicional: vía menor desde 6/7 sin anunciar; ES global empieza en 8.'),
        registration_status=T('Общий список: To be announced; кнопка Register не подтверждает открытый набор.','Lista general: To be announced; botón Register no confirma convocatoria abierta.'),
        note=T('Название Open / International и текст NATIONAL расходятся; список сети классифицирует этап как National. Тело явно называет даты tentative; ожидаемые 100 команд не фактический список. Площадка и тариф ещё неизвестны.',
               'Nombre Open / International y texto NATIONAL difieren; lista de red clasifica etapa National. Texto califica fechas de tentative; 100 equipos esperados no son lista real. Sede y tarifa aún desconocidas.'))
    for ident,slug,status in [('C084','china-beijing','open'),('C085','thursday-june-3-2027','not_announced'),('C086','taiwan-open-2027','not_announced'),('C087','roborave-world-championship-houston-2027','coming_soon')]:
        e=idx[ident];e.update(source=ROOT+'events/'+slug,checked=CHECKED,
            registration_status=T('Состояние набора в списке сети: ','Estado de convocatoria en lista de red: ')+status,
            references=list(e.get('references',[]))+refs((T('Свежая страница сети и статус набора','Página actual de red y estado de convocatoria'),EVENTS)))
        e['references']=list({x['url']:x for x in e['references']}.values())
    idx['C086']['note']=T('27–28 июля 2027, Taipei, точная площадка Por confirmar. Список challenge, возраст, язык, цена и квоты ещё не опубликованы. Статус списка To be announced; регистрация и семейный билет не подтверждены.',
        '27–28 de julio de 2027, Taipei, sede exacta Por confirmar. Challenge, edad, idioma, precio y cupos aún sin publicar. Lista indica To be announced; registro y entrada familiar sin confirmar.')
    idx['C087']['registration_status']=T('Coming soon; действующий соревновательный набор и квота семьи ещё не подтверждены.',
        'Coming soon; convocatoria competitiva vigente y cupo familiar aún sin confirmar.')
    for ident in ['C084','C086','C087']:
        idx[ident].update(age=T('Список challenge и divisions этого этапа ещё не объявлен на текущей странице. Глобальные рамки задачи — ориентир, не предложение конкретной категории.',
                              'Lista de challenge y divisions de esta etapa aún sin anunciar en página actual. Límites globales de reto son referencia, no oferta de categoría concreta.'),
            mat=overview['mat'],osc=overview['osc'])
    # Keep Korea's published local grade rule and dated discipline days. A
    # different global age table cannot silently replace that local rule.
    korean_note=T('Локальные правила Korea используют текущую школу, глобальная карточка ES — возраст 8–11; отдельные технические размеры тоже различаются. Применимость возрастной таблицы к иностранным детям согласовать, локальное правило не заменено глобальным.',
        'Reglas locales Korea usan colegio actual, ficha global ES edad 8–11; también difieren dimensiones técnicas. Acordar aplicación de tabla de edad a menores extranjeros, sin sustituir regla local por global.')
    for ident in ['C1148','C1149','C1150']:
        e=idx[ident];e['checked']=CHECKED
        if korean_note not in e['note']:e['note']+=' '+korean_note
        e['references']=list({r['url']:r for r in e.get('references',[])+refs((T('Глобальные возрастные таблицы: отдельная область действия','Tablas globales de edad: ámbito separado'),ROOT+'challenges/'+{'C1148':'sumolego','C1149':'fastbot','C1150':'soccerbot'}[ident]))}.values())
    route_url='https://roboraveinternational.org/eventos/roborave-ruta-cientifica-puerto-vallarta-2027'
    route=deepcopy(parent);route.update(id='E211',block='События',title='RoboRAVE · Ruta Científica / World Science & Technology Expo · Puerto Vallarta 2027',source=route_url,
        age=T('Общий анонс приглашает Primary и семьи; связанный Ruta challenge — 13–99, MS 11–14 / HS / UP. Детский показ проекта и семейный вход требуют отдельного согласования.',
              'Anuncio general invita Primary y familias; Ruta challenge enlazado indica 13–99, MS 11–14 / HS / UP. Exposición infantil y entrada familiar requieren acuerdo separado.'),
        mat=MAT_CONFLICT,osc=T('Условно только как семейный посетитель: возрастной вход и цена гостя не опубликованы. В связанный Ruta challenge по опубликованным рамкам не подходит.',
            'Condicional solo como visitante familiar: edad de entrada y tarifa de invitado sin publicar. No cumple límites publicados del Ruta challenge enlazado.'),
        gear=T('Технологические, дидактические и программные прототипы: показ и объяснение проекта. Младший формат и фактическое расписание уточнить.',
               'Prototipos tecnológicos, didácticos y de software: exposición y explicación del proyecto. Confirmar formato infantil y horario real.'),
        level=T('Международная научно-технологическая программа показа','Programa internacional de exposición científico-tecnológica'),
        proof=T('Прочитаны отдельный анонс Ruta, включения и противоречивые сроки; связанный challenge проверен отдельно.',
                'Leídos anuncio Ruta separado, inclusiones y plazos discrepantes; challenge enlazado comprobado aparte.'),
        format=T('Научно-технологический показ и международная программа; анонс прямо говорит, что это не традиционное соревнование.',
                 'Exposición científico-tecnológica y programa internacional; anuncio declara expresamente que no es competición tradicional.'),participation='visitor',
        reward=T('Сертификат участия и презентация проекта; не доказательство международной призовой победы.',
                 'Certificado de participación y presentación de proyecto; no acredita victoria internacional con premio.'),
        cost=T('Страница: 580 USD за участника / coach, включает заявленные проживание, еду / напитки и программу 25–28 февраля. Число ночей, размещение, плата родителей / младшего гостя, отмена и итоговый семейный счёт неизвестны. Дорога, личные трансферы и миграционные расходы исключены.',
               'Página: 580 USD por participante / coach, incluye alojamiento, comida / bebidas y programa 25–28 de febrero anunciados. Noches, habitación, precio de padres / invitado menor, cancelación y factura familiar final desconocidos. Excluye viaje, traslados personales y gastos migratorios.'),
        deadline='',registration_status=T('Противоречие: текст закрывает регистрацию / оплату 31 октября, ниже пишет окно 16 октября–15 ноября; интерфейс показывает Registro abierto. Новый допуск не подтверждён.',
            'Discrepancia: texto cierra registro / pago 31 de octubre, después indica periodo 16 de octubre–15 de noviembre; interfaz muestra Registro abierto. Admisión nueva sin confirmar.'),
        entry=T('Отдельная заявка Ruta и категория проекта / семейного посетителя. Сначала разрешить противоречия срока и возраста; регистрация робототехнического Open не заменяет допуск сюда.',
                'Solicitud Ruta separada y categoría de proyecto / visitante familiar. Resolver antes contradicciones de plazo y edad; registro del Open robótico no sustituye admisión aquí.'),
        note=T('Совпадают город, даты и гостиница с Open, но это другая программа и пакет. Её гостиничные включения не перенесены на Open. Уровни Primary в анонсе и MS / 13+ в связанном challenge расходятся; точные дни докладов не объявлены.',
               'Comparte ciudad, fechas y hotel con Open, pero programa y paquete son distintos. Inclusiones hoteleras no se trasladan al Open. Primary del anuncio y MS / 13+ del challenge enlazado discrepan; días exactos de presentaciones sin anunciar.'),
        references=refs((T('Связанный Ruta challenge: возраст и состав','Ruta challenge enlazado: edad e integrantes'),'https://roboraveinternational.org/retos/ruta-roborave')),related_ids=['C082'],priority='P3 — '+T('возраст, срок и гостевой пакет уточнить','confirmar edad, plazo y paquete visitante'),evidence_level='event_page')
    if route['id'] not in idx:
        d['events'].append(route)
        idx[route['id']]=route
    elif not idx[route['id']].get('canonical_event_id'):
        idx[route['id']].update(route)
    fll_cr_language=T('Язык занятий и защиты местного BIOGLOW ещё не подтверждён. Глобальное описание не устанавливает язык конкретного потока Costa Rica.',
                     'Idioma de clases y defensa BIOGLOW local aún sin confirmar. Descripción global no determina idioma del grupo concreto Costa Rica.')
    cr=idx['C003'];cr.update(checked=CHECKED,source=GLOBAL_FLL,languages=[],language_mode='unconfirmed',language=fll_cr_language,language_certainty=fll_cr_language,
        evidence_level='catalog',proof=T('В текущем глобальном каталоге подтверждён партнёр Fundación STEAM. Локальные условия BIOGLOW не подтверждены; HTTPS сайта завершился ошибкой сертификата, её обход не выполнялся.',
            'Directorio global actual confirma socio Fundación STEAM. Condiciones locales BIOGLOW sin confirmar; HTTPS terminó con error de certificado, sin eludirlo.'),
        format=T('Размер и школьный состав команды Costa Rica ещё подтвердить; размер другой страны автоматически не применяется.',
                 'Confirmar tamaño y composición escolar del equipo Costa Rica; tamaño de otro país no se aplica automáticamente.'),
        age=T('Глобальный ориентир Explore 6–10 / Challenge 9–16 с местными отличиями; условия Costa Rica BIOGLOW ещё не подтверждены текущим локальным анонсом.',
              'Referencia global Explore 6–10 / Challenge 9–16 con variantes locales; condiciones Costa Rica BIOGLOW aún sin confirmar mediante anuncio local actual.'),
        mat=T('Условно: возраст возможен по глобальному ориентиру, местный набор и категория неизвестны.','Condicional: edad posible según referencia global, convocatoria y categoría locales desconocidas.'),
        osc=T('Условно: Explore возможен по глобальному возрасту; местный набор, класс и состав неизвестны.','Condicional: Explore posible por edad global; convocatoria, curso y composición locales desconocidos.'),
        entry=T('Текущий глобальный каталог указывает Fundación STEAM для Costa Rica. Местный сайт не открылся из-за истёкшего TLS-сертификата; найденный запуск относится к UNEARTHED 2025–26. Не переносить разрешение независимых команд México на Costa Rica.',
                'Directorio global actual señala Fundación STEAM para Costa Rica. Web local no abrió por certificado TLS caducado; lanzamiento localizado pertenece a UNEARTHED 2025–26. No trasladar permiso de equipos independientes México a Costa Rica.'),
        gear=T('Founders: глобальные SPIKE Essential / Prime; разрешённые старые наборы и доступность Future именно в Costa Rica ещё подтвердить.',
               'Founders: SPIKE Essential / Prime globales; confirmar equipos antiguos permitidos y disponibilidad Future concreta en Costa Rica.'),
        priority='P2 — '+T('подтвердить местный BIOGLOW у партнёра','confirmar BIOGLOW local con socio'),
        note=T('Партнёр страны подтверждён каталогом, но не объявлены текущие даты, прайс, возрастная отсечка и иностранный / независимый вход. Медали Explore и конкурсные места Challenge различаются. Сезон 2026/27 последний FLL; новые правила после него отдельно.',
               'Socio nacional confirmado por directorio, pero fechas actuales, precio, corte de edad y admisión extranjera / independiente sin anunciar. Medallas Explore y puestos competitivos Challenge son distintos. Temporada 2026/27 última FLL; reglas posteriores aparte.'),
        references=refs((T('Локальный сайт: доступ не получен','Web local: acceso no obtenido'),'https://www.firstlegoleaguecr.com/')))
    tmr=idx['C043'];tmr.update(checked=CHECKED,registration_status=T('Сайт TMR 2027 открыт как страница в подготовке; convocatoria, календарь записи и правила ещё обещаны к публикации.',
         'Web TMR 2027 abierta como página en preparación; convocatoria, calendario de inscripción y reglas aún pendientes de publicación.'),
         references=list({r['url']:r for r in tmr.get('references',[])+refs((T('Новый официальный портал TMR 2027','Portal oficial nuevo TMR 2027'),'https://femexrobotica.org/tmr2027/'))}.values()))
    for ident in ['C004','C005','C1127','C1128','C1129','C1130']:idx[ident]['checked']=CHECKED
    guide=d['league_guide'];guide['version']=147;g=next(g for g in guide['profiles'] if g['id']=='roborave')
    g.update(age_summary=parent['age'],summary=T('Международная сеть открытых испытаний; все 9 challenge Puerto Vallarta прочитаны отдельно, общий тег ES не заменяет регламент.',
         'Red internacional de retos abiertos; los 9 challenge Puerto Vallarta leídos por separado, etiqueta ES general no sustituye reglamento.'),route=ENTRY,hardware=T('Для раннего самостоятельного старта Матвея сравнить a-MAZE-ing, SumoLEGO и FastBot. Размеры LEGO и поля не переносятся между этапами; Korea публикует собственные поправки.',
         'Para inicio autónomo temprano de Matvey comparar a-MAZE-ing, SumoLEGO y FastBot. Medidas LEGO y campo no se trasladan entre etapas; Korea publica modificaciones propias.'),language=LANG,cost=FEE,
         requirements=[TEAM,T('У каждого ученика и coach свой RRID; дети находятся в системе только по точному ID. Взрослый ведёт регистрацию и платежи.',
             'Cada alumno y coach tiene RRID propio; menores se localizan en sistema solo con ID exacto. Adulto gestiona registro y pagos.')],
         evidence=T('Прочитаны текущие события, все 9 challenge Puerto Vallarta, руководство регистрации и отдельная Ruta Científica. Несогласованные даты / цены / возраста не нормализованы догадкой.',
             'Leídos eventos actuales, los 9 challenge Puerto Vallarta, guía de registro y Ruta Científica separada. Fechas / precios / edades discrepantes no se normalizan por suposición.'))
    g['event_ids']=list(dict.fromkeys(g['event_ids']+new_ids+['C1148','C1149','C1150']))
    g['categories']=[dict(name=idx[i]['title'],age=idx[i]['age'],age_rule=T('Проверить конкретное событие, баннер, таблицу division и полный текст; местное правило не заменяется глобальным.',
        'Comprobar evento concreto, cabecera, tabla division y texto completo; regla local no se sustituye por global.'),team=idx[i]['format'],hardware=idx[i]['gear'],entry=idx[i]['entry'],event_id=i) for i in g['event_ids']]
    nuances=[T('Оскар 2020 года рождения ещё не достигает ES 8 в 2027. Для Matvey + Oscar команда Puerto Vallarta по текущим таблицам не подтверждается; для Matvey нужен партнёр допустимого возраста.',
        'Oscar nacido en 2020 aún no alcanza ES 8 en 2027. Equipo Matvey + Oscar Puerto Vallarta no acreditado según tablas actuales; Matvey necesita compañero de edad admitida.'),
        T('RoboEthics: metadata ES и 2–4, текст HS/UP и 2. Entrepreneurial / Alpine: metadata 12+ без ES, основной текст ES допускает. Firefighting / SumoOpen / SoccerBot: баннер 10+, таблица ES 8–11.',
          'RoboEthics: metadata ES y 2–4, texto HS/UP y 2. Entrepreneurial / Alpine: metadata 12+ sin ES, texto principal admite ES. Firefighting / SumoOpen / SoccerBot: cabecera 10+, tabla ES 8–11.'),
        T('Guanajuato 21–22 мая только tentative. Houston 5–7 ноября: Coming soon и площадка TBA. Аккредитация после Open не автоматическая мировая победа и не подтверждённая квота.',
          'Guanajuato 21–22 de mayo solo tentative. Houston 5–7 de noviembre: Coming soon y sede TBA. Acreditación tras Open no es victoria mundial automática ni cupo confirmado.')]
    g['nuances']=list(dict.fromkeys(g['nuances']+nuances))
    fresh=[dict(title=idx[i]['title'],url=idx[i]['source'],checked=CHECKED) for i in new_ids]+[dict(title=T('Свежие события и цены','Eventos y precios actuales'),url=EVENTS,checked=CHECKED),dict(title=T('От RRID до Confirmed','De RRID a Confirmed'),url=GUIDE,checked=CHECKED),dict(title=T('Puerto Vallarta: текущая цена и единица оплаты','Puerto Vallarta: precio y unidad de pago actuales'),url=VALLARTA,checked=CHECKED)]
    g['sources']=list({s['url']:s for s in g['sources']+fresh}.values())
    first=next(g for g in guide['profiles'] if g['id']=='first')
    first['sources']=list({s['url']:s for s in first['sources']+[dict(title=T('Текущий глобальный каталог: Fundación STEAM Costa Rica','Directorio global actual: Fundación STEAM Costa Rica'),url=GLOBAL_FLL,checked=CHECKED)]}.values())
    for cat in first['categories']:
        if cat.get('event_id')=='C003':cat.update(age=cr['age'],team=cr['format'],hardware=cr['gear'],entry=cr['entry'])
    f=d['family_strategy'];f['version']=147;f['checked']=CHECKED
    mat_step=T('RoboRAVE Puerto Vallarta: для SumoLEGO / FastBot / a-MAZE-ing искать партнёра 8–11, а не записывать младшего брата автоматически. Сначала собственная программа и серия повторяемых испытаний, затем согласованный challenge и счёт.',
        'RoboRAVE Puerto Vallarta: para SumoLEGO / FastBot / a-MAZE-ing buscar compañero 8–11, sin inscribir automáticamente al hermano menor. Primero programa propio y pruebas repetibles, después challenge y factura acordados.')
    osc_step=T('В 2027 RoboRAVE ES 8+ пока рано по опубликованным глобальным таблицам. Сохранить младший учебный / соревновательный маршрут и семейный показ; корейский школьный override требует собственного подтверждения.',
        'En 2027 RoboRAVE ES 8+ aún temprano según tablas globales publicadas. Mantener vía educativa / competitiva menor y exposición familiar; modificación coreana por colegio requiere confirmación propia.')
    for kid,step in [('mat',mat_step),('osc',osc_step)]:
        if step not in f['children'][kid]['current']:f['children'][kid]['current'].append(step)
    action=dict(period=T('Перед сезоном 2027','Antes de temporada 2027'),title=T('Состав и бюджет под конкретный регламент','Equipo y presupuesto según reglamento concreto'),
        detail=T('FLL México Future 6–9 требует 4 учеников, двоих братьев недостаточно. Глобальный RoboRAVE ES от 8: для Матвея нужен другой партнёр. Минимальный состав 2 ученика + 1 coach: базовые 1740 USD по тарифу 580 за человека; в списке 650 без единицы, полный счёт неизвестен. Для Costa Rica сначала подтвердить текущий BIOGLOW у Fundación STEAM; сайт со старым запуском не доказывает новый набор.',
            'FLL México Future 6–9 exige 4 alumnos, dos hermanos no bastan. RoboRAVE ES global desde 8: Matvey necesita otro compañero. Mínimo 2 alumnos + 1 coach: base 1740 USD según tarifa 580 por persona; lista indica 650 sin unidad, factura completa desconocida. Para Costa Rica confirmar primero BIOGLOW actual con Fundación STEAM; web con lanzamiento antiguo no acredita convocatoria nueva.'))
    f['actions']=[a for a in f['actions'] if a['title']!=action['title']]+[action]
    strategy_sources=[dict(s,claim=T('Текущая карточка правил или регистрации; возрастные и ценовые противоречия сохранены. Это не подтверждение заявки семьи.',
        'Ficha actual de reglas o registro; discrepancias de edad y precio conservadas. No confirma solicitud familiar.')) for s in fresh]
    strategy_sources.append(dict(title=T('Партнёр Costa Rica: текущий каталог','Socio Costa Rica: directorio actual'),url=GLOBAL_FLL,checked=CHECKED,
        claim=T('Подтверждён партнёр Fundación STEAM; текущий локальный набор и язык BIOGLOW не подтверждены.',
                'Socio Fundación STEAM confirmado; convocatoria local actual e idioma BIOGLOW sin confirmar.')))
    f['sources']=list({s['url']:s for s in f['sources']+strategy_sources}.values())
    for child in f['children'].values():
        child['sources']=list({s['url']:s for s in child['sources']+[s for s in strategy_sources if s['url'] in [VALLARTA,GUIDE]]}.values())
    sources={s['url'] for s in d['sources']}
    for e in [idx[i] for i in new_ids+['C052','C082','C083','C084','C085','C086','C087','E211','C003','C043','C1148','C1149','C1150']]:
        for ref in [dict(label=e['title'],url=e['source'])]+e.get('references',[]):
            if ref['url'] not in sources:d['sources'].append(dict(title=ref['label'],url=ref['url'],checked=CHECKED,evidence='official-primary'));sources.add(ref['url'])
