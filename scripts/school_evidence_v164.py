"""Bounded VEX history and permanent-school entry routes; never admission events."""
from copy import deepcopy
from pathlib import Path
import json

CHECKED = '2026-11-05'
SPANISH = {}
def T(ru, es):
    SPANISH[ru] = es
    return ru

ROOT = Path(__file__).resolve().parents[1]
SJS = 'https://sjsricelake.org/'
PAS = 'https://www.pacificamerican.org/'
HCAS = 'https://www.hcas.tw/'
IBSH = 'https://ibsh.tw/'
IBSH_GUIDE = 'https://drive.google.com/file/d/1vNRyKuNHhDdVeMX463Kw7G_rYU28XumR/view'
HCAS_FEES = HCAS + 'wp-content/uploads/2026/08/%E5%AD%B8%E8%B2%BBG1-G12-Tuition-2026-2027-1.pdf'
GRADE = T('Классы детей неизвестны. Дневная ступень — кандидат, а не подтверждённое место в школе или команде; возраст 9 / 6 не заменяет класс.',
          'Cursos de los niños desconocidos. Etapa diurna es candidata, no plaza confirmada en escuela o equipo; edad 9 / 6 no sustituye curso.')
GATE = T('Подтвердить класс, индивидуальный приём, язык именно команды, наставника, роль ребёнка и полную смету. Заявки, согласия, сообщения и оплаты не выполнялись.',
         'Confirmar curso, admisión individual, idioma del equipo, mentor, función del niño y presupuesto completo. Sin solicitudes, consentimientos, mensajes ni pagos.')
NO_BOARD = T('Действующий пансион для детей 6 / 9 не установлен. Дневная школа не заменяет внешнее жильё семьи.',
             'Sin residencia vigente acreditada para niños de 6 / 9. Escuela diurna no sustituye alojamiento familiar externo.')
NO_AI = T('Отдельная соревновательная AI-команда младших в этом проходе не подтверждена.',
          'Sin confirmar equipo competitivo de AI para primaria en esta revisión.')
AFFIL = T('Награда и категория взяты из протокола конкретного года. Организация / класс в текущей карточке команды проверены 05.11.2026 и могут отличаться от исторических; это не архивный снимок принадлежности.',
          'Premio y categoría proceden del protocolo del año concreto. Organización / curso de ficha actual del equipo comprobados el 05.11.2026 pueden diferir de los históricos; no es captura histórica de afiliación.')
JUNIOR = T('Elementary — категория события, а не обещание состава из шестилетних. Приём младшего ребёнка в победившую команду не установлен.',
           'Elementary es categoría del evento, no promesa de equipo de niños de seis años. Sin acreditar admisión del menor al equipo ganador.')

def source(title, url, claim, kind='school'):
    return dict(title=title, url=url, claim=claim, kind=kind, checked=CHECKED)

def base(ident, name, iso, city, private=True):
    return dict(id=ident, name=name, iso=iso,
        country=T('США','EE.UU.') if iso=='USA' else T('Тайвань','Taiwán'),
        region=T('Северная Америка','América del Norte') if iso=='USA' else T('Азия','Asia'),
        city=city, school_type='private' if private else 'public', curriculum='', ib_programmes=[],
        ages='', instruction_languages=[], language_note=T('Английский сайт не подтверждает язык всех предметов и соревновательной группы; язык и поддержку уточнить.',
        'Web inglesa no confirma idioma de todas las asignaturas y grupo competitivo; verificar idioma y apoyo.'),
        fit=dict(mat='candidate',osc='candidate',note=GRADE),boarding='unknown',boarding_note=NO_BOARD,
        programme='',labs='',ai=NO_AI,results=[],evidence='programme',admissions=GATE,cost='',questions=[GATE],
        sources=[],checked=CHECKED,priority=2,research_status='partial',verification=GATE)

def school_result(r, limit=AFFIL):
    return dict(league='VEX IQ' if r['category'].startswith('IQ') else 'VEX V5',season=r['year'],
        stage='VEX World Championship · '+r['category'],award=r['award'],team=r['team_name'],
        team_id=r['team_id'],source=r['event_url'],provenance='organizer_protocol',limit=limit)

