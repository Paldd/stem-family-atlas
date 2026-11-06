"""Ethiopian/Zimbabwean routes, separately dated archives and family age fixes."""
from copy import deepcopy
from nepal_maldives_v180 import P, src
from nearby_regional_v160 import event, programme

CHECKED = '2026-11-06'
SPANISH = {}
def T(ru, es):
    SPANISH[ru] = es
    return ru

ETH = 'https://stemforkids.et/'
STEM = 'https://www.stempower.org/'
GIST = 'https://girlsinstemtrust.org/'
ZRO = GIST + '2024/07/01/world-robot-olympiad-competition/'
ECA = 'https://uneca.org/eca-events/stories/ethiopia-and-tanzania-young-innovators-shine-national-finals-ahead-world-robot-olympiad'
NET = 'https://www.netrozim.co.zw/kit'
ELAB = 'https://elabrobotics.co.zw/'
HUNDRED = 'https://robotics.co.zw/kids-tech/robotics-for-kids-highfields/'
MATOR = 'https://www.matordesign.com/events'
TME = 'https://tmeeducation.com/en-ZZ/page/74412/zimbabwe-forms-robotics-team-through-holiday-stem-camp'
HARROW = 'https://aisloutdoor.com/products/ecobot-patrol-mission-green-city'
TKH = 'https://www.techknowhowkids.com/'
GATE = T('Подтвердить индивидуальный приём иностранного ребёнка, возраст / класс, язык преподавания, место и окончательный счёт. Заявки, сообщения, согласия и оплаты не выполнялись.', 'Confirmar admisión individual de menor extranjero, edad / curso, idioma docente, plaza y factura final. Sin solicitudes, mensajes, consentimientos ni pagos.')
LANG = T('Язык сайта — английский; язык преподавания и поддержка EN / ES / RU для выбранного ребёнка не подтверждены.', 'Web en inglés; idioma docente y apoyo EN / ES / RU para el menor elegido sin confirmar.')
UNKNOWN = T('Следующие даты, цена и наличие мест не установлены.', 'Fechas siguientes, precio y plazas sin establecer.')
TRIP = T('Жильё семьи, дорога, питание вне включений и страховка отдельно. Неизвестная цена не равна нулю.', 'Alojamiento familiar, transporte, comidas fuera de inclusiones y seguro aparte. Precio desconocido no equivale a cero.')
REGULAR = T('Регулярный курс; точные даты нового набора и каникулярная смена не опубликованы. Дневное обучение без подтверждённого пансиона.', 'Curso regular; fechas exactas del nuevo grupo y turno vacacional sin publicar. Enseñanza diurna sin residencia confirmada.')
ARCHIVE = T('Исторический результат 2024 года. Это не запись на следующий сезон и не доказательство текущего младшего набора, пансиона или международной победы.', 'Resultado histórico de 2024. No es inscripción en temporada siguiente ni acredita grupo infantil actual, residencia o victoria internacional.')

def fit(lo=None, hi=None):
    out = {}
    for child, age in [('matvey', 9), ('oscar', 6)]:
        status = 'unknown' if lo is None else 'later' if age < lo else 'not_eligible' if age > hi else 'conditional'
        text = GATE if lo is None else T(f'Сейчас {age} лет; опубликованный диапазон {lo}–{hi}. Возраст новой смены, уровень и язык подтвердить.', f'Ahora {age} años; intervalo publicado {lo}–{hi}. Confirmar edad del nuevo turno, nivel e idioma.')
        out[child] = dict(status=status, detail=text)
    return out

def profile(i, slug, name, iso, age, themes, lo=None, hi=None):
    p = P(i, slug, name, 'NPL', age, themes)
    p.update(iso=iso, country=T('Эфиопия', 'Etiopía') if iso == 'ETH' else T('Зимбабве', 'Zimbabue'), place='Addis Ababa' if iso == 'ETH' else 'Harare', family_fit=fit(lo, hi), language=LANG, questions=[GATE], checked=CHECKED)
    p['price'].update(currency='ETB' if iso == 'ETH' else 'USD', year=None, amount=None, unit='programme', label=UNKNOWN, extras=TRIP)
    p['timing'].update(status='next_unannounced', label=REGULAR, sessions=[], session_details=[])
    return p

