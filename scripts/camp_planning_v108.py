"""Source-based family budget scenarios; never parse free-text fees as a full quote."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CHECKED='2026-10-05'
BASE='5b0911e3833e1f5bb28ecadc195d26276d9c281d'
L='https://cdn.leselfes.com/wp-content/uploads/2026/07/2027-Summer-Camp-Registration-Form_Digital_avec-champs.pdf'
G='https://www.la-garenne.ch/summer/repository/summer-conditions.pdf'
T='https://summer.tasis.ch/dates-and-fees'
TF='https://summer.tasis.ch/admissions/faq'
F='https://fr.ermitage.fr/activities/holidaycamp'

def offer(ident,slug,label,base,**kwargs):
    q=dict(id=ident,slug=slug,label=label,currency='CHF',price_year=2027,children=['matvey','oscar'],
      base_by_child=dict(matvey=base,oscar=base),discount_second=0,required=[],unknown_required=[],optional=[],
      sources=[],sessions=[],gate='',deposit_note='',included='',unknown_trip=['travel','lodging','misc'],
      scope='Опубликованная часть стоимости двух детей. Полный счёт и места подтверждаются организатором.',checked=CHECKED)
    q.update(kwargs);return q

def build():
    offers=[]
    for ident,label,base,start,end in [('leselfes-june','Les Elfes · пансион 6–19 июня 2027',4990,'2027-06-06','2027-06-19'),('leselfes-july','Les Elfes · пансион 4–17 июля 2027',6500,'2027-07-04','2027-07-17')]:
        offers.append(offer(ident,'les-elfes',label,base,format='boarding',sessions=[[start,end]],sources=[L],
          required=[dict(id='registration',label='Регистрация · 150 × 2 ребёнка',amount=300),dict(id='health',label='Обязательная медстраховка · 120 × 2 недели × 2 ребёнка',amount=480)],
          optional=[dict(id='robotics',label='Робототехника Матвею · один мастер-класс на полдня',amount=180,min_matvey_age=10),dict(id='cancel',label='Страхование отмены · 80 × 2 недели × 2 ребёнка',amount=320),dict(id='geneva',label='Групповой трансфер Женева туда-обратно · 190 × 2',amount=380)],
          gate='Основной лагерь 6–17. Оскар в 2027 не достигает 10 лет и в Robotics не включается. Матвею Robotics доступна только после 10-летия; это один workshop, а не вся смена. Точный возраст на старт и места отдельно.',
          deposit_note='Аванс CHF 1 000 за ребёнка входит в цену и повторно не добавляется. Остаток за 30 дней; стандартный добровольный отказ не даёт автоматического возврата. У страховки отмены свои основания и удержание аванса.',
          included='Комната на 4 ребёнка с санузлом, полное питание, базовые занятия и экскурсии. Обязательный workshop Shelter Building 6+ включён; другой выбранный workshop оплачивается отдельно. Языковые уроки, одежда в прачечной и другие опции могут добавляться.',
          unknown_required=[]))
    for ident,label,base,fmt,sessions in [
      ('garenne-day','La Garenne · два ребёнка днём · 2 недели',6550,'day',[['2027-06-28','2027-07-09'],['2027-07-12','2027-07-23'],['2027-07-26','2027-08-06']]),
      ('garenne-board','La Garenne · два ребёнка в пансионе · 2 недели',7200,'boarding',[['2027-06-27','2027-07-10'],['2027-07-11','2027-07-24'],['2027-07-25','2027-08-07']])]:
        offers.append(offer(ident,'la-garenne',label,base,format=fmt,sessions=sessions,sources=[G,'https://www.la-garenne.ch/summer-camps/apply-online/'],discount_second=.10,
          unknown_required=[dict(id='insurance_days',label='Страховка · сумма оплачиваемых дней обоих детей',unit='child_days',rate=10,min=2),dict(id='pocket_age',label='Карманные деньги · 2 недели для обоих',unit='matvey_age',rates={'9':120,'10':160})],
          optional=[dict(id='robotics',label='Robotics & 3D · три занятия только Матвею 8–12',amount=500)],
          gate='Выбранный тариф общей программы для 5–12 лет; техника 8–12 подходит Матвею, Оскару 6–7 не подходит. Скидка 10% на базовую цену второго ребёнка требует одной смены и одинакового day или boarding; смешанные форматы братьев не разрешаются. Если родители живут рядом, дети должны быть day students.',
          deposit_note='CHF 500 за ребёнка — включённая невозвратная часть цены, не новая доплата. Отмена за 65 дней и раньше: возврат минус 500; позже возврата нет. Полная оплата подтверждает место.',
          included='EN или FR уроки, занятия, материалы, транспорт мероприятий, налоги/VAT. Day: обед и snack; первая неделя включает субботу. Boarding: жильё, питание и прачечная; Geneva transfer включён только в официальное время.',
          scope='База после семейной скидки, затем страховка и карманные деньги. Число оплачиваемых страховых дней нельзя выводить автоматически из дней пансиона или посещения.'))
    sessions=[['2027-06-27','2027-07-17'],['2027-07-19','2027-08-08']]
    for ident,label,osc,fmt,gate in [
      ('tasis-day-minnows','TASIS · CDE + Minnows до 15:00 · 3 недели',3500,'day','Матвей: CDE 7–10. Этот тариф Оскара относится к Minnows 4–6, только дневной; при 7-летии к первому дню нужен CDE. Разное время завершения групп и транспорт семьи отдельно.'),
      ('tasis-day-minnows-long','TASIS · CDE + Minnows до 17:30 · 3 недели',4500,'day','Матвей: CDE 7–10. Этот тариф Оскара — Minnows 4–6 с продлённым днём до 17:30; после 7-летия нужен CDE. Точный возраст на первый день определяет поток.'),
      ('tasis-day-cde','TASIS · оба CDE днём · 3 недели',4500,'day','Оба должны входить в CDE 7–10 на первый день. Оскару 2020 г.р. в 2027 будет 6–7: этот сценарий доступен только после его 7-летия.'),
      ('tasis-board-cde','TASIS · оба CDE в пансионе · 3 недели',9200,'boarding','Пансион CDE 7–10 для обоих только если Оскару исполнилось 7 к первому дню. Minnows до 7 — только day. Братьев не селят вместе по FAQ; общая программа не обещает робототехнику.')]:
        base=9200 if fmt=='boarding' else 4500
        offers.append(offer(ident,'tasis',label,base,base_by_child=dict(matvey=base,oscar=osc),format=fmt,sessions=sessions,sources=[T,TF],gate=gate,
          unknown_required=[dict(id='medical_total',label='Страховка day students · стоимость выбранного покрытия',unit='amount',rate=1,min=0)] if fmt=='day' else [],
          deposit_note='CHF 1 500 невозвратного аванса за ребёнка уже в цене. Остаток до 15 мая; позже поступившим — вся цена в течение 7 дней от invoice. Возврат до 15 мая возможен минус аванс; после — только документированные исключения.',
          included='Day: обучение и обед, будни без суббот/воскресений. Boarding: обучение, жильё и питание; FAQ добавляет книги, прачечную и medical/accident insurance для non-Swiss residents. Day students предъявляют свою страховку либо покупают TASIS по отдельному запросу.'))
    offers.append(offer('ermitage-autumn','ermitage-holiday','Ermitage · 19–23 октября 2026 · дневной',610,currency='EUR',price_year=2026,format='day',sessions=[['2026-10-19','2026-10-23']],sources=[F],
      gate='Текущая программа 4–10, группы 4–6 и 7–10; обоим нужны точный возраст и место. Французско-английское погружение; это общая тематическая программа Wizards, не доказанный интенсив робототехники.',
      unknown_required=[dict(id='meals_total',label='Питание обоих детей · включение и цену ещё подтвердить',unit='amount',rate=1,min=0)],
      included='Опубликованы двуязычные занятия и тематическая программа; обед и его включение в тариф не установлены в этой странице.',
      deposit_note='Оплата, отмена и применимость семейных скидок в текущей странице не разъяснены. EUR 610 относится к осени 2026 и не переносится на каникулы 2027.'))
    return dict(schema_version=1,version=108,asof=CHECKED,title='План каникул и семейная смета',offers=offers,
      methodology=['Отбор по месяцу использует опубликованный интервал; сезонное окно и точная смена остаются разными типами даты.','Порядок по возрасту помогает рассмотреть кандидатов; он не является мировым рейтингом качества лагерей.','Фиксированные компоненты взяты из первичных прайсов и договоров. Пропущенная обязательная сумма остаётся неизвестной, а не нулём.','Депозит в составе тарифа не добавляется второй раз. Скидка применяется только в условиях конкретного оператора.','Перелёт, жильё родителей и дополнительные расходы вводятся как ваши оценки в валюте лагеря. Они не становятся официальной ценой.','Ссылка сохраняет фильтры справочника. Введённые суммы сметы остаются на открытой странице и не отправляются оператору.'],
      fully_audited_countries=0,worldwide_complete=False,external_actions=dict(applications_submitted=False,payments_made=False,messages_sent=False))

if __name__=='__main__':
    p=ROOT/'data/catalog.json';d=json.loads(p.read_text());d['camp_planning']=build();p.write_text(json.dumps(d,ensure_ascii=False,indent=2))
    print(json.dumps(dict(offers=len(d['camp_planning']['offers']),new_camp_dossiers=0,all_old_events_retained=True)))
