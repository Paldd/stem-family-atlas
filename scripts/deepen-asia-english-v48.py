"""Bounded Singapore/Hong Kong pass: real cohorts, class gates and correctly scoped results."""
import ast, copy, json
from datetime import date, timedelta
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WORK=Path('/Users/pal/.codex/workspaces/stem-family-atlas-work')
CHECKED='2026-10-02';path=ROOT/'data/catalog.json';d=json.loads(path.read_text())
assert len(d['events'])==1712 and d['completeness_audit']['version']==47
urls={}
for name in ['urls-asia-english-v48.json','urls-asia-english-extra-v48.json','urls-asia-english-fll-v48.json']:
    urls.update(json.loads((WORK/name).read_text()))
new=[];byid={e['id']:e for e in d['events']}
tree=ast.parse((ROOT/'scripts/expand-oceania-v29.py').read_text())
for name in ['ref','event']:
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
    exec(compile(ast.Module(body=[node],type_ignores=[]),'event_helpers','exec'))
base_event=event
def event(*args,**kwargs):
    e=base_event(*args,**kwargs);e['region']='Азия';return e

# Four actual October weeks; a track/week is a cohort, not an independent camp operator.
camp_tracks=[
 ('Apprentice','worklab_apprentice','4.5–7 лет на первый день; у части таблицы есть 7+, верхний предел уточнить',0,2,'09:30–12:00','449','Оскар: Lego WeDo / механизмы и код; точную возрастную тему выбрать с оператором.',False,True,('robotics','coding')),
 ('Junior','worklab_junior','8–9 лет на первый день',0,2,'09:00–12:00','499','Lego robotics, механизмы и программирование; Junior и Senior — альтернативные уровни.',True,False,('robotics','coding')),
 ('Senior','worklab_junior','9–13 по тексту; таблица пишет 9+, фактическую верхнюю границу уточнить',0,2,'09:00–12:00','499','Lego robotics и усложнённые задачи; после трёх лет опыта нужен тест уровня.',True,False,('robotics','coding')),
 ('SPIKE Prime','worklab_spike','9+ на первый день; рекомендован опыт Scratch',0,3,'09:30–12:00','500','LEGO SPIKE Prime; конкретный уровень Camp 1 / 2 / 3 / 4 согласовать, недели не приравнивались к уровням.',True,False,('robotics','coding')),
 ('AI & Digital Citizenship','worklab_ai','7.5+ на первый день',2,4,'09:30–12:00','425','Вводные AI, текстовый код и digital citizenship; это не обещание углублённого ML.',True,False,('ai','coding','technology'))]
number=425
for monday in ['2026-10-05','2026-10-12','2026-10-19','2026-10-26']:
    for title,key,age,offset,last,time,price,gear,mat,osc,themes in camp_tracks:
        begin=date.fromisoformat(monday)+timedelta(days=offset);finish=date.fromisoformat(monday)+timedelta(days=last)
        locations='Forum · Orchard Road' if key=='worklab_ai' else 'Forum / UE Square / Coronation; конкретный филиал подтвердить'
        if key=='worklab_apprentice':locations='Forum / UE Square / Shaw Centre / Coronation; возрастную группу и филиал подтвердить'
        e=event(f'L{number}',f"Children’s Worklab · {title} · {begin.strftime('%d.%m')}–{finish.strftime('%d.%m.2026')}",
            'Сингапур',locations,urls[key],age,
            'Условно: возраст подходит; нужный технический уровень, филиал и место подтвердить' if mat else 'Нет по опубликованному верхнему диапазону этой младшей группы',
            'Условно: возраст подходит; точную группу 6–7 и место подтвердить' if osc else 'Нет: 6 лет ниже опубликованного минимума этой группы',
            'Индивидуальная дневная запись. Технический английский подтверждён; приём visiting family, опыт и свободное место ещё согласовать.',
            gear,block='Лагеря',start=str(begin),end=str(finish),participation='day_camp',
            language='Оператор прямо пишет, что все занятия ведутся на английском.',languages=('EN',),
            cost=f"${price} за базовые {last-offset+1} дня на местной странице; валюту, материалы и окончательный счёт подтвердить.",
            note=f"{time} по Singapore time. Это один трек одной опубликованной недели. Базовые Apprentice / Junior / Senior — Mon–Wed, опциональные 4 / 5 дней оплачиваются отдельно. Apprentice afternoon 14:30–17:00 только Shaw Centre; не перенесён на остальные филиалы. SPIKE — Mon–Thu, AI — Wed–Fri и только Forum. Жильё отдельно, текущая бронь не сделана.",
            themes=themes,evidence='program',date_scope='camp_window')
        e.update(provider='Children’s Worklab / Robotics Connection',language_mode='primary',language_certainty='Прямое All classes are taught in English в странице именно программы.',
            references=[ref('Контакты и филиалы',urls['sg_worklab_locations']),ref('Таблица фактических недель',urls['worklab_chart_'+('4' if key=='worklab_ai' else '3' if key=='worklab_spike' else '2' if key=='worklab_junior' else '0')])])
        number+=1
assert number==445

fll_gate='По сезонной странице проверяется также школьный класс. Команда зарубежной школы / организации допускается только в Overseas Category и не может представлять Singapore на World Festival. При переезде классификацию реальной местной команды согласовать отдельно.'
e=event('L445','FIRST Singapore · BIOGLOW Future 5+ · младшая программа','Сингапур','Организатор / учебный центр подтвердить',urls['fll_future5_current'],
 '5–7 лет и Grades 1–3 по BIOGLOW season page',
 'Нет: 9 сейчас выше диапазона Future 5–7', 'Условно: год рождения подходит; Grade 1–3, набор и место неизвестны',
 fll_gate,'LEGO Education Computer Science & AI; не заменять набор SPIKE по аналогии с Founders.',block='Лагеря',participation='day_camp',
 priority='P4 — текущий младший набор не подтверждён',note='Категория описана, но non-MOE список показывает Out of stock, конкретные даты младшего занятия / события не объявлены. Это не подтверждённый свободный лагерь и не мировая квота.',evidence='program')
e.update(participation='regular',format='Младшая учебная программа · фактический поток подтвердить',provider='FIRST LEGO League Singapore / Duck Learning',period='Сезон BIOGLOW 2026/27; текущий набор и даты Future 5+ не установлены',references=[ref('Класс и оборудование',urls['sg_fll_season']),ref('Статус non-MOE',urls['fll_nonmoe'])])
e=event('L446','Cobo Hong Kong · Vibe Coding Hackathon · будущая ступень 12–14','Гонконг','Wan Chai / Kowloon Tong · конкретный поток подтвердить',urls['cobo_camps'],
 'Principal 12–14; младшие Junior / Senior — отдельные программы',
 'Нет сейчас: минимальный возраст 12', 'Нет сейчас: минимальный возраст 12',
 'Выбрать фактическую неделю, кампус и слот; опубликованный список тем не подтверждает этот hackathon в каждую неделю.',
 'Vibe coding / авторский цифровой проект внутри учебного лагеря. Открытый международный соревновательный протокол и призовой фонд не установлены.',block='Лагеря',participation='day_camp',priority='P4 — будущий возраст и отдельное расписание',
 language='Medium of Instruction: English прямо указан оператором для holiday camps.',languages=('EN',),themes=('ai','coding','games'),
 cost='Октябрьская таблица: HKD 3600 / 4 дня или HKD 4500 / 5 дней. Счёт именно hackathon и будущего сезона уточнить.',
 note='Общее октябрьское окно имеет 4 недели; topic × week × campus не установлен, поэтому даты этой темы не выдуманы. Не является автоматическим путём на мировой чемпионат. Место и иностранный приём неизвестны.',evidence='program')
