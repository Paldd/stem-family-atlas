"""Link researched camp dossiers to stable catalogue events without fuzzy merges."""
from copy import deepcopy
import re

# Explicit relations: a shared operator/domain is not proof of an identical track.
RELATED = {
    'jersey-college-creative-minds-robotics': ['L693'],
    'guernsey-library-twine-game-design': ['L694'],
    'guernsey-library-sphero-taster': ['L695'],
    'giiyo-douala-summer-tech-bootcamp': ['L696'],
    'graines2genie-cotonou-kids-coding-camp': ['L697'],
    'bsi-panama-robotics': ['L687'],
    'bsi-panama-minar-y-crear': ['L688'],
    'la-garenne': ['L249','L250','L251','L252','L253','L254'],
    'aiglon': ['L419'], 'rosenberg': ['L447','L448'],
    'brillantmont': ['L168','L169'], 'abi-paris': ['L229'],
    'techcamp-uk': ['L182'], 'garna': ['L273'],
    'hfarm': ['L308','L309','L313','L314'], 'typa': ['L144'], 'tas': ['L021'],
    'xcl': ['L183'], 'nullspace': ['L016'], 'newtonshow': ['L186','L187'],
    'tokyo-coding': ['L201'], 'harrow-appi': ['L202'], 'id-tech': ['L007'],
    'camp-invention': ['L009'], 'wonder-camp': ['L193'],
    'ciberbots': ['L116','L117','L118','L451','L452','L453'],
    'programable': ['L147','L148'], 'village-leysin': ['L398','L399'],
    'mount-view-camps':['L119'], 'cenfotec-makers':['L139'],
    'robotecnia-holidays':['L028'], 'conversa-tech':['L121'],
    'liota-winter':['L141'], 'campo-aventuras':['L153'],
    'worklab-apprentice':['L425','L430','L435','L440'],
    'worklab-junior':['L426','L431','L436','L441'],
    'worklab-senior':['L427','L432','L437','L442'],
    'worklab-spike':['L428','L433','L438','L443'],
    'worklab-ai':['L429','L434','L439','L444'],
}
REUSE_DATES = {
    'jersey-college-creative-minds-robotics': RELATED['jersey-college-creative-minds-robotics'],
    'guernsey-library-twine-game-design': RELATED['guernsey-library-twine-game-design'],
    'guernsey-library-sphero-taster': RELATED['guernsey-library-sphero-taster'],
    'giiyo-douala-summer-tech-bootcamp': RELATED['giiyo-douala-summer-tech-bootcamp'],
    'brillantmont':['L168','L169'], 'abi-paris':['L229'],
    'tokyo-coding':['L201'], 'harrow-appi':['L202'],
    'programable':['L147','L148'],
    'cenfotec-makers':['L139'],
    'worklab-apprentice':['L425','L430','L435','L440'],
    'worklab-junior':['L426','L431','L436','L441'],
    'worklab-senior':['L427','L432','L437','L442'],
    'worklab-spike':['L428','L433','L438','L443'],
    'worklab-ai':['L429','L434','L439','L444'],
}
TECHSPARK_GAMES = ['L%03d' % i for i in list(range(122,131))+list(range(279,292))]
RELATED.update({'techspark-games':TECHSPARK_GAMES,'techspark-lego':['L131'],
                'lyceum-board':['L170','L171','L172'],'life-tech':['L180'],
                'stgeorge-barcelona':['L382','L383'],'ai-alicante':['L385']})
REUSE_DATES['techspark-games']=TECHSPARK_GAMES
RELATED.update({'kidsrobots-kids':['L347'],'kidsrobots-mini':['L%03d'%i for i in range(339,347)],'natuk-robotics':['L227','L228'],'costablanca-robotics':['L414'],'logiscool-spain-wedo':['L422']})
REUSE_DATES['kidsrobots-mini']=RELATED['kidsrobots-mini']
RELATED.update({slug:['L033'] for slug in ['techlab-chile-kids-holidays','techlab-chile-junior-holidays','techlab-chile-coding-afternoon']})
SEASON_WINDOWS = {'prefleuri','aiglon','rosenberg','newtonshow','ilsc-ubc','yres-sports-steam','yres-ai-robotics','swallowdale-forest','lacunza-general','madrid-chess-robotics'}
RELATED.update({'troonic-robotics-camp':['L149','L150'],
                'wecode-pocitos-lab':['L155'], 'wecode-pocitos-ia':['L157'],
                'wecode-pocitos-minecraft':['L159']})
