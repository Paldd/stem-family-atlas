"""Singapore family AI and nature programmes, plus a scoped Tokyo tariff correction."""
from collections import Counter
from pathlib import Path
from camp_planning_v108 import offer

ROOT=Path(__file__).resolve().parents[1]
BASE='b8fc7cddebbc41010819181352b1ebf0008e3ac6'
CHECKED='2026-10-06'
HOME='https://www.edutechfuture.com/'
PROGRAMS='https://www.edutechfuture.com/genaiprograms'
COURSE='https://www.edutechfuture.com/challenge-page/kids-ai-camp?programId=8ccdee9d-d2d2-4d8b-9a47-efcd11e5f720'
INDUSTRY='https://www.sginnovate.com/event/build-global-ai-product-singapore-6th-kids-ai-industry-immersion-camp-ages-7-15-and-parents'
KIDS='https://www.sginnovate.com/event/kids-ai-weekend-camp-responsible-ai-curious-young-minds-ages-6-10'
TEENS='https://www.sginnovate.com/event/kids-teens-ai-weekend-camp-build-your-first-responsible-ai-agent-ages-11-15'
NATURE='https://www.camp-challenge.com/nature-quest-kids-holiday-camp/'
GST='https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/basics-of-gst/goods-and-services-tax-(gst)-what-it-is-and-how-it-works'
AYLA='https://www.aylais.com/camp-ayla'
NEW=['edutech-industry-six','edutech-family-ideathon','edutech-tweens-weekend','camp-challenge-nature-quest']
ASK='Подтвердить место, точную возрастную группу, приём приезжей семьи, язык преподавания и полный договор/счёт. Сообщения, заявки и оплаты не выполнялись.'

