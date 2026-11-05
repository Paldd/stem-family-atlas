"""Oceania programmes: real daily age gates, equipment and family tariff units."""
from collections import Counter
from copy import deepcopy
from camp_east_asia_v159 import base, add as _add, age_fit, candidate
from camp_europe_v148 import weekdays

CHECKED='2026-11-05'
SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
STEAM='https://enrolmy.com/steam-ed/activity/194-January_2027_Holidays'
STEAM_PDF='https://s3-ap-southeast-2.amazonaws.com/enrolmy-nz/steam-ed/09183-docs/100/gau3doxr2zhqw56py84x.pdf'
SCR='https://scratchpad.co.nz/'
SCR_HOL=SCR+'after-school-coding-programmes/school-holiday-programme/'
SCR_TERMS=SCR+'registration-terms-conditions/'
TOT='https://www.totarasprings.org.nz/'
TOT_BOOK='https://book.venue.life/totarasprings/register/'
LSNZ='https://www.lsnz.co.nz/holiday-programme-young-learners'
BRAIN='https://www.brainplay.co.nz/'
CARA='https://www.caraeducation.com.au/camps/'
YOUNG='https://www.trybooking.com/au/event/1661016'
SK='https://www.trybooking.com/au/event/1671420'
AU='https://www.steampowerededucation.com.au/'
AU_POST=AU+'post/summer-school-holiday-programs-26-27'
AU_PDF='https://7da4c9e8-cb2e-44da-9256-b1f8e378e2c0.usrfiles.com/ugd/53628d_b2a3ff67078e440bb6fd2c678b387cb6.pdf?dn=Summer%202627%20Holiday%20Programs.pdf'
LOOK='https://stemlook.com.au/'
GIO='https://kids.giofai.com.au/'
LANG=T('Прямое подтверждение языка занятий EN / ES / RU не найдено. Английский сайт и страна не заменяют подтверждение преподавателя; язык выбранной группы уточнить.',
 'Sin localizar confirmación expresa del idioma de clases EN / ES / RU. Web inglesa y país no sustituyen confirmación docente; verificar idioma del grupo elegido.')
GATE=T('Подтвердить индивидуальный иностранный приём, язык, уровень после трёх лет соревнований, место и полный счёт. Формы, согласия, сообщения, брони и оплаты не выполнялись.',
 'Confirmar admisión extranjera individual, idioma, nivel tras tres años de competiciones, plaza y factura completa. Sin formularios enviados, consentimientos, mensajes, reservas ni pagos.')
GRADE=T('Условие по реальному школьному классу; классы детей неизвестны. Возраст 9 / 6 и годы рождения 2017 / 2020 не заменяют подтверждение класса.',
 'Condición según curso escolar real; cursos de los niños desconocidos. Edades 9 / 6 y años de nacimiento 2017 / 2020 no sustituyen confirmación del curso.')
TRIP=T('Дорога, внешнее жильё семьи, питание вне включений и итоговые сборы отдельно; неизвестная сумма не ноль.',
 'Viaje, alojamiento familiar externo, comida fuera de inclusiones y cargos finales aparte; importe desconocido no es cero.')
UNPRICED=T('Итог выбранной опции и налоги / сборы уточнить; публичный диапазон не цена любого отдельного занятия.',
 'Confirmar total de opción elegida e impuestos / cargos; rango público no es precio de cualquier clase individual.')
STEAM_CANCEL=T('Карточка 2027: 7 дней уведомления для возврата; плакат говорит более 7 дней, за меньше 7 — без возврата кроме согласованных обстоятельств / заполнения из waitlist. Границу ровно 7 дней подтвердить. При отмене организатором полный возврат. Старые общие terms 2025 содержат NZD 60/день, но выбранный курс и плакат 2027 — NZD 66. Поздний pickup NZD 10/15 минут. OSCAR — субсидия, не имя ребёнка и не автоматическая скидка иностранной семье.',
 'Ficha 2027: aviso de 7 días para devolución; cartel indica más de 7 días, con menos de 7 sin devolución salvo circunstancias acordadas / plaza cubierta desde waitlist. Confirmar límite de exactamente 7 días. Cancelación del organizador: devolución total. Terms generales antiguos 2025 indican NZD 60/día, curso elegido y cartel 2027 NZD 66. Recogida tardía NZD 10/15 minutos. OSCAR es subsidio, no nombre del niño ni descuento automático para familia extranjera.')
SCR_CANCEL=T('Holiday policy: отмена до 7 дней — возврат минус NZD 25; внутри 7 дней без возврата. Пропуски не возвращаются; неожиданная болезнь может дать кредит на 6 месяцев. В другой части описана оценка после первого дня с уведомлением за 6 часов до второго; применимость к однодневной программе согласовать. Договор не принимался.',
 'Holiday policy: cancelación hasta 7 días — devolución menos NZD 25; dentro de 7 días sin devolución. Ausencias sin devolución; enfermedad inesperada puede dar crédito por 6 meses. Otra sección describe evaluación tras primer día con aviso 6 horas antes del segundo; acordar aplicación a programa de un día. Contrato sin aceptar.')
FAITH=T('Общий outdoor / семейный лагерь с христианским содержанием, не технический курс. Религиозная составляющая заявлена организатором; язык и готовность семьи к программе уточнить.',
 'Campamento general outdoor / familiar con contenido cristiano, no curso técnico. Organizador declara componente religioso; confirmar idioma y compatibilidad familiar con programa.')

def source(label,url):return dict(title=label,url=url,checked=CHECKED)
def add(*args,**kwargs):
 scope=kwargs.pop('date_scope',None)
 _add(*args,**kwargs)
 if scope:args[0]['timing']['session_details'][-1]['date_scope']=scope
def B(i,slug,name,iso,place,themes,age,formats=None):
 p=base('CP'+str(i),slug,name,iso,'Новая Зеландия' if iso=='NZL' else 'Австралия',place,themes)
 p.update(age=age,language=LANG,questions=[GATE],formats=formats or ['day'])
 p['price'].update(label=UNPRICED,extras=TRIP,deposit=UNPRICED)
 return p
def fit(p,lo,hi,start='2027-01-01'):p['family_fit']=age_fit(lo,hi,start)
def grade(p):p['family_fit']={c:candidate('unknown',GRADE) for c in ['matvey','oscar']}
def refs(p,*rows):p['sources']=[source(a,b) for a,b in rows]