e.update(provider='Cobo Academy',language_mode='primary',language_certainty='Прямое Medium of Instruction: English.',period='Октябрь 2026: конкретная неделя Vibe Coding Hackathon не установлена')

for number in range(107,115):
    e=byid[f'L{number:03d}'];e.update(checked=CHECKED,language_mode='primary',languages=['EN'],language='Medium of Instruction: English прямо указан на текущей странице holiday camps.',language_certainty='Прочитано прямое указание языка преподавания именно лагерей.')
for number in range(56,78):
    e=byid[f'L{number:03d}'];e.update(checked=CHECKED,languages=[],language_mode='unconfirmed',language='Язык преподавания в текущем FAQ / программе прямо не установлен; EN-сайт не доказывает EN-занятия.',language_certainty='Старый EN-тег снят до подтверждения технического языка; реальные даты и ID смен сохранены.')

for id,title,age,key,start,end,mat,osc in [
 ('C1106','Founders Explore','6–10; Grades 1–4','fll_explore_current','','','Условно: рождение2017 допускает Explore2027; Grade1–4 и место подтвердить','Условно: возраст подходит; Grade1–4 и место подтвердить'),
 ('C1107','Founders Challenge · qualifiers','9–16; Grades 5–10','fll_challenge_current','2027-03-24','2027-03-25','Условно: возраст подходит; без Grade5 допуск не доказан','Нет: ниже минимального возраста9 и требуемого класса'),
 ('C1108','Founders Challenge · final','9–16; Grades 5–10','fll_challenge_current','2027-03-27','2027-03-27','Условно: нужен Grade5–10 и прошедший qualifier состав','Нет: ниже минимального возраста9 и требуемого класса'),
 ('C1109','Future 8+ · qualifiers','8–16; Grades 4–10','fll_future8_current','2027-03-24','2027-03-25','Условно: возраст подходит, но требуемый Grade4–10 подтвердить','Нет: ниже минимального возраста8'),
 ('C1110','Future 8+ · final','8–16; Grades 4–10','fll_future8_current','2027-03-27','2027-03-27','Условно: Grade4–10 и прошедшая qualifier команда','Нет: ниже минимального возраста8')]:
    e=event(id,'FIRST Singapore · BIOGLOW 2026/27 · '+title,'Сингапур','Точную площадку и личный слот подтвердить',urls['sg_fll'],age,mat,osc,
        fll_gate+(' Финал требует результата qualifier, не прямой семейной регистрации.' if 'final' in title else ''),
        'LEGO Education Computer Science & AI' if 'Future' in title else 'LEGO Education SPIKE / соответствующий Founders kit',
        start=start,end=end,deadline='2027-01-31',scope='national',
        note='FAQ указывает закрытие 31.01.2027 в10:00 SGT; старая registration-страница ещё содержит2025/26 cutoffs и не использована для новых рождений. Даты24–25/27марта относятся к Challenge / Future8; дату Explore из них не выводили. На homepage указано2–5 участников, локальный состав проверить. EN-интервью не подтверждено.',
        cost='$233 Explore; Challenge / Future8 $220–590 с вариантами kit на non-MOE страницах. Валюту, раннюю скидку и полный счёт подтвердить.')
    e.update(deadline_utc='2027-01-31T02:00:00Z',deadline_label='Регистрация BIOGLOW',deadline_note='FAQ:31Jan2027 10am SGT=02:00UTC. Срок не гарантирует свободное место.',
        references=[ref('Возраст / класс и оборудование',urls['sg_fll_season']),ref('Overseas category и дедлайн',urls['sg_fll_faq']),ref('Текущая non-MOE карточка',urls[key])],
        reward='Overseas: Champion /1stRunnerUp/2ndRunnerUp; Singapore World Festival quota иностранной организации не положена.')

nrc_data=[
 ('C1111','KUBO Preschool','5–6 по последним правилам2026','Нет: старше6','Условно: сейчас6; в2027исполнится7, новый возрастной срез критичен','KUBO;2–5 детей и максимум2coaches.'),
 ('C1112','Regular Lower Primary','7–9 по правилам2026','Условно: сейчас9, но в2027исполнится10; новую Upper категорию проверить','Нет сейчас:6ниже7; в2027возможна Lower после проверки нового cutoff','SPIKE Essential / WeDo по Lower описанию;2–3ученика+coach,25cmcube.'),
 ('C1113','Regular Upper Primary','10–12 по правилам2026','Нет сейчас:9; в2027исполнится10, возраст и класс нового сезона проверить','Нет: ниже10','SPIKE Prime / EV3 / Robot Inventor;2–3ученика+coach,25cmcube.'),
 ('C1114','Open Primary','7–12 по правилам2026','Условно: возраст подходит; класс и иностранный приём подтвердить','Нет сейчас:6ниже7; будущий2027cutoff ещё не опубликован','Свободные hardware/software,2–3ученика;booth2×2m; инженерный проект и предпринимательская защита.'),
 ('C1115','AI Maker Primary','7–12 по правилам2026','Условно: возраст подходит; класс и реальный foreign entry подтвердить','Нет сейчас:6ниже7; будущий2027cutoff ещё не опубликован','Свободный робот25×25cm без ограничения высоты;2–3ученика;дляPrimary минимумblockcodingplatform;AI/MLмиссии.')]
for id,title,age,mat,osc,gear in nrc_data:
    e=event(id,'NRC Singapore · '+title+' · следующий сезон','Сингапур','Science Centre Singapore / национальную площадку нового сезона уточнить',urls['sg_nrc_science'],age,mat,osc,
        'Организатор описывает MOE / international schools, private teams и learning centres. Это не прямое подтверждение зарубежной семейной команды. Национальный WRO теперь отдельный Space Faculty маршрут.',gear,
        scope='national',themes=('robotics','coding','ai') if title.startswith('AI') else ('robotics','coding'),evidence='historical_program',
        note='2026уже закончился:17–28августа,awards1сентября. Даты2027не объявлены в прочитанной странице; диапазоны2026не переименованы в гарантированные правила2027. Regular general controller list расходится с Lower WeDo/Essential: нужен конкретный division pack.',
        priority='P2 — новый возрастной и иностранный допуск')
    e.update(period='Следующий сезон не датирован; последние опубликованные правила2026',references=[ref('Типы команд и регистрация2026',urls['sg_nrc_duck'])])
