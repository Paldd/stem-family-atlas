"""SOLACYT project and robot routes, current calls and explicit source conflicts."""
from copy import deepcopy
CHECKED='2026-11-05'
SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
IM='https://infomatrix.lat/'
RM='https://robomatrix.org/'
IM_CALL='https://drive.google.com/file/d/1x9HlwJ4FOtPf9cu_bJsSwAPXUdW9jp27/view'
RM_CALL='https://drive.google.com/file/d/10BTty6JLpHxooXhXKXwx7OQOeY6KulVI/view'
SUMO='https://drive.google.com/file/d/1EgxgIEvysRcIzXE7M1a_QAdz3nJbOxlq/view'
CODI='https://drive.google.com/file/d/11Gn3vV5Sjb52os8OHjKJl2UYfVGhXqn_/view'
WER='https://www.wermexico.com/wer2026'
WER_OLD='https://www.wermexico.com/_files/ugd/aa4c42_ac3bc924c15d4833916cda0a469eaa1f.pdf'
WER_SEC='https://www.wermexico.com/_files/ugd/aa4c42_c63f55bc987441a3a131ff600bb36a5c.pdf'
WER_SEN='https://www.wermexico.com/_files/ugd/aa4c42_0468a5fddb0647caa479f5544552eb07.pdf'
IM_AGE=T('Общая convocatoria от 3 ноября 2026: 5–25 лет на закрытие регистрации, preescolar–universidad. Эквивалент класса и местные условия отдельно; в смешанной команде уровень старшего.',
 'Convocatoria general del 3 de noviembre de 2026: 5–25 años al cierre de inscripción, preescolar–universidad. Equivalencia de curso y condiciones locales aparte; equipo mixto compite al nivel del mayor.')
IM_TEAM=T('1–3 ученика + asesor старше 18; допускаются родственник, independent teams, клубы и homeschooling. Разные школы и уровни можно; зачёт по старшему уровню.',
 '1–3 estudiantes + asesor mayor de 18; admite familiar, independent teams, clubes y homeschooling. Puede mezclar escuelas y niveles; clasificación al nivel superior.')
IM_GEAR=T('Собственный проект: робототехника / электроника из kit или открытых деталей, software / videogame либо научный проект. AI допустим как помощь с раскрытием вклада в отчёте. Проект не ранее апреля 2026 либо явно продолжение. Базовый отчёт рекомендован Primaria; выступление до 7 минут.',
 'Proyecto propio: robótica / electrónica con kit o piezas abiertas, software / videogame o proyecto científico. AI permitido como apoyo declarando contribución en informe. Proyecto desde abril de 2026 o continuación explícita. Informe básico recomendado para Primaria; exposición hasta 7 minutos.')
IM_ENTRY=T('Сначала регион по географии команды; иной регион или национальность семьи не дают автоматического доступа. До срока нужны регистрация, подтверждение оплаты и отчёт; затем статус Finalista. Заявка, Finalista, медаль и аккредитация — разные результаты.',
 'Primero sede regional por geografía del equipo; otra sede o nacionalidad familiar no da acceso automático. Antes del plazo requiere registro, comprobante de pago e informe; después estado Finalista. Solicitud, Finalista, medalla y acreditación son resultados distintos.')
IM_COST=T('Таблица México: 450 / 900 / 1350 MXN за проект с 1 / 2 / 3 учениками; asesor без регистрационного взноса. Возможен дополнительный kit fee каждому финалисту и asesor по местной guía. Поездка и проживание отдельно; это не окончательный счёт.',
 'Tabla México: 450 / 900 / 1350 MXN por proyecto de 1 / 2 / 3 alumnos; asesor sin cuota de registro. Posible kit fee adicional por finalista y asesor según guía local. Viaje y alojamiento aparte; no es factura final.')
IM_LANG=T('Испанская convocatoria; научный рассказ разрешён ES / PT / EN, англоязычный фильм с испанскими субтитрами. Это не подтверждает EN / ES защиты каждого проекта на каждой площадке; согласовать выбранную категорию.',
 'Convocatoria española; cuento científico admite ES / PT / EN, película inglesa con subtítulos españoles. No confirma EN / ES de defensa de cada proyecto en cada sede; acordar categoría elegida.')
IM_AWARD=T('Диплом участия всем; диплом места, медаль и аккредитация только по результату. После международного Infomatrix по аккредитации из регионального / национального этапа повторная аккредитация в этом международном событии не выдаётся: цикл проекта завершён.',
 'Diploma de participación para todos; diploma de puesto, medalla y acreditación solo por resultado. Tras Infomatrix internacional acreditado desde regional / nacional no recibe nueva acreditación en ese evento internacional: ciclo del proyecto concluido.')
GENERAL_ACTION=T('Родителям: подтвердить географический вход, класс, язык защиты, наличие мест и полный счёт. Детям: собственный прототип / код, журнал испытаний, отчёт с вкладом каждого. Контакты и заявки не отправлялись.',
 'Padres: confirmar acceso geográfico, curso, idioma de defensa, plazas y factura completa. Niños: prototipo / código propio, registro de pruebas, informe con aportación de cada uno. Sin enviar contactos ni solicitudes.')
RM_TEAM=T('До 2 учеников + совершеннолетний asesor; нужен действующий школьный документ. Разные школы разрешены; смешанные ступени по старшему классу. Каждая категория / робот имеет отдельный регистрационный платёж.',
 'Hasta 2 alumnos + asesor adulto; requiere documento escolar vigente. Permite distintas escuelas; niveles mixtos por curso superior. Cada categoría / robot tiene pago de registro separado.')
RM_AGE=T('По школьной категории текущей таблицы: Primaria / Secundaria / Bachillerato / Universidad; числовой возраст не заменяет класс. Минимум 6 подтверждённых команд для открытия категории; при более 12 возможны деления по уровню.',
 'Según categoría escolar de tabla actual: Primaria / Secundaria / Bachillerato / Universidad; edad numérica no sustituye curso. Mínimo 6 equipos confirmados para abrir categoría; más de 12 permite divisiones por nivel.')
