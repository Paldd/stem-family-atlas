"""Edition-specific Asian exhibition dates, visitor fares and child admission."""
from copy import deepcopy

CHECKED='2026-11-05'
SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
WRC='https://kfqgw.beijing.gov.cn/ywdt/gzdt/202608/t20260826_4837862.html'
CIIF='https://www.hmf-china.com/En/Co/?AID=191&CID=21'
GSTAR='https://gstar.or.kr/part/gstar_btc_info.do'
COMPUTEX='https://www.computextaipei.com.tw/en/menu/C73E8F9D0454124DD0636733C6861689/info.html'
TIMTOS='https://www.timtos.com.tw/en/menu/24D4D472FDE8F915D0636733C6861689/info.html'
AUTOMATION='https://automationtaipei.chanchao.com.tw/en/VisitorInfo'
TOUCH='https://www.touchtaiwan.com/visitor.asp'
TAIREX='https://www.chanchao.com.tw/expoDetail.asp?id=TAIREX2027'

def ref(e,url,label):
    e['references']=[r for r in e.get('references',[]) if r['url']!=url]+[dict(url=url,label=label)]

def enrich_v152(d):
    rows={e['id']:e for e in d['events']}
    e=rows['E028']
    e.update(title=T('World Robot Conference 2027 · объявлено открытие; полный период уточняется',
                    'World Robot Conference 2027 · apertura anunciada; periodo completo pendiente'),
        start='2027-08-18',end='2027-08-18',date_scope='activity_start',date_status='Подтверждено',
        period=T('Подтверждено только открытие 18 августа 2027; окончание, дни Expo и семейные дни не объявлены.',
                 'Solo apertura confirmada el 18 de agosto de 2027; cierre, días de Expo y días familiares sin anunciar.'),
        source=WRC,checked=CHECKED,
        proof=T('Правительство Beijing E-Town прямо объявило открытие World Robot Conference 2027 на 18 августа. Полный период в прочитанном анонсе отсутствует.',
                'Gobierno de Beijing E-Town anuncia expresamente apertura de World Robot Conference 2027 el 18 de agosto. El anuncio leído no indica periodo completo.'),
        note=T('Один день в календаре обозначает объявленное начало конференции, а не однодневную выставку или подтверждённый вход семьи. Исторические даты 2026 и public days 22–23 августа не переносятся на 2027.',
               'Un día en calendario señala inicio anunciado de conferencia, no exposición de un día ni entrada familiar confirmada. Fechas históricas de 2026 y public days 22–23 de agosto no se trasladan a 2027.'),
        visitor_policy_note=T('Для 2027 ещё не подтверждены public open days, возраст, детский тариф и документы иностранных посетителей. Открытие конференции не гарантирует доступ на Expo или все стенды.',
                              'Para 2027 faltan public open days, edad, tarifa infantil y documentos de visitantes extranjeros. Apertura de conferencia no garantiza acceso a Expo ni a todos los stands.'),
        entry=T('Отслеживать полную программу 2027 и отдельные visitor tickets Expo. Подтвердить семейный день и паспортную регистрацию до поездки.',
                'Seguir programa completo de 2027 y visitor tickets de Expo separados. Confirmar día familiar y registro con pasaporte antes del viaje.'))
    e['adult_entry']=e['entry']
    ref(e,WRC,T('Правительство Пекина · открытие 18 августа 2027, без даты закрытия',
                'Gobierno de Pekín · apertura el 18 de agosto de 2027, sin fecha de cierre'))

    # A new season keeps its own stable ID; the October 2026 card remains intact.
    ident='E219'
    e=deepcopy(rows['E083'])
    e.update(id=ident,title='CIIF 2027 · Robotics Show / Industrial Automation Show',
        start='2027-09-20',end='2027-09-24',period='',date_scope='exhibition_window',checked=CHECKED,
        source=CIIF,references=[],event_group='CIIF Shanghai 2027',
        cost=T('Посетительский тариф 2027 и детские условия ещё не подтверждены; бесплатную регистрацию 2026 не переносим автоматически.',
               'Tarifa de visitante 2027 y condiciones infantiles aún sin confirmar; registro gratuito de 2026 no se traslada automáticamente.'),
        proof=T('Соорганизатор Hannover Milano Fairs China в отчёте от 16 октября 2026 прямо объявил CIIF 2027 на 20–24 сентября в NECC Shanghai.',
                'Coorganizador Hannover Milano Fairs China en informe del 16 de octubre de 2026 anuncia expresamente CIIF 2027 del 20–24 de septiembre en NECC Shanghai.'),
        note=T('Новый выпуск 2027; карточка CIIF 2026 сохранена отдельно. Robotics Show / IAS — части одной поездки на CIIF, не дополнительные самостоятельные выставки. Доступ детей и регистрация 2027 пока уточняются.',
               'Nueva edición de 2027; ficha CIIF 2026 conservada aparte. Robotics Show / IAS son partes de un viaje a CIIF, no exposiciones independientes adicionales. Acceso infantil y registro 2027 pendientes.'),
        exhibitor_note=T('Отчёт соорганизатора: в 2026 вся CIIF включала 3247 экспонентов из 24 стран / регионов, а не только роботов. Список компаний 2027 ещё не подтверждён.',
                         'Informe del coorganizador: toda CIIF de 2026 tuvo 3247 expositores de 24 países / regiones, no solo robots. Lista de empresas 2027 aún sin confirmar.'))
    ref(e,CIIF,T('Соорганизатор · точные даты CIIF 2027 и итоги 2026',
                 'Coorganizador · fechas exactas de CIIF 2027 y resultados de 2026'))
    if ident in rows:rows[ident].clear();rows[ident].update(e)
    else:d['events'].append(e)

    e=rows['E118']
    e.update(checked=CHECKED,source=GSTAR,visitor_policy='family',
        age=T('BTC: взрослый / youth-билет; дошкольная бесплатная категория. Тариф зависит от рождения и школьного статуса, документы нужны.',
              'BTC: entrada adulta / juvenil; categoría preescolar gratuita. Tarifa depende de nacimiento y escolarización, con documentos.'),
        mat=T('Да: youth-билет 8000 KRW за выбранный день; паспорт / подтверждение даты рождения.',
              'Sí: entrada juvenil de 8000 KRW para día elegido; pasaporte / prueba de nacimiento.'),
        osc=T('Да для BTC; бесплатность дошкольника 2020 года подтвердить по фактическому школьному статусу и документам. Иначе youth 8000 KRW.',
              'Sí para BTC; confirmar gratuidad preescolar para nacido en 2020 según escolarización real y documentos. En otro caso juvenil 8000 KRW.'),
        visitor_policy_note=T('Детские посетители допускаются в BTC. Youth 8000 KRW для родившихся после 1 января 2008; бесплатная категория названа preschool, с границей 2020 года. Оскару не обещаем бесплатность только по году рождения; возраст отдельных игр / зон проверяется отдельно.',
                              'Visitantes infantiles admitidos en BTC. Juvenil 8000 KRW para nacidos después del 1 de enero de 2008; categoría gratuita llamada preschool, con límite de 2020. Sin prometer gratuidad a Oscar solo por año de nacimiento; comprobar edades de juegos / zonas aparte.'),
        cost=T('BTC, один выбранный день: взрослый 18000 KRW; youth 8000 KRW; дошкольная категория бесплатно после проверки. Двое взрослых + Матвей: 44000 KRW, если Оскар принят бесплатно, либо 52000 KRW с его youth-билетом. Поездка отдельно.',
               'BTC, un día elegido: adulto 18000 KRW; juvenil 8000 KRW; categoría preescolar gratuita tras comprobar. Dos adultos + Matvey: 44000 KRW si Oscar entra gratis, o 52000 KRW con su entrada juvenil. Viaje aparte.'),
        entry=T('Платные BTC-билеты продаются только онлайн заранее, на месте продаж нет. На выбранный день купить до 24:00 предыдущего дня; один билет действует один день. Лимит 2 билета на человека в день; для семьи заранее согласовать корректную покупку.',
                'Entradas BTC de pago solo online anticipadas, sin venta presencial. Comprar para día elegido antes de las 24:00 del día previo; una entrada vale un día. Límite de 2 entradas por persona y día; acordar compra familiar correcta con antelación.'),
        deadline='2026-11-21',deadline_utc='2026-11-21T14:59:00Z',
        deadline_label=T('Последняя онлайн-продажа BTC на 22 ноября', 'Última venta online BTC para el 22 de noviembre'),
        deadline_note=T('Общая продажа закрывается 21 ноября 2026 в 23:59 KST. Для посещения 19–21 ноября действует более ранний предел: 24:00 предыдущего дня. Срок 6 ноября 16:00 относится к школьным группам от 30 человек, не к семейному билету.',
                        'Venta general cierra el 21 de noviembre de 2026 a las 23:59 KST. Para visitar el 19–21 de noviembre rige límite anterior: 24:00 del día previo. Plazo del 6 de noviembre a las 16:00 corresponde a grupos escolares de 30 personas o más, no a entrada familiar.'),
        proof=T('Прочитаны действующие правила BTC 2026: цены, бесплатная категория, онлайн-продажа, документы и ограничения. Overview 18–22 ноября включает Game Awards; публичная BTC остаётся 19–22 ноября.',
                'Leídas reglas vigentes de BTC 2026: precios, categoría gratuita, venta online, documentos y límites. Overview del 18–22 de noviembre incluye Game Awards; BTC pública sigue el 19–22 de noviembre.'),
        note=T('Бесплатный билет получают в информационном центре; он открывается за час до выставки. 19 ноября открытие 11:00; проверка билетов до 17:00, вход до 17:30. Нужен документ для youth / free. BTC не включает отдельные BTB, G-CON или специальные esports-пакеты. Билеты не куплены.',
               'Entrada gratuita se recoge en centro de información, abierto una hora antes de exposición. El 19 de noviembre abre a las 11:00; verificación de entradas hasta 17:00, acceso hasta 17:30. Documento necesario para youth / free. BTC no incluye BTB, G-CON ni paquetes esports especiales. Entradas sin comprar.'))
    e['adult_entry']=e['entry']
    ref(e,GSTAR,T('BTC 2026 · цены, дети, онлайн-билеты и документы',
                  'BTC 2026 · precios, niños, entradas online y documentos'))

    for ident,minimum,url in [('E020',12,TAIREX),('E021',12,AUTOMATION),('E022',18,TOUCH),('E201',12,TIMTOS)]:
        e=rows[ident]
        if e.get('checked', '') > CHECKED:
            continue
        e.update(checked=CHECKED,visitor_age_min=minimum)
        e['visitor_policy_note']=T('Действующие правила 2027: вход младше '+str(minimum)+' запрещён. Матвей и Оскар не допускаются; профессиональная регистрация взрослого этого не меняет.',
                                  'Reglas vigentes de 2027: entrada prohibida a menores de '+str(minimum)+'. Matvey y Oscar no admitidos; registro profesional adulto no cambia esta regla.')
        e['proof']=T('Свежая официальная страница конкретного выпуска подтверждает даты и возрастное ограничение; билет экспонента не подменяет visitor registration.',
                     'Página oficial actual de edición concreta confirma fechas y límite de edad; entrada de expositor no sustituye visitor registration.')
        ref(e,url,T('Правила посетителей 2027 и возрастной порог '+str(minimum)+'+',
                    'Reglas de visitantes 2027 y edad mínima de '+str(minimum)+'+'))
    e=rows['E021']
    if e.get('checked', '') <= CHECKED:
        e['cost']=T('Персональный QR после visitor registration; опубликована альтернатива на месте NT$300 при отказе от членской анкеты. Условия бесплатной предварительной регистрации перепроверить в выбранном потоке.',
                    'QR personal tras visitor registration; alternativa presencial publicada de NT$300 si no se desea formulario de miembro. Comprobar condiciones de registro anticipado gratuito para opción elegida.')
        e['adult_entry']=T('Отдельный QR каждому; 4–6 августа 10:00–17:00, 7 августа до 16:00. Вход NT$300 через VIP counter — вариант по опубликованным условиям обработки данных. Дети младше 12 не допускаются.',
                           'QR separado por persona; 4–6 de agosto 10:00–17:00, 7 de agosto hasta 16:00. Entrada NT$300 vía VIP counter es opción según condiciones publicadas sobre datos. Menores de 12 no admitidos.')
    e=rows['E022']
    e['cost']=T('Персональная visitor registration / QR; при сомнениях о передаче данных опубликован однодневный билет на месте NT$300 через VIP service counter. Только 18+.',
                'Visitor registration / QR personal; si existen dudas sobre entrega de datos se publica entrada presencial de un día NT$300 vía VIP service counter. Solo 18+.')
    e['adult_entry']=T('21–22 апреля 10:00–17:00, 23 апреля до 16:00; TaiNEX 1, этаж 4. QR персональный, либо опубликованная однодневная альтернатива NT$300. Младше 18 вход запрещён.',
                       '21–22 de abril 10:00–17:00, 23 de abril hasta 16:00; TaiNEX 1, planta 4. QR personal o alternativa publicada de un día NT$300. Entrada prohibida a menores de 18.')
    e=rows['E201']
    if e.get('checked', '') <= CHECKED:
        e['cost']=T('FAQ 2027: вход бесплатный после online pre-registration, QR обменивают на обязательный visitor badge. Стоимость стенда не входной билет.',
                    'FAQ 2027: entrada gratuita tras online pre-registration, QR se cambia por visitor badge obligatorio. Precio de stand no es entrada de visitante.')
        e['adult_entry']=T('Trade professionals, buyers и enthusiasts; бесплатная предварительная регистрация и badge. 2–6 марта 10:00–18:00. Младше 12 строго запрещено без исключений.',
                           'Trade professionals, buyers y enthusiasts; registro anticipado gratuito y badge. 2–6 de marzo 10:00–18:00. Menores de 12 estrictamente prohibidos sin excepciones.')
        e['note']=T('Текущий FAQ перечисляет TaiNEX 1 и 2; ранее проверенный application kit также называл TWTC Hall 1. Это расхождение площадок требует актуальной карты перед поездкой. 7–9 марта — демонтаж по kit, не дополнительные дни посещения.',
                    'FAQ actual enumera TaiNEX 1 y 2; application kit verificado antes también nombraba TWTC Hall 1. Discrepancia de recintos requiere plano actual antes del viaje. 7–9 de marzo son desmontaje según kit, no días de visita adicionales.')
        e['city']=T('Taipei · TaiNEX 1/2 по FAQ; TWTC Hall 1 в kit — проверить карту',
                    'Taipei · TaiNEX 1/2 según FAQ; TWTC Hall 1 en kit — comprobar plano')

    e=rows['E023']
    if e.get('checked', '') <= CHECKED:
        e.update(checked=CHECKED,visitor_policy='adults_only',visitor_age_min=18,
            age=T('18+ по действующим общим Admission Guidelines; отдельную редакцию 2027 перепроверить.',
                  '18+ según Admission Guidelines generales vigentes; comprobar edición específica de 2027.'),
            mat='Нет',osc='Нет',priority='P4 — '+T('по действующему правилу только взрослые','solo adultos según regla vigente'),
            proof=T('Общие Admission Guidelines, изменённые 3 февраля 2026 и действующие на сайте, запрещают вход младше 18 во время выставки. Это отдельная страница правил, а не только исторический Visitor Information 2026.',
                    'Admission Guidelines generales modificadas el 3 de febrero de 2026 y vigentes en web prohíben entrada a menores de 18 durante exposición. Página de reglas distinta del Visitor Information histórico de 2026.'),
            visitor_policy_note=T('Текущие общие правила организатора запрещают младше 18; детям 6/9 поездка не подходит. Год отдельной редакции 2027 в Guidelines не указан: перед поездкой взрослых проверить обновления. Не переносить публичный день и цены 2026 на 2027.',
                                  'Reglas generales actuales del organizador prohíben menores de 18; viaje no adecuado para niños de 6/9. Guidelines no indica edición específica de 2027: comprobar cambios antes del viaje adulto. No trasladar día público ni precios de 2026 a 2027.'),
            entry=T('Маршрут родителей по действующим правилам 18+. Visitor registration, цены и дни доступа именно 2027 ещё подтвердить.',
                    'Ruta de padres según reglas vigentes de 18+. Confirmar visitor registration, precios y días de acceso específicos de 2027.'),
            note=T('Даты 1–4 июня 2027 подтверждены ранее; общие правила входа 18+ проверены отдельно сейчас. Билет взрослого не разрешает вход ребёнка.',
                   'Fechas 1–4 de junio de 2027 confirmadas antes; reglas generales de entrada 18+ verificadas aparte ahora. Entrada adulta no permite acceso infantil.'))
        e['adult_entry']=e['entry']
        ref(e,COMPUTEX,T('Действующие общие Admission Guidelines · запрет до 18',
                         'Admission Guidelines generales vigentes · prohibición para menores de 18'))
    sources={s['url']:s for s in d['sources']}
    for ident in ['E028','E219','E118','E020','E021','E022','E023','E201']:
        record=next(e for e in d['events'] if e['id']==ident)
        for source in record['references']:
            if source['url'] not in {WRC,CIIF,GSTAR,COMPUTEX,TIMTOS,AUTOMATION,TOUCH,TAIREX}:continue
            item=dict(url=source['url'],title=source['label'],checked=CHECKED,
                      evidence=T('Первичный источник; границы сезона и семейного допуска сохранены.',
                                 'Fuente primaria; se conservan límites de temporada y admisión familiar.'))
            if item['url'] in sources:sources[item['url']].update(item)
            else:d['sources'].append(item);sources[item['url']]=item