GENERAL_STAYS = {'les-elfes','la-garenne','tasis','le-rosey','village-leysin','weequahic-general'}
RELATED.update({'aiglon-classic-board':['L419'], 'aiglon-classic-day':['L419'],
                'helvetic-zug-summer':['L221','L222','L223'],
                'helvetic-zurich-summer':['L224','L225','L226']})
REUSE_DATES.update({'helvetic-zug-summer':['L221','L222','L223'],
                    'helvetic-zurich-summer':['L224','L225','L226']})
RELATED.update({'grove-flight':['L143'], 'asij-chofu':['L454']})
REUSE_DATES['grove-flight']=['L143']
RELATED.update({'newtech-autumn-art':['L132'], 'newtech-christmas-film':['L133'], 'newtech-christmas-art':['L134']})
RELATED.update({
    'ntrc-myapp-union-island': ['L660'],
    'ntrc-myapp-mountain-view': ['L661'],
    'ntrc-myapp-st-vincent-grammar': ['L662'],
    'anguilla-robotics-association-summer': ['L663'],
    'orbtronics-junior-saint-lucia': ['L664'],
    'orbtronics-innovation-academy': ['L665'],
    'orbtronics-eccu-ai-python-summer': ['L666'],
    'dominica-cardtp-cybercreators': ['L667'],
    'dominica-state-college-summer': ['L668'],
    'grenada-steam-center-bridge': ['L669'],
    'wepala-robotics-summer-trinidad': ['L671'],
    'wepala-python-holidays-online': ['L672'],
})
RELATED.update({
    'brunei-studysmartable-robotics': ['L674'],
    'brunei-seria-selyi': ['L675'],
    'brunei-bicta-plus-primary': ['L676'],
    'bermuda-toya-holiday-primary-2026-2027': ['L677'],
    'bermuda-connectech-after-school': ['L679'],
    'bermuda-connectech-cubesat': ['L680'],
    'bvi-summer-robotics-camp': ['L681'],
    'st-kitts-robomindset-summer': ['L682'],
    'cook-islands-cocobots-club-2027': ['L683'],
    'cook-islands-kuki-code-avengers': ['L684'],
    'cook-islands-kuki-code-avengers-holidays': ['L685'],
    'bermuda-bzs-science-club': ['L686'],
})
REUSE_DATES.update({'newtech-autumn-art':['L132'], 'newtech-christmas-film':['L133'], 'newtech-christmas-art':['L134']})
GENERAL_STAYS.add('landheim-general-2027')
GENERAL_STAYS.add('frilingue-braunwald-language')
RELATED['englishsummer-tech']=['L006']
RELATED['ucr-pacific-archive']=['L120']
RELATED['ecolint-intro-robotics']=['L296']
RELATED['imdatbot-ashgabat-summer']=['L711']
RELATED['picrc-ocean-explorers']=['L717']
REUSE_DATES['ecolint-intro-robotics']=['L296']
RELATED.update({slug:['L012'] for slug in ['funtech-mod-day','funtech-redstone-day','funtech-tonbridge-board']})
# Undated programme cards cross-reference their source dossiers without creating sessions.
RELATED.update({
    'kidz-code-camp-fiji-nadi': ['L211'],
    'makerland-b-finder': ['L636'],
    'makerland-b-maker': ['L637'],
    'inspire-robotics-atoyac-6-8': ['L638'],
    'inspire-robotics-atoyac-9-11': ['L639'],
    'inspire-robotics-atoyac-12-17': ['L640'],
    'tech-science-kids-createlab': ['L641'],
    'tech-science-kids-robominds-bioglow': ['L642'],
    'techlabkids-online-scratch': ['L643'],
    'techlabkids-online-digital': ['L644'],
    'citc-san-jose-smartivo': ['L646'],
    'citc-san-jose-algoplay': ['L647'],
    'citc-san-jose-bricks-challenge': ['L648'],
    'citc-san-jose-galileo-technic': ['L649'],
    'citc-san-jose-robotoys': ['L650'],
    'citc-san-jose-algoc': ['L651'],
    'pulediamante-parquesol-navidad': ['L652'],
})
FIT = {'candidate':'Да по возрасту; зачисление отдельно',
       'conditional':'Условно; проверить возраст, класс и допуск',
       'later':'Нет сейчас; будущая возрастная ступень',
       'not_eligible':'Нет по условиям выбранного трека',
       'unknown':'Уточнить; возрастной допуск не установлен'}

