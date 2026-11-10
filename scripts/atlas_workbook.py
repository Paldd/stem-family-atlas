"""Write and verify complete Atlas workbooks with the standard library."""
import json
import zipfile
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

WORKBOOKS = {'ru': 'STEM_atlas_ru.xlsx', 'es': 'STEM_atlas_es.xlsx'}
SPREADSHEET_NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
NS = {'x': SPREADSHEET_NS}

HEADERS={
 'deadline_history':'Historial de plazos',
 'date_history':'Historial de fechas',
 'venue_status':'Estado del recinto',
 'previous_programme':'Descripción anterior del programa','previous_source_checks':'Historial de verificación de fuentes','source_refresh':'Actualización de fuentes',
 'local_calendar_key':'Clave del calendario local','local_programme':'Programa local','season':'Temporada',
 'route_iso':'ISO del país de la ruta',
 'id':'ID','block':'Tipo','title':'Título','country':'País','region':'Región','city':'Ciudad',
 'start':'Inicio','end':'Fin','period':'Período','date_status':'Estado de fechas','deadline':'Plazo límite',
 'deadline_label':'Tipo de plazo','deadline_note':'Nota sobre el plazo','deadline_utc':'Plazo UTC',
 'registration_status':'Estado de inscripción','age':'Edad / curso','mat':'Matvey','osc':'Oscar',
 'format':'Formato / equipo','participation':'Participación','delivery_mode':'Modalidad de participación','entry':'Cómo participar','gear':'Equipamiento',
 'language':'Idioma','cost':'Precio','scope':'Ámbito','level':'Nivel','importance_reason':'Motivo de prioridad',
 'reward':'Resultado / premio','priority':'Prioridad','action':'Próximo paso','source':'Fuente oficial',
 'references':'Fuentes relacionadas','proof':'Base de verificación','checked':'Fecha de verificación',
 'status':'Estado','note':'Notas','themes':'Temáticas','languages':'Idiomas confirmados',
 'language_certainty':'Certeza del idioma','iso':'ISO del país','provider':'Proveedor','name':'Nombre',
 'programme':'Programa','programme_options':'Módulos y edades publicadas','place':'Lugar','accommodation':'Alojamiento','price':'Precio y condiciones',
 'family_fit':'Requisitos para la familia','timing':'Calendario','sources':'Fuentes oficiales',
 'pairing':'Grupos simultáneos: sede y tarifa verificadas',
 'archive_offers':'Ofertas archivadas','previous_price_terms':'Condiciones de precios anteriores',
 'questions':'Preguntas pendientes','school_type':'Tipo de colegio','results':'Resultados',
 'requirements':'Requisitos','awards':'Premios','age_rule':'Regla de edad','age_range':'Edades',
 'format_rule':'Regla del formato','entry_route':'Vía de participación','availability':'Disponibilidad'
}
HEADERS.update({
 'evidence_level':'Nivel de evidencia','related_ids':'Registros relacionados','admission_kind':'Vía de admisión',
 'venue':'Sede','event_code':'Código del evento','event_region':'Región del evento','event_type':'Tipo de evento',
 'team_min':'Mínimo de integrantes','team_max':'Máximo de integrantes','birth_start':'Nacimiento desde',
 'birth_end':'Nacimiento hasta','date_scope':'Significado del período','event_group':'Grupo del evento',
 'language_mode':'Función del idioma','language_roles':'Idiomas según su función','historical_editions':'Ediciones anteriores','exhibition_tier':'Nivel de exposición',
 'visitor_policy':'Política de visitantes','visitor_policy_note':'Condiciones de visita','visitor_age_min':'Edad mínima de visitantes','adult_entry':'Entrada de adultos',
 'child_entry':'Acceso de niños y condiciones','child_entry_status':'Evidencia de acceso infantil','family_visit':'Visita familiar y días','exhibition_focus':'Temática de la exposición',
 'exhibitor_note':'Información de expositores','highlights':'Aspectos destacados','exhibitor_directory_url':'Directorio de expositores',
 'exhibitors':'Expositores','support_languages':'Idiomas de apoyo','age_conflict':'Conflicto de edades publicadas',
 'registration_url':'Enlace de inscripción','sessions':'Sesiones','published_start':'Inicio publicado',
 'published_end':'Fin publicado','planned_windows':'Períodos previstos','parent_event_id':'Evento principal',
 'age_reference_date':'Fecha de referencia para la edad','public_days':'Días de acceso público',
 'teaching_weeks':'Semanas de enseñanza','related_school_ids':'Colegios relacionados','materials_only':'Solo materiales',
 'date_precision':'Precisión de fechas','announced_months':'Meses anunciados sin día exacto','attendance_weekdays':'Días de asistencia','visitor_note':'Notas para visitantes',
 'company_scope':'Alcance de empresas participantes','start_time':'Hora de inicio','end_time':'Hora de fin',
 'timezone':'Zona horaria','language_lesson_languages':'Idiomas de las clases de idiomas','holiday_window':'Período vacacional',
 'language_support_scope':'Alcance del apoyo lingüístico','technical_sessions':'Sesiones técnicas',
 'registration_opens':'Apertura de inscripción','deadline_basis':'Base del plazo','camp_dossier_slug':'Identificador del dossier',
 'camp_programme_id':'ID del programa de campamento','date_rule':'Regla de fechas','event_kind':'Clase de evento',
 'grade_level':'Nivel escolar','exhibitor_deadline':'Plazo de expositores','exhibitor_age':'Edad para exponer',
 'visitor_age_status':'Estado de admisión por edad','rules_year':'Año del reglamento','next_season_status':'Estado de la próxima temporada',
 'international_circuit':'Circuito internacional','team_count_note':'Notas sobre tamaño del equipo','workshop_code':'Código del taller',
 'curriculum':'Plan de estudios','ib_programmes':'Programas IB','ages':'Edades','instruction_languages':'Idiomas de enseñanza',
 'language_note':'Notas sobre idiomas','fit':'Adecuación a la familia','boarding':'Internado','boarding_note':'Condiciones de internado',
 'labs':'Laboratorios','ai':'Inteligencia artificial','evidence':'Evidencia','admissions':'Admisiones',
 'research_status':'Estado de investigación','verification':'Verificación','en':'Nombre en inglés','wro':'Organizador WRO',
 'url':'Enlace','coverage':'Cobertura investigada','group':'Grupo','age_summary':'Resumen de edades',
 'age_tags':'Etiquetas de edad','summary':'Resumen','categories':'Categorías','event_ids':'IDs de eventos',
 'legacy_ids':'IDs anteriores','route':'Itinerario','hardware':'Equipamiento','importance':'Importancia',
 'strengths':'Puntos fuertes','nuances':'Condiciones y matices','award':'Premio','slug':'Identificador estable',
 'formats':'Formatos','confirmed_instruction_languages':'Idiomas de enseñanza confirmados','materials_languages':'Idiomas de los materiales','editorial_reason':'Motivo de selección',
 'shortlist':'Selección familiar','related_event_ids':'Eventos relacionados','calendar_links':'Enlaces al calendario',
 'language_evidence_role':'Función lingüística verificada','previous_seasons':'Temporadas anteriores','operator_key':'Clave del operador',
 'booking_channel':'Canal de reserva','operator_identity_status':'Estado de identidad del operador',
 'possible_same_operator_as':'Posible operador compartido','intake_evidence':'Evidencia de convocatoria',
 'eligibility_birth_years':'Años de nacimiento admitidos','parent_programme_slug':'Programa principal',
 'partner_locations_unconfirmed':'Sedes de socios sin confirmar','confirmed_support_languages':'Idiomas de apoyo confirmados',
 'programme_category':'Categoría de programa','available_staff_languages':'Idiomas del personal',
 'catalog_participation':'Participación en el catálogo','programme_type':'Tipo de programa','programme_kind':'Modalidad del programa','date_conflict':'Conflicto en la fecha fuente','source_date_text':'Fecha textual de la fuente','roster_update_deadline':'Plazo para cambios de integrantes',
 'canonical_event_id':'ID de la ficha principal','parent_programme_id':'ID del programa principal',
 'related_programme_ids':'IDs de programas relacionados',
 'requires_parent_programme_ids':'IDs de programas base obligatorios',
 'deadline_timezone':'Zona horaria del plazo',
 'grade_min':'Curso escolar mínimo','grade_max':'Curso escolar máximo',
 'grade_asof':'Período de referencia del curso escolar',
 'reported_start':'Inicio publicado pendiente de aclaración',
 'reported_end':'Fin publicado pendiente de aclaración',
 'reported_deadline':'Plazo publicado pendiente de aclaración',
 'entry_extra':'Condiciones adicionales de participación','fixture_id':'ID del torneo',
 'league_id':'ID de la liga','superseded_by':'Sustituido por'
})
def column(index):
    name=''
    while index:index,remainder=divmod(index-1,26);name=chr(65+remainder)+name
    return name