for id,cat in [('C1116','RoboMission'),('C1117','Future Innovators')]:
    e=event(id,'WRO Singapore · '+cat+' Elementary · следующий сезон','Сингапур','Space Faculty · площадку следующего сезона подтвердить',urls['sg_wro'],
        '8–12; опубликованные рождения2014–2018 относятся только к2026',
        'Условно: год2017 подходит по2026правилам; новый сезон и иностранный вход отдельно',
        'Нет сейчас:6; Elementary минимум8, будущий год не гарантирован',
        'Команда2–3ученика+coach; международный coach18+. Национальный допуск иностранцев и мировая квота не установлены. Каждый ученик только в одной команде, команда только в одной категории за сезон.',
        'Свободные hardware/software; RoboMission робот25cmcube; Future Innovators booth2×2×2m.',scope='national',evidence='historical_program',
        note='2026прошёл8–11сентября вSingaporePolytechnic. RoboMission2026Elementary/Junior закрывались по вместимости. Season Quests20% относится к preliminary; final формула50/50 отдельно. Не перенесли старые fees/cutoffs на2027. Взрослый не должен строить/кодировать за ребёнка.')
    e.update(period='Новый2027сезон / место / foreign qualification пока не подтверждены',references=[ref('RoboMission2026: возраст, команда, собственная работа',urls['wro_sg_rules']),ref('WROSG2026 terms',urls['wro_sg_terms'])])

hk_tracks=[('C1118','Lower · Intelligent colour classification'),('C1119','Lower · Line following'),('C1120','Lower · Child fun challenge'),('C1121','Lower · Curling programming'),('C1122','Lower · Curling mechanical'),('C1123','Upper · Space Challenge')]
for id,title in hk_tracks:
    lower=title.startswith('Lower')
    e=event(id,'Hong Kong Winter Robot Challenge2027 · '+title,'Гонконг','Дистанционная подача видео; поездка не требуется',urls['hk_winter'],
        'Lower: Primary3илиниже; школьная ступень определяет допуск' if lower else 'Upper: Primary6илиниже; точную нижнюю ступень и эквивалент иностранного класса уточнить',
        'Условно: точный школьный класс и зарубежный эквивалент неизвестны',
        'Условно: младший школьный класс / эквивалент, зарубежный приём и задача ещё проверить',
        'Индивидуально1ребёнок+coach или2–4детей+coach. Видеоподача7декабря–24января; иностранный приём и EN-защита не подтверждены. Заявка через опубликованный школьный/организационный процесс.',
        'Lower: WeDo2.0 / SPIKE Essential / Makerzoid Robot Master; механический curling не обещает программирования.' if lower else 'Upper: SPIKE Prime / EV3;7space-миссий за2минуты, старые field kits discontinued.',
        start='2026-12-07',end='2027-01-24',deadline='2027-01-24',scope='national',participation='individual_or_team',date_scope='submission_window',
        cost='HKD390 за solo1ребёнок+coach;HKD720 за команду2–4+coach, по опубликованной таблице.',
        note='Видео≤5мин,не ниже720p; робот от старта до остановки без ускорения/монтажа. UnlistedYouTube илиGoogleDrive по ссылке; школьную заявку/документы/английский подтвердить. Результаты объявлены на февраль2027без точного дня. WROHK-branding не доказывает отбор наWorldFinal.',
        themes=('robotics','technology') if 'mechanical' in title else ('robotics','coding'))
    e.update(reward='Оценка заданий и graded LEGO certificates. Это не доказанный международный podium / национальная квота WRO Worlds.',deadline_label='Видеоподача зимнего конкурса',deadline_note='24.01.2027; конкретный час не опубликован.',registration_status='Заявка семьи не подана; зарубежный допуск неизвестен.')

def expo(id,title,key,start,end,city,policy,age,cost,note,scope='international'):
    no=policy=='adults_only'
    e=event(id,title,'Сингапур',city,urls[key],age,
        'Нет: дети6/9не допускаются по опубликованному порогу' if no else 'Условно: детский минимум и профессиональный visitor допуск подтвердить',
        'Нет: дети6/9не допускаются по опубликованному порогу' if no else 'Условно: детский минимум и профессиональный visitor допуск подтвердить',
        'Регистрация trade / business visitor; семейное исключение не заявлено.' if no else 'Visitor pass / профессиональная регистрация; детское правило нужно подтвердить.',
        'Посетитель без робота',block='События',start=start,end=end,participation='visitor',scope=scope,
        priority='P4 — взрослым; детский вход запрещён' if no else 'P3 — детский доступ подтвердить',themes=('robotics','ai','technology'),cost=cost,note=note)
    e.update(exhibition_tier='global' if key=='gitex' else 'profile',visitor_policy=policy,visitor_policy_note=age,adult_entry=e['entry'],level='Отраслевая выставка / конференция',
        highlights=['Промышленная автоматизация и роботы','AI и цифровые технологии','Демонстрации и профессиональные контакты'],exhibitors=[],
        exhibitor_note='Полный список компаний именно этого выпуска не проверен; прошлые участники не гарантируют демонстрацию в новом сезоне.',exhibitor_directory_url=urls[key])
    return e
expo('E185','Industrial Transformation Asia-Pacific2026','itap_ticket','2026-10-21','2026-10-22','Suntec Singapore','confirm_children',
    'Детский минимум не установлен; visitor описан для industry professionals.',
    'Visitor:бесплатно для industry professionals;Delegate:SGD100 за конференцию+выставку,2026тариф.',
    'Нынешний2026выпуск21–22октября. Детский / семейный вход не подтверждён. Наличие registration button не означает допуск или полученный билет.')
expo('E186','Industrial Transformation Asia-Pacific2027','itap_ticket','2027-07-20','2027-07-22','Marina Bay Sands · Singapore','confirm_children',
    'Детский минимум и категории будущего visitor2027 не установлены.',
    'Тариф2027не установлен;2026DelegateSGD100не перенесён.',
    'Следующий2027выпуск20–22июля прямо указан в footer организатора. Место / даты нового выпуска известны, текущие билеты и список компаний отдельно.')
expo('E187','GITEX AI ASIA2027','gitex','2027-04-29','2027-04-30','Marina Bay Sands · Singapore','adults_only',
    'Строго для посетителей старше18лет; trade and business professionals only.',
    'Будущий профессиональный билет / категорию / окончательную цену сверить.',
    'Организатор прямо ограничивает expo посетителями over18. Отдельный взрослый маршрут; в семейный календарь детей не внесён.')
e=byid['E078'];e.update(checked=CHECKED,source=urls['innocarnival'],exhibition_tier='profile',visitor_policy='family',visitor_policy_note='Публичный InnoCarnival; дети и семьи прямо целевая аудитория, конкретные workshop age/quota отдельно.',
    adult_entry='Посещение Science Park; все активности объявлены бесплатными, мастер-классы могут требовать отдельной записи.',
    highlights=['Семейные технологии и демонстрации','Научные интерактивные активности','Тематические мастер-классы'],exhibitors=[],exhibitor_note='Список компаний / число всех роботопроизводителей не установлен;150workshopsне равно150companies.',exhibitor_directory_url=urls['innocarnival'],
    cost='Все активности объявлены бесплатными; места, возраст и язык отдельного workshop проверить.',note=e['note']+' Перепроверено24.10–01.11.2026: weekends10–18,weekdays10–17. Семейный формат подтверждён; языки и возраст каждого workshop отдельно.')

