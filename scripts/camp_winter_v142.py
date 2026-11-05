"""Published winter cohorts, checked against individual public booking pages."""
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
from calendar_time import local_to_utc

CHECKED = '2026-11-04'
SPANISH = {}


def T(ru, es):
    SPANISH[ru] = es
    return ru


FAQ = 'https://codecampworld.ch/faq'
WINTER = 'https://codecampworld.ch/unsere-camps-winter-ferien'
SMART = 'https://smartkids-school.ch/en/stages'
LANGUAGE = T('По текущему FAQ Code Camp занятия обычно на немецком; язык зависит от смены и места. EN/ES/RU группа для этих дат не подтверждена. Английский интерфейс не доказывает язык преподавателя.',
             'Según FAQ actual de Code Camp, clases normalmente en alemán; idioma según sesión y sede. Grupo EN/ES/RU para estas fechas sin confirmar. Interfaz inglesa no acredita idioma docente.')
HOURS = T('День 10:00–16:00; приём с 09:30, забрать до 16:30. По общему FAQ около 2 часов из 6 занимают перерывы и движение; это не 6 часов программирования.',
          'Día 10:00–16:00; recepción desde 09:30, recogida hasta 16:30. Según FAQ general, unas 2 horas de 6 son pausas y movimiento; no son 6 horas de programación.')
INCLUDED = T('Программа и надзор, включая обеденный перерыв; футболка и кепка по карточкам. По FAQ до 8 детей на преподавателя. Участническая медаль не международная победа.',
             'Programa y supervisión, incluida pausa del almuerzo; camiseta y gorra según fichas. FAQ: hasta 8 niños por docente. Medalla de participación distinta de victoria internacional.')
EXTRAS = T('Обед, перекус и вода свои. Жильё, дорога и страхование отдельно. FAQ: скидка второму ребёнку 10%, третьему 20%, нужен индивидуальный код до записи; не применена автоматически. Поздняя замена устройства менее чем за 72 часа или при поломке в первый день — 50 CHF, это не обычная аренда.',
           'Traer almuerzo, tentempié y agua. Alojamiento, transporte y seguro aparte. FAQ: descuento del 10% al segundo hijo y 20% al tercero, con código individual previo; sin aplicar automáticamente. Sustitución tardía del dispositivo con menos de 72 horas o fallo el primer día: 50 CHF, distinta del alquiler normal.')
CANCEL = T('FAQ: перенос или voucher согласуются; после первого дня возможен частичный возврат по письменному обращению, при продолжении позднего возврата нет. При отмене оператором возможны другой лагерь, voucher или возврат. Размер удержаний и применимые местные условия подтвердить до оплаты.',
           'FAQ: cambio o voucher por acuerdo; posible reembolso parcial tras primer día mediante petición escrita, sin devolución posterior si continúa. Cancelación del operador: posible otro campamento, voucher o reembolso. Confirmar retenciones y condiciones locales antes de pagar.')
QUESTIONS = [T('Получить письменное подтверждение EN/ES группы, свободного места, иностранного приёма, точной возрастной отсечки и уровня; иначе семье выбирать другой лагерь.',
               'Obtener confirmación escrita de grupo EN/ES, plaza, admisión extranjera, corte exacto de edad y nivel; en caso contrario elegir otro campamento.'),
             T('Сверить устройство и лицензии выбранного трека, аренду, скидку, итоговый счёт, страхование и условия отмены. Опубликованная форма не подтверждает зачисление.',
               'Comprobar dispositivo y licencias del itinerario, alquiler, descuento, factura total, seguro y cancelación. Formulario público no acredita aceptación.')]
AI_GATE = T('Карточки AI Camp: 9–13, но FAQ требует Microsoft-аккаунт 13+ для Bing AI. Законный сценарий для ребёнка младше 13 не установлен; не менять возраст аккаунта, сначала согласовать подходящие инструменты и правила сервиса.',
            'Fichas AI Camp: 9–13, pero FAQ exige cuenta Microsoft 13+ para Bing AI. Sin acreditar uso permitido para menores de 13; no falsear edad de cuenta, acordar herramientas y reglas del servicio.')
