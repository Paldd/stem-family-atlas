"""Asian winter teaching, dated robotics divisions and exhibition provenance."""
from copy import deepcopy
from datetime import date, timedelta

CHECKED='2026-11-04'
SPANISH={}
def T(ru,es):
    SPANISH[ru]=es
    return ru

WRL='https://worldrobotleague.net/'
SOR='https://www.sor.com.sg/holiday-program-nov-dec-2026'
CODING='https://codinglab.jp/holiday-coding-tech-camp/'
ROBOFEST='https://robofest.me/'
MARC='https://www.marc-association.org/post/marc-2027-international-final-coming-to-taiwan'
GST='https://www.iras.gov.sg/taxes/goods-services-tax-%28gst%29/basics-of-gst/current-gst-rates'
FIT=T('Условно: проверить класс, возраст на дату, уровень, язык и приём семьи.',
      'Condicional: confirmar curso escolar, edad en fecha, nivel, idioma y admisión familiar.')
NO=T('Нет по возрасту выбранной категории; другие варианты проверяются отдельно.',
     'No cumple edad de categoría elegida; comprobar otras opciones por separado.')

def age_fit(lo,hi,start,lower_unknown=False):
    fits={}
    for child,born in [('matvey',2017),('oscar',2020)]:
        youngest=date.fromisoformat(start).year-born-1;oldest=youngest+1
        status='later' if lo is not None and oldest<lo else 'not_eligible' if hi is not None and youngest>hi else 'candidate' if not lower_unknown and (lo is None or youngest>=lo) and (hi is None or oldest<=hi) else 'conditional'
        detail=T(f'В год программы возраст {youngest}–{oldest}; точный день рождения неизвестен. Допуск конкретного дня, уровень и зачисление отдельно.',
                 f'Edad en año del programa {youngest}–{oldest}; fecha exacta de nacimiento desconocida. Confirmar admisión por día, nivel y aceptación.')
        if lower_unknown:detail+=' '+T('Верхний предел указан, нижний возраст не опубликован.','Límite superior indicado; edad mínima sin publicar.')
        fits[child]=dict(status=status,detail=detail)
    return fits

JP_LANGUAGE=T('Общая страница Holiday Camp прямо заявляет обучение на английском. Очное и онлайн-участие указаны на карточках; это не вывод из языка интерфейса.',
              'Página general Holiday Camp declara enseñanza en inglés. Fichas indican asistencia presencial y en línea; no se infiere del idioma de interfaz.')
JP_PRICE=T('45000 JPY за выбранный 5-дневный курс, налог не включён. Полный итог с налогом и условия оплаты подтвердить; 9500 JPY без налога — опубликованный однодневный вариант Minecraft, не тариф всех курсов.',
           '45000 JPY por curso elegido de 5 días, impuesto excluido. Confirmar total con impuesto y pago; 9500 JPY sin impuesto corresponde a opción Minecraft de un día, no tarifa de todos los cursos.')
JP_QUESTIONS=[T('Подтвердить свободное место, формат очно / онлайн, точную возрастную отсечку, оценку уровня и совместимость своего устройства для онлайн.',
                'Confirmar plaza, formato presencial / en línea, corte de edad, evaluación de nivel y dispositivo propio compatible en línea.'),
              T('Получить итог с налогом, правила отмены, лицензию и оборудование; Available Tickets: 8 в виджете не является бронью. Текст sold out — скрытый шаблон ошибки, а не доказательство закрытого набора.',
                'Obtener total con impuesto, cancelación, licencia y equipo; Available Tickets: 8 del widget no es reserva. Texto sold out es plantilla oculta de error, no prueba de inscripción cerrada.')]

