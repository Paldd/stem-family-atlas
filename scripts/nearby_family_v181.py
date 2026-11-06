"""Verified shared FOD timetables and family astronomy options in Costa Rica."""
from datetime import date,timedelta
from nepal_maldives_v180 import P,src

CHECKED='2026-11-06'
SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
FOD='https://survey.zohopublic.com/zs/SjzWbS'
ASTRO='https://www.giorodriguez.com/producto/campamento-de-observacion-de-estrellas/'
ASTRO_DATES=['2026-12-12','2026-12-19','2027-01-02','2027-01-16','2027-02-06','2027-02-20','2027-02-27','2027-03-06','2027-03-20','2027-04-03','2027-04-17','2027-05-01']
GATE=T('Это вариант планирования, не принятая заявка. Подтвердить возраст, уровень, язык, места и итоговый счёт. Формы, аккаунты, сообщения, согласия и оплаты не выполнялись.', 'Opción de planificación, no solicitud aceptada. Confirmar edad, nivel, idioma, plazas y factura final. Sin formularios, cuentas, mensajes, consentimientos ni pagos.')
TRIP=T('Дорога, расходы родителей, страховка, питание вне включений и неизвестные доплаты отдельно; пустое поле не означает ноль.', 'Transporte, gastos parentales, seguro, comidas fuera de inclusiones y suplementos desconocidos aparte; campo vacío no equivale a cero.')
ASTRO_LANG=T('Официальное описание на испанском. Язык устной экскурсии и поддержка EN / ES отдельно не установлены; язык страницы не доказывает язык занятий.', 'Descripción oficial en español. Idioma de visita oral y apoyo EN / ES sin establecer por separado; idioma de página no acredita idioma de actividad.')
ASTRO_TERMS=T('Аванс CRC 10000 на платного участника входит в цену. Остаток за три дня; при авансе картой сайт объявляет автоматическое списание остатка с той же карты. При дожде / облаках сайт исключает перенос и возврат; при порывах выше 80 km/h купол не надувают. Согласия и платёж не оформлялись.', 'Anticipo CRC 10000 por participante de pago incluido en precio. Saldo tres días antes; con anticipo por tarjeta web anuncia cargo automático del saldo a misma tarjeta. Con lluvia / nubes web excluye cambio y reembolso; con ráfagas superiores a 80 km/h no inflan cúpula. Sin consentimientos ni pago.')

def age_fit(child,lo,hi,start):
    born={'matvey':2017,'oscar':2020}[child]
    # The family already reported ages 9 and 6 in 2026. December cannot still
    # contain the younger 8/5 possibilities implied by birth years alone.
    known_age={'matvey':9,'oscar':6}[child]
    earliest=date(born,1,1);latest=date(born,11,6);day=date.fromisoformat(start)
    ages=[day.year-b.year-((day.month,day.day)<(b.month,b.day))for b in [earliest,latest]]
    low,high=min(ages),max(ages)
    if start>=CHECKED and day.year==2026:low=high=known_age
    status='later'if high<lo else'not_eligible'if low>hi else'conditional'
    detail=T(f'Для этой даты возраст {low}–{high}; курс {lo}–{hi}. Сейчас семье известны 9 и 6 лет; точный день рождения не установлен. Язык, уровень и место ещё подтвердить.', f'Para esta fecha edad {low}–{high}; curso {lo}–{hi}. Familia conoce ahora edades 9 y 6; cumpleaños exacto sin establecer. Confirmar idioma, nivel y plaza.')
    return dict(status=status,detail=detail)