d['events']+=new
def profile(id,name,age,summary,categories,ids,route,nuances,keys):
    p=dict(id=id,name=name,group='regional',age_summary=age,age_tags=['6','9','10-12','teen'],summary=summary,categories=categories,event_ids=ids,legacy_ids=[],route=route,
        hardware='Зависит от категории; перед покупкой выбрать действующий division / edition.',language='EN-судейство конкретной команды / этапа прямо не подтверждено; язык сайта не использован как язык интервью.',
        importance='Конкретный национальный / местный путь внутри известного семейства; масштаб и иностранная квота показаны отдельно.',strengths=summary,
        requirements=['Точный класс, возрастной срез, состав команды и самостоятельную детскую работу проверить.', 'Место / иностранный допуск / мировая квота не следуют из регистрации или возраста.'],nuances=nuances,
        cost='Взнос, kit, coach, поездка и школа отдельно; старые тарифы не являются ценами нового сезона.',
        award='Награда именно своей категории и этапа; обучение, квалификация и мировой титул не объединены.',
        sources=[dict(title=title,url=urls[key],checked=CHECKED)for title,key in keys],evidence='Прочитаны первичные страницы и указанные PDF; неподтверждённые условия отмечены.',checked=CHECKED)
    assert id not in {p['id']for p in d['league_guide']['profiles']};d['league_guide']['profiles'].append(p);return p
def cat(name,age,team,hardware,rule,entry):return dict(name=name,age=age,team=team,hardware=hardware,age_rule=rule,entry=entry)
profile('fll-singapore-bioglow','FIRST Singapore · BIOGLOW Founders / Future','Explore6–10 /Grades1–4; Challenge9–16 /Grades5–10;Future5–7 /Grades1–3;Future8–16 /Grades4–10',
    'Для Матвея возраст недостаточен: Challenge требуетGrade5,Future8Grade4. Оскару Explore /Future5после проверки класса. Зарубежной организации толькоOverseasCategoryбезSingaporeWorldFestivalквоты.',
    [cat('Founders Explore','6–10','Homepage2–5; local roster confirm','SPIKE','Grades1–4; FAQ допускает исполняющиеся10в2027','ДатаExploreне объявлена'),cat('Founders Challenge','9–16','Homepage2–5; local roster confirm','SPIKE','Grades5–10','Qualifier24–25марта;final27марта2027'),cat('Future5+','5–7','Local roster confirm','LEGO Education Computer Science & AI','Grades1–3','Out of stockв non-MOEсписке; поток не датирован'),cat('Future8+','8–16','Homepage2–5; local roster confirm','LEGO Education Computer Science & AI','Grades4–10','Qualifier24–25марта;final27марта2027')],
    ['C1106','C1107','C1108','C1109','C1110','L445'],'Класс и edition→реальная местная / Overseasкоманда→qualifier→final→международная квота только разрешённой местной организации.',
    [fll_gate,'Старая registration2025/26не задаёт новые cutoffs. Exploreне получила датуChallengeпо аналогии.','FAQearlybird31.12.2026 22:00SGT;finalregistration31.01.2027 10:00SGT. Limitedslots,не обещание места.'],
    [('BIOGLOWseason','sg_fll_season'),('Даты','sg_fll'),('Overseas/FAQ','sg_fll_faq'),('non-MOE','fll_nonmoe')])
profile('nrc-singapore','NRC Singapore · KUBO, Regular, Open и AI Maker','KUBO5–6;Lower7–9;Upper10–12;Open/AIPrimary7–12 по2026',
    'NRCдаёт младшую практику и AI/инженерные проекты, но2026закончен. В2027Оскар станет7,Матвей10: нельзя заранее сохранить старые KUBO /Lowerкатегории.',
    [cat('KUBO','5–6','2–5 +max2coaches','KUBO','Preschool; новый cutoffнеизвестен','Следующий сезон не объявлен'),cat('Regular Lower /Upper','7–9 /10–12','2–3+coach','LowerWeDo/Essential;UpperPrime/EV3/RobotInventor','Возраст+школьнаяступень','Следующий сезон не объявлен'),cat('Open /AI Maker Primary','7–12','2–3+coach','Свободные platforms;PrimaryAIminimumblockcoding','Primary; новый пакет отдельно','MOE,international school,private /centreописаны')],
    [x[0]for x in nrc_data],'Школьная ступень и возраст→localprivate/schoolentry→categorypack→национальныйNRC;WROквота по отдельномуSpaceFacultyпути.',
    ['International schoolне означаетлюбойзарубежныйтуристическийfamilyteam.','LowerspecificWeDo/Essentialрасходится сgeneralcontrollerlist; конкретныйpackобязателен.','2023archiveawardstableнаDuckpageне является2026результатом.'],[('ScienceCentreправила','sg_nrc_science'),('Типыкоманд','sg_nrc_duck')])
profile('wro-singapore-spacefaculty','WRO Singapore · Space Faculty national route','Elementary8–12;2–3ученика,неsolo',
    'МатвеюElementaryпо возрасту; Оскару пока рано. ОрганизаторWROнационального путиSpaceFacultyотдельно отNRC. Следующий2027сезон и foreignworldquotaне установлены.',
    [cat('RoboMission Elementary','8–12','2–3+coach','Свободныеhardware/software;25cmcube','Age calendar year;рожденные2014–18только2026','Новый2027наборне объявлен'),cat('Future Innovators Elementary','8–12','2–3+coach','Свободныеhardware/software;booth2×2×2m','Сезонныйcutoffиownwork','Новый2027наборне объявлен')],
    ['C1116','C1117'],'Localcoach→проверкаforeign/национальногодопуска→свояработа→nationalresult→WorldFinalтолько по подтверждённой квоте.',
    ['RoboMission2026минимум2детей;internationalcoach18+,однакоманда/участник/сезон.','2026прошёл8–11сентября;старыеfees149/249/599SGDне цены2027.','SeasonQuests20%preliminaryне равно20%всемирногофинала.'],[('Национальныйорганизатор','sg_wro'),('GeneralRules2026PDF','wro_sg_rules'),('Terms2026PDF','wro_sg_terms')])
profile('hongkong-winter-robot','Hong Kong Winter Robot Challenge2027 · remote video','LowerPrimary3илиниже;UpperPrimary6илиниже;1или2–4ученика',
    'Дистанционный зимний конкурс со школьными категориями. Soloвозможен; наградыgradedLEGOcertificates. Зарубежныйэквиваленткласса/английскийиотборWROWorldsне доказаны.',
    [cat('Lower · five tracks','P3илиниже','1+coach /2–4+coach','WeDo2.0 /SPIKEEssential /Makerzoid','Класс и иностранный эквивалент','Видео07.12.2026–24.01.2027'),cat('Upper · SpaceChallenge','P6илиниже','1+coach /2–4+coach','SPIKEPrime /EV3;7missions','Точнуюнижнююступень и иностранный эквивалент уточнить','Видео07.12.2026–24.01.2027')],
    [x[0]for x in hk_tracks],'Класс /foreignentry /ENподтверждены→выбратьmission→самостоятельныйробот→unedited720pvideo≤5min→оценкаFeb2027месяцбезточнойдаты.',
    ['WROHKbrandне делаетзимнийchallengeквалификациейWorldFinal.','Video submissionwindowне является48днямиочногофестиваля.','Механическийcurlingотдельнаянепрограммируемаямиссия;цветоваяклассификацияне доказанныйAI/ML.'],[('Зимниеправила','hk_winter')])