def japanese_profiles():
    rows=[
        (1139,'scratch','Scratch 1',7,9,'10:00','12:00',['coding','games'],
         T('Scratch: игровые проекты и вычислительное мышление; без обязательного предшествующего курса. После 3 лет соревнований проверить, не слишком ли начальный уровень.',
           'Scratch: proyectos de juegos y pensamiento computacional; sin curso previo obligatorio. Tras 3 años de competición, comprobar si nivel inicial resulta adecuado.')),
        (1140,'python','Python 1',13,18,'10:00','12:00',['coding'],
         T('Начальный Python для 13–18 лет. Возрастное название курса отличается от Python Junior; обоим детям пока будущая ступень.',
           'Python inicial para 13–18 años. Curso distinto de Python Junior; etapa futura para ambos hijos.')),
        (1141,'python-junior','Python Junior 1',10,12,'10:00','12:00',['coding'],
         T('Python через математику начальной школы; без обязательной предварительной подготовки, но минимум 10 лет. В декабре 2026 Матвею ещё нет 10.',
           'Python mediante matemáticas de primaria; sin preparación previa obligatoria, pero mínimo 10 años. En diciembre de 2026 Matvey aún no cumple 10.')),
        (1142,'minecraft','Minecraft Coding',7,12,'13:00','15:00',['coding','games'],
         T('Кодирование мира Minecraft, постройки и автоматизация. Текст допускает все уровни, но поле prerequisite требует P102 Scratch 2 или одобрение учителя; размещение по уровню подтвердить.',
           'Programación de mundos Minecraft, construcciones y automatización. Texto admite todos los niveles, pero prerequisite exige P102 Scratch 2 o aprobación docente; confirmar asignación de nivel.')),
        (1143,'roblox','Roblox Game Design with Lua',10,12,'13:00','15:00',['coding','games'],
         T('Roblox Studio и Lua. Возраст рекомендаций 10–12, теги также 13–18; предварительные курсы расходятся: P201/P205/P206 против P205/S101 или одобрение. Билет содержит лишнее 3–7 рядом с Dec 14–18; не создаём из этого вторую смену.',
           'Roblox Studio y Lua. Recomendación 10–12, etiquetas también 13–18; previos discrepantes: P201/P205/P206 frente a P205/S101 o aprobación. Billete incluye 3–7 extra junto a Dec 14–18; sin crear una segunda sesión.'))]
    out=[]
    slugs={'scratch':'scratch-1','python':'python-1','python-junior':'python-junior-1','minecraft':'minecraft-coding','roblox':'roblox-game-design-camp-with-lua'}
    for ident,key,name,lo,hi,begin,end,themes,programme in rows:
        path=slugs[key]+('-5-days-holiday-camp-12-14-2026/' if key!='roblox' else '-5-days-holiday-camp-12-14-2026/')
        url='https://codinglab.jp/events/'+path+'?occurrence=2026-12-14'
        fit=age_fit(lo,hi,'2026-12-14')
        if key=='minecraft':fit['matvey']['status']='conditional'
        hours=T(f'14–18 декабря 2026: 5 блоков {begin}–{end}, Asia/Tokyo. Это 10 часов расписания; паузы не детализированы.',
                f'14–18 de diciembre de 2026: 5 bloques {begin}–{end}, Asia/Tokyo. Son 10 horas de horario; pausas sin detallar.')
        if key=='roblox':hours=T('Начало 14.12.2026, 13:00–15:00 Asia/Tokyo. Билет на 5 дней содержит одновременно Dec 14–18 и лишнее 3–7; период отмечен предварительным, ежедневные точные слоты не создаются.',
                                 'Inicio 14.12.2026, 13:00–15:00 Asia/Tokyo. Billete de 5 días incluye Dec 14–18 y 3–7 extra; período provisional, sin crear franjas diarias exactas.')
        label=T('14–18 декабря · 5 занятий · очно либо онлайн, один курс в двух форматах',
                '14–18 de diciembre · 5 clases · presencial o en línea, un curso en dos formatos')
        variant=dict(start='2026-12-14',end='2026-12-18',label=label,source=url,price=JP_PRICE,family_fit=fit,
            programme=programme+' '+hours,date_scope='session_days',
            date_status='Предварительно' if key=='roblox' else 'Подтверждено',
            sessions=[dict(date=f'2026-12-{n:02}',start_time=begin,end_time=end,timezone='Asia/Tokyo',ical_timed=True,topic=name,
                time_note=T('Местное японское время; для онлайн календарь переводится в часовой пояс устройства.','Hora local japonesa; calendario en línea se convierte a zona del dispositivo.')) for n in range(14,19)])
        if key=='roblox':
            variant['date_scope']='camp_window'
            variant.pop('sessions')
        profile=dict(id=f'CP{ident}',slug='codinglab-japan-winter-'+key+'-2026',provider='Coding Lab Japan · '+name,
            country='Япония',iso='JPN',place=T('Токио · кампус Coding Lab уточнить для выбранного курса; возможен онлайн из дома.',
                                          'Tokio · confirmar campus Coding Lab del curso; opción en línea desde casa.'),
            themes=themes,formats=['day','online'],catalog_participation='day_or_online',
            age=T(f'{lo}–{hi} лет по рекомендациям курса',f'{lo}–{hi} años según recomendaciones del curso'),
            language=JP_LANGUAGE,confirmed_instruction_languages=['EN'],programme=programme+' '+hours,
            timing=dict(status='partial_2026' if key=='roblox' else 'published_2026',label=label,sessions=[['2026-12-14','2026-12-18']],session_details=[variant]),
            price=dict(year=2026,currency='JPY',amount=45000,tax_included=False,unit='course',label=JP_PRICE,
                included=T('Карточки заявляют материалы и оборудование на занятии; для онлайн порядок предоставления техники и лицензии уточнить.',
                           'Fichas indican materiales y equipo en clase; confirmar dispositivo y licencia en modalidad en línea.'),
                extras=T('Налог, жильё, дорога и питание семьи отдельно; комплект домой не заявлен.','Impuesto, alojamiento, transporte y comida familiar aparte; sin kit anunciado para casa.'),
                deposit=T('Нужен вход в аккаунт для записи; текущие условия отмены и подтверждение места запросить до оплаты. Семья не записана.',
                          'Registro requiere cuenta; obtener cancelación y confirmación de plaza antes de pagar. Familia sin inscripción.')),
            accommodation=T('Пятидневный короткий дневной курс или онлайн, без пансиона.','Curso corto diurno de cinco días o en línea, sin internado.'),
            family_fit=fit,editorial_reason=T('Датированный англоязычный технический курс; Scratch и Minecraft потенциально по возрасту старшему, остальные пока старше обоих. Наличие мест отдельно.',
                                            'Curso técnico en inglés fechado; Scratch y Minecraft potencialmente por edad para el mayor, restantes para edades superiores a ambos. Plaza por separado.'),
            shortlist=[],questions=JP_QUESTIONS,sources=[dict(title=T('Официальная зимняя карточка курса','Ficha oficial de curso invernal'),url=url,checked=CHECKED),
                dict(title=T('Holiday Camp: EN преподавание и расписание','Holiday Camp: enseñanza EN y horario'),url=CODING,checked=CHECKED)],checked=CHECKED,parent_programme_id='CP285')
        if key=='roblox':
            profile['timing'].update(sessions=[],session_details=[],unpublished_session_hint=variant,
                label=T('Билет номинально Dec 14–18 2026, но содержит лишнее 3–7; подтверждённый диапазон не установлен, календарная смена не создаётся.',
                        'Billete nominal Dec 14–18 2026 con 3–7 extra; rango confirmado sin acreditar, sin crear sesión de calendario.'))
        out.append(profile)
    return out

SG_LANGUAGE=T('EN сайт и плакаты прочитаны; язык самого преподавания EN/ES/RU прямо не подтверждён. Согласовать английского преподавателя для выбранных дат.',
              'Leídos web y carteles EN; idioma docente EN/ES/RU sin confirmar expresamente. Acordar profesor en inglés para fechas elegidas.')
SG_PRICE=T('Цена за ребёнка-день без GST: 1–2 дня — 200 SGD; 3–4 — 180; 5–9 — 160; 10+ — 140. С GST 9% расчёт даёт соответственно 218 / 196.20 / 174.40 / 152.60 SGD за день. До 07.11.2026 заявлены 20% при записи и оплате; применение к пакету подтвердить. Это не цена всего периода каникул.',
           'Precio por niño-día sin GST: 1–2 días — 200 SGD; 3–4 — 180; 5–9 — 160; 10+ — 140. Con GST 9%, cálculo respectivo 218 / 196.20 / 174.40 / 152.60 SGD por día. Hasta 07.11.2026 se anuncia 20% con registro y pago; confirmar aplicación al paquete. No es precio de todo el período vacacional.')
