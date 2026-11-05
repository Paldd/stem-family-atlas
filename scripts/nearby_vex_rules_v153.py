"""Mexican VEX season calls and the October 2026 global age-policy revision."""
CHECKED='2026-11-05'
SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
POLICY='https://library.globalrobotics.org/hc/en-us/articles/51371951587732-Student-Eligibility-Policy'
MOBILE='https://academiastem.org/pdf/BasesRob%C3%B3ticaM%C3%B3vil2026-2027.pdf'
CALLS={
 'international':'https://academiastem.org/pdf/Convocatoria%20de%20participaci%C3%B3n%20%20Campeonato%20Internacional%20de%20Rob%C3%B3tica%20y%20Habilidades%20STEM%202026_2027v2.pdf',
 'national':'https://academiastem.org/pdf/Convocatoria%20de%20participaci%C3%B3n%20%2018vo.%20Campeonato%20Nacional%20de%20Rob%C3%B3tica%20y%20Habilidades%20STEM%202026v2.pdf',
 'girl':'https://academiastem.org/pdf/Convocatoria%20de%20participaci%C3%B3n%20GIRL%20POWERED.pdf'}
SEASON='https://academiastem.org/championships/'
TEAM_IQ=T('Местные Bases Robótica Móvil 2026–2027 требуют минимум 3 учеников для primaria / secundaria, одного ответственного преподавателя или asesor и один робот. Глобальные 2+ для IQ не отменяют местное требование: двух братьев недостаточно.',
          'Bases Robótica Móvil locales de 2026–2027 exigen mínimo 3 alumnos en primaria / secundaria, un docente o asesor responsable y un robot. El mínimo global de 2+ para IQ no elimina requisito local: dos hermanos no bastan.')
SCHOOL=T('Пункт 11 требует подтвердить регулярное обучение в участвующем учреждении действующим школьным документом. Допуск независимого клуба, homeschooling или команды из Коста-Рики к этой мексиканской заявке нужно согласовать; гражданство детей не определяет страну команды.',
         'Punto 11 exige acreditar matrícula regular en institución participante con documento escolar vigente. Acordar admisión de club independiente, homeschooling o equipo de Costa Rica a esta convocatoria mexicana; nacionalidad infantil no determina país del equipo.')
NOTEBOOK=T('Нужна инженерная тетрадь и три подготовленных учениками резюме: сезон, код и внешние источники / credits. Для команды без кода резюме кода не требуется. Это помощь интервью, не три отдельных приза; ребёнок должен понимать и объяснять своё решение.',
           'Se requiere cuaderno de ingeniería y tres resúmenes preparados por alumnos: temporada, código y fuentes externas / credits. Equipo sin código exento de resumen de código. Ayudan a entrevista, no son tres premios separados; el niño debe comprender y explicar su solución.')
WORLD=T('В действующих convocatorias выбранные путёвки на мировой финал становятся действительными лишь при участии в остальных двух чемпионатах сезона, включая Girl Powered. Но Girl Powered разрешён только женским командам. Это противоречие для команды мальчиков требует письменного разъяснения; гарантированный путь братьев на Worlds не подтверждён. Оно не доказывает запрет всех мировых турниров VEX для мальчиков.',
        'Convocatorias vigentes condicionan validez de ciertos pases mundiales a participar en otros dos campeonatos de temporada, incluido Girl Powered. Sin embargo Girl Powered admite solo equipos femeninos. Contradicción para equipo masculino requiere aclaración escrita; ruta garantizada de hermanos a Worlds sin confirmar. No demuestra prohibición de todos los torneos mundiales VEX para niños.')
SUBSIDY=T('Взнос события и VEX-ID различаются. В convocatorias объявлена субсидия 100% VEX-ID мексиканским командам; применимость семье, живущей в Коста-Рике, подтвердить отдельно. Робот, поле, сезонные детали, ноутбук, наставник, страховка и поездка в эту нулевую строку не входят.',
          'Cuota de evento y VEX-ID son distintos. Convocatorias anuncian subsidio del 100% de VEX-ID para equipos mexicanos; confirmar aplicación a familia residente en Costa Rica. Robot, campo, piezas de temporada, portátil, mentor, seguro y viaje no incluidos en esa línea de cero.')
QUESTION=T('До выбора мексиканской квалификации получить ответ: как мужская / смешанная или иностранная команда выполняет условие Girl Powered, какие категории получают квоту Worlds, принимается ли наш школьный статус и как применяется минимум состава. Вопрос подготовлен, организатору не отправлялся.',
           'Antes de elegir clasificación mexicana obtener respuesta: cómo equipo masculino / mixto o extranjero cumple requisito Girl Powered, qué categorías reciben cupo Worlds, si se acepta situación escolar y cómo se aplica mínimo de integrantes. Pregunta preparada, sin enviar al organizador.')