def school(id,name,iso,country,city,programme,labs,admissions,cost,keys,results,evidence='programme'):
    s=dict(id=id,name=name,iso=iso,country=country,region='Азия',city=city,school_type='private',curriculum='Американская учебная программа; IB PYP / MYP / DP не подтверждены.',ib_programmes=[],
        ages='Elementary / младшая школа; точный класс по assessment и возрастному правилу школы.',instruction_languages=['EN'],language_note='Учебная программа на английском; отдельно языковые предметы не являются языком STEM.',
        fit=dict(mat='candidate',osc='candidate',note='Точная дата рождения / класс и admission assessment неизвестны; поступление в школу не означает место в роботокоманде.'),
        boarding='unknown',boarding_note='Дневная школа; постоянный пансион в прочитанных источниках не установлен.',programme=programme,labs=labs,ai='Отдельную обязательную AI-младшую программу, часы и platform проверить.',
        results=results,evidence=evidence,admissions=admissions,cost=cost,
        questions=['Какие классы, возрастной срез и языковое assessment получит каждый ребёнок?','Кто действующий младший coach, код команды, сколько тренировочных часов и есть ли место обоим?','Какие реальные organizer protocols последних3–5лет и какие национальные/мировые квоты доступны?','Какой полный текущий годовой счёт, extracurricular, EAL и документы нового ученика?'],
        sources=[dict(title=title,url=urls[key],claim=claim,kind='school',checked=CHECKED)for title,key,claim in keys],checked=CHECKED,priority=2,research_status='partial',verification='Прочитаны первичные школьные тела. Школьный отчёт не заменяет мировой organizer protocol и не обещает свободное место.')
    assert id not in {s['id']for s in d['schools']};d['schools'].append(s);return s
s=school('S050','American International School Hong Kong','HKG','Гонконг','Kowloon Tong',
    'ElementaryGrades1–4;STEAMspecialist. VEXGO pipelineGrades2–4 и региональное участие Guangzhou2026; младшуюrobotteamGrade1 отдельно проверить.',
    'ElementaryiPads/STEAM; конкретное число инженерных часов, hardware и лабораторных мест не установлено.',
    'Grade1–12:assessmentанглийского и математики, дляoverseasвозможнаonlineassessment. Сайт принимает будущие2027/28 и2028/29;current2026/27placeslimited.',
    'Прочитанная tuitionтаблица явно2025/26:Grades1–4HKD152800/год, levy1st12000/2nd8000. Текущий2026/27полный счёт неизвестен;старую цену не использовать для бюджета переезда.',
    [('Elementary','ais_primary','Grades1–4,STEAM'),('Englishcurriculum','ais_about','Educationalprogramme inEnglish'),('RegionalVEXGO','ais_go_result','Schoolreporttwoawards'),('InternalVEXGO','ais_go_internal','Single-schoolchampionship'),('Admissions','ais_apply','EN/mathassessment'),('Feesoldyear','ais_fees','Таблица2025/26'),('LanguagesFAQ','ais_faq','Mandarinrequired;SpanishonlyHighSchool')],
    [dict(season='2025/26',league='VEX GO',stage='Guangzhou regional · report08.06.2026',award='AIS14:ExcellenceAwardиDriving/AutonomousSkills№1',source=urls['ais_go_result'],provenance='school_report'),dict(season='2025/26',league='VEX GO',stage='AISinternal ·10.06.2026',award='AIS13:SchoolChampion',source=urls['ais_go_internal'],provenance='school_report')],evidence='other_result')
s['language_note']='Englisheducationalprogrammeпрямо подтверждена. MandarinобязателенEarlyChildhood–Grade8;SpanishпредлагаетсятолькоHighSchool,не языкPrimarySTEM.'
s=school('S051','Singapore American School','SGP','Сингапур','Woodlands',
    'ElementarySTEAMеженедельнаяпрограммапо классамK–5;Krobotics/coding,G2oceancleanuprobots,G3deliveryrobot,G5sensorcleanup. MiddleSchoolVEXIQ,HighSchoolFRC/VEXV5/MATEROV — последующие ступени.',
    'Школа описывает2026/27:5science/engineeringlabs,4STEAMteachersи3assistants. Это штат/пространство,не результат мирового рейтинга.',
    'Возрастнойсрез1сентября;Grade1требует6леткэтойдате. Языковоеassessment:подробныйEALpageдаётGrade3Intermediate/Transition иGrades4–5Transition;общаяlanguagepageнеоднозначнапоEALbeyondGrade4,нужнаперсональнаяоценка.',
    'Страница ведётк2026/27feesPDF,полнаятаблица в этом проходе не извлечена;tuition/development/EAL/extracurricularсуммы неизвестны.',
    [('Elementary','sas_elementary','ENschool;ChineseORSpanishlanguageclass'),('STEAM','sas_steam','КлассыK–5,лаборатории2026/27'),('Roboticspipeline','sas_robotics','MiddleVEXIQ/HighFRC,VEXV5,MATEROV'),('Placement','sas_placement','Sep1age/grade'),('DetailedEAL','sas_eal','Grade3/4/5entrylevels'),('Languagepolicy','sas_language','НеоднозначностьEALграницы'),('Fees','sas_fees','2026/27PDFlink;суммы не извлечены')],[])
s['language_note']='Школа ведёт обучение наEN;ElementaryежедневноизучаетChineseИЛИSpanishкакязыковойпредмет. Это не испанский язык технического преподавания. EALplacementнужноassessment.'

h=d['school_history'];h.update(version=48,checked=CHECKED)
entities=[dict(id='AIS-HK',name='American International School Hong Kong',kind='school',country='Hong Kong',age='elementary',school_id='S050',note='JuniorGrades2–4VEXGO. Региональные и внутренние результаты не мировойVEXIQтитул.'),
    dict(id='SG-WRO-SOR-CIRCUIT',name='SOR CIRCUIT SHREDDER',kind='unresolved',country='Singapore',age='elementary',school_id=None,note='WROSG2026ElementaryChampionпоорганизатору;префиксSORне использовандлядогадкиконкретнойшколы/академии.')]
for entity in entities:
    assert entity['id']not in {r['id']for r in h['entities']};h['entities'].append(entity)
for id,entity,league,category,stage,award,level,key,team,note,provenance in [
 ('H147','AIS-HK','VEX GO','ElementaryGrades2–4','Guangzhou regional ·2026','Excellence Award ·OverallTournamentChampion','regional_judged','ais_go_result','AIS14','Schoolreport08.06.2026;комплекснаярегиональнаянаграда,неWRO/VEXIQWorldChampion.','school_report'),
 ('H148','AIS-HK','VEX GO','Driving and AutonomousSkills','Guangzhou regional ·2026','1st place ·Driving and AutonomousSkills','regional_skills','ais_go_result','AIS14','Техническаярегиональнаякатегория;необщиймировойтитул.','school_report'),
 ('H149','AIS-HK','VEX GO','Grades2–4 ·internal','AIS schoolchampionship ·10June2026','SchoolChampion ·playoff14points','school_internal','ais_go_internal','AIS13','16teams48studentsоднойшколы. Qualifiers31pointsбылиtie;чемпионпоplayoff14.','school_report'),
 ('H150','SG-WRO-SOR-CIRCUIT','WRO','RoboMission Elementary','WRO Singapore national2026','Champion','national_match','sg_wro','SOR CIRCUIT SHREDDER','Национальныйchampionпоорганизатору;школа/иностраннаяквота/WorldFinalresultне установлены.','organizer_protocol')]:
    h['results'].append(dict(id=id,entity_id=entity,year=2026,league=league,category=category,stage=stage,award=award,level=level,source=urls[key],provenance=provenance,team=team,team_id=None,note=note,checked=CHECKED))