MASTERS_GATE = T('Выбранные зимние карточки Masters дают 7–12, общее меню — 8–13. Для младшего требуется отдельное подтверждение; пройти Engineers или согласовать эквивалентный опыт.',
                 'Fichas invernales Masters seleccionadas indican 7–12, menú general 8–13. Confirmación específica para el menor; completar Engineers o acreditar experiencia equivalente.')


def family_fit(lo, hi, start, masters=False, ai=False):
    out = {}
    for child, year in [('matvey', 2017), ('oscar', 2020)]:
        ages = (date.fromisoformat(start).year-year-1, date.fromisoformat(start).year-year)
        status = 'later' if ages[1] < lo else 'not_eligible' if ages[0] > hi else 'conditional'
        detail = T(f'Возраст в год смены {ages[0]}–{ages[1]}; карточка {lo}–{hi}. Точный день рождения, возраст на старте, уровень, EN/ES группа и зачисление проверяются отдельно.',
                   f'Edad en año de sesión {ages[0]}–{ages[1]}; ficha {lo}–{hi}. Fecha exacta de nacimiento, edad al inicio, nivel, grupo EN/ES y admisión se comprueban aparte.')
        if masters: detail += ' '+MASTERS_GATE
        if ai: detail += ' '+AI_GATE
        out[child] = dict(status=status, detail=detail)
    return out


