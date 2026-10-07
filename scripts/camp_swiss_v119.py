"""Selected Swiss primary prices into partial, child-specific budget scenarios."""
from pathlib import Path
from camp_planning_v108 import offer

ROOT=Path(__file__).resolve().parents[1]
BASE='1dc04cb6c894ca9be2f738e47a13b260608751ac'
CHECKED='2026-10-06'
S='https://www.campsuisse.com/'
SD=S+'day-camp-dates-prices/'
SB=S+'register-online/dates-and-prices/'
SF=S+'summer-camp/faq/'
SI=S+'register-online/travel-insurance/'
SP=S+'wp-content/uploads/2025/09/IPID-2025-Summer-BY9-0000215-International-Camp-Suisse-BY9-Youth-Group.pdf'
ST=S+'wp-content/uploads/2017/11/Terms-updated-for-2018.pdf'
L='https://lovellcamps.ch/wp-content/uploads/2026/08/Session-Application-202627.pdf'
LW='https://lovellcamps.ch/winter-camp/'
Y='https://www.lyceum-alpinum.ch/en/summer-camps/junior-day-camp/'
YP='https://www.lyceum-alpinum.ch/wp-content/uploads/2026/09/Flyer-Junior-Day-Camp-2027.pdf'
G='https://www.la-garenne.ch/winter-camps/'
NEW_IDS=['suisse-day-five','suisse-board-matvey','suisse-board-both-seven',
         'lovell-winter-day','lovell-winter-board','lyceum-junior-week',
         'garenne-winter-integration-day','garenne-winter-integration-board']

def unknown(ident,label):return dict(id=ident,label=label,unit='amount',rate=1,min=0)

