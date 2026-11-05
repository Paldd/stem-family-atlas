"""Industrial/AI exhibition coverage with country-specific gates and unresolved windows."""
from copy import deepcopy
CHECKED='2026-11-05'
SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
CHTF='https://www.chtf.com/'
CHTF_NOTICE=CHTF+'canguanzhiyin/gonggao/'
CHTF_CN=CHTF+'canguanzhiyin/ruchangxuzhiX/'
CHTF_EN=CHTF+'english/Info/ForVisitors/Admission/'
ITES='https://global.iteschina.com/'
ITES_FAQ=ITES+'en/page/faq'
ITES_REG=ITES+'en/audience/registration?uniqueId=202598836'
INFOSEC='https://www.infosecurityeurope.com/en-gb/help.html'
SH='https://www.automatica-sh.com.cn/en/'
SH_PARENT='https://automatica-munich.com/en/automatica-shanghai/'
LATAM='https://www.gitexlatam.com/'
ITALY='https://www.gitexitaly.com/'
BELGRADE='https://www.gitexbelgrade.com/'
INDIA='https://www.gitex-india.com/'
KAZ='https://www.gitexcac.com/'
VIET='https://gitexvietnam.com/'
KEN='https://www.aieverythingkenya.com/'
EGYPT='https://www.aieverythingegypt.com/'
AFRICA='https://gitexafrica.com/'
EUROPE='https://www.gitexeurope.com/'
HM='https://www.hannovermesse.de/'
AUTO='https://automatica-munich.com/'
CONDITIONAL=T('Условно: детский допуск и билет уточнить','Condicional: confirmar admisión infantil y billete')
VISIT=T('Посещение компаний и технологий; демонстрация, сертификат или startup pitch не детская конкурсная награда.',
 'Visita de empresas y tecnologías; demostración, certificado o startup pitch no es premio competitivo infantil.')
NO_ACTION=T('Идея посещения, не принятая регистрация. Формы, сообщения, согласия, покупки и оплаты не выполнялись.',
 'Idea de visita, no registro aceptado. Sin formularios enviados, mensajes, consentimientos, compras ni pagos.')
LANG=T('Язык стенда, детской экскурсии и поддержки EN / ES уточнить отдельно. Английский сайт не подтверждает сопровождение семьи на английском.',
 'Confirmar idioma del stand, visita infantil y apoyo EN / ES por separado. Web inglesa no acredita acompañamiento familiar en inglés.')
UNKNOWN=T('Прямое правило входа детей 6 и 9 лет в выбранные залы не установлено; сопровождение взрослого само по себе не подтверждает допуск.',
 'Sin establecer regla directa para entrada de niños de 6 y 9 años en salas elegidas; acompañamiento adulto por sí solo no acredita admisión.')
PRICE=T('Текущий посетительский тариф, налоги, детские условия и окончательный пакет ещё уточнить. Неизвестная цена не считается нулём.',
 'Confirmar tarifa actual, impuestos, condiciones infantiles y paquete final. Precio desconocido no equivale a cero.')
DIRECTORY=T('Состав компаний выбранного выпуска и доступ к их демонстрациям подтвердить по актуальному каталогу. Логотипы прошлых лет и обещанный масштаб не доказательство участия всех компаний в новом сезоне.',
 'Confirmar empresas de edición elegida y acceso a demostraciones en catálogo vigente. Logotipos pasados y escala prevista no prueban participación de todas empresas en nueva temporada.')
LAUNCH=T('Новый региональный выпуск международной технологической сети; ожидаемый масштаб и выступавшие в других странах не являются результатами уже состоявшегося местного события.',
 'Nueva edición regional de red tecnológica internacional; escala prevista y ponentes de otros países no son resultados de un evento local ya celebrado.')