def refresh_profiles(raw):
    for p in raw['profiles']:
        if p['id']in {f'CP{i}'for i in range(1124,1136)}:
            import re
            lo,hi=map(int,re.match(r'(\d+)–(\d+)',p['age']).groups())
            for v in p['timing']['session_details']:v['family_fit']={k:age_fit(k,lo,hi,v['start'])for k in ['matvey','oscar']}
            for child in ['matvey','oscar']:
                states={v['family_fit'][child]['status']for v in p['timing']['session_details']}
                state='conditional'if'conditional'in states else'later'if states=={'later'}else'not_eligible'
                p['family_fit'][child]=dict(status=state,detail=T('Возраст проверен по каждой смене с учётом известных текущих 9 и 6 лет. Разные возрастные группы могут совпадать по месту и часам; запуск и оба места отдельно.', 'Edad revisada por turno con edades actuales conocidas de 9 y 6. Grupos de edades distintas pueden coincidir en sede y horario; apertura y ambas plazas aparte.'))
            p['pairing']=dict(venue_id='fod-central-francisco-peralta',verified_source=FOD,checked=CHECKED,fee=dict(amount=60000,currency='CRC',unit='per_child_course',tax_included=True))
            p['checked']=CHECKED
            for s in p['sources']:
                if s['url']==FOD:s['checked']=CHECKED
        elif p['id']=='CP613':
            p['checked']=CHECKED
            for s in p['sources']:
                if s['url']=='https://www.campcoyote.mx/':s['checked']=CHECKED
            for v in p['timing']['session_details']:
                if v['variant_key']=='autumn':v['availability']=dict(status='closed',label=T('Осень 2026 завершена; новый выпуск ещё не датирован.', 'Otoño 2026 terminado; edición nueva aún sin fecha.'),checked=CHECKED)
                if v['variant_key']=='winter':v['family_fit']={k:age_fit(k,6,14,v['start'])for k in ['matvey','oscar']}
            p['family_fit']={k:age_fit(k,6,14,'2026-12-21')for k in ['matvey','oscar']}

def make_profiles():
    rows=[]
    for i,key,name,overnight in [(1436,'overnight','Gio Rodríguez · Astrocamp familiar',True),(1437,'evening','Gio Rodríguez · Búho nocturno',False)]:
        p=P(i,'gio-grecia-astronomy-'+key,name,'NPL','families · 4–11 child rate; under 4 free',['science','space','adventure'],0,99,('family',))
        p.update(iso='CRI',country=T('Коста-Рика','Costa Rica'),place='Ventisqueros · Santa Gertrudis Sur · Grecia',language=ASTRO_LANG,programme=T('Семейная астрономия: телескопы со специалистами, планетарий, ужин и костёр. Это научный досуг с родителями; отдельного детского пансиона, робототехнического курса или конкурсной медали нет.', 'Astronomía familiar: telescopios con especialistas, planetario, cena y fogata. Ocio científico con padres; sin residencia infantil independiente, curso robótico ni medalla competitiva.'),accommodation=T('Семейная ночёвка в палатке организатора; прибытие в субботу 17:00, завершение в воскресенье 08:00. Завтрак включён.', 'Noche familiar en tienda del organizador; llegada sábado 17:00, final domingo 08:00. Desayuno incluido.')if overnight else T('Вечер без ночёвки; прибытие 17:00, планетарий 19:30. Точное окончание варианта без палатки отдельно не установлено.', 'Tarde sin pernocta; llegada 17:00, planetario 19:30. Final exacto de opción sin tienda sin establecer por separado.'),sources=[src('Gio Rodríguez · current programme and prices',ASTRO)],questions=[GATE],checked=CHECKED)
        adult,child=(27000,22000)if overnight else(17000,12000)
        p['family_fit']={k:dict(status='conditional',detail=T('Оба ребёнка входят в детский тариф 4–11 лет; участвуют со взрослыми. Рабочий язык, место и семейное размещение подтвердить.', 'Ambos niños dentro de tarifa infantil de 4–11 años; participan con adultos. Confirmar idioma de trabajo, plaza y alojamiento familiar.'))for k in ['matvey','oscar']}
        price=T(f'CRC {adult} за взрослого / {child} за ребёнка до 12 лет, плюс IVA. Пример: 2 взрослых + 2 ребёнка — CRC {2*adult+2*child} до IVA и выбранных доплат.', f'CRC {adult} por adulto / {child} por menor de 12, más IVA. Ejemplo: 2 adultos + 2 niños — CRC {2*adult+2*child} antes de IVA y suplementos elegidos.')
        p['price'].update(year=None,currency='CRC',amount=None,unit='participant',label=price,included=T('Телескопы, планетарий, ужин и костёр; для ночёвки палатка и завтрак. Конкретное размещение семьи и меню подтвердить.', 'Telescopios, planetario, cena y fogata; para pernocta tienda y desayuno. Confirmar alojamiento concreto de familia y menú.'),extras=T('IVA добавляется при оплате. Спальник CRC 3000 за штуку; специальное вегетарианское / безглютеновое меню CRC 10000 за человека. Дорога и страховка отдельно.', 'IVA se añade al pagar. Saco CRC 3000 por unidad; menú vegetariano / sin gluten especial CRC 10000 por persona. Transporte y seguro aparte.'),deposit=ASTRO_TERMS)
        p['timing'].update(status='published_2026_27',label=T('12 отдельных суббот с 12 декабря 2026 по 1 мая 2027; выбирается одна дата, а не непрерывная смена.', '12 sábados separados del 12 de diciembre de 2026 al 1 de mayo de 2027; se elige fecha, no turno continuo.'),sessions=[],session_details=[])
        for start in ASTRO_DATES:
            end=(date.fromisoformat(start)+timedelta(days=1)).isoformat()if overnight else start
            p['timing']['sessions'].append([start,end]);p['timing']['session_details'].append(dict(start=start,end=end,variant_key=key+'-'+start.replace('-',''),label=T('Семейная ночёвка','Noche familiar')if overnight else T('Вечер без ночёвки','Tarde sin pernocta'),price=price,source=ASTRO,date_scope='camp_session'if overnight else'workshop_window',accommodation=p['accommodation'],family_fit=p['family_fit'],entry=GATE))
        rows.append(p)
    return rows