h['methodology'].append('v48: AISрегиональныеVEXGOнаградыиsingle-schoolchampionshipв отдельныхуровнях;SASpipelineне приписанынепроверенныемировыетитулы. WROSGнациональнаяпобедаоставленаunresolvedбездогадкипоSORпрефиксу.')

def pick(kind,country,title,why,gate,ids,schools,keys):return dict(kind=kind,country=country,title=title,why=why,gate=gate,event_ids=ids,school_ids=schools,source_urls=[urls[k]for k in keys])
f=dict(version=48,checked=CHECKED,status='partial',title='Сингапур и Гонконг: лагеря, школьные категории и путь команд',region_label='АЗИЯ · СИНГАПУР / ГОНКОНГ',heading='Английские программы. Разные пути двум детям.',
 family=d['middleeast_focus']['family'],
 conclusion='Я бы начал с короткой английской пробы Worklab или Cobo: оба ребёнка имеют отдельные возрастные группы. Для реальных сезонных наград сначала выяснить классы: Singapore ChallengeтребуетGrade5,Future8Grade4;HongKongWinterChallengeпривязанкP3/P6. Переезд ради сильной школы оценивать после встречи с действующим младшим наставником. Коста-Рика / Мексика остаются приоритетной базой основного маршрута.',
 family_picks_heading='С чего я бы начал в Сингапуре и Гонконге',family_picks_note='Это подбор для вашей семьи по первичным возрастам, языку и опубликованным условиям. Он не является рейтингом всех лагерей / школ Азии; место и уровень после трёх лет соревнований проверяются отдельно.',
 limitations='Ограниченный проход двух направлений. Карточки недель / дисциплин — не число независимых фестивалей. Полный местный и мировой охват не завершён; HKTDCInnoEx/Electronicsстраницыв этомпроходенедоступны,ихновые даты/детскиеправиланеизобретены.',
 countries=[dict(iso='SGP',name='Сингапур',verdict='Сильная учебная проба на английском; классы важнее возраста',reason='WorklabпубликуетполностьюEnglishтехническиелагеря;FLLразделяетFounders/Futureпоклассам. NRCиWROимеютразныхорганизаторов.',
    mat='В9летWorklabJunior/Senior/SPIKE/AIподходятусловно. SingaporeChallengeGrade5,Future8Grade4;ExploreGrades1–4можетлучше соответствоватьклассу,уровеньприэтомпроверить.',
    osc='WorklabApprentice4.5–7. FLLExplore6–10/Grades1–4илиFuture5/Grades1–3послепроверкикласса;NRC KUBO5–6толькопо2026условиям,в2027исполнится7.',
    camp='20новыхWorklabcohorts:4октябрьскиенедели×5треков. Computhink22существующиеNovember/Decemberсменысохранены,ноязыкзанятийпрямонеподтверждён. Все — дневные,семьянуждаетсявжилье.',
    school='SAS:ENElementarySTEAMсK,позжеVEXIQ/FRC/VEXV5/MATEROV. РанееHorizon/Rulangдосьесохранены;поступлениевместнуюпубличнуюшколуотдельныйдопуск. МировыеElementaryтитулыSASнеустановлены.',
    city_route='Orchard/ForumдляAIиApprentice;UE Square/Coronationдляrobotics. SASWoodlandsдляшкольнойпробы. Слот/кампусзаранеевыбрать.',
    budget='Worklabбазовые3дняApprentice$449,Junior/Senior$499,4дняSPIKE$500,3дняAI$425;валюту/счётподтвердить. ПолныйSASгодовойсчёт2026/27неизвлечён.',
    results_check='FLL2025/26официальноразделяетschools/private/overseaschampions. WROSGSOR CIRCUIT SHREDDERnationalElementaryChampion2026;школанеустановлена. Местныепобедынемировыетитулы.',
    event_ids=['L425','L426','L427','L428','L429','L440','L441','L442','L443','L444','L445','C1106','C1107','C1108','C1109','C1110','C1111','C1112','C1113','C1114','C1115','C1116','C1117','E185','E186','E187'],school_ids=['S006','S007','S051'],profile_ids=['fll-singapore-bioglow','nrc-singapore','wro-singapore-spacefaculty'],risk=fll_gate),
    dict(iso='HKG',name='Гонконг',verdict='Английские лагеря; школьный remote-конкурс и семейная выставка',reason='CoboпрямопишетMediumofInstructionEnglishдляJunior6–8/Senior9–11. WinterChallengeимеетsoloвидеоподачу,InnoCarnivalсемейныйбесплатный.',
    mat='CoboSenior9–11;WinterLowerприP3илиниже,UpperSpaceприP6илинижеиусловияхорганизатора. Школьныйэквивалентиforeignentryещёнужнопроверить.',
    osc='CoboJunior6–8подходитпо возрасту. WinterLowerзависитоткласса/школьнойсправки;Grade1AISнеозначаетподтверждённуюVEXGOкомандуGrades2–4.',
    camp='Coboоктябрь:5–9/12–16/20–23/26–30,10–12или14–16. VibeCodingHackathon12–14покабудущийвозраст;конкретнаятематическаянеделянеустановлена.',
    school='AISведётAmericanprogrammeнаEN;ElementaryGrades1–4,роботопрактикаGrades2–4. AIS14имеетрегиональныеVEXGOнаградыGuangzhou2026,неWorldChampion.',
    city_route='WanChaiдляCobo;KowloonTongвыбранныеклассыпозапросу/AIS;ScienceParkдляInnoCarnival. Winterвидеоиздому,поездканенужна.',
    budget='CoboHKD4500/5днейили3600/4дняза2-часовойслот. WinterHKD390soloили720команда. AISпрочитанныеfees2025/26старые;полныйнынешнийсчётнеизвестен.',
    results_check='AIS14региональныеExcellenceиSkills№1;AIS13внутришкольныйChampion10июня2026. Wintergradedcertificatesнепредставленыкакмеждународныеpodiums.',
    event_ids=['L107','L108','L113','L114','L446','C1118','C1119','C1120','C1121','C1122','C1123','E078'],school_ids=['S050'],profile_ids=['hongkong-winter-robot'],risk='Иностранныйшкольныйэквивалент,ENподачаWinter,местаCobo/AISиage/languageкаждогоworkshopещёнеподтверждены.')],
 family_picks=[
    pick('camp','Сингапур','Worklab · отдельный робототрек каждому','ОскаруApprentice,МатвеюSeniorилиSPIKE. ТехническийENпрямоподтверждён.','Уровень,деньрождения,кампус,visitingfamilyentryиместазатем;этоучебнаяпроба.', ['L425','L427','L428','L440','L442','L443'],[],['worklab_apprentice','worklab_junior','worklab_spike']),
    pick('league','Сингапур','BIOGLOW · сначала точный класс','Exploreдлямладших;Challenge/Future8дляМатвеятолькопоподтверждённойступени.','Overseasимеетсвоинедавниепризыместногофинала,ноникакойSingaporeWorldFestivalквоты.', ['C1106','C1107','C1109','L445'],[],['sg_fll_season','sg_fll_faq']),
    pick('school','Сингапур','SAS · проверить младшего наставника','STEAMвElementary,дальшепонятныйVEXIQ/FRC/ROVмаршрут;английскаяучебнаясреда.','Младшаякоманда/результаты,assessment/EAL,полныйfeesсчётиприёмнеподтверждены.', [],['S051'],['sas_steam','sas_robotics','sas_placement']),
    pick('camp','Гонконг','Cobo · Junior и Senior на английском','Обаимеютажгруппы6–8/9–11итемыроботы/игры/AI.','Слоты2часавдень;topic×week×campusнужендооплаты. Hackathon12–14сейчасрано.', ['L107','L108','L113','L114','L446'],[],['cobo_camps']),
    pick('league','Гонконг','Winter Challenge · solo из дома','Можноодногоребёнкасcoachилипару/команду2–4;необязательноехать.','Зарубежныеклассы/ENнеподтверждены;наградыgradedLEGOcertificates,неWROWorldFinal.', ['C1118','C1119','C1122','C1123'],[],['hk_winter']),
    pick('school','Гонконг','AIS · действующая младшая VEX GO практика','РегиональныенаградыкомандыGrades2–4ианглийскоеElementaryподтвержденышколой.','НынешнийGrade1coach/места/feesнеизвестны;результатшкольногоотчётанезаменяетWorldprotocol.', [],['S050'],['ais_primary','ais_go_result','ais_apply'])],
 season_stops=[dict(country='Сингапур / Гонконг',date='05–30.10.2026',title='Октябрьские учебные недели на английском',detail='Worklab:4недели×5треков,базовыйлагерь3/4дня. Cobo4недели,20–23октября4дня;выбратькаждомусвоюгруппу.',event_ids=['L425','L426','L427','L428','L429','L113','L114']),
    dict(country='Гонконг',date='24.10–01.11.2026',title='InnoCarnival · семейные технологии',detail='SciencePark,всеактивностибесплатные. Конкретныйworkshopage/EN/регистрацияотдельно.',event_ids=['E078']),
    dict(country='Гонконг · онлайн',date='07.12.2026–24.01.2027',title='Winter Robot Challenge · видео',detail='LowerP3илиниже;UpperP6илиниже. Solo1+coach /team2–4+coach. Foreign/ENнеподтверждены.',event_ids=['C1118','C1119','C1123']),
    dict(country='Сингапур',date='24–25 /27.03.2027',title='BIOGLOW qualifiers и final',detail='ChallengeGrades5–10,Future8Grades4–10. ДедлайнFAQ31января10:00SGT;времяждёмвсёравнораньше. OverseasбезSingaporeWorldquota.',event_ids=['C1107','C1108','C1109','C1110'])],
 evidence_cards=[
    pick('evidence','Сингапур','FLL · новый сезон и зарубежная квота','BIOGLOWFounders/FutureиспользуютразныеhardwareиGrades. FAQOverseasограничиваетWorldFestival.','Стараяregistration2025/26неисключаетрождения2017/2020в2026/27.', ['C1106','C1107','C1109','L445'],[],['sg_fll_season','sg_fll_faq','sg_fll_registration']),
    pick('evidence','Сингапур','NRC и WRO · два национальных маршрута','ScienceCentreNRCимеетKUBO/Lower/Upper/Open/AI;WROSpaceFacultyотдельныйnationalorganiser.','Старые2026даты/cutoffsнебудущиесезоны. Возрастнойпереход7/10в2027можетсменитькатегорию.', ['C1111','C1112','C1113','C1114','C1115','C1116','C1117'],[],['sg_nrc_science','sg_wro','wro_sg_rules']),
    pick('evidence','Гонконг','AIS14 · региональные результаты младших','2026GuangzhouVEXGO:ExcellenceAwardиDriving/AutonomousSkills№1. AIS13победилвсобственномшкольномтурнире.','Триразныекатегории/уровня. Это schoolreport;ниоднойновоймировойпобедынеприписано.', [],['S050'],['ais_go_result','ais_go_internal']),
    pick('evidence','Сингапур','SAS · инженерия начинается в Elementary','Krobotics/coding;G2oceancleanup/G3deliveryrobots;позжеMiddleVEXIQ/HighFRC,VEXV5,MATEROV.','Middle/Highдостижениянеперенесенынамладшегошкольника. ГраницаEALвдвухschoolpagesнеоднозначна.', [],['S051'],['sas_steam','sas_robotics','sas_eal','sas_language']),
    pick('evidence','Сингапур / Гонконг','English · прямое обучение и язык сайта','Worklab/CoboпрямоуказываютENinstruction;Computhinkописываетреальныесменыбезпрямогоязыказанятий.','Computhink22датысохранены,ноEN-фильтробученияихневыдаёткакподтверждённые.', ['L425','L428','L107','L056'],[],['worklab_apprentice','cobo_camps','computhink_0']),
    pick('evidence','Сингапур / Гонконг','Выставки · семейная и профессиональная','InnoCarnivalсемейный;ITAPдетскоеправилонеизвестно;GITEXAIAsiaстрогоover18.','GITEXнесемейнаяпоездкадетей6/9. HKTDCнынешниеусловиявэтомпроходенепрочитаны.', ['E078','E185','E186','E187'],[],['innocarnival','itap_ticket','gitex'])],
 shortlist=[dict(title='Проба без переезда',detail='Однанеделя,отдельныезадачиобоим,проверкаcoach. Дляопытныхдетейоценитькод,механизмыидокументацию,неодинсертификат.',event_ids=['L425','L427','L428','L107','L108']),dict(title='Сезонный результат по настоящим правилам',detail='СначалаGrade/DOB/foreign/EN,потомконкретныйseasonentry. Неоплачиватьпоездкунафиналбезqualifier/teamplace.',event_ids=['C1106','C1107','C1109','C1118','C1123'])],
 steps=[dict(title='Сопоставить школьные ступени',detail='Взять фактические классы,точныеDOBиуровеньанглийского;сопоставитьFLLGradesиHongKongP3/P6,невыводитьклассизвозраста.'),dict(title='Увидеть действующего младшего coach',detail='Пробныйурок/проект;спроситьcurrentteamcode,наставника,частоту,местаобоим,независимостьдетскогокодаиорганизаторскиепротоколы.'),dict(title='Отделить участие от квоты',detail='OverseasSingaporeнаградивмироваяквотаразные;WRO/NRCсамостоятельны;WintercertificateнеWorldFinal. Закладыватьальтернативусвоейнациональнойлиги.'),dict(title='Сверить полный бюджет и язык',detail='Школьныйсчёт,дневнойлагерь2–3часа,жильёсемьи,языктехники,трансфер/питаниеиправилодетскойвыставкиподтвердитьдозаписи.')],sources=[])
