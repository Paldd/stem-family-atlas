"""Primary-source holiday options; language and attendance gaps stay explicit."""
from datetime import date, timedelta
from copy import deepcopy

CHECKED='2026-11-04'
SPANISH={}
def T(ru,es):
    SPANISH[ru]=es
    return ru

QUIMPI='https://www.quimpi.com/campamentos/'
SUMMER=QUIMPI+'verano/'
GANDARA='https://gandaraschool.com/es/campamento-navidad'
GTERMS='https://gandaraschool.com/es/condiciones-de-contratacion'
CYBROID='https://cybroid.com/events/tech-fun-camp-2026'
NH='https://form.jotform.com/252805351014851'
NHABOUT='https://complejonewhope.co.cr/quienes-somos/'
UNKNOWN_LANGUAGE=T('Язык конкретных занятий EN/ES/RU прямо не установлен. Язык сайта, плаката или школьной программы не доказывает язык этой смены.',
                   'Idioma EN/ES/RU de actividades concretas sin acreditar expresamente. Idioma de web, cartel o programa escolar no acredita idioma de esta sesión.')
QUESTIONS=[T('Подтвердить возраст на начало смены, язык ведущего и помощь ребёнку, свободное место и индивидуальный приём иностранной семьи.',
             'Confirmar edad al inicio, idioma del monitor y apoyo infantil, plaza y admisión individual de familia extranjera.'),
           T('Получить окончательную стоимость, включения, технику, питание, транспорт, страхование и письменные правила отмены выбранной смены.',
             'Obtener precio final, inclusiones, equipo, comida, transporte, seguros y cancelación escrita de sesión elegida.')]
NO_BOARD=T('Дневная программа без ночёвки. Жильё и сопровождение семьи отдельно.',
           'Programa diurno sin pernoctación. Alojamiento y acompañamiento familiar aparte.')
PLACE_Q=T('Тенерифе · Las Lagunetas · TF-24, km 16,3; офис La Esperanza не является местом лагеря.',
          'Tenerife · Las Lagunetas · TF-24, km 16,3; oficina de La Esperanza no es sede del campamento.')
NO_RANK=T('Редакционный кандидат по опубликованной программе и прозрачности условий; независимый мировой рейтинг качества не установлен.',
          'Candidato editorial por programa publicado y transparencia; sin acreditar clasificación mundial independiente de calidad.')

def fit(lo,hi,start,unknown=False):
    result={}
    for child,year in [('matvey',2017),('oscar',2020)]:
        minimum=date.fromisoformat(start).year-year-1;maximum=minimum+1
        status='conditional' if unknown else 'later' if lo is not None and maximum<lo else 'not_eligible' if hi is not None and minimum>hi else 'candidate' if (lo is None or minimum>=lo) and (hi is None or maximum<=hi) else 'conditional'
        detail=T(f'В год начала возраст {minimum}–{maximum}; точный день рождения и класс неизвестны. Возрастное соответствие не подтверждает язык, свободное место или зачисление.',
                 f'Edad en año de inicio {minimum}–{maximum}; cumpleaños exacto y curso desconocidos. Correspondencia de edad no confirma idioma, plaza ni aceptación.')
        if unknown:detail+=' '+T('Возраст выбранного набора не опубликован; предел другой программы не переносить.',
                                 'Edad de convocatoria elegida sin publicar; no trasladar límite de otro programa.')
        result[child]=dict(status=status,detail=detail)
    return result

def source(url,title):return dict(title=title,url=url,checked=CHECKED)
def profile(ident,slug,provider,country,iso,place,themes,formats,age,programme,price,accommodation,urls,lo=None,hi=None,start='2026-12-01',unknown=False):
    return dict(id=f'CP{ident}',slug=slug,provider=provider,country=country,iso=iso,place=place,themes=themes,formats=formats,
        age=age,language=UNKNOWN_LANGUAGE,confirmed_instruction_languages=[],programme=programme,
        timing=dict(status='published_2026_27',label='',sessions=[],session_details=[]),price=price,accommodation=accommodation,
        family_fit=fit(lo,hi,start,unknown),editorial_reason=NO_RANK,shortlist=[],questions=deepcopy(QUESTIONS),
        sources=[source(u,title) for u,title in urls],checked=CHECKED)