def ref(label,url):return dict(label=label,url=url)
def event(i,name,iso,city,start,end,url,themes,highlights,**fields):
 countries={'CHN':('Китай','Азия'),'GBR':('Великобритания','Европа'),'BRA':('Бразилия','Южная Америка'),'ITA':('Италия','Европа'),'SRB':('Сербия','Европа'),'IND':('Индия','Азия'),'KAZ':('Казахстан','Азия'),'VNM':('Вьетнам','Азия'),'KEN':('Кения','Африка'),'EGY':('Египет','Африка')}
 countries['KOR']=('Южная Корея','Азия')
 country,region=countries[iso]
 e=dict(id='E'+str(i),block='События',title=name,country=country,region=region,city=city,start=start,end=end,period='',date_status='Подтверждено' if start else 'Уточнить',deadline='',age=UNKNOWN,mat=CONDITIONAL,osc=CONDITIONAL,
  format=T('Посетитель выставки','Visitante de exposición'),entry=T('Деловой посетитель: проверить регистрацию, документы и категорию билета; детский доступ отдельно.',
  'Visitante profesional: verificar registro, documentos y categoría de billete; acceso infantil aparte.'),gear=T('Не нужен для посещения; demo и workshop могут иметь свои условия.','No necesario para visitar; demo y workshop pueden tener condiciones propias.'),language=LANG,languages=[],language_certainty=LANG,cost=PRICE,level=T('Выставка компаний и технологий','Exposición de empresas y tecnologías'),reward=VISIT,priority=T('P3 — поездка после проверки допуска','P3 — viaje tras verificar admisión'),action=UNKNOWN+' '+NO_ACTION,source=url,references=[ref(name,url)],proof=T('Прочитаны собственные страницы организатора и доступные visitor rules; неполные и конфликтующие условия сохранены.',
  'Leídas páginas propias del organizador y visitor rules disponibles; conservadas condiciones incompletas y contradictorias.'),checked=CHECKED,status='Идея',note=NO_ACTION,themes=themes,scope='international',participation='visitor',admission_kind='visitor',evidence_level='event_page',registration_status=NO_ACTION,exhibition_tier='regional_major',visitor_policy='confirm_children',visitor_policy_note=UNKNOWN,highlights=highlights,exhibitor_note=DIRECTORY,exhibitor_directory_url=url,importance_reason=LAUNCH,adult_entry=T('Проверить деловой профиль, действующий visitor pass и доступ в нужные залы.','Verificar perfil profesional, visitor pass vigente y acceso a salas elegidas.'),iso=[iso],date_scope='exhibition_window',event_group=name)
 e.update(language_mode='unconfirmed',exhibitor_directory_url='');e.update(fields);return e
def policy(e,minimum,note):
 e.update(visitor_policy='adults_only',visitor_policy_note=note,age=note,visitor_age_min=minimum,mat=T('Нет: дети младше опубликованного ограничения.','No: niños menores del límite publicado.'),osc=T('Нет: дети младше опубликованного ограничения.','No: niños menores del límite publicado.'),priority=T('P4 — взрослый маршрут','P4 — ruta adulta'),action=T('В семейный план с детьми не включать; взрослый visitor route отдельно.','Sin incluir en plan familiar con niños; ruta de visitante adulto aparte.')+' '+NO_ACTION)
 return e