def ref(e,url,label):
    e['references']=[r for r in e.get('references',[]) if r['url']!=url]+[dict(url=url,label=label)]

def enrich_v153(d):
    rows={e['id']:e for e in d['events']}
    groups={'C337':'girl','C513':'state','C514':'international','C597':'national',
            'C1155':'national','C1156':'state','C1157':'national','C1158':'international'}
    for ident,group in groups.items():
        e=rows[ident];iq=ident not in ['C1157','C1158']
        e.update(checked=CHECKED,evidence_level='rules',team_min=3 if iq else 1,
                 proof=T('Свежая карточка VEX Events подтверждает даты, уровень и срок регистрации. Местные Bases и convocatorias прочитаны; существенные страницы состава, пола, квалификации и цен осмотрены визуально. Неизвестный допуск семьи не считается открытым местом.',
                         'Ficha actual de VEX Events confirma fechas, nivel y plazo de registro. Leídas Bases y convocatorias locales; páginas relevantes de integrantes, género, clasificación y precios inspeccionadas visualmente. Admisión familiar desconocida no equivale a plaza abierta.'))
        e['format']=TEAM_IQ if iq else T('Местная preparatoria: минимум 1 ученик, ответственный преподаватель / asesor и один VEX V5 робот. Подходящий школьный уровень и приём подтвердить.',
                                                        'Preparatoria local: mínimo 1 alumno, docente / asesor responsable y un robot VEX V5. Confirmar nivel escolar adecuado y admisión.')
        e['gear']=(T('VEX IQ Level Up: допустимый робот и notebook; LEGO / V5 не заменяют. ',
                     'VEX IQ Level Up: robot permitido y notebook; LEGO / V5 no sustituyen. ') if iq else
                   T('VEX V5 Override: допустимый робот и notebook; IQ / LEGO не заменяют. ',
                     'VEX V5 Override: robot permitido y notebook; IQ / LEGO no sustituyen. '))+NOTEBOOK
        e['entry']=T('Актуальный VEX-ID, регистрация команды и подтверждение конкретного турнира. ',
                     'VEX-ID vigente, registro de equipo y confirmación de torneo concreto. ')+SCHOOL
        e['registration_status']=T('Заявка, школьный допуск, приглашение и квота семьи не подтверждены; согласия и платежи не оформлялись.',
                                   'Solicitud, admisión escolar, invitación y cupo familiar sin confirmar; sin aceptar consentimientos ni efectuar pagos.')
        base_note=NOTEBOOK+' '+SCHOOL
        if group=='state':
            e['admission_kind']='invitation'
            e['entry']=T('Invitational для команд Chihuahua: сначала приглашение, затем команда и турнир. ',
                         'Invitational para equipos de Chihuahua: primero invitación, después equipo y torneo. ')+SCHOOL
            e['note']=base_note+' '+T('Payment Deadline на странице ошибочно указывает январь 2026 при турнире января 2027. В календаре сохранён срок Registration Deadline 2027; оплату по старому году не планировать.',
                'Payment Deadline de página señala enero de 2026 erróneamente para torneo de enero de 2027. Calendario conserva Registration Deadline de 2027; sin planificar pago con año antiguo.')
            e['cost']=T('Портал и местные Bases показывают отсутствие взноса Robótica Móvil; приглашение и итоговые обязательные расходы подтвердить. ',
                        'Portal y Bases locales indican ausencia de cuota Robótica Móvil; confirmar invitación y gastos obligatorios finales. ')+SUBSIDY
        else:
            call=CALLS[group]
            e['admission_kind']='open_application'
            ref(e,call,T('Convocatoria сезона · условия участия, мировая квота и тариф',
                          'Convocatoria de temporada · admisión, cupo mundial y tarifa'))
            e['cost']=T('Связанный официальный PDF: Robótica Móvil / VEX Air без регистрационного взноса за событие. Отдельные Robótica Colaborativa / AI & IoT стоят 1000 MXN + IVA; это не цена IQ и не цена VEX AI автоматически. ',
                        'PDF oficial enlazado: Robótica Móvil / VEX Air sin cuota de inscripción del evento. Robótica Colaborativa / AI & IoT aparte cuestan 1000 MXN + IVA; no es precio IQ ni automáticamente de VEX AI. ')+SUBSIDY
            e['note']=base_note+' '+WORLD
            e['reward']=T('Местные награды только по официальному результату. ',
                          'Premios locales solo según resultado oficial. ')+WORLD
            e['action']=QUESTION
            if group=='national':
                e['note']+=' '+T('Название и первая страница связанного National PDF ещё печатают 2026; внутри указаны чемпионаты 2026–2027, а действующая карточка VEX Events даёт 3–5 марта 2027. Даты берём из текущей карточки, редакцию PDF и тариф именно 2027 до поездки перепроверить.',
                    'Título y primera página del National PDF enlazado aún imprimen 2026; dentro figuran campeonatos 2026–2027 y ficha vigente VEX Events da 3–5 de marzo de 2027. Fechas de ficha actual; comprobar edición del PDF y tarifa específica de 2027 antes del viaje.')
            if group=='international':
                e['note']+=' '+T('В Payment Deadline ещё стоит январь 2026; подтверждённый Registration Deadline относится к январю 2027. Заголовок International и общий текст с названием National расходятся; квоту Signature / Worlds по одному заголовку не выводим.',
                    'Payment Deadline aún indica enero de 2026; Registration Deadline confirmado corresponde a enero de 2027. Encabezado International y texto general que dice National discrepan; sin deducir cupo Signature / Worlds solo de encabezado.')
        if iq and ident!='C337':
            e['mat']=T('Условно: нужен состав минимум 3, подтверждённый школьный уровень и допуск команды. Одного возраста и мексиканского паспорта недостаточно.',
                       'Condicional: requiere mínimo de 3 integrantes, nivel escolar acreditado y admisión de equipo. Edad y pasaporte mexicano no bastan.')
            e['osc']=e['mat']
        ref(e,MOBILE,T('Bases Robótica Móvil 2026–2027 · минимум состава, школьный статус и notebook',
                       'Bases Robótica Móvil 2026–2027 · mínimo de integrantes, matrícula y notebook'))
        ref(e,POLICY,T('Глобальная Student Eligibility Policy · обновление 27 октября 2026',
                       'Student Eligibility Policy global · actualización del 27 de octubre de 2026'))
    e=rows['C337']
    e.update(mat=T('Нет: действующая convocatoria допускает только женские команды.',
                  'No: convocatoria vigente admite solo equipos femeninos.'),
             osc=T('Нет: действующая convocatoria допускает только женские команды.',
                   'No: convocatoria vigente admite solo equipos femeninos.'),
             priority='P4 — '+T('только женские команды','solo equipos femeninos'),
             age=T('IQ Elementary по возрасту; дополнительно только женская команда. Раздел 2 convocatoria прямо устанавливает пол состава.',
                   'IQ Elementary por edad; además equipo exclusivamente femenino. Sección 2 de convocatoria establece expresamente composición por género.'))
    e['entry']=T('Для братьев этот выпуск не подходит: convocatoria прямо исключает мужской и смешанный состав. Сохранено как часть мирового календаря; поиск другой подходящей IQ-площадки.',
                 'Esta edición no es adecuada para hermanos: convocatoria excluye expresamente equipos masculinos y mixtos. Conservada en calendario mundial; buscar otro recinto IQ adecuado.')

    e=rows['C024']
    e.update(checked=CHECKED,team_min=2,
        proof=T('Повторно прочитана глобальная Student Eligibility Policy с обновлением 27 октября 2026: IQ Elementary максимум 12 на 1 июня 2027, глобальный состав 2+. Местные мексиканские Bases отдельно требуют 3.',
                'Releída Student Eligibility Policy global actualizada el 27 de octubre de 2026: IQ Elementary máximo 12 al 1 de junio de 2027, equipo global de 2+. Bases mexicanas locales exigen 3 aparte.'))
    marker=T('Мексика 2026/27: ', 'México 2026/27: ')
    e['note']=e['note'].split(marker)[0].rstrip()+' '+marker+TEAM_IQ+' '+WORLD
    ref(e,POLICY,T('Глобальные возраст и состав; AI / AIR теперь от 14',
                   'Edad e integrantes globales; AI / AIR ahora desde 14'))
    ref(e,MOBILE,T('Мексика · локальное правило строже глобальных 2+',
                   'México · regla local más estricta que mínimo global de 2+'))

    p=next(p for p in d['league_guide']['profiles'] if p['id']=='vex')
    # Official event cards already in the atlas must also appear in the league
    # filter. Indexing their existing source URLs does not refresh their dates.
    linked=set(p['event_ids'])
    p['event_ids'] += [e['id'] for e in d['events'] if e['block']=='Соревнования'
                      and e['source'].startswith('https://events.vex.com/robot-competitions/')
                      and e['id'] not in linked]
    p['age_summary']=T('IQ Elementary ≤12 / Middle ≤15; V5 ≤19; VEX U — после школы; AI / AIR от 14',
                       'IQ Elementary ≤12 / Middle ≤15; V5 ≤19; VEX U — después de secundaria; AI / AIR desde 14')
    p['categories']=[c for c in p['categories'] if c['name']!='VEX AIR']
    ai=next(c for c in p['categories'] if c['name']=='VEX AI')
    ai.update(age=T('От 14 лет; до и включая post-secondary', 'Desde 14 años; hasta e incluyendo post-secondary'),
              age_rule=T('По фактическому дню рождения, не на 1 июня окончания сезона.',
                         'Según fecha de nacimiento real, no al 1 de junio de fin de temporada.'),
              entry=T('Матвей и Оскар младше 14; это будущий трек. Локальный образовательный статус и турнир отдельно.',
                      'Matvey y Oscar menores de 14; programa futuro. Situación educativa local y torneo aparte.'))
    p['categories'].append(dict(name='VEX AIR',age=ai['age'],team=T('От 1 ученика','Desde 1 alumno'),
        hardware=T('Дрон и оснащение по действующему AIR manual; это отдельная программа, не IQ.',
                   'Dron y equipo según AIR manual vigente; programa separado, no IQ.'),age_rule=ai['age_rule'],entry=ai['entry']))
    p['nuances']=[n for n in p['nuances'] if not n.startswith('v153 · ')]
    p['nuances'] += ['v153 · '+TEAM_IQ,'v153 · '+WORLD,'v153 · '+T('Политика от 27 октября 2026: VEX AI и AIR минимум 14 по фактическому дню рождения. Для IQ / V5 возраст по-прежнему на 1 июня года окончания сезона.',
        'Política del 27 de octubre de 2026: VEX AI y AIR mínimo de 14 según nacimiento real. IQ / V5 siguen usando edad al 1 de junio del año en que termina temporada.')]
    p['requirements']=[s for s in p['requirements'] if not s.startswith('v153 · ')]+['v153 · '+NOTEBOOK]
    p['sources']=[s for s in p['sources'] if s['url'] not in [POLICY,MOBILE,*CALLS.values()]]
    p['sources'] += [dict(title=label,url=url,checked=CHECKED) for url,label in [
        (POLICY,T('Глобальная политика возраста и команд · 27 октября 2026','Política global de edad y equipos · 27 de octubre de 2026')),
        (MOBILE,T('Мексика · состав и школьные документы','México · integrantes y documentos escolares')),
        (CALLS['girl'],T('Girl Powered · только женские команды','Girl Powered · solo equipos femeninos')),
        (CALLS['international'],T('International · бесплатная mobile-категория и противоречие мировой квоты','International · categoría mobile gratuita y contradicción del cupo mundial')),
        (CALLS['national'],T('National · год обложки расходится с сезоном внутри','National · año de portada discrepa de temporada interior'))]]
    p['checked']=CHECKED
    p['evidence']=T('Обновлены глобальная политика и локальные документы. Глобальные 2+ / местные 3+, право участия и подтверждённая мировая квота показаны раздельно.',
                    'Actualizadas política global y documentos locales. Se distinguen mínimo global de 2+ / local de 3+, derecho a participar y cupo mundial confirmado.')
    for child in ['mat','osc']:
        a=d['family_strategy']['children'][child]['current']
        a[:]=[s for s in a if not s.startswith('VEX México 2026/27:')]
        a.append(T('VEX México 2026/27: братьям нужен третий участник IQ, наставник и подтверждённый школьный маршрут. Girl Powered для них закрыт; до ставки на Worlds получить разъяснение противоречивого обязательного участия. Для подготовки вести notebook и объяснять собственный код; для ближайшего совместного проекта сравнить уже проверенный Infomatrix.',
                   'VEX México 2026/27: hermanos necesitan tercer integrante IQ, mentor y ruta escolar acreditada. Girl Powered no los admite; antes de apostar por Worlds aclarar requisito contradictorio de participación obligatoria. Preparación con notebook y explicación de código propio; para proyecto conjunto próximo comparar Infomatrix ya verificado.'))
    d['family_strategy'].update(version=153,checked=CHECKED)
    sources={s['url']:s for s in d['sources']}
    for item in p['sources']:
        if item['url'] not in [POLICY,MOBILE,*CALLS.values()]:continue
        row=dict(url=item['url'],title=item['title'],checked=CHECKED,evidence=p['evidence'])
        if row['url'] in sources:sources[row['url']].update(row)
        else:d['sources'].append(row);sources[row['url']]=row