STEAM_DAYS=[
 ('2027-01-14','robotics','Freestyle Robotics',5),('2027-01-15','general','Polymer Clay Creations',5),
 ('2027-01-18','general','ABCs of Bees',5),('2027-01-19','robotics','Emergency Vehicles',5),
 ('2027-01-20','general','Design a Playground',5),('2027-01-21','music','Create Music & Dancing Robots',8),
 ('2027-01-22','minecraft','Minecraft Mania',7),('2027-01-25','general','Mark Rober Crunchlab',5),
 ('2027-01-26','combat','Combat Robotics',8),('2027-01-27','general','Build a Tiny House',5),
 ('2027-01-28','general','Pasifika STEAM',5),('2027-01-29','robotics','Freestyle Robotics',5)]
AU_DAYS=['2026-12-15','2026-12-16','2026-12-17','2027-01-05','2027-01-06','2027-01-07','2027-01-12','2027-01-13','2027-01-14']
AU_TOPICS={
 'junior':['Slime Lab','Robot Rescue Lab','Santas Toy Workshop','Treasure Hunt Math','Dinosaurs','Human Body Lab','Rocket Rangers','Super STEM Heroes','Creature Lab'],
 'youth':['Forensic Crime Lab','AI & Robotics','Minecraft Education','Math & Magic','Lost Creatures: De-extinction','Anatomy','Rocket Rangers','AI & Robotics Lab','Game Makers Studio']}

