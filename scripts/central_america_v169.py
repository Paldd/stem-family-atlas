"""Sourced Central American school routes and learning candidates, without invented dates."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
from camp_east_asia_v159 import base, candidate
from nearby_regional_v160 import event, programme

ROOT=Path(__file__).resolve().parents[1]
CHECKED='2026-11-05'; SPANISH={}
def T(a,b): SPANISH[a]=b; return a
TBOX='https://www.tboxplanet.com/web/codigo26/'
WRO='https://www.wroelsalvador.org/temporada-2026/'
STARTER=WRO+'categor%C3%ADas/robo-starter'
BOOT='https://fusalmo.org/bootcamp-aventura/'
PLAN='https://plan.fusalmo.org/calendario'
FUS='https://fusalmo.org/steam-maker-challenge-fusalmo-2/'
COOPE='https://www.coopecoceic.ed.cr/tecnologia'
HN='https://robotedhn.tech/'
NIC='https://createch-mind.com/'
LANG=T('Язык преподавания / судейства этой группы прямо не установлен. Испанская страница и билингвальные школы-клиенты не доказывают ES / EN обучение; согласовать конкретную группу.',
 'Idioma de enseñanza / evaluación de este grupo sin establecer expresamente. Página española y colegios clientes bilingües no acreditan enseñanza ES / EN; acordar grupo concreto.')
GATE=T('Подтвердить новый набор, место, класс / возраст, приём внешних и иностранных детей, уровень после трёх лет соревнований, язык, оборудование и полный счёт. Заявки, согласия, сообщения и оплаты не выполнялись.',
 'Confirmar nueva convocatoria, plaza, curso / edad, admisión externa y extranjera, nivel tras tres años de competiciones, idioma, equipo y factura completa. Sin solicitudes, consentimientos, mensajes ni pagos.')
UNKNOWN=T('Текущая полная цена не опубликована в прочитанных источниках. Неизвестные расходы не считаются нулём.',
 'Precio total actual sin publicar en fuentes leídas. Gastos desconocidos no equivalen a cero.')
EDU=T('Учебные проекты и сертификат не доказывают конкурсную международную победу.',
 'Proyectos educativos y certificado no acreditan victoria competitiva internacional.')
NEXT=T('Сезон 2026 завершён; даты, запись и правила 2027 ещё не подтверждены. Это наблюдение за следующим набором, не открытая регистрация.',
 'Temporada 2026 terminada; fechas, inscripción y reglas 2027 aún sin confirmar. Seguimiento de siguiente convocatoria, no inscripción abierta.')
GRADE=T('Условно — нужен фактический школьный класс и представительство подходящей школы. Даты рождения 2017 / 2020 не устанавливают класс.',
 'Condicional — exige curso escolar real y representación de colegio admisible. Años de nacimiento 2017 / 2020 no determinan curso.')

def sources(p,*items):
 p['sources']=[dict(title=a,url=b,checked=CHECKED) for a,b in items]

def make_profiles():
 out=[]
 for i,lo,hi in [(1331,4,7),(1332,8,11)]:
  p=base('CP'+str(i),'creston-coronado-'+str(lo)+'-'+str(hi),'Creston CFP · COOPECOCEIC · '+str(lo)+'–'+str(hi),'CRI',T('Коста-Рика','Costa Rica'),'Coronado · San Rafael',['robotics','coding','engineering'])
  p.update(age=str(lo)+'–'+str(hi),language=LANG,programme=T('Регулярные очные STEAM-занятия: базовая робототехника, блоки, модели, сенсоры / моторы, Scratch и Tinkercad. Две разные возрастные группы; конкретные марки наборов в странице заменены пустыми полями. Нельзя обещать LEGO / VEX или подготовку к конкретной лиге.',
   'Clases STEAM presenciales regulares: robótica inicial, bloques, modelos, sensores / motores, Scratch y Tinkercad. Dos grupos de edad distintos; marcas concretas de kits sustituidas por campos vacíos. Sin prometer LEGO / VEX ni preparación para liga concreta.'))
  p['timing'].update(status='next_unannounced',label=T('Очные курсы с гибким расписанием; дат лагеря, ближайшего набора, часов и продолжительности нет.',
   'Cursos presenciales con horario flexible; sin fechas de campamento, próxima convocatoria, horas ni duración.'))
  for child,age in [('matvey',9),('oscar',6)]:
   p['family_fit'][child]=candidate('conditional' if lo<=age<=hi else 'not_eligible',T('Сейчас '+str(age)+' лет: '+('возраст соответствует группе; набор, уровень и язык неизвестны.' if lo<=age<=hi else 'вне опубликованной возрастной группы.'),
    'Ahora '+str(age)+' años: '+('edad compatible con grupo; convocatoria, nivel e idioma desconocidos.' if lo<=age<=hi else 'fuera del grupo de edad publicado.')))
  p['price'].update(currency='CRC',amount=None,label=UNKNOWN,deposit=UNKNOWN)
  p.update(questions=[GATE],shortlist=[],programme_type='regular_course',checked=CHECKED)
  sources(p,('Technology course: two child age groups; blank kit names',COOPE));out.append(p)
 for i,key,lo,hi in [(1333,'Comparte',4,6),(1334,'Sueña',7,9),(1335,'Transforma',10,13),(1336,'Crea',14,17)]:
  p=base('CP'+str(i),'fusalmo-bootcamp-'+key.lower(),'FUSALMO · Bootcamp Aventura · '+key,'SLV',T('Сальвадор','El Salvador'),'Soyapango / Santa Ana / San Miguel',['robotics','coding','science','general'])
  p.update(age=str(lo)+'–'+str(hi),language=LANG,programme=T('На публичной странице четыре учебные группы: Comparte 4–6 — STEAM через игру; Sueña 7–9 — первые роботы и код; Transforma 10–13 — механика, датчики и оптимизация; Crea 14–17 — более сложные проекты. Это возраста Bootcamp, не доказанный возраст турнирных лиг STEAM Maker Challenge. Старые модальные окна повторяют Comparte для всех, полные нижние описания различаются.',
   'Página pública presenta cuatro grupos educativos: Comparte 4–6 — STEAM mediante juego; Sueña 7–9 — primeros robots y código; Transforma 10–13 — mecánica, sensores y optimización; Crea 14–17 — proyectos más complejos. Son edades del Bootcamp, no edades acreditadas de ligas competitivas STEAM Maker Challenge. Ventanas modales antiguas repiten Comparte para todos; descripciones inferiores completas sí difieren.'))
  p['timing'].update(status='partial_2026',label=T('План Maestro 2026: начало 16 ноября, общий интервал 17 ноября – 19 декабря; есть перекрывающиеся строки 17–20 и 23–27 ноября. Это план организации, не подтверждённая публичная смена. Страница набора ещё обещает Academy 2026 и 4,5 недели: новый договор / расписание неизвестны. Старые часы Пн–Чт 08–12, пятница выезд не перенесены в новый календарь.',
   'Plan Maestro 2026: inicio 16 de noviembre, intervalo general 17 de noviembre – 19 de diciembre; filas superpuestas 17–20 y 23–27 de noviembre. Plan de organización, no turno público confirmado. Página de inscripción aún promete Academy 2026 y 4,5 semanas: nuevo contrato / horario desconocidos. Horas antiguas lunes–jueves 08–12, viernes excursión no trasladadas al nuevo calendario.'),planned_windows=[dict(start='2026-11-16',end='2026-12-19',status='organizational_plan_only')])
  p['price'].update(currency='',amount=None,label=T('Архивная страница обещает $100, 20% скидку, материалы, выезды и стипендию Academy 2026. Код валюты, срок акции и цена Bootcamp конца 2026 не установлены; $100 не применены к новой смене и не добавлены как действующая смета.',
   'Página antigua promete $100, descuento 20%, materiales, excursiones y beca Academy 2026. Código de moneda, vigencia de oferta y precio Bootcamp de finales 2026 sin establecer; $100 no aplicados al nuevo turno ni añadidos como presupuesto vigente.'),included=UNKNOWN,extras=UNKNOWN,deposit=UNKNOWN)
  for child,age in [('matvey',9),('oscar',6)]:
   status='conditional' if lo<=age<=hi else 'later' if age<lo else 'not_eligible'
   p['family_fit'][child]=candidate(status,T('Возраст ребёнка сейчас '+str(age)+'; группа '+str(lo)+'–'+str(hi)+'. Это старое описание: правила нового набора, день отсечения и иностранный доступ подтвердить.',
    'Edad actual del niño '+str(age)+'; grupo '+str(lo)+'–'+str(hi)+'. Descripción antigua: confirmar reglas de nueva convocatoria, fecha de corte y acceso extranjero.'))
  p.update(availability=dict(status='unknown',label=GATE),questions=[GATE],shortlist=[],programme_type='holiday_camp',checked=CHECKED)
  sources(p,('Public Bootcamp page still targets Academy 2026',BOOT),('Organizational Plan Maestro 2026; overlapping planning windows',PLAN),('Challenge selection is separate from Bootcamp admission',FUS));out.append(p)
 p=base('CP1337','robotedh-mbot-camp','ROBOTEDH · mBot / mBlock Summer Camp','HND',T('Гондурас','Honduras'),'Jardines del Valle · 27 calle / 9 avenida #33 · San Pedro Sula',['robotics','coding','ai'])
 p.update(age=T('Возраст набора не объявлен; mBot 8+ на общей странице описывает устройство, не персональный допуск.',
  'Edad de convocatoria sin anunciar; mBot 8+ en página general describe dispositivo, no admisión personal.'),language=LANG,programme=T('Страница курса прямо называет Summer Camp с mBot / mBlock 5: моторы, RGB, кнопка, расстояние, линия, траектории, начальная AI / vision. Даты, длительность, очный / дистанционный формат конкретной смены и минимум возраста не опубликованы. Botley 5+ / Codey Rocky 6+ в каталоге оборудования не доказывают младшую лагерную группу.',
  'Página del curso menciona expresamente Summer Camp con mBot / mBlock 5: motores, RGB, botón, distancia, línea, trayectorias, AI / vision inicial. Sin fechas, duración, modalidad presencial / remota ni edad mínima de turno concreto. Botley 5+ / Codey Rocky 6+ del catálogo de equipo no acreditan grupo menor de campamento.'),formats=['unknown'],accommodation=T('Формат конкретного Summer Camp и проживание не установлены.','Modalidad del Summer Camp concreto y alojamiento sin establecer.'),questions=[GATE],shortlist=[],programme_type='undated_camp')
 p['timing'].update(status='next_unannounced',label=NEXT);p['price'].update(currency='HNL',amount=None,label=UNKNOWN,deposit=UNKNOWN)
 sources(p,('Actual Summer Camp curriculum',HN+'curso-de-robotica/'),('Hardware ages are not camp admission ages',HN));out.append(p)
 p=base('CP1338','robotedh-arduino-online','ROBOTEDH · Arduino UNO / Tinkercad','HND',T('Гондурас','Honduras'),'Online · operator San Pedro Sula',['robotics','coding','engineering'])
 p.update(age=T('Возраст детей в этом курсе не указан.','Edad infantil del curso sin indicar.'),formats=['online'],language=LANG,accommodation=T('Предусмотрена онлайн-модальность; пансион не заявлен.','Modalidad online prevista; sin residencia anunciada.'),programme=T('Введение в электронику, protoboard, C++, цифровые / аналоговые pins, serial, датчики, LCD, stepper и Tinkercad. Для онлайн перечислены компьютер Windows 8 64-bit или новее, mouse, internet, microphone, Gmail и рекомендованная webcam; это опубликованный старый технический список, совместимость текущего ПО уточнить. Arduino kit указан как включённый, доставка в другую страну / собственность / итоговая цена не подтверждены.',
  'Introducción a electrónica, protoboard, C++, pins digitales / analógicos, serial, sensores, LCD, stepper y Tinkercad. Online enumera ordenador Windows 8 64-bit o posterior, mouse, internet, microphone, Gmail y webcam recomendada; lista técnica antigua publicada, confirmar compatibilidad de software actual. Arduino kit indicado como incluido; envío internacional / propiedad / precio final sin confirmar.'),questions=[GATE],shortlist=[],programme_type='online_course')
 p['timing'].update(status='next_unannounced',label=T('Курс без дат ближайшей группы, длительности и расписания. Не датированный лагерь.','Curso sin fechas de próximo grupo, duración ni horario. No campamento fechado.'));p['price'].update(currency='HNL',amount=None,label=UNKNOWN,included=T('Arduino basic kit указан как включённый в курс; условия доставки и выдачи согласовать.','Arduino basic kit indicado como incluido en curso; acordar envío y entrega.'),deposit=UNKNOWN)
 sources(p,('Online requirements, curriculum and included kit',HN+'curso-de-arduino/'));out.append(p)
 p=base('CP1339','createch-mind-nicaragua','Createch Mind · STEM / robotics / VR','NIC',T('Никарагуа','Nicaragua'),'Km 4½ Carretera a Masaya · Edificio CAR · Managua',['robotics','coding','engineering','games'])
 p.update(age=T('Дети и подростки; числовые границы и класс не опубликованы.','Niños y jóvenes; límites numéricos y curso sin publicar.'),formats=['unknown'],language=LANG,accommodation=T('Центр внеурочного обучения; формат группы и проживание не установлены.','Centro extracurricular; modalidad de grupo y alojamiento sin establecer.'),programme=T('Оператор предлагает robotics, programming, virtual reality и applied technologies; упоминает виртуальные / физические прототипы, 3D printers и VR. Страница Cursos не раскрывает читаемого расписания / возраста / цены. Наличие Campus Virtual не доказывает онлайн-приём иностранного ребёнка. Заявление «единственный центр» не использовано как независимый рейтинг.',
  'Operador ofrece robotics, programming, virtual reality y applied technologies; menciona prototipos virtuales / físicos, 3D printers y VR. Página Cursos sin horario / edad / precio legibles. Campus Virtual no acredita admisión online de niño extranjero. Afirmación «único centro» no usada como ranking independiente.'),questions=[GATE],shortlist=[],programme_type='extracurricular_centre')
 p['timing'].update(status='next_unannounced',label=T('Текущий каталог центра без опубликованных дат лагеря или ближайшего курса.','Catálogo actual del centro sin fechas publicadas de campamento ni curso próximo.'));p['price'].update(currency='NIO',amount=None,label=UNKNOWN,deposit=UNKNOWN)
 sources(p,('Primary learning centre and programme themes',NIC),('Course index without readable current offers',NIC+'cursos/'));out.append(p)
 return out

def update_report(report):
 rows=make_profiles();by={p['id']:p for p in rows};old={p['id'] for p in report['profiles']}
 report['profiles']=[by.get(p['id'],p) for p in report['profiles']]+[p for p in rows if p['id'] not in old]
 report['counts'].update(dossiers=len(report['profiles']),countries=len({p['iso'] for p in report['profiles']}),swiss=sum(p['iso']=='CHE' for p in report['profiles']),by_status=dict(Counter(p['timing']['status'] for p in report['profiles'])),source_urls=len({s['url'] for p in report['profiles'] for s in p['sources']}))
 report['countries']=[dict(country=c,count=n) for c,n in sorted(Counter(p['country'] for p in report['profiles']).items())];report.update(version=169,asof=CHECKED)

TBOX_ROUTE=T('Только школьные команды: 4 ученика одной школы + преподаватель-coach; один ученик в одной команде / категории. Большинство категорий требует программу TBox у школы. Открытая web+AI категория допускает школы без TBox, но с 7 класса. Два брата не полная команда; паспорта не заменяют школьный вход. Школы из всей LATAM допускаются по общим правилам 2026, новые условия 2027 неизвестны.',
 'Solo equipos escolares: 4 alumnos del mismo colegio + docente-coach; un alumno en un equipo / categoría. Mayoría de categorías exige programa TBox del colegio. Categoría abierta web+AI admite colegios sin TBox, pero desde 7.º curso. Dos hermanos no forman equipo completo; pasaportes no sustituyen acceso escolar. Reglas generales 2026 admiten colegios de toda LATAM, condiciones nuevas 2027 desconocidas.')
TBOX_RULE_GAP=T('Основная страница категорий прочитана. Восемь связанных PDF возвращают 404; шесть JPG-страниц Expo / En Vivo содержат фон без текстового слоя, BIN также недоступны. Технические таблицы, возрастные исключения и точные допустимые наборы из этих viewer не считаются проверенными.',
 'Página principal de categorías leída. Ocho PDF enlazados devuelven 404; seis páginas JPG Expo / En Vivo contienen fondo sin capa de texto, BIN también inaccesibles. Tablas técnicas, excepciones de edad y kits exactos de estos viewer no considerados verificados.')
TBOX_SUBMIT=T('Для применимых проектных категорий: PDF-предложение, исходники и видео ≤6 минут; публикация видео в YouTube / виртуальной выставке требует согласия родителей. Есть отдельные исключения в правилах категорий. Для активации минимум 5 команд, иначе возможен показ. Квалификация / тренировка En Vivo и drones, предоценка Expo / 3D зависят от конкретных условий.',
 'Para categorías de proyectos aplicables: propuesta PDF, fuentes y vídeo ≤6 minutos; publicación de vídeo en YouTube / feria virtual requiere autorización parental. Reglas de categorías contienen excepciones. Activación con mínimo 5 equipos, de lo contrario posible exhibición. Clasificación / entrenamiento En Vivo y drones, preevaluación Expo / 3D dependen de condiciones concretas.')

def competition_rows(d):
 country=next(c for c in d['countries'] if c['iso']=='SLV');rows=[]
 cats=[('Scratch','Aventuras espaciales con Scratch','4–6','Scratch',['coding','games'],'virtual'),('GDevelop','Exploración espacial con GDevelop','6–9','GDevelop',['coding','games'],'virtual'),('App Inventor','Aplicaciones espaciales','10–12','App Inventor',['coding'],'virtual'),('En Vivo','Robótica en vivo','4+',T('Допустимые наборы не прочитаны: связанный регламент недоступен.','Kits admisibles sin leer: reglamento enlazado inaccesible.'),['robotics','coding'],'in_person'),('Drones','Control de drones','7+','DJI Neo · version 1',['drones','engineering'],'in_person'),('Expo','Expo Robótica','preescolar–bachillerato',T('Технология по школьному подуровню; точная таблица пока недоступна.','Tecnología según subnivel escolar; tabla exacta aún inaccesible.'),['robotics','engineering'],'in_person'),('3D','Modelado e impresión 3D','7+','Tinkercad + 3D printer',['engineering','art'],'in_person'),('Web AI','Desarrollo web con inteligencia artificial','7+',T('AI tools по выбору команды.','AI tools elegidas por equipo.'),['ai','coding'],'virtual')]
 for i,(key,title,grade,gear,themes,mode) in enumerate(cats,1469):
  row=event('C'+str(i),'Código TBox · '+title+' · next season',country['country'],TBOX+'page2.html',iso=['SLV'],region=country['region'],league_id='codigo-tbox',city=T('Онлайн / школа LATAM' if mode=='virtual' else 'Soyapango / San Salvador · El Salvador', 'Online / colegio LATAM' if mode=='virtual' else 'Soyapango / San Salvador · El Salvador'),age=T('Школьные классы: '+grade+'. Это не числовой возраст.','Cursos escolares: '+grade+'. No es edad numérica.'),mat=GRADE,osc=GRADE,format=T('4 ученика одной школы + преподаватель','4 alumnos de mismo colegio + docente'),team_min=4,team_max=4,entry=TBOX_ROUTE,gear=gear,language=LANG,themes=themes,scope='regional',level=T('C — региональная школьная серия LATAM','C — serie escolar regional LATAM'),period=NEXT,action=TBOX_ROUTE+' '+NEXT,note=TBOX_RULE_GAP+' '+TBOX_SUBMIT,proof=T('Прочитаны страницы 2026: категории, школьные условия, календарь. Восемь карточек — дисциплины одной серии, не восемь независимых турниров.',
   'Leídas páginas 2026: categorías, condiciones escolares, calendario. Ocho fichas son disciplinas de una serie, no ocho torneos independientes.'),date_scope='next_season_watch',admission_kind='school_selection',registration_status=NEXT,references=[dict(label='General school entry rules 2026',url=TBOX+'page1.html'),dict(label='Completed 2026 calendar',url=TBOX+'page3.html')],delivery_mode=mode)
  row['cost']=UNKNOWN
  if key=='Expo':row['note']+=' '+T('Оба ребёнка могут быть кандидатами только по реальному школьному уровню и технологии; нельзя объявить две возрастные подкатегории без читаемой таблицы.',
   'Ambos niños pueden ser candidatos solo según nivel escolar real y tecnología; sin declarar dos subcategorías de edad sin tabla legible.')
  rows.append(row)
 for ident,kind,path in [('C1477','RoboMission Elementary','robomission'),('C1478','Future Innovators Elementary','future-innovators')]:
  gear=T('Свободные hardware / software; автономный робот ≤25×25×25 cm. Конкретные правила сезона и совместимость набора отдельно.',
   'Hardware / software libres; robot autónomo ≤25×25×25 cm. Reglas de temporada y compatibilidad de kit aparte.') if path=='robomission' else T('Свободные материалы / controller / software; проект в stand 2×2×2 m. В сезоне 2026 отчёт и видео ≤90 секунд до 29 июля.',
   'Materiales / controller / software libres; proyecto en stand 2×2×2 m. Temporada 2026 exigía informe y vídeo ≤90 segundos hasta 29 de julio.')
  row=event(ident,'WRO El Salvador · '+kind+' · next season',country['country'],WRO+'categor%C3%ADas/'+path,iso=['SLV'],region=country['region'],league_id='wro-el-salvador',age=T('Опубликовано 2026: Elementary 8–12; максимальный возраст в календарном году соревнования. Правила 2027 ещё неизвестны.',
   'Publicado 2026: Elementary 8–12; edad máxima en año natural de competición. Reglas 2027 aún desconocidas.'),mat=T('Условно: родился в 2017, в календарном 2027 исполнится 10; новые правила и национальный вход отдельно.',
   'Condicional: nacido en 2017, en año natural 2027 cumple 10; nuevas reglas y acceso nacional aparte.'),osc=T('Условно: родился в 2020, в календарном 2027 исполнится 7 — ниже опубликованных 8. Возможность младшего участника в старшей команде не доказана страницей; не считать готовым допуском.',
   'Condicional: nacido en 2020, en año natural 2027 cumple 7 — menor del mínimo publicado 8. Página no acredita posibilidad de menor en equipo mayor; no considerar admisión lista.'),team_min=2,team_max=3,format=T('2–3 ученика + coach; для международного coach 18+.','2–3 alumnos + coach; coach internacional 18+.'),gear=gear,entry=T('Национальная квалификация → рейтинг → национальная олимпиада → возможная международная квота через national organizer. Иностранный / нерезидентский маршрут и выбор страны команды ещё не подтверждены.',
   'Clasificación nacional → ranking → olimpiada nacional → posible cupo internacional mediante national organizer. Ruta extranjera / no residente y país del equipo aún sin confirmar.'),period=NEXT,language=LANG,scope='national',level=T('B — национальный квалификационный путь','B — ruta de clasificación nacional'),admission_kind='qualification',date_scope='next_season_watch',registration_status=NEXT,action=GATE,note=NEXT,references=[dict(label='National entry route and inclusions',url=WRO+'c%C3%B3mo-participar'),dict(label='Closed 2026 calendar',url=WRO+'calendario-2026')])
  rows.append(row)
 return rows

def enrich_v169(d):
 rows=competition_rows(d);by={e['id']:e for e in d['events']}
 by['C095'].update(checked=CHECKED,languages=[],language=LANG,language_certainty=LANG,language_mode='unconfirmed',
  mat=T('Условно: 2017 год рождения → 10 в календарном 2027; Junior 7–10 только по опубликованным правилам 2026.',
   'Condicional: nacimiento 2017 → 10 en año natural 2027; Junior 7–10 solo según reglas publicadas 2026.'),
  osc=T('Условно: 2020 год рождения → 7 в календарном 2027; граница Elementary 5–7 / Junior 7–10 пересекается, дивизион подтвердить.',
   'Condicional: nacimiento 2020 → 7 en año natural 2027; límite Elementary 5–7 / Junior 7–10 se solapa, confirmar división.'),
  note=T('По максимальному возрасту за календарный год в 2027 Матвею 10, Оскару 7. Если рамки 7–10 сохранятся, оба могут быть возрастными кандидатами Junior; правила 2027, иностранный вход и границу 7 уточнить. На странице есть несогласованные вводные «с 4» / общий итог «5–10»; применены явные дивизионы 5–7 / 7–10. RoboStarter формативный и не даёт мировой квоты.',
   'Por edad máxima del año natural en 2027 Matvey 10, Oscar 7. Si se mantienen límites 7–10, ambos podrían ser candidatos Junior por edad; confirmar reglas 2027, acceso extranjero y límite 7. Página contiene introducciones discordantes «desde 4» / resumen «5–10»; aplicadas divisiones explícitas 5–7 / 7–10. RoboStarter es formativo y no concede cupo mundial.'))
 by['C099'].update(checked=CHECKED,language=LANG,languages=[],language_certainty=LANG,language_mode='unconfirmed',references=[dict(label='Bootcamp age groups are not competition regulations',url=BOOT),dict(label='Organizational 2026 calendar, not open enrollment',url=PLAN)])
 for e in rows:
  if e['id'] in by:by[e['id']].update(e)
  else:d['events'].append(e);by[e['id']]=e
 for n,p in enumerate(make_profiles(),476):
  country=next(c for c in d['countries'] if c['iso']==p['iso'])
  def fit(child):
   s=p['family_fit'][child]['status']
   return T('Нет сейчас — вне возрастной группы','No ahora — fuera del grupo de edad') if s in ['later','not_eligible'] else T('Условно — набор, возраст и язык подтвердить','Condicional — confirmar convocatoria, edad e idioma')
  e=event('L'+str(n),p['provider'],country['country'],p['sources'][0]['url'],block='Лагеря',iso=[p['iso']],region=country['region'],city=p['place'],age=p['age'],mat=fit('matvey'),osc=fit('oscar'),format=p['accommodation'],entry=GATE,gear=p['programme'],language=p['language'],cost=p['price']['label'],period=p['timing']['label'],note=p['programme']+' '+GATE,themes=p['themes'],participation='online_course' if p['formats']==['online'] else 'holiday_workshop',camp_programme_id=p['id'],camp_dossier_slug=p['slug'],reward=EDU,scope='local',level=T('D — местная учебная программа','D — programa educativo local'),references=[dict(label=s['title'],url=s['url']) for s in p['sources']],date_scope='next_season_watch',admission_kind='unknown')
  e['participation']={'regular_course':'regular','online_course':'regular','extracurricular_centre':'regular','holiday_camp':'holiday_workshop','undated_camp':'unconfirmed_program'}[p['programme_type']]
  existing=by.get(e['id'])
  if existing:existing.update(e)
  else:d['events'].append(e);by[e['id']]=e
  q=next(q for q in d['camp_programmes']['profiles'] if q['id']==p['id']);q['related_event_ids']=list(dict.fromkeys(q.get('related_event_ids',[])+[e['id']]))
  if not any(x['programme_id']==p['id'] and x['event_id']==e['id'] for x in d['camp_programmes']['event_links']):d['camp_programmes']['event_links'].append(dict(programme_id=p['id'],event_id=e['id'],relation='existing_programme'))
 trows=rows[:8];wrows=[by['C095']]+rows[8:]
 leagues=[programme('codigo-tbox','Código TBox · LATAM school STEAM','regional',T('По классам: Expo preschool–bachillerato; Scratch 4–6; GDevelop 6–9; App 10–12; остальные 4+ / 7+.','Por cursos: Expo preschool–bachillerato; Scratch 4–6; GDevelop 6–9; App 10–12; resto 4+ / 7+.'),['unknown'],[e['id'] for e in trows],summary=TBOX_ROUTE,route=TBOX_ROUTE,hardware=T('Scratch / GDevelop / App Inventor / Tinkercad / DJI Neo v1; точные робототехнические наборы пока не прочитаны.','Scratch / GDevelop / App Inventor / Tinkercad / DJI Neo v1; kits robóticos exactos aún sin leer.'),language=LANG,cost=UNKNOWN,importance=T('Школьная региональная серия для проектов и подготовки; статус мирового финала / единого мирового рейтинга не установлен.','Serie escolar regional para proyectos y preparación; sin acreditar condición de final mundial / ranking mundial único.'),strengths=TBOX_SUBMIT,nuances=[NEXT,TBOX_RULE_GAP,TBOX_SUBMIT],requirements=[TBOX_ROUTE,GATE],award=T('Призовые места по категориям; видео / диплом участия не доказательство международного выигрыша.','Puestos premiados por categorías; vídeo / diploma de participación no prueban triunfo internacional.'),sources=[dict(title='School rules and four-student teams',url=TBOX+'page1.html',checked=CHECKED),dict(title='Eight categories and grade gates',url=TBOX+'page2.html',checked=CHECKED),dict(title='2026 completed dates',url=TBOX+'page3.html',checked=CHECKED)],evidence=NEXT),
 programme('wro-el-salvador','WRO El Salvador · RoboStarter / Elementary','regional',T('RoboStarter Elementary 5–7 / Junior 7–10; Mission / Innovators Elementary 8–12 по 2026.','RoboStarter Elementary 5–7 / Junior 7–10; Mission / Innovators Elementary 8–12 según 2026.'),['6','9','10-12'],[e['id'] for e in wrows],summary=by['C095']['note'],route=rows[-1]['entry'],hardware=T('RoboStarter RoboRobo ≤25×25×35 cm; Mission свободный набор ≤25×25×25 cm; Innovators свободный проект ≤2×2×2 m. Это три разных ограничения.','RoboStarter RoboRobo ≤25×25×35 cm; Mission kit libre ≤25×25×25 cm; Innovators proyecto libre ≤2×2×2 m. Tres límites distintos.'),language=LANG,cost=T('Регистрация национальной олимпиады включает badge, завтрак, обед и диплом для команды / coach по странице 2026. $70 — старый поздний взнос июля 2026, не текущая цена 2027. Международная поездка за счёт команды.','Inscripción de olimpiada nacional incluye badge, desayuno, almuerzo y diploma para equipo / coach según página 2026. $70 era tarifa tardía julio 2026, no precio actual 2027. Viaje internacional a cargo del equipo.'),award=by['C095']['reward'],importance=T('Реальный национальный путь WRO; младшая RoboStarter без международной квалификации, старшие категории — через отбор и квоту.','Ruta nacional real WRO; RoboStarter menor sin clasificación internacional, categorías mayores mediante selección y cupo.'),requirements=[GATE,rows[-1]['entry']],nuances=[by['C095']['note'],NEXT],sources=[dict(title='RoboStarter rules',url=STARTER,checked=CHECKED),dict(title='National route',url=WRO+'c%C3%B3mo-participar',checked=CHECKED),dict(title='2026 calendar',url=WRO+'calendario-2026',checked=CHECKED)],evidence=NEXT)]
 for pr,es in zip(leagues,[trows,wrows]):
  pr['categories']=[dict(name=e['title'],age=e['age'],team=e['format'],hardware=e['gear'],entry=e['entry'],event_id=e['id']) for e in es]
  profiles=d['league_guide']['profiles'];existing=next((x for x in profiles if x['id']==pr['id']),None)
  if existing:existing.update(pr)
  else:profiles.append(pr)
 d['league_guide'].update(version=169,checked=CHECKED)
 known={s['url'] for s in d['sources']}
 for e in rows+[by['C095'],by['C099']]+[by['L'+str(i)] for i in range(476,485)]:
  for s in [dict(title=e['title'],url=e['source'])]+[dict(title=x['label'],url=x['url']) for x in e.get('references',[])]:
   if s['url'] not in known:d['sources'].append(dict(**s,checked=CHECKED,evidence=GATE));known.add(s['url'])
 d['central_america_v169']=dict(version=169,checked=CHECKED,new_camp_dossiers=9,new_competition_category_watches=10,new_league_profiles=2,new_confirmed_dates=0,fully_audited_countries=0,worldwide_complete=False)