def make_profiles():
    rows = []
    for i, slug, name, amount, desc in [
        (1438, 'stem-for-kids-ethiopia-beginner', 'STEM For Kids Ethiopia · Beginner', 5750, T('Начальный поток: Programming I / II и Robotics I; материалы, комплекты и еженедельные занятия включены по FAQ.', 'Track inicial: Programming I / II y Robotics I; materiales, kits y clases semanales incluidos según FAQ.')),
        (1439, 'stem-for-kids-ethiopia-advanced', 'STEM For Kids Ethiopia · Advanced', 7187.50, T('Продвинутый поток: Robotics II, Python, Raspberry Pi и Web Development; конкретный курс и входной уровень выбираются отдельно.', 'Track avanzado: Robotics II, Python, Raspberry Pi y Web Development; curso concreto y nivel de entrada se eligen aparte.')),
        (1440, 'stem-for-kids-ethiopia-private', 'STEM For Kids Ethiopia · Private Class', 73400, T('Индивидуально организованная группа до 6 учеников, дома или в центре, с согласуемым расписанием и выбором курса. Цена названа для Private Class; единица за ученика / всю группу и итоговый счёт не разъяснены.', 'Grupo organizado de hasta 6 alumnos, en casa o centro, con horario acordado y curso elegido. Precio indicado para Private Class; unidad por alumno / grupo entero y factura final sin aclarar.'))]:
        p = profile(i, slug, name, 'ETH', '4–17 programme page; homepage also says 4–18', ['robotics', 'coding', 'engineering'], 4, 17)
        p.update(place='Summit AICC / Flamingo Youth Center / Varnero · Addis Ababa', programme=desc + ' ' + REGULAR + ' ' + T('Возраст 4–17 относится к общей программе, не гарантирует одинаковый допуск на каждый курс. На homepage встречается 4–18; для семьи обе границы выше текущего возраста. Даты лагеря и язык занятий отдельно не обещаны.', 'Edad 4–17 corresponde al programa general y no garantiza igual admisión en cada curso. Homepage también indica 4–18; ambos límites superiores superan edades actuales de familia. Sin promesa separada de fechas de campamento o idioma docente.'), sources=[src('STEM For Kids · programmes', ETH+'programs'), src('STEM For Kids · pricing', ETH+'pricing'), src('STEM For Kids · centres', ETH+'contactus')])
        p['price'].update(amount=amount, unit='private_plan_month_unit_unconfirmed' if i == 1440 else 'child_per_month', label=T(f'ETB {amount} в месяц, включая VAT, по опубликованному плану. Год тарифной сетки не указан.', f'ETB {amount} al mes, VAT incluido, según plan publicado. Año de tarifa sin indicar.'), included=desc, deposit=T('Beginner / Advanced: сайт объявляет при оплате 3 месяцев 5% sibling + 5% retained-student. Применимость к новой семье и порядок суммирования отдельно; скидка не вычтена автоматически. Условия отмены не установлены.', 'Beginner / Advanced: web anuncia con pago de 3 meses 5% sibling + 5% retained-student. Aplicación a familia nueva y forma de combinar aparte; sin descuento automático. Cancelación sin establecer.') if i != 1440 else GATE)
        rows.append(p)
    p = profile(1441, 'netro-zimbabwe-holiday-bootcamp', 'Netro · Kidz in Tech · Holiday Bootcamp', 'ZWE', '6–17', ['robotics', 'coding', 'engineering'], 6, 17)
    p.update(programme=T('Двухнедельные каникулы: код, электроника, дроны и проектные сборки. Оператор также поддерживает школьные команды; обещания конкретной мировой квалификации нет. Трёхдневная сертификация учителей — другая, взрослая программа.', 'Vacaciones de dos semanas: código, electrónica, drones y construcción de proyectos. Operador también apoya equipos escolares; sin promesa de clasificación mundial concreta. Certificación docente de tres días es otro programa para adultos.'), sources=[src('Netro · Kidz in Tech', NET)], place=T('Зимбабве · площадка следующей смены уточняется', 'Zimbabue · sede del siguiente turno por confirmar'))
    p['timing']['label'] = T('Заявлена длительность 2 недели; следующие календарные дни не опубликованы.', 'Duración anunciada de 2 semanas; días siguientes sin publicar.')
    rows.append(p)
    p = profile(1442, 'elab-zimbabwe-holiday-robotics', 'Elab · Holiday Robotics / Drone / AI Camps', 'ZWE', T('Возраст не опубликован', 'Edad sin publicar'), ['robotics', 'ai', 'coding'])
    p.update(place='Office W8-9 · Bervic Building · 9 Selkirk Road · Eastlea · Harare; camp venue TBD', programme=T('Недельные каникулярные лагеря по роботам, дронам и ИИ, школьные клубы и наставничество. В календаре событий нет предстоящих записей. Возраст в отзыве ученика и адрес офиса не заменяют правила приёма и место лагеря.', 'Campamentos vacacionales semanales de robots, drones e IA, clubes escolares y mentoría. Calendario sin eventos próximos. Edad de alumno en testimonio y dirección de oficina no sustituyen reglas de admisión y sede del campamento.'), sources=[src('Elab · programmes', ELAB), src('Elab · event calendar', ELAB+'events/')])
    p['timing']['label'] = T('Типовая длительность 1 неделя; календарь на дату проверки без предстоящих событий.', 'Duración habitual de 1 semana; calendario sin eventos próximos al verificar.')
    rows.append(p)
    for i, slug, name, lo, desc, themes in [
        (1443, 'robotics', 'Robotics', 7, T('Сборка и код роботов, датчики, механика; начальный курс 8–12 недель, возможны выходные. Комплекты Arduino-based / LEGO Mindstorms-style предоставляются по FAQ.', 'Montaje y código de robots, sensores y mecánica; curso inicial de 8–12 semanas, opción de fines de semana. Kits Arduino-based / LEGO Mindstorms-style proporcionados según FAQ.'), ['robotics', 'coding', 'engineering']),
        (1444, 'coding', 'Coding & Programming', 7, T('Игры, приложения и сайты на Scratch / Python; уровень и фактический инструмент младшей группы подтвердить.', 'Juegos, aplicaciones y webs con Scratch / Python; confirmar nivel y herramienta real del grupo menor.'), ['coding', 'games']),
        (1445, 'electronics', 'Electronics for Kids', 9, T('Цепи и собственные электронные устройства. Девятилетний Матвей — возрастной кандидат, шестилетний Оскар ниже опубликованного минимума.', 'Circuitos y dispositivos electrónicos propios. Matvey de nueve años es candidato por edad, Oscar de seis menor del mínimo publicado.'), ['engineering', 'maker']),
        (1446, 'arduino', 'Arduino for Kids', 10, T('Микроконтроллеры, датчики и моторы. Оба ребёнка пока младше 10; следующий этап развития, не текущий приём.', 'Microcontroladores, sensores y motores. Ambos menores de 10; etapa futura, no admisión actual.'), ['robotics', 'engineering', 'coding']),
        (1447, 'python', 'Python for Kids', 10, T('Отдельный курс Python с минимумом 10 лет. Не переносить на него младший возраст общего Coding & Programming.', 'Curso específico de Python con mínimo de 10 años. No trasladar edad menor de Coding & Programming general.'), ['coding']),
        (1448, 'cybersecurity', 'Cyber Security for Kids', 10, T('Безопасность в интернете и начальные понятия ethical hacking. Это учебная программа с сертификатом; конкурсного места она не доказывает.', 'Seguridad en internet y conceptos iniciales de ethical hacking. Programa lectivo con certificado; no acredita puesto competitivo.'), ['technology', 'coding'])]:
        p = profile(i, 'hundred-tech-zimbabwe-'+slug, 'Hundred Tech Academy · '+name, 'ZWE', f'{lo}–17', themes, lo, 17)
        p.update(place='No. 32 Jason Moyo · Harare; Highfields partner venue TBD', programme=desc + ' ' + T('Страница содержит общий баннер 4–17, но карточки отдельных курсов указывают более высокий минимум. Для допуска применён минимум курса; новое расписание и исключения не подтверждены.', 'Página contiene banner general de 4–17, pero fichas de cursos indican mínimo superior. Se aplica mínimo del curso para admisión; horario nuevo y excepciones sin confirmar.'), sources=[src('Hundred Tech · course ages and FAQ', HUNDRED), src('Hundred Tech · children curriculum', 'https://robotics.co.zw/courses-for-kids/'), src('Hundred Tech · main address', 'https://robotics.co.zw/contact/')])
        rows.append(p)
    return rows