HEADERS.update({'access_url':'Web accesible verificada','website_checked':'Fecha de revisión web','website_note':'Notas de acceso web','website_status':'Estado de acceso web','network_route_ids':'IDs de vías nacionales','wro_checked':'Fecha del directorio WRO','wro_directory_status':'Estado en directorio WRO','network':'Red de robótica','league_id':'ID de la liga','division':'Categoría','source':'Fuente oficial'})

RUSSIAN_HEADERS = {
    'id': 'ID', 'block': 'Раздел', 'title': 'Название', 'country': 'Страна', 'region': 'Регион', 'city': 'Город',
    'start': 'Начало', 'end': 'Окончание', 'period': 'Период', 'date_status': 'Статус дат',
    'deadline': 'Срок', 'deadline_label': 'Тип срока', 'deadline_note': 'Условия срока',
    'deadline_utc': 'Срок UTC', 'registration_status': 'Статус регистрации',
    'age': 'Возраст / класс', 'mat': 'Матвей', 'osc': 'Оскар', 'format': 'Формат / команда',
    'participation': 'Участие', 'delivery_mode': 'Режим участия', 'entry': 'Как участвовать',
    'gear': 'Оборудование', 'language': 'Язык', 'cost': 'Стоимость', 'scope': 'Масштаб',
    'level': 'Уровень', 'importance_reason': 'Причина приоритета', 'reward': 'Результат / приз',
    'priority': 'Приоритет', 'action': 'Следующий шаг', 'source': 'Официальный источник',
    'references': 'Связанные источники', 'proof': 'Основание проверки', 'checked': 'Дата проверки',
    'status': 'Статус', 'note': 'Примечания', 'themes': 'Тематики', 'languages': 'Языки',
    'language_certainty': 'Подтверждение языка', 'iso': 'Код страны ISO', 'provider': 'Организатор',
    'name': 'Название', 'programme': 'Программа', 'programme_options': 'Модули и опубликованные возрастные условия', 'place': 'Место', 'accommodation': 'Проживание',
    'price': 'Цена и условия', 'family_fit': 'Условия для семьи', 'timing': 'Расписание',
    'sources': 'Официальные источники', 'pairing': 'Совпадение групп по времени и месту',
    'questions': 'Открытые вопросы', 'school_type': 'Тип школы', 'results': 'Результаты',
    'requirements': 'Требования', 'age_rule': 'Правило расчёта возраста', 'age_range': 'Возрастной диапазон',
    'format_rule': 'Условия формата', 'entry_route': 'Путь участия', 'availability': 'Доступность',
    'evidence_level': 'Уровень подтверждения', 'venue': 'Площадка', 'team_min': 'Минимум участников',
    'team_max': 'Максимум участников', 'date_scope': 'Назначение периода', 'language_mode': 'Роль языка',
    'visitor_policy': 'Правила посещения', 'adult_entry': 'Вход для взрослых', 'child_entry': 'Вход для детей',
    'family_visit': 'Семейное посещение', 'registration_url': 'Ссылка на регистрацию',
    'sessions': 'Смены / занятия', 'public_days': 'Дни доступа публики', 'timezone': 'Часовой пояс',
    'start_time': 'Время начала', 'end_time': 'Время окончания', 'curriculum': 'Учебная программа',
    'ib_programmes': 'Программы IB', 'ages': 'Возраст', 'instruction_languages': 'Языки обучения',
    'boarding': 'Пансион', 'labs': 'Лаборатории', 'ai': 'Искусственный интеллект',
    'admissions': 'Поступление', 'research_status': 'Статус исследования', 'url': 'Ссылка',
    'coverage': 'Покрытие', 'group': 'Группа', 'age_summary': 'Возрастные категории',
    'summary': 'Описание', 'categories': 'Категории', 'event_ids': 'ID мероприятий',
    'route': 'Маршрут', 'hardware': 'Техника', 'importance': 'Значимость', 'strengths': 'Сильные стороны',
    'nuances': 'Особенности и условия', 'award': 'Награда', 'slug': 'Стабильный идентификатор',
    'formats': 'Форматы', 'confirmed_instruction_languages': 'Подтверждённые языки занятий',
    'materials_languages': 'Языки материалов', 'shortlist': 'Семейная подборка',
    'network': 'Сеть', 'division': 'Дивизион', 'season': 'Сезон',
}