for c in f['evidence_cards']:
    c['detail']=c.pop('why');c['limit']=c.pop('gate')
d['asia_english_focus']=f

read_keys=set(urls)-{'gitex_terms'}
known={s['url']for s in d['sources']}
for key in sorted(read_keys):
    if key.startswith('worklab_chart_'):continue
    if urls[key]not in known:d['sources'].append(dict(url=urls[key],title='Сингапур/Гонконг · '+key,checked=CHECKED,evidence='Прочитано релевантное первичное тело; PDFпо указанным страницам, языки и ограничения раздельно.'));known.add(urls[key])
    f['sources'].append(dict(title='Первичный источник · '+key,url=urls[key],checked=CHECKED))
issues=[dict(name=title,status=note,official_alternative=url,checked=CHECKED)for title,note,url in [
 ('FLLregistrationoldseason','Registrationpage2025/26birthcutoffsнеперенесенынаBIOGLOW2026/27;FAQ2027timeиseasonGradesотдельно.',urls['sg_fll_registration']),
 ('NRCgeneralversusLowerhardware','LowerWeDo/Essentiallisted;generalcontrollerlistothermodels. Categorypackneeded;2023awardstableне2026.',urls['sg_nrc_science']),
 ('ComputhinkEnglishnotstated','22реальныеNovember/Decembercohortsсохранены;ENinstructiontagснятдопрямогоподтверждения.',urls['computhink_0']),
 ('SASEALpolicyinconsistency','DetailedEALG4/G5TransitionversusgeneralbeyondGrade4wording;newchildassessmentneeded.',urls['sas_language']),
 ('AISfeesoldyear','Tuitionpageexplicit2025/26не2026/27;неиспользоватьстарыйfeeкакновый.',urls['ais_fees']),
 ('HKTDCaccessfailure','Webopenнеполучилbody;предыдущийHTTP20013bytesForbiddenнепризнанпрочитаннымsource. InnoEx/Electronics2027newdate/childpolicyunknown.','https://www.hktdc.com/event/innoex/en/fair-information'),
 ('Winterforeigngradeandcertificates','Foreignequivalent/ENunknown. GradedcertificatesнеWorldFinalquota;submissionwindowнеочнаяпоездка.',urls['hk_winter'])]]
