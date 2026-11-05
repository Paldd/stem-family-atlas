"""Reviewed French holiday weeks and Spanish English-immersion camp windows."""
from datetime import date, timedelta
from camp_europe_v148 import lesson, merge_sources, weekdays

CHECKED = '2026-11-05'
SPANISH = {}


def T(ru, es):
    SPANISH[ru] = es
    return ru


IH = 'https://ih.fl-france.com/anglais/day-camp/'
IH_PDF = 'https://ih.fl-france.com/wp-content/uploads/2026/07/Brochure-Holiday-Camp-2026-2027.pdf'
IH_PREMIUM = 'https://ih.fl-france.com/wp-content/uploads/2026/07/Brochure-Holiday-Camp-Premium-avec-HiPe-Kids-2026-2027.pdf'
IH_TERMS = 'https://sejour.fl-france.fr/cgv/'
WANDER = 'https://www.wanderandwonderclub.com/summer-camp'
WANDER_HOLIDAY = 'https://www.wanderandwonderclub.com/holiday-camp'
WANDER_TERMS = 'https://www.wanderandwonderclub.com/terms-and-conditions'
GARENNE = 'https://www.la-garenne.ch/summer-camps/'
GARENNE_PDF = 'https://www.la-garenne.ch/summer/repository/summer-conditions.pdf'
NLD = 'https://www.nldeducation.com/english-camp-espana-2027/'
NLD_BOOKING = 'https://www.nldeducation.com/como-reservar/'
NLD_TERMS = 'https://www.nldeducation.com/condiciones-generales-contratacion/'


def source(title, url):
    return dict(title=title, url=url, checked=CHECKED)


NLD_PRICE = T('EUR 960 / 1 неделя; 1850 / 2 недели; 2680 / 3 недели на ребёнка. Одинаковые цены в Salamanca, Granada и Zaragoza. Точные заезды коротких пакетов ещё не указаны.',
              'EUR 960 / 1 semana; 1850 / 2 semanas; 2680 / 3 semanas por niño. Mismos precios en Salamanca, Granada y Zaragoza. Llegadas exactas de paquetes cortos aún sin indicar.')
NLD_PAYMENT = T('Бронь не подтверждается одной формой: оператор проверяет места и выдаёт ficha técnica / счёт. Сумма аванса назначается отдельно и входит в цену; остаток максимум за 45 дней до начала. Включённый management fee EUR 300 для Европы не добавлять повторно. При отмене этот сбор, визовые / почтовые расходы и возможные удержания поставщика не возвращают; дополнительно 10% за 90–60 дней, 25% за 31–60, 40% за 8–30, 100% за 7 и менее дней / неявку. На границе 60 дней две ставки, ранняя отмена описана не полностью — получить точное правило выбранного пакета. Условия не принимались.',
                'Reserva no confirmada por un formulario: operador comprueba plazas y emite ficha técnica / factura. Anticipo fijado aparte e incluido en precio; saldo como máximo 45 días antes del inicio. Management fee EUR 300 para Europa ya incluido, sin sumarlo otra vez. En cancelación no se devuelven este cargo, gastos de visado / envío y posibles cargos del proveedor; además 10% a 90–60 días, 25% a 31–60, 40% a 8–30, 100% a 7 o menos días / inasistencia. En límite de 60 días hay dos tasas y cancelación temprana incompleta: obtener regla exacta del paquete elegido. Sin aceptar condiciones.')
NLD_EXTRAS = T('Перелёты, страховка и трансфер к резиденции в цену явно не включены. Финальный email-счёт имеет приоритет над ценой сайта. Техника / модель робота / часы robotics не опубликованы; покупку набора не закладываем как подтверждённую обязанность.',
               'Vuelos, seguro y traslado a residencia no figuran expresamente incluidos. Presupuesto final por email prevalece sobre precio web. Equipo / modelo de robot / horas de robotics sin publicar; compra de kit no asumida como obligación confirmada.')
NLD_WINDOW = T('Опубликовано общее окно 4–25 июля 2027 во всех трёх городах и выбор 1 / 2 / 3 недель. Все комбинации заездов не перечислены: это окно выбора, а не подтверждённое проживание на 22 календарных дня. Даты конкретного пакета получить в ficha técnica.',
               'Publicado periodo general 4–25 de julio de 2027 en las tres ciudades y elección de 1 / 2 / 3 semanas. Sin lista de todas las combinaciones de llegada: periodo de elección, sin confirmar estancia de 22 días de calendario. Obtener fechas del paquete concreto en ficha técnica.')
