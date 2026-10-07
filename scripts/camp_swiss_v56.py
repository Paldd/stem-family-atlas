"""Distinct Regent tracks and source-linked JFK day/boarding variants."""
from datetime import date,timedelta

def add_swiss_programmes(add,src,fit,profiles,checked):
    dates=[['2027-07-04','2027-07-16'],['2027-07-18','2027-07-30'],['2027-08-01','2027-08-13']]
    sources=[src('Треки, даты и цены 2027','https://www.regentcamps.ch/'),src('FAQ: English throughout the day / проживание','https://www.regentcamps.ch/copy-of-faq'),src('Заявка и условия: переход 2026→2027','https://www.regentcamps.ch/enrolment')]
    tracks=[
        ('regent-labs','Labs & Passions','8–14; Life Skills отдельно 10–13','science,general,languages,sport',8200,
         'Утренний выбор STEM (science / technology / engineering / maths) или Young Communicators. Life Skills только 10–13. Во второй половине дня одна Passion на пять занятий: спорт, Art in Nature, golf или racket sports. Комплект робота, язык STEM и технический проект пока не раскрыты.',
         fit('candidate','Возраст Labs 8–14 подходит; Life Skills только после 10-летия.'),fit('later','Минимум основной программы 8 лет; в 2027 Оскару 6–7.'),['technical','general']),
        ('regent-leadership','Leadership','13–16','general,entrepreneurship,sport',8200,
         'Заявлены 42 часа личного развития и outdoor challenges: коммуникация, эмоциональная осознанность, здоровые привычки и командные горные задания. Не робототехническая лига.',
         fit('later','Трек с 13 лет; сохраняем на будущее.'),fit('later','Трек с 13 лет.'),[]),
        ('regent-pre-university','Pre-University','15–17','general,science,sport',11900,
         'Выбор IB & IGCSE Maths или SAT Preparation; 36 часов за две недели и шесть adventure afternoons. Это подготовка к учёбе, не университетская степень или гарантия поступления.',
         fit('later','Трек с 15 лет; будущая ступень.'),fit('later','Трек с 15 лет.'),[])]
    for slug,title,age,themes,fee,programme,mat,osc,short in tracks:
        add(slug,'Régent Camps · '+title,'Швейцария','CHE','Crans-Montana',themes,'boarding',age,
            'FAQ заявляет English throughout the day. Для Leadership / Pre-University требуется хороший английский. FAQ содержит лето 2026; язык конкретного STEM Lab и условия 2027 подтвердить.',
            programme,'2027: 04–16.07, 18–30.07, 01–13.08. Набор в ноябре 2026, подробный programme coming soon; точный ноябрьский день не указан.',
            dict(year=2027,label=f'CHF {fee:,}/2 недели + CHF 400 pocket money.',included='Пансион; FAQ описывает питание, прачечную, emergency cover и Geneva shuttle в официальные дни/часы. Состав пакета 2027 подтвердить.',extras='Pocket money — личный расходный фонд, не учебный fee. Дополнительный трансфер, UM, дорога и cancellation cover отдельно. Невозвратный application fee CHF 1 000 описан в enrolment; включение в цену не установлено.',deposit='На странице набора 2027 даты отмены/единого платежа всё ещё 2026. Актуальные financial conditions 2027 и зачёт application fee получить письменно; старые сроки не переносим.'),
            'Двухместные комнаты, санузел на две комнаты; пол/возраст разделены, сотрудники на этаже. Дневной формат 2027 не заявлен.',mat,osc,
            'Отдельный возрастной трек одного оператора. Labs — кандидат Матвею; старшие направления показаны как будущие ступени, а не доступные сейчас лагеря.',
            ['Подтвердить язык выбранного трека, часы и материалы STEM, полный invoice и financial conditions 2027.'],sources,status='partial_2027',priority=short,confirmed=['EN'],sessions=dates)
        p=profiles[-1];p['language_evidence_role']='camp_life';p['operator_key']='regent-camps'
        p['timing']['session_details']=[dict(start=start,end=end,label=title,price=f'CHF {fee:,} + CHF 400 pocket money / 2 недели',place='Crans-Montana',source='https://www.regentcamps.ch/') for start,end in dates]
    pdf='https://swissoutdoorcamp.ch/downloads/JFK%20Camp%20fees%20conditions%202027.pdf'
    add('jfk-outdoor','JFK Swiss Outdoor Camp','Швейцария','CHE','Saanen / Gstaad','general,sport,science','day,boarding','6–14 на главных страницах; один старый блок school camps говорит 6–13',
        'Язык именно summer camp не подтверждён прочитанными страницами. Английская школьная программа и английский сайт не доказывают EN всех outdoor instructors.',
        'Outdoor learning, командные задачи и природа: недели Water / Mountain / Rock повторяются дважды. Подтверждённого робототехнического интенсива нет. День — только Пн–Пт; пансион — Вс–Вс. Некоторые активности и экскурсии меняются.',
        '2027: 04.07–15.08, варианты 1/2/3 недели. Недельные варианты рассчитаны по опубликованным правилам Вс–Вс и Пн–Пт; PDF перечисляет 2/3-недельные интервалы, но содержит опечатки отдельных дат. Заявки открываются 02.11.2026.',
        dict(year=2027,label='Пансион CHF 3 300 / 6 600 / 9 900 за 1/2/3 недели. Дневной CHF 2 700 / 5 400 / 8 100. HTML и визуально проверенный PDF 2027 совпадают.',included='День: обед и основные занятия. Пансион: жильё, все meals, вечер/выходные, прачечная и постельное бельё. Medical/accident cover есть; private liability: PDF включает, admissions исключает — подтвердить.',extras='PDF: трансфер за направление Geneva CHF 520 / Zurich 800; shared Geneva 300 / Zurich 450. Cancellation cover, личные расходы и UM отдельно; bath/pool towels не включены. Семейное жильё при day camp отдельно.',deposit='PDF 2027: до 01.05 возврат 70%, после — удержание полной суммы; уход раньше срока без возврата. Зачисление после полной оплаты. Security deposit упомянут без суммы. Условия страховки и актуальный invoice проверить.'),
        'Пансион в швейцарских chalet либо дневное посещение. Недельные даты форматов различаются.',
        fit('candidate','Соответствует обеим опубликованным границам 6–13/14; язык и готовность к outdoor подтвердить.'),fit('candidate','В лето 2027 минимум 6 лет выполнен; проверить младшую группу, язык и готовность к пансиону.'),
        'Новый общий швейцарский outdoor-кандидат для обоих с опубликованными 2027 тарифами и форматами. Для инженерной глубины нужен другой технический курс.',
        ['Подтвердить EN и младшую группу, liability insurance, security deposit и полный семейный расчёт. Не считать открытый portal или capacity counter доказательством зачисления.'],
        [src('Основная программа / возраст','https://www.swissoutdoorcamp.ch/'),src('Даты и тарифы 2027','https://swissoutdoorcamp.ch/admissions.html'),src('Тарифы и условия 2027 · PDF визуально сверено',pdf),src('Школьная страница camp / day vs boarding','https://jfk.ch/camps/'),src('Открытие заявок 02.11.2026','https://www.swissoutdoorcamp.ch/applicationnew.html')],status='published_2027',priority=['both','general','boarding'])
    p=profiles[-1];p['operator_key']='jfk-swiss-outdoor';p['timing']['session_details']=[]
    for weeks in [1,2,3]:
        for index in range(7-weeks):
            sunday=date(2027,7,4)+timedelta(days=7*index)
            for boarding in [True,False]:
                start=sunday if boarding else sunday+timedelta(days=1)
                end=sunday+timedelta(days=7*weeks) if boarding else sunday+timedelta(days=7*(weeks-1)+5)
                label=('Пансион' if boarding else 'Дневной · Пн–Пт')+f' · {weeks} нед.'
                v=dict(start=start.isoformat(),end=end.isoformat(),label=label,price=f'CHF {(3300 if boarding else 2700)*weeks:,} / {weeks} нед.',place='Saanen / Gstaad',source=pdf if weeks>1 else 'https://swissoutdoorcamp.ch/admissions.html',formats=['boarding' if boarding else 'day'],date_scope='camp_session' if boarding else 'day_camp_window',date_precision='published_rule',date_status='Опубликованное правило · даты рассчитаны',accommodation='Швейцарский пансион' if boarding else 'Дневной; выходные не входят, родители организуют жильё.',programme=p['programme'],proof='Даты рассчитаны по официальному диапазону и правилу недель. Это альтернативные варианты длительности; day camp не посещается по выходным. PDF 2027 визуально сверён с актуальной загрузкой; опечатки не копируются как валидные даты.')
                p['timing']['sessions'].append([v['start'],v['end']]);p['timing']['session_details'].append(v)
    opened=dict(start='2026-11-02',end='2026-11-02',label='Открытие заявок на лето 2027',price='Тариф выбранного пакета — в досье; время открытия не указано',place='Онлайн / Saanen',source='https://www.swissoutdoorcamp.ch/applicationnew.html',date_scope='registration_open',date_precision='published_date',programme='Объявленное открытие заявок на лето 2027, а не учебный день и не подтверждённое место.')
    p['timing']['sessions'].append([opened['start'],opened['end']]);p['timing']['session_details'].append(opened)