def add_asia_v134(add,src,fit,profiles):
    def emit(i,name,themes,formats,place,age,lang,programme,dates,price,housing,mf,of,sources,status='next_unannounced',sessions=None):
        add(NEW[i],name,'Сингапур','SGP',place,themes,formats,age,lang,programme,dates,price,housing,mf,of,
            'Редакционный кандидат по содержанию опубликованной программы; собственная реклама не независимый мировой рейтинг.',[ASK],sources,
            status=status,sessions=sessions or [])
        p=profiles[-1];p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
        return p
    unknown='Язык преподавания (EN/ES/RU) прямо не установлен. Англоязычная страница, международные спикеры и интерфейс AI-инструментов не заменяют подтверждение языка конкретного занятия.'
    price=dict(year=2026,label='Каталог/курс показывает $1 500; SGInnovate публикует S$200–1 500 для flexible attendance. Какой тариф относится к взрослому, ребёнку, одному дню и полному пакету, ещё не разъяснено.',
        unit='unconfirmed',
        included='Страница курса заявляет curriculum, две mentor rounds, welcome gift, certificate, транспорт программы и питание (lunches/dinners/coffee breaks). Это собственное описание включений; точный пакет и часы отдельно.',
        extras='Перелёт, жильё семьи, дорога к площадке, налог, устройства/accounts, страховка и семейная цена не установлены. Family/friends discount заявлен без формулы; две детские цены автоматически не складываются.',
        deposit='Курс пишет registration AND payment до 15 ноября 2026; сроки депозита/отмены и полный invoice неизвестны. SGInnovate предупреждает, что изменения организатора ещё не прошли его review.')
    p=emit(0,'EDUTech Future · 6th Kids AI Industry Immersion', 'ai,coding,entrepreneurship','day,family',
        'Singapore · ACE Ideation/Innovation Centre · 79 Ayer Rajah Crescent #01-13 + выезды', '7–15; родители и члены семьи отдельно',unknown,
        'Два AI-прототипа (индивидуальный и командный), проблема/клиент/цена/pitch, обратная связь, responsible design, две mentor rounds и три learning journeys. Lovable, Google AI Studio, Claude; начинающий уровень. Организатор заявляет встречи с технологическими компаниями и Enabling Village. Заявленная 3-часовая RSAF/RAiD поездка требует подтверждения допуска иностранцев. Внутреннее жюри не мировая медаль.',
        '21–26 ноября 2026, шесть последовательных дней, включая субботу и воскресенье. Заявлено 48,5 часов с присмотром; ежедневные часы не опубликованы. Registration/payment до 15 ноября; набор 2027 ещё не объявлен.',price,
        'Дневная программа с выездами; семейное участие разрешено, лагерный пансион не заявлен.',
        fit('conditional','В ноябре 2026 возраст 8–9 входит в 7–15; точный младший поток, сложность, язык и приём иностранцев подтвердить.'),
        fit('later','Оскару 5–6: полный лагерь 7–15 пока не подходит. Отдельный семейный Ideathon для 5–6 с родителями рассматривается в другом досье; его допуск не переносится на все шесть дней.'),
        [src('Собственная страница курса: состав, включения, deadline и младший Ideathon',COURSE),src('SGInnovate: даты, 7–15, 48,5h, S$range и pending organizer review',INDUSTRY),src('Собственный каталог: $1500',PROGRAMS)],
        status='published_2026',sessions=[['2026-11-21','2026-11-26']])
    p['timing']['session_details']=[dict(start='2026-11-21',end='2026-11-26',label='Шесть дней · суббота–четверг · часы уточнить',price=price['label'],place=p['place'],source=COURSE,date_scope='camp_session',
        deadline='2026-11-15',entry='Открытая заявка на лагерь 7–15 с family attendance; scope иностранного участия и выездов отдельно.',proof='Own course + SGInnovate текущая редакция; visitor place не подтверждён.')]
    p=emit(1,'EDUTech Future · 5th Family AI Ideathon · младший компонент','ai,entrepreneurship','family,day','Singapore · площадка отдельного Ideathon ещё не установлена',
        '5–6 только с родителями; возраст других потоков отдельно',unknown,
        'Семейное придумывание AI-решения и командная презентация родителям/сверстникам/жюри. Собственная страница полного лагеря отдельно допускает младших builders с родителями; это не право посещать шестидневный лагерь 7–15.',
        'Ideathon входит в неделю 21–26 ноября 2026. Точный день, часы, продолжительность и отдельная регистрация не опубликованы; окно недели не превращено в календарную смену.',
        dict(year=2026,label='Отдельная цена для ребёнка 5–6 и родителя неизвестна. Диапазон S$200–1500 полного мероприятия сюда не назначен.',
            included='Заявлены работа в команде и презентация; отдельное включение питания/транспорта/материалов уточнить.',extras='Жильё семьи/дорога/страховка и полный семейный счёт неизвестны.',deposit='Общий course deadline 15 ноября; применимость к отдельному Ideathon и отмена ещё нужны.'),
        'Родитель участвует вместе с младшим ребёнком; самостоятельного пансиона нет.',
        fit('unknown','Матвей 8–9 старше названного младшего потока 5–6. Может рассмотреть полный 7–15; возраст смешанной семейной команды и доступ к отдельному Ideathon ещё неизвестны.'),
        fit('conditional','Оскар 5–6 в ноябре 2026 входит в явно названный младший компонент только с родителем. Точный день, места, язык и пакет ещё нужно подтвердить.'),
        [src('Собственный курс: именно 5th Family AI Ideathon допускает 5–6 с родителями',COURSE)],status='published_2026',sessions=[['2026-11-21','2026-11-26']])
    p['timing']['precision']='season_window'
    emit(2,'EDUTech Future · AI for Tweens · weekend classes','ai,coding,entrepreneurship','day','Singapore · onsite по согласованию; точный адрес не указан',
        '9–14',unknown,'Двухчасовые customised занятия AI на выходных, rolling enrolment. Детальный syllabus именно этой группы не опубликован; шестидневный programme не перенесён на каждое занятие.',
        'Октябрь–декабрь 2026: двухчасовые занятия на выходных с текущим набором. Даты отдельных занятий неизвестны. Срок октябрьского набора — 18 сентября — уже прошёл; поздний приём и набор ноября/декабря уточнить.',
        dict(year=2026,label='Цена weekend занятия/серии не опубликована; $1500 шестидневного лагеря сюда не переносится.',included='Индивидуализированные двухчасовые занятия; оборудование/материалы уточнить.',extras='Налог, питание, дорога, жильё семьи и технические accounts неизвестны.',deposit='Договор/отмена и срок оплаты не опубликованы.'),
        'Короткое занятие, не full-day care или boarding.',
        fit('conditional','Матвею подходит возраст 9–14 только после девятого дня рождения; в 8 ещё нет. Приём на оставшиеся месяцы отдельно.'),
        fit('later','Оскар 5–6 ниже минимума 9; семейный Ideathon для 5–6 рассматривается отдельно.'),[src('Сайт организатора: 9–14, двухчасовые занятия октября–декабря и прошедший срок октябрьского набора',HOME)],status='published_2026')
    price=dict(year=2026,label='3 дня: $356 за ребёнка до GST; один день: $145 до GST. При стандартном GST 9%: 388,04 за ребёнка, 776,08 за двоих за 3 дня. Сайт пишет $, валюта SGD принята по местному контексту и должна быть подтверждена счётом.',
        included='Дневные активности и присмотр подготовленных ведущих. FAQ включает питание по расписанию; соотношение числа сотрудников и детей, полный состав питания, страховки и транспорта не опубликованы.',
        extras='До 31 октября 2026 заявлена скидка 10% каждому ребёнку; итог с налогом и округлением ещё подтвердить. Перелёт, жильё семьи, доставка к двум площадкам и возможные обязательные доплаты отдельно.',
        deposit='Условия оплаты, депозита, возврата при болезни и отмены не опубликованы. Непогода может изменить активности; при болезни день нужно пропустить, право на возврат не установлено.')
    p=emit(3,'CAMP CHALLENGE · Nature Quest · дневные приключения','general,nature,sport,art,makers','day',
        'Сингапур · 23/25 ноября: KOKOMO Beach Club, 131 Pasir Ris Road; 24 ноября: Beach Station, Sentosa', '5–10',unknown,
        'Природа и рыбалка, прогулка по Sentosa, изготовление лодки и слайма, окрашивание кепок, кулинария, спортивные игры и вечер кино. Общий отдых с ручными проектами; отдельный интенсив по робототехнике, программированию или ИИ не заявлен. Сертификат подтверждает участие, а не международную победу.',
        '23–25 ноября 2026. Первые два дня: 09:00–17:30. На 25 ноября заголовок указывает конец в 20:00, подробный план — выдачу детей в 20:30; время уточнить. 24 ноября привозить и забирать в Sentosa. Смены 2027 ещё не объявлены.',price,
        'Три дневных посещения с поздним вечером 25 ноября, без заявленной ночёвки. Родители обычно не остаются; исключение согласуется отдельно.',
        fit('conditional','В ноябре 2026 возраст 8–9 входит в 5–10; приём приезжих, язык, здоровье и наличие места отдельно.'),
        fit('conditional','В ноябре 2026 возраст 5–6 входит в 5–10; готовность к длинному дню, язык и допуск отдельно.'),
        [src('Программа организатора: даты, возраст 5–10, цены, две площадки и FAQ',NATURE),src('IRAS: стандартная ставка GST 9%; счёт конкретного лагеря ещё неизвестен',GST)],
        status='published_2026',sessions=[['2026-11-23','2026-11-25']])
    p['timing']['session_details']=[dict(start='2026-11-23',end='2026-11-25',label='Три дневных посещения · две площадки · 25 ноября: конфликт 20:00/20:30',price=price['label'],source=NATURE,place=p['place'],date_scope='camp_session')]