def codecamp_profiles(existing, facts):
    """Update stable dossiers; a different country needs its own dossier."""
    profiles = deepcopy(existing)
    by_slug = {p['slug']:p for p in profiles}
    mapping = {'Spark':'spark', 'Ignite':'ignite', 'Web Builders':'web',
               'Minecraft Engineers':'engineers', 'Minecraft Masters':'masters',
               'Minecraft Experts':'experts', 'AI Camp':'ai'}
    for ident, kind in [(1136, 'ignite'), (1137, 'engineers')]:
        slug = 'codecamp-vaduz-'+kind
        if slug not in by_slug:
            p = deepcopy(by_slug['codecamp-'+kind])
            p.update(id=f'CP{ident}', slug=slug, country='Лихтенштейн', iso='LIE',
                     provider='Code Camp Liechtenstein · '+('Ignite' if kind=='ignite' else 'Minecraft Engineers'))
            profiles.append(p); by_slug[slug]=p
    groups = {}
    for row in facts:
        name = row['name'].rsplit(' (', 1)[0]
        kind = mapping[name]
        slug = ('codecamp-vaduz-' if row['iso']=='LIE' else 'codecamp-')+kind
        groups.setdefault(slug, []).append(row)
    for slug, rows in groups.items():
        p=by_slug[slug]; kind=slug.rsplit('-',1)[-1]
        archive = [deepcopy(v) for v in p.get('timing',{}).get('session_details',[]) if v['end'] < CHECKED]
        # Published AI IDs already used city keys; never rename them.
        ai_keys = {'2418':'aarau','2379':'basel','2385':'wettingen','2393':'steinhausen'}
        details=[]
        for r in sorted(rows, key=lambda x:(x['start'],x['id'])):
            amount=int(r['course_fee']); rent=int(r['laptop_rental']); days=r['days']
            price=T(f'{amount} CHF за {days} дня; своё подходящее устройство или аренда {rent} CHF. Курс с выбранной арендой = {amount+rent} CHF, расчёт без скидок и поездки.',
                    f'{amount} CHF por {days} días; dispositivo propio compatible o alquiler {rent} CHF. Curso con alquiler elegido = {amount+rent} CHF, cálculo sin descuentos ni viaje.')
            label=r['name']+' · '+r['venue']
            place=r['venue']+' · '+r['address']
            age=T(f"{r['booking_age_min']}–{r['booking_age_max']} лет по карточке выбранной смены",
                  f"{r['booking_age_min']}–{r['booking_age_max']} años según ficha de sesión elegida")
            fit=family_fit(r['booking_age_min'],r['booking_age_max'],r['start'],kind=='masters',kind=='ai')
            proof=T('Прочитаны официальный зимний список с годом 2027 и индивидуальная карточка с датами, адресом, возрастом, часами, ценой и арендой. Форму семьи не продолжали и не отправляли; место и EN группа не подтверждены.',
                    'Leídos listado invernal oficial con año 2027 y ficha individual con fechas, dirección, edad, horario, precio y alquiler. Sin avanzar ni enviar formulario familiar; plaza y grupo EN sin confirmar.')
            detail=dict(start=r['start'],end=r['end'],variant_key=ai_keys.get(r['id'],'booking-'+r['id']),
                label=label,place=place,source=r['url'],price=price,age=age,family_fit=fit,
                date_scope='session_days',course_fee_chf=amount,device_rental_chf=rent,
                device_included=False,days=days,booking_id=r['id'],proof=proof,
                sessions=[dict(date=(date.fromisoformat(r['start'])+timedelta(days=n)).isoformat(),start_time='10:00',end_time='16:00',timezone=r['timezone'],
                    topic=label,ical_timed=True,time_note=HOURS) for n in range(days)])
            if kind=='masters': detail['age']+='; '+MASTERS_GATE
            details.append(detail)
        all_details=archive+details
        lo=min(r['booking_age_min'] for r in rows); hi=max(r['booking_age_max'] for r in rows)
        p.update(checked=CHECKED,language=LANGUAGE,confirmed_instruction_languages=[],
            place=T('Вадуц · Universität Liechtenstein; точный адрес в каждой смене.' if p['iso']=='LIE' else 'Швейцария · точные кампусы и адреса в каждой смене.',
                    'Vaduz · Universität Liechtenstein; dirección exacta por sesión.' if p['iso']=='LIE' else 'Suiza · sedes y direcciones exactas por sesión.'),
            age=T(f'{lo}–{hi} лет по зимним карточкам 2027',f'{lo}–{hi} años según fichas invernales 2027'),
            timing=dict(status='published_2026_27' if archive else 'published_2027',variant_keyed=True,precision='published_sessions',
                label=T(f'Опубликовано зимних смен 2027: {len(details)}; даты, часы и адреса ниже. Архивных смен: {len(archive)}. Язык и свободное место подтвердить.',
                        f'Sesiones invernales 2027 publicadas: {len(details)}; fechas, horarios y direcciones abajo. Sesiones archivadas: {len(archive)}. Confirmar idioma y plaza.'),
                sessions=[[v['start'],v['end']] for v in all_details],session_details=all_details),
            price=dict(year=2027,currency='CHF',unit='course',
                label=T('Точные тарифы зимних карточек: 242 CHF за 2 дня или 363 CHF за 3 дня; аренда соответственно 24 CHF или 36 CHF. У конкретного курса использовать его строку, не общий ориентир FAQ.',
                        'Tarifas exactas de fichas invernales: 242 CHF por 2 días o 363 CHF por 3 días; alquiler respectivo 24 CHF o 36 CHF. Usar fila del curso concreto, no aproximación general del FAQ.'),
                included=INCLUDED,extras=EXTRAS,deposit=CANCEL),
            accommodation=T('Дневной лагерь без ночёвки.','Campamento diurno sin pernoctación.'),
            questions=QUESTIONS+([AI_GATE] if kind=='ai' else [MASTERS_GATE] if kind=='masters' else []),
            editorial_reason=T('Подтверждены конкретные зимние цены и даты, но предпочтительный язык семьи ещё не доказан; условный вариант, не рекомендация бронировать поездку.',
                               'Precios y fechas invernales concretos acreditados; idioma familiar preferido sin probar. Opción condicional, sin recomendar reservar viaje.'))
        if HOURS not in p['programme']: p['programme'] += ' '+HOURS
        if kind=='masters':p['age']+='; '+MASTERS_GATE
        if kind=='ai':p['age']+='; '+AI_GATE
        p['family_fit']=deepcopy(details[0]['family_fit'])
        urls={s['url'] for s in p['sources']}
        for title,url in [(T('Зимний каталог и год сезона','Catálogo invernal y año de temporada'),WINTER),
                          (T('Текущий FAQ: язык, питание, техника и скидки','FAQ actual: idioma, comida, dispositivos y descuentos'),FAQ)]+[(T('Индивидуальная зимняя карточка','Ficha invernal individual'),r['url']) for r in rows]:
            if url not in urls:p['sources'].append(dict(title=title,url=url,checked=CHECKED));urls.add(url)
    return profiles