def refresh_profiles(raw):
    for p in raw['profiles']:
        if p['id'] not in ['CP720', 'CP737']:
            continue
        p['family_fit'] = dict(matvey=dict(status='not_eligible', detail=T('Матвею уже 9 лет; верхняя граница этого курса 8. Не предлагать как подходящий трек и не предполагать исключение.', 'Matvey ya tiene 9 años; límite superior de este curso 8. No ofrecer como track compatible ni suponer excepción.')), oscar=dict(status='conditional', detail=T('Оскару уже 6 лет: опубликованный возраст подходит. Место, иностранный приём и конкретную смену подтвердить.', 'Oscar ya tiene 6 años: edad publicada compatible. Confirmar plaza, admisión extranjera y turno concreto.')))
        for v in p['timing']['session_details']:
            v['family_fit'] = deepcopy(p['family_fit'])
        p['checked'] = CHECKED
        if p['id'] == 'CP720':
            p['sources'].append(src('AISL Outdoor · English medium and age requirement', 'https://aisloutdoor.com/pages/general-information'))
            p['questions'].append(T('Возраст 6–8 вновь прочитан через официальный web-reader; прямой GET карточки вернул HTTP 429. Текущий остаток мест не перепроверен. Общая политика требует возраст курса; зимние условия отдельно.', 'Edad 6–8 releída mediante lector web oficial; GET directo de ficha devolvió HTTP 429. Plazas actuales sin reverificar. Política general exige edad del curso; condiciones de invierno aparte.'))
        else:
            for s in p['sources']:
                s['checked'] = CHECKED
            p['price']['label'] = T('USD355/3 дня или 465/4 дня; aftercare до 17:00 +80 или +105. Цена за одного ребёнка. Матвей старше опубликованных 5–8; общий бюджет двух братьев по этому курсу не рассчитан.', 'USD355/3 días o 465/4 días; aftercare hasta 17:00 +80 o +105. Precio por niño. Matvey mayor de los 5–8 publicados; presupuesto conjunto de hermanos para este curso sin calcular.')
            p['questions'].append(T('Свежие страницы Glen Park и Sunset подтверждают старые интервалы, адреса и цены. Обобщённая страница Pokémon смешивает другие площадки и 3-/4-дневные строки; её 4 дня не перенесены на Sunset.', 'Páginas actuales de Glen Park y Sunset confirman intervalos, direcciones y precios previos. Página general Pokémon mezcla otras sedes y filas de 3/4 días; sus 4 días no trasladados a Sunset.'))