def build_offers():
    out=[]
    out.append(offer(NEW_IDS[0],'camp-suisse-day','Camp Suisse · обоим днём · 5 будних дней',1000,
      format='day',checked=CHECKED,period_type='season_window',sessions=[['2027-06-21','2027-08-13']],
      sources=[SD,S+'summer-day-camp/',SF,SI],
      optional=[dict(id='return_minibus',label='Минибус туда-обратно · 20 × 5 дней × 2 ребёнка',amount=200)],
      unknown_required=[unknown('day_cover','Страховка двух детей · включение именно в day и нужную доплату уточнить')],
      gate='Дневная программа 5–17 подходит по годам рождения обоим. Тариф относится к пяти будним дням внутри сезона, а не ко всему окну 21 июня–13 августа. Конкретная неделя, индивидуальный иностранный приём и места отдельно. Опция ночёвки CHF 120 не добавлена: допуск 5–6-летних к ночёвке не установлен.',
      included='08:30–17:30, обед, альпийские активности и экскурсии. Это общая программа; полный языковой курс или робототехника в дневном тарифе не обещаны. Минибус: Champéry, Val d’Illiez или Monthey.',
      deposit_note='FAQ летнего лагеря: CHF 500 невозвратного аванса, остаток за 4 недели. Применимость к выбранному пятидневному day-пакету и его отмена неизвестны; аванс не добавлен повторно. В downloads всё ещё договор 2018.',
      scope='CHF 2 000 за пять дней обоих; с выбранным опубликованным минибусом CHF 2 200. Покрытие day, жильё семьи и поездка не установлены.'))
    board_sessions=[['2027-06-19','2027-07-03'],['2027-07-03','2027-07-17'],['2027-07-17','2027-07-31'],['2027-07-31','2027-08-14']]
    for ident,label,children in [(NEW_IDS[1],'Camp Suisse · пансион только Матвею · 2 недели',['matvey']),
                               (NEW_IDS[2],'Camp Suisse · пансион обоим · Оскар только после 7-летия',['matvey','oscar'])]:
      out.append(offer(ident,'camp-suisse-board',label,4400,format='boarding',checked=CHECKED,
        children=children,base_by_child={k:4400 for k in children},sessions=board_sessions,sources=[SB,S+'summer-camp/',SF,SI,SP,ST],
        optional=[dict(id='two_parents',label='Два взрослых · Geneva → лагерь → Aigle в тот же день',amount=200)],
        unknown_required=[unknown('cover_topup','Дополнительное покрытие выбранных детей · после проверки полиса 2027')],
        gate=('Пансион 7–17. Матвей 2017 подходит по возрасту; Оскар не включён в этот счёт и должен иметь отдельную программу/уход с семьёй.' if len(children)==1 else 'Пансион 7–17: обоим только после 7-летия Оскара к началу выбранной смены. В 2027 ему будет 6–7; без точного возраста этот сценарий условный. До 7 лет рассматривать day, не обычный пансион.')+' Возраст не подтверждает места или приём.',
        included='Пансион, три приёма пищи и snack, занятия/экскурсии и оборудование, постель, прачечная раз за две недели, языковые занятия EN/FR/ES и сопровождение. Страховка и финансовая защита заявлены в цене. Детский Geneva/Aigle transfer включён только в официальные дни и часы: прибытие Geneva 09–16, вылет 11–17.',
        deposit_note='CHF 500 за каждого невозвратного аванса уже в цене; остаток за 4 недели. Текущий сайт ссылается на договор 2018 и краткий полис из папки 2025: применимость к 2027 ещё проверить. В полисе нужна регистрация у врача в домашней стране; полный договор покрытия выдают после регистрации. Это не обещание возврата при любой отмене.',
        scope=('CHF 4 400 — только Матвей; стоимость ухода/лагеря Оскара отсутствует.' if len(children)==1 else 'CHF 8 800 — база двух детей, только если Оскар достиг 7 лет.')+' Поездка и достаточность включённого покрытия для семьи с ПМЖ Коста-Рики и гражданством Мексики/РФ не подтверждены. Взрослый трансфер заканчивается в Aigle, не в аэропорту.'))
    starts=['2026-12-13','2026-12-20','2026-12-27','2027-01-03','2027-01-10','2027-01-17','2027-01-24','2027-01-31','2027-02-07','2027-02-14','2027-02-21','2027-02-28','2027-03-07','2027-03-14']
    import datetime
    def shifted(s,n):return (datetime.date.fromisoformat(s)+datetime.timedelta(days=n)).isoformat()
    for ident,label,base,fmt,reg in [(NEW_IDS[3],'Lovell · обоим зимой днём · 1 неделя',1900,'day',50),
                                   (NEW_IDS[4],'Lovell · обоим зимний пансион · 1 неделя',2600,'boarding',100)]:
      sessions=[[shifted(s,1),shifted(s,5)] if fmt=='day' else [s,shifted(s,6)] for i,s in enumerate(starts,1) if fmt=='day' or i not in [5,6,7]]
      out.append(offer(ident,'lovell-winter-'+('day' if fmt=='day' else 'board'),label,base,
        format=fmt,checked=CHECKED,sessions=sessions,sources=[L,LW],
        required=[dict(id='weekly_registration',label=f'Невозвратная регистрация · {reg} × 2 ребёнка × 1 неделю',amount=reg*2)],
        unknown_required=[unknown('gear_cover','Нужное снаряжение и медстраховка обоих · свой комплект / rental / полис уточнить')],
        gate='PDF сезона 2026/27: все гражданства, 5–16 лет; веб-описание board 5–15, нижняя граница совпадает и обоим по годам подходит. Нужны состояние здоровья и подписанная врачом справка за 30 дней. '+('Day: понедельник–пятница; PDF 09–17, в веб-расписании другое время окончания, уточнить.' if fmt=='day' else 'Пансион: воскресенье–суббота. Недели 5–7, 10–30 января 2027, исключены: PDF прямо «No boarding spaces available».')+' Наличие места отдельно.',
        included='Лыжи/сноуборд, занятия и ski pass, английский или французский на выбор, afternoon activities, supplies, экскурсии и транспорт до склонов. '+('Day: обед и snacks; weekends отдельно.' if fmt=='day' else 'Board: проживание, питание и snacks; weekend programme для остающихся на 2+ смены.')+' Это спортивно-языковая программа, не STEM-интенсив. PDF предлагает язык либо afternoon programme; одновременный полный объём не обещан.',
        deposit_note='CHF 1 000 аванса за ребёнка уже внутри базы. Письменная отмена минимум за 30 дней позволяет возврат аванса; регистрационный сбор невозвратный. Остаток и extras за 30 дней. Уход, исключение и временное отсутствие не уменьшают цену. Итоговый договор и доплаты отдельно.',
        scope=f'База плюс обязательная регистрация: CHF {(base+reg)*2:,} для двух детей за одну неделю. Личный ski/snowboard/helmet rental, медстраховка, аэропорт и door-to-door bus исключены. Трансферы вводить в поле поездки, не второй раз в extras. T-shirt PDF исключает, веб включает: итог уточнить.'))
    out.append(offer(NEW_IDS[5],'lyceum-junior','Lyceum Junior · обоим днём · Матвей только пока ему 9',1000,
      format='day',checked=CHECKED,sessions=[['2027-07-05','2027-07-09'],['2027-07-12','2027-07-16'],['2027-07-19','2027-07-23'],['2027-07-26','2027-07-30']],sources=[Y,YP],
      unknown_required=[unknown('health_liability','Медицинская, accident и liability страховка двух детей · стоимость уточнить')],
      gate='Junior Day строго 6–9. Оскар в 2027 6–7 подходит по возрасту; Матвей 9–10 — этот тариф только пока ему 9. После 10-летия нужен другой поток, не этот счёт. Ночёвок нет. Точная возрастная дата и места отдельно.',
      included='Понедельник–пятница 08:30–16:00, 16 уроков EN или DE в неделю, материалы, обед, afternoon activities. Сайт включает местный pick-up/drop-off; маршрут максимум St. Moritz/Madulain и выбор with/without ещё подтвердить. Аэропорт не обещан. Общее языковое приключение, не Digital Skills старшего пансиона.',
      deposit_note='Отмена за 30 дней без расходов; за 29–15 дней возврат 50%; за 14 и меньше, no-show, поздний заезд или ранний отъезд возврата нет. Страховки обеспечивают родители; включённой медицинской страховки не заявлено.',
      scope='CHF 2 000 за одну опубликованную неделю обоих, только при соблюдении возраста. Страховка, жильё семьи и поездка отдельно.'))
    gi=[['2027-01-10','2027-01-23'],['2027-01-24','2027-02-06'],['2027-02-07','2027-02-20'],['2027-02-21','2027-03-06'],['2027-03-07','2027-03-19']]
    for ident,label,base,fmt in [(NEW_IDS[6],'La Garenne · Winter Integration обоим днём · от 2 недель',7500,'day'),
                               (NEW_IDS[7],'La Garenne · Winter Integration обоим в пансионе · от 2 недель',7950,'boarding')]:
      out.append(offer(ident,'garenne-integration',label,base,format=fmt,checked=CHECKED,price_basis='from',sessions=gi,sources=[G],
        unknown_required=[unknown('winter_invoice','Обязательные зимние доплаты, страховка и снаряжение обоих · полного прайса нет')],
        gate='Winter Integration 5–14: обоим подходит по возрасту, но нужны индивидуальный приём, школьное размещение и язык выбранного класса. Это интеграция в обычные занятия школы и минимум две ski sessions в неделю. Super Ski и English+Ski с 8 лет — другие программы; Оскару их не подставлять. '+('Day: только понедельник–пятница 08:30–16.' if fmt=='day' else 'Board: полный срок на кампусе; условия ночного сопровождения младших отдельно.')+' 7–19 марта: во вторую неделю лыж нет.',
        included='Регулярные школьные занятия и минимум две лыжные сессии за неделю по описанию. '+('Дневное посещение в будни; пансион не включён.' if fmt=='day' else 'Проживание на кампусе весь опубликованный период.')+' Полное питание, rentals, transfers и страховку зимней версии нельзя выводить из летнего договора.',
        deposit_note='Зимние General Conditions и полный invoice выдаёт Admissions по запросу. Зимние депозит, возврат и семейная скидка не опубликованы на этой странице. Летнюю скидку 10% и летние CHF 500 автоматически не применять.',
        scope=f'От CHF {base*2:,} за двух детей в минимальном опубликованном формате. Это нижняя опубликованная база, не окончательный счёт. Список показывает границы сессий: day внутри них только будни; последний блок 7–19 марта короче 14 календарных дней.'))
    assert [q['id'] for q in out]==NEW_IDS
    return out

def extend_planning_v119(d):
    m=d['camp_planning'];out=build_offers();existing={q['id'] for q in m['offers']}
    authored={q['id']:q for q in out}
    m['offers']=[authored.get(q['id'],q) for q in m['offers']]+[q for q in out if q['id'] not in existing]
    m.update(version=119,asof=CHECKED)