IH_PAYMENT = T('Brochure 2026/27 отменяет registration fee. Общие CGV предусматривают полную оплату для окончательного зачисления и отдельные условия несовершеннолетним / не-ЕЭЗ. Применимость разделов отмены именно к English Holiday Camp и premium нужно письменно подтвердить: 14-дневный отказ в CGV прямо относится только к French courses. Не переносим его автоматически на этот лагерь.',
               'Brochure 2026/27 exime registration fee. CGV generales prevén pago completo para inscripción definitiva y condiciones específicas para menores / no EEE. Confirmar por escrito aplicación de cancelación a English Holiday Camp y premium: desistimiento de 14 días en CGV se refiere expresamente solo a French courses. Sin trasladarlo automáticamente a este campamento.')
IH_HOLIDAY = T('12–16 июля: в CGV есть общее исключение занятий в праздничные дни; работа Holiday Camp 14 июля отдельно не подтверждена. Сохраняем недельное окно, без обещания пяти фактических дней и без рассчитанной скидки.',
               '12–16 de julio: CGV excluyen en general clases en festivos; funcionamiento de Holiday Camp el 14 de julio sin confirmar aparte. Se conserva periodo semanal, sin prometer cinco días reales ni calcular descuento.')
WANDER_PAYMENT = T('Terms & Conditions ведут на незаполненный шаблон Wix о том, как писать условия. Реальный договор, срок оплаты, отмена, возврат, погода и переносы не установлены. До брони нужен договор именно выбранной смены; шаблон не принят за правила оператора.',
                   'Terms & Conditions lleva a plantilla Wix sin completar sobre cómo redactar condiciones. Sin contrato real, plazo de pago, cancelación, devolución, clima ni cambios establecidos. Antes de reservar obtener contrato de la sesión elegida; plantilla no tratada como reglas del operador.')