def E(ident, title, iso, source, **fields):
    e = event(ident, title, T('Эфиопия', 'Etiopía') if iso == 'ETH' else T('Зимбабве', 'Zimbabue'), source, **fields)
    e.update(region=T('Африка', 'África'), iso=[iso], checked=CHECKED)
    return e

def make_events(profiles):
    rows = []
    for ident, iso, title, url, note in [
        ('C1924', 'ETH', 'WRO Ethiopia · next national route / STEMpower', STEM+'restricted-grants', T('STEMpower описывает завершённый проект для 600 учащихся 8–19; на международный финал в Турции отбирались команды. Это архив, не действующая квота или набор 2027. Новые категории, язык, иностранное представительство и сроки не объявлены.', 'STEMpower describe proyecto terminado para 600 alumnos de 8–19; se seleccionaban equipos para final internacional en Turquía. Archivo, no cupo vigente ni inscripción 2027. Categorías nuevas, idioma, representación extranjera y plazos sin anunciar.')),
        ('C1926', 'ZWE', 'WRO Zimbabwe · next national route / Girls in STEM Trust', GIST, T('Отчёт 2024 описывает провинциальный отбор Harare / Bulawayo / Masvingo, затем национальный финал NUST. Новый сезон и доступ внешней команды не подтверждены. Название Girls in STEM не доказывает ограничение только девочками; актуальное правило пола не найдено.', 'Informe 2024 describe clasificación provincial Harare / Bulawayo / Masvingo y final nacional NUST. Temporada nueva y acceso de equipo externo sin confirmar. Nombre Girls in STEM no acredita exclusividad para niñas; regla actual de género no encontrada.'))]:
        rows.append(E(ident, title, iso, url, age=T('Исторически 8–19 / Junior и Senior; новая категория уточняется', 'Históricamente 8–19 / Junior y Senior; confirmar categoría nueva'), scope='national', entry=GATE, note=note, proof=note, language=LANG, mat=T('Условно: возраст и страна представительства по новому регламенту', 'Condicional: edad y país representado según reglamento nuevo'), osc=T('Не подтверждён младший трек для 6 лет', 'Sin confirmar track para 6 años'), status='Идея'))
    rows.append(E('C1925', 'WRO Ethiopia · National Competition 2024 · archive', 'ETH', ECA, start='2024-10-04', end='2024-10-04', city='UN Conference Center · Addis Ababa', age='2024 · 8–19 training project; category-specific rules unconfirmed', scope='national', status='Идея', period='2024-10-04', mat=ARCHIVE, osc=ARCHIVE, entry=ARCHIVE, note=ARCHIVE, proof=T('Отчёт ECA от 7 октября 2024 прямо называет день соревнования 4 октября, площадку и национальных победителей. Это не дата публикации отчёта.', 'Informe ECA de 7 de octubre de 2024 identifica día competitivo 4 de octubre, sede y ganadores nacionales. No es fecha de publicación del informe.'), language=LANG, gear=T('Архив 2024: собственный выбор hardware / software для проектов устойчивого развития. Новые технические правила отдельно.', 'Archivo 2024: hardware / software elegidos para proyectos de sostenibilidad. Reglas técnicas nuevas aparte.')))
    rows.append(E('C1927', 'WRO Zimbabwe · National Finals 2024 · archive', 'ZWE', ZRO, city='National University of Science and Technology · Bulawayo', age='Junior / Senior · numerical ages not stated in report', scope='national', status='Идея', date_status=T('Архив 2024; точный день неизвестен', 'Archivo 2024; día exacto desconocido'), period=T('2024; точный день не установлен. 1 июля — дата публикации.', '2024; día exacto sin establecer. 1 de julio es publicación.'), mat=ARCHIVE, osc=ARCHIVE, entry=ARCHIVE, note=ARCHIVE, proof=T('Официальный отчёт организатора подтверждает шесть мест Junior / Senior и специальные награды; день финала в тексте не указан.', 'Informe oficial del organizador confirma seis puestos Junior / Senior y premios especiales; sin día del final en texto.'), language=LANG))
    rows.append(E('C1928', 'Mator Design · Robotics & AI Hackathon · year TBD', 'ZWE', MATOR, city='Media Centre · Bothwell House · 2nd floor · 1st / Jason Moyo · Harare', age='8–19', scope='local', themes=['robotics', 'ai', 'coding'], format=T('Команды по 3; можно сформировать на месте. Собрать двух братьев недостаточно; Оскар младше 8.', 'Equipos de 3; se pueden formar allí. Dos hermanos insuficientes; Oscar menor de 8.'), team_min=3, team_max=3, period=T('9–11 декабря, 09:00–15:30; ГОД НЕ УКАЗАН', '9–11 de diciembre, 09:00–15:30; AÑO SIN INDICAR'), mat=T('Условно: 9 входит в 8–19; год, язык и приём ещё неизвестны', 'Condicional: 9 dentro de 8–19; año, idioma y admisión desconocidos'), osc=T('Нет сейчас: минимум 8', 'No ahora: mínimo 8'), language=LANG, gear=T('Все необходимые kits предоставляет организатор; начальная micro-training без требования опыта. Еда и напитки свои.', 'Organizador proporciona kits necesarios; micro-training inicial sin experiencia exigida. Comida y bebida propias.'), cost=T('USD30 admission fee; единица за человека / команду и год цены не установлены. Нельзя автоматически умножать на двух детей.', 'USD30 admission fee; unidad por persona / equipo y año del precio sin establecer. Sin multiplicar automáticamente por dos niños.'), reward=T('Призы до USD100 в отдельных категориях; приз не обещан каждому. Национальная / мировая квота не опубликована.', 'Premios de hasta USD100 en categorías concretas; sin promesa para cada participante. Cupo nacional / mundial sin publicar.'), note=T('Ссылка Register now ведёт на общий контактный опрос, а не датированную заявку этого события. Copyright 2026 не доказывает год 9–11 декабря; даты в календарь не перенесены.', 'Enlace Register now lleva a consulta general de contacto, no inscripción fechada del evento. Copyright 2026 no acredita año del 9–11 de diciembre; fechas no trasladadas al calendario.'), entry=GATE))
    rows.append(E('C1929', 'Zimbabwe · Robotics for Good Youth Challenge preparation / next qualifier', 'ZWE', TME, age=T('Возраст не установлен; 16 в отчёте — число учеников', 'Edad sin establecer; 16 en informe es número de alumnos'), scope='national', language=LANG, entry=GATE, note=T('Отчёт 9 января 2026 описывает декабрьский лагерь 2025 в Oriel Boys High School и подготовку национального этапа в начале 2026. Следующие соревнования и лагерь 2026/27 не датированы. Название школьной площадки не является правилом возраста или пола участников.', 'Informe del 9 de enero de 2026 describe campamento de diciembre 2025 en Oriel Boys High School y preparación nacional a principios de 2026. Competición siguiente y campamento 2026/27 sin fecha. Nombre del colegio sede no constituye regla de edad o género.'), proof=T('Первичный отчёт TME Education о подготовке и сформированной команде; это не опубликованный новый регламент или открытая заявка.', 'Informe primario de TME Education sobre preparación y equipo formado; no reglamento nuevo publicado ni inscripción abierta.')))
    for number, p in enumerate(profiles, 559):
        e = E('L'+str(number), p['provider'], p['iso'], p['sources'][0]['url'], block='Лагеря', age=p['age'], themes=p['themes'], city=p['place'], period=p['timing']['label'], entry=GATE, note=p['programme'], proof=p['programme'], language=LANG, cost=p['price']['label'], participation='individual', admission_kind='unknown', scope='local', references=[dict(label=s['title'], url=s['url']) for s in p['sources']], mat=p['family_fit']['matvey']['detail'], osc=p['family_fit']['oscar']['detail'])
        e['mat'] = T('Нет сейчас; будущая ступень', 'No ahora; etapa futura') if p['family_fit']['matvey']['status']=='later' else e['mat']
        e['osc'] = T('Нет сейчас; будущая ступень', 'No ahora; etapa futura') if p['family_fit']['oscar']['status']=='later' else e['osc']
        rows.append(e)
    return rows