def smartkids_profile():
    language=T('Есть EN версия сайта, но EN/ES/RU преподавание выбранной группы не заявлено прямо. Уточнить язык учителя; перевод страницы не подтверждает английский лагерь.',
               'Existe web EN, pero docencia EN/ES/RU del grupo elegido no consta expresamente. Confirmar idioma del profesor; traducción web no acredita campamento inglés.')
    hours=T('4 полудня по 3 часа: выбрать 09:00–12:00 либо 14:00–17:00. Часовой пояс организатор не указал; UTC и время Коста-Рики не рассчитаны. Перерывы включены.',
            '4 medias jornadas de 3 horas: elegir 09:00–12:00 o 14:00–17:00. Organizador no indica zona horaria; sin calcular UTC ni hora de Costa Rica. Pausas incluidas.')
    programme=T('Онлайн, максимум 5 детей в группе. Темы зависят от периода: Scratch, Python Turtle, Python, Advanced Python с 12 лет. Не установлено, какая тема доступна в каждой рождественской неделе; это не 4 подтверждённых трека на каждую дату. Проект и сертификат оператора; подготовка к олимпиадам не означает участие или победу. Утверждение о выпускниках EPFL/ETH принадлежит оператору, это не программа этих университетов.',
                'En línea, máximo 5 niños por grupo. Temas según período: Scratch, Python Turtle, Python, Advanced Python desde 12 años. Sin acreditar tema de cada semana navideña; no son 4 itinerarios confirmados en cada fecha. Proyecto y certificado del operador; preparación olímpica no acredita participación ni victoria. Afirmación sobre graduados EPFL/ETH atribuida al operador, sin ser programa de esas universidades.')
    price=T('449 CHF за одну неделю из 4 полудней. Опубликована ранняя цена 404 CHF при записи до 07.12.2026; использовать опубликованную сумму. Скидка второму ребёнку расходится: баннер 99 CHF, FAQ 11%; семейный итог не рассчитан.',
            '449 CHF por semana de 4 medias jornadas. Precio anticipado publicado de 404 CHF al inscribirse antes de 07.12.2026; se usa importe publicado. Descuento segundo hijo discrepante: banner 99 CHF, FAQ 11%; sin calcular total familiar.')
    extras=T('Нужны компьютер PC/Mac/Chromebook, интернет и гарнитура, желательно webcam. По общей странице 7–9-летним рекомендуют взрослого рядом. Физическая техника или набор домой не обещаны; время подключения подтвердить.',
             'Se necesitan PC/Mac/Chromebook, internet y auriculares, preferible webcam. Web general recomienda adulto cerca para edades 7–9. Sin promesa de equipo físico o kit para casa; confirmar hora de conexión.')
    cancel=T('Бесплатная отмена до 14 дней перед лагерем; позднее возможны сборы, полная шкала не установлена. Баннер приёма до 27.12.2026 не даёт отдельного срока январской недели. Оплата на странице описана как резервирование, затем подтверждение расписания в течение 24 рабочих часов; семья не записана и не оплачивала.',
             'Cancelación gratuita hasta 14 días antes; después posibles cargos, sin escala completa. Banner de admisión hasta 27.12.2026 no fija plazo separado de semana de enero. Web describe reserva al pagar y confirmación de horario en 24 horas laborables; familia sin inscripción ni pago.')
    questions=[T('Подтвердить EN/ES учителя, часовой пояс, конкретную тему недели, возрастную отсечку и подходящий уровень; Advanced Python с 12 лет обоим пока рано.',
                 'Confirmar profesor EN/ES, zona horaria, tema concreto de semana, corte de edad y nivel; Advanced Python desde 12 años aún no corresponde a ambos.'),
               T('Получить единый расчёт ранней и семейной скидки, срок оплаты каждой недели и полные условия отмены; январский допуск Оскара зависит от точной даты рождения.',
                 'Obtener cálculo único de descuentos anticipado y familiar, plazo de pago por semana y cancelación completa; admisión de Oscar en enero depende de fecha exacta de nacimiento.')]
    details=[]
    for start,end in [('2026-12-28','2026-12-31'),('2027-01-04','2027-01-07')]:
        fit={}
        fit['matvey']=dict(status='conditional',detail=T('Основной минимум 7 лет подходит; конкретный уровень и EN/ES группа требуют подтверждения. Advanced Python 12+ пока позже.',
                                                       'Cumple mínimo general de 7 años; confirmar nivel concreto y grupo EN/ES. Advanced Python 12+ queda para más adelante.'))
        fit['oscar']=dict(status='later' if start.startswith('2026') else 'conditional',detail=T('В декабре 2026 Оскару ещё 6, минимум 7 не выполнен.' if start.startswith('2026') else 'На 04.01.2027 минимум 7 возможен только при дне рождения 1–4 января; точная дата неизвестна. Язык и допуск отдельно.',
                                                                                          'En diciembre de 2026 Oscar aún tiene 6, no cumple mínimo de 7.' if start.startswith('2026') else 'El 04.01.2027 solo cumple mínimo de 7 si nació del 1 al 4 de enero; fecha exacta desconocida. Confirmar idioma y admisión.'))
        details.append(dict(start=start,end=end,label=T('4 полудня · утро или день на выбор','4 medias jornadas · mañana o tarde a elegir'),source=SMART,
            price=price,programme=programme+' '+hours,family_fit=fit,date_scope='camp_session',
            time_options=[dict(start_time='09:00',end_time='12:00'),dict(start_time='14:00',end_time='17:00')],timezone=None,
            proof=T('Две недели и тариф прочитаны на собственной странице. Варианты тем и времени не размножены в отдельные якобы подтверждённые группы; часовой пояс не назначен.',
                    'Dos semanas y tarifa leídas en web propia. Temas y horarios no multiplicados en grupos supuestamente confirmados; zona horaria sin asignar.')))
    return dict(id='CP1138',slug='smartkids-online-christmas-2026-27',provider='Smart Kids School · Christmas Coding Camps',
        country='Швейцария',iso='CHE',place=T('Онлайн из любой страны; оператор в Швейцарии, место ребёнка дома.','En línea desde cualquier país; operador en Suiza, niño desde casa.'),
        themes=['coding','games'],formats=['online'],catalog_participation='online_camp',age=T('Основные лагеря от 7 лет; Advanced Python от 12, верхний возраст основной группы не указан.',
                                                                                             'Campamentos generales desde 7 años; Advanced Python desde 12, máximo del grupo general sin indicar.'),
        language=language,confirmed_instruction_languages=[],programme=programme+' '+hours,
        timing=dict(status='published_2026_27',label=T('28–31 декабря 2026 и 4–7 января 2027; две отдельные 4-дневные недели, не непрерывный лагерь.',
                                                    '28–31 de diciembre de 2026 y 4–7 de enero de 2027; dos semanas separadas de 4 días, no campamento continuo.'),
                    sessions=[[v['start'],v['end']] for v in details],session_details=details,precision='published_sessions'),
        price=dict(year=2026,season='2026/27',currency='CHF',amount=449,unit='week',label=price,
                   included=T('4 полудня с перерывами, онлайн-преподаватель, итоговый проект и сертификат оператора.','4 medias jornadas con pausas, profesor en línea, proyecto final y certificado del operador.'),extras=extras,deposit=cancel),
        accommodation=T('Из дома, без пансиона и очного дневного присмотра.','Desde casa, sin internado ni cuidado diurno presencial.'),
        family_fit=dict(matvey=details[0]['family_fit']['matvey'],oscar=dict(status='conditional',detail=T('Декабрь не подходит; январь только после 7-летия на момент начала. Язык и конкретную группу подтвердить.',
                                                                                                    'Diciembre no cumple; enero solo tras cumplir 7 al inicio. Confirmar idioma y grupo concreto.'))),
        editorial_reason=T('Датированный вариант без перелёта для старшего; предпочтительный язык и часовой пояс пока не доказаны, для младшего существенное возрастное ограничение.',
                           'Opción fechada sin vuelo para el mayor; idioma preferido y zona horaria sin acreditar, con límite de edad importante para el menor.'),
        shortlist=[],questions=questions,sources=[dict(title=T('Официальные лагеря: недели, цена и условия','Campamentos oficiales: semanas, precio y condiciones'),url=SMART,checked=CHECKED),
            dict(title=T('Официальная школа: оборудование и сопровождение дома','Escuela oficial: dispositivo y acompañamiento en casa'),url='https://smartkids-school.ch/en',checked=CHECKED)],checked=CHECKED)