SG_PROGRAMME=T('День 10:30–15:30, включая обед 12:30–13:30: 4 часа занятий, не 5. Выбирается только один курс в день. Указанные даты — варианты посещения, не обязательная непрерывная смена; филиалы и курсы не перемножены автоматически.',
               'Día 10:30–15:30, incluido almuerzo 12:30–13:30: 4 horas de clases, no 5. Solo un curso por día. Fechas son opciones de asistencia, no estancia continua obligatoria; sin multiplicar automáticamente sedes y cursos.')
SG_EXTRAS=T('Обед включён; свой разрешён без обещания снижения цены. Дополнительный присмотр 5 SGD без GST за 15 минут; при 9% это 5.45 SGD. Карточная admin fee без опубликованного размера; жильё и дорога отдельно. Техника в пользование, выдача набора домой не обещана.',
            'Almuerzo incluido; comida propia permitida sin prometer rebaja. Cuidado adicional 5 SGD sin GST por 15 minutos; con 9% son 5.45 SGD. Comisión de tarjeta sin importe publicado; alojamiento y transporte aparte. Equipo de uso, sin promesa de kit para casa.')
SG_CANCEL=T('Кредиты действуют до конца выбранных каникул, без возврата и переноса на другой период; могут делиться между братьями/сёстрами одной семьи. Доплата к пакету не предусмотрена. Перенос занятия минимум за 48 часов и при наличии мест; при отмене оператором предлагают альтернативу.',
            'Créditos hasta fin de vacaciones elegidas, sin devolución ni traslado a otro período; compartibles entre hermanos de misma familia. Sin recarga del paquete. Cambio de clase con mínimo 48 horas y plaza; cancelación del operador con alternativa.')

def singapore_profiles(facts):
    courses=[(1144,'essential','SPIKE Essential · Roboquest / Twinbot',None,7,['robotics'],
              T('Плакат: младше 8; нижний возраст не указан. Матвей 2017 уже старше этой группы; Оскару проверить минимум.','Cartel: menores de 8; mínimo sin indicar. Matvey 2017 supera grupo; confirmar mínimo para Oscar.')),
             (1145,'prime','SPIKE Prime · Battlebots',7,None,['robotics'],T('Плакат 7+.','Cartel 7+.')),
             (1146,'minecraft','Minecraft · World Manipulator',8,None,['coding','games'],T('Плакат 8+.','Cartel 8+.')),
             (1147,'printing','3D Printing · Spin Strikers / Trinket',8,None,['makers'],
              T('Плакат 8+, подзаголовок страницы 7+; до уточнения использовать 8+. Нужен навык мыши.','Cartel 8+, subtítulo web 7+; usar 8+ hasta aclarar. Requiere manejo de ratón.')),
             (1148,'python','Python · Level 1 / Level 2',9,None,['coding'],T('Плакат 9+; Level 2 требует посещения Level 1.','Cartel 9+; Level 2 exige haber asistido a Level 1.')),
             (1149,'vex','VEX IQ · Controller Commanders',9,None,['robotics'],T('Плакат 9+; только Bukit Timah по расписанию.','Cartel 9+; solo Bukit Timah según horario.'))]
    out=[]
    for ident,key,name,lo,hi,themes,age in courses:
        details=[]
        for branch in facts['branches']:
            days=[(day,offers[key]) for day,offers in branch['schedule'].items() if key in offers]
            if not days:continue
            groups=[days] if key!='python' else [days[n:n+3] for n in range(0,len(days),3)]
            for n,group in enumerate(groups):
                start,end=group[0][0],group[-1][0];fit=age_fit(lo,hi,start,lo is None)
                label=branch['name']+' · '+(group[0][1] if key=='python' else T('выбор отдельных дней','selección de días individuales'))
                detail=dict(start=start,end=end,variant_key=branch['key']+('-'+str(n+1) if key=='python' else ''),label=label,
                    place=branch['name']+' · '+branch['address'],source=SOR,price=SG_PRICE,age=age,family_fit=fit,date_scope='session_days',
                    programme=name+'; '+age+' '+SG_PROGRAMME,
                    sessions=[dict(date=day,start_time='10:30',end_time='15:30',timezone='Asia/Singapore',ical_timed=True,topic=name+' · '+topic,
                        time_note=T('Обед 12:30–13:30 включён в длительность; один выбранный курс в день.','Almuerzo 12:30–13:30 incluido en duración; un curso elegido por día.')) for day,topic in group],
                    proof=T('Визуально прочитаны оригинальные расписания всех 3 филиалов и возрастные плакаты. Только перечисленные дни и темы; общий период не превращён в ежедневный курс.',
                            'Leídos visualmente horarios originales de 3 sedes y carteles de edad. Solo días y temas enumerados; período general no convertido en curso diario.'))
                if key=='python':detail['programme']+=' '+T('Трёхдневная полоса уровня на плакате; обязательность всех 3 дней уточнить.','Franja de nivel de tres días en cartel; confirmar obligatoriedad de los 3 días.')
                details.append(detail)
        out.append(dict(id=f'CP{ident}',slug='sor-nov-dec-'+key+'-2026',provider='School of Robotics Singapore · '+name,country='Сингапур',iso='SGP',
            place=T('Сингапур · конкретный филиал и дни указаны в варианте курса.','Singapur · sede y días concretos por variante.'),themes=themes,formats=['day'],age=age,
            language=SG_LANGUAGE,confirmed_instruction_languages=[],programme=name+'; '+age+' '+SG_PROGRAMME,
            timing=dict(status='published_2026',label=T('24 ноября — 18 декабря 2026; точные дни различаются по курсу и филиалу.','24 de noviembre — 18 de diciembre de 2026; días exactos según curso y sede.'),
                variant_keyed=True,sessions=[[v['start'],v['end']] for v in details],session_details=details),
            price=dict(year=2026,currency='SGD',unit='child_day',tax_included=False,gst_rate=9,early_offer_deadline='2026-11-07',label=SG_PRICE,
                tiers=[dict(min_days=a,max_days=b,net_per_day=n,gross_per_day=round(n*1.09,2)) for a,b,n in [(1,2,200),(3,4,180),(5,9,160),(10,None,140)]],
                included=T('Два блока по 2 часа, час обеда с едой; оборудование используется на занятии.','Dos bloques de 2 horas, hora de almuerzo con comida; equipo de uso en clase.'),extras=SG_EXTRAS,deposit=SG_CANCEL),
            accommodation=T('Дневной курс без ночного проживания.','Curso diurno sin alojamiento nocturno.'),family_fit=deepcopy(details[0]['family_fit']),
            editorial_reason=T('Проверено точное расписание, но язык и место в группе требуют подтверждения. Внутренние Battlebots не являются международным турниром или отбором VEX.',
                               'Horario exacto verificado; confirmar idioma y plaza. Battlebots internos no son torneo internacional ni clasificación VEX.'),shortlist=[],
            questions=[T('Подтвердить EN преподавание, возраст конкретного дня, наличие мест, технику и единую сумму с GST, скидкой и комиссией.',
                         'Confirmar enseñanza EN, edad por día, plazas, equipo e importe único con GST, descuento y comisión.'),
                       T('Выбрать один курс на день; отдельно проверить медицинские сведения, питание и условия фото. Форму семьи не заполняли, согласия и оплату не оформляли.',
                         'Elegir un curso por día; revisar datos médicos, comida y condiciones de fotos. Sin completar formulario familiar, consentimientos ni pago.')],
            sources=[dict(title=T('Официальный сезон: часы, пакеты и условия','Temporada oficial: horas, paquetes y condiciones'),url=SOR,checked=CHECKED),
                dict(title=T('Официальная ставка GST для расчёта','Tipo oficial GST para cálculo'),url=GST,checked=CHECKED)]+
                [dict(title=T('Оригинальный календарь филиала','Calendario original de sede'),url=b['source_image'],checked=CHECKED) for b in facts['branches']]+
                [dict(title=T('Возрастной плакат выбранного курса','Cartel de edad del curso elegido'),url=facts['age_posters'][key]['url'],checked=CHECKED)],checked=CHECKED))
    return out