def add_session(p,start,end,label,url,scope='camp_session',**extra):
    p['timing']['sessions'].append([start,end])
    p['timing']['session_details'].append(dict(start=start,end=end,label=label,source=url,date_scope=scope,price=p['price']['label'],
        family_fit=deepcopy(p['family_fit']),**extra))
def weekdays(start,end):
    a=date.fromisoformat(start);b=date.fromisoformat(end)
    return [(a+timedelta(days=n)).isoformat() for n in range((b-a).days+1) if (a+timedelta(days=n)).weekday()<5]

def quimpi_profiles():
    included=T('На странице декабрьского моста включены проживание, полный пансион, экскурсии и входы, активности, специалисты, мониторы 24 часа и страховки. Это цена программы, не всей поездки семьи.',
               'Página del puente incluye alojamiento, pensión completa, excursiones y entradas, actividades, especialistas, monitores 24 horas y seguros. Precio del programa, no de todo el viaje familiar.')
    extras=T('Перелёты, жильё родителей и трансфер аэропорта не оценены. Условия покрытия страховки, местных трансферов и отмены подтвердить письменно.',
             'Vuelos, alojamiento de padres y traslado aeroportuario sin valorar. Confirmar por escrito cobertura de seguro, traslados locales y cancelación.')
    deposit=T('Форма — запрос; оператор подтверждает место и порядок оплаты по email или WhatsApp. Семья не зарегистрирована.',
              'Formulario es solicitud; operador confirma plaza y pago por email o WhatsApp. Familia sin registrar.')
    p=profile(1150,'quimpi-december-2026','Quimpi · Puente de diciembre','Испания','ESP',PLACE_Q,['general','science','sport'],['boarding'],
        T('6–14 лет','6–14 años'),
        T('4–8 декабря 2026: 5 дней / 4 ночи, прибытие и выезд после обеда без точного часа. Природа, ориентирование, ремёсла, рождественская культурная программа, Forestal Park и введение в астрономию. Это общий лагерь с наукой, не соревнование по робототехнике.',
          '4–8 de diciembre de 2026: 5 días / 4 noches, llegada y salida por la tarde sin hora exacta. Naturaleza, orientación, manualidades, cultura navideña, Forestal Park e iniciación astronómica. Campamento general con ciencia, no competición robótica.'),
        dict(year=2026,currency='EUR',amount=200,unit='stay',label=T('200 EUR за ребёнка / 5 дней и 4 ночи. Двое детей = 400 EUR без скидок и поездки; это расчёт по опубликованной цене.',
             '200 EUR por hijo / 5 días y 4 noches. Dos hijos = 400 EUR sin descuentos ni viaje; cálculo con precio publicado.'),included=included,extras=extras,deposit=deposit),
        T('Пансион 4 ночи; точный тип комнаты и ночной ratio подтвердить.','Residencial de 4 noches; confirmar habitación concreta y ratio nocturna.'),
        [(QUIMPI+'puente-de-diciembre/',T('Декабрьский мост: возраст, цена и включения','Puente de diciembre: edad, precio e inclusiones'))],6,14,'2026-12-04')
    p['timing']['label']=T('4–8 декабря 2026 · прибытие / выезд после обеда','4–8 de diciembre de 2026 · llegada / salida por la tarde')
    add_session(p,'2026-12-04','2026-12-08',p['timing']['label'],QUIMPI+'puente-de-diciembre/')
    out=[p]
    programme=T('22 декабря 2026 – 3 января 2027: 13 дней / 12 ночей; прибытие 12:00 в первый день, выезд после завтрака без точного часа. Teide, Museo de la Ciencia y el Cosmos, Starlight, природа, парки, каяк и праздничная программа. Возраст в этой карточке не указан.',
                '22 de diciembre de 2026 – 3 de enero de 2027: 13 días / 12 noches; llegada 12:00 el primer día, salida después del desayuno sin hora exacta. Teide, Museo de la Ciencia y el Cosmos, Starlight, naturaleza, parques, kayak y programa festivo. Edad sin indicar en esta ficha.')
    p=profile(1151,'quimpi-christmas-2026-27','Quimpi · Navidad 2026/27','Испания','ESP',PLACE_Q,['general','science','sport'],['boarding'],
        T('Возраст именно рождественской смены не опубликован.','Edad de sesión navideña concreta sin publicar.'),programme,
        dict(year=2026,currency='EUR',amount=None,unit='stay',label=T('Цена рождественской смены не опубликована; 200 EUR относится к другой декабрьской программе и сюда не переносится.',
             'Precio de sesión navideña sin publicar; 200 EUR corresponde a otro programa de diciembre y no se traslada aquí.'),
             included=T('Программа с ночёвками и экскурсиями описана; полный состав тарифа нужно запросить.','Descrito programa con pernoctación y excursiones; solicitar composición completa de tarifa.'),extras=extras,deposit=deposit),
        T('12 ночей в лагере; персонал, комната, страховка и ночное сопровождение этой смены уточняются.',
          '12 noches en campamento; confirmar personal, habitación, seguro y acompañamiento nocturno de esta sesión.'),
        [(QUIMPI+'navidad/',T('Полный рождественский план по дням','Plan navideño completo por días'))],start='2026-12-22',unknown=True)
    p['timing']['label']=T('22 декабря 2026 – 3 января 2027 · 13 дней / 12 ночей','22 de diciembre de 2026 – 3 de enero de 2027 · 13 días / 12 noches')
    add_session(p,'2026-12-22','2027-01-03',p['timing']['label'],QUIMPI+'navidad/')
    out.append(p)
    annex=T('Сайт 2027 ссылается на PDF в каталогах 2026 и 2024. Это примеры и список вещей, не доказательство актуальных часов, транспорта, цен или условий 2027. Использованы текущие HTML даты и тарифные атрибуты калькулятора; с PDF часы расходятся.',
            'Web 2027 enlaza PDF en carpetas 2026 y 2024. Son ejemplos y lista de equipo, no prueba de horarios, transporte, precios o condiciones vigentes 2027. Usadas fechas HTML actuales y atributos de tarifas del calculador; horarios discrepan con PDF.')
    for ident,boarding in [(1152,False),(1153,True)]:
        amount=270 if boarding else 150;lo=6 if boarding else 4;pair=486 if boarding else 270
        programme=T('Лето 2027: восемь недель Пн–Пт с 5 июля по 27 августа. Общая природа, спорт, ремёсла и сценическое творчество; вечерние наблюдения звёзд заявлены для пансиона. Астрономия не превращает лагерь в курс ИИ или робототехники.',
                    'Verano 2027: ocho semanas de lunes a viernes desde 5 de julio hasta 27 de agosto. Naturaleza, deporte, manualidades y teatro; observación estelar nocturna declarada en residencial. Astronomía no convierte campamento en curso de IA o robótica.')+' '+annex
        price=dict(year=2027,currency='EUR',amount=amount,unit='week',label=T(f'{amount} EUR за ребёнка / неделю; второй брат со скидкой 20% даёт {pair} EUR за двоих за одну одинаковую неделю, расчёт без поездки. Калькулятор называет цену ориентировочной; окончательный счёт подтверждает оператор.',
             f'{amount} EUR por hijo / semana; descuento del segundo hermano de 20% resulta en {pair} EUR por ambos en una misma semana, cálculo sin viaje. Calculador llama precio orientativo; operador confirma factura final.'),
             included=T('Полный пансион и ночёвки Пн–Пт.' if boarding else 'Завтрак, обед, полдник и активности Пн–Пт.',
                        'Pensión completa y pernoctación de lunes a viernes.' if boarding else 'Desayuno, comida, merienda y actividades de lunes a viernes.'),
             extras=extras,deposit=deposit)
        if boarding:
            age=T('6–13 лет · пансион','6–13 años · residencial');accommodation=T('Пн 10:00 – Пт 16:00, 4 ночи в домиках / убежищах с двухъярусными кроватями внутри огороженного лагеря. Выходные не включены.',
             'Lunes 10:00 – viernes 16:00, 4 noches en casetas / refugios con literas dentro de recinto vallado. Fines de semana excluidos.')
        else:
            age=T('4–13 лет · дневной формат','4–13 años · modalidad diurna');accommodation=T('Пн–Пт 08:00–16:00, без ночёвки. Жильё родителей отдельно.',
             'Lunes a viernes 08:00–16:00, sin pernoctación. Alojamiento parental aparte.')
        p=profile(ident,'quimpi-summer-'+('boarding' if boarding else 'day')+'-2027','Quimpi · Verano 2027 · '+('Día y noche' if boarding else 'De día'),
            'Испания','ESP',PLACE_Q,['general','science','sport'],['boarding' if boarding else 'day'],age,programme,price,accommodation,
            [(SUMMER,T('Текущие даты, варианты и калькулятор 2027','Fechas, modalidades y calculador actuales 2027')),
             ('https://www.quimpi.com/pdf/2026/CAMPAMENTOS%20DE%20DIA%20-%20ANEXOS.pdf',T('Связанный пример дневной программы; версия не 2027','Ejemplo diurno enlazado; versión distinta de 2027')),
             ('https://www.quimpi.com/pdf/2024/CAMPAMENTOS%20NOCTURNOS%20-%20ANEXOS.pdf',T('Связанный старый список вещей пансиона','Lista antigua enlazada de equipo residencial'))],lo,13,'2027-07-05')
        p['timing']['status']='published_2027';p['timing']['label']=T('8 отдельных недель Пн–Пт; ночёвка только в выбранном пансионном варианте.','8 semanas separadas de lunes a viernes; pernoctación solo en modalidad residencial elegida.')
        for n in range(8):
            a=date(2027,7,5)+timedelta(days=n*7);b=a+timedelta(days=4)
            label=T(f'Неделя {n+1} · выбранный формат','Semana '+str(n+1)+' · modalidad elegida')
            extra={}
            if not boarding:
                extra['sessions']=[dict(date=d,start_time='08:00',end_time='16:00',timezone='Atlantic/Canary',ical_timed=True,topic='Quimpi · De día') for d in weekdays(a.isoformat(),b.isoformat())]
            add_session(p,a.isoformat(),b.isoformat(),label,SUMMER,'camp_session' if boarding else 'session_days',**extra)
        out.append(p)
    return out