def build_profiles():
    age = T('8–15; Матвей 9–10 в 2027, Оскар 6–7 ниже минимума',
            '8–15; Matvey 9–10 en 2027, Oscar 6–7 por debajo del mínimo')
    cities = [('salamanca', 'Salamanca'), ('granada', 'Granada'), ('zaragoza', 'Zaragoza')]
    questions = [
        T('Получить ficha técnica с названием и адресом резиденции, выбранными датами 1 / 2 / 3 недель и местом для иностранного ребёнка.',
          'Obtener ficha técnica con nombre y dirección de residencia, fechas elegidas de 1 / 2 / 3 semanas y plaza para niño extranjero.'),
        T('Подтвердить требуемый английский: в примерном плане группы A2–C1; это не опубликованный обязательный порог допуска.',
          'Confirmar inglés requerido: plan orientativo muestra grupos A2–C1; no es umbral obligatorio de admisión publicado.'),
        T('Уточнить robotics: фактические часы, оборудование, ведущего и обязательность / выбор занятия. Примерный план не гарантирует ежедневный технический интенсив.',
          'Aclarar robotics: horas reales, equipo, instructor y actividad obligatoria / optativa. Plan orientativo no garantiza intensivo técnico diario.'),
        T('Получить полный счёт, страховку, трансфер, минимальную группу и правила отмены; общий минимум группы 15 может уточняться в ficha técnica.',
          'Obtener factura completa, seguro, traslado, grupo mínimo y cancelación; mínimo general de grupo 15 puede precisarse en ficha técnica.')]
    details = [dict(start='2027-07-04', end='2027-07-25', variant_key=key,
                    label=city+' · '+T('окно выбора 1 / 2 / 3 недель', 'periodo para elegir 1 / 2 / 3 semanas'),
                    place=city, formats=['boarding'], date_scope='camp_window', price=NLD_PRICE,
                    source=NLD, entry=NLD_WINDOW, questions=questions)
               for key, city in cities]
    p = dict(id='CP1173', slug='nld-english-spain-2027', provider='NLD Education · English Camp España 2027',
             country='Испания', iso='ESP', place='Salamanca / Granada / Zaragoza',
             themes=['general', 'languages'], formats=['boarding'], age=age,
             language=T('Оператор прямо указывает английский для уроков, активностей, экскурсий и всей лагерной жизни. Испанский сайт не означает испанский язык программы.',
                        'Operador declara inglés para clases, actividades, excursiones y toda la vida del campamento. Web española no implica programa en español.'),
             confirmed_instruction_languages=['EN'], language_evidence_role='primary',
             programme=T('Общий языковой пансион: английский, спорт, театр, кино, debate, творчество и robotics в примерном плане. NLD League Houses — внутренняя игра домов; её очки и награды не мировая соревновательная лига. Отдельный робототехнический интенсив, конкретный kit и число технических часов не подтверждены.',
                         'Residencia general de idiomas: inglés, deporte, teatro, cine, debate, creatividad y robotics en plan orientativo. NLD League Houses es juego interno de casas; puntos y premios no son liga mundial competitiva. Sin confirmar intensivo específico de robótica, kit concreto ni horas técnicas.'),
             timing=dict(status='published_2027', label=NLD_WINDOW, variant_keyed=True,
                         sessions=[[v['start'], v['end']] for v in details], session_details=details),
             price=dict(year=2027, currency='EUR', amount=None, unit='programme', label=NLD_PRICE,
                        included=T('Пансион и питание в резиденции, учебная и социальная программа заявлены. Налоги и management fee 300 включены по общим условиям. Точный перечень услуг выбранного тарифа закрепляется ficha técnica.',
                                   'Residencia y pensión completa, programa educativo y social declarados. Impuestos y management fee 300 incluidos según condiciones generales. Ficha técnica fija servicios exactos de tarifa elegida.'),
                        extras=NLD_EXTRAS, deposit=NLD_PAYMENT),
             accommodation=T('Salamanca: campus и отдельные спальни в общих апартаментах; Granada / Zaragoza: студенческие резиденции. Названия площадок и точные адреса не опубликованы, не подставляем случайный университет. Жильё родителей отдельно.',
                             'Salamanca: campus y dormitorios individuales en apartamentos compartidos; Granada / Zaragoza: residencias estudiantiles. Nombres de recintos y direcciones exactas sin publicar; sin asignar universidad arbitraria. Alojamiento de padres aparte.'),
             family_fit=dict(matvey=dict(status='candidate', detail=T('Возраст подходит 8–15; иностранный приём, уровень, конкретный заезд и место ещё подтвердить.',
                                                                    'Edad compatible con 8–15; confirmar admisión extranjera, nivel, llegada concreta y plaza.')),
                             oscar=dict(status='later', detail=T('Весь 2027 год 6–7: минимум 8 не достигается. Сопровождение старшего брата не отменяет правило.',
                                                                 'Todo 2027 tiene 6–7: no alcanza mínimo de 8. Acompañar al hermano mayor no elimina la regla.'))),
             editorial_reason=T('Кандидат Матвею на английский пансион с разнообразными занятиями в Испании; доступный прайс не доказывает мировой рейтинг качества или интенсивность робототехники.',
                                'Candidato para Matvey a residencia inglesa con actividades variadas en España; precio publicado no acredita ranking mundial de calidad ni intensidad de robótica.'),
             shortlist=['general'], questions=questions,
             sources=[source(T('English Camp España 2027 · города, язык, цены и окно', 'English Camp España 2027 · ciudades, idioma, precios y periodo'), NLD),
                      source(T('Порядок брони и подтверждение места', 'Reserva y confirmación de plaza'), NLD_BOOKING),
                      source(T('Оплата, включённый management fee и отмена', 'Pago, management fee incluido y cancelación'), NLD_TERMS)], checked=CHECKED)
    return [p]