WRL_ENTRY=T('Регистрация местных и международных участников 09.11–21.12.2026; форма откроется 9 ноября. При классификации важна текущая школа; смешанная elementary / middle команда идёт в старшую группу. Возрастные цифры регламента и школьный класс иностранного ребёнка сверить вместе.',
            'Registro local e internacional 09.11–21.12.2026; formulario abre el 9 de noviembre. Clasificación según escuela actual; equipo mixto elementary / middle compite en mayor. Comprobar conjuntamente edades del reglamento y curso del alumno extranjero.')
WRL_REWARD=T('Организатор объявляет World Champion и Champion по 1 команде, Gold/Silver/Bronze по 2, специальные награды и электронные сертификаты. Названия наград — система WRL, не независимый мировой рейтинг. Переход к MRC Bangkok / RoboRAVE Houston заявлен для лучших; конкретную квоту и категорию подтвердить.',
             'Organizador anuncia World Champion y Champion para 1 equipo cada uno, Gold/Silver/Bronze para 2, premios especiales y certificados electrónicos. Títulos propios de WRL, no ranking mundial independiente. Vía a MRC Bangkok / RoboRAVE Houston anunciada para destacados; confirmar cuota y categoría.')
WRL_NOTE=T('Фестиваль 19–21.02.2027 в Goyang YMCA Youth Center. День категории указан отдельно; финальный тайминг может меняться. Взнос и жильё не опубликованы, комнаты на площадке на 3/4 человека бронирует руководитель. Младший JBC sub-event ограничен корейским гражданством и семье не подходит.',
           'Festival 19–21.02.2027 en Goyang YMCA Youth Center. Día por categoría separado; horario final sujeto a cambios. Cuota y alojamiento sin publicar, habitaciones de 3/4 personas por responsable. Subevento JBC infantil limitado a ciudadanía coreana, no apto para esta familia.')