RM_FIT=T('Условно: подтвердить реальный класс и допуск выбранной категории. Для команды из Коста-Рики с гражданством México отдельно согласовать страну команды; гражданство не определяет тариф и аккредитацию автоматически.',
 'Condicional: confirmar curso real y admisión de categoría elegida. Equipo de Costa Rica con nacionalidad México debe acordar país del equipo; nacionalidad no determina tarifa ni acreditación automáticamente.')
RM_COST=T('Continental Junior / Master: 900 MXN для национальной команды или 85 USD для иностранной за зарегистрированный проект, не за каждого ребёнка. Для acreditados — по аккредитации; socio 10% только при подтверждённом статусе. Полная поездка и техника отдельно.',
 'Continental Junior / Master: 900 MXN para equipo nacional o 85 USD extranjero por proyecto registrado, no por cada niño. Acreditados según acreditación; socio 10% solo con estado confirmado. Viaje completo y equipo aparte.')
SUMO_GEAR=T('LEGO автономный: один NXT / EV3 / SPIKE / 15151; все детали LEGO, 15×15 см, до 1 кг. Bluetooth / Wi-Fi выключены, загрузка USB, стартовая задержка 5 с. Алгоритм предъявляется судье по запросу.',
 'LEGO autónomo: un NXT / EV3 / SPIKE / 15151; todas las piezas LEGO, 15×15 cm, hasta 1 kg. Bluetooth / Wi-Fi apagados, carga USB, espera inicial 5 s. Algoritmo se presenta al juez si lo solicita.')

# Latest call gives new-season rows; old page dates are retained separately below.
MEXICO=[
 ('aguascalientes','Aguascalientes / Zacatecas','2027-02-20','2027-02-20','2027-02-05','Aguascalientes · Instituto Tecnológico de Aguascalientes'),
 ('baja-california','Baja California','','','','Mexicali · CEART'),
 ('baja-california-sur','Baja California Sur','2027-02-25','2027-02-27','2027-02-12','La Paz · Universidad Mundial'),
 ('campeche','Campeche','2026-11-27','2026-11-28','2026-11-12','Ciudad del Carmen · Colegio Morelos Lizardi'),
 ('mexico-centro','Centro CDMX / EDOMEX','','','','Ecatepec · Planetario El Gran Ehécatl'),
 ('chihuahua','Chihuahua','2027-03-05','2027-03-06','2027-02-08','Ciudad Juárez · Tec de Monterrey'),
 ('coahuila','Coahuila','2027-03-06','2027-03-06','2027-02-05','Saltillo · Cumbres International School'),
 ('colima','Colima','2027-03-11','2027-03-12','2027-02-25','Manzanillo · Monte Corona'),
 ('golfo','Golfo Norte','2027-03-04','2027-03-05','2027-02-17','Tampico · Universidad Anglo Hispano Mexicana'),
 ('guanajuato','Guanajuato','','','','Guanajuato'),
 ('jalisco','Jalisco','','','','Guadalajara'),
 ('michoacan','Michoacán / Guerrero','2027-03-05','2027-03-05','2027-02-16','Tarímbaro / Morelia · CBTA 233'),
 ('nuevo-leon','Nuevo León','2027-02-26','2027-02-27','2027-02-08','Monterrey · Euroamerican School'),
 ('oaxaca','Oaxaca / Chiapas','2027-04-09','2027-04-10','2027-03-18','Oaxaca · Instituto Blaise Pascal'),
 ('pacifico','Pacífico','2027-03-04','2027-03-06','2026-12-18','Mazatlán · Polideportivo Zona Sur UAS'),
 ('puebla','Puebla','','','','Puebla'),('queretaro','Querétaro','','','','Querétaro'),
 ('quintana-roo','Quintana Roo','2027-02-25','2027-02-26','2027-02-09','Cancún · Colegio St John’s'),
 ('san-luis','San Luis Potosí','','','','San Luis Potosí'),
 ('sonora','Sonora','2027-03-04','2027-03-04','2027-02-15','Hermosillo · Instituto Vanguardia'),
 ('tabasco','Tabasco','','','','Villahermosa'),
 ('golfo-sur','Veracruz Sur','2026-12-11','2026-12-11','2026-11-23','Minatitlán · CBTIS 213'),
 ('yucatan','Yucatán','2027-02-18','2027-02-19','2027-01-29','Mérida · Preparatoria CELA')]
LATAM=[
 ('ecuador','Ecuador','ECU','2027-02-24','2027-02-27','2027-01-29','Quito · Arena UDLA'),
 ('infomatrix-regional-guayaquil','Guayaquil','ECU','2027-01-08','2027-01-09','2026-12-14','Guayaquil · UE Torremolinos'),
 ('infomatrix-regional-cuenca','Cuenca','ECU','','','','Cuenca · Universidad Católica'),
 ('infomatrix-regional-manabi','Manabí','ECU','','','','Portoviejo · UE Jean Piaget'),
 ('santo-domingo','Santo Domingo','ECU','2026-10-15','2026-10-15','2026-09-26','Santo Domingo · UE Cavanis'),
 ('colombia','Colombia','COL','2026-11-11','2026-11-13','2026-10-28','Bogotá · Colegio El Minuto de Dios'),
 ('bolivia','Bolivia','BOL','','','','La Paz · sede TBD'),
 ('cochabamba','Cochabamba','BOL','2026-07-18','2026-07-19','2026-07-01','Cochabamba · Colegio San Agustín'),
 ('santa-cruz','Santa Cruz','BOL','2026-11-06','2026-11-07','2026-10-24','Santa Cruz · UNIVALLE'),
 ('brasil','Brasil','BRA','2026-09-15','2026-09-18','2026-07-31','Florianópolis · UNISUL'),
 ('nacional-chile','Chile','CHL','2026-09-04','2026-09-06','2026-08-06','Chillán · Colegio Alturas'),
 ('nacional-argentina','Argentina','ARG','2026-10-08','2026-10-10','2026-09-18','Realicó · Gimnasio Dorita Lucesoli'),
 ('infomatrix-sudamerica-peru','Perú','PER','','','','Lima · sede TBD'),
 ('costa-rica','Costa Rica','CRI','2026-10-10','2026-10-10','2026-09-17','San José · CEDES Don Bosco')]