def refresh_existing(report):
    profiles = {p['id']: p for p in report['profiles']}
    p = profiles['CP061']
    p['checked'] = CHECKED
    p['language_evidence_role'] = 'primary'
    p['timing']['label'] = T('Brochure 2026/27 и текущая страница подтверждают лето 5–30 июля 2027 во всех трёх городах: четыре недельных варианта на город. Зима / весна сохранены. Реальные дни 08:30–16:30 вынесены отдельно; неделя 12–16 июля остаётся окном из-за неопределённости 14 июля.',
                            'Brochure 2026/27 y página actual confirman verano 5–30 de julio de 2027 en las tres ciudades: cuatro opciones semanales por ciudad. Invierno / primavera conservados. Días reales 08:30–16:30 separados; semana 12–16 de julio sigue como periodo por incertidumbre del 14 de julio.')
    p['programme'] = T('Языковой дневной лагерь 8–17, группы 8–10 / 11–12 / 13–14 / 15–17, максимум 12 по brochure. Все уровни английского принимаются; утром English workshops, после обеда игры, культура и спорт, английский во всех взаимодействиях. Пансиона нет. Premium brochure: 3 индивидуальных онлайн-сессии до, 1 после и тест; точную комплектацию согласовать из-за неоднозначной нумерации на странице.',
                       'Campamento diurno de idiomas 8–17, grupos 8–10 / 11–12 / 13–14 / 15–17, máximo 12 según brochure. Todos los niveles de inglés admitidos; English workshops por la mañana, juegos, cultura y deporte por la tarde, inglés en todas las interacciones. Sin residencia. Brochure premium: 3 sesiones online individuales antes, 1 después y test; acordar contenido exacto por numeración ambigua de página.')
    p['price']['deposit'] = IH_PAYMENT
    p['price']['included'] = T('Стандарт: недельная дневная программа; registration fee отменён. Premium: отдельный пакет с online-подготовкой и итоговой сессией, не обязательная доплата.',
                              'Estándar: programa diurno semanal; registration fee exento. Premium: paquete separado con preparación online y sesión final, no suplemento obligatorio.')
    p['price']['extras'] = T('Холодный обед с собой; возможный транспорт по активностям, страховка и семейная поездка отдельно. Недельный тариф на праздничной неделе не уменьшен без счёта.',
                            'Comida fría propia; posible transporte de actividades, seguro y viaje familiar aparte. Tarifa semanal en semana festiva sin reducir sin factura.')
    addresses = {'paris': 'Paris · 9 rue de Saint-Pétersbourg · 75008',
                 'nice': 'Nice · 3 rue Alfred Mortier · 06100',
                 'biarritz': 'Biarritz · 6 avenue Jaulerry · 64200'}
    for key in ['paris', 'nice', 'biarritz']:
        amount = 360 if key == 'biarritz' else 340
        for week, start in enumerate(['2027-07-05', '2027-07-12', '2027-07-19', '2027-07-26'], 1):
            end = (date.fromisoformat(start) + timedelta(days=4)).isoformat()
            p['timing']['session_details'].append(dict(start=start, end=end,
                label=addresses[key].split(' · ')[0]+' · '+T('Лето · неделя ', 'Verano · semana ')+str(week),
                price='EUR '+str(amount)+' '+T('стандарт / ', 'estándar / ')+str(amount+90)+' premium '+T('за неделю', 'por semana'),
                place=addresses[key], source=IH_PDF, formats=['day'], date_scope='day_camp_window',
                variant_key=key+'-summer-'+str(week)))
    for v in p['timing']['session_details']:
        if v['end'] < CHECKED:
            continue
        v['place'] = addresses[v['variant_key'].split('-')[0]]
        if v['start'] == '2027-07-12':
            v['date_scope'] = 'day_camp_window'
            v['attendance_weekdays'] = []
            v['entry'] = IH_HOLIDAY
            v.pop('sessions', None)
        else:
            v['date_scope'] = 'session_days'
            v['sessions'] = [lesson(day, '08:30', '16:30', 'Europe/Paris', 'English Holiday Camp')
                             for day in weekdays(v['start'], v['end'])]
    p['timing']['sessions'] = [[v['start'], v['end']] for v in p['timing']['session_details']]
    p['questions'] = [T('Подтвердить места, адрес, работу 14 июля и условия English Holiday Camp для иностранного несовершеннолетнего; Оскару нужен лагерь с минимумом ниже 8.',
                        'Confirmar plazas, dirección, actividad del 14 de julio y condiciones de English Holiday Camp para menor extranjero; Oscar necesita mínimo inferior a 8.'),
                      T('Уточнить местный транспорт, страхование, premium-пакет, оплату и отмену. Полный недельный тариф не гарантирует пять дней при праздничном исключении.',
                        'Aclarar transporte local, seguro, paquete premium, pago y cancelación. Tarifa semanal completa no garantiza cinco días si hay excepción festiva.')]
    merge_sources(p, [source('Holiday Camp 2026/27 · PDF', IH_PDF), source('Holiday Camp Premium 2026/27 · PDF', IH_PREMIUM),
                      source(T('Текущая страница · лето 2027', 'Página actual · verano 2027'), IH),
                      source(T('CGV · применимость к английскому лагерю уточнить', 'CGV · confirmar aplicación a campamento inglés'), IH_TERMS)])

    p = profiles['CP060']
    p['checked'] = CHECKED
    p['price']['deposit'] = WANDER_PAYMENT
    p['price']['label'] = T('Лето / обычные holiday-недели: EUR 380 за 1 неделю; EUR 360 за неделю при выборе 2 и более недель одним ребёнком. Два брата на одну неделю не равны многонедельной скидке. Christmas MiniCamp 21–23 декабря: отдельный трёхдневный тариф не опубликован.',
                           'Verano / semanas holiday normales: EUR 380 por 1 semana; EUR 360 por semana si un niño elige 2 o más semanas. Dos hermanos en una semana no equivalen a descuento por varias semanas. Christmas MiniCamp 21–23 de diciembre: tarifa específica de tres días sin publicar.')
    p['timing']['label'] = T('Лето: пять отдельных недель 2027; зима 8–19 февраля — выбор 1 / 2 недель; Christmas MiniCamp 21–23 декабря 2026 — три дня. Весенний год на странице остаётся 2017, поэтому весну 2027 не подтверждаем. Старое осеннее окно сохранено как архив.',
                            'Verano: cinco semanas separadas de 2027; invierno 8–19 de febrero: elegir 1 / 2 semanas; Christmas MiniCamp 21–23 de diciembre de 2026: tres días. Año de primavera en página sigue 2017, sin confirmar primavera 2027. Periodo anterior de otoño conservado como archivo.')
    mini = dict(start='2026-12-21', end='2026-12-23', label=T('Christmas MiniCamp · три дня', 'Christmas MiniCamp · tres días'),
                price=T('Тариф трёх дней не опубликован; недельные 380 не переносим и не делим автоматически.',
                        'Tarifa de tres días sin publicar; sin trasladar ni dividir automáticamente 380 semanales.'),
                place=p['place'], source=WANDER_HOLIDAY, formats=['day'], date_scope='session_days')
    p['timing']['session_details'].append(mini)
    for v in p['timing']['session_details']:
        if v['end'] < CHECKED:
            continue
        v['date_scope'] = 'session_days'
        v['sessions'] = [lesson(day, '09:00', '16:00', 'Europe/Paris', 'English Nature Camp')
                         for day in weekdays(v['start'], v['end'])]
    p['timing']['sessions'] = [[v['start'], v['end']] for v in p['timing']['session_details']]
    p['questions'] = [T('Подтвердить конкретную площадку и группу братьев, наличие мест, реальный договор и правила погоды / отмены. Christmas: получить цену именно трёх дней.',
                        'Confirmar recinto y grupo de hermanos, plazas, contrato real y reglas de clima / cancelación. Christmas: obtener precio específico de tres días.'),
                      T('Два перекуса включены, lunchbox свой. Полная поездка, цена public transport для экскурсии и страховка отдельно. Исправленный год весны получить у оператора.',
                        'Dos meriendas incluidas, lunchbox propio. Viaje completo, coste de public transport para excursión y seguro aparte. Obtener año corregido de primavera del operador.')]
    merge_sources(p, [source(T('Летние недели 2027, EN и многонедельная цена', 'Semanas de verano 2027, EN y precio de varias semanas'), WANDER),
                      source(T('Christmas 2026, зима 2027 и опечатка весны', 'Christmas 2026, invierno 2027 y errata de primavera'), WANDER_HOLIDAY),
                      source(T('Незаполненный шаблон условий · не договор', 'Plantilla de condiciones sin completar · no contrato'), WANDER_TERMS)])

    p = profiles['CP002']
    p['checked'] = CHECKED
    p['accommodation'] = T('Пансион 5–12: комнаты 4–6; day без ночёвок 08:50–18:00. Если родители живут поблизости во время смены, PDF разрешает ребёнку только day, не boarding. Пансион братьев и day нельзя смешивать в одной смене. Конкретная техническая опция и язык ведущего отдельно.',
                            'Residencia 5–12: habitaciones de 4–6; day sin pernocta 08:50–18:00. Si padres se alojan cerca durante sesión, PDF permite al niño solo day, no boarding. Hermanos no pueden mezclar residencia y day en misma sesión. Opción técnica concreta e idioma de instructor aparte.')
    p['timing']['label'] = T('Те же опубликованные смены 2027 и цены 5–12 подтверждены повторно. Три day-пакета по 2 недели включают субботу первой недели: 11 дней 08:50–18:00, не только Пн–Пт. Два day-пакета по 4 недели остаются окнами: расписание промежуточных суббот не разъяснено.',
                            'Mismas sesiones 2027 y precios 5–12 confirmados de nuevo. Tres paquetes day de 2 semanas incluyen sábado de primera semana: 11 días 08:50–18:00, no solo Lu–Vi. Dos paquetes day de 4 semanas siguen como periodos: sábados intermedios sin aclarar.')
    for v in p['timing']['session_details']:
        if v['formats'] != ['day']:
            continue
        if (date.fromisoformat(v['end'])-date.fromisoformat(v['start'])).days == 11:
            first_saturday = (date.fromisoformat(v['start'])+timedelta(days=5)).isoformat()
            days = sorted(weekdays(v['start'], v['end'])+[first_saturday])
            v['date_scope'] = 'session_days'
            v['sessions'] = [lesson(day, '08:50', '18:00', 'Europe/Zurich', 'La Garenne · Day Camp') for day in days]
        else:
            v['date_scope'] = 'camp_window'
            v['entry'] = T('Дневное окно 4 недель. Уточнить субботы промежуточных недель; это не непрерывный пансион и не подтверждённое посещение всех календарных дней.',
                           'Periodo diurno de 4 semanas. Confirmar sábados intermedios; no es residencia continua ni asistencia confirmada todos los días de calendario.')
    merge_sources(p, [source('Summer Camp 2027 · conditions / fees / day attendance', GARENNE_PDF),
                      source(T('Summer Camp · общий обзор', 'Summer Camp · resumen general'), GARENNE)])


