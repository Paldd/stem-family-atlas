"""Localize calendar text from translated records; preserve every scheduling property."""
from localization import unfold_ics


def escape(value):
    return str(value).replace('\\', '\\\\').replace('\r\n', '\n').replace('\r', '\n').replace('\n', '\\n').replace(';', '\\;').replace(',', '\\,')


def fold(line):
    lines = []; chunk = ''
    for char in line:
        if len((chunk + char).encode('utf-8')) > 73:
            lines.append(chunk); chunk = ' ' + char
        else: chunk += char
    lines.append(chunk)
    return '\r\n'.join(lines)


PREFIXES = {
    'registration_open': '[Apertura de inscripción] ',
    'submission_open': '[Apertura de envío de proyectos] ',
    'judging': '[Presentación virtual] ',
    'submission_window': '[Período de envío de resultados] ',
    'festival_window': '[Días del evento] ',
    'camp_window': '[Período del campamento · confirmar horario] ',
    'activity_start': '[Inicio · confirmar período completo] ',
    'workshop_window': '[Días de elección de taller] ',
    'camp_session': '[Turno de campamento] ',
}


def localize_calendar(source, original, translated):
    records = {}
    for ru, es in zip(original['events'], translated['events']):
        records['stem-' + ru['id'] + '@family-stem.local'] = (ru, es, None, False)
        records['stem-' + ru['id'] + '-deadline@family-stem.local'] = (ru, es, None, True)
        records['stem-exhibition-' + ru['id'] + '@family-stem.local'] = (ru, es, None, False)
        for s, t in zip(ru.get('sessions', []), es.get('sessions', [])):
            records['stem-' + ru['id'] + '-' + s['date'] + '@family-stem.local'] = (ru, es, t, False)
    lines = unfold_ics(source); result = []; index = 0
    exhibition_calendar = 'Exhibitions calendar' in source
    while index < len(lines):
        line = lines[index]
        if line == 'BEGIN:VEVENT':
            end = lines.index('END:VEVENT', index)
            block = lines[index:end + 1]
            uid = next(v.partition(':')[2] for v in block if v.startswith('UID:'))
            ru, e, session, deadline = records[uid]
            if uid.startswith('stem-exhibition-'):
                gate = {'family': 'visita en familia', 'adults_only': 'niños de 6/9 años no admitidos', 'confirm_children': 'confirmar admisión de menores'}[e['visitor_policy']]
                title = '[Exposición · ' + gate + '] ' + e['title']
                description = f"Idea de visita; no es una inscripción aceptada. {e['visitor_policy_note']} Entrada de adultos: {e['adult_entry']}. {e['note']} Empresas: {e['exhibitor_note']}. Fuente verificada el {e['checked']}."
            else:
                session_note = ''
                if session:
                    session_note = f"Clase: {session['topic']}; {session['start_time']}–{session['end_time']} {session['timezone']}. {session.get('time_note', '')}"
                    prefix = '[Día de clase] '
                elif deadline:
                    label = e.get('deadline_label') or 'Plazo límite'
                    timed = any(v.startswith('DTSTART:') for v in block)
                    prefix = '[' + label + ('' if timed else ', confirmar hora') + '] '
                elif e.get('date_scope') == 'day_camp_window':
                    prefix = '[Período de campamento diurno · lun–vie] ' if e.get('attendance_weekdays') else '[Período de campamento diurno · confirmar horario] '
                else:
                    prefix = PREFIXES.get(e.get('date_scope'), '[Idea] ')
                title = prefix + e['title']
                description = f"Idea para planificar; no es una inscripción aceptada. ID {e['id']}. {session_note}. Matvey: {e['mat']}; Oscar: {e['osc']}. Cómo participar: {e['entry']}. Próximo paso: {e['action']}. {e['note']}. {e.get('deadline_note', '')}. {e.get('registration_status', '')}. Fuente verificada el {e['checked']}."
            replacements = {'SUMMARY': title, 'DESCRIPTION': description, 'LOCATION': e['city'] + ', ' + e['country']}
            for property in block:
                key, sep, value = property.partition(':')
                result.append(fold(key + sep + escape(replacements[key])) if key in replacements else property)
            index = end + 1
        else:
            if line.startswith('X-WR-CALNAME:'):
                line = 'X-WR-CALNAME:STEM Atlas — ' + ('exposiciones; admisión de menores por separado' if exhibition_calendar else 'fechas y plazos para planificar')
            if line.startswith('PRODID:'): line = line.removesuffix('//RU') + '//ES'
            result.append(fold(line)); index += 1
    return ('\r\n'.join(result) + '\r\n').encode('utf-8')