def budget_offers(d):
    profiles={p['id']:p for p in d['camp_programmes']['profiles']};rows=[]
    for start,mat,osc in [('2026-12-07','CP1127','CP1124'),('2027-01-11','CP1127','CP1124'),('2027-01-18','CP1128','CP1125')]:
        end=(date.fromisoformat(start)+timedelta(days=4)).isoformat();mp,op=profiles[mat],profiles[osc]
        rows.append(dict(id='fod-family-parallel-'+start,slug=op['slug'],label=T('FOD · разные группы двух детей · '+start, 'FOD · grupos distintos de ambos niños · '+start),currency='CRC',price_year=2027 if start.startswith('2027')else 2026,children=['matvey','oscar'],base_by_child=dict(matvey=60000,oscar=60000),discount_second=0,required=[],unknown_required=[dict(id='materials',label=T('Устройство / материалы и обязательные доплаты по итоговому счёту','Dispositivo / materiales y suplementos obligatorios según factura final'),rate=1,min=0,unit='invoice')],optional=[],sources=[FOD],sessions=[[start,end]],gate=T('Матвей 9–12; Оскар 6–8. Разные курсы в одной подтверждённой sede, оба 08:00–12:00, пять дней. Два места, рабочий язык и нужный уровень подтвердить отдельно.', 'Matvey 9–12; Oscar 6–8. Cursos diferentes en una sede confirmada, ambos 08:00–12:00, cinco días. Confirmar ambas plazas, idioma de trabajo y nivel.'),deposit_note=mp['price']['deposit'],included=T('Два курса по CRC 60000 с IVAI: опубликованная часть CRC 120000. Это два параллельных полудня, не полный день присмотра.', 'Dos cursos de CRC 60000 con IVAI: parte publicada CRC 120000. Dos medias jornadas paralelas, no día completo de cuidado.'),unknown_trip=['travel','lodging','misc'],scope=GATE+' '+TRIP,checked=CHECKED,format='day',programme_ids=[mat,osc]))
    for i,adult,child in [(1436,27000,22000),(1437,17000,12000)]:
        p=profiles['CP'+str(i)];rows.append(dict(id=p['slug']+'-two-parents',slug=p['slug'],label=p['provider']+T(' · 2 взрослых и 2 ребёнка',' · 2 adultos y 2 niños'),currency='CRC',price_year=None,children=['matvey','oscar'],base_by_child=dict(matvey=child,oscar=child),discount_second=0,required=[dict(id='parents',label=T('Два сопровождающих взрослых','Dos adultos acompañantes'),amount=2*adult)],unknown_required=[dict(id='iva',label=T('IVA всей семьи по итоговому счёту','IVA de toda la familia según factura final'),rate=1,min=0,unit='invoice')],optional=[dict(id='sleeping-bags',label=T('Четыре спальника напрокат · при ночёвке','Cuatro sacos alquilados · con pernocta'),amount=12000)]if i==1436 else[],sources=[ASTRO],sessions=p['timing']['sessions'],gate=T('Сценарий именно для двух взрослых и детей 9 / 6 лет. Детская цена 4–11; неизвестный язык, места и окончательный налог требуют подтверждения.', 'Escenario para dos adultos y niños de 9 / 6 años. Precio infantil 4–11; confirmar idioma desconocido, plazas e impuesto final.'),deposit_note=ASTRO_TERMS,included=p['price']['included'],unknown_trip=['travel','lodging','misc'],scope=GATE+' '+TRIP,checked=CHECKED,format='family'))
    return rows