ROBOTS=[
 ('continental','Continental Master','MEX','2026-12-04','2026-12-05','2026-11-12','León · Universidad Iberoamericana'),
 ('sede-continental-junior-xalapa-mexico','Continental Junior','MEX','2026-11-27','2026-11-28','2026-11-06','Xalapa · Colegio Las Hayas'),
 ('tijuana','Baja California','MEX','2026-10-31','2026-10-31','2026-10-12','Tijuana · Museo El Trompo'),
 ('guadalajara','Occidente','MEX','2026-07-01','2026-07-01','','Guadalajara · UNITEC'),
 ('regional-puebla','Puebla','MEX','2026-06-26','2026-06-26','','San Pedro Zacachimalpa · Puebla'),
 ('oaxaca','Oaxaca','MEX','2026-10-23','2026-10-24','2026-10-06','Oaxaca · Instituto Blaise Pascal'),
 ('sudamerica-argentina','Argentina','ARG','2026-10-10','2026-10-10','2026-09-20','Realicó · Gimnasio Dorita Lucesoli'),
 ('cochabamba','Cochabamba','BOL','2026-06-26','2026-06-27','','Cochabamba · Av. América 1359'),
 ('santa-cruz','Santa Cruz','BOL','2026-11-06','2026-11-07','2026-10-24','Santa Cruz · UNIVALLE'),
 ('sudamerica-chile','Chile','CHL','2026-09-03','2026-09-03','2026-08-18','Chillán · Colegio Alturas'),
 ('sudamerica-ecuador','Ecuador','ECU','2026-03-04','2026-03-07','2026-02-03','Quito'),
 ('guayaquil','Guayaquil','ECU','2026-10-03','2026-10-03','2026-09-18','Guayaquil · UE Mariscal Sucre'),
 ('santo-domingo','Santo Domingo','ECU','2026-10-15','2026-10-15','2026-10-01','Santo Domingo · UE Cavanis'),
 ('costa-rica','Costa Rica','CRI','2026-10-10','2026-10-10','2026-09-20','San José · CEDES Don Bosco')]