def enrich_v142(d):
    # Static and browser exports use the same exact, build-derived instants.
    # Historical records stay byte-for-byte unchanged.
    for e in d['events']:
        if not e.get('end') or e['end'] < CHECKED: continue
        for s in e.get('sessions', []):
            if not s.get('ical_timed'): continue
            for field, clock in [('start_utc','start_time'),('end_utc','end_time')]:
                s[field]=local_to_utc(s['date'],s[clock],s['timezone']).isoformat().replace('+00:00','Z')
            assert s['end_utc'] > s['start_utc']
    # Registration is an indicative window, not a fixed competition deadline.
    note=T('Полный FAQ LEGO содержит обе формулировки: регистрация после BIOGLOW и между мартом–маем 2027; запуск сезона в августе 2027. Это ориентиры будущей регистрации, не точный дедлайн, не дата турнира и не подтверждённый национальный вход. Новая LEGO League и новая FIRST K–8 — независимые программы.',
           'FAQ completo LEGO incluye ambas formulaciones: registro después de BIOGLOW y entre marzo–mayo de 2027; lanzamiento en agosto de 2027. Son orientaciones de registro futuro, sin plazo exacto, fecha de torneo ni vía nacional confirmada. Nueva LEGO League y nueva FIRST K–8 son programas independientes.')
    event=next(e for e in d['events'] if e['id']=='C1048')
    event.update(checked=CHECKED,registration_status=note)
    url='https://education.lego.com/en-au/lego-league/program-update/'
    if not any(r['url']==url for r in event['references']):event['references'].append(dict(label=T('Полный FAQ перехода LEGO League','FAQ completo de transición LEGO League'),url=url))
    guide=next(p for p in d['league_guide']['profiles'] if p['id']=='lego-league-2027')
    guide['nuances']=[n for n in guide.get('nuances',[]) if not n.startswith('Полный FAQ LEGO')]+[note]
    if not any(s['url']==url for s in guide['sources']):guide['sources'].append(dict(title=T('Полный FAQ перехода LEGO League','FAQ completo de transición LEGO League'),url=url,checked=CHECKED))
    d['league_guide']['version']=142
    d['asof']=max(d['asof'],CHECKED)