def workbook_sheets(data, language):
    if language == 'ru':
        blocks = ('Соревнования', 'События', 'Лагеря')
        names = ('Соревнования', 'Выставки и события', 'Лагеря и курсы', 'Досье лагерей',
                 'Лиги', 'Школы', 'Страны', 'Национальные маршруты')
    else:
        blocks = ('Competiciones', 'Eventos', 'Campamentos')
        names = ('Competiciones', 'Eventos y exposiciones', 'Campamentos y cursos',
                 'Fichas de campamentos', 'Ligas', 'Colegios', 'Países', 'Vías nacionales')
    events = [[row for row in data['events'] if row['block'] == block] for block in blocks]
    assert sum(map(len, events)) == len(data['events']), 'Workbook is missing an event block'
    return list(zip(names, (*events, data['camp_programmes']['profiles'],
                            data['league_guide']['profiles'], data['schools'], data['countries'],
                            data['national_routes']['routes'])))


def write_workbook(path,data,language):
    groups = workbook_sheets(data, language)
    headers = RUSSIAN_HEADERS if language == 'ru' else HEADERS
    part_label = 'часть' if language == 'ru' else 'parte'
    ns = SPREADSHEET_NS
    contents={}
    for sheet,(name,rows) in enumerate(groups,1):
        keys=list(dict.fromkeys(k for row in rows for k in row))
        if 'id' in keys:keys.remove('id');keys.insert(0,'id')
        expanded=[]
        if language == 'es':
            assert not set(keys)-headers.keys(), 'Add Spanish workbook headers: '+repr(sorted(set(keys)-headers.keys()))
        def value(row,key):
            x=row.get(key,'');return json.dumps(x,ensure_ascii=False) if isinstance(x,(dict,list)) else str(x)
        for key in keys:
            parts=max([1]+[(len(value(row,key))+32699)//32700 for row in rows]);expanded.extend((key,i) for i in range(parts))
        xml=[f'<worksheet xmlns="{ns}"><sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews><sheetData>']
        for index,row in enumerate([None,*rows],1):
            xml.append(f'<row r="{index}">')
            for c,(key,part) in enumerate(expanded,1):
                text=(headers.get(key,key)+(f' ({part_label} {part+1})' if part else '')) if row is None else value(row,key)[part*32700:(part+1)*32700]
                text=''.join(ch for ch in text if ch in '\n\t\r' or ord(ch)>=32)
                xml.append(f'<c r="{column(c)}{index}" t="inlineStr"><is><t xml:space="preserve">{escape(text)}</t></is></c>')
            xml.append('</row>')
        xml.append(f'</sheetData><autoFilter ref="A1:{column(len(expanded))}{len(rows)+1}"/></worksheet>')
        contents[f'xl/worksheets/sheet{sheet}.xml']=''.join(xml)
    contents['xl/workbook.xml']=f'<workbook xmlns="{ns}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'+''.join(f'<sheet name="{escape(name)}" sheetId="{i}" r:id="rId{i}"/>' for i,(name,rows) in enumerate(groups,1))+'</sheets></workbook>'
    rels='http://schemas.openxmlformats.org/package/2006/relationships'
    contents['xl/_rels/workbook.xml.rels']=f'<Relationships xmlns="{rels}">'+''.join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1,len(groups)+1))+'</Relationships>'
    contents['_rels/.rels']=f'<Relationships xmlns="{rels}"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>'
    contents['[Content_Types].xml']='<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'+''.join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1,len(groups)+1))+'</Types>'
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,body in sorted(contents.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+body)
    return {name:len(rows) for name,rows in groups}


def verify_workbook(path, data, language):
    groups = workbook_sheets(data, language)
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None, path
        sheets = ET.fromstring(archive.read('xl/workbook.xml')).findall('x:sheets/x:sheet', NS)
        assert [sheet.attrib['name'] for sheet in sheets] == [name for name, _ in groups], path
        for index, (name, rows) in enumerate(groups, 1):
            identity = 'id' if any('id' in row for row in rows) else next(iter(rows[0]), None) if rows else None
            expected = [str(row.get(identity, '')) for row in rows]
            with archive.open(f'xl/worksheets/sheet{index}.xml') as sheet:
                actual = []
                for _, element in ET.iterparse(sheet, events=('end',)):
                    if element.tag == f'{{{SPREADSHEET_NS}}}row':
                        if element.attrib['r'] != '1':
                            actual.append(element.findtext('x:c/x:is/x:t', namespaces=NS))
                        element.clear()
            assert actual == expected, (path, name, len(actual), len(expected))
