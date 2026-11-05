"""Current European winter programmes; preserve archive, age and language gates."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
from camp_east_asia_v159 import base, add, age_fit, candidate
from nearby_regional_v160 import event

ROOT=Path(__file__).resolve().parents[1]
CHECKED='2026-11-05'
SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
TEC='https://tecnoeduka.es/navidad/'
TEC_PRODUCT='https://tecnoeduka.es/producto/reserva-campamento-navidad/'
BEE='https://www.beelingueacademy.com/christmas-camp'
BEE_PDF=BEE+'/CHRISTMAS-CAMP-2026.pdf'
BEE_TERMS='https://www.beelingueacademy.com/cgdv'
TINY='https://www.tiny-tiny-school.com/pages/pendant-les-vacances.html'
TINY_TERMS='https://www.tiny-tiny-school.com/about/cgv/'
ROB='https://oeiras.tecnico.ulisboa.pt/en/2026/11/02/rob9-16-mission-a-bright-christmas/'
ROB_UNI='https://www.ulisboa.pt/evento/rob9-16-missao-natal-iluminado'
SHARK='https://www.sharkcoders.pt/en/camps/nacional'
INV='https://theinventors.io/en/campos-de-ferias/'
INV_FAQ='https://theinventors.io/en/perguntas-frequentes-campos-de-ferias/'
HOG='https://escueladeciencia.com/campamentos/hogwarts'
GOOGLE='https://techsparkacademy.ch/in-person-workshops/hack-google-weekend-2027/'
GATE=T('Подтвердить место, индивидуальный иностранный приём, уровень группы и итоговый счёт. Возрастная возможность не означает зачисление; заявки и оплаты не выполнялись.',
 'Confirmar plaza, admisión extranjera individual, nivel del grupo y factura final. Compatibilidad de edad no significa admisión; sin solicitudes ni pagos.')
LANG=T('Язык преподавания EN / ES / RU именно этой программы не подтверждён. Язык сайта не доказывает язык занятий.',
 'Idioma docente EN / ES / RU de este programa sin confirmar. Idioma web no acredita idioma de las clases.')
UNKNOWN=T('Полная цена, включения, техника, питание и условия выбранного набора ещё требуют подтверждения; неизвестные расходы не считаются нулём.',
 'Precio completo, inclusiones, equipo, comida y condiciones de convocatoria elegida requieren confirmación; gastos desconocidos no equivalen a cero.')
TRIP=T('Перелёты, жильё семьи, трансферы, сопровождение, страховка и неуказанные расходы отдельно.',
 'Vuelos, alojamiento familiar, traslados, acompañamiento, seguro y gastos no indicados aparte.')
EDU=T('Учебная программа / собственный проект; участие и внутренние задания не международная конкурсная победа.',
 'Programa educativo / proyecto propio; participación y retos internos no son victoria competitiva internacional.')
BEETERM=T('CGDV ateliers: ежегодный сбор EUR 30 на семью, применимость к этому camp и уже оплаченный год уточнить. Общие условия требуют уведомления об отмене минимум за 48 часов, при позднем отказе возврата нет; ранний cash refund отдельного camp не обещан. Согласия на фото и условия не принимались.',
 'CGDV ateliers: cuota anual EUR 30 por familia, confirmar aplicación a este camp y año ya abonado. Condiciones generales exigen aviso de cancelación al menos 48 horas antes, sin devolución tardía; sin promesa de cash refund anticipado específico del camp. Sin consentimientos de fotos ni condiciones.')
TINYTERM=T('Общие CGV требуют полной оплаты и допускают отмену оператором при недостатке участников; для holiday stage заявлен отказ от последующей отмены. Текст содержит старые платёжные годы 2021 / 2022: запросить актуальный договор 2026 и применимые права возврата. Публикуется late pickup EUR 10 / 15 минут; согласия не давались.',
 'CGV generales exigen pago completo y permiten cancelación del operador por pocos participantes; holiday stage declara ausencia de cancelación posterior. Texto contiene años de pago antiguos 2021 / 2022: solicitar contrato vigente 2026 y derechos de devolución aplicables. Publica late pickup EUR 10 / 15 minutos; sin consentimientos.')

def refs(p,*items):p['sources']=[dict(title=a,url=b,checked=CHECKED) for a,b in items]
def B(i,slug,title,iso,place,themes,age,lo=None,hi=None):
 country={'FRA':T('Франция','Francia'),'PRT':T('Португалия','Portugal'),'ESP':T('Испания','España'),'CHE':T('Швейцария','Suiza')}[iso]
 p=base('CP'+str(i),slug,title,iso,country,place,themes)
 p.update(age=age,language=LANG,questions=[GATE],shortlist=[])
 p['timing'].update(status='next_unannounced',label=UNKNOWN)
 p['price'].update(label=UNKNOWN,extras=TRIP,deposit=UNKNOWN)
 if lo is not None:p['family_fit']=age_fit(lo,hi,'2026-12-01')
 return p

def update_tecno(p):
 p=deepcopy(p)
 if p['price'].get('year')==2025 and not p.get('archive_offers'):
  p['archive_offers']=[dict(checked=p['checked'],timing=deepcopy(p['timing']),price=deepcopy(p['price']),sources=deepcopy(p['sources']))]
 p.update(checked=CHECKED,age='4–14',language=T('Страница прямо указывает En inglés. Минимальный уровень не требуется, обещана помощь с объяснениями; это подтверждение EN занятий конкретного лагеря.',
 'Página declara expresamente En inglés. Sin nivel mínimo, ofrece ayuda con explicaciones; confirma clases EN del campamento concreto.'),confirmed_instruction_languages=['EN'],language_evidence_role='primary',themes=['robotics','coding','games','engineering'])
 p['programme']=T('Робототехника, программирование игр и механика по возрасту; в старших группах 3D / VR. 8–10 детей в группе, распределение по возрасту и опыту. Школьный уровень и сложность после трёх лет соревнований согласовать; одна программа не обещает каждый инструмент каждому возрасту.',
 'Robótica, programación de juegos y mecánica según edad; 3D / VR en grupos mayores. 8–10 niños por grupo, reparto según edad y experiencia. Acordar curso escolar y dificultad tras tres años de competiciones; un programa no promete cada herramienta para toda edad.')
 p['timing']=dict(status='published_2026',label=T('28–30 декабря 2026, 09:00–13:00; по выбору ранний час 08–09 и поздний 13–14. Старый SEO-заголовок 2025–26 не отменяет новые даты в основном тексте и товарных вариантах.',
 '28–30 de diciembre 2026, 09:00–13:00; opcional hora temprana 08–09 y tardía 13–14. Título SEO antiguo 2025–26 no anula fechas nuevas del texto principal y opciones del producto.'),sessions=[],session_details=[],variant_keyed=True)
 p['price']=dict(year=2026,season='Christmas 2026',currency='EUR',amount=81,unit='child_camp',label=T('EUR 81 за три утра или 30 за отдельный день; ранний / поздний час по 2 за день. На странице товара полный пакет 81 / 87 / 93 по режиму. Двум базово 162; 5% hermanos опубликованы, размер применения к счёту не проверен. 12% только действующим ученикам 26–27, не применены семье.',
 'EUR 81 por tres mañanas o 30 por día suelto; hora temprana / tardía 2 por día. Producto muestra paquete completo 81 / 87 / 93 según horario. Base para ambos 162; 5% hermanos publicados, aplicación a factura sin comprobar. 12% solo alumnos actuales 26–27, sin aplicar a familia.'),included=T('Выбранные занятия; ownership робота, полный комплект техники и питание отдельно подтвердить. Есть перерыв 10:30–11:00.',
 'Clases elegidas; confirmar propiedad del robot, equipo completo y comida por separado. Descanso 10:30–11:00.'),extras=TRIP,deposit=UNKNOWN)
 p['family_fit']=age_fit(4,14,'2026-12-28');p['shortlist']=['both','technical'];p['questions']=[GATE,UNKNOWN]
 p['editorial_reason']=T('Актуальный короткий EN лагерь по робототехнике для обоих по возрасту, с опубликованным прайсом и возрастными группами. Сложность для опытных детей подтвердить.',
 'Campamento EN de robótica corto vigente para ambos por edad, con precio publicado y grupos por edad. Confirmar dificultad para niños experimentados.')
 add(p,'2026-12-28','2026-12-30','christmas-2026','Christmas robotics',p['price']['label'],TEC,days=['2026-12-28','2026-12-29','2026-12-30'],begin='09:00',finish='13:00',zone='Europe/Madrid',admission_kind='open_application')
 refs(p,('Christmas 2026 · ages, English and fees',TEC),('Read-only native date / time / price variants',TEC_PRODUCT))
 return p

def make_profiles():
 out=[]
 for i,key in [(1308,'full'),(1309,'half')]:
  full=key=='full';p=B(i,'beelingue-paris-christmas-'+key,'BeeLingue Academy · Paris Christmas '+key,'FRA','49 rue de Prony · 75017 Paris',['general','languages','science','art','culture'],'3–6 / 7–10',3,10)
  p.update(language=T('100% English прямо на странице и в PDF; две возрастные группы 3–6 и 7–10. Подходит начинающим, максимум 10 детей в группе.',
   '100% English expresamente en web y PDF; dos grupos 3–6 y 7–10. Apto para principiantes, máximo 10 niños por grupo.'),confirmed_instruction_languages=['EN'],language_evidence_role='primary',shortlist=['both','general'])
  p['programme']=T('Winter Wonders и Hello, New Year!: английские игры, истории, поделки и опытные задания. Для 7–10 предусмотрен Mini Lab, для 3–6 Art & Play. Общая языковая / творческая программа, робототехнический интенсив не заявлен.',
   'Winter Wonders y Hello, New Year!: juegos ingleses, historias, manualidades y experimentos. Mini Lab para 7–10, Art & Play para 3–6. Programa general lingüístico / creativo, sin intensivo robótico anunciado.')
  p['timing'].update(status='published_2026',label=T('21–24 и 28–31 декабря 2026, пакеты по четыре дня Пн–Чт. 25 декабря / 1 января только при достаточном наборе, в подтверждённый календарь не включены. Подробная таблица web / PDF задаёт утро 09–12; общий рисунок PDF также пишет 10–12, часы подтвердить.',
   '21–24 y 28–31 de diciembre 2026, paquetes de cuatro días lunes–jueves. 25 de diciembre / 1 de enero solo con suficientes inscritos, fuera del calendario confirmado. Tabla detallada web / PDF fija mañana 09–12; dibujo general PDF también indica 10–12, confirmar horario.'))
  p['price'].update(currency='EUR',year=2026,amount=396 if full else 180,unit='child_four_days',label=T('Полный день EUR 396 / 4 дня, 115 / день; полдня 180 / 4 утра или послеобеденных блока, 50 / раз. Второму ребёнку −10% только на четырёхдневный пакет. Двум 752.40 полный или 342 полдня до возможного annual fee и опций; это расчёт, не счёт.',
   'Jornada completa EUR 396 / 4 días, 115 / día; media jornada 180 / 4 mañanas o tardes, 50 / sesión. Segundo niño −10% solo en paquete de cuatro días. Ambos 752.40 completa o 342 media antes de posible annual fee y opciones; cálculo, no factura.'),included=T('Выбранный пакет занятий. Полный день 09–17 с обеденным промежутком; lunch supervision второй раз автоматически не прибавлена. Еду приносить самим.',
   'Paquete elegido de clases. Jornada completa 09–17 con intervalo de almuerzo; lunch supervision sin añadir automáticamente otra vez. Llevar comida propia.'),extras=T('Lunchbox и перекусы свои; микроволновка доступна. Lunch supervision 12–14: 15 / день или 60 / 4 дня для неполного пакета. Ludothèque 17–18: 15 / день или 60 / 4 дня. Приём 08:30 возможен, цена не установлена. Annual EUR 30 / семья по общим CGDV требует проверки применимости.',
   'Lunchbox y meriendas propios; microondas disponible. Lunch supervision 12–14: 15 / día o 60 / 4 días para paquete parcial. Ludothèque 17–18: 15 / día o 60 / 4 días. Acogida 08:30 posible, precio sin establecer. Annual EUR 30 / familia según CGDV generales requiere comprobar aplicación.'),deposit=BEETERM)
  for week,start in enumerate([21,28],1):
   days=['2026-12-'+str(day) for day in range(start,start+4)]
   for block,begin,finish in ([('full','09:00','17:00')] if full else [('morning','09:00','12:00'),('afternoon','14:00','17:00')]):
    add(p,days[0],days[-1],'week-'+str(week)+'-'+block,('Winter Wonders' if week==1 else 'Hello, New Year!')+' · '+block,'EUR '+str(p['price']['amount'])+' / child / 4 days',BEE,days,begin,finish,'Europe/Paris',admission_kind='open_application')
  refs(p,('Christmas 2026 · specific four-day packages',BEE),('Six-page visual timetable and prices',BEE_PDF),('General ateliers CGDV, applicability to camp unconfirmed',BEE_TERMS));out.append(p)
 tiny=[(1310,'brest-younger','Brest / Gouesnou · Ecole St Joseph',4,6,['2026-12-21','2026-12-22','2026-12-23'],'09:30','12:30',150),
  (1311,'brest-older','Brest / Gouesnou · Ecole St Joseph',7,10,['2026-12-21','2026-12-22','2026-12-23'],'14:00','17:00',150),
  (1312,'quimper','Quimper · Ludo Trotter',7,10,['2026-12-21','2026-12-22','2026-12-23'],'14:00','17:00',150),
  (1313,'nort-younger','Nort-sur-Erdre',4,6,['2026-12-22'],'09:00','12:00',50),
  (1314,'nort-older','Nort-sur-Erdre',7,10,['2026-12-23'],'09:00','12:00',50),
  (1315,'auray','Auray · Chez Telles mères telles filles',6,10,['2026-12-23'],'14:00','16:00',30)]
 for i,key,place,lo,hi,days,begin,finish,fee in tiny:
  p=B(i,'tiny-tiny-christmas-'+key,'Tiny Tiny School · Christmas '+key,'FRA',place,['general','languages','art','culture'],str(lo)+'–'+str(hi),lo,hi)
  p.update(confirmed_instruction_languages=['EN'],language_evidence_role='primary',language=T('Полная английская иммерсия прямо заявлена. Общая методика — маленькие возрастные группы до 8; локальный числовой возраст и часы имеют приоритет над общим заголовком 3–15.',
   'Inmersión inglesa completa declarada expresamente. Método general: grupos pequeños por edad de hasta 8; edad numérica y horario local prevalecen sobre título general 3–15.'))
  p['catalog_participation']='holiday_workshop';p['programme']=T('Короткий языковой / творческий Christmas stage: игры, английские традиции, открытки и командные задания. Это '+str(len(days))+' учебных дня по '+('2' if i==1315 else '3')+' часа, без полного дня и пансиона. В Brest дети разных возрастов идут утром и после обеда; в Nort ещё и в разные даты.',
   'Christmas stage lingüístico / creativo corto: juegos, tradiciones inglesas, tarjetas y retos grupales. Son '+str(len(days))+' días de '+('2' if i==1315 else '3')+' horas, sin jornada completa ni residencia. En Brest edades distintas asisten por mañana y tarde; en Nort también fechas distintas.')
  p['timing'].update(status='published_2026',label=days[0]+'–'+days[-1]+' · '+begin+'–'+finish+' · '+T('Регистрация минимум за две недели до начала. Другим городам без опубликованной смены дата не назначена.',
   'Inscripción al menos dos semanas antes del inicio. Sin asignar fecha a otras ciudades sin sesión publicada.'))
  p['price'].update(year=2026,currency='EUR',amount=fee,unit='child_stage',label='EUR '+str(fee)+' / '+str(len(days))+T(' учебных дня / ребёнок; скидки не установлены.',' días lectivos / niño; descuentos sin establecer.'),included=T('Опубликованная короткая языковая программа. Состав материалов и все дополнительные сборы подтвердить.',
   'Programa lingüístico corto publicado. Confirmar materiales y todos los cargos adicionales.'),deposit=TINYTERM)
  add(p,days[0],days[-1],key+'-christmas-2026','Christmas English · '+str(lo)+'–'+str(hi),p['price']['label'],TINY,days,begin,finish,'Europe/Paris',admission_kind='open_application')
  refs(p,('Current Christmas 2026 city-specific hours and ages',TINY),('General CGV with old payment-year references',TINY_TERMS));out.append(p)
 p=B(1316,'rob9-16-oeiras-bright-christmas','ROB9-16 · Mission: A Bright Christmas','PRT','Instituto Superior Técnico · Oeiras Campus',['robotics','coding','engineering','science'],'9–16',9,16)
 p['programme']=T('Три дня: 3D-печатная конструкция, проектирование PCB, пайка компонентов, сборка, программирование и тестирование работающего проекта. Опубликовано 24 места, это предельный набор, не подтверждение текущего остатка.',
  'Tres días: estructura impresa 3D, diseño PCB, soldadura, montaje, programación y prueba de proyecto funcional. Publica 24 plazas, capacidad máxima, no confirmación del saldo actual.')
 p['timing'].update(status='published_2026',label='21–23 December 2026 · 10:00–17:00')
 p['price'].update(year=2026,currency='EUR',amount=90,unit='child_camp',label=T('EUR 90 за все три дня одному ребёнку. Матвей подходит по возрасту, Оскар младше 9; цена не семейный пакет.',
  'EUR 90 por los tres días para un niño. Matvey compatible por edad, Oscar menor de 9; precio no es paquete familiar.'),included=T('Три учебных дня по анонсу; право забрать проект, питание, техника и материалы в цене отдельно подтвердить.',
  'Tres días lectivos según anuncio; confirmar derecho a llevarse proyecto, comida, equipo y materiales incluidos.'))
 add(p,'2026-12-21','2026-12-23','bright-christmas-2026','Mission: A Bright Christmas',p['price']['label'],ROB,['2026-12-21','2026-12-22','2026-12-23'],'10:00','17:00','Europe/Lisbon',admission_kind='open_application')
 refs(p,('Oeiras campus official dates, age and full three-day fee',ROB),('Universidade de Lisboa event notice',ROB_UNI));out.append(p)
 p=B(1317,'sharkcoders-portugal-christmas','SHARKCODERS · Portugal Christmas network','PRT',T('Португалия · конкретную школу выбрать','Portugal · elegir escuela concreta'),['robotics','coding','games','ai'],'network 4–17')
 p['programme']=T('Сеть предлагает workshop 6h, express 9h и course 15h: робототехника, игры, coding и AI по площадке. Возраст сети 4–17 не доказывает отдельную Christmas группу обоим. Время, тариф, адрес и язык нужного локального курса ещё не опубликованы в прочитанной общей странице.',
  'Red ofrece workshop 6h, express 9h y course 15h: robótica, juegos, coding y AI según sede. Edad de red 4–17 no acredita grupo Christmas concreto para ambos. Horario, tarifa, dirección e idioma del curso local requerido sin publicar en página general leída.')
 p['price']['included']=T('Школы обещают компьютеры и оборудование; личный ноутбук необязателен. Обед обычно не включён, зависит от филиала.',
  'Escuelas ofrecen ordenadores y equipo; portátil propio opcional. Almuerzo generalmente excluido, depende de sede.')
 p['price']['deposit']=T('Опубликован полный возврат при отмене минимум за 48 часов до курса; позднее возврата нет. Точные условия выбранного филиала подтвердить; уведомления не отправлялись.',
  'Publica devolución completa cancelando al menos 48 horas antes del curso; sin devolución posterior. Confirmar condiciones de sede elegida; sin enviar avisos.')
 p['timing']['label']=T('Christmas Camp без явного года, точных дат и тарифов; наблюдение за новым локальным набором.','Christmas Camp sin año explícito, fechas exactas ni tarifas; seguimiento de convocatoria local nueva.')
 refs(p,('Network Christmas offer, devices and refund policy',SHARK));out.append(p)
 p=B(1318,'the-inventors-portugal-camps','The Inventors · Portugal holiday camps','PRT',T('Португалия · площадка будущего набора не установлена','Portugal · sede de próxima convocatoria sin establecer'),['engineering','coding','science','art'],'6–12',6,12)
 p['programme']=T('Электроника, программирование, изобретательство и искусство. Активности 10–17, приём 09–18. Общие возраст и режим не заменяют подтверждение конкретной будущей площадки, языка и места.',
  'Electrónica, programación, inventos y arte. Actividades 10–17, acogida 09–18. Edad y horario generales no sustituyen confirmación de sede futura concreta, idioma y plaza.')
 p['timing'].update(status='archive_next_unannounced',label=T('На основном сайте лето 29 июня – 4 сентября 2026 уже прошло; FAQ содержит рождественские числа без года. Они не перенесены на 2026/27. Будущий набор и адрес ещё не подтверждены.',
  'Web principal muestra verano 29 de junio – 4 de septiembre 2026 ya pasado; FAQ contiene fechas navideñas sin año. Sin trasladarlas a 2026/27. Convocatoria futura y dirección sin confirmar.'))
 p['family_fit']={c:candidate('conditional',GATE) for c in ['matvey','oscar']}
 p['price']['label']=T('Полный tuition неизвестен. FAQ называет EUR 7 за день питания, уже включённые в итоговую цену; это не цена лагеря и не отдельная обязательная доплата второй раз.',
  'Tuition completo desconocido. FAQ indica EUR 7 por día de comida ya incluidos en precio final; no es precio del campamento ni cargo obligatorio que añadir otra vez.')
 p['price']['included']=T('FAQ обещает обед и два перекуса в день внутри итогового пакета. Полный прайс и материалы будущей смены проверить.',
  'FAQ promete almuerzo y dos meriendas diarios dentro del paquete final. Comprobar precio completo y materiales de próxima sesión.')
 refs(p,('Current summer page · old 2026 season',INV),('Ages, hours, food fee and undated Christmas FAQ',INV_FAQ));out.append(p)
 p=B(1319,'escuela-ciencia-hogwarts-christmas','Escuela de Ciencia · Hogwarts School of Science','ESP','C/ Islas Canarias 90 · València',['robotics','coding','science','engineering'],'1º Primaria–2º ESO')
 p['catalog_participation']='holiday_workshop';p['programme']=T('Шесть дней химии, робототехники / дронов, биологии и coding / AR. Группы по возрасту максимум 14. Допуск опубликован по классу 1º Primaria–2º ESO; реальные классы детей неизвестны, возраст их не заменяет.',
  'Seis días de química, robótica / drones, biología y coding / AR. Grupos por edad máximo 14. Acceso publicado según curso 1º Primaria–2º ESO; cursos reales de niños desconocidos, edad no los sustituye.')
 p['family_fit']={c:candidate('conditional',p['programme']) for c in ['matvey','oscar']}
 p['timing'].update(status='published_2026_27',label=T('28–31 декабря 2026 и 4–5 января 2027, ровно шесть учебных дней 09–14. 1–3 января занятий нет; дни по отдельности не продаются.',
  '28–31 de diciembre 2026 y 4–5 de enero 2027, exactamente seis días lectivos 09–14. Sin clases 1–3 de enero; sin venta de días sueltos.'))
 p['price'].update(year=2026,season='Christmas 2026/27',currency='EUR',amount=195,unit='child_camp',label=T('EUR 195 за все шесть дней, без matrícula; двум 390 при подтверждённом школьном уровне. Ранний / поздний час 5 за каждый extra hour; порядок расчёта на ребёнка подтвердить.',
  'EUR 195 por los seis días, sin matrícula; ambos 390 sujeto a curso escolar confirmado. Hora temprana / tardía 5 por extra hour; confirmar cálculo por niño.'),included=T('Материалы и техника, преподаватели, almuerzo — сэндвичи и напитки, RC / medical insurance по организатору. Это не обещание полноценного обеда после 14:00; детали покрытия и аллергий подтвердить.',
  'Materiales y equipo, docentes, almuerzo de sándwiches y bebidas, RC / medical insurance según organizador. Sin promesa de comida completa después de 14:00; confirmar cobertura y alergias.'),deposit=UNKNOWN)
 days=['2026-12-28','2026-12-29','2026-12-30','2026-12-31','2027-01-04','2027-01-05']
 add(p,days[0],days[-1],'hogwarts-christmas-2026','Hogwarts · six days',p['price']['label'],HOG,days,'09:00','14:00','Europe/Madrid',admission_kind='open_application')
 refs(p,('Exact six-day schedule, grade gate and inclusions',HOG));out.append(p)
 p=B(1320,'techspark-hack-google-2027-watch','TechSpark Academy · Hack @ Google 2027 watch','CHE','Google Switzerland · Europaallee 8 · Building B · Zürich',['coding','engineering'],'12–17',12,17)
 p['catalog_participation']='holiday_workshop';p['programme']=T('Cybersecurity workshops и hackathon с инструкторами и Googlers. Точные правила judging / награды текущего набора не опубликованы; это учебный технологический маршрут на будущий возраст, не подтверждённый мировой турнир.',
  'Cybersecurity workshops y hackathon con instructores y Googlers. Reglas exactas de judging / premios de convocatoria actual sin publicar; ruta educativa tecnológica para edad futura, no torneo mundial confirmado.')
 p['timing'].update(status='next_unannounced',label=T('Заголовок 2027 прямо пишет New Dates Coming Soon. Ниже осталась таблица Saturday 14 March / Sunday 15 March и SOLD OUT. В 2027 это другие дни недели: таблица не признана новой сменой 2027, даты в календарь не выгружены.',
  'Título 2027 dice expresamente New Dates Coming Soon. Debajo queda tabla Saturday 14 March / Sunday 15 March y SOLD OUT. En 2027 corresponden otros días de semana: tabla no reconocida como sesión nueva 2027, sin exportar fechas al calendario.'))
 p['price'].update(year=None,label=T('Старая недатированная таблица: CHF 50 / workshop, 95 / weekend и отдельные Boost packages. Цена набора 2027 не объявлена; 95 не использованы как действующий бюджет.',
  'Tabla antigua sin año: CHF 50 / workshop, 95 / weekend y Boost packages separados. Precio de convocatoria 2027 sin anunciar; 95 sin usar como presupuesto vigente.'))
 p['price']['extras']=T('Родители организуют проезд и жильё сами. Возраст обоих сейчас меньше 12, запись не подходит; следить за будущим треком.',
  'Padres organizan transporte y alojamiento. Ambos actualmente menores de 12, inscripción incompatible; seguir ruta futura.')
 refs(p,('2027 watch page with unresolved old March table',GOOGLE));out.append(p)
 assert len(out)==13
 return out

def update_report(report):
 new=make_profiles();by={p['id']:p for p in new};old={p['id'] for p in report['profiles']}
 report['profiles']=[update_tecno(p) if p['id']=='CP261' else by.get(p['id'],p) for p in report['profiles']]+[p for p in new if p['id'] not in old]
 report['counts'].update(dossiers=len(report['profiles']),countries=len({p['iso'] for p in report['profiles']}),swiss=sum(p['iso']=='CHE' for p in report['profiles']),by_status=dict(Counter(p['timing']['status'] for p in report['profiles'])),source_urls=len({s['url'] for p in report['profiles'] for s in p['sources']}))
 report['countries']=[dict(country=c,count=n) for c,n in sorted(Counter(p['country'] for p in report['profiles']).items())]
 report.update(version=167,asof=CHECKED)

def enrich_v167(d):
 profiles=make_profiles();report=d['camp_programmes']
 fit={'conditional':T('Условно — допуск / язык / набор подтвердить','Condicional — confirmar acceso / idioma / convocatoria'),'later':T('Нет сейчас — минимум 12, будущий трек','No ahora — mínimo 12, ruta futura')}
 for number,p in enumerate([p for p in profiles if not p['timing']['sessions']],473):
  c=next(c for c in d['countries'] if c['iso']==p['iso'])
  row=event('L'+str(number),p['provider'],c['country'],p['sources'][0]['url'],block='Лагеря',iso=[p['iso']],region=c['region'],city=p['place'],age=p['age'],format=p['accommodation'],mat=fit[p['family_fit']['matvey']['status']],osc=fit[p['family_fit']['oscar']['status']],gear=p['programme'],language=p['language'],cost=p['price']['label'],entry=GATE,period=p['timing']['label'],note=p['programme']+' '+GATE,participation='holiday_workshop',camp_programme_id=p['id'],camp_dossier_slug=p['slug'],themes=p['themes'],reward=EDU,scope='local',level=T('D — местная учебная программа','D — programa educativo local'),references=[dict(label=s['title'],url=s['url']) for s in p['sources']])
  existing=next((e for e in d['events'] if e['id']==row['id']),None)
  if existing:existing.update(row)
  else:d['events'].append(row)
  q=next(q for q in report['profiles'] if q['id']==p['id']);q['related_event_ids']=list(dict.fromkeys(q.get('related_event_ids',[])+[row['id']]))
  if not any(x['programme_id']==p['id'] and x['event_id']==row['id'] for x in report['event_links']):report['event_links'].append(dict(programme_id=p['id'],event_id=row['id'],relation='existing_programme'))
 offers=[]
 def O(key,slug,label,amount,children,dates,sources,gate,included,deposit=UNKNOWN,discount=0,optional=None):
  offers.append(dict(id=key,slug=slug,label=label,currency='EUR',price_year=2026,format='day',children=children,base_by_child={c:amount for c in children},discount_second=discount,required=[],unknown_required=[dict(id='unpriced',unit='money',rate=1,min=0,label=UNKNOWN)],optional=optional or [],unknown_trip=['travel','lodging','misc'],sessions=dates,sources=sources,checked=CHECKED,gate=gate,included=included,deposit_note=deposit,scope=TRIP))
 tec=next(p for p in report['profiles'] if p['id']=='CP261')
 O('tecnoeduka-christmas-2026-siblings',tec['slug'],'Tecnoeduka · both · 3 mornings',81,['matvey','oscar'],[['2026-12-28','2026-12-30']],[TEC,TEC_PRODUCT],tec['price']['label'],tec['price']['included'],optional=[dict(id='early',label=T('Ранний час · 3 дня × 2 ребёнка','Hora temprana · 3 días × 2 niños'),amount=12),dict(id='late',label=T('Поздний час · 3 дня × 2 ребёнка','Hora tardía · 3 días × 2 niños'),amount=12)])
 for mode,amount in [('full',396),('half',180)]:
  p=next(p for p in profiles if p['slug']=='beelingue-paris-christmas-'+mode)
  for week,start in enumerate([21,28],1):
   O('beelingue-christmas-2026-'+mode+'-week-'+str(week),p['slug'],'BeeLingue · '+mode+' · 4 days · week '+str(week),amount,['matvey','oscar'],[['2026-12-'+str(start),'2026-12-'+str(start+3)]],[BEE,BEE_PDF,BEE_TERMS],p['price']['label']+' '+GATE,p['price']['included'],BEETERM,.1,optional=[dict(id='aftercare',label=T('Ludothèque 17–18 · 4 дня × 2 ребёнка','Ludothèque 17–18 · 4 días × 2 niños'),amount=120)] if mode=='full' else [])
 for pid,key,label,amount,children in [('CP1315','tiny-auray-christmas-2026','Tiny Tiny · Auray · both · 2 hours',30,['matvey','oscar']),('CP1310','tiny-brest-christmas-2026','Tiny Tiny · Brest · different sibling hours',150,['matvey','oscar']),('CP1316','rob9-bright-christmas-2026','ROB9-16 · Matvey only · 3 days',90,['matvey']),('CP1319','hogwarts-christmas-2026','Hogwarts · both conditional on grade · 6 days',195,['matvey','oscar'])]:
  p=next(p for p in profiles if p['id']==pid)
  gate=p['programme']+' '+GATE
  if pid=='CP1310':gate=T('Матвей: CP1311 14–17; Оскар: CP1310 09:30–12:30, одни даты. Это два разных возрастных блока, перерыв и полный день не включены.',
   'Matvey: CP1311 14–17; Oscar: CP1310 09:30–12:30, mismas fechas. Dos bloques de edad distintos, sin incluir pausa ni jornada completa.')+' '+GATE
  O(key,p['slug'],label,amount,children,p['timing']['sessions'],[s['url'] for s in p['sources']],gate,p['price']['included'],p['price']['deposit'])
 ids={o['id'] for o in offers};d['camp_planning']['offers']=[o for o in d['camp_planning']['offers'] if o['id'] not in ids]+offers
 d['camp_planning'].update(version=167,checked=CHECKED)
 # integrate() owns dated rows and all canonical source references.
 known={s['url'] for s in d['sources']}
 for p in profiles+[tec]:
  for s in p['sources']:
   if s['url'] not in known:d['sources'].append(dict(**s,evidence=EDU));known.add(s['url'])
 d['europe_v167']=dict(version=167,checked=CHECKED,new_camp_dossiers=13,updated_camp_dossiers=['CP261'],new_budget_offers=len(offers),fully_audited_countries=0,worldwide_complete=False)