a=d['completeness_audit'];a['validation_previous']=copy.deepcopy(a['validation']);a.update(version=48,checked=CHECKED,scope='Singapore/HongKong real English cohorts, school-grade routes, results and visitor policy',
 conclusion='43новыекарточки:18дисциплин/этапов,22учебныесмены/программы,3выставки. Двешколыи4результатаразныхуровней. Мировойохватчастичный.',new_ids=[e['id']for e in new],new_profiles=['fll-singapore-bioglow','nrc-singapore','wro-singapore-spacefaculty','hongkong-winter-robot'],
 new_school_ids=['S050','S051'],updated_ids=['E078']+[f'L{n:03d}'for n in range(56,78)]+[f'L{n:03d}'for n in range(107,115)],updated_profile_ids=[],validation=dict(version=48,status='pending',publication='pending'))
a['school_history']['results']=150;a['source_issues']+=issues;a['caveats'].append('v48:СингапурGrade5/4≠возраст9;OverseasбезSGWorldquota;NRCотдельноWRO. Worklab/CoboEnglishпрямой,Computhinkнеизвестный. AISregional/internal≠Worlds. GITEXstrictlyover18.')
d['camp_focus'].update(version=48,checked=CHECKED,added_ids=[e['id']for e in new if e['block']=='Лагеря'],updated_ids=[f'L{n:03d}'for n in range(56,78)]+[f'L{n:03d}'for n in range(107,115)],
 conclusion='446учебныхкарточек. Worklab20фактическихOctobercohortsнаEN;CoboENпрямо. Future5набор/hackathon12–14отдельныеundatedкандидаты. Computhinkязыкнеподтверждён.',validation=dict(version=48,status='pending'))
d['camp_focus']['hack_event_ids'].append('L446')
d['school_focus'].update(version=48,checked=CHECKED,conclusion='51школьноедосье:добавленыAIS HongKongсregional/internalVEXGOиSASсElementarySTEAMpipeline. Новыемладшиемировыетитулынеприписаны;fees/currentteamplacesещёнеизвестны.')
d['asof']=CHECKED;d['expansion_log'].append(dict(version=48,checked=CHECKED,scope='Singapore/HongKong English cohorts,class gates,school results,exhibitions',added=43,new_profiles=4,new_schools=2,new_history=4,status='partial;worldwideobjectivepreserved'))
assert len(new)==43 and len(d['events'])==1755 and len(d['schools'])==51 and len(h['results'])==150
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
receipts=[]
for name in ['receipt.json','receipt-extra.json','receipt-fll.json']:
    for row in json.loads((WORK/'sources-asia-english-v48'/name).read_text()):
        row.pop('path',None);key=row['name'];row['primary_body_read']=key in read_keys
        if key.startswith('worklab_chart_'):row.update(primary_body_read=False,visual_read=True,scope='October2026week/date/age/time/pricechartsvisuallyinspected')
        if key.startswith('wro_sg_'):row['read_scope']='GeneralRulesage/team/ownworktextandpage4visual' if key=='wro_sg_rules' else 'One-pagetermsfullyreadandvisuallyinspected'
        if key=='sas_fees':row['limitation']='Primarypagebodyread;actual2026/27feesPDFnotextracted'
        if key=='gitex_terms':row['limitation']='UnusedtermsURL;admissionverifiedonprimaryhomepagefooter'
        receipts.append(row)
(ROOT/'data/asia-english-source-receipts-v48.json').write_text(json.dumps(dict(version=48,checked=CHECKED,sources=receipts,issues=issues),ensure_ascii=False,indent=2)+'\n')
rpath=ROOT/'data/research-plan.json';r=json.loads(rpath.read_text());r.update(updated=CHECKED,completeness_audit='data/audit-v48.json',latest_validation_previous=r['latest_validation'],latest_validation=dict(version=48,status='pending',publication='pending'))
r['research_passes'].append(dict(version=48,checked=CHECKED,scope='Worldwidegoalcontinuation:Singapore/HongKongprimaryEnglishcohorts,schoolroutes,results,andvisitorpolicy',status='implementation;validationpending',added=43,new_profiles=4,new_schools=2,new_history_results=4))
r['previous_goal_turn_classification']=dict(status='progress',evidence='v47deployed;anonymousbytehashesmatchedall78staticfiles,liveUI/calendarsverified;12cards,1school,9resultsdelivered.',remaining='Fullworldscopeandlocalcountryauditsremainactive.')
r['next_research'].insert(0,'Singapore/HongKongv48:foreignGradeequivalenceandENjudging;HKTDCInnoEx/Electronicsprimaryaccess;new2027camps;schoolcurrentjuniorcoaches/places/fullfees;WorldgoalcontinuesCostaRica/México/LATAMandremainingcountries.')
rpath.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=48,cards=len(d['events']),schools=len(d['schools']),results=len(h['results']),new_ids=[e['id']for e in new]),ensure_ascii=False))