def enrich_v149(d):
    countries={c['iso']:c for c in d['countries']};authored=[];by_key={}
    def make(key,title,iso,start,end,deadline,place,url,robot=False):
        eid='C'+str(1208+len(authored));c=countries[iso]
        fit=RM_FIT if robot else T('Да по общему возрасту 5–25; местная категория, регион и приём отдельно. Это не подтверждение регистрации.',
             'Sí por edad general 5–25; categoría local, región y admisión aparte. No confirma registro.')
        row=dict(id=eid,block='Соревнования',title=title,country=c['country'],region=c['region'],city=place,start=start,end=end,deadline=deadline,period='',date_status='Подтверждено' if start else 'Не объявлено',
            age=RM_AGE if robot else IM_AGE,mat=fit,osc=fit,format=RM_TEAM if robot else IM_TEAM,entry=IM_ENTRY,
            gear=T('Категории и модели роботов только по текущей таблице выбранной площадки; Junior не означает допуск ко всем задачам.',
                   'Categorías y robots solo según tabla actual de sede elegida; Junior no admite automáticamente todas las tareas.') if robot else IM_GEAR,
            language=IM_LANG if not robot else T('Правила на ES; язык судейства и общения с командой отдельно подтвердить.','Reglas ES; confirmar idioma del jurado y comunicación con equipo.'),
            languages=[],language_mode='unconfirmed',language_certainty=T('Язык документов не перенесён автоматически на язык защиты / судейства.','Idioma de documentos no se traslada automáticamente a defensa / jurado.'),
            cost=RM_COST if robot else IM_COST,level='C — '+T('проверенная национальная / региональная сеть','red nacional / regional verificada'),reward=IM_AWARD if not robot else T('Диплом участия, место и международная аккредитация различаются; конкретный приз только по протоколу и правилам площадки.','Diploma de participación, puesto y acreditación internacional distintos; premio concreto según acta y reglas de sede.'),
            priority='P2 — '+T('подготовка после проверки входа','preparación tras comprobar admisión'),action=GENERAL_ACTION,source=url,
            references=[dict(url=RM_CALL if robot else IM_CALL,label=T('Текущая общая convocatoria · сверены таблицы','Convocatoria general actual · tablas comprobadas'))],
            proof=T('Проверены текущая официальная страница и связанный PDF; сезон, единицы тарифа и расхождения сохранены.','Comprobados página oficial actual y PDF enlazado; temporada, unidades de tarifa y discrepancias conservadas.'),
            checked=CHECKED,status='Идея',note='',iso=[iso],themes=['robotics'] if robot else ['robotics','coding','games','science','technology'],scope='regional',
            importance_reason=T('Региональная / национальная сеть с международным путём; не универсальный мировой рейтинг.','Red regional / nacional con vía internacional; no clasificación mundial universal.'),
            participation='team',admission_kind='open_application',evidence_level='rules',date_scope='competition')
        if not start:row['registration_status']=T('Дата нового набора не опубликована; архив не подтверждает приём.','Fecha de nueva convocatoria sin publicar; archivo no confirma admisión.')
        elif deadline and deadline<CHECKED:row['registration_status']=T('Опубликованный срок уже прошёл; поздний вход не подтверждён.','Plazo publicado ya vencido; admisión tardía sin confirmar.')
        else:row['registration_status']=T('Наличие дат и формы не подтверждает место семьи.','Fechas y formulario no confirman plaza familiar.')
        authored.append(row);by_key[key]=row;return row
    # Finals and an expressly restricted virtual fallback.
    for key,title,a,b,dead,place,path in [('im-ibero','Infomatrix Iberoamérica 2027','2027-05-19','2027-05-22','2027-04-23','Tijuana · Museo El Trompo','iberoamericana'),('im-national','Infomatrix Nacional México 2027','2027-06-16','2027-06-19','2027-05-21','Oaxaca · Universidad La Salle Oaxaca','nacionalmexico'),('im-virtual','Infomatrix General Virtual 2027','2027-04-09','2027-04-09','2027-03-16','Online','')]:
        e=make(key,title,'MEX',a,b,dead,place,IM+path+'/' if path else IM_CALL)
        e['scope']='international' if key=='im-ibero' else 'national';e['admission_kind']='qualifier'
        e['mat']=e['osc']=T('Условно: возраст возможен, но требуется аккредитация / разрешение именно для этой стадии.','Condicional: edad posible, requiere acreditación / permiso para esta fase concreta.')
        if key=='im-ibero':
            e['entry']=T('Аккредитованные с региональных / партнёрских этапов и приглашённые. В PDF рядом со сроком 23 апреля стоит Registro por Cerrado; страница срока не даёт. Текущий приём и условие для неаккредитованных согласовать.',
                'Acreditados de regionales / afiliados e invitados. PDF junto a plazo 23 de abril indica Registro por Cerrado; página sin plazo. Acordar admisión actual y condición de no acreditados.')
            e['registration_status']=T('Статус источника противоречив; не объявлен открытым набором.','Estado de fuente contradictorio; no se declara inscripción abierta.')
        elif key=='im-national':e['entry']=T('Аккредитация региональных Infomatrix или партнёрских ярмарок. Региональные acreditados не создают повторную заявку; для внешних feria нужны регистрация, отчёт и оплата до 21 мая 2027.',
             'Acreditación regional Infomatrix o feria afiliada. Acreditados regionales no crean nueva solicitud; feria externa requiere registro, informe y pago hasta 21 de mayo de 2027.')
        else:
            e['participation']='team';e['date_scope']='judging';e['admission_kind']='invitation';e['priority']='P3 — '+T('только после письменного разрешения','solo tras autorización escrita')
            e['entry']=T('Исключительный виртуальный вход: отсутствие своей площадки либо доказанные проблемы поездки по экономике / здоровью. Требуется отдельное разрешение организатора. Даёт только национальные аккредитации и цифровые награды; это не свободный онлайн-финал для всех.',
                'Acceso virtual excepcional: falta de sede propia o dificultades económicas / de salud acreditadas para viajar. Requiere autorización del organizador. Solo acreditaciones nacionales y premios digitales; no final online libre para todos.')
        e['deadline_note']=T('Год срока взят из блока этого события в текущем PDF; точный час не указан.','Año del plazo tomado del bloque de este evento en PDF actual; hora exacta no indicada.')
    for slug,label,a,b,dead,place in MEXICO:
        e=make('im-'+slug,'Infomatrix · '+label+(' · '+a[:4] if a else ' · '+T('следующий набор','próxima convocatoria')),'MEX',a,b,dead,place,IM+slug+'/')
        e['entry']+= ' '+T('Площадка относится к указанному штату / региону; проживание в Коста-Рике и мексиканский паспорт не заменяют географическое разрешение.',
            'Sede corresponde al estado / región indicado; vivir en Costa Rica y pasaporte mexicano no sustituye permiso geográfico.')
        if slug=='mexico-centro':
            e['date_status']='Спорные';e['planned_windows']=[dict(start='2027-02-05',end='2027-02-06',source=e['source']),dict(start='2027-03-05',end='2027-03-06',source=IM_CALL)]
            e['note']=T('Страница: 5–6 февраля 2027 и срок 8 февраля 2026; PDF: 5–6 марта 2027 и 8 февраля. Дату и срок не исправляли догадкой; подтверждённый календарь пока без этого этапа.',
                'Página: 5–6 de febrero de 2027 y plazo 8 de febrero de 2026; PDF: 5–6 de marzo de 2027 y 8 de febrero. Sin corregir fecha / plazo por suposición; fuera del calendario confirmado.')
        if slug=='yucatan':e['deadline_note']=T('Страница даёт 29 января 2027, PDF — 1 февраля в блоке 2027. Для планирования сохранён более ранний опубликованный срок; подтверждение организатора ещё нужно.',
             'Página indica 29 de enero de 2027, PDF 1 de febrero en bloque 2027. Para planificar se conserva plazo publicado anterior; aún requiere confirmación del organizador.')
        if slug in ['nuevo-leon','oaxaca','sonora']:
            e['note']=T('Дата и год нового сезона по общей convocatoria 2027; отдельная страница может быть старой или не повторять год срока. Источники не объявлены полностью согласованными.',
                'Fecha y año de nueva temporada según convocatoria general 2027; página específica puede ser anterior o no repetir año del plazo. Fuentes no se declaran totalmente concordantes.')
        if slug=='michoacan':e['note']=T('CBTA 233 совпадает, но страница называет Tarímbaro, PDF Morelia. Точный адрес подтвердить.','CBTA 233 coincide, página indica Tarímbaro y PDF Morelia. Confirmar dirección exacta.')
    for slug,label,iso,a,b,dead,place in LATAM:
        e=make('im-'+slug,'Infomatrix · '+label+(' · '+a[:4] if a else ' · '+T('следующий набор','próxima convocatoria')),iso,a,b,dead,place,IM+slug+'/')
        e['scope']='national' if slug in ['ecuador','colombia','bolivia','brasil','nacional-chile','nacional-argentina','infomatrix-sudamerica-peru','costa-rica'] else 'regional'
        e['entry']+= ' '+T('Иностранным командам национальные страницы обычно требуют acreditación; местный open не переносится на приезжую семью.',
             'Páginas nacionales suelen exigir acreditación a extranjeros; open local no se traslada a familia visitante.')
        e['mat']=e['osc']=T('Условно по общей рамке 5–25; местная редакция, эквивалент класса и иностранная аккредитация отдельно.','Condicional por marco general 5–25; edición local, equivalencia de curso y acreditación extranjera aparte.')
        e['cost']=T('Тариф своей страны / иностранного проекта — по таблице текущего PDF; 90 USD у ряда национальных площадок относится к проекту с 1–3 детьми. Не переносить мексиканские 450 MXN на другие страны; kit fee и поездка отдельно.',
             'Tarifa del país / proyecto extranjero según tabla PDF actual; 90 USD de varias sedes nacionales es por proyecto de 1–3 niños. No trasladar 450 MXN mexicanos a otros países; kit fee y viaje aparte.')
        if slug=='infomatrix-regional-manabi':
            e['date_status']='Спорные';e['planned_windows']=[dict(start='2026-12-04',end='2026-12-04',source=IM_CALL),dict(start='2027-12-04',end='2027-12-04',source=e['source'])]
            e['note']=T('PDF: 4 декабря 2026, срок 16 ноября 2026; страница: 4 декабря 2027 без срока. Ни один год не объявлен бесспорным; в ICS не добавлен.',
                'PDF: 4 de diciembre de 2026, plazo 16 de noviembre de 2026; página: 4 de diciembre de 2027 sin plazo. Ningún año se declara inequívoco; no añadido a ICS.')
        if slug=='ecuador':e['deadline_note']=T('Страница: 29 января 2027; PDF: 1 февраля. Для планирования сохранён ранний срок страницы; конфликт требует подтверждения.',
             'Página: 29 de enero de 2027; PDF: 1 de febrero. Se conserva plazo anterior de página para planificar; discrepancia requiere confirmación.')
        if slug=='costa-rica':e['deadline_note']=T('Страница: 17 сентября 2026; PDF: 19 сентября. Оба срока прошли; нового набора 2027 нет.','Página: 17 de septiembre de 2026; PDF: 19 de septiembre. Ambos vencidos; sin nueva convocatoria 2027.')
        if slug=='brasil':e['deadline_note']=T('Страница: 31 июля; общий PDF: 20 августа 2026. Использован ранний срок страницы; архивный набор, не места 2027.','Página: 31 de julio; PDF general: 20 de agosto de 2026. Plazo anterior de página; convocatoria archivada, no plazas 2027.')
        if slug=='nacional-chile':e['note']=T('Страница даёт 4–6 сентября и срок 6 августа; PDF 4–5 сентября и 16 августа 2026. Сохранён датированный архив страницы с явным расхождением, не будущий сезон.',
             'Página indica 4–6 de septiembre y plazo 6 de agosto; PDF 4–5 de septiembre y 16 de agosto de 2026. Archivo fechado de página con discrepancia explícita, no temporada futura.')
        if slug=='infomatrix-sudamerica-peru':e['note']=T('Отдельная страница всё ещё 29–31 октября 2025, PDF будущих дат не даёт и помечает Registro Cerrado; 2027 не выдуман.','Página específica aún 29–31 de octubre de 2025, PDF sin fechas futuras e indica Registro Cerrado; 2027 no inventado.')
    for slug,label,iso,a,b,dead,place in ROBOTS:
        url=RM_CALL if slug=='costa-rica' else RM+slug+'/'
        e=make('rm-'+slug,'Robomatrix · '+label+' · 2026',iso,a,b,dead,place,url,True)
        e['entry']=T('Сначала выбрать школьную дисциплину и страну команды. До срока зарегистрировать робота, оплатить и подтвердить платёж; окончательный статус Finalista проверяется отдельно. Для иностранцев Continental требуется аккредитация, открытый вход всем мексиканским командам не равен открытому входу всем иностранцам.',
             'Primero elegir disciplina escolar y país del equipo. Antes del plazo registrar robot, pagar y confirmar comprobante; estado final Finalista se verifica aparte. Continental exige acreditación a extranjeros; open para equipos mexicanos no equivale a open para todos los extranjeros.')
        e['scope']='international' if slug in ['continental','sede-continental-junior-xalapa-mexico'] else 'regional'
        if slug=='continental':e['mat']=e['osc']=T('Нет по требуемой ступени Preparatoria / Universidad; Junior — другой этап.','No por nivel requerido Preparatoria / Universidad; Junior es otra fase.');e['priority']='P4 — '+T('будущая ступень','nivel futuro')
        if slug=='sede-continental-junior-xalapa-mexico':e['priority']='P1 — '+T('срок 6 ноября · класс и страна команды отдельно','plazo 6 de noviembre · curso y país del equipo aparte')
        if 'continental' not in slug:
            e['cost']=T('Таблица 2026 за проект: México regional 650 MXN; Costa Rica 21600 CRC национальный / 90 USD иностранный; Santa Cruz 105 BOB; Ecuador / Argentina 35 USD местный. NA для иностранцев не означает бесплатное участие; действующий местный пакет отдельно.',
                'Tabla 2026 por proyecto: México regional 650 MXN; Costa Rica 21600 CRC nacional / 90 USD extranjero; Santa Cruz 105 BOB; Ecuador / Argentina 35 USD local. NA extranjero no significa participación gratis; paquete local vigente aparte.')
    parent=by_key['rm-sede-continental-junior-xalapa-mexico']
    parent['deadline_note']=T('6 ноября 2026 — общий срок регистрации и подтверждения оплаты; точный час и часовой пояс не указаны. Свободное место или поздний вход не подтверждены.',
        '6 de noviembre de 2026 — plazo común de registro y confirmación del pago; hora y zona horaria exactas no indicadas. Plaza libre o admisión tardía sin confirmar.')
    for key,name,grade,gear in [
        ('sumo','Sumo LEGO',T('Primaria / Secundaria / Bachillerato; обоим нужен подтверждённый класс Primaria.','Primaria / Secundaria / Bachillerato; ambos requieren curso Primaria confirmado.'),SUMO_GEAR),
        ('codi','Codi-Bot',T('Последний дошкольный год либо Primaria 1–3 по специальному регламенту. Общий заголовок Junior говорит Primaria–Preparatoria: дошкольный вход подтвердить. Матвею особенно проверить, не старше ли 3 класса.',
             'Último curso preescolar o Primaria 1–3 según reglamento específico. Título general Junior indica Primaria–Preparatoria: confirmar admisión preescolar. Matvey debe comprobar especialmente no superar 3er curso.'),
          T('Bee-Bot, Andy или аналог с кнопками: шаг 15 см, поворот 90°. До 2 учеников; каждый хотя бы раз программирует. Родители и coach не вмешиваются, трасса меняется на каждом событии.',
             'Bee-Bot, Andy o similar con botones: paso 15 cm, giro 90°. Hasta 2 alumnos; cada uno programa al menos una vez. Padres y coach no intervienen, pista cambia en cada evento.')),
        ('line-kits','Seguidor de Líneas Kits',T('Primaria / Secundaria / Bachillerato по таблице Junior; класс обоих подтвердить.','Primaria / Secundaria / Bachillerato según tabla Junior; confirmar curso de ambos.'),
          T('Таблица допускает kit Mbot / LEGO / VEX / Zmrobot. Размеры, датчики и версия частного регламента выбранного kit ещё требуют сверки; это не открытая аппаратная категория.',
             'Tabla admite kit Mbot / LEGO / VEX / Zmrobot. Dimensiones, sensores y edición del reglamento de kit elegido aún por comprobar; no categoría de hardware abierto.'))]:
        e=make('rm-junior-'+key,'Robomatrix Junior Xalapa · '+name,'MEX',parent['start'],parent['end'],parent['deadline'],parent['city'],SUMO if key=='sumo' else CODI if key=='codi' else RM_CALL,True)
        e.update(age=grade,gear=gear,entry=parent['entry'],cost=RM_COST,parent_event_id=parent['id'],scope='international',priority=parent['priority'])
        e['deadline_note']=parent['deadline_note']
        parent.setdefault('related_ids',[]).append(e['id'])
    for level,url,deadline,team in [('Secundaria',WER_SEC,'2026-10-09',3),('Bachillerato / Universidad',WER_SEN,'2026-10-02',None)]:
        e=make('wer-'+level,'WER México 2026 · '+level,'MEX','2026-11-04','2026-11-05',deadline,'Aguascalientes · Tec de Monterrey · Duela LiFE',url,True)
        e.update(age=T('Требуется школьная ступень ','Requiere nivel escolar ')+level,mat=T('Нет по требуемой школьной ступени; будущий трек.','No por nivel escolar requerido; itinerario futuro.'),osc=T('Нет по требуемой школьной ступени; будущий трек.','No por nivel escolar requerido; itinerario futuro.'),
            format=T('3 ученика + docente coach; Secondary максимум 15 лет.','3 alumnos + docente coach; Secondary máximo 15 años.') if team else T('2–3 ученика + docente coach; отдельные beginner / master условия возраста и опыта.','2–3 alumnos + docente coach; condiciones separadas de edad y experiencia beginner / master.'),
            gear=T('Abilix Krypton и арена WER 2026 по собственной категории; старый Oculus 5 из Primaria 2019 не переносится.','Abilix Krypton y arena WER 2026 según categoría propia; Oculus 5 de Primaria 2019 no se traslada.'),
            cost=T('Текущий пакет и цена не найдены в convocatoria; призовые льготы мирового этапа различаются по категории и не относятся к младшим детям.',
                'Paquete y precio actual no encontrados en convocatoria; beneficios de premio mundial varían por categoría y no aplican a menores.'),
            entry=T('Набор национального финала 2026 закрыт по опубликованному сроку. Это конкретные старшие категории, а не текущий набор Primaria.',
                'Inscripción a final nacional 2026 cerrada según plazo publicado. Categorías mayores concretas, no convocatoria Primaria actual.'),priority='P4 — '+T('будущая ступень','nivel futuro'),scope='national')
        e['references']=[dict(url=WER,label=T('Текущая страница WER 2026','Página actual WER 2026'))]
    # Upsert only our new stable rows; all earlier rows retain their identifiers.
    index={e['id']:e for e in authored};previous_ids={e['id'] for e in d['events']}
    d['events']=[index.get(e['id'],e) for e in d['events']]+[e for e in authored if e['id'] not in previous_ids]
    old={e['id']:e for e in d['events']}
    old['C044'].update(title=T('WER México · Primaria · новый набор не подтверждён','WER México · Primaria · nueva convocatoria sin confirmar'),checked=CHECKED,format=RM_TEAM,
        participation='team',languages=[],language_mode='unconfirmed',age=T('Ссылка Primaria ведёт на convocatoria 2019: 9–15 и действующий класс Primaria. Это архив, не текущий допуск 2026/27. Новые convocatoria 2026 относятся к Secundaria / Bachillerato / Universidad.',
         'Enlace Primaria lleva a convocatoria 2019: 9–15 y curso Primaria vigente. Archivo, no admisión actual 2026/27. Nuevas convocatoria 2026 son Secundaria / Bachillerato / Universidad.'),
        mat=T('Условно: новый Primaria набор и возраст не подтверждены.','Condicional: nueva convocatoria Primaria y edad sin confirmar.'),osc=T('Условно: младший набор не объявлен; архив 2019 с 9 лет не применён как правило нового сезона.',
         'Condicional: convocatoria menor sin anunciar; archivo 2019 desde 9 no aplicado como regla de nueva temporada.'),
        format_rule=T('Текущие WER-команды не индивидуальные; состав 3 или 2–3 зависит от старшей категории. Primaria 2019: 3. Для нового младшего набора требуется новая редакция.',
         'Equipos WER actuales no individuales; 3 o 2–3 según categoría mayor. Primaria 2019: 3. Nueva convocatoria menor requiere edición nueva.'),
        proof=T('Визуально сверены старый Primaria PDF 2019 и отдельные официальные convocatoria 2026; общий пункт меню не доказывает наличие категории в новом финале.',
         'Comprobados visualmente PDF Primaria 2019 y convocatoria oficiales separadas 2026; menú general no acredita categoría en final nuevo.'),source=WER,
        note=T('Фраза INSCRIPCIONES ABIERTAS на главной не отменяет прошедшие сроки 2 / 9 октября. Пакеты наград и финансирование Китая из разных лет / категорий не смешаны.',
         'INSCRIPCIONES ABIERTAS en portada no invalida plazos vencidos 2 / 9 de octubre. Premios y financiación China de distintos años / categorías no mezclados.'))
    old['C044']['format']=old['C044']['format_rule'];old['C044']['references']=[dict(url=u,label=T('Проверенная редакция правил','Edición de reglas comprobada')) for u in [WER_OLD,WER_SEC,WER_SEN]]
    old['C045'].update(checked=CHECKED,age=T('Infomatrix 5–25, до 3 учеников; Robomatrix до 2 и школьные категории. Это разные конкурсы одной сети.',
         'Infomatrix 5–25, hasta 3 alumnos; Robomatrix hasta 2 y categorías escolares. Concursos distintos de una red.'),entry=T('Выбрать проектный Infomatrix или робототехнический Robomatrix; текущие региональные и финальные стадии вынесены отдельно. География, иностранная аккредитация и право следующего этапа проверяются до оплаты.',
         'Elegir Infomatrix de proyectos o Robomatrix de robots; fases regionales y finales actuales separadas. Geografía, acreditación extranjera y derecho de siguiente fase se comprueban antes de pago.'),
         proof=T('Сверены текущие сети площадок, Infomatrix convocatoria от 3 ноября и Robomatrix от 16 октября 2026. Различия дат и правил сохранены.',
         'Comprobadas redes actuales de sedes, convocatoria Infomatrix de 3 de noviembre y Robomatrix de 16 de octubre de 2026. Discrepancias de fechas y reglas conservadas.'),note=T('Текущие международные аккредитации не являются гарантией допуска семьи и не равны победе мирового финала.','Acreditaciones internacionales actuales no garantizan admisión familiar ni equivalen a victoria en final mundial.'))
    old['C002'].update(checked=CHECKED,entry=T('Официальный Infomatrix Costa Rica даёт только завершённый этап 10 октября 2026 в CEDES Don Bosco; будущая LUVÁ 2027 не объявлена. Для международного пути выбрать конкретную аккредитацию и категорию.',
         'Infomatrix Costa Rica oficial solo indica fase finalizada el 10 de octubre de 2026 en CEDES Don Bosco; futura LUVÁ 2027 sin anunciar. Para vía internacional elegir acreditación y categoría concreta.'),
         proof=T('Прямая LUVÁ-страница сейчас отдаёт короткую оболочку; старый поисковый снимок не объявлен текущим набором. Дата прошедшего этапа подтверждена официальной сетью.',
         'Página LUVÁ directa devuelve ahora estructura breve; captura de búsqueda antigua no se declara convocatoria actual. Fecha de fase pasada confirmada por red oficial.'))
    old['C080'].update(start='2026-10-28',end='2026-10-28',city='Panamá · Parque Tecnológico Ciudad del Saber',date_status='Подтверждено',checked=CHECKED,
         period=T('Опубликованный очный этап 28 октября 2026 уже прошёл; следующая дата неизвестна.','Fase presencial publicada de 28 de octubre de 2026 ya pasada; próxima fecha desconocida.'),
         mat=T('Условно по возрасту: в 2026 Матвею 8–9; Game Fest требует уже 9. До дня рождения возможная другая категория отдельно.',
         'Condicional por edad: en 2026 Matvey tiene 8–9; Game Fest requiere 9 cumplidos. Antes de cumpleaños posible otra categoría aparte.'),
         osc=T('Условно: Artifact 6–8 только после 6-летия; в 2026 возраст 5–6.','Condicional: Artifact 6–8 solo tras cumplir 6; en 2026 edad 5–6.'),
         languages=[],language_mode='unconfirmed',registration_status=T('Этап завершён; новый приём не объявлен.','Fase finalizada; admisión nueva sin anunciar.'),
         proof=T('Текущая официальная страница прямо называет Panamá 28 октября 2026 и Ciudad del Saber; заголовок сезона 2026–2027 не делает его будущим событием.',
         'Página oficial actual indica Panamá 28 de octubre de 2026 y Ciudad del Saber; título de temporada 2026–2027 no lo convierte en evento futuro.'))
    old['C081'].update(checked=CHECKED,title=T('TecPro Colombia · следующий очный набор не подтверждён','TecPro Colombia · próxima convocatoria presencial sin confirmar'),city='',period=T('Текущий список очных площадок не содержит дат Colombia; отсутствие строки не доказательство отмены.',
         'Lista actual de sedes presenciales sin fechas Colombia; ausencia no prueba cancelación.'),languages=[],language_mode='unconfirmed',mat=old['C080']['mat'],osc=old['C080']['osc'],
         proof=T('Повторно прочитаны текущая страница и очный регламент; 2027 или Bogotá не добавлены догадкой.','Releídos página actual y reglamento presencial; 2027 o Bogotá no añadidos por suposición.'))
    # Sources are current per entry; unrelated league and camp dates are untouched.
    srcs={s['url']:s for s in d['sources']}
    for e in authored+[old[i] for i in ['C002','C044','C045','C080','C081']]:
        for s in [dict(url=e['source'],title=e['title']),*e.get('references',[])]:
            url=s['url'];srcs[url]=dict(url=url,title=s.get('label',s.get('title','')),checked=CHECKED,evidence=T('Текущая официальная страница или связанный PDF; границы проверки в карточке.','Página oficial actual o PDF enlazado; alcance de comprobación en ficha.'))
    d['sources']=list(srcs.values());d['asof']=max(d['asof'],CHECKED)
    def profile(pid,name,events,robot=False):
        chosen=[by_key[k] for k in events];return dict(id=pid,name=name,group='international',age_summary=RM_AGE if robot else IM_AGE,age_tags=['6','9','10-12','teen','university'],summary=RM_TEAM if robot else IM_TEAM,
            categories=[dict(name=e['title'],age=e['age'],age_rule=e['age'],team=e['format'],hardware=e['gear'],event_id=e['id'],entry=e['entry'],language=e['language'],note=e['note'],source=e['source'],checked=CHECKED) for e in chosen],
            event_ids=[e['id'] for e in authored if e['title'].startswith('Robomatrix' if robot else 'Infomatrix')],legacy_ids=['C045'],route=chosen[0]['entry'],hardware=SUMO_GEAR if robot else IM_GEAR,
            language=chosen[0]['language'],importance=T('Доказанный региональный / международный путь; награды конкретного этапа, а не общий мировой титул.','Vía regional / internacional acreditada; premios de fase concreta, no título mundial general.'),
            strengths=RM_TEAM if robot else IM_TEAM,requirements=[RM_TEAM,RM_AGE] if robot else [IM_TEAM,IM_ENTRY,IM_GEAR],nuances=[RM_FIT,RM_COST] if robot else [IM_AWARD,IM_LANG],cost=RM_COST if robot else IM_COST,
            award=chosen[0]['reward'],sources=[dict(title=T('Текущая convocatoria','Convocatoria actual'),url=RM_CALL if robot else IM_CALL,checked=CHECKED)],evidence=T('Повторно сверены правила и все текущие страницы сети; неизвестные и спорные поля не признаны подтверждёнными.',
             'Recomprobados reglas y todas las páginas actuales de red; campos desconocidos y discutidos no declarados confirmados.'))
    newprofiles=[profile('infomatrix-solacyt','Infomatrix · SOLACYT · proyectos',['im-quintana-roo','im-national','im-ibero','im-virtual']),profile('robomatrix','Robomatrix · Junior / Master',['rm-junior-sumo','rm-junior-codi','rm-junior-line-kits','rm-continental'],True)]
    guides={p['id']:p for p in d['league_guide']['profiles']}
    for p in newprofiles:guides[p['id']]=p
    guides['matrix'].update(age_summary=old['C045']['age'],route=old['C045']['entry'],summary=old['C045']['proof'],nuances=[old['C045']['note']],event_ids=['C045','C002']+[e['id'] for e in authored if not e['title'].startswith('WER')])
    guides['matrix']['categories']=[dict(name=old['C045']['title'],age=old['C045']['age'],age_rule=old['C045']['age'],team=T('Infomatrix до 3 / Robomatrix до 2 + взрослый asesor','Infomatrix hasta 3 / Robomatrix hasta 2 + asesor adulto'),hardware=old['C045']['gear'],event_id='C045',entry=old['C045']['entry'],language=old['C045']['language'],note=old['C045']['note'],source=RM_CALL,checked=CHECKED)]
    guides['wer'].update(age_summary=old['C044']['age'],route=old['C044']['entry'],nuances=[old['C044']['note']],hardware=by_key['wer-Secundaria']['gear'])
    guides['wer']['categories']=[dict(name=e['title'],age=e['age'],age_rule=e['age'],team=e['format'],hardware=e['gear'],event_id=e['id'],entry=e['entry'],language=e['language'],note=e['note'],source=e['source'],checked=CHECKED) for e in [old['C044'],*[by_key[k] for k in ['wer-Secundaria','wer-Bachillerato / Universidad']]]]
    guides['wer']['event_ids']=['C044',by_key['wer-Secundaria']['id'],by_key['wer-Bachillerato / Universidad']['id']]
    guides['tecpro']['nuances']=list(dict.fromkeys(guides['tecpro']['nuances']+[old['C080']['period'],old['C081']['period']]))
    for c in guides['tecpro']['categories']:
        if c.get('event_id') in ['C080','C081']:
            e=old[c['event_id']]
            for target,key in [('entry','entry'),('note','period'),('checked','checked')]:c[target]=e[key]
    for pid,urls in [('matrix',[IM_CALL,RM_CALL]),('wer',[WER,WER_OLD,WER_SEC,WER_SEN]),('tecpro',['https://www.tdrobotica.co/tecpro-challenge-2026-2027'])]:
        sources={s['url']:s for s in guides[pid]['sources']}
        for u in urls:sources[u]=dict(url=u,title=T('Проверенный текущий источник / явно отмеченный архив','Fuente actual verificada / archivo señalado explícitamente'),checked=CHECKED)
        guides[pid]['sources']=list(sources.values())
    d['league_guide'].update(profiles=list(guides.values()),version=149)
    f=d['family_strategy'];f.update(version=149,checked=CHECKED)
    childnotes={
        'mat':T('Infomatrix: собственный инженерный прототип или программа, испытания и отчёт с раскрытием AI-помощи. Можно семейную команду до 3 учеников; смешанный уровень определяется старшим. Для Халапы 27–28 ноября проверить класс и страну команды до срока 6 ноября.',
             'Infomatrix: prototipo de ingeniería o programa propio, pruebas e informe declarando ayuda AI. Equipo familiar hasta 3 alumnos posible; nivel mixto según mayor. Para Xalapa 27–28 de noviembre comprobar curso y país del equipo antes del plazo 6 de noviembre.'),
        'osc':T('Infomatrix разрешает участников с 5 лет и независимые семейные команды: выделить Оскару собственную понятную часть проекта. Codi-Bot — только последний preschool или 1–3 класс, не просто любой ребёнок 6 лет. В TecPro Artifact минимум уже исполненные 6; поздний день рождения учитывать.',
             'Infomatrix permite desde 5 años y equipos familiares independientes: asignar a Oscar parte propia y comprensible del proyecto. Codi-Bot solo último preschool o curso 1–3, no cualquier niño de 6. TecPro Artifact exige 6 cumplidos; considerar cumpleaños tardío.')}
    for k,v in childnotes.items():f['children'][k]['current']=list(dict.fromkeys(f['children'][k]['current']+[v]))
    action=dict(period=T('5–6 ноября 2026','5–6 de noviembre de 2026'),title=T('Халапа: проверить реальный младший вход до срока','Xalapa: comprobar acceso menor real antes del plazo'),detail=RM_FIT+' '+RM_COST)
    if not any(a['title']==action['title'] for a in f['actions']):f['actions'].append(action)
    action=dict(period='2026–2027',title=T('Собственный проект → регион → аккредитация','Proyecto propio → regional → acreditación'),detail=IM_ENTRY+' '+IM_AWARD)
    if not any(a['title']==action['title'] for a in f['actions']):f['actions'].append(action)
    existing={s['url'] for s in f['sources']}
    for url,claim in [(IM_CALL,IM_TEAM+' '+IM_ENTRY),(RM_CALL,RM_TEAM+' '+RM_COST),(CODI,by_key['rm-junior-codi']['age'])]:
        if url not in existing:f['sources'].append(dict(title=T('Проверенные младшие проектные / робототехнические правила','Reglas verificadas de proyectos / robótica menores'),url=url,checked=CHECKED,claim=claim))
    return {'new_ids':list(index),'by_key':{k:e['id'] for k,e in by_key.items()},'new_profiles':[p['id'] for p in newprofiles]}
