"""Official winter course inventories, sibling options and explicit date corrections."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
from camp_europe_v148 import lesson,weekdays

CHECKED='2026-11-05'
SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
ROOT=Path(__file__).resolve().parents[1]
ESF='https://www.esfexplore.org.hk/winter-camp/'
ESF_EVENTS='https://www.esfexplore.org.hk/events/'
ESF_POLICY='https://www.esfexplore.org.hk/policies/'
ESF_PDF='https://www.esfexplore.org.hk/wp-content/uploads/2026/10/2026-ESF-Explore-Winter-Camp-Offerings-Full-Day-Camps.pdf'
ESF_PARENT='https://www.esfexplore.org.hk/wp-content/uploads/2026/10/Full-Day-Camp-%E2%80%93-Important-Information-for-Parents.pdf'
SG='https://www.campasia.asia/'
SG_BOOK=SG+'book-a-camp'
SG_PROMISE=SG+'about-us/our-promise.html'
SG_FAQ=SG+'about-us/faqs.html'
SG_TERMS=SG+'about-us/terms-and-conditions.html'
HK='https://www.campasia.hk/'
HK_SCHEDULE=HK+'holiday-camp-schedule/'
HK_TERMS=HK+'getting-ready/terms-and-conditions/'
HK_FAQ=HK+'getting-ready/faq/'
DULWICH='https://www.dulwich.org/world/camps'
DUL_PDF='https://assets.dulwich.org/dulwich/blocks/201790/p/0/download/winter-camps-en-v1.pdf'
GOOD='https://goodgoodenglish.com/en/summer-winter-camps-en/'
GOOD_POSTER='https://goodgoodenglish.com/wp-content/uploads/2026/10/winter_camp_poster.jpg'
GMI='https://kti-camp.web.app/'
STARK='https://www.starklabtw.com/en/programs/winter-2027'
GRADE=T('Реальный класс детей неизвестен. Опубликованный школьный уровень проверяется отдельно; год рождения и возраст его не заменяют.',
 'Curso escolar real de los niños desconocido. Comprobar nivel escolar publicado por separado; año de nacimiento y edad no lo sustituyen.')
UNKNOWN_LANG=T('Прямое подтверждение языка преподавания для этого курса не найдено. Английская страница / международная школа не доказывают EN преподавания.',
 'Sin localizar confirmación expresa del idioma de enseñanza de este curso. Página inglesa / colegio internacional no acreditan enseñanza EN.')
NO_BOOKING=T('Возрастная возможность не означает место или зачисление. Уровень после трёх лет соревнований, индивидуальный иностранный приём, итоговый invoice и условия подтвердить; заявка и оплата не выполнялись.',
 'Posibilidad por edad no significa plaza ni admisión. Confirmar nivel tras tres años de competiciones, admisión extranjera individual, invoice final y condiciones; sin solicitud ni pago.')
TRIP=T('Перелёты, жильё родителей, расходы семьи и включения итогового счёта отдельно.',
 'Vuelos, alojamiento parental, gastos familiares e inclusiones de factura final aparte.')
ESF_CANCEL=T('Holiday policy: за 3 и более дня до первого занятия, не считая день занятия, возврат минус HKD 200; меньше 3 дней — без возврата / кредита. Один перенос за неделю с тем же сроком и сбором 200. При болезни более 50% лагеря и справке в течение 7 дней — 80% кредит, не cash refund. Погодная отмена обычно 50% кредит на год. Full day соединяет два enrollment: количество административных сборов согласовать. Промо не применяется задним числом; согласия не давались.',
 'Holiday policy: con 3 o más días antes de primera clase, sin contar día de clase, devolución menos HKD 200; menos de 3 días sin devolución / crédito. Un cambio semanal con mismo plazo y cargo 200. Enfermedad superior al 50% del campamento con certificado dentro de 7 días: 80% de crédito, no cash refund. Cancelación meteorológica normalmente 50% de crédito anual. Full day combina dos enrollment: acordar número de cargos administrativos. Promoción no retroactiva; sin consentimientos.')
SG_CANCEL=T('Полная предоплата; после подтверждения и оплаты отмена / возврат лагеря, автобуса и merchandise не предусмотрены, включая болезнь, погодное закрытие и невозможность приезда. Перенос курса не позднее 10 дней при наличии мест, доплата разницы за более дорогой курс. Liability insurance оператора не заменяет личную accident / medical insurance ребёнка. FAQ не обещает скидку за братьев / сестёр. Условия не принимались.',
 'Prepago total; tras confirmación y pago sin cancelación / devolución de campamento, autobús ni merchandise, incluidas enfermedad, cierre meteorológico e imposibilidad de llegar. Cambio de curso al menos 10 días antes sujeto a plazas, abonando diferencia de curso más caro. Liability insurance del operador no sustituye accident / medical insurance personal del niño. FAQ no promete descuento por hermanos. Sin aceptar condiciones.')
HK_CANCEL=T('Полная предоплата. По terms отмена не менее чем за 14 дней даёт возврат минус HKD 300 за каждый camp; для AM + PM сбор может быть 600. Менее 14 дней, пропуски / болезнь и погодные закрытия обычно без возврата / кредита. Перенос за 10 дней, HKD 100 за camp и возможная разница цены. Terms и FAQ сверять с выбранным invoice; согласие не давалось.',
 'Prepago total. Según terms cancelación al menos 14 días antes permite devolución menos HKD 300 por cada camp; AM + PM puede suponer cargo 600. Menos de 14 días, ausencias / enfermedad y cierres meteorológicos normalmente sin devolución / crédito. Cambio con 10 días, HKD 100 por camp y posible diferencia de tarifa. Contrastar terms y FAQ con invoice elegido; sin consentimiento.')
ESF_LANGUAGE=T('ESF прямо описывает программы как проводимые на английском. Spanish Beginner / Fiesta — занятия испанским; при полном дне спорт после обеда на английском, поэтому это смешанные языковые блоки, а не целый день только на испанском.',
 'ESF describe expresamente programas impartidos en inglés. Spanish Beginner / Fiesta son clases de español; en jornada completa deportes de tarde en inglés, por tanto bloques de idiomas mixtos, no día entero solo en español.')
SG_LANGUAGE=T('Our Promise прямо называет английский основным языком; FAQ приветствует детей разных национальностей, школ и стран. Это опубликованный маршрут иностранного индивидуального доступа, не персональное зачисление и не визовое разрешение.',
 'Our Promise identifica expresamente inglés como idioma principal; FAQ acoge niños de distintas nacionalidades, colegios y países. Ruta publicada de acceso extranjero individual, no admisión personal ni permiso migratorio.')

def source(label,url):return dict(title=label,url=url,checked=CHECKED)
def merge(p,items):p['sources']=list({s['url']:s for s in p['sources']+items}.values())
def candidate(status,detail):return dict(status=status,detail=detail)
def age_fit(lo,hi,start,skills=False):
 out={}
 for child,ages in [('matvey',[9,10] if start>='2027' else [9]),('oscar',[6,7] if start>='2027' else [6])]:
  if min(ages)>hi:state='not_eligible'
  elif max(ages)<lo:state='later'
  elif skills or min(ages)<lo or max(ages)>hi:state='conditional'
  else:state='candidate'
  text=T('На дату этой смены нужен опубликованный диапазон и соответствующий уровень. В конце 2026 семье известны возраста 9 и 6; в 2027 возможны 9–10 и 6–7, точные дни рождения неизвестны. Условия группы и место отдельно.',
   'Para esta sesión exige rango publicado y nivel correspondiente. A finales de 2026 familia conoce edades 9 y 6; en 2027 pueden ser 9–10 y 6–7, fechas exactas de nacimiento desconocidas. Condiciones de grupo y plaza aparte.')
  out[child]=candidate(state,text)
 return out
def base(ident,slug,provider,iso,country,place,themes):
 return dict(id=ident,slug=slug,provider=provider,iso=iso,country=country,place=place,themes=themes,formats=['day'],age='',programme='',language=UNKNOWN_LANG,confirmed_instruction_languages=[],language_evidence_role='unconfirmed',timing=dict(status='published_2026_27',label='',sessions=[],session_details=[],variant_keyed=True),price=dict(year=2026,currency='',amount=None,unit='programme',label='',included='',extras=TRIP,deposit=''),accommodation=T('Дневная программа без пансиона.','Programa diurno sin residencia.'),family_fit={c:candidate('conditional',NO_BOOKING) for c in ['matvey','oscar']},editorial_reason=T('Редакционный кандидат по содержанию, возрасту и прозрачности условий; независимый мировой рейтинг качества не установлен. Учебный проект / показ / сертификат не международная конкурсная медаль.',
  'Candidato editorial por contenido, edad y transparencia de condiciones; sin ranking mundial independiente de calidad acreditado. Proyecto / muestra / certificado educativo no es medalla competitiva internacional.'),shortlist=[],questions=[NO_BOOKING],sources=[],checked=CHECKED)
def add(p,start,end,key,label,price,url,days=None,begin=None,finish=None,zone=None,**extra):
 v=dict(start=start,end=end,variant_key=key,label=label,price=price,source=url,formats=p['formats'],date_scope='camp_session',**extra)
 if days and begin:v.update(date_scope='session_days',sessions=[lesson(day,begin,finish,zone,v.get('programme',p['programme'])) for day in days])
 p['timing']['sessions'].append([start,end]);p['timing']['session_details'].append(v)

ESF_META=[
 ('drama','Drama Loop',['art'],T('Сценическая речь, роли, музыка, движение и театральные поделки. Первая неделя Narnia, третья The Polar Express; финальный учебный показ, не внешнее театральное соревнование.',
  'Expresión escénica, roles, música, movimiento y manualidades teatrales. Primera semana Narnia, tercera The Polar Express; muestra educativa final, no concurso teatral externo.')),
 ('spanish','Winter Wonders in Spanish',['languages','culture'],T('Начальный испанский через зимние традиции, crafts, игры и лексику. Уверенно владеющим испанским детям сложность может быть недостаточной; полный день добавляет отдельный английский sports-блок.',
  'Español inicial mediante tradiciones invernales, crafts, juegos y vocabulario. Para niños con español sólido puede resultar demasiado básico; jornada completa añade bloque deportivo inglés separado.')),
 ('pokemon','Pokemon-Inspired STEAM Lab',['science','robotics','engineering'],T('Механические модели: bump-and-go робот, гидравлический подъёмник, плот и экологичный транспорт. Выбранный native-набор и PDF ограничены 6–8; общий анонс также пишет 6–9. Матвею 9: в опубликованные конкретные группы он не включён.',
  'Modelos mecánicos: robot bump-and-go, elevador hidráulico, balsa y transporte sostenible. Oferta native seleccionada y PDF limitados a 6–8; anuncio general también dice 6–9. Matvey tiene 9: no incluido en grupos concretos publicados.')),
 ('arcade','MakeCode Arcade · Pixel Game Studio',['coding','games'],T('Microsoft MakeCode Arcade: блоки, sprites, циклы, переменные, события, условия и работающая игра. Печатать код заранее не требуется. Нужен свой ноутбук / iPad, современный браузер, зарядка и международный адаптер.',
  'Microsoft MakeCode Arcade: bloques, sprites, bucles, variables, eventos, condiciones y juego funcional. Sin exigir escribir código previamente. Llevar portátil / iPad propio, navegador actualizado, cargador y adaptador internacional.')),
 ('minigame','Mini-Game Lab · Co-Op Creators',['coding','games'],T('HTML, CSS и JavaScript в браузере, совместная клавиатура двух игроков, логика и отладка. Описано 13 проектов и финальный Game Jam; это учебная демонстрация. Свой ноутбук обязателен, iPad не подходит.',
  'HTML, CSS y JavaScript en navegador, teclado compartido de dos jugadores, lógica y depuración. Se describen 13 proyectos y Game Jam final; muestra educativa. Portátil propio obligatorio, iPad no sirve.')),
 ('entrepreneur','Entrepreneur Launchpad',['entrepreneurship','technology'],T('Идея, проверка рынка, планирование затрат и цены, презентация, переговоры, UX / UI, сайт и маркетинг. Нужны собственные ноутбук и мышь. Лагерь не обещает реальных инвестиций или дохода.',
  'Idea, validación de mercado, costes y precios, presentación, negociación, UX / UI, web y marketing. Requiere portátil y ratón propios. Campamento sin prometer inversión real ni ingresos.')),
 ('spanish-fiesta','Fiesta de Navidad · Spanish Crafts & Treats',['languages','art'],T('Разовый испанский рождественский workshop с crafts и праздничными угощениями. Варианты разных дней / площадок не многодневный пансион.',
  'Workshop navideño de español de un día con crafts y dulces festivos. Opciones de días / sedes distintos no son residencia de varios días.')),
 ('magical','Primary Magical Winter Workshop',['languages','art'],T('Короткие английские зимние занятия: истории и творческие задания для младшей primary. Часы каждого отдельного билета сохранены; полный день присмотра не обещается.',
  'Clases invernales breves en inglés: historias y tareas creativas para primary menor. Horario de cada billete conservado; sin prometer cuidado de día entero.')),
 ('playtime','Merry and Bright Playtime',['languages','general'],T('Короткая англоязычная праздничная игровая программа для младших. Это отдельный workshop, а не вся зимняя смена.',
  'Programa festivo breve de juegos en inglés para menores. Workshop separado, no toda temporada invernal.')),
 ('santa','Storytime with Santa · Parent & Child',['languages','culture'],T('Рождественское чтение / общение на английском. Native-название билета прямо включает одного взрослого и одного ребёнка: родитель сопровождает, это не drop-off camp.',
  'Lectura / interacción navideña en inglés. Nombre native del billete incluye expresamente un adulto y un niño: adulto acompaña, no campamento drop-off.')),
 ('swimming','Swimming · SWC levels',['sport'],T('Каникулярные занятия плаванием по отдельным уровням SWC. Возрастной диапазон не доказывает нужный навык: требуется согласовать уровень / оценку. Часы короче полного дня лагеря.',
  'Clases vacacionales de natación en niveles SWC separados. Rango de edad no acredita habilidad necesaria: acordar nivel / evaluación. Horario menor que campamento de día completo.')),
 ('gymnastics','Gymnastics · GYC levels',['sport'],T('Каникулярная гимнастика по возрастным / учебным группам GYC. Техника, координация и движение; уровень и требования инструктора отдельно.',
  'Gimnasia vacacional en grupos GYC de edad / aprendizaje. Técnica, coordinación y movimiento; nivel y requisitos del instructor aparte.')),
 ('football','Football · FBC levels',['sport'],T('Каникулярные футбольные занятия по группам FBC, движения, владение мячом и игра в команде. Это спортивное обучение, не национальный чемпионат.',
  'Clases vacacionales de fútbol por grupos FBC, movimiento, control de balón y juego en equipo. Enseñanza deportiva, no campeonato nacional.')),
 ('multisports','Multi-Sports · Dry Camp',['sport','general'],T('Разные виды спорта, ловкость, координация и командные задания по группам SC. Dry Camp не включает водные занятия. Отдельный трёхчасовой блок не целый день присмотра.',
  'Deportes variados, agilidad, coordinación y tareas de equipo por grupos SC. Dry Camp sin sesiones acuáticas. Bloque separado de tres horas no es cuidado de día entero.')),
 ('basketball','Basketball · BBC levels',['sport'],T('Каникулярный баскетбол в возрастных группах BBC; навыки мяча и командная практика. Цена относится к расписанию курса, не к академическому пансиону.',
  'Baloncesto vacacional por grupos BBC de edad; habilidades de balón y práctica de equipo. Precio corresponde al horario del curso, no residencia académica.')),
 ('tennis','Tennis · TENC levels',['sport'],T('Каникулярные теннисные занятия по отдельным группам TENC. Инвентарь, спортивную обувь и уровень подготовки согласовать; часы и цену смотреть у конкретной площадки.',
  'Clases vacacionales de tenis por grupos TENC separados. Acordar material, calzado y nivel; consultar horario y tarifa de sede concreta.')),
]
SG_META=[
 ('kidz-economy',['entrepreneurship'],T('Kindness Economy для младших: деньги, накопления, выбор и общий рынок. Для старших описаны Smart Saver и Entrepreneurship: цели сбережений, бизнес-план, branding, прототип и pitch. Конкретный старший трек недели уточнить.',
  'Kindness Economy para menores: dinero, ahorro, elección y mercado compartido. Mayores: Smart Saver y Entrepreneurship, metas de ahorro, plan de negocio, branding, prototipo y pitch. Confirmar itinerario mayor de semana elegida.')),
 ('multi-activity',['general','sport','science'],T('Младшие возрастные группы: игры, спорт, creative play и практические задания. Не специализированная робототехническая команда и не лагерь для всех возрастов до подростков.',
  'Grupos de edad menores: juegos, deportes, creative play y tareas prácticas. No equipo especializado de robótica ni campamento para todas las edades adolescentes.')),
 ('little-clay-gardeners',['art','nature'],T('Творческая работа с глиной и природными темами для старшей группы. Это художественный каникулярный курс, не программа AI / робототехники.',
  'Creación con arcilla y temas naturales para grupo mayor. Curso artístico vacacional, no programa de AI / robótica.')),
 ('parkour',['sport'],T('Паркур, координация и движение под руководством тренеров; уровень и требования к обуви согласовать. Младший порог относится к возрасту на начало.',
  'Parkour, coordinación y movimiento guiados por entrenadores; acordar nivel y calzado. Edad mínima al inicio.')),
 ('super-gymnastics',['sport'],T('Гимнастика в отдельных возрастных группах; физическая координация и технические упражнения. Наличие мест в соседней группе не означает перевод без согласования.',
  'Gimnasia en grupos de edad separados; coordinación física y ejercicios técnicos. Plazas en grupo vecino no implican cambio sin acuerdo.')),
 ('junior-scientist',['science'],T('Практические научные опыты и исследование в младшей группе. Общая страница описывает и старших, но текущий зимний booking board предлагает только младший поток.',
  'Experimentos prácticos e investigación en grupo menor. Página general describe también mayores, pero booking board invernal actual solo ofrece grupo menor.')),
 ('fabric-hackerspace',['design','technology','entrepreneurship'],T('Product design и изготовление вещей: Affinity / Canva, логотип, Silhouette cutter, sewing machine и heat press; сумки, футболки, подушки и кружки. Название Hackerspace не означает курс кибербезопасности или электроники.',
  'Product design y fabricación: Affinity / Canva, logotipo, Silhouette cutter, sewing machine y heat press; bolsas, camisetas, cojines y tazas. Hackerspace no significa curso de ciberseguridad ni electrónica.')),
 ('future-city',['engineering','science','design'],T('Командные модели будущего города, изобретательство, дизайн и решение практических задач. Образец пятидневного timetable не добавляет несуществующий пятый день в опубликованный четырёхдневный декабрьский набор.',
  'Modelos de ciudad futura en equipo, invención, diseño y resolución de retos prácticos. Timetable ilustrativo de cinco días no añade quinto día inexistente a oferta de diciembre de cuatro días.')),
 ('drama-academy',['art'],T('Театр, движение и творческое выражение для младшей группы. Финальная презентация лагеря не внешняя конкурсная победа.',
  'Teatro, movimiento y expresión creativa para grupo menor. Presentación final de campamento no es victoria competitiva externa.')),
 ('music-explorers',['art','music'],T('Музыкальные и творческие занятия; младшая и старшая группы предлагаются в разные недели. Конкретную подготовку, инструменты и уровень согласовать.',
  'Actividades musicales y creativas; grupos menor y mayor ofrecidos en semanas distintas. Acordar preparación, instrumentos y nivel.')),
 ('conversational-english',['languages'],T('Английская разговорная практика, общение и командные задания. Это языковое развитие, не техническая специализация и не обязательная программа для уже уверенно говорящего ребёнка.',
  'Práctica conversacional inglesa, comunicación y tareas de equipo. Desarrollo lingüístico, no especialización técnica ni programa obligatorio para niño que ya habla con seguridad.')),
 ('passion-for-art',['art'],T('Изобразительное творчество и художественные проекты. Возрастные потоки чередуются по неделям; не считать их одновременной общей группой.',
  'Creación visual y proyectos artísticos. Grupos de edad alternan por semanas; no considerarlos grupo conjunto simultáneo.')),
 ('super-chef',['general','culture'],T('Практическая кулинария и кухонные навыки в отдельных возрастных группах. Обеим возрастным группам семьи есть зимние варианты; меню, аллергии и инструменты уточнить.',
  'Cocina práctica y habilidades culinarias en grupos de edad separados. Hay opciones invernales para ambos grupos familiares; confirmar menú, alergias y utensilios.')),
 ('super-swim',['sport'],T('Плавание и водные навыки в опубликованной старшей группе. Умение плавать / распределение по уровню согласовать; возраст сам по себе не подтверждает уровень.',
  'Natación y habilidades acuáticas en grupo mayor publicado. Acordar capacidad de nadar / nivel; edad no acredita habilidad por sí sola.')),
 ('super-basketball',['sport'],T('Баскетбольная техника, упражнения и командная игра в отдельных возрастных группах. Для Оскара в январе нужно проверить достижение нижнего порога.',
  'Técnica de baloncesto, ejercicios y juego de equipo en grupos de edad separados. En enero comprobar que Oscar cumpla edad mínima.')),
 ('super-soccer',['sport'],T('Футбол, координация, работа с мячом и командное взаимодействие. Возрастной поток выбирается отдельно для каждого ребёнка.',
  'Fútbol, coordinación, balón y cooperación en equipo. Elegir grupo de edad por separado para cada niño.')),
]

def make_profiles():
 evidence=json.loads((ROOT/'data/east-asia-winter-native-schedules-v159.json').read_text());out=[]
 for number,(kind,name,themes,programme) in enumerate(ESF_META,1208):
  rows=[v for v in evidence['esf_variants'] if v['kind']==kind]
  p=base('CP'+str(number),'esf-winter-'+kind,'ESF Explore · '+name,'HKG',T('Гонконг','Hong Kong'),T('Гонконг · площадка конкретного курса','Hong Kong · sede del curso concreto'),themes)
  p['age']=str(min(v['min_age'] for v in rows))+'–'+str(max(v['max_age'] for v in rows))+T(' · отдельные группы и уровни в вариантах',' · grupos y niveles separados en opciones')
  p.update(programme=programme,language=ESF_LANGUAGE,confirmed_instruction_languages=['EN','ES'] if kind in ['spanish','spanish-fiesta'] else ['EN'],language_evidence_role='bilingual' if kind in ['spanish','spanish-fiesta'] else 'primary')
  p['timing'].update(status='published_2026',label=T('Фактические варианты из действующего native course search: дата, часы, возраст, площадка, цена и опубликованные дни проверены отдельно. Полный день и отдельный блок — альтернативы, не независимые лагеря. Полного дня во вторую неделю нет в официальном PDF.',
   'Opciones reales de native course search vigente: fecha, horario, edad, sede, tarifa y días publicados cotejados por separado. Jornada completa y bloque separado son alternativas, no campamentos independientes. PDF oficial no ofrece jornada completa en segunda semana.'))
  p['price'].update(currency='HKD',unit='family_package' if kind=='santa' else 'programme',label=T('Тариф каждого курса указан в таблице вариантов; это цена всего опубликованного периода, не умножать повторно на число занятий. Full Day включает два учебных блока, но не еду.',
   'Tarifa de cada curso en tabla de opciones; precio de periodo publicado completo, sin multiplicar de nuevo por número de clases. Full Day incluye dos bloques educativos, pero no comida.'),included=T('Обучение / выбранные занятия. Для Pokémon личное оборудование не требуется; для coding и Entrepreneurship нужна собственная техника согласно программе.',
   'Enseñanza / clases elegidas. Pokémon sin equipo personal exigido; coding y Entrepreneurship requieren dispositivo propio según programa.'),extras=T('Full day 09–16: обеденный присмотр 12–13, но lunch, два перекуса и вода с собой; доставка еды, холодильник и микроволновка не предусмотрены. Спортивная обувь без следов; вход / выход и взрослое сопровождение младших согласовать. Ноутбук и адаптер для coding отдельно.',
   'Full day 09–16: supervisión de almuerzo 12–13, pero llevar lunch, dos meriendas y agua; sin entrega de comida, nevera ni microondas. Calzado deportivo que no marque; acordar acceso / recogida y acompañamiento adulto de menores. Portátil y adaptador para coding aparte.'),deposit=ESF_CANCEL)
  p['sources']=[source('Winter programme descriptions and devices',ESF),source('Explicit English instruction statement',ESF_EVENTS),source('Course administration and refunds',ESF_POLICY),source('Full-day matrix · visually checked',ESF_PDF),source('Parent instructions · lunch and care',ESF_PARENT)]
  p['questions'] += [T('Промокод ESF_WINTER10: 10% только full-day до 16 ноября 2026, 11:00 HKT; это срок промо, не дедлайн записи. Проверить совместимость / invoice; скидка не применена автоматически.',
   'Código ESF_WINTER10: 10% solo full-day hasta 16 de noviembre de 2026, 11:00 HKT; plazo promocional, no inscripción. Comprobar compatibilidad / invoice; sin descuento automático.'),T('Native capacity используется страницей как признак возможности добавления в корзину; это не подтверждённое число оставшихся мест. Приём не оформлен.',
   'Página usa native capacity como indicador de poder añadir a cesta; no es número confirmado de plazas restantes. Sin admisión tramitada.')]
  if kind=='santa':p['formats']=['family'];p['catalog_participation']='holiday_workshop'
  elif kind in ['spanish-fiesta','magical','playtime','swimming','gymnastics','football','basketball','tennis']:p['catalog_participation']='holiday_workshop'
  p['family_fit']=age_fit(min(v['min_age'] for v in rows),max(v['max_age'] for v in rows),'2026-12-01',kind=='swimming')
  for v in rows:
   key='native-'+'-'.join(str(x) for x in v['tuition_ids'])
   label=v['place']+' · '+str(v['min_age'])+'–'+str(v['max_age'])+' · '+('Full Day' if v['full'] else v['start_time']+'–'+v['end_time'])
   extra=dict(place=v['place'],age=str(v['min_age'])+'–'+str(v['max_age']),family_fit=age_fit(v['min_age'],v['max_age'],v['start'],kind=='swimming'))
   add(p,v['start'],v['end'],key,label,'HKD '+format(v['amount'],'g')+(T(' / один взрослый и один ребёнок',' / un adulto y un niño') if kind=='santa' else ''),ESF,v['days'],v['start_time'],v['end_time'],'Asia/Hong_Kong',**extra)
  out.append(p)
 for number,(key,themes,programme) in enumerate(SG_META,1224):
  native=next(v for v in evidence['sg_programmes'] if v['key']==key);slots=native['slots'];allgroups=[g for s in slots for g in s['age_groups']]
  p=base('CP'+str(number),'campasia-sg-winter-'+key,'Camp Asia Singapore · '+native['name'],'SGP',T('Сингапур','Singapur'),'Singapore · AIS / Stamford',themes)
  p.update(age=str(min(g[0] for g in allgroups))+'–'+str(max(g[1] for g in allgroups)),programme=programme,language=SG_LANGUAGE,confirmed_instruction_languages=['EN'],language_evidence_role='language_lessons' if key=='conversational-english' else 'primary')
  p['family_fit']=age_fit(min(g[0] for g in allgroups),max(g[1] for g in allgroups),'2026-12-01',key=='super-swim')
  p['timing']['label']=T('Опубликованы только реально выставленные возрастные потоки и недели. Декабрьские короткие недели содержат четыре дня, январская пять; рождественские / новогодние праздники не добавлены как занятия. Образец timetable не равен записи на любой трек в любую неделю.',
   'Solo grupos y semanas realmente ofertados. Semanas cortas de diciembre contienen cuatro días, enero cinco; festivos navideños / de Año Nuevo no añadidos como clases. Timetable de ejemplo no implica oferta de cualquier curso en cualquier semana.')
  p['price'].update(year=2026,season='2026/27',currency='SGD',label=T('Актуальная стоимость по каждой неделе и возрасту в вариантах. Booking board имеет приоритет над общей старой пятидневной примерной ценой; валюту / окончательный счёт подтвердить.',
   'Precio vigente por semana y edad en opciones. Booking board prevalece sobre precio genérico antiguo de ejemplo de cinco días; confirmar moneda / factura final.'),included=T('Обед, утренний и дневной перекусы, Camp Asia T-shirt, оборудование и учебные материалы перечислены как включённые. Свой ноутбук автоматически не добавляется в смету.',
   'Almuerzo, meriendas matinal y de tarde, Camp Asia T-shirt, equipo y material educativo enumerados como incluidos. Sin añadir automáticamente portátil propio al presupuesto.'),extras=T('Автобус отдельно; взять воду, головной убор и солнцезащиту, для водных занятий соответствующую одежду. Личная accident / medical insurance семьи отдельно. Скидки за братьев / сестёр не начислены.',
   'Autobús aparte; llevar agua, gorro y protector solar, ropa adecuada para actividades acuáticas. Accident / medical insurance personal familiar aparte. Sin aplicar descuento por hermanos.'),deposit=SG_CANCEL)
  p['sources']=[source('Actual winter booking board',SG_BOOK),source('Subject content and normal daily hours',native['url']),source('Primary language and welcome',SG_PROMISE),source('Foreign children and practical arrangements',SG_FAQ),source('Payment and cancellation',SG_TERMS)]
  for s in slots:
   lo=min(g[0] for g in s['age_groups']);hi=max(g[1] for g in s['age_groups'])
   add(p,s['start'],s['end'],'week-'+str(s['week']),native['name']+' · '+s['place'],'SGD '+str(s['amount']),SG_BOOK,weekdays(s['start'],s['end']),'09:00','15:00','Asia/Singapore',place=s['place'],age=' / '.join(str(a)+'–'+str(b) for a,b in s['age_groups']),family_fit=age_fit(lo,hi,s['start'],key=='super-swim'))
  out.append(p)
 hk=[('CP1240','coding','Cobo Minecraft Education',8,10,'2026-12-14','2026-12-18',3500,6500,'09:00','12:00',HK+'age-8-10-years-old/coding-ii/',['coding','games']),('CP1241','stem','STEM Explorers',6,7,'2026-12-28','2026-12-31',3200,5900,'09:00','12:00',HK+'age-4-to-7-years-old/stem-explorers/',['science','engineering']),('CP1242','robo','Robo-Tech Explorers',8,10,'2026-12-28','2026-12-31',3200,5900,'09:00','12:00',HK+'age-8-10-years-old/robo-tech-explorers/',['robotics','coding']),('CP1243','science','Science & Tech Explorers',8,10,'2026-12-21','2026-12-24',3200,5900,'12:30','15:30',HK+'age-8-10-years-old/science-and-tech-explorers/',['science','technology']),('CP1244','multi','Multi-Activity',4,7,'2026-12-14','2026-12-18',3500,6500,'09:00','12:00',HK+'age-4-to-7-years-old/multi-activity/',['general','sport','art'])]
 for ident,key,name,lo,hi,start,end,half,full,begin,finish,url,themes in hk:
  p=base(ident,'campasia-hk-winter-'+key,'Camp Asia Hong Kong · '+name,'HKG',T('Гонконг','Hong Kong'),'Stamford American School · Ho Man Tin',themes);p['age']=str(lo)+'–'+str(hi);p['family_fit']=age_fit(lo,hi,start)
  descriptions={
   'coding':T('Cobo Academy: Minecraft Education и MakeCode, построение интерактивных 3D-миров, автоматизация сооружений, circuits, наглядные физика и химия. Нужен iPad / Macbook / PC с установленным Minecraft Education и зарядкой; страница допускает заимствование устройства на кампусе, условия / наличие подтвердить.',
    'Cobo Academy: Minecraft Education y MakeCode, mundos 3D interactivos, automatizar construcciones, circuits, física y química visuales. Requiere iPad / Macbook / PC con Minecraft Education y cargador; página permite préstamo de dispositivo en campus, confirmar condiciones / disponibilidad.'),
   'stem':T('Научные эксперименты, блочное программирование, сборка моделей и 3D-моделирование для 6–7 лет; творческие командные задания и подвижные перерывы. Заголовок / URL старой страницы шире: допуск взят из актуальной таблицы конкретной смены.',
    'Experimentos científicos, programación por bloques, construir modelos y modelado 3D para 6–7 años; tareas creativas en equipo y pausas activas. Título / URL antiguos más amplios: admisión tomada de tabla vigente de sesión concreta.'),
   'robo':T('Проектирование, сборка и программирование роботов, включая Vexgo; командное решение задач и внутренние испытания роботов. Внутренний турнир лагеря не квалификация VEX и не международная конкурсная медаль.',
    'Diseñar, construir y programar robots, incluido Vexgo; resolver retos en equipo y pruebas internas de robots. Torneo interno del campamento no es clasificatorio VEX ni medalla competitiva internacional.'),
   'science':T('Практические эксперименты с технологиями и природными материалами, science, coding и robotics; design-based thinking. Точный недельный проект / модель оборудования не опубликованы, не обещать конкретный роботокомплект.',
    'Experimentos prácticos con tecnología y materiales naturales, science, coding y robotics; design-based thinking. Proyecto semanal / modelo de equipo exactos sin publicar, sin prometer kit robótico concreto.'),
   'multi':T('Art / crafts, театральные игры, движение, командные и творческие задания. Темы недель: Winter Engineer, Winter Celebrations, Winter Animals. Название первой недели не означает отдельный технический курс или роботолигу.',
    'Art / crafts, juegos teatrales, movimiento, retos creativos y de equipo. Temas semanales: Winter Engineer, Winter Celebrations, Winter Animals. Nombre de primera semana no implica curso técnico separado ni liga robótica.')}
  p['programme']=descriptions[key]+T(' Полный день соединяет выбранные AM и PM блоки одной недели / возраста; это не целый день одного технического предмета.',
   ' Jornada completa combina bloques AM y PM elegidos de misma semana / edad; no día entero de una sola materia técnica.')
  p.update(language=T('На конкретных страницах STEM, Robo-Tech, Science & Tech и Multi-Activity прямо заявлено: все лагеря проводятся на английском; Coding отдельно подтверждает English у Cobo Academy. Язык подтверждён текстом программ, а не языком сайта.',
   'Páginas concretas STEM, Robo-Tech, Science & Tech y Multi-Activity declaran expresamente todos los campamentos en inglés; Coding confirma English de Cobo Academy por separado. Idioma acreditado por texto de programas, no por idioma de web.'),confirmed_instruction_languages=['EN'],language_evidence_role='primary')
  p['timing'].update(status='published_2026',label=T('Даты сопоставлены с текущим Winter Camp Schedule 2026. AM 09–12, PM 12:30–15:30, full 09–15:30 с отдельным обеденным промежутком; не переносить часы ESF на Camp Asia.',
   'Fechas cotejadas con Winter Camp Schedule 2026 vigente. AM 09–12, PM 12:30–15:30, full 09–15:30 con pausa de almuerzo; no trasladar horarios ESF a Camp Asia.'))
  p['price'].update(currency='HKD',label=T('Пять дней: half HKD 3500, full 6500; четыре дня: half 3200, full 5900. Полный день требует выбора доступного второго блока той же возрастной группы и недели.',
   'Cinco días: half HKD 3500, full 6500; cuatro días: half 3200, full 5900. Jornada completa exige elegir segundo bloque disponible de misma edad y semana.'),included=T('Выбранные занятия; точные включения техники по треку уточнить.','Clases elegidas; confirmar inclusiones de equipo del itinerario.'),extras=T('Обед / перекусы / вода с собой; для full day предусмотрен lunch supervision, еда не включена. Личная accident / medical insurance отдельно; окончательный invoice и акции уточнить.',
   'Llevar almuerzo / meriendas / agua; full day ofrece lunch supervision, comida no incluida. Accident / medical insurance personal aparte; confirmar invoice final y promociones.'),deposit=HK_CANCEL)
  p['sources']=[source('Specific winter course and fee table',url),source('Current cross-programme timetable',HK_SCHEDULE),source('Camp-specific terms',HK_TERMS),source('Practical camp FAQ',HK_FAQ)]
  slots=[(start,end,half,full)] if key!='multi' else [('2026-12-14','2026-12-18',3500,6500),('2026-12-21','2026-12-24',3200,5900),('2026-12-28','2026-12-31',3200,5900)]
  for a,b,h,f in slots:
   options=[('half',begin,finish,h),('full','09:00','15:30',f)] if key!='multi' else [('am','09:00','12:00',h),('pm','12:30','15:30',h),('full','09:00','15:30',f)]
   for variant,bs,es,amount in options:
    add(p,a,b,a.replace('-','')+'-'+variant,name+' · '+variant.upper(),'HKD '+str(amount),url,weekdays(a,b),bs,es,'Asia/Hong_Kong')
  if key=='science':p['questions'].append(T('Конфликт подписи тарифа: дата и общая таблица говорят Week 2, но ценовая ячейка пишет Week 3. Сумму за выбранную неделю подтвердить до оплаты.',
   'Conflicto de etiqueta de tarifa: fecha y tabla general dicen Week 2, pero celda de precio dice Week 3. Confirmar importe de semana elegida antes de pagar.'))
  out.append(p)
 p=base('CP1245','good-good-qingpu-winter-2027','Good Good English · Winter Camp 2027','TWN',T('Тайвань','Taiwán'),'Qingpu · Taoyuan',['languages','general','sport','art','entrepreneurship'])
 p.update(age='Grades 1–6',programme=T('Десять реальных дней: pickleball, junior golf, ice skating, международная кухня и art; затем Junior Chef, Little Artist, Junior Tailor, Marketing Master, Little CEO и Market Day. Это общий англоязычный отдых / знакомство с профессиями, не техническая роботолига.',
  'Diez días reales: pickleball, junior golf, ice skating, cocina internacional y art; después Junior Chef, Little Artist, Junior Tailor, Marketing Master, Little CEO y Market Day. Vacaciones generales en inglés / profesiones, no liga técnica robótica.'),language=T('Оператор прямо описывает полностью английскую среду весь день и использование English в общении с преподавателями и сверстниками.',
  'Operador describe expresamente entorno íntegramente inglés durante el día y uso de English con docentes y compañeros.'),confirmed_instruction_languages=['EN'],language_evidence_role='primary')
 p['family_fit']={c:candidate('conditional',GRADE) for c in ['matvey','oscar']}
 p['timing'].update(status='published_2027',label=T('21 января–3 февраля 2027: десять будних дней прямо перечислены на постере. Присутствие 09:30–16:00; обед / отдых 11:30–13:30 и snack 15:30–16:00 входят во время, а не в технические учебные часы. Отдельные пятидневные билеты не опубликованы.',
  '21 de enero–3 de febrero de 2027: diez días laborables enumerados en póster. Presencia 09:30–16:00; almuerzo / descanso 11:30–13:30 y snack 15:30–16:00 incluidos en horario, no horas técnicas lectivas. Sin billetes separados de cinco días publicados.'))
 p['price'].update(year=2027,currency='TWD',amount=22000,label=T('NTD 22000 за десять дней; early bird 19800 до 20 ноября 2026. Дополнительные 1000 только действующим / бывшим ученикам или записанным на следующий семестр, семье автоматически не применены.',
  'NTD 22000 por diez días; early bird 19800 hasta 20 de noviembre de 2026. Otros 1000 solo alumnos actuales / anteriores o inscritos próximo semestre, sin aplicar automáticamente a familia.'),included=T('Объявлена десятидневная программа; питание, поездки, прокат, материалы и страховку включёнными без invoice не считать.',
  'Programa de diez días anunciado; no dar comida, excursiones, alquiler, materiales ni seguro por incluidos sin invoice.'),deposit=T('Возвраты, аванс, способ оплаты, точный адрес Qingpu и иностранный индивидуальный доступ не опубликованы в прочитанных winter / FAQ; согласовать отдельно.',
  'Devoluciones, depósito, pago, dirección exacta Qingpu y acceso extranjero individual sin publicar en winter / FAQ leídos; acordar aparte.'))
 p['sources']=[source('Winter 2027 · prices and English throughout',GOOD),source('Ten-day poster · visually checked',GOOD_POSTER),source('Teaching environment and campus access','https://goodgoodenglish.com/en/faq-en/')]
 add(p,'2027-01-21','2027-02-03','ten-days','10-day programme','NTD 22000 / early 19800',GOOD,weekdays('2027-01-21','2027-02-03'),'09:30','16:00','Asia/Taipei');out.append(p)
 p=base('CP1246','gmi-malaysia-winter-2027','KTI / STARK · GMI Overseas Tech Camp · '+T('набор заполнен','grupo completo'),'MYS',T('Малайзия','Malasia'),'GMI · Kajang, Selangor',['robotics','ai','coding','engineering']);p['formats']=['boarding'];p['age']='10–15'
 p.update(programme=T('Пять учебных дней 22–26 января, включая выходные: двигатели / EV, collaborative robot и мобильный робот, 3D-печать, AI-видео, информационная безопасность и итоговое выступление. Опасное промышленное оборудование только демонстрируется; hands-on объём по утверждённой программе. GMI Certificate of Attendance не международная конкурсная медаль.',
  'Cinco días lectivos 22–26 de enero, incluidos fines de semana: motores / EV, collaborative robot y robot móvil, impresión 3D, vídeo AI, seguridad informática y presentación. Equipos industriales peligrosos solo demostrados; práctica según programa aprobado. GMI Certificate of Attendance no es medalla competitiva internacional.'),language=T('Пять учебных дней в GMI полностью на английском; требуется базовое разговорное владение. Тайваньские сопровождающие помогают на китайском, их ночную / бытовую поддержку на EN для семьи отдельно согласовать.',
  'Cinco días lectivos en GMI íntegramente en inglés; exige conversación básica. Acompañantes taiwaneses apoyan en chino, confirmar atención nocturna / cotidiana EN para familia.'),confirmed_instruction_languages=['EN'],language_evidence_role='primary')
 p['family_fit']=age_fit(10,15,'2027-01-21');p['questions'].append(T('На связанной организатором странице прямо 報名額滿: набор заполнен. Лист ожидания / дополнительный набор не обещан. Матвей допускается по возрасту только после десятилетия; иностранный ребёнок в тайваньской группе ещё не принят.',
  'Página enlazada por organizador dice expresamente 報名額滿: grupo completo. Sin lista de espera / grupo adicional prometidos. Matvey cumple edad solo tras décimo cumpleaños; niño extranjero en grupo taiwanés aún sin admitir.'))
 p['timing'].update(status='published_2027',label=T('21–29 января 2027 — девятидневная поездка из Тайваня, из них GMI 22–26 января 09:00–17:30. Проживание и учебные дни различаются; из-за заполненного набора исключено из рабочего календаря.',
  '21–29 de enero de 2027 — viaje de nueve días desde Taiwán, GMI 22–26 de enero 09:00–17:30. Estancia y clases distintas; excluido del calendario operativo por grupo completo.'))
 p['price'].update(year=2027,currency='TWD',amount=99000,unit='participant',label=T('NTD 99000 на ученика за девятидневный пакет. Набор заполнен, цена не означает доступное место.',
  'NTD 99000 por alumno por paquete de nueve días. Grupo completo, precio no implica plaza disponible.'),included=T('Заявлены перелёт из Тайваня, двухместное проживание, еда, местный транспорт, GMI курс, все практические материалы и подготовка перед выездом.',
  'Se anuncian vuelo desde Taiwán, habitación doble, comida, transporte local, curso GMI, todo material práctico y preparación previa.'),extras=T('Прилёт семьи в Тайвань, документы / страховые исключения и расходы родителей отдельно; цену на отправление из Коста-Рики не переносить.',
  'Llegada familiar a Taiwán, documentos / exclusiones del seguro y gastos parentales aparte; no trasladar precio a salida desde Costa Rica.'),deposit=T('Подробный аванс / отмену и страховой полис запросить до будущего договора; заявки и согласия не отправлялись.',
  'Obtener depósito / cancelación detallados y póliza antes de contrato futuro; sin solicitudes ni consentimientos.'))
 p['accommodation']=T('Mercure Kuala Lumpur Trion, два ученика в комнате; сопровождающие проживают в том же отеле. Заявлено не менее одного ассистента на четырёх учеников; это утверждение организатора, не независимый аудит.',
  'Mercure Kuala Lumpur Trion, dos alumnos por habitación; acompañantes alojados en mismo hotel. Se declara al menos un asistente por cuatro alumnos; afirmación del organizador, no auditoría independiente.')
 p['sources']=[source('Linked organiser page · sold out, full price and actual teaching days',GMI),source('STARK official winter programme link',STARK)]
 add(p,'2027-01-21','2027-01-29','boarding','Taiwan → Malaysia · 9 days','NTD 99000',GMI,availability=dict(status='closed',label=T('Набор заполнен; дополнительное место не подтверждено.','Grupo completo; sin plaza adicional confirmada.')));out.append(p)
 for ident,kind,name,grade,fee in [('CP1247','eureka','Eureka','Y1–Y3 / KG–G2',10800),('CP1248','ted-junior','TED Junior','Y4–Y6 / G3–G5',13800),('CP1249','medicine','Little Medical School','Reception–Y5 / KG–G3 · '+T('границы групп расходятся','límites de grupos discrepantes'),6600),('CP1250','sensetime','SenseTime AI & Future Tech','12–16',23800)]:
  iso='HKG' if kind=='sensetime' else 'CHN';p=base(ident,'eimx-winter-'+kind,'EIMx · '+name,iso,T('Гонконг','Hong Kong') if iso=='HKG' else T('Китай','China'),'Hong Kong' if iso=='HKG' else 'Beijing / Shanghai',['ai','coding','technology'] if kind=='sensetime' else ['science'] if kind=='medicine' else ['languages','entrepreneurship'])
  p['age']=grade;p['family_fit']=age_fit(12,16,'2027-01-25') if kind=='sensetime' else {c:candidate('conditional',GRADE) for c in ['matvey','oscar']}
  desc={
   'eureka':T('Наблюдение, обсуждение, планирование и самостоятельная / групповая презентация. Темы младших: повседневная экономика и космос. До восьми учеников; точный класс и English proficiency proof / короткое интервью для внешних учеников.',
    'Observación, discusión, planificación y presentación individual / grupal. Temas menores: economía cotidiana y espacio. Hasta ocho alumnos; curso real y English proficiency proof / entrevista breve para externos.'),
   'ted-junior':T('Исследование темы, структура, письменный черновик и репетиция оригинальной речи на английском. Темы экономики / финансов и мировых вопросов; до восьми учеников. Это учебный speech camp, не официальный TED конкурс или международная медаль.',
    'Investigar tema, estructura, borrador y ensayo de discurso original en inglés. Temas económicos / financieros y mundiales; hasta ocho alumnos. Speech camp educativo, no concurso TED oficial ni medalla internacional.'),
   'medicine':T('Mind Craft: эмоции, чувства, память, зрение и научные эксперименты; Little Scouts: очистка воды, первая помощь, ориентирование и сигналы. Два тематических курса не привязаны достоверно к каждой из противоречивых дат.',
    'Mind Craft: emociones, sentidos, memoria, visión y experimentos; Little Scouts: purificar agua, primeros auxilios, orientación y señales. Dos temas sin asignación fiable a cada fecha contradictoria.'),
   'sensetime':T('AI / AGI, нейросети, Transformers, LLM, prompting и собственный AIGC-проект; нужны основы Python и личный Windows-ноутбук. Визиты в университеты и SenseTime зависят от подтверждённых бронирований. Сертификат программы не мировая соревновательная награда.',
    'AI / AGI, redes neuronales, Transformers, LLM, prompting y proyecto AIGC propio; exige bases de Python y portátil Windows propio. Visitas universitarias y SenseTime sujetas a reservas confirmadas. Certificado de programa no es premio competitivo mundial.')}
  p.update(programme=desc[kind],language=T('English прямо указан в конкретной программе; для внешних учеников может требоваться подтверждение уровня / интервью. Институциональный campus visit не поступление в университет.',
   'English indicado expresamente en programa concreto; externos pueden necesitar prueba de nivel / entrevista. Campus visit institucional no es admisión universitaria.'),confirmed_instruction_languages=['EN'],language_evidence_role='primary')
  p['price'].update(year=2027 if kind=='sensetime' else 2026,currency='CNY',amount=fee,label='RMB '+str(fee)+T(' standard; скидки EiM / early bird не применены семье.',
   ' estándar; sin aplicar a familia descuentos EiM / early bird.'),included=T('Объявленная программа; точные питание, материалы, налоги и страхование согласовать.',
   'Programa anunciado; acordar comida, material, impuestos y seguro exactos.'),deposit=T('Публичная полная шкала аванса / возвратов для выбранного заезда не установлена. Interest form не резервирует доказанное место; форма не отправлялась.',
   'Escala pública completa de depósito / devoluciones para estancia elegida sin acreditar. Interest form no prueba plaza reservada; sin enviar formulario.'))
  p['sources']=[source('Current programme announcement',DULWICH),source('Winter 2026–27 brochure · tables visually checked',DUL_PDF)]
  if kind=='medicine':
   p['timing'].update(status='partial_2026_27',label=T('КОНФЛИКТ: HTML 19–23 декабря 2026 и 25–29 января 2026; PDF 21–25 / 27–31 декабря 2026 и 25–29 января 2027. Школьные группы также различаются. Пока нет подтверждённой смены в календаре; январь автоматически не исправлен на новый год.',
    'CONFLICTO: HTML 19–23 de diciembre de 2026 y 25–29 de enero de 2026; PDF 21–25 / 27–31 de diciembre de 2026 y 25–29 de enero de 2027. Grupos escolares también distintos. Sin sesión confirmada en calendario; enero no corregido automáticamente a año nuevo.'))
   p['questions'].append(p['timing']['label'])
  elif kind=='sensetime':
   p['formats']=['boarding'];p['timing'].update(status='published_2027',label=T('PDF прямо объявляет 25–31 января 2027, семь дней проживания. HTML всё ещё показывает отдельный октябрьский набор 2026: не выдан за зимнее расписание.',
    'PDF anuncia expresamente 25–31 de enero de 2027, siete días residenciales. HTML aún muestra periodo separado de octubre de 2026: no presentado como calendario invernal.'))
   p['accommodation']=T('Отель в Гонконге, по описанию Trip.com Four-Diamond, обычно по два / три ученика в комнате; фактический отель и включения подтвердить. Текст PDF всё ещё упоминает National Day holiday — сезонные детали требуют уточнения.',
    'Hotel en Hong Kong descrito como Trip.com Four-Diamond, normalmente dos / tres alumnos por habitación; confirmar hotel real e inclusiones. PDF aún menciona National Day holiday: aclarar detalles de temporada.')
   add(p,'2027-01-25','2027-01-31','boarding','SenseTime · 7-day residential','RMB 23800 standard',DUL_PDF)
  else:
   p['timing'].update(status='published_2026',label=T('Shanghai 14–18 декабря и Beijing 26–30 декабря 2026, по пять дней. Расписание 09–16 в брошюре примерное, поэтому UTC-занятия не придуманы. В Shanghai конкретный Dulwich / Dehong campus уточнить.',
    'Shanghai 14–18 de diciembre y Beijing 26–30 de diciembre de 2026, cinco días cada uno. Horario 09–16 de folleto ilustrativo, sin inventar clases UTC. Confirmar campus Dulwich / Dehong concreto en Shanghai.'))
   for a,b,city in [('2026-12-14','2026-12-18','Shanghai'),('2026-12-26','2026-12-30','Beijing')]:add(p,a,b,city.lower(),name+' · '+city,'RMB '+str(fee)+' standard',DULWICH,place=city)
  out.append(p)
 return out

def update_report(report):
 rows={p['id']:p for p in report['profiles']};evidence=json.loads((ROOT/'data/east-asia-winter-native-schedules-v159.json').read_text())
 for ident in ['CP069','CP070','CP071','CP072']:
  p=rows[ident];p.update(checked=CHECKED,language=SG_LANGUAGE,confirmed_instruction_languages=['EN'],language_evidence_role='primary');merge(p,[source('Current English-primary promise',SG_PROMISE),source('International individual route',SG_FAQ),source('Winter booking board',SG_BOOK)])
 p=rows['CP069'];p['timing']['status']='published_2026';p['timing']['label']=T('В действующем зимнем board Robotics 6–8 только 21–24 декабря, Robotics 9–12 только 28–31 декабря 2026. Оба ребёнка не записываются в одну общую роботосмену. Старый октябрь сохранён как история, не ближайший набор.',
  'Board invernal actual: Robotics 6–8 solo 21–24 de diciembre, Robotics 9–12 solo 28–31 de diciembre de 2026. Niños no se inscriben en una sesión robótica conjunta. Octubre antiguo conservado como historia, no próxima oferta.')
 p['price'].update(year=2026,currency='SGD',amount=655,label=T('Текущий зимний board SGD 655 за четыре дня / ребёнка; общая страница с 725 за пять дней не заменяет этот тариф.',
  'Board invernal vigente SGD 655 por cuatro días / niño; página general con 725 por cinco días no sustituye esta tarifa.'),deposit=SG_CANCEL)
 p['family_fit']=age_fit(6,12,'2026-12-21')
 for s in next(x for x in evidence['sg_programmes'] if x['key']=='robotics')['slots']:
  if [s['start'],s['end']] in p['timing']['sessions']:continue
  lo,hi=s['age_groups'][0];v=dict(start=s['start'],end=s['end'],label='Robotics '+str(lo)+'–'+str(hi),price='SGD 655 / 4 days',source=SG_BOOK,place=s['place'],formats=['day'],date_scope='session_days',age=str(lo)+'–'+str(hi),family_fit=age_fit(lo,hi,s['start']),sessions=[lesson(day,'09:00','15:00','Asia/Singapore',p['programme']) for day in weekdays(s['start'],s['end'])])
  p['timing']['sessions'].append([s['start'],s['end']]);p['timing'].setdefault('session_details',[]).append(v)
 # A corroborated Shanghai reschedule keeps the published ID and calendar UID.
 p=rows['CP709'];p['checked']=CHECKED;p['timing']['label']=T('Beijing 19–24 декабря 2026; Shanghai 27 декабря 2026–1 января 2027. HTML и новая PDF-обложка согласуются. Старое Shanghai 26–31 декабря исправлено; идентификатор сохранён для обновления календаря.',
  'Beijing 19–24 de diciembre de 2026; Shanghai 27 de diciembre de 2026–1 de enero de 2027. HTML y portada PDF nueva coinciden. Shanghai antiguo 26–31 de diciembre corregido; identificador conservado para actualizar calendario.')
 p['timing']['sessions']=[['2026-12-19','2026-12-24'],['2026-12-27','2027-01-01']]
 for i,v in enumerate(p['timing']['session_details']):
  v.update(start=p['timing']['sessions'][i][0],end=p['timing']['sessions'][i][1],place='Beijing' if i==0 else 'Shanghai',date_scope='camp_session',proof=p['timing']['label'],price='RMB 14800 standard; PDF student 13350 / expired early 12850')
  v.pop('attendance_weekdays',None)
  if i==1:v['catalogue_id']='CP709-20261226-20261231-dec26'
 p['price']['label']=T('Standard RMB 14800. PDF: student 13350, early 12850; HTML называет 12850 student и срок 31 октября. Льготный тариф противоречив / прежний срок прошёл, семье не применён.',
  'Estándar RMB 14800. PDF: student 13350, early 12850; HTML llama 12850 student con plazo 31 de octubre. Tarifa reducida contradictoria / plazo anterior vencido, sin aplicar a familia.')
 p['family_fit']={c:candidate('later',T('Минимум 11; в конце 2026 детям 9 и 6, оба ниже порога.',
  'Mínimo 11; a finales de 2026 niños de 9 y 6, ambos menores del mínimo.')) for c in ['matvey','oscar']};merge(p,[source('Updated city-specific announcement',DULWICH),source('Updated winter brochure · reschedule corroborated',DUL_PDF)])
 # A formerly listed departure is not silently kept as a confirmed future trip.
 p=rows['CP710'];p['checked']=CHECKED
 p['timing'].update(status='partial_2027',label=T('В текущих HTML / PDF только 26 января–4 февраля и 11–20 февраля 2027. Прежний декабрьский выезд больше не подтверждён; не объявлен отменённым, оставлен отдельной недатированной записью наблюдения.',
  'HTML / PDF actuales solo indican 26 de enero–4 de febrero y 11–20 de febrero de 2027. Salida de diciembre anterior sin corroborar ahora; no declarada cancelada, conservada como registro de seguimiento sin fecha operativa.'))
 p['timing']['sessions']=[['2027-01-26','2027-02-04'],['2027-02-11','2027-02-20']]
 p['timing']['session_details']=[v for v in p['timing']['session_details'] if v['start']>='2027']
 note=T('22–31 декабря 2026 было опубликовано в прежнем источнике. В действующих HTML и PDF такого выезда нет: дату убрали из рабочего календаря, отмена не доказана. До новой публикации не покупать поездку по старой дате; ранее импортированную копию календаря проверить отдельно.',
  '22–31 de diciembre de 2026 publicado en fuente anterior. HTML y PDF vigentes no muestran esa salida: fecha retirada del calendario operativo, cancelación sin acreditar. No comprar viaje con fecha antigua hasta anuncio nuevo; revisar copia de calendario importada previamente por separado.')
 p['timing']['unconfirmed_previous']=[dict(catalogue_id='CP710-20261222-20261231-dec22',start='2026-12-22',end='2026-12-31',label=T('Прежняя декабрьская дата · подтверждение ожидается','Fecha de diciembre anterior · pendiente de corroborar'),note=note)]
 p['questions']=[s for s in p['questions'] if s!=note]+[note]
 p['price']['label']=T('PDF: RMB 43000 standard, 41800 EiM student, 40800 early; HTML ещё показывает indicative 40800 со сроком 31 октября. Единица тарифа ребёнок / взрослый / семья не установлена; не умножать автоматически.',
  'PDF: RMB 43000 estándar, 41800 EiM student, 40800 early; HTML aún muestra indicative 40800 con plazo 31 de octubre. Unidad niño / adulto / familia sin establecer; no multiplicar automáticamente.')
 p['price']['unit']='unconfirmed'
 for v in p['timing']['session_details']:v.update(price='RMB 43000 standard / 41800 EiM / 40800 early; '+T('единица тарифа неизвестна','unidad de tarifa desconocida'),proof=p['timing']['label'])
 p['family_fit']=age_fit(6,17,'2027-01-26');merge(p,[source('Current remaining departures',DULWICH),source('Brochure · current dates and fee categories',DUL_PDF)])
 for ident,url in [('CP075','https://www.english-adventure.org/en/winter/'),('CP284','https://steamsquad.io/en/camps/expedition27')]:
  p=rows[ident];p['checked']=CHECKED;merge(p,[source('Current season, fees and restrictions re-read',url)])
 merge(rows['CP075'],[source('Current availability by actual programme','https://www.english-adventure.org/en/availability/')])
 p=rows['CP1013'];p['checked']=CHECKED;merge(p,[source('HIF own current Winter Camp 2027','https://hif.ch/camps/winter-camp-2027/'),source('Partner brochure · differing package date',DUL_PDF)])
 hif_note=T('HIF собственная страница по-прежнему 10–20 февраля 2027; партнёрская EIMx обложка 9–19 февраля при той же CHF 4586. Для прямого HIF заезда сохранена дата самой школы; условия партнёрского пакета и трансферов согласовать отдельно.',
  'Página propia HIF sigue indicando 10–20 de febrero de 2027; portada EIMx asociada dice 9–19 de febrero con mismos CHF 4586. Para estancia HIF directa se conserva fecha del colegio; acordar paquete del socio y traslados por separado.')
 if hif_note not in p['questions']:p['questions'].append(hif_note)
 new=make_profiles();index={p['id']:p for p in new};old={p['id'] for p in report['profiles']}
 report['profiles']=[index.get(p['id'],p) for p in report['profiles']]+[p for p in new if p['id'] not in old]
 report['counts'].update(dossiers=len(report['profiles']),countries=len({p['iso'] for p in report['profiles']}),by_status=dict(Counter(p['timing']['status'] for p in report['profiles'])),source_urls=len({s['url'] for p in report['profiles'] for s in p['sources']}))
 report['countries']=[dict(country=c,count=n) for c,n in sorted(Counter(p['country'] for p in report['profiles']).items())]
 report.update(version=159,asof=CHECKED)

def enrich_v159(d):
 # Closed intake stays researched, but is not an active family application route.
 for e in d['events']:
  if e.get('camp_programme_id')=='CP1246':e['priority']=T('P4 — набор заполнен','P4 — grupo completo');e['registration_status']=T('Набор заполнен; лист ожидания не подтверждён.','Grupo completo; lista de espera sin confirmar.')
 offers=[]
 def offer(ident,slug,label,currency,amounts,sessions,sources,gate,**extra):
  offers.append(dict(id=ident,slug=slug,label=label,currency=currency,price_year=2027 if all(a>='2027' for a,b in sessions) else 2026,format=extra.pop('format','day'),children=list(amounts),base_by_child=amounts,discount_second=0,required=[],unknown_required=extra.pop('unknown_required',[]),optional=extra.pop('optional',[]),unknown_trip=['travel','lodging','misc'],sessions=sessions,sources=sources,checked=CHECKED,gate=gate,included=extra.pop('included',T('Опубликованная часть стоимости; включения по досье.','Parte publicada del coste; inclusiones según ficha.')),deposit_note=extra.pop('deposit_note',NO_BOOKING),scope=extra.pop('scope',TRIP),**extra))
 pairs=[('dec14','super-chef','super-chef',800,800,'2026-12-14','2026-12-18'),('dec21','fabric-hackerspace','robotics',730,655,'2026-12-21','2026-12-24'),('dec28','robotics','future-city',655,705,'2026-12-28','2026-12-31'),('jan04','kidz-economy','junior-scientist',780,730,'2027-01-04','2027-01-08')]
 for key,mat,osc,ma,oa,a,b in pairs:
  slug='campasia-robotics' if mat=='robotics' else 'campasia-sg-winter-'+mat
  offer('campasia-sg-siblings-'+key+'-2026-27',slug,'Camp Asia Singapore · '+mat+' + '+osc,'SGD',dict(matvey=ma,oscar=oa),[[a,b]],[SG_BOOK,SG_PROMISE,SG_FAQ,SG_TERMS]+[x['url'] for x in json.loads((ROOT/'data/east-asia-winter-native-schedules-v159.json').read_text())['sg_programmes'] if x['key'] in [mat,osc]],T('Два ребёнка в разных подходящих возрастных группах на одной площадке. Это альтернативные недельные каникулы, не обязательный месячный маршрут. English и иностранный доступ опубликованы, персональные места не подтверждены.',
   'Dos niños en grupos de edad adecuados separados en misma sede. Alternativas de vacaciones semanales, no itinerario mensual obligatorio. English y acceso extranjero publicados, plazas personales sin confirmar.'),deposit_note=SG_CANCEL,included=T('Лабораторное / учебное оборудование, обед, два перекуса и T-shirt включены. Автобус, личная страховка и поездка семьи отдельно.',
   'Equipo educativo / de laboratorio, almuerzo, dos meriendas y T-shirt incluidos. Autobús, seguro personal y viaje familiar aparte.'),child_slugs=dict(matvey=slug,oscar='campasia-robotics' if osc=='robotics' else 'campasia-sg-winter-'+osc))
 for key,ma,oa,a,b in [('week1',8625,8625,'2026-12-14','2026-12-18'),('week3',6900,6900,'2026-12-28','2026-12-31')]:
  total=ma+oa
  offer('esf-games-siblings-'+key+'-2026','esf-winter-minigame','ESF · Mini-Game + MakeCode · Full Day','HKD',dict(matvey=ma,oscar=oa),[[a,b]],[ESF,ESF_PDF,ESF_POLICY],T('Матвей 9: Mini-Game 9–11; Оскар 6: MakeCode 6–8, full-day sport в соответствующей возрастной группе. Выбрать одну общую площадку KJS либо RC; отдельные младшие/старшие группы и места подтвердить.',
   'Matvey 9: Mini-Game 9–11; Oscar 6: MakeCode 6–8, deporte full-day en grupo de edad correspondiente. Elegir misma sede KJS o RC; confirmar grupos menores / mayores separados y plazas.'),optional=[dict(id='winter10',amount=-total*0.1,label=T('Промо 10% full-day, только при применимости до 16 ноября 2026 11:00 HKT','Promoción 10% full-day, solo si aplicable antes del 16 de noviembre de 2026 11:00 HKT'))],deposit_note=ESF_CANCEL,included=T('Двум детям полный день 09–16 в опубликованные дни недели, с lunch supervision, но без еды и персональных ноутбуков.',
   'Jornada completa 09–16 para ambos niños en días publicados de semana, con lunch supervision, pero sin comida ni portátiles personales.'))
 for kind,amount in [('half',3200),('full',5900)]:
  offer('campasia-hk-siblings-'+kind+'-dec2026','campasia-hk-winter-robo','Camp Asia Hong Kong · Robo-Tech + STEM · '+kind.upper(),'HKD',dict(matvey=amount,oscar=amount),[['2026-12-28','2026-12-31']],[HK+'age-8-10-years-old/robo-tech-explorers/',HK+'age-4-to-7-years-old/stem-explorers/',HK_SCHEDULE,HK_TERMS],T('Матвей 9: Robo-Tech 8–10; Оскар 6: STEM 6–7, одна площадка Stamford Ho Man Tin, четыре дня. AM 09–12; полный день до 15:30 включает выбранный второй блок, а не целый день роботов. English подтверждён; места и иностранный приём отдельно.',
   'Matvey 9: Robo-Tech 8–10; Oscar 6: STEM 6–7, misma sede Stamford Ho Man Tin, cuatro días. AM 09–12; jornada completa hasta 15:30 incluye segundo bloque elegido, no robots todo el día. English acreditado; plazas y admisión extranjera aparte.'),deposit_note=HK_CANCEL,included=T('Выбранные занятия; full включает обеденный присмотр, но lunch, перекусы и вода с собой. Заём техники, личная страховка и поездка семьи уточняются отдельно.',
   'Clases elegidas; full incluye supervisión de almuerzo, pero llevar lunch, meriendas y agua. Préstamo de equipo, seguro personal y viaje familiar a confirmar aparte.'),child_slugs=dict(matvey='campasia-hk-winter-robo',oscar='campasia-hk-winter-stem'))
 offer('goodgood-qingpu-siblings-2027','good-good-qingpu-winter-2027','Good Good English · '+T('два ребёнка / десять дней','dos niños / diez días'),'TWD',dict(matvey=22000,oscar=22000),[['2027-01-21','2027-02-03']],[GOOD,GOOD_POSTER],GRADE,optional=[dict(id='early',amount=-4400,label=T('Early bird до 20 ноября 2026 · только при подтверждённой применимости','Early bird hasta 20 de noviembre de 2026 · solo si aplicabilidad confirmada'))],unknown_required=[dict(id='camp_extras',label=T('Питание, поездки, материалы, прокат и страховка по invoice','Comida, excursiones, material, alquiler y seguro según invoice'),unit='amount',rate=1,min=0)],scope=T('Обычная цена за двоих 44000; ранняя при применимости 39600. Дополнительные 1000 на ребёнка для прежних / текущих учеников семье не начислены. Пакет содержит десять будних дней, не все календарные дни периода.',
  'Precio estándar de ambos 44000; anticipado si aplicable 39600. Otros 1000 por niño para alumnos previos / actuales sin aplicar a familia. Paquete contiene diez días laborables, no todos días naturales del periodo.'))
 offer('ea-immersion-matvey-dec2026','english-adventure-winter','English Adventure · Immersion · '+T('Матвей / декабрь','Matvey / diciembre'),'JPY',dict(matvey=137250),[['2026-12-26','2026-12-30']],['https://www.english-adventure.org/en/winter/','https://www.english-adventure.org/en/availability/'],T('Проверить класс, fluent English, самостоятельность и место в Immersion. Оскар 2020 подходит только при рождении до 1 апреля включительно и Grade 1+, поэтому в эту смету не включён.',
  'Comprobar curso, fluent English, autonomía y plaza en Immersion. Oscar de 2020 solo cumple si nació hasta el 1 de abril inclusive y Grade 1+, por eso no incluido.'),format='boarding',optional=[dict(id='ski',amount=9000,label=T('Прокат лыж, ботинок и палок','Alquiler de esquís, botas y bastones')),dict(id='wear',amount=6000,label=T('Прокат лыжной одежды','Alquiler de ropa de esquí')),dict(id='nagoya',amount=15000,label=T('Nagoya meetup вместо включённого Tokyo','Nagoya meetup en lugar de Tokyo incluido'))],included=T('Tokyo transfer, проживание, еда, основные занятия, лыжные уроки / lifts / helmet при катании, заявленная страховка и налоги.',
  'Tokyo transfer, alojamiento, comida, actividades principales, clases de esquí / lifts / helmet al esquiar, seguro anunciado e impuestos.'))
 index={o['id']:o for o in offers};old={o['id'] for o in d['camp_planning']['offers']}
 d['camp_planning']['offers']=[index.get(o['id'],o) for o in d['camp_planning']['offers']]+[o for o in offers if o['id'] not in old]
 d['camp_planning'].update(version=159,asof=CHECKED)