def competition_updates(d):
    idx={e['id']:e for e in d['events']}
    days={'C1145':'2027-02-20','C1146':'2027-02-21','C1147':'2027-02-21','C1148':'2027-02-20','C1149':'2027-02-21','C1150':'2027-02-20'}
    for ident,day in days.items():
        e=idx[ident];e.update(start=day,end=day,deadline='2026-12-21',date_status='Подтверждено',date_scope='festival_window',checked=CHECKED,
            city='Goyang · Goyang YMCA Youth Center',period=T('19–21 февраля 2027 · выбранная дисциплина в указанную дату','19–21 de febrero de 2027 · disciplina elegida en fecha indicada'),
            entry=WRL_ENTRY,reward=WRL_REWARD,note=WRL_NOTE,
            registration_status=T('Открытие 09.11.2026, закрытие 21.12.2026; точное время не указано. Заявка семьи не подана.',
                                  'Apertura 09.11.2026, cierre 21.12.2026; hora exacta sin indicar. Sin solicitud familiar.'),
            action=T('До записи сверить текущий школьный класс, категорию, версию правил, язык судейства и полный счёт. Для MRC обещаны финальные изменения минимум за 50 дней.',
                     'Antes del registro comprobar curso escolar, categoría, versión de reglas, idioma de jueces y factura total. MRC promete cambios finales con mínimo 50 días.'),
            proof=T('Повторно прочитаны текущие приглашение, по-дневное расписание и правила WRL; даты и город теперь объявлены. Английский/испанский текст правил не доказывает язык судей.',
                    'Releídos invitación actual, calendario por día y reglas WRL; fechas y ciudad ya anunciadas. Texto de reglas inglés/español no acredita idioma de jueces.'))
    idx['C1145']['note']+=' '+T('AI Othello теперь имеет опубликованные отличия и отдельную карточку C1180.','AI Othello ya tiene diferencias publicadas y ficha separada C1180.')
    idx['C1146']['gear']=T('Только официальные LEGO; Junior SPIKE Prime. До 1000 g, 20 × 20 × 20 cm, расширение до 25 × 25 cm. WRL по умолчанию 3 vs 3; 2–3 участника и 2–4 робота по summary. Окончательную редакцию и требование 3 роботов подтвердить.',
                           'Solo LEGO oficial; Junior SPIKE Prime. Hasta 1000 g, 20 × 20 × 20 cm, expansión a 25 × 25 cm. WRL por defecto 3 vs 3; 2–3 participantes y 2–4 robots según resumen. Confirmar edición final y requisito de 3 robots.')
    idx['C1147']['format']=T('Альянсы участников формируются на месте; единая лига по очкам, окончательный состав и техника ещё TBA.',
                             'Alianzas de participantes se forman en sede; liga única por puntuación, composición final y equipo aún TBA.')
    idx['C1147']['priority']='P3 — '+T('дата есть, полные правила ещё не опубликованы','fecha publicada, reglamento completo aún pendiente')
    idx['C1148']['note']+=' '+T('Кольцо Korea Open 800 mm, глобальная версия 100 cm; действует локальная поправка. Open 3 kg здесь не проводится.',
                               'Dohyo Korea Open 800 mm, versión global 100 cm; rige ajuste local. Sin categoría Open 3 kg aquí.')
    for ident in ['C1148','C1149','C1150']:
        idx[ident]['age']=T('ES: начальная школа по текущему обучению; минимальный возраст и дата определения иностранного класса не объявлены.',
                           'ES: primaria según escolarización actual; mínimo de edad y fecha de equivalencia extranjera sin anunciar.')
        idx[ident]['mat']=idx[ident]['osc']=FIT
    e=idx['C1151'];e.update(checked=CHECKED,date_status='Не объявлено',priority='P3 — '+T('категория отсутствует в текущем местном списке','categoría ausente de lista local actual'),
        period=T('a-MAZE-ing не входит в текущие 4 дисциплины RoboRAVE Korea Open 2027; дату и местный приём не переносить с фестиваля.',
                 'a-MAZE-ing no figura entre 4 disciplinas actuales de RoboRAVE Korea Open 2027; sin trasladar fechas ni admisión del festival.'),
        entry=T('Глобальная категория существует, но местный запуск Korea Open 2027 не подтверждён.','Existe categoría global, sin confirmar edición local Korea Open 2027.'),
        registration_status=T('Не подтверждена для Korea Open 2027.','Sin confirmar para Korea Open 2027.'),
        action=T('Следить за отдельным анонсом a-MAZE-ing; не записывать на неё ребёнка по общему календарю WRL.','Esperar anuncio propio a-MAZE-ing; no inscribir mediante calendario general WRL.'),
        proof=T('Текущие главный список, расписание и страница RoboRAVE содержат SumoBot, Line Following, MiddleBot, SoccerBot RC; a-MAZE-ing отсутствует.',
                'Lista principal, horario y web RoboRAVE actuales contienen SumoBot, Line Following, MiddleBot, SoccerBot RC; a-MAZE-ing ausente.'))
    added=[]
    for ident,title,day,age,gear,source in [
        ('C1180','WRL 2027 · AI Othello Junior U12','2027-02-19',
         T('U12: 12 лет включительно и младше; текущая школьная классификация и минимальный возраст отдельно.','U12: 12 años o menos; clasificación escolar actual y mínimo por separado.'),
         T('AI camera, максимум 600 g, высота не ограничена; остальные базовые Othello правила. Нет start target; движение через 3 секунды после сигнала. Исключение по вылету блока; это отдельный AI дивизион.',
           'AI camera, máximo 600 g, sin límite de altura; restantes reglas básicas Othello. Sin start target; movimiento tras 3 segundos de señal. Excepción de salida del bloque; división AI separada.'),'othello'),
        ('C1181','WRL 2027 · MRC Soccer Open Hardware Junior','2027-02-19',
         T('Junior 5–13 по summary; текущую школу и финальную редакцию 2027 подтвердить.','Junior 5–13 según resumen; confirmar escuela actual y edición final 2027.'),
         T('Любая марка, до 1000 g и 20 × 20 × 20 cm; только колёса. WRL 3 vs 3 по умолчанию, 2–3 участника / 2–4 робота; два тайма по 2 минуты.',
           'Cualquier marca, hasta 1000 g y 20 × 20 × 20 cm; solo ruedas. WRL 3 vs 3 por defecto, 2–3 participantes / 2–4 robots; dos mitades de 2 minutos.'),'mrc-soccer'),
        ('C1182','WRL 2027 · MRC Soccer Micro Junior','2027-02-20',
         T('Summary Micro: 8–19; главный календарь делит Junior / Senior. Возраст и школьный дивизион сверить.',
           'Resumen Micro: 8–19; calendario principal divide Junior / Senior. Comprobar edad y división escolar.'),
         T('До 100 g без пульта; 5 × 5 × 8 cm, расширение 7 × 7 × 10 cm. Дистанционное управление, 3 vs 3 по WRL, 2–3 участника / 2–3 робота. Два тайма по 2 минуты.',
           'Hasta 100 g sin mando; 5 × 5 × 8 cm, expansión 7 × 7 × 10 cm. Control remoto, 3 vs 3 WRL, 2–3 participantes / 2–3 robots. Dos mitades de 2 minutos.'),'mrc-soccer'),
        ('C1183','WRL 2027 · Humanoid Battle Featherweight Junior','2027-02-19',
         T('Junior 7–12; Оскару только после 7-летия, школьный дивизион и отсечку подтвердить.','Junior 7–12; Oscar solo tras cumplir 7, confirmar división escolar y corte.'),
         T('Гуманоид менее 1.7 kg, допуск +3 g; базовая стойка от 300 mm. Ревизия Ver 25.06.30; дополнительно Humanoid Standards. Матч 3 минуты, 5 downs для TKO; выбранный класс Feather Jr прямо в расписании.',
           'Humanoide de menos de 1.7 kg, tolerancia +3 g; postura básica desde 300 mm. Revisión Ver 25.06.30; además Humanoid Standards. Combate de 3 minutos, 5 downs para TKO; Feather Jr explícito en horario.'),'humanoid-battle')]:
        e=deepcopy(idx['C1145']);e.update(id=ident,title=title,start=day,end=day,source=WRL+'rules/'+source+'/',age=age,gear=gear,mat=FIT,osc=FIT,
            participation='team' if source=='mrc-soccer' else 'individual',format=T('Формат конкретной категории; параметры робота и число участников ниже.','Formato de categoría concreta; robot y número de participantes abajo.'),note=WRL_NOTE)
        if ident=='C1182':e['osc']=NO
        if ident=='C1183':e['themes']=['robotics']
        if ident=='C1180':e['themes']=['robotics','ai']
        added.append(e)
    base=deepcopy(idx['C053'])
    # Global championship metadata must not become evidence for local Taiwan rules.
    for inherited in ['language_mode','date_precision','evidence_level']:base.pop(inherited,None)
    tw_note=T('Главная страница объявляет Taiwan Robofest 06–07.03.2027, но день каждой категории, площадка, взносы, срок и приём иностранной семьи не раскрыты. Двухдневный диапазон — окно фестиваля, не обещание 2 дней участия. Локальные категории не гарантируют отбор на мировой финал.',
              'Web principal anuncia Taiwan Robofest 06–07.03.2027, sin día por categoría, sede, cuota, plazo ni admisión de familia extranjera. Rango de dos días es ventana del festival, sin promesa de participar 2 días. Categorías locales no garantizan clasificación mundial.')
    rules={
        'master':'https://drive.google.com/file/d/17j3UXf4NQu_nqbxynCxQ3qcnpN1OhKhs/view',
        'cat-k':'https://drive.google.com/file/d/14RT59HufskRfO3ZBPZB5eyNA5ZLn9--u/view',
        'cat-p':'https://drive.google.com/file/d/11hudU9vf8bifMrLpoLurgYBo3rKTxLUY/view',
        'parade':'https://drive.google.com/file/d/1JWxtu2wH5XGJPUXrRe8ERbbe9IRnvft_/view'}
    for ident,title,age,gear,key in [
        ('C1184','Taiwan Robofest 2027 · национальный фестиваль / отбор',
         T('Категории от детского сада до университета; точный школьный класс важнее года рождения.','Categorías desde infantil a universidad; curso escolar exacto importa más que año de nacimiento.'),
         T('Платформа, команда и материалы зависят от категории; не покупать общий набор без выбора.','Plataforma, equipo y materiales según categoría; no comprar kit general sin elegir.'),None),
        ('C1185','Taiwan Robofest 2027 · RoboCatapult Kindergarten',
         T('Детский сад: младшая–старшая группа; 1 участник и тренер от 20 лет.','Infantil: grupos menor a mayor; 1 participante y entrenador desde 20 años.'),
         T('Механическая катапульта из конструктора, ручной запуск; не автономный программируемый робот. Сборка на месте 30 минут, 10 мячей за 5 минут, размер до 40 × 40 cm, высота без лимита. Связанный PDF маркирован 2026, редакцию 2027 подтвердить.',
           'Catapulta mecánica de construcción, lanzamiento manual; no robot autónomo programable. Montaje en sede de 30 minutos, 10 pelotas en 5 minutos, hasta 40 × 40 cm, altura sin límite. PDF enlazado marcado 2026, confirmar edición 2027.'),'cat-k'),
        ('C1186','Taiwan Robofest 2027 · RoboCatapult Primary',
         T('Начальная школа: группы классов 1–3 и 4–6; 1 участник и тренер от 20 лет.','Primaria: grupos de cursos 1–3 y 4–6; 1 participante y entrenador desde 20 años.'),
         T('LEGO WeDo / BOOST / SPIKE / EV3 или VEX GO / IQ по связанному PDF. Сборка 30 минут, 10 мячей за 5 минут; ручная установка мяча, но автоматический запуск. До 30 × 30 cm и 500 g, один контроллер; число моторов и датчиков не ограничено. PDF 2026 — подтвердить редакцию 2027.',
           'LEGO WeDo / BOOST / SPIKE / EV3 o VEX GO / IQ según PDF enlazado. Montaje de 30 minutos, 10 pelotas en 5 minutos; colocar pelota a mano, lanzamiento automático. Hasta 30 × 30 cm y 500 g, un controlador; motores y sensores sin límite. PDF 2026: confirmar edición 2027.'),'cat-p'),
        ('C1187','Taiwan Robofest 2027 · Master Builder',
         T('Старшая группа детсада–класс 3; отдельно классы 4–6. Индивидуально.','Último curso infantil–curso 3; separados cursos 4–6. Individual.'),
         T('Оригинальные LEGO, основание 32 × 32 studs, без моторных элементов; тема Fun and Games. Сборка 50 минут, презентация 4 минуты и вопросы 2 минуты. PDF 10.11.2025: сдача рисунка 3/2 без года; дедлайн 2027 не назначен.',
           'LEGO original, base 32 × 32 studs, sin motores; tema Fun and Games. Montaje de 50 minutos, presentación de 4 minutos y preguntas de 2 minutos. PDF 10.11.2025: dibujo a entregar 3/2 sin año; sin asignar plazo 2027.'),'master'),
        ('C1188','Taiwan Robofest 2027 · RoboParade Explorer',
         T('Классы 1–4; команда 1–5 человек. Один участник разрешён, но минимальный балл teamwork.','Cursos 1–4; equipo de 1–5. Un participante permitido, con puntuación mínima de teamwork.'),
         T('Автономная платформа любой марки, чёрная линия и остановка перед роботом; тема Fun and Games. Ширина до 35 cm, вся длина до 60 cm, секция до 35 cm; скорость 7–16 cm/sec. Правила 2027 V1 от 25.09.2026.',
           'Plataforma autónoma de cualquier marca, línea negra y parada ante robot; tema Fun and Games. Ancho hasta 35 cm, longitud total hasta 60 cm, sección hasta 35 cm; velocidad 7–16 cm/sec. Reglas 2027 V1 de 25.09.2026.'),'parade')]:
        e=deepcopy(base);e.update(id=ident,title=title,country='Тайвань',iso=['TWN'],region='Азия',city=T('Тайвань · площадка 2027 не установлена','Taiwán · sede 2027 sin acreditar'),start='2027-03-06',end='2027-03-07',deadline='',
            period=tw_note,date_status='Подтверждено',date_scope='festival_window',age=age,mat=FIT,osc=FIT,gear=gear,
            source=ROBOFEST,checked=CHECKED,entry=tw_note,note=tw_note,format=T('По выбранной категории','Según categoría elegida'),
            participation='individual' if key in ['cat-k','cat-p','master'] else 'individual_or_team' if key is None else 'team',admission_kind='qualifier',
            language=T('Объявление ZH; есть EN правила RoboParade. Язык судейства и помощь EN/ES не подтверждены.','Anuncio ZH; hay reglas EN RoboParade. Idioma de jueces y apoyo EN/ES sin confirmar.'),languages=[],
            cost=T('Взнос и цена местного этапа 2027 не установлены; мировой тариф не переносить.','Cuota y precio de etapa local 2027 sin acreditar; no trasladar tarifa mundial.'),scope='national',level=T('Национальный этап / локальная категория Robofest','Etapa nacional / categoría local Robofest'),
            importance_reason=T('Местный формат и школьный возраст проверены по первичным источникам; допуск семьи и международный переход отдельно.','Formato local y curso escolar verificados mediante fuentes primarias; admisión familiar y paso internacional aparte.'),
            reward=T('Местный результат только по официальному протоколу; не автоматическая мировая награда.','Resultado local solo mediante acta oficial; sin premio mundial automático.'),
            priority='P2 — '+T('после проверки класса и иностранного допуска','tras confirmar curso escolar y admisión extranjera'),
            action=T('Уточнить площадку, день категории, класс по зарубежной школе, EN помощь, взнос и способ регистрации; локальное участие и отбор на мир разные условия.',
                     'Confirmar sede, día de categoría, equivalencia de curso extranjero, apoyo EN, cuota y registro; participación local y clasificación mundial son condiciones distintas.'),
            registration_status=T('Форма и срок 2027 для семьи не установлены.','Formulario y plazo 2027 de familia sin acreditar.'),
            proof=T('Прочитаны текущее объявление и связанные публичные PDF; старые версии и неизвестные условия сохранены явно.','Leídos anuncio actual y PDF públicos enlazados; versiones anteriores y condiciones desconocidas conservadas.'),
            references=[dict(label=T('Текущее объявление Taiwan Robofest','Anuncio actual Taiwan Robofest'),url=ROBOFEST)],themes=['makers','technology'] if key in ['master','cat-k'] else ['robotics'])
        e['related_ids']=['C1184'] if key else []
        if key:e['parent_event_id']='C1184';e['references'].append(dict(label=T('Связанный регламент выбранной категории','Reglamento enlazado de categoría elegida'),url=rules[key]))
        if key=='cat-k':e['mat']=T('Нет по школьной ступени детского сада.','No corresponde a etapa infantil.')
        added.append(e)
    e=deepcopy(idx['C035']);e.update(id='C1189',title='MARC 2027 · International Final · Taipei',start='2027-05-20',end='2027-05-23',deadline='',source=MARC,checked=CHECKED,
        country='Тайвань',iso=['TWN'],region='Азия',city=T('Тайбэй · точная площадка 2027 ещё не объявлена','Taipéi · sede exacta 2027 aún sin anunciar'),date_status='Подтверждено',date_scope='festival_window',
        period=T('20–23 мая 2027 · финал; дни отдельных категорий ещё неизвестны','20–23 de mayo de 2027 · final; días por categoría aún pendientes'),
        age=T('Возраст, классы и состав категорий финала 2027 ещё не объявлены.','Edades, cursos y categorías de final 2027 aún sin anunciar.'),mat=FIT,osc=FIT,
        format=T('Состав команды и категории финала ещё TBA.','Composición de equipo y categorías de final aún TBA.'),admission_kind='unknown',
        languages=[],language=T('EN анонс прочитан; язык судейства и помощи семье ещё не установлен.','Leído anuncio EN; idioma de jueces y apoyo familiar aún sin acreditar.'),
        priority='P3 — '+T('даты финала есть, возраст и путь входа пока не объявлены','fechas de final publicadas, edad y acceso aún pendientes'),
        entry=T('Оператор приглашает команды со всего мира; условия прямой заявки, отбора и wildcard 2027 ещё не опубликованы. Путь отбора 2026 не переносить автоматически.',
                'Operador invita equipos de todo el mundo; solicitud directa, clasificación y wildcard 2027 aún sin publicar. No trasladar automáticamente vía de 2026.'),
        gear=T('Анонсирован новый Drone Competition; техника, возраст и правила 2027 TBA. Не переносить LOM / TM hardware без регламента финала.',
               'Nueva Drone Competition anunciada; equipo, edad y reglas 2027 TBA. No trasladar hardware LOM / TM sin reglamento de final.'),
        cost=T('Взнос, техника, поездка и проживание 2027 не установлены.','Cuota, equipo, viaje y alojamiento 2027 sin acreditar.'),
        reward=T('Объявлен международный финал MARC; конкретные награды и признание результата проверить по регламенту 2027 и протоколу.',
                 'Final internacional MARC anunciada; verificar premios y reconocimiento mediante reglamento 2027 y acta.'),
        action=T('Следить за регистрацией, категориями, возрастом и площадкой; не бронировать семейную поездку по фотографиям площадки 2026.',
                 'Seguir registro, categorías, edades y sede; no reservar viaje familiar mediante fotos de sede 2026.'),
        note=T('NTSEC показан как воспоминание 2026, не подтверждён как площадка 2027. Международное приглашение не гарантирует место или допуск возраста.',
               'NTSEC aparece como recuerdo de 2026, sin confirmar sede 2027. Invitación internacional no garantiza plaza ni edad admitida.'),
        registration_status=T('Регистрация и полное расписание обещаны позже.','Registro y horario completo prometidos para más adelante.'),
        proof=T('Прочитан собственный анонс MARC: Тайбэй, 20–23.05.2027 и новая дроновая категория; подробные правила ещё обещаны.',
                'Leído anuncio propio MARC: Taipéi, 20–23.05.2027 y nueva categoría de drones; reglas detalladas aún prometidas.'),
        scope='international',level=T('Международный финал MARC · по названию организатора','Final internacional MARC · denominación del organizador'),
        references=[dict(label='MARC · International Final 2027',url=MARC)])
    for field in ['deadline_note','deadline_label','deadline_utc','registration_url','team_min','team_max','related_ids','event_code','parent_event_id']:
        e.pop(field,None)
    added.append(e)
    for e in added:
        if e['id'] in idx:idx[e['id']].update(e)
        else:d['events'].append(e);idx[e['id']]=e
    guide=next(p for p in d['league_guide']['profiles'] if p['id']=='world-robot-league')
    ids=list(dict.fromkeys(guide['event_ids']+[f'C{i}' for i in range(1180,1184)]))
    guide['event_ids']=ids;guide['categories']=[dict(name=idx[i]['title'],age=idx[i]['age'],team=idx[i]['format'],hardware=idx[i]['gear'],age_rule=idx[i]['age'],entry=idx[i]['entry'],event_id=i) for i in ids]
    guide['age_summary']=T('19–21.02.2027, Коян: U12 Othello / AI, MRC 5–13, Micro 8–19, Feather Jr 7–12, RoboRAVE ES. Школьная классификация обязательна; a-MAZE-ing пока вне местной программы.',
                           '19–21.02.2027, Goyang: U12 Othello / AI, MRC 5–13, Micro 8–19, Feather Jr 7–12, RoboRAVE ES. Clasificación escolar obligatoria; a-MAZE-ing fuera de programa local por ahora.')
    guide['route']=WRL_ENTRY
    for gid,ids in [('robofest',[f'C{i}' for i in range(1184,1189)]),('marc',['C1189'])]:
        g=next(p for p in d['league_guide']['profiles'] if p['id']==gid)
        g['event_ids']=list(dict.fromkeys(g['event_ids']+ids));g['categories']=[c for c in g['categories'] if c.get('event_id') not in ids]
        g['categories'] += [dict(name=idx[i]['title'],age=idx[i]['age'],team=idx[i]['format'],hardware=idx[i]['gear'],entry=idx[i]['entry'],event_id=i) for i in ids]
        url=ROBOFEST if gid=='robofest' else MARC
        if not any(s['url']==url for s in g['sources']):g['sources'].append(dict(title=T('Текущий анонс 2027','Anuncio actual 2027'),url=url,checked=CHECKED))
    for url in [WRL]+[WRL+'rules/'+s+'/' for s in ['othello','mrc-soccer','roborave','humanoid-relay','humanoid-battle']]:
        match=next((s for s in guide['sources'] if s['url']==url),None)
        if match:match['checked']=CHECKED
        else:guide['sources'].append(dict(title=T('Текущий анонс и правила WRL','Anuncio y reglas actuales WRL'),url=url,checked=CHECKED))
    for i in ['C035','C779']:
        ref=dict(label=T('Международный финал 2027: условия перехода ещё TBA','Final internacional 2027: acceso aún TBA'),url=MARC)
        if not any(r['url']==MARC for r in idx[i].get('references',[])):idx[i].setdefault('references',[]).append(ref)