def correct_ayla_v134(p):
    if p['slug']!='ayla-tokyo':return
    old='Часы Regular 09–13, Extended 09–15, Super Extended 09–17, Super Duper Extended 09–18.'
    new='Часы Prime 09–13, Regular 09–15, Extended 09–17, Super Extended 09–18. Названия четырёх пакетов исправлены по текущей странице; соответствующие часы и суммы не изменены.'
    p['programme']=p['programme'].replace(old,new)
    for v in p['timing']['session_details']:v['price']=v['price'].replace('Extended 09–15:','Regular 09–15:')
    p['price']['label']=p['price']['label'].replace('Extended 5 дней','Regular09–15 5 дней')
    p['price']['extras']=p['price']['extras'].replace('Extended 200 000 / Super 220 000','Extended09–17 200 000 / Super Extended09–18 220 000')
    p['checked']=CHECKED
    next(s for s in p['sources'] if s['url']==AYLA)['checked']=CHECKED

def extend_report_v134(r):
    r.update(version=134,asof=CHECKED)
    r['shortlist'] += [dict(label='Сингапур · AI и семейный Ideathon',slugs=NEW[:3],reason='Матвею — лагерь 7–15; Оскару — отдельный компонент 5–6 с родителем. Язык, единица цены, допуск к выездам и день Ideathon ещё не установлены.'),
        dict(label='Сингапур · общий ноябрьский отдых',slugs=NEW[3:],reason='Оба входят в 5–10; три дня на двух площадках. Английский не подтверждён; время окончания 25 ноября расходится: 20:00/20:30.')]
    for title,url,detail in [
        ('EDUTech · младший Ideathon и полный лагерь',COURSE,'Отдельный компонент 5–6 с родителем: точный день и цена неизвестны. Полный лагерь 7–15: 48,5 часов, регистрация и оплата до 15 ноября. Допуск иностранцев к специальным объектам, язык, страховка, налог и единица цены ещё требуют ответа.'),
        ('EDUTech · архив и занятия 9–14',HOME,'Программы AI 6–10 и 11–15 от 5 сентября 2026 завершены. Двухчасовые занятия 9–14 октября–декабря — короткий формат; срок октябрьского набора 18 сентября прошёл. Набор ноября/декабря и цены неизвестны.'),
        ('CAMP CHALLENGE · язык, возврат и вечер 25 ноября',NATURE,'23–25 ноября 2026, 5–10, три дня $356 до GST. Окончание последнего дня: 20:00/20:30, две площадки. Язык, приём приезжих, количество ведущих, возврат, валюта счёта и состав включений ещё уточнить.')]:
        r['gaps'].append(dict(iso='SGP',country='Сингапур',provider='v134 · '+title,url=url,detail=detail,next_action=ASK))
    review=r['family_review']
    for slug,goals,reason,limit in [(NEW[0],['technical','entrepreneurship'],'AI-продукт, клиент, цена и презентация: практический кандидат для Матвея в группе 7–15.','Оскару — отдельный семейный Ideathon. Язык, допуск к выездам и семейный счёт неизвестны.'),
        (NEW[3],['general','nature'],'Короткий общий отдых обоим в группе 5–10 в конце ноября 2026.','Язык не установлен, другая площадка 24 ноября, конец 25 ноября: 20:00/20:30. Полная стоимость поездки неизвестна.')]:
        assert not any(e['slug']==slug for e in review['entries'])
        review['entries'].append(dict(slug=slug,goals=goals,reason=reason,key_limit=limit,dossier_checked=CHECKED))
    review.update(version=134,asof=CHECKED)
    ps={p['slug']:p for p in r['profiles']}
    review['coverage']=dict(candidates=len(review['entries']),countries=len({ps[e['slug']]['iso'] for e in review['entries']}),fully_audited_countries=0)
    r['counts']=dict(dossiers=len(r['profiles']),countries=len({p['iso'] for p in r['profiles']}),swiss=sum(p['iso']=='CHE' for p in r['profiles']),by_status=dict(Counter(p['timing']['status'] for p in r['profiles'])),source_urls=len({s['url'] for p in r['profiles'] for s in p['sources']}))