def gandara_profile():
    p=profile(1154,'gandara-christmas-2026-27','Gándara International School · Navidad','Испания','ESP','Gondomar · Pontevedra · Lugar de Moureira, 1, Mañufe',
        ['general','makers'],['day'],T('3–12 лет','3–12 años'),
        T('22 декабря 2026 – 7 января 2027, кроме праздников. Дневной лагерь 09:00–14:00, расширение 08:30–15:30. Творчество, кухня, сенсорное искусство, прогулки, рассказы и музыка. Три периода выбора в форме не доказывают занятия в выходные; точные дни уточнить.',
          '22 de diciembre de 2026 – 7 de enero de 2027, excepto festivos. Campamento diurno 09:00–14:00, ampliación 08:30–15:30. Creatividad, cocina, arte sensorial, aire libre, cuentos y música. Tres periodos elegibles en formulario no acreditan clases en fin de semana; confirmar días exactos.'),
        dict(year=2026,currency='EUR',amount=225,unit='full_camp_nonmember',tax_included=True,
             label=T('Для внешней семьи: 100 EUR за неделю или 225 EUR за весь лагерь на ребёнка; двоим весь лагерь = 450 EUR без скидок. Для членов школы 80 / 200 EUR. Применимые налоги включены по общим условиям; расширенные часы и питание отдельно уточнить.',
                     'Familia externa: 100 EUR por semana o 225 EUR por campamento completo por hijo; ambos completo = 450 EUR sin descuentos. Miembros del colegio 80 / 200 EUR. Impuestos aplicables incluidos según condiciones generales; confirmar ampliación y comida aparte.'),
             included=T('Основная программа и страхование гражданской ответственности / несчастных случаев по общим условиям лагерей.',
                        'Programa básico y seguro de responsabilidad civil / accidentes según condiciones generales de campamentos.'),
             extras=T('Стоимость раннего входа, позднего выхода, еды, трансфера и семейного жилья не установлена.',
                      'Coste de entrada anticipada, salida tardía, comida, traslado y alojamiento familiar sin acreditar.'),
             deposit=T('По условиям лагерей: более 2 недель до начала возврат 100%; от 2 недель до 72 часов — 50%; менее 72 часов / неявка — без возврата. Неиспользованные дни не переносятся. Подтверждение места по email и оплате; аванс 50 EUR относится к дням рождения, не к лагерю.',
                       'Según condiciones de campamentos: más de 2 semanas antes, devolución 100%; entre 2 semanas y 72 horas, 50%; menos de 72 horas / ausencia, sin devolución. Días no usados no se recuperan. Confirmación por email y pago; fianza de 50 EUR corresponde a cumpleaños, no campamento.')),
        NO_BOARD,[(GANDARA,T('Рождественская программа и цены внешних участников','Programa navideño y precios de externos')),(GTERMS,T('Условия именно лагерей: цена, отмена и страховки','Condiciones de campamentos: precio, cancelación y seguros'))],3,12,'2026-12-22')
    p['timing']['label']=T('Окно 22 декабря 2026 – 7 января 2027; праздничные / рабочие дни внутри не перечислены.',
                           'Ventana de 22 de diciembre de 2026 – 7 de enero de 2027; días festivos / laborables interiores sin enumerar.')
    add_session(p,'2026-12-22','2027-01-07',p['timing']['label'],GANDARA,'camp_window')
    return p