def extend_planning(d):
    offers = []
    common = dict(currency='EUR', price_year=2027, discount_second=0, required=[],
                  unknown_trip=['travel', 'lodging', 'misc'], checked=CHECKED)
    for weeks, amount in [(1, 960), (2, 1850), (3, 2680)]:
        offers.append(dict(common, id='nld-matvey-'+str(weeks)+'-weeks-2027', slug='nld-english-spain-2027',
            label='NLD · '+T('Матвей · ', 'Matvey · ')+str(weeks)+T(' нед. · город и даты выбрать', ' sem. · elegir ciudad y fechas'),
            format='boarding', period_type='season_window', children=['matvey'], base_by_child=dict(matvey=amount), optional=[],
            sessions=[['2027-07-04', '2027-07-25']], sources=[NLD, NLD_BOOKING, NLD_TERMS],
            unknown_required=[dict(id='invoice_services', label=T('Обязательные услуги по ficha técnica / страховка / transfer · уточнить', 'Servicios obligatorios según ficha técnica / seguro / transfer · confirmar'), unit='amount', rate=1, min=0)],
            gate=T('Только Матвей 8–15. Salamanca / Granada / Zaragoza: город, фактические даты выбранной длительности и приём иностранной семьи подтвердить. Оскар ниже 8.',
                   'Solo Matvey 8–15. Salamanca / Granada / Zaragoza: confirmar ciudad, fechas reales de duración elegida y admisión de familia extranjera. Oscar menor de 8.'),
            deposit_note=NLD_PAYMENT, included=T('Опубликованный тариф на одного ребёнка, пансион и питание. Management fee 300 уже внутри, не доплата.',
                                               'Tarifa publicada de un niño, residencia y pensión completa. Management fee 300 ya incluido, no suplemento.'),
            scope=NLD_WINDOW+' '+NLD_EXTRAS))
    for city, amount, key in [('Paris / Nice', 340, 'paris-nice'), ('Biarritz', 360, 'biarritz')]:
        offers.append(dict(common, id='ih-'+key+'-matvey-summer-2027', slug='ih-holiday',
            label='IH · '+city+' · '+T('Матвей · неделя 5–9 июля 2027', 'Matvey · semana 5–9 de julio de 2027'),
            format='day', children=['matvey'], base_by_child=dict(matvey=amount),
            sessions=[['2027-07-05', '2027-07-09']], sources=[IH_PDF, IH_PREMIUM, IH_TERMS],
            unknown_required=[dict(id='lunch_transport_cover', label=T('Lunchbox, транспорт активностей и страховка при необходимости', 'Lunchbox, transporte de actividades y seguro si procede'), unit='amount', rate=1, min=0)],
            optional=[dict(id='premium', label=T('Вместо standard выбрать premium · доплата 90', 'Elegir premium en lugar de standard · suplemento 90'), amount=90)],
            gate=T('Матвей соответствует Explorers 8–10; Оскар ниже 8. Город и места подтвердить. Это одна неделя, не цена месяца.',
                   'Matvey cumple Explorers 8–10; Oscar menor de 8. Confirmar ciudad y plazas. Una semana, no precio de mes.'),
            deposit_note=IH_PAYMENT, included=T('Дневная программа 08:30–16:30; registration fee 0 по brochure. Premium добавлен только разницей 90, не второй полной ценой.',
                                               'Programa diurno 08:30–16:30; registration fee 0 según brochure. Premium añadido solo por diferencia 90, no otro precio completo.'),
            scope=T('Жильё семьи, перелёты, питание и возможные местные расходы не закрыты тарифом. Неделя 12–16 июля требует отдельной проверки 14 июля.',
                    'Tarifa no cubre alojamiento familiar, vuelos, comida ni posibles gastos locales. Semana 12–16 de julio requiere comprobar aparte el 14 de julio.')))
    for weeks, per_child in [(1, 380), (2, 720)]:
        offers.append(dict(common, id='wander-both-'+str(weeks)+'-weeks-2027', slug='wander-wonder',
            label='Wander & Wonder · '+T('двое · ', 'dos niños · ')+str(weeks)+T(' нед. с 5 июля 2027', ' sem. desde 5 de julio de 2027'),
            format='day', children=['matvey', 'oscar'], base_by_child=dict(matvey=per_child, oscar=per_child),
            sessions=[['2027-07-05', '2027-07-09' if weeks == 1 else '2027-07-16']], sources=[WANDER, WANDER_TERMS], optional=[],
            unknown_required=[dict(id='lunch_trip_cover', label=T('Lunchbox обоих, transport экскурсии / страховка если нужны', 'Lunchbox de ambos, transport de excursión / seguro si procede'), unit='amount', rate=1, min=0)],
            gate=T('Оба соответствуют 3–12; выбрать Paris или Saint-Germain-en-Laye и группы. Скидка 360 / неделю применяется при 2 неделях каждому, не за одного брата на одну неделю.',
                   'Ambos cumplen 3–12; elegir Paris o Saint-Germain-en-Laye y grupos. Descuento 360 / semana corresponde a 2 semanas de cada niño, no a un hermano por una semana.'),
            deposit_note=WANDER_PAYMENT,
            included=T('09:00–16:00 и два перекуса в день, обед из дома. База двух 760 за одну неделю или 1440 за две; без дополнительной sibling-скидки.',
                       '09:00–16:00 y dos meriendas diarias, comida propia. Base de dos 760 por una semana o 1440 por dos; sin descuento sibling adicional.'),
            scope=T('Тариф обычных летних недель. Рождественские три дня не оценены этим тарифом; цена поездки и действующий договор ещё нужны.',
                    'Tarifa de semanas normales de verano. Tres días navideños no valorados con esta tarifa; faltan precio de viaje y contrato vigente.')))
    # The existing dossier's stable slug is retained in both editions and offers.
    wander_slug = next(p['slug'] for p in d['camp_programmes']['profiles'] if p['id'] == 'CP060')
    for offer in offers:
        if offer['id'].startswith('wander-'):
            offer['slug'] = wander_slug
    idx = {o['id']: o for o in offers}
    old = {o['id'] for o in d['camp_planning']['offers']}
    d['camp_planning']['offers'] = [idx.get(o['id'], o) for o in d['camp_planning']['offers']]+[o for o in offers if o['id'] not in old]
    d['camp_planning'].update(version=150, asof=CHECKED)


def enrich_v150(d):
    extend_planning(d)
