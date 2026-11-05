"""ITR editions and virtual RoboLiga; preserve historical and entry boundaries."""
from copy import deepcopy
from datetime import date,timedelta

CHECKED='2026-11-04'
SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
ITR='https://internationaltournamentofrobots.org/'
FEES=ITR+'contribution/'
FORM='https://docs.google.com/forms/d/e/1FAIpQLSfYIltbcdyfuek-G3izwGE-NvLeBVSd4QdYE6piXhQBGVlvZw/viewform'
OLD_FEE='https://torneiojrobotica.org/CONTRIBUTE-2026-1/'
VIRTUAL='https://virtual.roboliga.ar/'
PHYSICAL_DOC='https://docs.google.com/document/d/1GLNQwzEIh--KUx2IyDM9K4zCRIIjYBCf7aDOea4ASgw/edit'
GUIDELINES='https://docs.google.com/presentation/d/18egdBVLDzlErVKysSlTuvoYiOtLnGrkePdxC1-lgZGc/edit'
FIT=T('Условно: возрастная группа выглядит возможной, но допуск выбранной дисциплины, младшего участника и иностранной независимой команды ещё подтвердить.',
      'Condicional: grupo de edad parece posible, pero confirmar disciplina elegida, integrante menor y equipo independiente extranjero.')
AGE=T('Общая текущая форма: Level 1 по возрасту старшего 6–11; остальные уровни отдельно. Минимум младшего не указан. Наградной BASIC в связанном документе требует всем 6–14; это другая группировка, её применимость к выбранному этапу уточнить.',
      'Formulario general actual: Level 1 según mayor de 6–11; otros niveles aparte. Mínimo del menor sin indicar. BASIC de premios en documento enlazado exige todos de 6–14; agrupación distinta, confirmar aplicación a etapa elegida.')
TEAM=T('2–4 ученика по общей форме, до 2 наставников по странице регистрации; независимая команда разрешена как INDEPENDENT TEAM. Для конкретной дисциплины подтвердить состав и возрастную отсечку.',
       '2–4 estudiantes según formulario general, hasta 2 mentores según página de registro; admite INDEPENDENT TEAM. Confirmar composición y corte de edad de disciplina concreta.')
HARDWARE=T('Обзор содержит 12 дисциплин, но точные размеры, масса и платформа зависят от актуального регламента категории. Старые связанные папки Rescue 2020 не считаются правилами нового сезона.',
           'Resumen contiene 12 disciplinas, pero dimensiones, masa y plataforma dependen de reglamento actual de categoría. Carpetas Rescue 2020 enlazadas no se consideran reglas de temporada nueva.')
ENTRY=T('Создать команду и робота в RoboLeague → действительная Performance Sheet и индекс эффективности → отдельная регистрация каждой дисциплины и этапа → согласовать взнос и допуск. Форма предлагает текущие этапы, но содержит старый текст об отборе 2023/2024; его квоты не переносятся на 2027.',
        'Crear equipo y robot en RoboLeague → Performance Sheet válida e índice de eficiencia → registro separado por disciplina y etapa → acordar cuota y admisión. Formulario ofrece etapas actuales, pero conserva texto de clasificación 2023/2024; no trasladar cuotas a 2027.')
LANG=T('Есть EN/ES/PT документы. Язык судейства, технического интервью и поддержки ребёнка на конкретном этапе не подтверждён.',
       'Existen documentos EN/ES/PT. Idioma de jueces, entrevista técnica y apoyo infantil en etapa concreta sin confirmar.')
AWARD=T('Место / награда только по официальному протоколу. Международное название ITR не означает финал WRO / FIRST / RoboCup. BASIC / ADVANCED наград и регистрационные Level 1–4 различаются.',
        'Puesto / premio solo según acta oficial. Nombre internacional ITR no implica final WRO / FIRST / RoboCup. BASIC / ADVANCED de premios difieren de Level 1–4 de registro.')
PRICE=T('Международный калькулятор: не менее 90 дней до события — 750 USD за команду / 50 USD за сопровождающего; 60–89 — 850 / 150; 15–59 — 950 / 250. Последний диапазон частично помечен provisional. Это чтение тарифа формы, не принятый счёт; набор, техника, жильё и поездка отдельно.',
        'Calculador internacional: al menos 90 días antes — 750 USD por equipo / 50 USD por acompañante; 60–89 — 850 / 150; 15–59 — 950 / 250. Último intervalo marcado parcialmente provisional. Lectura de tarifa del formulario, no factura aceptada; convocatoria, equipo, alojamiento y viaje aparte.')