def make_schools(native):
    by_team={(r['year'],r['team_id']):r for r in native['selected_results']}
    out=[]
    s=base('S063','St. Joseph Catholic School · Spartan Robotics','USA','Rice Lake · Wisconsin')
    s.update(curriculum=T('Частная католическая школа PreK–Grade 8; реальная школьная VEX IQ программа с родительскими наставниками.',
        'Escuela católica privada PreK–Grade 8; programa escolar real VEX IQ con mentores familiares.'),
        ages=T('PreK–Grade 8. VEX IQ клуб 2026–27: только Grades 3–8; классы Матвея и Оскара не установлены.',
        'PreK–Grade 8. Club VEX IQ 2026–27: solo Grades 3–8; cursos de Matvey y Oscar sin acreditar.'),
        programme=T('Spartan Robotics: небольшие VEX IQ команды Grades 3–8, обычно среда 15:30–17:30, сезон октябрь–январь. Level Up 2026–27; на странице Registration Closed. Победители Excellence 2026 названы шестиклассниками — Elementary здесь не означает возраст 6 лет.',
        'Spartan Robotics: pequeños equipos VEX IQ Grades 3–8, normalmente miércoles 15:30–17:30, temporada octubre–enero. Level Up 2026–27; página indica Registration Closed. Ganadores Excellence 2026 identificados como sexto curso — Elementary aquí no significa edad de 6 años.'),
        labs=T('Сборка и программирование VEX IQ в школьном зале; родительские наставники и помощь Warrior Robotics. Гарантированный личный robot kit не заявлен.',
        'Construcción y programación VEX IQ en gimnasio escolar; mentores familiares y ayuda Warrior Robotics. Sin promesa de robot kit personal garantizado.'),
        admissions=T('Есть процесс нового приёма 2026–27: подтверждение школы, документы и регистрационный сбор. Международное зачисление, поддержка английского и место в клубе не подтверждены. У клуба старый текст Friday, August 29th не соответствует календарю 2026; дедлайн не перенесён догадкой.',
        'Existe proceso de nueva admisión 2026–27: confirmación escolar, documentos y cargo de registro. Sin acreditar admisión internacional, apoyo de inglés ni plaza en club. Texto antiguo Friday, August 29th no coincide con calendario 2026; sin trasladar plazo por suposición.'),
        cost=T('Опубликовано: K–8 USD 4000 в год; невозвратная регистрация USD 150 за ребёнка. Для двоих в K–8: 8300 до дополнительных расходов. VEX IQ USD 100 за участника включает турнирные взносы и футболку; участие обоих не гарантировано. PreK 3 — 2000, PreK 4 — 3500. Льгота Wisconsin Choice не считается автоматически доступной иностранной семье.',
        'Publicado: K–8 USD 4000 por año; registro no reembolsable USD 150 por niño. Para dos en K–8: 8300 antes de extras. VEX IQ USD 100 por participante incluye cuotas de torneos y camiseta; participación de ambos sin garantizar. PreK 3 — 2000, PreK 4 — 3500. Ayuda Wisconsin Choice no se considera automáticamente disponible para familia extranjera.'),
        evidence='world_result')
    s['results']=[school_result(by_team[(2026,'34362H')],JUNIOR+' '+T('Протокол организатора и школьная публикация согласуются по команде Natural Disaster; это Excellence, не Teamwork или Skills.',
        'Protocolo del organizador y publicación escolar coinciden en equipo Natural Disaster; es Excellence, no Teamwork ni Skills.'))]
    s['sources']=[source('VEX IQ club 2026–27',SJS+'athletics-activities/robotics/',s['programme']),
        source('Tuition and financial assistance',SJS+'admissions/tuition-and-financial-assistance/',s['cost']),
        source('New student enrollment',SJS+'admissions/enroll/',s['admissions']),
        source('School account of Worlds 2026',SJS+'press-release/robotics-team-makes-history/',JUNIOR),
        source('VEX Worlds 2026 Elementary awards',by_team[(2026,'34362H')]['event_url'],'Excellence Award · 34362H','organizer')]
    out.append(s)
    s=base('S064','Schilling Farms Elementary School · Stallionbots','USA','Collierville · Tennessee',False)
    s.update(curriculum=T('Государственная начальная школа Collierville Schools. NCES: Grades PK–5, справочник 2025–26; справочник не является аккредитацией или мировым рейтингом.',
        'Primaria pública Collierville Schools. NCES: Grades PK–5, directorio 2025–26; directorio no equivale a acreditación ni clasificación mundial.'),
        ages='PK–Grade 5',programme=T('Команда 6593A Stallionbots получила VEX IQ Elementary Excellence 2024. Текущая запись организатора называет Schilling Farms; историческое прикрепление к школе и нынешние младшие группы требуют дополнительного архивного подтверждения.',
        'Equipo 6593A Stallionbots obtuvo VEX IQ Elementary Excellence 2024. Ficha actual del organizador identifica Schilling Farms; afiliación histórica y grupos actuales de primaria requieren corroboración archivística adicional.'),
        labs=T('Текущий состав наставников, часы, оборудование младшей команды и условия входа не восстановлены; титул 2024 не доказывает доступную группу 2026–27.',
        'Sin reconstruir mentores actuales, horas, equipo de primaria ni acceso; título 2024 no acredita grupo disponible 2026–27.'),
        admissions=T('Государственный округ: проверить реальный адрес проживания, школьную зону, класс и индивидуальные документы. Факт PK–5 подтверждён федеральным NCES, школьные команды — публикациями школы / округа 2025–2026. Место в школе и клубе для новой семьи отдельно не подтверждено.',
        'Distrito público: verificar domicilio real, zona escolar, curso y documentación individual. PK–5 acreditado por NCES federal, equipos escolares por publicaciones escolares / distritales 2025–2026. Plaza escolar y de club para familia nueva sin confirmar por separado.'),
        cost=T('Полная текущая смета школы, клуба, соревнований, транспорта и жилья не проверена. Государственный статус не означает нулевую стоимость семейного маршрута.',
        'Sin verificar presupuesto completo actual de escuela, club, competiciones, transporte y vivienda. Carácter público no significa coste nulo del itinerario familiar.'),evidence='world_result')
    s['results']=[school_result(by_team[(2024,'6593A')])]
    s['sources']=[source('NCES public-school directory',native['schilling_nces_url'],s['curriculum'],'government'),
        source('VEX IQ Elementary 2024 awards',by_team[(2024,'6593A')]['event_url'],'Excellence Award · 6593A','organizer'),
        source('Current team metadata',by_team[(2024,'6593A')]['identity_url'],AFFIL,'organizer')]
    out.append(s)
    s=base('S065','Sandpiper School · Robo Cats','USA','Redwood City · California',False)
    s.update(curriculum=T('Государственная TK–Grade 8 школа Belmont–Redwood Shores School District. Программа науки, инженерных практик и поддержки изучающих английский.',
        'Escuela pública TK–Grade 8 de Belmont–Redwood Shores School District. Ciencias, prácticas de ingeniería y apoyo a quienes aprenden inglés.'),
        ages='TK–Grade 8',programme=T('Родительский Robotics Club подтверждён PTA; отдельный Coding Club описан для middle school. 2014K Robo Cats — Excellence VEX IQ Elementary 2025. Возраст входа в робототехнику, отбор и часы нынешнего сезона не опубликованы в прочитанных источниках.',
        'PTA confirma Robotics Club dirigido por familias; Coding Club separado se describe para middle school. 2014K Robo Cats — Excellence VEX IQ Elementary 2025. Edad de acceso a robótica, selección y horas actuales sin publicar en fuentes leídas.'),
        labs=T('Начальная наука Twig Science, средняя StemScopes; Grades 4–5 science specialist дважды в неделю. Это часы науки, не часы подготовки команды VEX.',
        'Ciencias de primaria Twig Science, secundaria StemScopes; Grades 4–5 science specialist dos veces por semana. Son horas de ciencias, no preparación de equipo VEX.'),
        language_note=T('Есть English Language Arts и прямое описание English Language Development для изучающих английский. Язык конкретной робототехнической команды и полное расписание предметов отдельно не установлены.',
        'Existe English Language Arts y descripción expresa de English Language Development para estudiantes de inglés. Sin acreditar por separado idioma del equipo de robótica y horario completo de materias.'),
        admissions=T('Округ открыл enrollment 2026–27. Проверить документы проживания и School Assignment Process: регистрация в округе не гарантирует назначение в Sandpiper или место в победившей команде.',
        'Distrito abrió enrollment 2026–27. Verificar documentos de domicilio y School Assignment Process: registro distrital no garantiza asignación a Sandpiper ni plaza en equipo ganador.'),
        cost=T('Полная семейная стоимость не подтверждена: клуб, турниры, материалы, транспорт и внешнее жильё отдельно. Налоговый статус государственной школы не превращён в итоговую цену 0.',
        'Sin confirmar coste familiar completo: club, torneos, materiales, transporte y alojamiento externo aparte. Carácter fiscal de escuela pública no convertido en precio total 0.'),evidence='world_result')
    s['results']=[school_result(by_team[(2025,'2014K')])]
    s['sources']=[source('Sandpiper PTA clubs','https://sandpiper.brssd.org/family-and-partner-groups/pta',s['programme']),
        source('Curriculum and instruction','https://sandpiper.brssd.org/programs/curriculum-and-instruction',s['labs']+' '+s['language_note']),
        source('BRSSD enrollment','https://www.brssd.org/online-enrollment',s['admissions'],'public_school'),
        source('VEX IQ Elementary 2025 awards',by_team[(2025,'2014K')]['event_url'],'Excellence Award · 2014K','organizer'),
        source('Current team metadata',by_team[(2025,'2014K')]['identity_url'],AFFIL,'organizer')]
    out.append(s)
    s=base('S066','Pacific American School · PAS','TWN','Zhubei · Hsinchu County')
    s.update(curriculum=T('Частная англоязычная школа Grades 1–12; младшая STEAM и старшие VEX / AIoT / предпринимательские проекты.',
        'Escuela privada en inglés Grades 1–12; STEAM de primaria y VEX / AIoT / proyectos empresariales de secundaria.'),
        ages='Grades 1–12; Elementary Grades 1–5',instruction_languages=['EN'],
        language_note=T('How to Apply прямо называет all-English-speaking school; есть ESL. Для Grades 1–2 оценивают базовый английский, Grades 3–5 — тестирование. Английский робототехнической группы и свободное место отдельно подтвердить.',
        'How to Apply indica expresamente all-English-speaking school; dispone de ESL. Grades 1–2 evalúan inglés básico, Grades 3–5 — pruebas. Confirmar por separado inglés del grupo de robótica y plaza.'),
        programme=T('В Elementary STEAM дважды в неделю. На странице клубов VEX и AIoT относятся к Middle / High School, не к младшим. Проведение VEX Signature Event не доказывает собственную победу школы.',
        'Elementary tiene STEAM dos veces por semana. En clubes, VEX y AIoT corresponden a Middle / High School, no primaria. Organizar VEX Signature Event no acredita victoria propia escolar.'),
        labs=T('Есть технологические и VEX направления; младшим подтверждены STEAM занятия. Объём личной работы с роботами, наставник и доступ к соревновательной группе уточнить.',
        'Existen áreas tecnológicas y VEX; primaria tiene clases STEAM acreditadas. Verificar trabajo personal con robots, mentor y acceso al grupo competitivo.'),
        boarding='yes',boarding_note=T('Опубликован Dormitory & Meal Service NTD 150000 за семестр для boarders. Минимальный возраст и приём детей 6 / 9 в пансион не установлены; цену пансиона не применять автоматически обоим.',
        'Publicado Dormitory & Meal Service NTD 150000 por semestre para boarders. Sin acreditar edad mínima ni admisión residencial de niños de 6 / 9; no aplicar precio automáticamente a ambos.'),
        admissions=T('Приоритет сильному академическому английскому и иностранному / второму паспорту; конкретный класс, interview, ESL и места требуют решения школы. Наличие паспорта не означает зачисление.',
        'Prioridad a inglés académico sólido y pasaporte extranjero / segundo; curso concreto, interview, ESL y plazas requieren decisión escolar. Pasaporte no equivale a admisión.'),
        cost=T('2026–27, NTD: G1–5 tuition 319800 за семестр; годовая регистрация 50000; capital 45000 и facility & technology 35000 за семестр. Для двоих в G1–5 за два семестра: tuition 1279200; с этими регулярными обязательными сборами 1699200 при начислении facility & technology каждому ученику. Единицу этого сбора подтвердить. Это не полный счёт: first-time application 100000, страхование 800 и PTA 1000 за ребёнка требуют уточнения периода / применения; ESL 70000 за семестр при необходимости. Lunch G1–5 20000 за год; ERB test 5500; транспорт, книги, турниры и жильё отдельно. Boarding 150000 за семестр — только при принятом residential admission.',
        '2026–27, NTD: G1–5 tuition 319800 por semestre; registro anual 50000; capital 45000 y facility & technology 35000 por semestre. Para dos en G1–5 durante dos semestres: tuition 1279200; con estos cargos obligatorios periódicos 1699200 si facility & technology se cobra a cada alumno. Confirmar unidad de este cargo. No es factura completa: first-time application 100000, seguro 800 y PTA 1000 por niño requieren aclarar período / aplicación; ESL 70000 por semestre si procede. Lunch G1–5 20000 por año; ERB test 5500; transporte, libros, torneos y vivienda aparte. Boarding 150000 por semestre — solo con residential admission aceptada.'))
    s['sources']=[source('Elementary STEAM',PAS+'elementary-school/',s['programme']),source('School clubs',PAS+'school-clubs/',s['programme']),
        source('How to apply',PAS+'how-to-apply/',s['language_note']+' '+s['admissions']),source('Tuition and fees 2026–27',PAS+'tuition-fees/',s['cost']),source('Robotics / VEX',PAS+'robotics/',s['labs'])]
    out.append(s)
    s=base('S067','Hsinchu County American School · HCAS','TWN','Zhubei · Hsinchu County')
    s.update(curriculum=T('Частная школа Kindergarten–Grade 12. First Program Grades 1–5; английский основной язык преподавания, китайский ежедневно.',
        'Escuela privada Kindergarten–Grade 12. First Program Grades 1–5; inglés es idioma principal de enseñanza, chino a diario.'),
        ages='Kindergarten–Grade 12; First Program Grades 1–5',instruction_languages=['EN'],language_note=T('Основной English прямо подтверждён First Program; это не только английская версия сайта. Китайский — ежедневный предмет. Обязательный EAL при результате WIDA ниже школьного порога; платный и не по желанию семьи.',
        'First Program confirma expresamente inglés principal; no es solo versión web inglesa. Chino es asignatura diaria. EAL obligatorio si WIDA queda bajo umbral escolar; con coste y no opcional para familia.'),
        programme=T('VEX team на странице Teams — Grades 6–12. Школьный отчёт 2023–24 сообщает Creative Award на Taiwan Open; точное название и уровень без независимого протокола не переименованы. Для 6 / 9 это школьная база с будущим командным входом, не доказанная младшая VEX команда.',
        'VEX team en Teams es Grades 6–12. Informe escolar 2023–24 declara Creative Award en Taiwan Open; sin renombrar título ni nivel sin protocolo independiente. Para 6 / 9 es base escolar con futuro acceso al equipo, no equipo VEX de primaria acreditado.'),
        labs=T('Опубликованы robotics lab, computer lab и две science labs. Собственное устройство обязательно Grades 7–12 и рекомендовано Grades 5–6; школа не выдаёт каждому ноутбук.',
        'Publicados robotics lab, computer lab y dos science labs. Dispositivo propio obligatorio Grades 7–12 y recomendado Grades 5–6; escuela no entrega portátil a cada alumno.'),
        admissions=T('Годовой rolling admission; предпочтительны начало учебного года и второго семестра, промежуточный вход индивидуально. G1 без прежней выписки; G2–4 предыдущий и текущий год, G5–8 два предыдущих и текущий; G1–8 одна рекомендация. FAQ допускает все национальности; для тайваньского ученика нужен второй паспорт или доказательство оформления. Тест, документы и решение школы обязательны.',
        'Rolling admission anual; preferencia por inicio de año y segundo semestre, entrada intermedia individual. G1 sin expediente anterior; G2–4 año anterior y actual, G5–8 dos anteriores y actual; G1–8 una recomendación. FAQ admite todas las nacionalidades; alumno taiwanés requiere segundo pasaporte o prueba de trámite. Prueba, documentos y decisión escolar obligatorios.'),
        cost=T('Официальный PDF 2026–27, NTD: G1–4 tuition 208000, G5–8 248000, G9–12 288000 за семестр; annual registration 25000; first-time application 50000; technology 7000 и miscellaneous 3300 за семестр. Для двоих в G1–4 за два семестра tuition 832000, с registration + technology + miscellaneous 923200, без first-time и прочих платежей. Lunch G1–4 15500 за семестр обязателен кроме medical exemption; EAL 45000 при необходимости. MAP G1–5 1100 и library 1000: период уточнить. Шаблон возврата boarding fee не доказывает действующий пансион.',
        'PDF oficial 2026–27, NTD: G1–4 tuition 208000, G5–8 248000, G9–12 288000 por semestre; annual registration 25000; first-time application 50000; technology 7000 y miscellaneous 3300 por semestre. Para dos en G1–4 durante dos semestres tuition 832000, con registration + technology + miscellaneous 923200, sin first-time ni otros pagos. Lunch G1–4 15500 por semestre obligatorio salvo medical exemption; EAL 45000 si procede. MAP G1–5 1100 y library 1000: confirmar período. Plantilla de devolución de boarding fee no acredita residencia vigente.'),evidence='other_result')
    s['results']=[dict(league='VEX V5',season='2023–24',stage='Taiwan Open',award='Creative Award',team='HCAS VEX Team',team_id=None,source=HCAS+'campus-life/sports_academic_teams/',provenance='school_report',limit=s['programme'])]
    s['sources']=[source('First Program',HCAS+'learning/first-program/',s['language_note']),source('VEX teams',HCAS+'campus-life/sports_academic_teams/',s['programme']),
        source('Campus labs',HCAS+'about-us/campus/',s['labs']),source('Admissions',HCAS+'admissions/',s['admissions']),source('Admissions FAQ',HCAS+'admissions/frequently-asked-questions/',s['admissions']),source('Official tuition PDF 2026–27',HCAS_FEES,s['cost'])]
    out.append(s)
    s=base('S068','International Bilingual School at Hsinchu Science Park · IBSH','TWN','Hsinchu · 300 Jieshou Road',False)
    s.update(curriculum=T('Государственное bilingual отделение National Experimental High School; Grades 1–12. Сокращение IBSH не подтверждает программу International Baccalaureate; IB не установлен.',
        'Sección pública bilingual de National Experimental High School; Grades 1–12. Sigla IBSH no acredita programa International Baccalaureate; IB sin acreditar.'),
        ages=T('Grades 1–12. Для G1 в 2026–27: родиться не позже 2020-09-01; точная дата Оскара неизвестна. Ранний вход с 5.5 лет — специальное одобрение gifted evaluation, не автоматическое исключение.',
        'Grades 1–12. G1 en 2026–27: nacer no después de 2020-09-01; fecha exacta de Oscar desconocida. Entrada temprana desde 5.5 años exige aprobación especial gifted evaluation, no excepción automática.'),
        fit=dict(mat='unknown',osc='unknown',note=T('Наличие младшей ступени не снимает ограничений Article III / V, теста и возрастного cutoff; допуск семьи не доказан.',
        'Etapa primaria no elimina restricciones Article III / V, examen ni cutoff de edad; admisibilidad familiar sin acreditar.')),
        language_note=T('Школа прямо описывает bilingual environment; требуется English Admission Exam, Chinese Placement Test определяет группу. Это не обещание всех предметов и робототехники только на английском.',
        'Escuela describe expresamente bilingual environment; exige English Admission Exam, Chinese Placement Test asigna grupo. No promete todas las materias y robótica exclusivamente en inglés.'),
        programme=T('Robotics Club указан в Gr.7–12 Clubs. Genesis 78181A — VEX V5 Middle School Excellence 2024; Curious Robotics прямо называет себя тренером, а участников — учениками IBSH. Достижение учеников с внешним тренером не приписано только школьной лаборатории. Младший Gr.1–6 robotics вход не доказан.',
        'Robotics Club aparece en Gr.7–12 Clubs. Genesis 78181A — VEX V5 Middle School Excellence 2024; Curious Robotics se identifica como entrenador y alumnos como estudiantes IBSH. Logro de alumnos con entrenador externo no atribuido solo al laboratorio escolar. Acceso robotics Gr.1–6 sin acreditar.'),
        labs=T('Опубликована билингвальная учебная структура и старший robotics club. Личные часы младших, оборудование и EN-группа требуют проверки.',
        'Publicados estructura curricular bilingüe y robotics club de cursos superiores. Verificar horas personales de primaria, equipo y grupo EN.'),
        admissions=T('Guide 2026–27 требует конкретной категории Article III или V и вступительного английского. В Technology-категории прямо приведена Taiwan Employment Gold Card in Technology field; любая Gold Card сама по себе не доказывает этот маршрут. Для special foreign professional есть отдельное условие Article V. Промежуточный набор закрылся 30.10.2026, экзамен 05.11.2026 не открыт для новой заявки. В guide второй семестр: экзамены 07.01.2027 Article III и 13.01.2027 Article V; окно заявок, категорию и места подтвердить по свежему notice. При расхождении действует китайский оригинал.',
        'Guide 2026–27 exige categoría concreta Article III o V y examen de inglés. Categoría Technology cita Taiwan Employment Gold Card in Technology field; cualquier Gold Card por sí sola no acredita esta vía. Special foreign professional tiene condición separada Article V. Admisión intermedia cerró el 30.10.2026, examen 05.11.2026 no admite solicitud nueva. Guide para segundo semestre: exámenes 07.01.2027 Article III y 13.01.2027 Article V; confirmar ventana de solicitudes, categoría y plazas según notice reciente. En discrepancia prevalece original chino.'),
        cost=T('Guide: review NTD 400, English exam 700, Chinese placement 700 при сдаче. Эти суммы не tuition и не полный семейный бюджет. Свежая полная стоимость школы, жилья и внешнего тренера не установлена.',
        'Guide: review NTD 400, English exam 700, Chinese placement 700 si se realiza. No son tuition ni presupuesto familiar completo. Coste completo reciente de escuela, vivienda y entrenador externo sin acreditar.'),evidence='world_result')
    s['results']=[school_result(by_team[(2024,'78181A')],s['programme'])]
    s['sources']=[source('Official admission guide 2026–27',IBSH_GUIDE,s['admissions']+' '+s['ages'],'public_school'),
        source('Admission guide announcement',IBSH+'p/406-1001-1583%2Cr26.php',s['admissions'],'public_school'),
        source('Bilingual curriculum',IBSH+'p/412-1001-157.php',s['language_note'],'public_school'),
        source('Grades 7–12 clubs',IBSH+'p/412-1001-161.php',s['programme'],'public_school'),
        source('VEX V5 Middle School 2024 protocol',by_team[(2024,'78181A')]['event_url'],'Excellence Award · 78181A','organizer'),
        source('Trainer account of Genesis / IBSH',native['genesis_trainer_url'],s['programme'],'school_team')]
    out.append(s)
    return out