def add_history(d):
    h = d['school_history']
    entries = [
        ('ZWE-ZIMUTO', 'Zimuto High School', 'school', 'Зимбабве', 'Senior', '1st place', ZRO),
        ('ZWE-QUEEN-ELIZABETH', 'Queen Elizabeth High School · Zimbabwe', 'school', 'Зимбабве', 'Senior', '2nd place', ZRO),
        ('ZWE-PETRA-SENIOR', 'Petra College Senior', 'school', 'Зимбабве', 'Senior', '3rd place', ZRO),
        ('ZWE-DOMINICAN-PRIMARY', 'Dominican Convent Primary School', 'school', 'Зимбабве', 'Junior', '1st place', ZRO),
        ('ZWE-MASIYEPHAMBILI', 'Masiyephambili Junior College', 'school', 'Зимбабве', 'Junior', '2nd place', ZRO),
        ('ZWE-HELEN-MCGHIE', 'Helen McGhie Primary School', 'school', 'Зимбабве', 'Junior', '3rd place', ZRO),
        ('ZWE-CHIKATO', 'Chikato Primary School', 'school', 'Зимбабве', 'Special', 'Best Team Spirit', ZRO),
        ('ETH-KOTEBE', 'Kotebe STEM Center', 'club', 'Эфиопия', 'Future Innovators · national overall', '1st place', ECA),
        ('ETH-KALLAMINO', 'Kallamino STEM Center', 'club', 'Эфиопия', 'Future Innovators · national overall', '2nd place', ECA),
        ('ETH-AASTU', 'AASTU STEM Center', 'club', 'Эфиопия', 'Future Innovators · national overall', '3rd place', ECA),
        ('TZA-AZANIA', 'Azania Secondary School', 'school', 'Объединенная Республика Танзания', 'Future Innovators · national overall', 'Overall winner', ECA)]
    for eid, name, kind, country, category, award, source in entries:
        note = ARCHIVE + ' ' + T('Категория сохранена словами источника; числовой возраст, школьная ступень детей и текущая связь с командой отдельно не доказаны. STEM Center при университете не принят за постоянную школу. Одного сезона недостаточно для вывода о лидерстве за 5–10 лет.', 'Categoría conservada según fuente; edad numérica, etapa escolar de niños y relación actual con equipo sin acreditar aparte. STEM Center universitario no tomado como colegio permanente. Una temporada insuficiente para liderazgo de 5–10 años.')
        if not any(e['id']==eid for e in h['entities']):
            h['entities'].append(dict(id=eid, name=name, kind=kind, country=T(country, {'Зимбабве':'Zimbabue','Эфиопия':'Etiopía','Объединенная Республика Танзания':'Tanzania'}[country]), age=T('Историческая категория; текущий приём неизвестен', 'Categoría histórica; admisión actual desconocida'), note=note, school_id=None))
        next(e for e in h['entities'] if e['id']==eid).setdefault('school_id',None)
        if not any(r['entity_id']==eid and r['year']==2024 and r['award']==award for r in h['results']):
            h['results'].append(dict(id='H'+str(max(int(r['id'][1:]) for r in h['results'])+1).zfill(3), entity_id=eid, year=2024, league='WRO', category=category, stage='National Finals 2024', award=award, level='national_other', source=source, provenance='organizer_report' if source==ZRO else 'institutional_primary_report', team=name, team_id=None, note=note, checked=CHECKED))
    for r in h['results']:
        if r.get('source')==ECA:
            limitation=T('Отчёт ECA доступен в официальном поисковом представлении; прямые GET ссылок вернули HTTP 404. Архивная информация проверена по этому представлению, оригинал целиком не получен.', 'Informe ECA disponible en representación oficial de búsqueda; GET directos de enlaces devolvieron HTTP 404. Información histórica revisada mediante esa representación, sin original completo.')
            if limitation not in r['note']:r['note'] += ' ' + limitation
    h.update(version=182, checked=CHECKED, status='partial')