REVIEW=T('Подтвердить именно местный регламент, возраст каждого ребёнка, независимый иностранный вход, Performance Sheet, валюту и итоговый счёт до оплаты.',
         'Confirmar reglamento local, edad de cada hijo, admisión extranjera independiente, Performance Sheet, moneda y factura final antes de pagar.')

def refs(items):return [dict(label=label,url=url) for label,url in items]
def event(ident,title,country,iso,city,url):
    return dict(id=ident,block='Соревнования',title=title,country=country,iso=[iso],region='Европа' if iso in ['ESP','PRT'] else 'Южная Америка',city=city,
        start='',end='',deadline='',period='',date_status='Даты не объявлены',age=AGE,mat=FIT,osc=FIT,format=TEAM,entry=ENTRY,gear=HARDWARE,
        language=LANG,languages=[],language_mode='unconfirmed',language_certainty=LANG,cost=PRICE,scope='international',
        level=T('Международный турнир организатора; не автоматический мировой финал','Torneo internacional del organizador; sin final mundial automático'),
        importance_reason=T('Редакционная оценка по правилам входа и полезности практики; независимый мировой рейтинг не установлен.',
                            'Valoración editorial por acceso y utilidad práctica; clasificación mundial independiente sin acreditar.'),
        reward=AWARD,priority='P2 — '+T('после подтверждения категории и бюджета','tras confirmar categoría y presupuesto'),action=REVIEW,
        source=url,references=[],proof='',checked=CHECKED,status='Идея',note='',themes=['robotics'],participation='team',admission_kind='open_application',evidence_level='event_page')