def extend_planning_v134(d):
    planning=d['camp_planning'];ident='nature-quest-both-standard'
    q=offer(ident,NEW[3],'Nature Quest · 23–25 ноября · двое · обычная цена + GST 9%',388.04,currency='SGD',price_year=2026,format='day',sessions=[['2026-11-23','2026-11-25']],sources=[NATURE,GST],checked=CHECKED,
        gate='Возраст 5–10 подходит обоим; язык и приём приезжих ещё неизвестны. $ сайта принят как SGD по местному контексту; валюта, налог и округление требуют счёта. 25 ноября конец указан по-разному: 20:00/20:30; 24 ноября — Sentosa.',
        unknown_required=[dict(id='extras_total',label='Обязательные доплаты обоих · транспорт/страховка/состав пакета ещё проверить',unit='amount',rate=1,min=0)],
        included='Базовая цена 356 × 1,09 = 388,04 каждому; 776,08 за двоих. Питание по расписанию, активности и присмотр. Скидка 10% до 31 октября в этом расчёте не применена.',
        deposit_note='Оплата/депозит/возврат неизвестны; расчёт не quote или оплаченная бронь.',
        scope='Расчёт стоимости трёх дней для двоих со стандартным GST 9%. Валюта SGD принята по местному контексту; окончательный счёт ещё нужен. Остальные обязательные суммы и семейная поездка не оценены.')
    planning['offers']=[e for e in planning['offers'] if e['id']!=ident]+[q];planning.update(version=134,asof=CHECKED)