def make_profiles():
 out=[]
 for ident,key,name,lo,themes in [(1265,'robotics','VEX Freestyle / Emergency Vehicles',5,['robotics','coding','engineering']),
  (1266,'general','Arts / Science / Engineering',5,['general','science','engineering','art']),
  (1267,'music','Music & Dancing Robots',8,['robotics','coding','art']),
  (1268,'combat','Combat Robotics',8,['robotics','engineering']),
  (1269,'minecraft','Minecraft Education',7,['coding','games'])]:
  p=B(ident,'steamed-nz-'+key,'STEAM-ED Tauranga · '+name,'NZL','671 Cameron Road · Tauranga South · Tauranga 3112',themes,str(lo)+'–13')
  p['programme']=T('Дневные самостоятельные занятия по выбранным датам, 09:00–15:00. VEX robotics, проекты искусства / науки / инженерии, BandLab и танцующие роботы, Minecraft Education и внутренний Combat Robotics по разным дням. Внутренний Giant Donut trophy не результат международной лиги.',
   'Clases diurnas independientes en fechas elegidas, 09:00–15:00. VEX robotics, proyectos de arte / ciencia / ingeniería, BandLab y robots que bailan, Minecraft Education y Combat Robotics interno en días distintos. Giant Donut trophy interno no es resultado de liga internacional.')
  p['timing']['label']=T('14–29 января 2027, 12 отдельных будних дней. В этой карточке только выбранная тема; не ежедневная одинаковая программа. 21 января: badge 8–13, текст over 8; для девятилетнего подходит, границу восьми лет уточнить.',
   '14–29 de enero de 2027, 12 días laborables separados. Esta ficha solo tema elegido; no programa idéntico diario. 21 de enero: badge 8–13, texto over 8; compatible con nueve años, confirmar límite de ocho.')
  p['price'].update(year=2027,currency='NZD',amount=66,unit='child_day',label=T('NZD 66 за ребёнка / выбранный день 2027; старый общий тариф 60 не применён.',
   'NZD 66 por niño / día elegido 2027; sin aplicar tarifa general antigua de 60.'),included=T('Заявленное занятие и оборудование STEAM-ED; личный kit домой обещан только для отдельных art / build проектов, не для каждого робота.',
   'Clase y equipo STEAM-ED anunciados; kit personal para llevar solo prometido en proyectos art / build concretos, no cada robot.'),extras=TRIP+' '+T('Принести lunch, snack, воду, закрытую обувь и одежду для поделок.','Traer lunch, snack, agua, calzado cerrado y ropa para manualidades.'),deposit=STEAM_CANCEL)
  fit(p,lo,13);refs(p,(T('Официальная карточка января 2027 и terms','Ficha oficial enero 2027 y terms'),STEAM),(T('Оригинальный двухстраничный плакат','Cartel original de dos páginas'),STEAM_PDF))
  for n,(day,k,topic,minimum) in enumerate(STEAM_DAYS):
   if k==key:add(p,day,day,'day-'+str(n+1),topic,'NZD 66',STEAM,days=[day],begin='09:00',finish='15:00',zone='Pacific/Auckland',admission_kind='unknown')
  out.append(p)
 for ident,key,name,lo,prices,path in [
  (1270,'code5','Roll Up Your Sleeves · Let Us Code',5,[110,145],'roll-sleeves-let-us-code/'),
  (1271,'mbot','mBot Robotics',7,[110,160],'code-the-bot/'),
  (1272,'edison','Edison Robotics',7,[110,155],'code-bot-program-edison-robot/'),
  (1273,'ai','Video Stories Using AI',9,[125,150],'bring-stories-to-life-create-videos-using-ai/'),
  (1274,'print','3D Printing',7,[110,145],'lets-learn-3d-printing/')]:
  p=B(ident,'scratchpad-nz-'+key,'SCRATCHPAD · '+name,'NZL',T('Auckland / Christchurch · конкретный центр и слот выбрать','Auckland / Christchurch · elegir centro y franja concretos'),['coding','robotics'] if key in ['mbot','edison'] else ['ai','art'] if key=='ai' else ['design','engineering'] if key=='print' else ['coding','games'],str(lo)+'+')
  p['programme']=T('Короткий технический holiday workshop. Coding 5+ — начальное знакомство; mBot — программирование датчиков, препятствий и линии; Edison — робототехника; AI — создание видеорассказа; 3D — моделирование и печать. Уровень после трёх лет соревнований оценить отдельно.',
   'Holiday workshop técnico corto. Coding 5+ es introducción; mBot programa sensores, obstáculos y línea; Edison robótica; AI creación de relato en vídeo; 3D modelado e impresión. Evaluar nivel tras tres años de competiciones por separado.')
  p.update(language=T('Собственные terms Course Delivery прямо: обучение на английском, нужны письменный / разговорный English и участие в групповых обсуждениях / презентациях. EN подтверждён для преподавания, не только для сайта.',
   'Terms propios Course Delivery explícitos: enseñanza en inglés, exige English escrito / hablado y participación en discusiones / presentaciones grupales. EN acreditado para enseñanza, no solo web.'),confirmed_instruction_languages=['EN'],language_evidence_role='primary')
  p['timing'].update(status='next_unannounced',label=T('Общая holiday-сетка содержит December / January без года; фактические product options местами расходятся с общей сеткой. У AI product стоит SEP 29, хотя общий список говорит JAN 26. Год и доступность отдельных вариантов не подтверждены; операционных дат нет.',
   'Calendario holiday general contiene December / January sin año; product options reales difieren en algunos casos del calendario. AI product indica SEP 29, lista general JAN 26. Año y disponibilidad de variantes sin confirmar; sin fechas operativas.'))
  p['price'].update(year=None,currency='NZD',amount=None,unit='selected_option',label=T('Диапазон product options NZD ','Rango de product options NZD ')+str(prices[0])+'–'+str(prices[1])+T(', GST включён. Длительность 09–15 / 09–17, ранний drop-off и аренда робота меняют пакет; не единый тариф и не гарантия места.',
   ', GST incluido. Duración 09–15 / 09–17, drop-off temprano y alquiler de robot cambian paquete; no tarifa única ni garantía de plaza.'),included=T('Состав техники и материалов выбранной опции подтвердить; у mBot / Edison есть Bring Your Own либо Rent. Аренда и покупка робота — разные условия.',
   'Confirmar equipo y materiales de opción elegida; mBot / Edison tienen Bring Your Own o Rent. Alquiler y compra de robot son condiciones distintas.'),deposit=SCR_CANCEL)
  fit(p,lo,99);p['questions'].append(T('Проверить конкретный год и вариант: часть JSON-вариантов помечена out of stock, это не означает закрытие всей сети. В корзину ничего не добавлялось.',
   'Comprobar año y variante concretos: parte de variantes JSON indica out of stock, no cierre de toda red. Sin añadir nada al carrito.'))
  refs(p,(name,SCR+'product/'+path),(T('Возрастные категории общей holiday-сетки','Categorías de edad del calendario holiday general'),SCR_HOL),(T('Английское преподавание и holiday cancellation','Enseñanza inglesa y holiday cancellation'),SCR_TERMS));out.append(p)
 p=B(1275,'totara-senior-kids-2027','Tōtara Springs · Senior Kids Camp','NZL','Matamata · Tōtara Springs',['general','sport'], '8–12',['boarding']);p['programme']=FAITH
 p['accommodation']=T('Самостоятельный детский пансион; минимальный возраст 8, готовность к ночёвкам и сопровождение уточнить.','Residencia infantil sin padres; edad mínima 8, confirmar preparación para pernoctar y supervisión.')
 p['timing'].update(status='partial_2027',label=T('Body и страница Kids Camp: 25–29 января 2027. Header собственной booking page: 24–29 января. Точный заезд противоречив, в операционный календарь не добавлен.',
  'Body y página Kids Camp: 25–29 de enero de 2027. Header de booking page propia: 24–29 de enero. Llegada exacta contradictoria, sin añadir a calendario operativo.'))
 p['price'].update(year=2027,currency='NZD',amount=255,unit='child_camp',label=T('NZD 255 за одного camper; аванс 50 входит в цену, остаток до / в первый день. Shuttle Auckland–Matamata 30 в одну сторону; не обязательная доплата.',
  'NZD 255 por camper; anticipo 50 incluido en precio, saldo antes de / en primer día. Shuttle Auckland–Matamata 30 por trayecto; no cargo obligatorio.'),included=T('Overnight camp по выбранному детскому тарифу; конкретное меню, бельё и отмена уточняются.','Overnight camp según tarifa infantil elegida; confirmar menú, ropa de cama y cancelación.'))
 fit(p,8,12);refs(p,('Kids Camp',TOT+'kids-camp/'),('Senior Kids Camp Summer 2027',TOT_BOOK+'senior-kids-camp-summer27'));out.append(p)
 for ident,key,name,start,end in [(1276,'summer','Summer Family Camp B','2027-01-03','2027-01-08'),(1277,'easter','Easter Family Camp','2027-03-26','2027-03-29')]:
  page=TOT+('family-camp/' if key=='summer' else 'easter-camp/');book=TOT_BOOK+('family-camp-b-27' if key=='summer' else 'easter-camp-2027')
  p=B(ident,'totara-family-'+key,'Tōtara Springs · '+name,'NZL','Matamata · Tōtara Springs',['general','sport'],'all ages',['family','boarding']);p['programme']=FAITH
  p['accommodation']=T('Семья живёт вместе: собственная палатка, cabin, ensuite или lodge по отдельным ценам. Семейные adult + child тарифы не стоимость самостоятельного пансиона двух детей.',
   'Familia alojada junta: tienda propia, cabin, ensuite o lodge con precios separados. Tarifas familiares adult + child no son coste de residencia independiente de dos niños.')
  p['timing']['label']=T('Подтверждённый диапазон этой семейной смены по своей booking page; заезд, выезд и места отдельно.',
   'Rango de esta sesión familiar acreditado por booking page propia; confirmar llegada, salida y plazas.')
  if key=='summer':p['timing']['label']+=' '+T('Family Camp A отдельно: landing 27.12.2026–02.01.2027, FAQ и booking 27.12–01.01. Конфликт окончания A сохранён; A не добавлен как подтверждённая смена.',
   'Family Camp A aparte: landing 27.12.2026–02.01.2027, FAQ y booking 27.12–01.01. Conservado conflicto de fin de A; A no añadido como sesión confirmada.')
  tariff=T('NZD за человека / всю смену B, adult 13+ / child 4–12: unpowered tent 430 / 330; powered 450 / 350; new cabin 550 / 450; ensuite 630 / 530; lodge 660 / 560. Infant 0–3 бесплатно. Аванс 500 за семью входит в итог. У ensuite / lodge waitlist; cabin показывает 1 place, значение для семьи из четырёх подтвердить.',
   'NZD por persona / sesión B completa, adult 13+ / child 4–12: unpowered tent 430 / 330; powered 450 / 350; new cabin 550 / 450; ensuite 630 / 530; lodge 660 / 560. Infant 0–3 gratis. Anticipo 500 por familia incluido en total. Ensuite / lodge con waitlist; cabin muestra 1 place, confirmar significado para familia de cuatro.') if key=='summer' else T('NZD за человека / всю Easter смену, adult 13+ / child 4–12: unpowered tent 198 / 127; powered 220 / 150; cabin 253 / 165; ensuite 264 / 198; lodge 303 / 231. Infant 0–3 бесплатно. Аванс 200 за семью входит в итог; ensuite / lodge отмечены waitlist.',
   'NZD por persona / sesión Easter completa, adult 13+ / child 4–12: unpowered tent 198 / 127; powered 220 / 150; cabin 253 / 165; ensuite 264 / 198; lodge 303 / 231. Infant 0–3 gratis. Anticipo 200 por familia incluido en total; ensuite / lodge marcados waitlist.')
  p['price'].update(year=2027,currency='NZD',amount=330 if key=='summer' else 127,unit='child_with_family_tent',label=tariff,included=T('Полный семейный пакет проживания / питания / основных активностей по выбранной категории; палатка и бельё по правилам категории, поездка отдельно.',
   'Paquete familiar completo de alojamiento / comida / actividades básicas según categoría elegida; tienda y ropa de cama según categoría, viaje aparte.'),extras=TRIP,deposit=tariff)
  fit(p,0,99);refs(p,(name,page),(T('Реальные family тарифы и состояние вариантов','Tarifas family reales y estado de variantes'),book))
  if key=='summer':p['sources'].append(source(T('Family A: конфликт дат и отличающийся waitlist','Family A: conflicto de fechas y waitlist distinto'),TOT_BOOK+'family-camp-a-27'))
  add(p,start,end,key,name,tariff,book,admission_kind='unknown');out.append(p)
 p=B(1278,'elrancho-family-2027','El Rancho · Family Camp 2027','NZL','Waikanae Beach · Kapiti Coast',['general','sport'],'all ages',['family','boarding']);p['programme']=T('Общие семейные каникулы: водные / outdoor активности, проживание и catered meals. Это не robotics camp и не замена Holiday Park, который предоставляет другое наполнение.',
  'Vacaciones familiares generales: actividades acuáticas / outdoor, alojamiento y catered meals. No es robotics camp ni sustituto de Holiday Park, que ofrece contenido distinto.')
 p['timing']['label']=T('5–8 января 2027. Собственная страница прямо сообщает SOLD OUT и длинный waitlist. Соседний Summer Holiday Park 27 декабря–1 января — другой пакет без полного питания / развлечений Family Camp.',
  '5–8 de enero de 2027. Página propia declara SOLD OUT y waitlist largo. Summer Holiday Park vecino 27 de diciembre–1 de enero es paquete distinto sin comida completa / entretenimiento Family Camp.')
 p['price']['deposit']=T('Аванс 20%, получить в течение 7 дней или место могут передать; полная оплата до 1 декабря. Это условия опубликованного, но заполненного лагеря, не подтверждение брони.',
  'Anticipo 20%, recibido en 7 días o pueden liberar plaza; pago total antes del 1 de diciembre. Condiciones de campamento publicado pero completo, no reserva acreditada.')
 p['accommodation']=T('Семейное проживание с питанием по пакету Family Camp; тип комнаты и цена неизвестны. Опубликованный набор заполнен.',
  'Alojamiento familiar con comida según paquete Family Camp; tipo de habitación y precio desconocidos. Convocatoria publicada completa.')
 p.update(availability=dict(status='sold_out',checked=CHECKED));fit(p,0,99);refs(p,('Family Camp 2027','https://www.elrancho.co.nz/Our%2BEvents/Family%2BCamp.html'));add(p,'2027-01-05','2027-01-08','sold-out','Family Camp 2027',UNPRICED,p['sources'][0]['url'],availability=p['availability'],admission_kind='closed');out.append(p)
 p=B(1279,'lsnz-christchurch-junior','LSNZ Christchurch · Junior Camp','NZL','Level 1 · 99 Cashel Street · Christchurch Central',['general','languages'],'14–17',['boarding']);p['programme']=T('Три недели: английский утром, культурные / природные поездки после обеда, homestay у местной семьи. Возраст 14–17, обоим детям пока рано; homestay не школьный пансион.',
  'Tres semanas: inglés por mañana, visitas culturales / naturales por tarde, homestay con familia local. Edad 14–17, aún demasiado pronto para ambos niños; homestay no es internado escolar.')
 p.update(language=T('English classes прямо заявлены; многоязычные сотрудники / материалы без перечня конкретных языков. ES / RU поддержка не обещана автоматически.',
  'English classes declaradas expresamente; personal / materiales multilingües sin lista concreta de idiomas. Sin prometer automáticamente apoyo ES / RU.'),confirmed_instruction_languages=['EN'],language_evidence_role='language_lessons')
 p['timing']['label']=T('Начала 11 января, 1 марта, 12 апреля, 5 и 26 июля 2027. Продолжительность 3 недели; точный checkout не опубликован. Каждая календарная запись отмечает только старт, не однодневную длительность всего лагеря.',
  'Inicios 11 de enero, 1 de marzo, 12 de abril, 5 y 26 de julio de 2027. Duración 3 semanas; checkout exacto sin publicar. Cada registro de calendario marca solo inicio, no duración total de un día.')
 p['price'].update(year=2027,currency='NZD',amount=4622,unit='three_week_from',label=T('От NZD 4622, GST включён, за 3 недели. From не окончательный полный invoice; медицинская страховка, диета и выбранный intake отдельно.',
  'Desde NZD 4622, GST incluido, por 3 semanas. From no es invoice final completo; seguro médico, dieta e intake elegido aparte.'),included=T('English course, ежедневные afternoon activities, homestay, placement, enrolment/material, junior surcharge и частный airport transfer перечислены в пакете.',
  'English course, actividades afternoon diarias, homestay, placement, enrolment/material, junior surcharge y airport transfer privado enumerados en paquete.'))
 p['accommodation']=p['programme'];fit(p,14,17);refs(p,('Junior Camp · Christchurch',LSNZ))
 for n,day in enumerate(['2027-01-11','2027-03-01','2027-04-12','2027-07-05','2027-07-26']):add(p,day,day,'intake-'+str(n+1),T('Старт трёхнедельного intake','Inicio de intake de tres semanas'),p['price']['label'],LSNZ,date_scope='activity_start',date_precision='published_start_only')
 out.append(p)
 p=B(1280,'brainplay-nz-holidays','Brain Play · Holiday Workshops','NZL','Auckland / Christchurch / Wellington / Hamilton',['robotics','coding','design'],'5–12')
 p['programme']=T('Робототехника, coding, 3D и инженерные holiday workshops через собственные и партнёрские площадки. Это провайдерский watch, не новый датированный летний поток.',
  'Holiday workshops de robótica, coding, 3D e ingeniería en sedes propias y asociadas. Watch de proveedor, no nueva cohorte estival fechada.')
 p['timing'].update(status='next_unannounced',label=T('Страница показывает October без года и старые сочетания дней недели. Январь 2027 не подтверждён, даты не перенесены.',
  'Página muestra October sin año y combinaciones antiguas de días semanales. Enero 2027 sin acreditar, sin trasladar fechas.'))
 p['price'].update(year=None,currency='NZD',amount=None,label=T('FAQ: half day NZD 48–60, full day 68–95; цена партнёрского события может отличаться. Не тариф конкретной смены 2027.',
  'FAQ: half day NZD 48–60, full day 68–95; precio de evento asociado puede diferir. No tarifa de sesión concreta 2027.'))
 fit(p,5,12);refs(p,('Holiday workshops',BRAIN+'events-and-holidays'),('Provider FAQ',BRAIN+'about'));out.append(p)
 p=B(1281,'cara-canberra-summer','CARA Canberra · Summer Camp','AUS','Level 1 · 55 Woolley Street · Dickson ACT 2602',['robotics','coding','ai','design'],'YEAR 6–12')
 p['programme']=T('Робототехника, engineering, coding / games, AI и 3D. Camp page прямо YEAR 6–12; младшие Pre-K / Year 1–2 относятся к регулярным курсам и не доказывают младший holiday camp.',
  'Robótica, engineering, coding / games, AI y 3D. Camp page explícita YEAR 6–12; Pre-K / Year 1–2 menores corresponden a cursos regulares y no acreditan holiday camp menor.')
 p['timing']['label']=T('Три опубликованных окна: 11–15, 18–22 и 25–29 января 2027. Третье по ошибке снова названо Week 2. Минимум 5 дней; дни работы и часы третьей недели, включая 26 января, подтвердить — ежедневные timed slots не созданы.',
  'Tres ventanas publicadas: 11–15, 18–22 y 25–29 de enero de 2027. Tercera erróneamente también llamada Week 2. Mínimo 5 días; confirmar días de funcionamiento y horas de tercera semana, incluido 26 de enero; sin franjas timed diarias.')
 p['price'].update(year=2027,currency='AUD',amount=130,unit='child_day_min5',label=T('AUD 130/день, минимум 5 дней: арифметически 650 за 5 оплачиваемых дней до уточнения налога. Single day только waitlist. 5% sibling / friend discount заявлен, база и применимость ещё подтвердить.',
  'AUD 130/día, mínimo 5 días: aritméticamente 650 por 5 días pagados antes de confirmar impuesto. Single day solo waitlist. Descuento sibling / friend 5% anunciado, confirmar base y aplicación.'),included=T('Все classroom equipment: robotics kits, microcontrollers, laptops, 3D materials, sensors, software subscriptions; morning / afternoon tea и фрукты. Lunch отдельно подтвердить.',
  'Todo classroom equipment: robotics kits, microcontrollers, laptops, materiales 3D, sensores, software subscriptions; morning / afternoon tea y fruta. Confirmar lunch aparte.'))
 grade(p);refs(p,('Holiday Camp · school-year gate',CARA),('January 11 booking',CARA+'book/3/'),('January 25 booking',CARA+'book/10/'))
 for a,b,key in [('2027-01-11','2027-01-15','week1'),('2027-01-18','2027-01-22','week2'),('2027-01-25','2027-01-29','week3')]:add(p,a,b,key,'Summer Camp',p['price']['label'],CARA,date_scope='camp_window',admission_kind='unknown')
 out.append(p)
 p=B(1282,'young-engineers-nsw-jan2027','Young Engineers NSW · LEGO Engineering / Robotics','AUS','Eastwood / Castle Hill / Baulkham Hills · NSW',['robotics','coding','engineering'],'Kindergarten–Year 6')
 p['programme']=T('LEGO механика и visual coding; старшим / опытным могут предложить SPIKE Prime, Scratch, sensors и вводный Arduino. Это не гарантия, что каждый ребёнок получит все модули. Начинающие допускаются, устройства и robotics equipment включены.',
  'Mecánica LEGO y visual coding; mayores / experimentados pueden explorar SPIKE Prime, Scratch, sensores y Arduino inicial. No garantiza todos los módulos a cada niño. Admite principiantes, dispositivos y robotics equipment incluidos.')
 p['timing']['label']=T('Четыре точных двухдневных кампуса: 11–12, 13–14, 18–19, 20–21 января 2027; также выбор одного дня. Общее рекламное окно до 22 января не доказательство занятия 22 числа. Drop-off 08:45–09:00, pickup 14:45–15:00; календарь основного дня 09–15.',
  'Cuatro campus exactos de dos días: 11–12, 13–14, 18–19, 20–21 de enero de 2027; también opción de un día. Ventana publicitaria hasta 22 de enero no prueba clase el 22. Drop-off 08:45–09:00, pickup 14:45–15:00; calendario de jornada principal 09–15.')
 p['price'].update(year=2027,currency='AUD',amount=120,unit='child_day',label=T('AUD 120 за один день или 215 за два; два single day стоят 240. Двухдневный пакет альтернативен отдельным дням, не три обязательных покупки. Финальные booking fees уточнить.',
  'AUD 120 por un día o 215 por dos; dos single day cuestan 240. Paquete de dos días alternativo a días individuales, no tres compras obligatorias. Confirmar booking fees finales.'),included=T('LEGO, robotics equipment, laptops / tablets для занятий включены; принести lunch, snacks и воду.','LEGO, robotics equipment, laptops / tablets de clases incluidos; traer lunch, snacks y agua.'))
 grade(p);refs(p,('January 2027 · organiser listing and four actual school venues',YOUNG))
 for k,a,b,place in [('eastwood','2027-01-11','2027-01-12','Eastwood Heights Public School · 9A Lincoln St · Eastwood NSW 2122'),('samuel-gilbert','2027-01-13','2027-01-14','Samuel Gilbert Public School · Ridgecrop Dr · Castle Hill NSW 2154'),('baulkham','2027-01-18','2027-01-19','Baulkham Hills North Public School · 2 Girralong Ave · NSW 2153'),('oakhill','2027-01-20','2027-01-21','Oakhill Drive Public School · 1–5 Oakhill Dr · Castle Hill NSW 2154')]:
  days=weekdays(a,b);add(p,a,b,k+'-two-day',place+' · '+T('2 дня','2 días'),'AUD 215',YOUNG,days=days,begin='09:00',finish='15:00',zone='Australia/Sydney',place=place,admission_kind='unknown')
  for day in days:add(p,day,day,k+'-'+day[-2:],place+' · '+T('1 день','1 día'),'AUD 120',YOUNG,days=[day],begin='09:00',finish='15:00',zone='Australia/Sydney',place=place,admission_kind='unknown')
 out.append(p)
 for ident,key,name,begin,finish,days,themes in [
  (1283,'paper','Paper Circuits','09:00','12:00',['11','12','18','19'],['engineering','science']),
  (1284,'breadboard','Breadboard Electronics','13:00','16:00',['11','12','18','19'],['engineering','robotics']),
  (1285,'scratch','Scratch Games','09:00','12:00',['13','14'],['coding','games']),
  (1286,'python','Python Animations','13:00','16:00',['13','14'],['coding','art'])]:
  p=B(ident,'sk-edge-'+key,'SK Robotics EDGE · '+name,'AUS','4 Kyneton Cct · Caroline Springs VIC 3023',themes,'8–15')
  p['programme']=T('Практические схемы с copper tape / LED либо breadboard с buzzer / traffic light; Scratch games и текстовый Python с геометрией. Собственные компоненты, а не только сборка готового робота. Четыре учебных направления одной площадки, не четыре независимых лагерных бренда.',
   'Circuitos prácticos con copper tape / LED o breadboard con buzzer / traffic light; juegos Scratch y Python textual con geometría. Componentes reales, no solo montaje de robot preparado. Cuatro temas educativos de una sede, no cuatro marcas independientes.')
  p['timing']['label']=T('11–14 и 18–21 января 2027. Вторая неделя повторяет четыре направления с продолжением по уровню; во вторую среду / четверг Python утром и Scratch после обеда, в первую наоборот. Один блок 3 часа; full day 09–16 включает lunch 12–13, не 7 учебных часов.',
   '11–14 y 18–21 de enero de 2027. Segunda semana repite cuatro temas con progresión por nivel; segundo miércoles / jueves Python por mañana y Scratch por tarde, primera semana al revés. Bloque de 3 horas; full day 09–16 incluye lunch 12–13, no 7 horas lectivas.')
  p['price'].update(year=2027,currency='AUD',amount=None,label=T('Структурированные данные объявления: AUD 150–920 по всем билетам события. Полная таблица цен отдельных half day / full day / bundles не получена; 150 не выдано за цену каждого модуля.',
   'Datos estructurados del anuncio: AUD 150–920 entre todos los billetes del evento. Sin tabla completa de half day / full day / bundles individuales; 150 no presentado como precio de cada módulo.'),included=T('Электронные компоненты и инструменты выдаются на занятии; для CODING нужен свой Windows laptop, зарядка и mouse. Принести nut-free lunch / snacks для full day. Максимум 12 учеников заявлен, не доказательство текущих мест.',
   'Componentes electrónicos y herramientas en clase; CODING requiere Windows laptop propio, cargador y mouse. Traer lunch / snacks sin frutos secos para full day. Máximo declarado 12 alumnos, no prueba de plazas actuales.'),deposit=T('5+ дней уведомления — полный возврат; 3–4 дня — 90%, 10% admin fee; меньше 72 часов — без возврата. Болезнь / emergency может дать перенос по усмотрению; при отмене SK полный возврат.',
   'Aviso con 5+ días — devolución total; 3–4 días — 90%, 10% admin fee; menos de 72 horas sin devolución. Enfermedad / emergency puede dar traslado discrecional; cancelación SK devolución total.'))
  fit(p,8,15);refs(p,('Summer Camp 2027 · exact modules / device rule / cancellation',SK))
  slots=[('2027-01-'+day,begin,finish) for day in days]
  if key=='scratch':slots += [('2027-01-'+day,'13:00','16:00') for day in ['20','21']]
  if key=='python':slots += [('2027-01-'+day,'09:00','12:00') for day in ['20','21']]
  for day,a,b in slots:add(p,day,day,key+'-'+day[-2:],name,p['price']['label'],SK,days=[day],begin=a,finish=b,zone='Australia/Melbourne',admission_kind='unknown')
  out.append(p)
 for ident,key,lo,hi,begin,finish in [(1287,'junior',6,8,'09:00','12:00'),(1288,'youth',9,13,'12:30','15:30')]:
  p=B(ident,'steam-powered-au-'+key,'STEAM Powered Education · '+key.title()+' Lab','AUS','Brisbane / Robina Gold Coast',['general','science','engineering','robotics']+(['coding','ai','games'] if key=='youth' else []),str(lo)+'–'+str(hi))
  p['programme']=T('Девять отдельных трёхчасовых workshops: младшим опыты, Robot Rescue, игрушки, динозавры и ракеты; старшим forensics, AI / robotics, Minecraft, anatomy, rockets и MakeCode games с micro:bit controller. Не одинаковый robotics camp каждый день.',
   'Nueve workshops independientes de tres horas: menores experimentos, Robot Rescue, juguetes, dinosaurios y cohetes; mayores forensics, AI / robotics, Minecraft, anatomy, rockets y juegos MakeCode con micro:bit controller. No robotics camp idéntico cada día.')
  p['timing']['label']=T('15–17 декабря 2026, 5–7 и 12–14 января 2027, вторник–четверг. PDF печатает невозможное 517th Dec; blog и реальные билеты прямо подтверждают 17 декабря. Gold Coast youth URL ошибочно содержит junior, фактический заголовок / часы youth. Один ticket description AI дублирует младший Robot Rescue; точный технический проект уточнить.',
   '15–17 de diciembre de 2026, 5–7 y 12–14 de enero de 2027, martes–jueves. PDF imprime imposible 517th Dec; blog y billetes reales confirman expresamente 17 de diciembre. URL Gold Coast youth contiene junior por error, título / horas reales son youth. Una descripción de billete AI duplica Robot Rescue menor; confirmar proyecto técnico exacto.')
  p['price'].update(year=2026,currency='AUD',amount=49,unit='child_workshop_early',label=T('AUD 49 early bird за workshop / 55 standard, GST включён; три workshop package 150. Текст before 30 Nov / after 1 Dec не объясняет границы 30 ноября и 1 декабря; promo cutoff не дедлайн регистрации.',
   'AUD 49 early bird por workshop / 55 standard, GST incluido; package de tres workshops 150. Texto before 30 Nov / after 1 Dec no aclara límites del 30 de noviembre y 1 de diciembre; promo cutoff no es plazo de registro.'),included=T('Материалы включены; для Tech workshops BYO device, совместимую модель и software уточнить. Brisbane venue TBD, Robina Community Centre: 196 Robina Town Centre Dr, QLD 4226.',
   'Materiales incluidos; Tech workshops con BYO device, confirmar modelo y software compatibles. Sede Brisbane TBD, Robina Community Centre: 196 Robina Town Centre Dr, QLD 4226.'),deposit=T('Отмена за 7+ дней — credit; менее 7 без возврата / credit, допускается передача другому ребёнку. По medical certificate credit либо 50% возврата. Условия групповых incursions не применены к holiday ticket.',
   'Cancelación con 7+ días — credit; menos de 7 sin devolución / credit, permite transferencia a otro niño. Con medical certificate credit o devolución 50%. Sin aplicar condiciones de incursions grupales a holiday ticket.'))
  fit(p,lo,hi);urls=[AU+'events/'+('junior-science-technology-labs-summer-26-27-brisbane' if key=='junior' else 'youth-science-technology-labs-summer-26-27-brisbane'),AU+'events/'+('junior-science-tech-workshops-goldcoast' if key=='junior' else 'junior-science-technology-labs-summer-26-27-goldcoast')]
  refs(p,('Summer School Holiday Programs 26/27',AU_POST),('Original Junior / Youth curriculum matrix',AU_PDF),('Brisbane course and tickets',urls[0]),('Gold Coast course and tickets',urls[1]),('Holiday cancellation',AU+'termsconditions'))
  for place,url,k in [(T('Brisbane · точный адрес TBD','Brisbane · dirección exacta TBD'),urls[0],'brisbane'),('Robina Community Centre · 196 Robina Town Centre Dr · QLD 4226',urls[1],'robina')]:
   for n,day in enumerate(AU_DAYS):add(p,day,day,k+'-'+str(n+1),AU_TOPICS[key][n],p['price']['label'],url,days=[day],begin=begin,finish=finish,zone='Australia/Brisbane',place=place,admission_kind='unknown')
  out.append(p)
 for ident,key,year_max,path,dates in [(1289,'ai',8,'ai-robot-engineers-camp-y2-y8/',[('chatswood','2026-12-18'),('chatswood','2027-01-18'),('chatswood','2027-01-28'),('burwood','2026-12-21'),('burwood','2027-01-21'),('zetland','2027-01-20')]),(1290,'robot',7,'robotics-and-coding-camp/',[('chatswood','2026-12-23'),('chatswood','2027-01-13'),('burwood','2026-12-22'),('burwood','2027-01-13'),('zetland','2026-12-18'),('zetland','2027-01-13')])]:
  url=LOOK+'products/'+path;p=B(ident,'stemlook-'+key+'-camp','STEMLOOK · '+('AI Robot Engineers' if key=='ai' else 'Robot Engineers'),'AUS','Chatswood / Burwood / Zetland · Sydney',['robotics','coding','engineering']+(['ai'] if key=='ai' else []),'Year 3–'+str(year_max))
  p['programme']=T('Практический robot camp 08:30–16:00: coding, maths, engineering и physics; у AI добавлены задачи искусственного интеллекта. Robot Engineers описывает 50% coding. Возрастная ступень определяется школьным Year 3–8 / 3–7, не цифрами в старом URL.',
   'Robot camp práctico 08:30–16:00: coding, maths, engineering y physics; AI añade retos de inteligencia artificial. Robot Engineers describe 50% coding. Nivel de edad determinado por curso Year 3–8 / 3–7, no cifras de URL antiguo.')
  p['timing']['label']=T('Шесть точных campus × day вариантов этой программы из собственного body и WooCommerce JSON; Camp ONLY и Camp + Robot — два тарифных варианта одного занятия, не две смены.',
   'Seis variantes campus × día exactas de este programa según body propio y WooCommerce JSON; Camp ONLY y Camp + Robot son dos tarifas de misma clase, no dos sesiones.')
  p['price'].update(year=2026,currency='AUD',amount=129,unit='child_day_camp_only',label=T('AUD 129 Camp ONLY; Camp + Robot ','AUD 129 Camp ONLY; Camp + Robot ')+str(410 if key=='ai' else 399)+T('. Robot RRP 350 не дополнительный обязательный сбор и не цена camp. Laptop hire product 17; единицу аренды, налог и окончательный checkout подтвердить.',
   '. Robot RRP 350 no es cargo obligatorio adicional ni precio del camp. Laptop hire product 17; confirmar unidad de alquiler, impuesto y checkout final.'),included=T('Робот предоставлен для использования в классе. Домой только при покупке Camp + Robot; BYO laptop / разрешённый iPad по конкретному курсу, иначе платная аренда. FAQ о выдаче робота со второго term относится к регулярным занятиям, не к camp-only пакету.',
   'Robot para uso en clase. Para casa solo al comprar Camp + Robot; BYO laptop / iPad admitido según curso, o alquiler de pago. FAQ de robot desde segundo term corresponde a clases regulares, no paquete camp-only.'))
  grade(p);refs(p,('Selected dated camp and option prices',url),('Separate device hire',LOOK+'products/laptop-hire-robotics-classes-camps/'))
  for city,day in dates:add(p,day,day,city+'-'+day.replace('-',''),city.title()+' · '+p['provider'],p['price']['label'],url,days=[day],begin='08:30',finish='16:00',zone='Australia/Sydney',place=city.title()+' · '+T('точный campus address подтвердить','confirmar campus address exacto'),admission_kind='unknown')
  out.append(p)
 p=B(1291,'giofai-future-ai-2027','GIofAI Kids · Future AI Innovators','AUS',T('Онлайн · Australian intake, зарубежный доступ уточнить','En línea · Australian intake, confirmar acceso desde extranjero'),['ai','coding'],'Junior 8–12; Senior 13–17',['online']);p['catalog_participation']='online'
 p['programme']=T('10 утренних занятий по 2 часа: machine learning, проверка ошибок AI, создание assistant и финальный проект. Junior 8–12, Senior 13–17; не подготовка к конкретной мировой лиге. Отзывы на сайте относятся к взрослым программам GIofAI, не доказательство результатов нового детского потока.',
  '10 clases matutinas de 2 horas: machine learning, comprobación de errores AI, creación de assistant y proyecto final. Junior 8–12, Senior 13–17; no preparación para liga mundial concreta. Reseñas del sitio corresponden a programas adultos GIofAI, no prueba de resultados de cohorte infantil nueva.')
 p['timing']['label']=T('4–15 января 2027, 10:00–12:00 AEDT по будням; 20 часов. Для Коста-Рики это 17:00–19:00 предыдущего календарного дня. Приём до 18 декабря 2026 без опубликованного часа; setup того же дня около 45 минут, точное время не найдено.',
  '4–15 de enero de 2027, 10:00–12:00 AEDT entre semana; 20 horas. En Costa Rica corresponde a 17:00–19:00 del día calendario anterior. Admisión hasta 18 de diciembre de 2026 sin hora publicada; setup ese día unos 45 minutos, sin hora exacta localizada.')
 p['price'].update(year=2027,currency='AUD',amount=595,unit='child_course_launch',label=T('AUD 595 launch до 1 декабря, затем 695; GST включён. Reservation 99 входит в 595, balance 496 до 1 декабря, полностью оплатить до 3 декабря. Additional child 449, но Оскару 6–7 и минимум 8 — скидка не делает его подходящим.',
  'AUD 595 launch antes del 1 de diciembre, luego 695; GST incluido. Reservation 99 incluida en 595, balance 496 hasta 1 de diciembre, pago completo hasta 3 de diciembre. Additional child 449, pero Oscar de 6–7 no cumple mínimo 8; descuento no lo hace elegible.'),included=T('Live teaching и coaching groups 10–12 по опубликованному предложению. Нужны компьютер, internet и webcam; телефон не подходит, tablet не рекомендован. Зарубежный доступ, фактический English и текущие места отдельно.',
  'Live teaching y coaching groups 10–12 según oferta publicada. Requiere ordenador, internet y webcam; teléfono no sirve, tablet no recomendado. Acceso extranjero, English real y plazas actuales aparte.'),deposit=T('99 refundable до 1 декабря; terms обещают full programme refund до конца Day 2. Deadline обучения 18 декабря отдельно от цены 1 декабря и оплаты 3 декабря. Consents на camera / запись / работу ребёнка не принимались.',
  '99 refundable hasta 1 de diciembre; terms prometen full programme refund hasta fin de Day 2. Plazo de admisión 18 de diciembre separado de precio 1 de diciembre y pago 3 de diciembre. Sin aceptar consents de cámara / grabación / trabajo infantil.'))
 p['accommodation']=T('Онлайн из дома, без проживания. Рекламируется across Australia; персональный доступ из Коста-Рики / Мексики ещё не доказан.',
  'En línea desde casa, sin alojamiento. Anunciado across Australia; acceso personal desde Costa Rica / México aún sin acreditar.')
 fit(p,8,12);refs(p,('January 2027 programme and real AEDT times',GIO),('Specific children programme payment / refund terms',GIO+'program-terms'))
 add(p,'2027-01-04','2027-01-15','junior','Future AI Innovators Junior',p['price']['label'],GIO,days=weekdays('2027-01-04','2027-01-15'),begin='10:00',finish='12:00',zone='Australia/Melbourne',deadline='2026-12-18',admission_kind='unknown');out.append(p)
 assert len(out)==27 and len({p['id'] for p in out})==27
 return out