def enrich_v145(d):
    idx={e['id']:e for e in d['events']}
    brazil=idx['C066'];brazil.update(age=AGE,mat=FIT,osc=FIT,format=TEAM,entry=ENTRY,gear=HARDWARE,language=LANG,languages=[],language_mode='unconfirmed',
        language_certainty=LANG,checked=CHECKED,deadline='2026-11-15',deadline_label=T('Performance Sheet · предварительный допуск','Performance Sheet · admisión previa'),
        deadline_note=T('Страница взносов 2026 требует действительную Performance Sheet с ненулевым индексом до 15 ноября. В калькуляторе закрытие оплаты вычисляется за 15 дней до 5 декабря, то есть 20 ноября; час неизвестен. Это разные условия, а не один дедлайн.',
                        'Página de cuotas 2026 exige Performance Sheet válida e índice no nulo hasta 15 de noviembre. Calculador cierra pago 15 días antes de 5 de diciembre, es decir 20 de noviembre; hora desconocida. Condiciones diferentes, no único plazo.'),
        cost=T('Текущий международный калькулятор даёт на дату проверки 950 USD за команду и 250 USD за сопровождающего. Связанная старая страница даёт 350 / 80 со знаком $ на ноябрь; код валюты не указан. Таблица BRL тоже расходится по датам и суммам. Итоговый счёт и применимость квоты подтвердить письменно; оплату не проводили.',
               'Calculador internacional actual da en fecha de revisión 950 USD por equipo y 250 USD por acompañante. Página antigua enlazada da 350 / 80 con símbolo $ para noviembre; sin código monetario. Tabla BRL también discrepa en fechas e importes. Confirmar factura y cuota aplicable por escrito; sin efectuar pago.'),
        action=REVIEW,registration_url=FORM,registration_status=T('Форма доступна; место и допуск семьи не подтверждены. RoboLeague — обязательная предварительная ступень.',
                                                                'Formulario disponible; plaza y admisión familiar sin confirmar. RoboLeague es paso previo obligatorio.'),
        proof=T('Дату 5 декабря 2026 подтверждают отдельная страница Brazil, общий регистрационный список и калькулятор. Прочитаны общее возрастное правило, независимый вход и обязательная Performance Sheet. Технический регламент конкретной категории ещё нужен.',
                'Fecha de 5 de diciembre de 2026 confirmada por página Brazil, lista general y calculador. Leídos regla general de edad, admisión independiente y Performance Sheet obligatoria. Falta reglamento técnico de categoría concreta.'),
        note=T('São Paulo · Convention Center Novotel Center Norte. В форме регистрационные уровни и наградные группы не тождественны. Полный комплект технических правил 2026 ещё не установлен; не применять параметры файлов 2020 автоматически.',
               'São Paulo · Convention Center Novotel Center Norte. Niveles de registro y grupos de premios no son equivalentes. Reglamento técnico completo 2026 sin acreditar; no aplicar automáticamente parámetros de archivos 2020.'),
        team_min=2,team_max=4,references=refs([(T('Текущая международная форма оплаты','Formulario internacional actual de cuotas'),FEES),
             (T('Связанная альтернативная таблица 2026','Tabla alternativa 2026 enlazada'),OLD_FEE),(T('Общая форма: уровни и независимые команды','Formulario general: niveles y equipos independientes'),FORM)]))
    brazil.pop('deadline_utc',None)
    new=[]
    for ident,slug,title,country,iso,city,start,end in [
        ('C1190','SPAIN','ITR Spain 2027 · Barcelona','Испания','ESP','Barcelona · Hyatt Regency Barcelona Tower','2027-02-20','2027-02-21'),
        ('C1191','ARGENTINA','ITR Argentina 2027 · Buenos Aires','Аргентина','ARG','Buenos Aires · Hilton Buenos Aires','2027-05-01','2027-05-01'),
        ('C1192','PORTUGAL','ITR Portugal 2027 · Lisboa','Португалия','PRT','Lisboa · Novotel Lisboa','2027-06-19','2027-06-20')]:
        e=event(ident,title,country,iso,city,ITR+slug+'/');closing=(date.fromisoformat(start)-timedelta(days=15)).isoformat()
        e.update(start=start,end=end,date_status='Подтверждено',date_scope='festival_window',deadline=closing,
            deadline_label=T('По правилу калькулятора · закрытие за 15 дней','Según regla del calculador · cierre 15 días antes'),
            deadline_note=T(f'{closing} вычислено от первого дня этапа по опубликованному коду формы, не отдельное письмо организатора. Точный час не указан; отдельный срок Performance Sheet этого этапа уточнить.',
                            f'{closing} calculado desde primer día según código publicado del formulario, no correo específico del organizador. Hora sin indicar; confirmar plazo propio de Performance Sheet.'),
            team_min=2,team_max=4,registration_url=FORM,registration_status=brazil['registration_status'],
            proof=T('Прочитаны отдельная страница страны, текущие варианты общей формы и тарифный калькулятор. Для двухдневных этапов использованы обе даты страницы страны; калькулятор хранит только первый день.',
                    'Leídas página nacional, opciones actuales de formulario general y calculador. Para etapas de dos días se usan ambas fechas de página nacional; calculador solo guarda primer día.'),
            note=T('Общие возрастные уровни и BASIC / ADVANCED наград не взаимозаменяемы. Связанные инструкции содержат исторические блоки 2024/2025; применимость к этой редакции подтвердить. Место, язык и конкретный challenge не считаются принятым участием.',
                   'Niveles generales de edad y BASIC / ADVANCED de premios no son intercambiables. Instrucciones enlazadas contienen bloques históricos 2024/2025; confirmar aplicación a esta edición. Plaza, idioma y challenge concreto no equivalen a participación aceptada.'),
            references=refs([(T('Калькулятор: даты и международные тарифы','Calculador: fechas y tarifas internacionales'),FEES),
                (T('Регистрация и возрастные уровни','Registro y niveles de edad'),FORM),(T('Связанные дополнительные правила; проверить сезон','Directrices complementarias enlazadas; comprobar temporada'),GUIDELINES)]))
        if iso=='ESP':
            e['cost']+=' '+T('Локальная ссылка Spain даёт 820 EUR за команду / 120 EUR за сопровождающего за период 03.02–30.08.2026; это другой период и валюта, не текущий подтверждённый счёт.',
                             'Enlace local Spain da 820 EUR por equipo / 120 EUR por acompañante para periodo 03.02–30.08.2026; periodo y moneda distintos, no factura actual confirmada.')
            e['references'].append(dict(label=T('Локальная таблица Spain с прошедшим периодом оплаты','Tabla local Spain con periodo de pago ya pasado'),url='https://torneiojrobotica.org/CONTRIBUTE-ITR-SPAIN-2027/'))
            e['note']+=' '+T('20–21 февраля совпадает с WRL Korea 19–21 февраля; две полные поездки одновременно не совместить.',
                             '20–21 de febrero coincide con WRL Korea 19–21 de febrero; no se pueden combinar ambos viajes completos simultáneamente.')
        new.append(e)
    team=T('2026: 1–4 участника, можно одному; школа не обязательна по FAQ. Следующий набор и согласие взрослого уточняются.',
           '2026: 1–4 integrantes, se admite uno; colegio no obligatorio según FAQ. Confirmar próxima convocatoria y consentimiento adulto.')
    foreign=T('Rescate 2026 прямо приветствует участников всех стран и возрастов. Сборная Аргентины для RoboCup — другой отбор: аргентинская команда по условиям организатора, возраст 13–18 на 01.07.2026, более 50% взвешенного результата, финальная индивидуальная очная задача в CABA. Семье не обещан этот национальный путь.',
              'Rescate 2026 acoge expresamente participantes de todos los países y edades. Selección argentina para RoboCup es otra vía: equipo argentino según condiciones del organizador, edad 13–18 al 01.07.2026, más de 50% del resultado ponderado, tarea final individual presencial en CABA. Sin prometer esta vía nacional a la familia.')
    virtual_language=T('Опубликованные правила и организационные материалы — на испанском. Игра оценивается программно; язык живой помощи и отдельного очного отбора подтвердить.',
                       'Reglas y materiales organizativos publicados en español. Juego evaluado por software; confirmar idioma de ayuda en vivo y selección presencial aparte.')
    virtual_award=T('Результат виртуальной дисциплины подтверждается протоколом. Участие, победа в виртуальном этапе и допуск в национальную сборную RoboCup — разные результаты.',
                    'Resultado virtual se acredita por acta. Participación, victoria en etapa virtual y selección nacional RoboCup son resultados distintos.')
    virtual_urls=[(T('Текущий сезон и возрастные рамки','Temporada actual y edades'),VIRTUAL),
        (T('FAQ: бесплатно, индивидуально и без школы','FAQ: gratis, individual y sin colegio'),VIRTUAL+'faq.html'),
        (T('Расписание раундов 2026','Calendario de rondas 2026'),VIRTUAL+'calendario.html'),
        (T('Sumo: полный возрастной и технический регламент','Sumo: reglamento completo de edad y técnica'),VIRTUAL+'reglamentos_sumo.html'),
        (T('Rescate: международный вход и отдельный национальный отбор','Rescate: admisión internacional y selección nacional separada'),VIRTUAL+'reglamentos_rescate.html')]
    past=T('Объявленный срок регистрации 2026 — 4 сентября 23:59 UTC−3 — прошёл; текущий список раундов относится к уже отобранным командам. Поздний вход не объявлен.',
           'Plazo anunciado de inscripción 2026 — 4 de septiembre 23:59 UTC−3 — vencido; lista de rondas actual corresponde a equipos clasificados. Admisión tardía sin anunciar.')
    for ident,kind,start,end,rounds,gear in [
        ('C1193','Sumo','2026-09-26','2026-11-07','26.09, 10.10, 31.10, 07.11',
          T('Webots R2023b, Python 3.12+ либо редактор блоков. Стандартный робот: 2 датчика дистанции, 1 цвета, 2 касания сзади, 2 мотора; можно менять позицию / поворот разрешённых датчиков. Подача одного .py и, при кастомизации, одного .json.',
            'Webots R2023b, Python 3.12+ o editor de bloques. Robot estándar: 2 sensores de distancia, 1 de color, 2 de contacto trasero, 2 motores; admite cambiar posición / giro de sensores autorizados. Entrega de un .py y, si personalizado, un .json.')),
        ('C1194','Fútbol','2026-09-19','2026-10-17','19.09, 26.09, 03.10, 10.10, 17.10',
          T('Симуляция: 3 автономных робота на стороне, один тайм 3:30 минуты, автоматический судья; языки программирования по среде. Свой компьютер, физический робот не нужен.',
            'Simulación: 3 robots autónomos por equipo, un tiempo de 3:30 minutos, árbitro automático; lenguajes según entorno. Ordenador propio, sin robot físico.')),
        ('C1195','Rescate','2026-09-19','2026-10-31','19.09, 03.10, 17.10, 31.10',
          T('Erebus v26.1; Python, исходники, библиотеки и структура робота .json одним ZIP, без исполняемых файлов. По 2 раунда на дату; для отбора учитывают 7 лучших из 8.',
            'Erebus v26.1; Python, fuentes, bibliotecas y estructura .json en un ZIP, sin ejecutables. 2 rondas por fecha; selección toma mejores 7 de 8.'))]:
        e=event(ident,'RoboLiga Virtual 2026 · '+kind,'Аргентина','ARG',T('Онлайн из своего места подготовки','En línea desde lugar propio de preparación'),VIRTUAL)
        age=T('Общие Fútbol / Rescate — все возрасты. Sumo Infantil: каждому не менее 9 и старшему не более 12 на 01.07.2026; Juvenil старший до 18; Libre без возрастного ограничения. Календарь 2026 объединил все Sumo в одну сетку.',
              'Fútbol / Rescate generales: todas las edades. Sumo Infantil: todos al menos 9 y mayor máximo 12 al 01.07.2026; Juvenil mayor hasta 18; Libre sin límite. Calendario 2026 unificó todos los Sumo en una llave.')
        e.update(start=start,end=end,date_status='Подтверждено',date_scope='festival_window',deadline='2026-09-04',deadline_utc='2026-09-05T02:59:00Z',
            deadline_label=T('Набор 2026 завершён','Inscripción 2026 terminada'),deadline_note=past,age=age,mat=FIT,osc=FIT,format=team,
            participation='individual_or_team',gear=gear,entry=past+' '+foreign,cost=T('В FAQ сезон 2026 бесплатен; свой компьютер и интернет. Тариф нового сезона ещё неизвестен.',
            'FAQ declara temporada 2026 gratuita; ordenador e internet propios. Tarifa de temporada nueva aún desconocida.'),
            level=T('Виртуальное соревнование / практика; отдельный национальный маршрут','Competición / práctica virtual; vía nacional aparte'),reward=virtual_award,
            language=virtual_language,language_certainty=virtual_language,
            priority='P4 — '+T('обычный набор 2026 завершён; история и тренировка','convocatoria ordinaria 2026 terminada; historial y práctica'),
            action=T('Использовать опубликованные задания для подготовки; ждать объявления нового набора. Discord и передачу файлов организует взрослый наставник.',
                     'Usar retos publicados para preparación; esperar nueva convocatoria. Mentor adulto gestiona Discord y archivos.'),
            note=T(f'Даты раундов: {rounds}. Диапазон в календаре не означает ежедневное участие. У Sumo четвертьфинал в ноябре без точной даты; национальный финал Rescate тоже TBA.',
                   f'Fechas de rondas: {rounds}. Intervalo de calendario no implica participación diaria. Cuartos Sumo en noviembre sin día exacto; final nacional Rescate también TBA.'),
            proof=T('Прочитаны текущие HTML правила, календарь, FAQ и условия национального отбора. Игровой код и бинарные пакеты не запускались.',
                    'Leídos reglamentos HTML actuales, calendario, FAQ y selección nacional. Sin ejecutar código de juego ni paquetes binarios.'),
            references=refs(virtual_urls),availability=dict(status='closed',note=past),registration_status=past,admission_kind='open_application',evidence_level='rules')
        if kind=='Fútbol':
            e['age']=T('2026: общая категория для всех возрастов; следующий набор проверяется отдельно.',
                       '2026: categoría general para todas las edades; próxima convocatoria se comprueba aparte.')
        elif kind=='Rescate':
            e['age']=T('2026: все возрасты и участники всех стран. Отбор сборной Аргентины требует 13–18 на 01.07.2026 и дополнительных условий.',
                       '2026: todas las edades y países. Selección argentina exige 13–18 al 01.07.2026 y condiciones adicionales.')
        new.append(e)
    watch=event('C1196',T('RoboLiga Virtual · следующий набор и домашняя подготовка','RoboLiga Virtual · próxima convocatoria y preparación en casa'),'Аргентина','ARG',
        T('Онлайн; новые международные условия уточняются','En línea; condiciones internacionales nuevas por confirmar'),VIRTUAL)
    watch.update(age=T('Новый набор ещё не объявлен; возраст 2026 служит историей, не правилом будущего сезона.',
                       'Convocatoria nueva aún sin anunciar; edades 2026 son historia, no reglas de temporada futura.'),
        format=team,participation='individual_or_team',language=virtual_language,language_certainty=virtual_language,reward=virtual_award,gear=T('Последний опубликованный набор: Webots / Python и блоки для Sumo, футбол и Erebus Rescue. Совместимость компьютера и актуальную версию нового сезона проверить.',
            'Última convocatoria publicada: Webots / Python y bloques Sumo, fútbol y Erebus Rescue. Confirmar ordenador y versión de temporada nueva.'),
        entry=foreign,cost=T('FAQ 2026: бесплатно; условия следующего набора и собственная техника отдельно.',
                            'FAQ 2026: gratis; condiciones de próxima convocatoria y equipo propio aparte.'),
        priority='P3 — '+T('новые даты и условия ещё не объявлены','fechas y condiciones nuevas aún sin anunciar'),
        action=T('Практиковать блоки → Python, журнал версий и повторяемые тесты; следить за новым набором и возрастной отсечкой. Ребёнок пишет и объясняет собственный код.',
                 'Practicar bloques → Python, versiones y pruebas repetibles; seguir convocatoria y corte de edad nuevos. Niño escribe y explica código propio.'),
        note=T('Это путь подготовки, не открытая регистрация. Матвею может понадобиться уже 9-летие к фиксированной отсечке; Оскару в предыдущем Infantil нельзя, но существовала Libre и общие дисциплины.',
               'Vía de preparación, no registro abierto. Matvey podría necesitar cumplir 9 antes de corte fijo; Oscar no entra en anterior Infantil, pero existían Libre y disciplinas generales.'),
        references=refs(virtual_urls),proof=foreign,registration_status=T('Следующий сезон не объявлен.','Próxima temporada sin anunciar.'))
    new.append(watch)
    mexico=event('C1197',T('ITR Mexico 2028 · Cancún · даты расходятся','ITR Mexico 2028 · Cancún · fechas discrepantes'),'Мексика','MEX','Cancún · Hotel Hyatt Ziva Cancun',ITR+'MEXICO/')
    mexico.update(region='Северная Америка',priority='P3 — '+T('две разные даты источников','dos fechas distintas de fuentes'),
        period=T('Страница México: 29–30 апреля 2028; калькулятор: 1 апреля 2028. До разрешения противоречия календарной даты нет.',
                 'Página México: 29–30 de abril de 2028; calculador: 1 de abril de 2028. Sin fecha de calendario hasta resolver discrepancia.'),
        cost=T('Тариф и срок нельзя надёжно рассчитать при разных исходных датах; требуется подтверждение редакции и счёта.',
               'Tarifa y plazo no se pueden calcular con fiabilidad con fechas de origen distintas; confirmar edición y factura.'),
        note=T('Это дальний ориентир для мексиканской базы семьи. Не перенесён на 2027 и не добавлен в ICS как подтверждённая смена или соревнование.',
               'Referencia lejana para base mexicana de familia. Sin trasladar a 2027 ni añadir al ICS como sesión o competición confirmada.'),
        proof=T('Свежие страница страны и код калькулятора прочитаны отдельно; несовпадение дат сохранено явно.',
                'Leídas por separado página nacional y código del calculador actuales; discrepancia de fechas conservada explícitamente.'),
        references=refs([(T('Калькулятор с другой исходной датой','Calculador con otra fecha inicial'),FEES)]))
    new.append(mexico)
    chile=event('C1198',T('ITR Chile 2026 · Santiago · архив','ITR Chile 2026 · Santiago · archivo'),'Чили','CHL','Santiago · Hotel Almacruz',ITR+'CHILE/')
    chile.update(start='2026-09-05',end='2026-09-06',date_status='Подтверждено',date_scope='festival_window',
        priority='P4 — '+T('прошедший этап; следующий ещё не объявлен','etapa pasada; siguiente aún sin anunciar'),
        cost=T('Исторический тариф этого этапа не проверен; текущие международные цены не переносятся на прошедший сезон.',
               'Tarifa histórica de esta etapa sin verificar; precios internacionales actuales no se trasladan a temporada pasada.'),
        entry=T('Архив 2026; набор на будущий Chile ещё не подтверждён. Не повторять эти даты в 2027 автоматически.',
                'Archivo 2026; convocatoria futura Chile aún sin confirmar. No repetir automáticamente estas fechas en 2027.'),
        proof=T('На отдельной странице страны явно указаны 2026, 5–6 сентября и Hotel Almacruz.',
                'Página nacional indica expresamente 2026, 5–6 de septiembre y Hotel Almacruz.'),
        note=T('Историческая география международной серии; не активная возможность регистрации.',
               'Geografía histórica de serie internacional; no oportunidad activa de inscripción.'),
        action=T('Следить за следующим чилийским анонсом и новым регламентом.','Seguir próximo anuncio chileno y reglamento nuevo.'))
    new.append(chile)
    for e in new:
        if e['id'] in idx:idx[e['id']].update(e)
        else:d['events'].append(e);idx[e['id']]=e
    expired=T('Регламент 2026 по-прежнему указывает 31 октября для команд; срок прошёл, продление не объявлено. Поздний соревновательный допуск требует отдельного подтверждения.',
              'Reglamento 2026 sigue indicando 31 de octubre para equipos; plazo vencido, prórroga sin anunciar. Admisión competitiva tardía requiere confirmación aparte.')
    for ident in range(663,674):
        e=idx['C'+str(ident)];e.update(checked=CHECKED,registration_status=expired,action=expired)
    visitor=idx['E048'];visitor.update(checked=CHECKED,deadline='2026-11-07',deadline_label=T('Заявка посетителя','Solicitud de visitante'),
        deadline_note=T('Свежий регламент отдельно устанавливает 7 ноября 2026 для посетителей. Час не указан; это не срок регистрации команды.',
                        'Reglamento actual fija por separado 7 de noviembre de 2026 para visitantes. Hora sin indicar; no es plazo del equipo.'),
        registration_url='https://forms.gle/a9T2JSGjALnhoho38',entry=T('Прямая форма посетителя до 7 ноября допускает родственников и независимых посетителей, взрослых и несовершеннолетних. Каждый родитель и каждый ребёнок регистрируются отдельно. Исключение с количеством учеников в заявке взрослого относится к педагогам / директорам со школьной группой.',
          'Formulario directo hasta 7 de noviembre admite familiares y visitantes independientes, adultos y menores. Cada padre y cada hijo se registra por separado. Excepción de cantidad de alumnos en solicitud adulta corresponde a docentes / directivos con grupo escolar.'),
        age=T('Форма явно допускает взрослых и несовершеннолетних посетителей; отдельная запись каждого. Ограничение возрастов соревнования к посетителям не применяется автоматически.',
              'Formulario admite expresamente visitantes adultos y menores; inscripción separada por persona. Edades competitivas no se aplican automáticamente a visitantes.'),
        mat=T('Да как посетитель по форме; запись и фактический вход отдельно.','Sí como visitante según formulario; inscripción y entrada efectiva aparte.'),
        osc=T('Да как посетитель по форме; запись и фактический вход отдельно.','Sí como visitante según formulario; inscripción y entrada efectiva aparte.'),
        visitor_policy='family',visitor_policy_note=T('Прямая форма прямо упоминает несовершеннолетних и семейных посетителей. Это доступ зрителя, не соревновательный допуск.',
            'Formulario directo menciona expresamente menores y visitantes familiares. Acceso de público, no admisión competitiva.'),
        priority='P2 — '+T('семейное посещение после подтверждения заявки','visita familiar tras confirmar solicitud'),
        proof=T('Прочитаны текущий регламент, Agenda 2026 и прямая форма посетителей. Форма явно различает школьные делегации и индивидуально заявленных родственников / независимых посетителей, включая несовершеннолетних.',
                'Leídos reglamento actual, Agenda 2026 y formulario directo de visitantes. Formulario distingue delegaciones escolares y familiares / visitantes independientes inscritos individualmente, incluidos menores.'),
        note=T('В Feria посетителей пускают с 09:00; с 08:00 только делегации экспонентов. Стоимость входа не опубликована; заявка не подтверждённый билет и не участие в соревновании.',
               'Feria admite visitantes desde 09:00; desde 08:00 solo delegaciones expositoras. Precio de entrada sin publicar; solicitud no equivale a entrada confirmada ni competición.'),
        references=refs([(T('Свежий регламент с отдельным сроком посетителей','Reglamento actual con plazo propio de visitantes'),PHYSICAL_DOC),
                         (T('Прямая форма посетителей из регламента','Formulario directo de visitantes del reglamento'),'https://forms.gle/a9T2JSGjALnhoho38'),
                         (T('Agenda 2026: вход с 09:00','Agenda 2026: entrada desde 09:00'),'https://roboliga.edu.ar/edicion-2026/agenda.asp')]))
    guide=d['league_guide'];itr=next(g for g in guide['profiles'] if g['id']=='itr')
    itr.update(name=T('ITR · международная серия TJR / RoboLeague','ITR · serie internacional TJR / RoboLeague'),group='international',age_summary=AGE,age_tags=['6','9','10-12','teen'],summary=ENTRY,route=ENTRY,hardware=HARDWARE,language=LANG,
        strengths=T('Международные очные этапы и измеряемая предварительная работа робота в RoboLeague.',
                    'Etapas presenciales internacionales y pruebas previas medibles del robot en RoboLeague.'),cost=PRICE,award=AWARD,
        requirements=[TEAM,REVIEW],nuances=[AGE,T('Общая форма содержит старые квоты 2023/2024, технические папки — материалы 2020. Исторические блоки не доказывают действующие правила каждого этапа.',
            'Formulario general conserva cuotas antiguas 2023/2024, carpetas técnicas materiales 2020. Bloques históricos no acreditan reglas vigentes por etapa.')],
        evidence=T('Прочитаны текущие страницы стран, общая форма, код тарифного калькулятора и связанные инструкции; противоречия сохранены явно.',
                   'Leídas páginas nacionales actuales, formulario general, código del calculador y directrices; discrepancias conservadas explícitamente.'))
    itr['event_ids']=list(dict.fromkeys(itr['event_ids']+['C1190','C1191','C1192','C1197','C1198']))
    itr['categories']=[dict(name=idx[i]['title'],age=idx[i]['age'],age_rule=T('У регистрационного Level 1 проверяется старший; у наградного BASIC — каждый участник. Точную отсечку и применимую редакцию уточнить.',
         'En Level 1 de registro se comprueba el mayor; en BASIC de premios, cada integrante. Confirmar corte exacto y edición aplicable.'),team=idx[i]['format'],hardware=idx[i]['gear'],entry=idx[i]['entry'],event_id=i) for i in itr['event_ids']]
    itr['sources']=[dict(title=label,url=url,checked=CHECKED) for label,url in [(T('Текущая форма и тарифы','Formulario y tarifas actuales'),FEES),(T('Возраст, уровни и независимые команды','Edades, niveles y equipos independientes'),FORM)]+[(idx[i]['title'],idx[i]['source']) for i in itr['event_ids']]]
    g=dict(id='roboliga-virtual',name='RoboLiga Virtual',group='regional',age_summary=idx['C1193']['age']+' '+watch['age'],age_tags=['6','9','10-12','teen'],summary=foreign,
        categories=[dict(name=idx[i]['title'],age=idx[i]['age'],age_rule=T('Правила 2026 и возраст на указанную фиксированную дату; следующий набор не подтверждён. Национальный отбор имеет отдельные условия.',
             'Reglas 2026 y edad en fecha fija indicada; próxima convocatoria sin confirmar. Selección nacional tiene condiciones propias.'),team=team,hardware=idx[i]['gear'],entry=idx[i]['entry'],event_id=i) for i in ['C1193','C1194','C1195','C1196']],
        event_ids=['C1193','C1194','C1195','C1196'],legacy_ids=[],route=watch['action'],hardware=watch['gear'],language=virtual_language,importance=itr['importance'],strengths=team,
        requirements=[team,foreign],nuances=[past,idx['C1193']['age']],cost=watch['cost'],award=virtual_award,
        sources=[dict(title=label,url=url,checked=CHECKED) for label,url in virtual_urls],evidence=idx['C1193']['proof'])
    existing=next((x for x in guide['profiles'] if x['id']==g['id']),None)
    if existing:existing.update(g)
    else:guide['profiles'].append(g)
    guide['version']=145
    urls={s['url'] for s in d['sources']}
    for e in [brazil,visitor]+new:
        for ref in [dict(url=e['source'],label=e['title'])]+e['references']:
            if ref['url'] not in urls:d['sources'].append(dict(url=ref['url'],title=ref['label'],evidence='official-primary',checked=CHECKED));urls.add(ref['url'])