def enrich_v143(d):
    competition_updates(d)
    idx={e['id']:e for e in d['events']}
    # Preserve the evidence records; one edition appears once in normal discovery.
    for alias,canonical in [('E185','E089'),('E186','E090'),('E187','E080')]:
        idx[alias]['canonical_event_id']=canonical
        idx[alias]['note']=T(f'Дополнительная запись источника той же выставки. Основная карточка {canonical}; сохранена для истории, не отдельное мероприятие.',
                             f'Registro adicional de fuente de misma feria. Ficha principal {canonical}; conservado como historial, no evento separado.')
    for ident in ['E080','E187']:
        idx[ident].update(checked=CHECKED,visitor_policy='adults_only',mat=NO,osc=NO,
            visitor_policy_note=T('Текущая visitor-страница ограничивает выставку Trade / Business Professionals 18+; форма регистрации интереса тоже требует 18+. Детского исключения не найдено.',
                                  'Página actual de visitantes limita exposición a Trade / Business Professionals 18+; formulario de interés también exige 18+. Sin excepción infantil encontrada.'),
            adult_entry=T('Профессиональная регистрация взрослого; форма интереса не является билетом.','Registro profesional adulto; formulario de interés no es entrada.'),
            references=[dict(label=T('Действующая visitor-страница','Página actual de visitantes'),url='https://visit.gitexasia.com/login'),
                        dict(label=T('Форма интереса, связанная с сайтом 2027','Formulario de interés enlazado desde web 2027'),url='https://event.gitexasia.com/pre-register-enquiry')])
    idx['E080']['note']=T('29–30.04.2027 в Marina Bay Sands. Для семьи планировать отдельный взрослый визит, а не детское участие. Старая дополнительная запись E187 сохранена как источник.',
                         '29–30.04.2027 en Marina Bay Sands. Planificar visita adulta separada, sin participación infantil. Registro adicional E187 conservado como fuente.')
    for ident in ['E090','E186']:
        idx[ident].update(checked=CHECKED,city='Singapore · Marina Bay Sands',proof=T('Текущая официальная страница отдельно объявляет 20–22.07.2027 в Marina Bay Sands; основной текст 2026 сохранён как другое издание.',
                                                                                 'Web oficial actual anuncia por separado 20–22.07.2027 en Marina Bay Sands; texto principal 2026 corresponde a otra edición.'))
    idx['E012'].update(checked=CHECKED,proof=T('Новый баннер iREX подтверждает начало декабря 2027 и приём заявок экспонентов с середины декабря 2026; точные дни и visitor-правила 2027 по-прежнему не опубликованы.',
                                            'Banner actual iREX confirma principios de diciembre de 2027 y solicitudes de expositores desde mediados de diciembre de 2026; días exactos y reglas de visitantes 2027 siguen sin publicar.'))
    d['league_guide']['version']=143
    existing={s['url'] for s in d['sources']}
    for e in d['events']:
        if e['id'] in {f'C{i}' for i in range(1180,1190)}|{'E080','E187'}:
            for ref in [dict(url=e['source'],label=e['title'])]+e.get('references',[]):
                if ref['url'] not in existing:
                    d['sources'].append(dict(url=ref['url'],title=ref['label'],evidence='official-primary',checked=CHECKED));existing.add(ref['url'])
    d['asof']=max(d['asof'],CHECKED)