def cybroid_profiles():
    dates=weekdays('2026-11-16','2026-12-18')+weekdays('2027-01-04','2027-01-15')
    assert len(dates)==35
    out=[]
    rows=[(1155,'robotics','Robotics and Electronics',['robotics','makers'],
            T('Цепи, Arduino и автономная робот-машина.','Circuitos, Arduino y coche robot autónomo.')),
          (1156,'coding','Coding and Games',['coding','games'],
            T('Scratch, игры и анимация; Python для старших, не автоматическое обещание Python младшей группе.','Scratch, juegos y animación; Python para mayores, sin promesa automática de Python al grupo menor.')),
          (1157,'ai','AI for Kids',['ai','coding'],
            T('Обучение распознаванию изображений / звуков и использование результата в собственной игре.','Entrenar reconocimiento de imágenes / sonidos e incorporar resultado a juego propio.'))]
    for ident,key,name,themes,content in rows:
        programme=content+' '+T('Выбирают один трек на весь bootcamp. Группы Explorers 7–10 и Builders 11–15. Пн–Пт 09:00–12:00: первая часть 16 ноября – 18 декабря 2026, вторая 4–15 января 2027. Получается 35 опубликованных утренних дней, 105 часов расписания; перерывы внутри занятия не детализированы. Финал — семейный Demo Day и сертификат оператора, не международная победа.',
          'Se elige una vía durante todo el bootcamp. Grupos Explorers 7–10 y Builders 11–15. Lunes a viernes 09:00–12:00: primera parte 16 de noviembre – 18 de diciembre de 2026, segunda 4–15 de enero de 2027. Resultan 35 mañanas publicadas, 105 horas de horario; pausas internas sin detallar. Final con Demo Day familiar y certificado del operador, no victoria internacional.')
        p=profile(ident,'cybroid-tech-fun-'+key+'-2026-27','Cybroid · Tech Fun Camp · '+name,'Уганда','UGA','Kampala · Kansanga Complex, Level 2, near KIU',themes,['day'],
            T('7–15 лет; младшая группа Explorers 7–10','7–15 años; grupo menor Explorers 7–10'),programme,
            dict(year=2026,currency='UGX',amount=450000,unit='selected_bootcamp_track',early_bird_amount=380000,early_bird_until='2026-11-15',
             label=T('Один выбранный bootcamp-трек: 380000 UGX до 15 ноября, затем 450000 UGX; два допущенных участника по обычной цене = 900000 UGX, расчёт без скидок. Оскар на старте младше минимума. Плакат говорит before 15th Nov, текст until 15 Nov; точную границу скидки подтвердить. Это условие цены, не крайний срок записи.',
                     'Una vía elegida del bootcamp: 380000 UGX hasta 15 de noviembre, después 450000 UGX; dos participantes admitidos a precio ordinario = 900000 UGX, cálculo sin descuentos. Oscar al inicio no alcanza mínimo. Cartel dice before 15th Nov, texto until 15 Nov; confirmar límite exacto del descuento. Condición de precio, no cierre de registro.'),
             included=T('Занятия выбранного трека, семейный Demo Day и сертификат заявлены; включение платы за комплект и устройство прямо не установлено.',
                        'Declaradas clases de vía elegida, Demo Day familiar y certificado; inclusión de kit y dispositivo sin acreditar expresamente.'),
             extras=T('Налоги, ноутбук, комплект домой, еда, транспорт и жильё семьи не оценены.',
                      'Impuestos, portátil, kit para casa, comida, transporte y alojamiento familiar sin valorar.'),
             deposit=T('Оплата при записи; оператор обещает подтверждение email после оплаты. Общая refund-страница касается подписок и материалов; её 14-дневное правило для этого очного детского bootcamp не подтверждено.',
                       'Pago al reservar; operador promete confirmación por email tras pago. Página general de reembolsos trata suscripciones y materiales; regla de 14 días sin confirmar para este bootcamp infantil presencial.')),
            NO_BOARD,[(CYBROID,T('Первичная карточка детского bootcamp','Ficha primaria de bootcamp infantil')),
                     ('https://cybroid.com/legal/refunds',T('Общая refund-страница; применимость к лагерю неизвестна','Página general de reembolsos; aplicación al campamento desconocida'))],7,15,'2026-11-16')
        p['family_fit']['oscar']['detail']+=' '+T('На старте в ноябре 2026 ещё нет 7; январское присоединение после дня рождения не обещано.',
                                               'Al inicio en noviembre de 2026 aún no cumple 7; incorporación en enero tras cumpleaños no está prometida.')
        p['timing']['label']=T('16 ноября 2026 – 15 января 2027; зимний перерыв 19 декабря – 3 января, без занятий по выходным.',
                               '16 de noviembre de 2026 – 15 de enero de 2027; pausa invernal de 19 de diciembre – 3 de enero, sin clases de fin de semana.')
        add_session(p,'2026-11-16','2027-01-15',name,CYBROID,'session_days',
            sessions=[dict(date=d,start_time='09:00',end_time='12:00',timezone='Africa/Kampala',ical_timed=True,topic=name) for d in dates])
        out.append(p)
    return out