def enrich_v182(d):
    profiles=make_profiles(); rows=make_events(profiles); ids={e['id'] for e in rows}
    d['events']=[e for e in d['events'] if e['id'] not in ids]+rows
    for ident, name, eventids, url in [('wro-ethiopia-local','WRO · Ethiopia / STEMpower',['C1924','C1925'],STEM),('wro-zimbabwe-local','WRO · Zimbabwe / Girls in STEM Trust',['C1926','C1927'],GIST)]:
        ev=[e for e in rows if e['id'] in eventids]
        p=programme(ident,name,'regional',ev[0]['age'],['9','10-12','teen'],eventids,summary=ev[0]['note'],categories=[dict(name=e['title'],age=e['age'],entry=e['entry'],source=e['source'],event_id=e['id']) for e in ev],route=GATE,language=LANG,importance=T('Национальный маршрут WRO; новый отбор не объявлен', 'Ruta nacional WRO; selección nueva sin anunciar'),nuances=[ARCHIVE,ev[0]['note']],sources=[src(name,url)],evidence=ev[0]['proof'])
        d['league_guide']['profiles']=[x for x in d['league_guide']['profiles'] if x['id']!=ident]+[p]
    for r in d['national_routes']['routes']:
        if r['id'] not in ['NR-WRO-ETH','NR-WRO-ZWE','NR-FLL-ZWE-general']:
            continue
        r.update(website_checked=CHECKED, website_status='http_ok', access_url=STEM+'restricted-grants' if r['id']=='NR-WRO-ETH' else ZRO if r['id']=='NR-WRO-ZWE' else 'https://firstsa.org/')
        r['website_note'] = T('Официальная страница прочитана. История / общая программа подтверждены; местные категории нового сезона, индивидуальный иностранный приём и даты ещё нет.', 'Página oficial leída. Historia / programa general confirmados; categorías locales de temporada nueva, admisión individual extranjera y fechas aún no.')
    add_history(d)
    for c in d['countries']:
        if c['iso'] in ['ETH','ZWE']:
            c['coverage']=T('Частично: есть записи; полный местный аудит не завершён', 'Parcial: hay registros; auditoría local completa sin terminar')
    for e in rows:
        if e['source']==ECA:
            e['proof'] += ' ' + T('Прочитано официальное поисковое представление архива ECA; прямые GET вернули HTTP 404. Полный оригинал и текущая доступность ссылки не подтверждены.', 'Leída representación oficial de búsqueda del archivo ECA; GET directos devolvieron HTTP 404. Original completo y acceso actual al enlace sin confirmar.')
        if not any(s['url']==e['source'] for s in d['sources']):
            d['sources'].append(dict(title=e['title'], url=e['source'], evidence=e['proof'], checked=CHECKED))
    d['ethiopia_zimbabwe_v182']=dict(version=182, checked=CHECKED, new_competition_programme_rows=6, new_manual_learning_rows=11, new_camp_dossiers=11, new_league_profiles=2, new_history_results=11, refreshed_camp_dossiers=['CP720','CP737'], worldwide_complete=False, fully_audited_countries=0)