def integrate(catalog, dossier_report):
    report=deepcopy(dossier_report)
    previous=catalog.get('camp_programmes',{})
    managed=set(previous.get('generated_event_ids',[]))
    previous_managed={e['id']:e for e in catalog['events'] if e['id'] in managed}
    events=[e for e in catalog['events'] if e['id'] not in managed]
    original={e['id']:e for e in events}
    countries={c['iso']:c for c in catalog['countries']}
    new_events=[]; links=[]
    sources={s['url'] for s in catalog['sources']}
    for p in report['profiles']:
        for s in p['sources']:
            if s['url'] not in sources:
                catalog['sources'].append(dict(url=s['url'],title=s['title'],
                    evidence='Официальный источник досье; неизвестные условия отмечены в программе',checked=s['checked']))
                sources.add(s['url'])
        p['related_event_ids']=[i for i in RELATED.get(p['slug'],[]) if i in original]
        p['calendar_links']=[]
        verified_session_source=p['timing'].get('verified_session_source')
        if verified_session_source:
            # Only an explicitly sourced session calendar can replace a broad
            # season window. Every calculated option needs its own date rule.
            variants=p['timing'].get('session_details',[])
            assert verified_session_source in {s['url'] for s in p['sources']}
            assert variants and [[v['start'],v['end']] for v in variants]==p['timing']['sessions']
            assert len({(v['start'],v['end']) for v in variants})==len(variants)
            assert all(v.get('source')==verified_session_source and
                       v.get('date_precision')=='published_rule' and v.get('date_rule')
                       for v in variants)
            p['timing']['precision']='published_sessions'
        else:
            p['timing']['precision']=p['timing']['precision'] if p['timing'].get('precision') in ['announced_month','published_sessions_and_announced_month'] else 'season_window' if p['slug'] in SEASON_WINDOWS or p['timing'].get('precision')=='season_window' else 'published_sessions'
        # Opt-in keys preserve different campuses sharing the same dates.
        # Legacy IDs and their first matching dated variant stay unchanged.
        if p['timing'].get('variant_keyed'):
            variants=p['timing']['session_details']
            assert [[v['start'],v['end']] for v in variants]==p['timing']['sessions']
            assert len({v['variant_key'] for v in variants})==len(variants)
            assert all(re.fullmatch(r'[a-z0-9-]+',v['variant_key']) for v in variants)
            dated=[(v['start'],v['end'],v) for v in variants]
        else:
            dated=[(start,end,next((v for v in p['timing'].get('session_details',[]) if v['start']==start and v['end']==end),{})) for start,end in p['timing']['sessions']]
        for start,end,variant in dated:
            if p['timing']['precision']=='season_window':
                p['calendar_links'].append(dict(start=start,end=end,kind='season_window',event_ids=[]))
                continue
            # A dated campus variant can narrow reuse to its explicitly linked IDs.
            # Same dates at different campuses must not merge into one another.
            reuse_ids=variant.get('legacy_event_ids',REUSE_DATES.get(p['slug'],[]))
            assert set(reuse_ids)<=set(REUSE_DATES.get(p['slug'],[]))
            existing=[e for i in reuse_ids if (e:=original.get(i)) and
                ((e['start']==start and e['end']==end) or
                 (e.get('date_scope')=='session_days' and e['start']<=start and e['end']>=end))]
            if existing:
                ids=[e['id'] for e in existing]
                p['calendar_links'].append(dict(start=start,end=end,kind='existing_programme',event_ids=ids))
                for e in existing: links.append(dict(programme_id=p['id'],event_id=e['id'],relation='existing_programme'))
                continue
            eid=p['id']+'-'+start.replace('-','')+'-'+end.replace('-','')
            if p['timing'].get('variant_keyed'):eid+='-'+variant['variant_key']
            if variant.get('catalogue_id'):
                # An explicitly researched reschedule keeps its existing identity.
                # The original date in an ID is not the current event date.
                eid=variant['catalogue_id']
                assert eid.startswith(p['id']+'-') and eid in previous_managed
            # Explicit published lesson calendars may retain their earlier days.
            # This opt-in does not turn undated old camp listings into events.
            if variant.get('include_published_past_schedule'):
                assert variant.get('date_scope')=='session_days' and variant.get('sessions') and variant.get('source')
            if end<report['asof'] and not variant.get('include_published_past_schedule'):
                # Advancing the research date must not erase researched history.
                # Do not invent new archival rows, but retain previously published ones.
                if eid in previous_managed:
                    new_events.append(deepcopy(previous_managed[eid]))
                    p['calendar_links'].append(dict(start=start,end=end,kind='catalogue_session',event_ids=[eid]))
                    links.append(dict(programme_id=p['id'],event_id=eid,relation='catalogue_session'))
                continue
            family_fit=variant.get('family_fit',p['family_fit'])
            # A stay offering several optional workshops is not a robotics-only course.
            themes=[t for t in p['themes'] if t not in ['robotics','coding','ai']] if p['slug'] in GENERAL_STAYS else list(p['themes'])
            if not themes:themes=['general']
            formats=variant.get('formats',p['formats'])
            mode='unconfirmed_program' if 'unknown' in formats else 'mixed_camp' if {'day','boarding'}<=set(formats) else 'residential' if ('boarding' in formats or p['slug']=='family-aviation') else 'day_camp'
            # New dossiers may explicitly classify accompanied residential stays.
            # Preserve the legacy classification of all prior catalogue objects.
            mode=p.get('catalog_participation',mode)
            title=p['provider']+(' · '+variant['label'] if variant else ' · общая смена / выбор трека' if p['slug'] in GENERAL_STAYS else '')+' · '+start+'–'+end
            row=dict(id=eid,block='Лагеря',title=title,country=p['country'],
                region=countries[p['iso']]['region'],city=variant.get('place',p['place']),start=start,end=end,
                period=p['timing']['label'],date_status=variant.get('date_status','Подтверждено'),deadline=variant.get('deadline',''),
                age=variant.get('age',p['age']),mat=FIT[family_fit['matvey']['status']],osc=FIT[family_fit['oscar']['status']],
                format=variant.get('accommodation',p['accommodation']),entry=variant.get('entry','Индивидуальная заявка оператору; точный трек, возраст, язык и наличие мест подтвердить.'),
                gear=variant.get('programme',p['programme']),language=p['language'],cost=(('2026/27' if start<'2027-01-01' else '2027')+' · '+variant['price']+' · доплаты и условия в досье') if variant else str(p['price']['year'] or 'Год уточнить')+' · '+p['price']['label'],
                level='D — обучение',reward='Учебная программа / проект; внутренний конкурс не международная победа',
                priority='P4 — будущий возраст' if all(family_fit[k]['status']=='later' for k in ['matvey','oscar']) else 'P2 — поездка после подтверждения допуска',
                action='; '.join(variant.get('questions',p['questions'])),source=variant.get('source',p['sources'][0]['url']),references=[dict(url=s['url'],label=s['title']) for s in p['sources']],
                proof=variant.get('proof','Официальные источники подробного досье прочитаны; неизвестные условия сохранены явно.'),
                checked=p['checked'],status='Идея',
                note='Матвей: '+family_fit['matvey']['detail']+' Оскар: '+family_fit['oscar']['detail']+' Доплаты: '+variant.get('extras',p['price']['extras'])+' Оплата: '+variant.get('deposit',p['price']['deposit']),
                iso=[p['iso']],themes=themes,scope='local',
                importance_reason='Редакционный кандидат под семейную поездку; международный состав не означает мировую лигу.',
                languages=list(p['confirmed_instruction_languages']),language_mode=p['language_evidence_role'] if p.get('language_evidence_role') in ['bilingual','language_lessons'] else 'camp_life' if p['slug']=='les-elfes' or p.get('language_evidence_role')=='camp_life' else 'primary' if p['confirmed_instruction_languages'] else 'unconfirmed',
                language_certainty=p['language'],participation=mode,admission_kind=variant.get('admission_kind','open_application'),evidence_level='program',
                date_scope=variant.get('date_scope','camp_session'),date_precision=variant.get('date_precision','published_session'),camp_dossier_slug=p['slug'],camp_programme_id=p['id'])
            if p.get('language_evidence_role') == 'support' and p.get('confirmed_support_languages'):
                row['language_mode'] = 'support'
                row['support_languages'] = list(p['confirmed_support_languages'])
            # An explicit empty list means attendance days are still unknown.
            if variant.get('date_scope')=='day_camp_window' and 'attendance_weekdays' not in variant:
                row['attendance_weekdays']=['MO','TU','WE','TH','FR']
            if variant.get('attendance_weekdays'):
                row['attendance_weekdays']=list(variant['attendance_weekdays'])
            if variant.get('date_scope')=='session_days':
                row['sessions']=deepcopy(variant['sessions'])
                assert row['sessions'] and all(start<=s['date']<=end for s in row['sessions'])
            if variant.get('availability'):row['availability']=deepcopy(variant['availability'])
            if variant.get('date_precision')=='published_rule':
                legacy_rule='2027-07-04–2027-08-15; пансион Вс–Вс, дневной Пн–Пт; выбор 1/2/3 недель. Даты вариантов рассчитаны по этому опубликованному правилу.'
                row['date_rule']=variant.get('date_rule') or (legacy_rule if p['slug']=='jfk-outdoor' else '')
                assert row['date_rule'], 'A calculated date needs its own published rule'
            new_events.append(row)
            p['calendar_links'].append(dict(start=start,end=end,kind='catalogue_session',event_ids=[eid]))
            links.append(dict(programme_id=p['id'],event_id=eid,relation='catalogue_session'))
        for i in p['related_event_ids']:
            if not any(x['programme_id']==p['id'] and x['event_id']==i for x in links):
                links.append(dict(programme_id=p['id'],event_id=i,relation='related_track_or_operator'))
        for previous_window in p['timing'].get('unconfirmed_previous',[]):
            # Keep the researched record, but remove an uncorroborated old future
            # date from operational calendars. Absence is not a cancellation.
            eid=previous_window['catalogue_id']
            assert eid.startswith(p['id']+'-') and eid in previous_managed
            row=deepcopy(previous_managed[eid])
            row.update(title=p['provider']+' · '+previous_window['label'],start='',end='',deadline='',
                reported_start=previous_window['start'],reported_end=previous_window['end'],
                date_status='Уточнить',date_scope='camp_window',date_precision='previous_listing_unconfirmed',
                period=previous_window['note'],proof=previous_window['note'],note=previous_window['note'],
                action='; '.join(p['questions']),source=p['sources'][0]['url'],checked=p['checked'],
                references=[dict(url=s['url'],label=s['title']) for s in p['sources']],cost=p['price']['label'],
                mat=FIT[p['family_fit']['matvey']['status']],osc=FIT[p['family_fit']['oscar']['status']])
            for key in ['sessions','deadline_utc','attendance_weekdays']:row.pop(key,None)
            new_events.append(row)
            p['calendar_links'].append(dict(kind='unconfirmed_previous_listing',start='',end='',reported_start=previous_window['start'],reported_end=previous_window['end'],event_ids=[eid]))
            links.append(dict(programme_id=p['id'],event_id=eid,relation='unconfirmed_previous_listing'))
    links=list({(x['programme_id'],x['event_id']):x for x in links}.values())
    assert len({e['id'] for e in new_events})==len(new_events)
    assert not set(original)&{e['id'] for e in new_events}
    catalog['events']=events+new_events
    catalog['asof']=max(catalog['asof'],report['asof'])
    report['event_links']=links
    report['generated_event_ids']=[e['id'] for e in new_events]
    report['integration']=dict(generated_sessions=len(new_events),
        reused_legacy_events=len({x['event_id'] for x in links if x['relation']=='existing_programme'}),
        seasonal_windows=sum(x['kind']=='season_window' for p in report['profiles'] for x in p['calendar_links']),
        scope='Точные смены добавлены в общий календарь. Существующие эквивалентные программы связаны без повторных карточек; широкие сезонные окна не создают смен. Связь related_track_or_operator не означает одинаковую программу или допуск.')
    catalog['camp_programmes']=report
    return report