def newhope_profiles():
    out=[]
    provenance=T('Свежая публичная форма New Hope указывает институциональные адреса школы, но прямую ссылку на неё с текущего сайта найти не удалось. Школьный сайт подтверждает оператора и общие языковые варианты; привязку формы, кампус, возраст и приём внешних детей подтвердить до записи.',
                 'Formulario público actual New Hope incluye direcciones institucionales, pero no se halló enlace directo desde web actual. Web escolar acredita operador y modalidades lingüísticas generales; confirmar atribución del formulario, sede, edad y admisión externa antes de registrar.')
    for ident,key,name,themes,hours,programme in [
        (1158,'steam','STEAM Program',['robotics','science','makers'],'07:00–16:00',T('Робототехника, Science Lab, искусство, музыка, Mini Chef, спорт и окружающая среда. Доля робототехники и язык STEAM неизвестны.',
           'Robótica, Science Lab, arte, música, Mini Chef, deporte y ambiente. Proporción de robótica e idioma STEAM desconocidos.')),
        (1159,'english','English Program',['languages','general'],'07:00–12:00',T('Выравнивание английского и билингвальные активности. Школьный сайт отдельно описывает English Summer Camp полностью на EN и более формальный English Summer School; соответствие этой формы именно одному из них не доказано.',
           'Nivelación de inglés y actividades bilingües. Web escolar describe por separado English Summer Camp íntegramente EN y English Summer School más formal; correspondencia de este formulario con uno concreto sin acreditar.')),
        (1160,'sports','Sports Program',['sport','general'],'07:00–12:00',T('Плавание, волейбол, футбол и моторика. Это спортивный вариант, не робототехника и не спортивная лига.',
           'Natación, voleibol, fútbol y motricidad. Modalidad deportiva, no robótica ni liga deportiva.'))]:
        programme+=' '+provenance
        p=profile(ident,'newhope-'+key+'-2026-27','New Hope · '+name,'Коста-Рика','CRI',
            T('Heredia · Santa Bárbara · San Juan; это адрес школы, кампус выбранного лагеря ещё подтвердить.',
              'Heredia · Santa Bárbara · San Juan; dirección escolar, sede de campamento concreto aún por confirmar.'),themes,['day'],
            T('Возраст / класс выбранной программы не указан; школьный диапазон не переносить.','Edad / curso del programa elegido sin indicar; no trasladar rango escolar.'),programme,
            dict(year=2026,currency='CRC',amount=None,unit='programme',
                 label=T('Стоимость, единица оплаты и скидки в публичной форме не указаны; не считать программу бесплатной.',
                         'Formulario público no indica importe, unidad de pago ni descuentos; no considerar programa gratuito.'),
                 included=T('Выбранная программа описана; включение еды, материалов и техники не подтверждено.',
                            'Programa elegido descrito; inclusión de comida, materiales y equipo sin confirmar.'),
                 extras=T('Форма предлагает обед / перекус отдельным выбором; доплата, транспорт и техника неизвестны.',
                          'Formulario ofrece almuerzo / merienda como elección separada; suplemento, transporte y equipo desconocidos.'),
                 deposit=T('Есть выбор оплаты в кассе или запрос платёжной ссылки; возврат, предоплата, срок и подтверждение места не опубликованы.',
                           'Hay elección de pago en caja o solicitud de enlace; reembolso, anticipo, plazo y confirmación de plaza sin publicar.')),
            T(f'Дневной вариант {hours}; точные дни посещения, праздники и расширение уточнить.',
              f'Modalidad diurna {hours}; confirmar días exactos, festivos y ampliación.'),
            [(NH,T('Свежая публичная форма: программы и периоды','Formulario público actual: programas y periodos')),
             (NHABOUT,T('Школьный сайт: оператор, адрес и общие языковые варианты','Web escolar: operador, dirección y modalidades lingüísticas generales'))],start='2026-12-02',unknown=True)
        p['editorial_reason']=T('Близкий кандидат в Коста-Рике с опубликованной программой; возраст, стоимость и прямая связь формы ещё не подтверждены. Не включён в проверенный топ.',
                                'Candidato cercano en Costa Rica con programa publicado; edad, precio y vínculo directo del formulario aún sin confirmar. No incluido en selección superior verificada.')
        p['timing']['label']=T('Свежая форма: 2–18 декабря 2026 и 4–29 января 2027. Поисковый кэш содержал другие конечные / начальные дни; ежедневное расписание неизвестно.',
                               'Formulario actual: 2–18 de diciembre de 2026 y 4–29 de enero de 2027. Caché de búsqueda contenía otros días finales / iniciales; horario diario desconocido.')
        p['timing']['status']='partial_2026_27'
        p['timing']['unverified_periods']=[dict(start=start,end=end,source=NH) for start,end in
            [('2026-12-02','2026-12-18'),('2027-01-04','2027-01-29')]]
        p['timing']['label']+=' '+T('До подтверждения связи формы со школой эти окна не добавлены в календарь подтверждённых смен.',
                                    'Hasta confirmar vínculo del formulario con colegio, ventanas excluidas del calendario de sesiones confirmadas.')
        out.append(p)
    return out

def new_profiles():return quimpi_profiles()+[gandara_profile()]+cybroid_profiles()+newhope_profiles()