def make_events():
 out=[]
 conflict=T('Китайское ticket notice разрешает младше 16 с опекуном и подписанным на месте соглашением. Другая китайская entry page запрещает младше 16; английская требует возраст above 16. Все страницы собственной CHTF. До подтверждения актуального правила, иностранных паспортов и соглашения детское посещение не считать разрешённым.',
  'Ticket notice chino permite menores de 16 con tutor y acuerdo firmado presencialmente. Otra entry page china prohíbe menores de 16; inglesa exige edad above 16. Todas páginas propias CHTF. Sin confirmar regla vigente, pasaportes extranjeros y acuerdo no considerar permitida visita infantil.')
 e=event(220,'China Hi-Tech Fair · CHTF 2026','CHN','Shenzhen World · Bao’an · No.1 Zhancheng Rd','2026-11-26','2026-11-28',CHTF+'english/',['robotics','ai','technology'],[T('ИИ и робототехника','IA y robótica'),T('Электроника и high-tech разработки','Electrónica y desarrollos high-tech'),T('Межотраслевая промышленная экспозиция','Exposición industrial multisectorial')],exhibition_tier='global',age=conflict,visitor_policy_note=conflict,
  deadline='2026-11-28',deadline_utc='2026-11-28T07:00:00Z',deadline_label=T('Окончание продаж / регистрации посетителей','Fin de venta / registro de visitantes'),
  deadline_note=T('28 ноября 15:00 China / 07:00 UTC — прекращение ticket registration. Бесплатная предрегистрация до 25 ноября 12:00 — ценовое условие, не окончание регистрации; отдельный дедлайн для него не создан. Вход заканчивается 16:00, залы закрываются 17:00.',
   '28 de noviembre 15:00 China / 07:00 UTC: fin de ticket registration. Prerregistro gratis antes de 25 de noviembre 12:00 es condición de precio, no cierre de registro; sin plazo de inscripción separado. Última entrada 16:00, cierre de salas 17:00.'),
  cost=T('Взрослый предварительный вход бесплатно до 25 ноября 2026, 12:00 China; позднее RMB 120. Китайское особое правило обещает детям до 16 бесплатно без предрегистрации с опекуном и соглашением, но противоречит другим admission pages. Личное принятие соглашения и действующий билет не подтверждены.',
   'Entrada adulta previa gratis antes de 25 de noviembre de 2026, 12:00 China; después RMB 120. Regla especial china promete gratis a menores de 16 sin prerregistro con tutor y acuerdo, pero contradice otras admission pages. Sin aceptación personal de acuerdo ni billete vigente confirmados.'),
  adult_entry=T('Профессиональная регистрация; паспорт / ID, QR или badge. Для иностранных документов китайская страница направляет в visitor service desk. 26–28 ноября 09:00–17:00, последний вход 16:00.',
   'Registro profesional; pasaporte / ID, QR o badge. Página china dirige documentos extranjeros al visitor service desk. 26–28 de noviembre 09:00–17:00, última entrada 16:00.'),
  importance_reason=T('Крупная международная межотраслевая high-tech ярмарка в Шэньчжэне. Это обзор разных отраслей, не обещание присутствия всех мировых роботокомпаний.',
   'Gran feria internacional multisectorial high-tech en Shenzhen. Panorama de sectores distintos, sin prometer presencia de todas empresas robóticas mundiales.'),references=[ref('Own Chinese ticket notice / fee and guardian exception',CHTF_NOTICE),ref('Own Chinese entry page / under-16 prohibition',CHTF_CN),ref('Own English entry rules / above-16 wording',CHTF_EN)])
 e['note']=conflict+' '+NO_ACTION
 out.append(e)
 note=T('Обе собственные регистрации ITES — EN и CN — запрещают посетителей младше 18; только профессиональный вход. Оба ребёнка не допускаются.',
  'Ambos registros propios ITES, EN y CN, prohíben visitantes menores de 18; acceso solo profesional. Ninguno de los niños admitido.')
 e=policy(event(221,'ITES Shenzhen 2027 · robotics / industrial manufacturing','CHN','Shenzhen World · Bao’an · No.1 Zhancheng Rd','2027-03-24','2027-03-27',ITES,['robotics','technology','engineering'],[T('Роботы и автоматизация','Robots y automatización'),T('Промышленное оборудование и точные компоненты','Equipo industrial y componentes de precisión'),T('Machine vision и производственные цепочки','Machine vision y cadenas de producción')],exhibition_tier='global'),18,note)
 e.update(deadline='2027-03-23',deadline_label=T('Закрытие онлайн-предрегистрации','Cierre de prerregistro en línea'),deadline_note=T('FAQ указывает 23 марта 2027 без часа; это онлайн-предрегистрация, не доказательство запрета последующего onsite оформления. Час и UTC не придуманы.',
  'FAQ indica 23 de marzo de 2027 sin hora; es prerregistro en línea, no prueba de prohibir registro onsite posterior. Sin inventar hora ni UTC.'),cost=T('CN registration обещает отсутствие entrance fee и metro voucher; применимость к иностранному потоку подтвердить, дополнительные программы отдельно. Полный visitor package не рассчитан.',
  'Registro CN anuncia sin entrance fee y metro voucher; confirmar aplicación al flujo extranjero, programas extra aparte. Sin calcular visitor package completo.'),adult_entry=T('Иностранцы направляются в EN регистрацию. FAQ: confirmation, паспорт / ID и две business cards; среда–пятница 09:00–17:00, суббота 09:00–15:00. Footer Contact упрощает часы до 17:00 для всех дней: ориентир — подробная FAQ-таблица, финальные часы уточнить.',
  'Extranjeros dirigidos a registro EN. FAQ: confirmation, pasaporte / ID y dos business cards; miércoles–viernes 09:00–17:00, sábado 09:00–15:00. Footer Contact simplifica hasta 17:00 todos días: referencia es tabla FAQ detallada; confirmar horario final.'),references=[ref('2027 dates and industrial sectors',ITES),ref('FAQ · pre-registration and actual hours',ITES_FAQ),ref('English professional registration / under 18',ITES_REG),ref('Chinese registration / under 18','https://www.iteschina.com/zh-cn/audience/register/1')])
 e['importance_reason']=T('Крупная отраслевая производственная площадка Южного Китая. Robotics / automation являются разделами ITES, а масштаб всей ярмарки не равен числу роботокомпаний.',
  'Gran plataforma industrial sectorial del sur de China. Robotics / automation son secciones ITES; escala de feria completa no equivale a número de empresas robóticas.')
 out.append(e)
 e=policy(event(222,'Infosecurity Europe 2027','GBR','ExCeL London · One Western Gateway','2027-06-08','2027-06-10',INFOSEC,['technology'],[T('Кибербезопасность и цифровая инфраструктура','Ciberseguridad e infraestructura digital'),T('Профессиональные демонстрации','Demostraciones profesionales'),T('Конференции и отраслевое обучение','Conferencias y formación sectorial')],exhibition_tier='global'),16,T('FAQ прямо запрещает детей младше 16. Student Pass предназначен студентам / выпускникам, ищущим работу, а не детям 6 и 9; требуется подтверждение.',
  'FAQ prohíbe expresamente menores de 16. Student Pass dirigido a estudiantes / graduados que buscan empleo, no niños de 6 y 9; exige confirmación.'))
 e['adult_entry']=T('Проверить свою категорию Visitor / Student / Conference Pass. Вторник и среда 09:30–17:30, четверг 09:30–16:00; профессиональное событие по cybersecurity, не выставка всех производителей роботов.',
  'Verificar categoría propia Visitor / Student / Conference Pass. Martes y miércoles 09:30–17:30, jueves 09:30–16:00; evento profesional de cybersecurity, no exposición de todos fabricantes de robots.')
 e['importance_reason']=T('Крупная профильная cybersecurity выставка в Лондоне для взрослого профессионального маршрута; технологии безопасности выделены отдельной темой.',
  'Gran exposición especializada de cybersecurity en Londres para ruta profesional adulta; tecnologías de seguridad identificadas como tema propio.')
 out.append(e)
 out.append(event(223,'automatica Shanghai 2027','CHN','Shanghai New International Expo Centre · No.2345 Longyang Rd, Pudong','2027-03-08','2027-03-10',SH,['robotics','ai','technology'],[T('Промышленные, мобильные и сервисные роботы','Robots industriales, móviles y de servicio'),T('Machine vision, сенсоры и автоматизация','Machine vision, sensores y automatización'),T('AI-driven производственные решения','Soluciones industriales AI-driven')],note=T('Первый международный выпуск automatica, организованный Messe Muenchen Shanghai с профильными ассоциациями. Проходит параллельно LASER World of Photonics China, но это разные тематические выставки. Понедельник / вторник 09:00–17:00, среда до 16:00. Правила детей Munich не перенесены на Shanghai.',
  'Primera edición internacional automatica, organizada por Messe Muenchen Shanghai con asociaciones sectoriales. Paralela a LASER World of Photonics China, pero exposiciones temáticas distintas. Lunes / martes 09:00–17:00, miércoles hasta 16:00. Sin trasladar reglas infantiles Munich a Shanghai.'),references=[ref('Shanghai own programme / date / venue / hours',SH),ref('Shanghai own visitor scope',SH+'why-visit'),ref('Parent brand announcement / same dates',SH_PARENT)]))
 definitions=[
 (224,'GITEX AI LATAM 2027','BRA','São Paulo · Anhembi Convention Center','2027-03-16','2027-03-17',LATAM,18,LATAM+'terms-and-conditions'),
 (225,'GITEX AI Mediterranean / Italy 2027','ITA','Rome · Roma Convention Center La Nuvola','2027-04-21','2027-04-22',ITALY,18,ITALY+'terms-and-conditions'),
 (226,'GITEX AI Belgrade 2027','SRB','Belgrade Fair · Serbia','2027-05-25','2027-05-27',BELGRADE+'home',18,BELGRADE+'terms-and-conditions'),
 (227,'GITEX AI India 2027','IND','BIEC · Bengaluru','2027-06-02','2027-06-04',INDIA,18,INDIA+'faqs'),
 (228,'GITEX AI Kazakhstan 2027','KAZ','Almaty · '+T('площадку 2027 подтвердить','confirmar sede 2027'),'2027-06-07','2027-06-08',KAZ,None,'https://event.gitexcac.com/pre-registration')]
 for i,name,iso,city,start,end,url,minimum,rules in definitions:
  e=event(i,name,iso,city,start,end,url,['ai','technology','entrepreneurship'],[T('ИИ и цифровые технологии','IA y tecnologías digitales'),T('Enterprise / startups / инвестиционные экосистемы','Enterprise / startups / ecosistemas de inversión'),T('Отраслевые экспозиции и деловая программа','Exposiciones sectoriales y programa profesional')],references=[ref('Own edition dates and venue',url),ref('Own admission / registration conditions',rules)])
  if minimum:policy(e,minimum,T('Собственные условия этой страны: только trade / business professionals, вход с 18 лет. Детям 6 и 9 нельзя; Student Pass не отменяет возрастной запрет.',
   'Condiciones propias de este país: solo trade / business professionals, entrada desde 18. Niños de 6 y 9 no admitidos; Student Pass no elimina límite de edad.'))
  else:
   e['visitor_policy_note']=e['age']=T('Форма 2027 требует заявителя 18+, но это возраст автора запроса интереса, не подтверждённое правило входа сопровождаемых детей. Отдельный детский visitor gate не найден; допуск пока неизвестен.',
    'Formulario 2027 exige solicitante 18+, edad del autor de consulta de interés, no regla confirmada de entrada de niños acompañados. Sin localizar visitor gate infantil separado; admisión aún desconocida.')
   e['note']=T('Текущий body и форма согласуют 7–8 июня 2027 в Almaty. Footer terms остаётся с понедельником 4 мая / вторником 5 мая из прежнего выпуска; эти часы не перенесены на июнь 2027.',
    'Body actual y formulario coinciden en 7–8 de junio de 2027 en Almaty. Footer terms conserva lunes 4 de mayo / martes 5 de mayo de edición anterior; sin trasladar esas horas a junio de 2027.')
  if i==227:e['note']=T('Hero и FAQ: 2–4 июня 2027, BIEC Bengaluru. Meta title ещё говорит April 2027; июньская дата относится к India, а не к Berlin. Supernova — отбор бизнес-стартапов, не юниорская роботолига.',
   'Hero y FAQ: 2–4 de junio de 2027, BIEC Bengaluru. Meta title aún dice April 2027; fecha de junio corresponde a India, no Berlin. Supernova selecciona startups comerciales, no liga robótica junior.')
  out.append(e)
 e=policy(event(229,'GITEX AI Vietnam · '+T('даты выпуска требуют сверки','fechas de edición por contrastar'),'VNM','Hanoi · '+T('точную площадку уточнить','confirmar sede exacta'),'','',VIET,['ai','technology','entrepreneurship'],[T('ИИ и digital-индустрия','IA e industria digital'),T('Startup / enterprise-программы','Programas startup / enterprise')],date_status='Уточнить',reported_start='2026-11-26',reported_end='2026-11-27'),None,T('Terms говорит trade / business only и over 18; форма запроса интереса дополнительно требует декларацию автора 21+. Это два разных ограничения, не подтверждение семейного доступа.',
  'Terms indica trade / business only y over 18; formulario de interés exige además declaración del autor 21+. Son dos condiciones distintas, no acceso familiar confirmado.'))
 e['period']=T('Homepage news и title terms указывают 26–27 ноября 2026, footer terms — 1–2 октября 2026. Согласованной новой программы / расписания не найдено; даты сохранены как reported, без операционного календаря.',
  'News de homepage y title terms indican 26–27 de noviembre de 2026, footer terms 1–2 de octubre de 2026. Sin programa / horario nuevo coherente; fechas conservadas como reported, sin calendario operativo.')
 e['references']=[ref('Own current homepage date claim',VIET),ref('Own terms title / conflicting footer / adult gate',VIET+'terms-and-conditions'),ref('Interest request / author 21+','https://event.gitexvietnam.com/pre-register-enquiry')];out.append(e)
 e=policy(event(230,'AI Everything Kenya × GITEX Kenya · '+T('следующий выпуск / расписание уточнить','próxima edición / confirmar horario'),'KEN','Nairobi · '+T('площадки 2027 не подтверждены','sedes 2027 sin confirmar'),'','',KEN+'register',['ai','technology','entrepreneurship'],[T('AI exhibition / summit','Exposición / cumbre AI'),T('Startup-экосистема','Ecosistema startup')],reported_start='2027-05-12',reported_end='2027-05-14'),None,T('Доступные собственные Kenya terms и footer регистрационной страницы говорят strictly over 21 only. Границу 21 года уточнить; детям 6 и 9 нельзя.',
  'Kenya terms propios y footer de registro disponibles dicen strictly over 21 only. Confirmar límite de 21 años; niños de 6 y 9 no admitidos.'))
 e['period']=T('Title регистрационной страницы: общий диапазон 12–14 мая 2027; footer говорит May 2027. Body FAQ ещё разделяет Summit 19 мая 2026 / Sarit и Expo 20–21 мая 2026 / KICC. Конкретные дни и площадки экспозиции 2027 не объявлены; root URL сейчас перенаправляет на Morocco. Перенаправление не объявлено отменой.',
  'Title de registro: rango general 12–14 de mayo de 2027; footer dice May 2027. Body FAQ aún separa Summit 19 de mayo de 2026 / Sarit y Expo 20–21 de mayo de 2026 / KICC. Sin días y sedes concretos de exposición 2027; root URL redirige ahora a Morocco. Redirección no declarada cancelación.')
 e['references']=[ref('Own retained register page / mixed season evidence',KEN+'register'),ref('Own Kenya age policy',KEN+'terms-and-conditions'),ref('Root redirect observation',KEN)];out.append(e)
 e=event(231,'Ai Everything MEA Egypt 2027','EGY','Cairo · '+T('площадку нового выпуска уточнить','confirmar sede de nueva edición'),'','',EGYPT,['ai','robotics','technology'],[T('Physical AI и промышленная робототехника','Physical AI y robótica industrial'),T('AI infrastructure и deep tech','Infraestructura AI y deep tech')])
 e['period']=T('Собственные страницы объявляют Cairo, июнь 2027 и переход на три дня / два зала. Точные дни не опубликованы в прочитанной программе; 1–2 июня из сводных анонсов не приняты как подтверждённая трёхдневная экспозиция.',
  'Páginas propias anuncian Cairo, junio de 2027 y cambio a tres días / dos salas. Sin días exactos publicados en programa leído; 1–2 de junio de anuncios generales no adoptados como exposición de tres días confirmada.')
 e['references']=[ref('Own 2027 / June edition',EGYPT),ref('Own three-day format and physical AI / robotics',EGYPT+'why-exhibit'),ref('Terms page without a located child gate',EGYPT+'terms-and-conditions')];out.append(e)
 assert len(out)==12
 return out