def update_report(report):
 rows=make_profiles();idx={p['id']:p for p in rows};old={p['id'] for p in report['profiles']}
 report['profiles']=[idx.get(p['id'],p) for p in report['profiles']]+[p for p in rows if p['id'] not in old]
 report['counts'].update(dossiers=len(report['profiles']),countries=len({p['iso'] for p in report['profiles']}),by_status=dict(Counter(p['timing']['status'] for p in report['profiles'])),source_urls=len({s['url'] for p in report['profiles'] for s in p['sources']}))
 report['countries']=[dict(country=c,count=n) for c,n in sorted(Counter(p['country'] for p in report['profiles']).items())];report.update(version=163,asof=CHECKED)

def enrich_v163(d):
 for e in d['events']:
  if e.get('camp_programme_id')=='CP1278':e.update(priority=T('P4 — набор заполнен','P4 — grupo completo'),registration_status=T('Полностью заполнен; организатор сообщает длинный waitlist.','Completo; organizador anuncia waitlist largo.'))
 rows={p['id']:p for p in make_profiles()};offers=[]
 def offer(ident,profile,amounts,sessions,required=None,**extra):
  p=rows[profile];offers.append(dict(id=ident,slug=p['slug'],label=p['provider'],currency=p['price']['currency'],price_year=2027,format=p['formats'][0],children=list(amounts),base_by_child=amounts,discount_second=0,required=required or [],unknown_required=[dict(id='uncosted',unit='money',rate=1,min=0,label=T('Неуказанные обязательные расходы по итоговому счёту','Gastos obligatorios no indicados según factura final'))],optional=[],unknown_trip=['travel','lodging','misc'],sessions=sessions,sources=[s['url'] for s in p['sources']],checked=CHECKED,gate=GATE,included=p['price']['included'],deposit_note=p['price']['deposit'],scope=TRIP,**extra))
 offer('steamed-nz-siblings-jan14-2027','CP1265',dict(matvey=66,oscar=66),[['2027-01-14','2027-01-14']])
 for ident,profile,child,adult,a,b in [('totara-family-b-tent-2027','CP1276',330,430,'2027-01-03','2027-01-08'),('totara-easter-tent-2027','CP1277',127,198,'2027-03-26','2027-03-29')]:
  offer(ident,profile,dict(matvey=child,oscar=child),[[a,b]],required=[dict(id='adults',amount=adult*2,label=T('Два взрослых · семейная unpowered tent категория','Dos adultos · categoría familiar unpowered tent'))])
  offers[-1].update(unknown_trip=['travel','misc'],scope=T('Сценарий: двое взрослых и двое детей 4–12, собственная палатка без электричества; проживание / питание родителей уже включены. Это не самостоятельный пансион детей. Снаряжение, дорога и конечные extras отдельно; языковой / религиозный выбор и места не подтверждены.',
   'Escenario: dos adultos y dos niños de 4–12, tienda propia sin electricidad; alojamiento / comida parental ya incluidos. No residencia infantil independiente. Equipo, viaje y extras finales aparte; elección lingüística / religiosa y plazas sin confirmar.'))
 offer('giofai-matvey-launch-2027','CP1291',dict(matvey=595),[['2027-01-04','2027-01-15']]);offers[-1]['format']='online';offers[-1]['unknown_trip']=[];offers[-1]['scope']=T('Только Матвей, launch price AUD 595, без повторного добавления reservation 99. Оскар младше 8. Онлайн доступ из Коста-Рики, язык преподавания, подходящее устройство и места ещё уточнить.',
  'Solo Matvey, launch price AUD 595, sin sumar reservation 99 otra vez. Oscar menor de 8. Confirmar acceso en línea desde Costa Rica, idioma docente, dispositivo compatible y plazas.')
 ids={o['id'] for o in offers};d['camp_planning']['offers']=[o for o in d['camp_planning']['offers'] if o['id'] not in ids]+offers;d['camp_planning'].update(version=163,checked=CHECKED)