def enrich_v181(d):
    for p in d['camp_programmes']['profiles']:
        if p.get('pairing'):p['pairing']['checked']=CHECKED
    ids={'E041','E211'}
    for e in d['events']:
        if e.get('camp_programme_id')in {'CP1436','CP1437'}:e.update(participation='family_visit',admission_kind='family')
        if e['id']in ids:
            e.update(checked=CHECKED,visitor_policy='confirm_children',visitor_policy_note=T('Родители / сопровождающие приглашены, но объявление Primary расходится с MS / 13+ challenge. Посетительский допуск детей 6 / 9 и детский тариф отдельно не подтверждены.', 'Padres / acompañantes invitados, pero anuncio Primary discrepa con challenge MS / 13+. Admisión de visitantes de 6 / 9 y tarifa infantil sin confirmar por separado.'),registration_status=T('Список событий пишет открытую регистрацию; текст одной страницы содержит закрытие 31 октября и интервал 16 октября–15 ноября 2026. На 6 ноября новый допуск семьи не подтверждён.', 'Lista de eventos indica inscripción abierta; texto de una página contiene cierre del 31 de octubre e intervalo del 16 de octubre al 15 de noviembre de 2026. Al 6 de noviembre admisión familiar nueva sin confirmar.'),cost=T('Страница пакета: USD 580 за человека / coach; общий список: USD 650 без ясной единицы. Отель / питание относятся к Ruta, не автоматически к Robotics Open. Цена младших гостей и полный семейный счёт неизвестны.', 'Página del paquete: USD 580 por persona / coach; lista general: USD 650 sin unidad clara. Hotel / comidas corresponden a Ruta, sin aplicarlos automáticamente a Robotics Open. Precio de visitantes menores y factura familiar completa desconocidos.'))
    offers=budget_offers(d);new={o['id']for o in offers};d['camp_planning']['offers']=[o for o in d['camp_planning']['offers']if o['id']not in new]+offers
    if not any(s['url']==ASTRO for s in d['sources']):d['sources'].append(dict(title='Gio Rodríguez · astronomy programme 2026–2027',url=ASTRO,checked=CHECKED,evidence=T('Свежая страница перечисляет 12 отдельных дат, два семейных формата и возрастные тарифы.', 'Página actual enumera 12 fechas separadas, dos formatos familiares y tarifas por edad.')))
    d['nearby_family_v181']=dict(version=181,checked=CHECKED,new_camp_dossiers=2,new_generated_learning_rows=24,refreshed_FOD_dossiers=12,new_budget_offers=5,paired_sessions_require_verified_venue_and_equal_timetable=True,worldwide_complete=False,fully_audited_countries=0)