def enrich_v162(d):
 index={e['id']:e for e in d['events']}
 hm=index['E014'];hm.update(checked=CHECKED,cost=T('Публичный прайс 2027: взрослый advance day EUR 35 / onsite 57; full-event advance 93 / onsite 111; reduced day 24 с доказательством права. Применимость reduced к детям отдельно, семейная сумма не рассчитана. Все цены с VAT; общественный транспорт не включён.',
  'Tarifa pública 2027: adulto advance day EUR 35 / onsite 57; full-event advance 93 / onsite 111; reduced day 24 con prueba de elegibilidad. Aplicación de reduced a niños aparte, sin calcular total familiar. Precios con VAT; transporte público no incluido.'),visitor_policy_note=T('Младше 15 только с ответственным взрослым. DE прямо: бесплатно до 5 включительно, с 6 нужен билет. EN одновременно пишет up to 6 и from 6: для Оскара бесплатный вход не обещан, индивидуальный детский тариф уточнить.',
  'Menores de 15 solo con adulto responsable. DE explícito: gratis hasta 5 inclusive, desde 6 exige billete. EN dice a la vez up to 6 y from 6: sin prometer entrada gratuita a Oscar; confirmar tarifa infantil individual.'),period=T('5–8 апреля 2027, ежедневно 09:00–18:00. EN ticket page ожидает открытие early November, DE late November; действующий checkout и билет не проверялись.',
  '5–8 de abril de 2027, diariamente 09:00–18:00. Ticket page EN espera apertura early November, DE late November; checkout vigente y billete sin verificar.'))
 hm['references']=hm.get('references',[])+[ref('German child boundary and current price',HM+'de/fuer-besucher/tickets/index-2'),ref('English prices / inconsistent six-year wording',HM+'en/for-visitors/tickets/index-2'),ref('Exact four-day hours',HM+'en/for-visitors/opening-hours/')]
 hm['age']=hm['visitor_policy_note']
 hm['proof']=T('Собственные opening-hours и ticket pages прямо подтверждают 5–8 апреля 2027, тарифы и сопровождение младше 15; расхождения EN / DE о шести годах и начале продаж сохранены.',
  'Opening-hours y ticket pages propias confirman expresamente 5–8 de abril de 2027, tarifas y acompañamiento de menores de 15; conservadas diferencias EN / DE sobre seis años y apertura de ventas.')
 hm['entry']=hm['adult_entry']=T('Каждому нужен действующий билет по своей возрастной категории; дети младше 15 со взрослым. DE требует билет с 6 лет. Тариф ребёнка и реальное открытие ticket shop подтвердить перед покупкой.',
  'Cada persona exige billete vigente de su categoría de edad; menores de 15 con adulto. DE exige billete desde 6 años. Confirmar tarifa infantil y apertura real del ticket shop antes de comprar.')
 auto=index['E019'];auto.update(checked=CHECKED,source=AUTO+'en/trade-fair/plan-your-visit/opening-hours/',period=T('22–25 июня 2027, Messe München East Entrance: вторник–четверг 09:00–17:00, пятница до 16:00. FAQ требует индивидуальный ticket и photo ID; правило детей не найдено.',
  '22–25 de junio de 2027, Messe München East Entrance: martes–jueves 09:00–17:00, viernes hasta 16:00. FAQ exige ticket individual y photo ID; sin localizar regla infantil.'),cost=T('Тарифы 2027 ещё не опубликованы; DE ticket page говорит начало 2027, EN содержит опечатку 20257. Optional PLUS TICKET EUR 5 не базовая стоимость билета.',
  'Tarifas 2027 aún sin publicar; ticket page DE dice inicio de 2027, EN contiene errata 20257. Optional PLUS TICKET EUR 5 no es precio base de billete.'))
 auto['references']=auto.get('references',[])+[ref('Actual visitor hours',auto['source']),ref('Ticket page / no base tariff yet',AUTO+'en/trade-fair/tickets/'),ref('German ticket opening year',AUTO+'de/messe/tickets/'),ref('Own FAQ / individual pass and photo ID',AUTO+'en/trade-fair/plan-your-visit/contact-faq/')]
 auto['proof']=T('Собственная таблица opening hours подтверждает 22–25 июня 2027 и разные часы последнего дня. FAQ и EN / DE tickets прочитаны; отдельное правило детей не найдено.',
  'Tabla propia opening hours confirma 22–25 de junio de 2027 y horario distinto de último día. Leídos FAQ y tickets EN / DE; sin localizar regla infantil separada.')
 auto['note']=T('Профессиональная робототехническая выставка. Индивидуальный ticket и photo ID обязательны по FAQ; детский доступ и подходящая категория билета неизвестны. PLUS TICKET — добровольная надбавка, а не полная цена.',
  'Exposición profesional de robótica. FAQ exige ticket individual y photo ID; acceso infantil y categoría adecuada desconocidos. PLUS TICKET es suplemento voluntario, no precio completo.')
 europe=index['E081'];europe.update(checked=CHECKED,note=T('Homepage / FAQ описывают Berlin 30 июня–1 июля 2026. Блок 2–4 июня 2027 ссылается на India / Bengaluru; это не дата Berlin. Форма интереса 2027 не датированная программа. Подтверждённого следующего Berlin slot и заявления об отмене в прочитанной первичной выдаче нет.',
  'Homepage / FAQ describen Berlin 30 de junio–1 de julio de 2026. Bloque 2–4 de junio de 2027 enlaza India / Bengaluru; no fecha de Berlin. Formulario de interés 2027 no es programa fechado. Sin próximo slot Berlin confirmado ni declaración de cancelación en fuentes primarias leídas.'))
 europe['references']=europe.get('references',[])+[ref('Own cross-country carousel',EUROPE),ref('Own still-2026 FAQ',EUROPE+'faqs'),ref('2027 enquiry without event date','https://event.gitexeurope.com/pre-register-enquiry')]
 africa=index['E082'];africa.update(title='GITEX Africa 2027',start='2027-04-26',end='2027-04-28',date_status='Подтверждено',checked=CHECKED,city=T('Marrakech · площадку 2027 уточнить','Marrakech · confirmar sede 2027'),source=AFRICA,period=T('Homepage и отдельная Startup page объявляют 26–28 апреля 2027. FAQ ещё содержит 7–9 апреля 2026 и 14–16 апреля 2025; старые часы / площадки / тарифы не перенесены на 2027.',
  'Homepage y Startup page separada anuncian 26–28 de abril de 2027. FAQ aún contiene 7–9 de abril de 2026 y 14–16 de abril de 2025; sin trasladar horarios / sedes / tarifas antiguos a 2027.'),cost=PRICE)
 africa['references']=africa.get('references',[])+[ref('2027 date / title and new edition',AFRICA),ref('Independent own programme page with same dates',AFRICA+'startup'),ref('Age rule / school 16–17 exception; older-season FAQ',AFRICA+'faqs')]
 africa['proof']=T('Собственные homepage и Startup page прямо подтверждают 26–28 апреля 2027, Marrakech. Возрастной FAQ отдельно: 18+ либо 16–17 с учебным заведением; детям семьи это не подходит.',
  'Homepage y Startup page propias confirman expresamente 26–28 de abril de 2027, Marrakech. FAQ de edad aparte: 18+ o 16–17 con institución educativa; no corresponde a niños de familia.')
 africa['note']=T('Даты 2027 найдены и сохранены из собственных новых страниц. FAQ продолжает описывать другие сезоны; финальная площадка, тариф и новая редакция visitor conditions требуют подтверждения.',
  'Fechas 2027 localizadas y conservadas de páginas propias nuevas. FAQ sigue describiendo otras temporadas; confirmar sede final, tarifa y nueva edición de visitor conditions.')
 india=index['E107'];policy(india,18,T('Собственная visitor page запрещает вход младше 18. Student entry только 5 июня 2027 не объявлен исключением из возрастного запрета; оба ребёнка не допускаются.',
  'Visitor page propia prohíbe entrada a menores de 18. Student entry solo 5 de junio de 2027 no se declara excepción de edad; ninguno de los niños admitido.'))
 india.update(checked=CHECKED,source='https://www.automationindiaexpo.com/visit',city='Bombay Exhibition Centre · Goregaon, Mumbai · Halls 2, 3, 4 & 6',cost=T('Объявлена бесплатная регистрация профессионального посетителя. Билет не получен; отдельные conference / workshop и дорожные расходы уточнить.',
  'Anunciado registro gratuito de visitante profesional. Sin billete recibido; confirmar conference / workshop y gastos de viaje aparte.'))
 india['references']=india.get('references',[])+[ref('Own 2027 date / 18 minimum / student day',india['source'])]
 india['entry']=india['adult_entry']=T('Бесплатная visitor registration для взрослого профессионала. Вход младше 18 запрещён; student day 5 июня не исключение для школьников 6 и 9. Билет и подтверждение не получены.',
  'Visitor registration gratuita para profesional adulto. Prohibida entrada de menores de 18; student day 5 de junio no es excepción para escolares de 6 y 9. Sin billete ni confirmación recibidos.')
 india['proof']=T('Собственная visitor page прямо подтверждает 2–5 июня 2027, залы BEC Mumbai, запрет младше 18 и отдельный student day 5 июня.',
  'Visitor page propia confirma expresamente 2–5 de junio de 2027, salas BEC Mumbai, prohibición de menores de 18 y student day separado 5 de junio.')
 rows=make_events();ids=set(index);replacements={e['id']:e for e in rows};d['events']=[replacements.get(e['id'],e) for e in d['events']]+[e for e in rows if e['id'] not in ids]
 for e in rows+[hm,auto,europe,africa,india]:
  e['references']=list({r['url']:r for r in e.get('references',[])}.values())
 known={s['url'] for s in d['sources']}
 for e in rows+[hm,auto,europe,africa,india]:
  for r in [ref(e['title'],e['source'])]+e.get('references',[]):
   if r['url'] not in known:d['sources'].append(dict(url=r['url'],title=r['label'],checked=CHECKED,evidence=T('Собственная выставочная страница; возраст, редакция, город и неоднозначные сроки проверяются раздельно.',
    'Página propia de exposición; edad, edición, ciudad y plazos ambiguos verificados por separado.')));known.add(r['url'])
