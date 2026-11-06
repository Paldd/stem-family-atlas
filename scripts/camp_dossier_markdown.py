"""Human-readable companion to the current full camp-programme JSON export."""

def render(report):
    profiles=report['profiles'];countries=len({p['iso'] for p in profiles})
    lines=['# Каникулы 2026–2027: подробные досье',
           f"Состояние базы: {report['asof']}. {len(profiles)} досье в {countries} странах. Даты проверки отдельных источников приведены в каждом досье.",
           report['scope'],'## Как читать']
    lines += ['- '+x for x in report['methodology']]
    by_slug={p['slug']:p for p in profiles}
    lines += ['## Выбор для семьи']
    for row in report['shortlist']:
        lines += ['### '+row['label'],row['reason']]
        for slug in row['slugs']:
            p=by_slug[slug]
            lines.append('- '+p['provider']+' · '+p['country']+' · '+p['editorial_reason'])
    lines += ['## Смета',report['budget_method']]
    def field(label,value):
        if value is not None and value!='':lines.append('**'+label+':** '+str(value))
    def child_rows(fits):
        for key,label in [('matvey','Матвей'),('oscar','Оскар')]:
            fit=fits.get(key,{})
            field(label,fit.get('detail'))
    for p in profiles:
        lines += ['## '+p['id']+' · '+p['provider'],p['country']+' · '+p['place']]
        for label,key in [('Проверено','checked'),('Возраст','age'),('Язык','language'),('Программа','programme'),('Проживание','accommodation')]:field(label,p.get(key))
        field('Даты / статус',p['timing']['label'])
        field('Цена / год',str(p['price'].get('season') or p['price'].get('year') or 'не установлен')+' · '+p['price']['label'])
        for label,key in [('Включено','included'),('Доплаты','extras'),('Оплата','deposit')]:field(label,p['price'].get(key))
        child_rows(p['family_fit']);field('Почему в отборе',p['editorial_reason'])
        if p['questions']:lines += ['### Перед заявкой']+['- '+q for q in p['questions']]
        for v in p['timing'].get('session_details',[]):
            lines.append('### '+str(v.get('label') or 'Даты и условия смены'))
            field('Даты / статус',v['start']+' — '+v['end'])
            for label,key in [('Место','place'),('Возраст','age'),('Цена','price'),('Программа','programme'),('Проживание','accommodation'),('Доплаты','extras'),('Оплата','deposit'),('Условия участия','entry')]:field(label,v.get(key))
            for s in v.get('sessions',[]):
                lines.append('- '+s['date']+' · '+s.get('start_time','')+'–'+s.get('end_time','')+' · '+s.get('timezone','')+' · '+s.get('topic',''))
            if v.get('availability'):field('Наличие мест',v['availability'].get('label') or v['availability'].get('status'))
            if v.get('family_fit'):child_rows(v['family_fit'])
            lines += ['- '+q for q in v.get('questions',[])]
            if v.get('source'):lines.append('[Источник]('+v['source']+')')
        lines.append('### Источники')
        lines += ['- ['+s['title']+']('+s['url']+') · '+s['checked'] for s in p['sources']]
    lines += ['## Не закрытые проверки']
    for g in report['gaps']:
        if isinstance(g,str):
            lines.append('- '+g)
            continue
        lines += ['### '+g['country']+' · '+g['provider'],g['detail'],g['next_action']]
        if g.get('url'):lines.append(g['url'])
    return '\n\n'.join(lines)+'\n'