def enrich_v164(d):
    native=json.loads((ROOT/'data/school-evidence-native-v164.json').read_text())
    schools={s['id']:s for s in d['schools']}
    for s in make_schools(native):
        if s['id'] in schools:
            assert schools[s['id']]['name']==s['name']
            schools[s['id']].update(deepcopy(s))
        else:d['schools'].append(deepcopy(s));schools[s['id']]=d['schools'][-1]
    schilling=schools['S064']
    state_note=T('Официальные публикации школы / округа подтверждают: в 2025 Schilling получила три названные награды штата, в 2026 шесть. Это региональные результаты и квалификация, не дополнительные мировые титулы. Многолетняя школьная программа подтверждена, место и младший класс для нового ученика требуют отдельного решения.',
        'Publicaciones oficiales escolares / distritales acreditan: en 2025 Schilling recibió tres premios estatales citados, en 2026 seis. Son resultados regionales y clasificación, no títulos mundiales adicionales. Programa escolar de varios años acreditado, plaza y curso inferior para alumno nuevo requieren decisión separada.')
    schilling['programme']+=' '+state_note
    for r in native.get('schilling_regional_results',[]):
        schilling['results'].append(dict(league='VEX IQ',season=r['year'],stage='Tennessee State Championship · Elementary',award=r['award'],team='Stallionbots',team_id=r['team_id'],source=r['source'],provenance='school_report',limit=state_note))
    for url in dict.fromkeys(r['source'] for r in native.get('schilling_regional_results',[])):
        schilling['sources'].append(source('Official school / district state results',url,state_note,'public_school'))
    if native.get('sandpiper_roster_index_url'):
        roster_note=T('В поисковом извлечении официального roster Engineering Division 2025 прямо указаны 2014K, Robo Cats и Sandpiper School. Сам PDF по этому адресу сейчас не удалось скачать; это дополнительное индексированное свидетельство исторической связи, а не заявление о прочтении оригинального PDF.',
            'Extracción de búsqueda del roster oficial Engineering Division 2025 identifica 2014K, Robo Cats y Sandpiper School. No se pudo descargar el PDF de esa dirección; es evidencia indexada adicional de afiliación histórica, no afirmación de lectura del PDF original.')
        schools['S065']['results'][0]['limit']+=' '+roster_note
        schools['S065']['sources'].append(source('Indexed official roster · Engineering Division 2025',native['sandpiper_roster_index_url'],roster_note,'organizer'))
    ast=schools['S020'];r=next(r for r in native['selected_results'] if r['year']==2022 and r['team_id']=='66799T')
    ast['results']=[school_result(r,T('В старой HTML-таблице организатора прямо названы American School in Taichung, 66799T и Elementary Excellence. Ранее неклассифицированное World Champions уточнено без создания второй награды.',
        'Tabla HTML antigua del organizador identifica expresamente American School in Taichung, 66799T y Elementary Excellence. World Champions antes sin clasificar aclarado sin crear segundo premio.')) if x['season']==2022 else x for x in ast['results']]
    ast['sources'].append(source('VEX IQ Elementary 2022 legacy awards',r['event_url'],'66799T · Elementary Excellence Award','organizer')) if not any(x['url']==r['event_url'] for x in ast['sources']) else None
    ast['checked']=CHECKED
    tas=schools['S003'];tas['checked']=CHECKED
    tas_source=native['tas_regional_url']
    tas_note=T('Школьный отчёт 12.01.2026 о региональном ASIJ в Tokyo, High School. Не мировое событие и не результат младших.',
        'Informe escolar 12.01.2026 sobre ASIJ regional en Tokyo, High School. No es evento mundial ni resultado de primaria.')
    for team,award,level in [('4253Z','Excellence Award','regional_judged'),('4253S','Tournament Champion','regional_match'),('4253V','Tournament Champion','regional_match'),('4253A','Robot Skills Champion','regional_skills')]:
        if not any(x.get('source')==tas_source and x.get('team_id')==team and x.get('award')==award for x in tas['results']):
            tas['results'].append(dict(league='VEX V5',season=2026,stage='ASIJ Tournament · Tokyo · High School',award=award,team='TAS Tigers',team_id=team,source=tas_source,provenance='school_report',limit=tas_note))
    if not any(x['url']==tas_source for x in tas['sources']):tas['sources'].append(source('ASIJ Tokyo 2026',tas_source,tas_note))
    sesi=schools['S015'];sesi['name']='Escola SESI Humberto Cereser · CE 021 · Heroes';sesi['checked']=CHECKED
    sesi_note=T('Оператор называет конкретный кампус CE 021 и международный Open Guadalajara 27–30.05.2026. Champions и Innovation — оценённые награды Open; вторые места Robot Performance / Alliances не мировые титулы Houston.',
        'Operador identifica campus concreto CE 021 e International Open Guadalajara 27–30.05.2026. Champions e Innovation son premios evaluados del Open; segundos puestos Robot Performance / Alliances no son títulos mundiales Houston.')
    for award in ['Champions Award','Innovation Project · 1st place','Robot Performance · 2nd place','Alliances · 2nd place']:
        if not any(x.get('source')==native['sesi_open_url'] and x['award']==award for x in sesi['results']):
            sesi['results'].append(dict(league='FIRST LEGO League Challenge',season=2026,stage='International Open · Guadalajara · México',award=award,team='SESI Heroes · CE 021',team_id=None,source=native['sesi_open_url'],provenance='school_operator_report',limit=sesi_note))
    for url,title,claim in [(native['sesi_open_url'],'SESI Heroes Mexico Open 2026',sesi_note),(native['sesi_admission_url'],'SESI admission 2027',T('Общая запись на 2027 закрыта: beneficiary 06–15.10.2026, non-beneficiary 19–21.10.2026 только при оставшихся местах; это не действующая открытая форма.',
        'Inscripción general 2027 cerrada: beneficiary 06–15.10.2026, non-beneficiary 19–21.10.2026 solo con vacantes; no es formulario abierto vigente.'))]:
        if not any(x['url']==url for x in sesi['sources']):sesi['sources'].append(source(title,url,claim,'school_operator'))
    sesi['admissions']=sesi['sources'][-1]['claim']+' '+GATE
    for result in sesi['results']:
        if result['season']==2025:result['limit']=T('Houston 2025 Champion’s Award сохраняется как отдельный титул. Кампус CE 021 уточнён по сообщению оператора 2026; независимый протокол Houston 2025 и историческое прикрепление кампуса требуют сверки.',
        'Houston 2025 Champion’s Award se conserva como título separado. Campus CE 021 aclarado por informe del operador 2026; protocolo independiente Houston 2025 y afiliación histórica del campus requieren cotejo.')
    h=d['school_history'];h.update(version=164,checked=CHECKED,status='partial')
    entities={x['id']:x for x in h['entities']}
    entities['S015']['name']=sesi['name']
    for row in native['selected_results']:
        eid=row.get('school_id') or 'VIQ-'+str(row['year'])+'-'+row['team_id']
        if row['team_id']=='78181A':eid='GENESIS-78181A'
        note=(AFFIL if not row['historical_affiliation'] else T('Организация названа в исторической таблице награды; не текущая догадка по сходству имени.',
            'Organización identificada en tabla histórica del premio; no conjetura actual por parecido del nombre.'))
        note+=' '+(JUNIOR if row['category']=='IQ Elementary' else T('Результат Middle School; он не подтверждает соревновательную группу для детей 6 / 9.',
            'Resultado Middle School; no acredita grupo competitivo para niños de 6 / 9.'))
        if row.get('affiliation_note'):note+=' '+row['affiliation_note']
        if eid not in entities:
            e=dict(id=eid,name=row['organization'] or row['team_name'],kind=row['entity_kind'],country=next(c['country'] for c in d['countries'] if c['iso']==row['country']),age='primary' if row['category']=='IQ Elementary' else 'secondary',note=note,school_id=row.get('school_id'))
            h['entities'].append(e);entities[eid]=e
        entities[eid].setdefault('school_id',row.get('school_id'))
        if eid.startswith('VIQ-') or eid in ['S063','S064','S065','GENESIS-78181A']:
            entities[eid].update(note=note,school_id=row.get('school_id'),country=next(c['country'] for c in d['countries'] if c['iso']==row['country']))
        rec=dict(entity_id=eid,year=row['year'],league='VEX',category=row['category'],stage='VEX World Championship',award=row['award'],level=row['level'],source=row['event_url'],provenance='organizer_protocol',team=row['team_name'],team_id=row['team_id'],note=note,checked=CHECKED)
        if row['year']==2022 and row['team_id']=='66799T':next(x for x in h['results'] if x['id']=='H100').update(rec)
        else:
            existing=next((x for x in h['results'] if x.get('team_id')==row['team_id'] and x['year']==row['year'] and x['award']==row['award'] and x['source']==row['event_url']),None)
            if existing:existing.update(rec)
            else:
                rec['id']='H'+str(max(int(x['id'][1:]) for x in h['results'])+1).zfill(3);h['results'].append(rec)
    for sid in ['S003','S015']:
        for r in schools[sid]['results']:
            if r['season']!=2026 or r['source'] not in [tas_source,native['sesi_open_url']]:continue
            level=next((level for team,award,level in [('4253Z','Excellence Award','regional_judged'),('4253S','Tournament Champion','regional_match'),('4253V','Tournament Champion','regional_match'),('4253A','Robot Skills Champion','regional_skills')] if team==r['team_id']),'international_open_podium' if '2nd' in r['award'] else 'international_open_judged')
            if not any(x['entity_id']==sid and x['year']==2026 and x['award']==r['award'] and x.get('team_id')==r['team_id'] and x['source']==r['source'] for x in h['results']):
                h['results'].append(dict(id='H'+str(max(int(x['id'][1:]) for x in h['results'])+1).zfill(3),entity_id=sid,year=2026,league='VEX' if sid=='S003' else 'FLL',category='V5 High School' if sid=='S003' else 'Challenge',stage=r['stage'],award=r['award'],level=level,source=r['source'],provenance=r['provenance'],team=r['team'],team_id=r['team_id'],note=r['limit'],checked=CHECKED))
    for r in native.get('schilling_regional_results',[]):
        existing=next((x for x in h['results'] if x['entity_id']=='S064' and x['year']==r['year'] and x['award']==r['award'] and x.get('team_id')==r['team_id'] and x['source']==r['source']),None)
        if existing:existing['note']=state_note
        else:
            h['results'].append(dict(id='H'+str(max(int(x['id'][1:]) for x in h['results'])+1).zfill(3),entity_id='S064',year=r['year'],league='VEX',category='IQ Elementary',stage='Tennessee State Championship',award=r['award'],level=r['level'],source=r['source'],provenance='school_report',team='Stallionbots',team_id=r['team_id'],note=state_note,checked=CHECKED))
    c=next(c for c in h['coverage'] if c['id']=='VEX')
    c['detail']=T('IQ Elementary 2022–2026: полностью извлечены три выбранные категории — Excellence, обе команды Teamwork Champions и Robot Skills Champions, всего 20 командных записей. 2022 из legacy HTML, 2023–2026 из публичного JSON организатора. Дополнительно четыре победителя IQ Middle 2026 и Genesis V5 Middle 2024. Это не полный архив всех наград VEX, всех возрастов или школ за десять лет.',
        'IQ Elementary 2022–2026: extraídas completas tres categorías elegidas — Excellence, ambos equipos Teamwork Champions y Robot Skills Champions, total 20 registros de equipos. 2022 de legacy HTML, 2023–2026 de JSON público del organizador. Además cuatro ganadores IQ Middle 2026 y Genesis V5 Middle 2024. No es archivo completo de todos los premios VEX, edades o escuelas durante diez años.')
    c['sources']=list(dict.fromkeys(c['sources']+[r['event_url'] for r in native['selected_results']]))
    for y in range(2022,2027):c['years'][str(y)]='verified_selected'
    h['conclusion']=T('VEX IQ Elementary: пять Excellence за 2022–2026 принадлежат пяти разным организациям в проверенных протоколах / текущих карточках команд; единый многолетний школьный лидер из этого не следует. Внешние клубы, школы и школьные округа показаны отдельно. Рейтинг школ по всем лигам остаётся частичным.',
        'VEX IQ Elementary: cinco Excellence de 2022–2026 corresponden a cinco organizaciones distintas según protocolos / fichas actuales; no demuestra líder escolar único de varios años. Clubes externos, escuelas y distritos aparecen separados. Clasificación escolar de todas las ligas sigue parcial.')
    extra=T('v164: историческая категория берётся из события, даже если текущий team profile уже Middle School. Зарегистрированная компания, название команды со словом School и реальная школа не отождествляются. Франшизы Magikid в Frisco и Cupertino и разные STEMSTAR центры не объединены по бренду. International Open не входит в мировые титулы; IBSH / Genesis показывает внешнего тренера Curious Robotics.',
        'v164: categoría histórica procede del evento aunque team profile actual ya sea Middle School. Empresa registrante, nombre de equipo con palabra School y escuela real no se identifican entre sí. Franquicias Magikid de Frisco y Cupertino y distintos centros STEMSTAR no se fusionan por marca. International Open no suma títulos mundiales; IBSH / Genesis muestra entrenador externo Curious Robotics.')
    if extra not in h['methodology']:h['methodology'].append(extra)
    route=dict(name=T('Новые школьные варианты · США / Тайвань','Nuevas opciones escolares · EE.UU. / Taiwán'),ids=['S063','S064','S065','S066','S067','S068'],detail=T('St. Joseph: доказанный титул, но клуб Grades 3–8 и запись закрыта. Schilling Farms: подтверждённая программа 2025–2026, поступление по округу. Sandpiper: родительский клуб и назначение по округу. PAS: младшая STEAM, VEX старше. HCAS: английская начальная база, VEX Grades 6–12. IBSH: сначала доказать категорию admission и возрастной cutoff; результат Genesis связан с внешним тренером. Выбирать школьную среду и доступ ребёнка, а не покупать название титула.',
        'St. Joseph: título acreditado, pero club Grades 3–8 e inscripción cerrada. Schilling Farms: programa acreditado 2025–2026, admisión distrital. Sandpiper: club familiar y asignación distrital. PAS: STEAM de primaria, VEX posterior. HCAS: base primaria en inglés, VEX Grades 6–12. IBSH: acreditar primero categoría de admission y cutoff de edad; resultado Genesis vinculado a entrenador externo. Elegir entorno escolar y acceso del niño, no comprar nombre de título.'))
    if not any(r['ids']==route['ids'] for r in h['family_routes']):h['family_routes'].append(route)
    focus=d['school_focus'];focus.update(version=164,checked=CHECKED)
    focus['conclusion']=T('Добавлены школьные маршруты США / Тайваня с опубликованными тарифами и ограничениями допуска. Мировая награда, текущая школьная ступень, внешний тренер и место конкретного ребёнка проверяются отдельно. Полного мирового рейтинга школ нет.',
        'Añadidas rutas escolares de EE.UU. / Taiwán con tarifas publicadas y restricciones de admisión. Premio mundial, etapa escolar actual, entrenador externo y plaza concreta del niño se verifican por separado. Sin clasificación mundial completa de escuelas.')
    focus['counts'].update(records=len(d['schools']),countries=len({s['iso'] for s in d['schools']}),
        public=sum(s['school_type']=='public' for s in d['schools']),private=sum(s['school_type'].startswith('private') for s in d['schools']),
        organizer_protocol=sum(any(r['provenance']=='organizer_protocol' for r in s['results']) for s in d['schools']),
        world_result=sum(s['evidence']=='world_result' for s in d['schools']),boarding=sum(s['boarding']=='yes' for s in d['schools']))
    for row in focus['coverage']:
        row['records']=sum(s['iso']==row['iso'] for s in d['schools'])
        row['status']='partial' if row['records'] else 'unresearched'
    if not any(r['ids']==route['ids'] for r in focus['routes']):focus['routes'].append(deepcopy(route))
    known_sources={s['url'] for s in d['sources']}
    for school in d['schools']:
        if school['id'] not in ['S003','S015','S020','S063','S064','S065','S066','S067','S068']:continue
        for s in school['sources']:
            if s['url'] not in known_sources:
                d['sources'].append(dict(url=s['url'],title=s['title'],evidence=s['claim'],checked=s['checked']))
                known_sources.add(s['url'])
    for r in native['selected_results']:
        if r['event_url'] not in known_sources:
            d['sources'].append(dict(url=r['event_url'],title='VEX World Championship '+str(r['year'])+' · '+r['category'],evidence=AFFIL,checked=CHECKED))
            known_sources.add(r['event_url'])
    state_urls={r['source'] for r in native.get('schilling_regional_results',[])}
    for s in d['sources']:
        if s['url'] in state_urls:s['evidence']=state_note
    d['school_evidence_v164']=dict(version=164,checked=CHECKED,selected_elementary_seasons=5,selected_elementary_result_rows=20,new_schools=6,status='partial',worldwide_complete=False)
