"""Official national entry contacts, kept separate from competition fixtures."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
CHECKED='2026-11-05';SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
WRO='https://wro-association.org/about-wro/association/member-countries/'
JOIN='https://wro-association.org/join-support/join-the-competition/'
FLL='https://firstlegoleague.org/#find'
FIRST='https://www.firstinspires.org/find-local-support'
RECF='https://kb.roboticseducation.org/hc/en-us/articles/41060488433047-RECF-Support-Contacts'
CRITERIA='https://kb.roboticseducation.org/hc/en-us/articles/5474199602071-Qualifying-Criteria-for-RECF-Robotics-Competition-Programs'
def enrich_v171(d):
    routes=json.loads((ROOT/'data/national-routes-native-v171.json').read_text())['routes']
    captions={
      'all_divisions_unconfirmed':T('Категории у этого партнёра уточняются','Confirmar categorías con este socio'),
      'discover':'Discover','explore':'Explore','challenge':'Challenge'}
    for r in routes:r['programme']=captions[r['division']]
    gate=T('Справочник подтверждает контакт сети, а не даты, свободные места или допуск семьи. Проверить конкретный сезон, возраст / класс, язык занятий и судейства, состав команды, тренера, стоимость, место команды и правила местного отбора. Паспорт не заменяет условия допуска.',
     'Directorio acredita contacto de la red, sin confirmar fechas, plazas ni admisión familiar. Verificar temporada concreta, edad / curso, idioma de clases y evaluación, equipo, entrenador, coste, sede del equipo y selección local. Pasaporte no sustituye requisitos de admisión.')
    pathways=[dict(id='wro-national',network='WRO',title=T('WRO: через национального организатора','WRO: mediante organizador nacional'),summary=T('Региональные и национальные этапы определяет местный оператор; победители могут получить международную квалификацию. Не все категории и возрасты доступны в каждой стране.',
      'Operador local define fases regionales y nacionales; ganadores pueden lograr clasificación internacional. No todas categorías y edades disponibles en cada país.'),steps=[T('Найти организатора страны, где будет базироваться команда','Encontrar organizador del país donde estará el equipo'),T('Сверить местную категорию и регламент сезона','Revisar categoría local y reglamento de temporada'),T('Собрать команду и пройти доступный местный этап','Formar equipo y participar en fase local disponible'),T('Проверить квоту и условия международного отбора','Verificar cupo y requisitos de clasificación internacional')],source=JOIN),
     dict(id='first-local',network='FIRST LEGO League',title=T('FIRST: партнёр программы и местная команда','FIRST: socio del programa y equipo local'),summary=T('FIRST не распределяет детей по готовым командам. Команды создают школы, библиотеки, клубы и семьи. Во Франции Discover / Explore ведёт Educabot, Challenge — West Side Robot Lab; в Бразилии Discover / Explore — Positivo, Challenge — SESI. Общий контакт страны не доказывает проведение всех категорий.',
      'FIRST no asigna niños a equipos existentes. Colegios, bibliotecas, clubes y familias forman equipos. En Francia Discover / Explore corresponden a Educabot, Challenge a West Side Robot Lab; en Brasil Discover / Explore a Positivo, Challenge a SESI. Contacto general del país no acredita todas las categorías.'),steps=[T('Выбрать возрастную программу по актуальному профилю лиги','Elegir programa por edad según perfil actual de la liga'),T('Проверить партнёра именно выбранной категории','Verificar socio de la categoría concreta'),T('Найти или создать местную команду с тренером','Encontrar o crear equipo local con entrenador'),T('Уточнить фестиваль, турнир и квалификацию этой программы','Aclarar festival, torneo y clasificación de este programa')],source=FIRST),
     dict(id='vex-event-route',network='VEX',title=T('VEX: платформа, команда и турнир','VEX: plataforma, equipo y torneo'),summary=T('Руководство VEX для тренеров описывает VEX IQ и VEX V5, выбор платформы, работу команды и подготовку к сезону. Проверять название конкретного турнира и его действующий регламент; одинаковый робот не подтверждает общий чемпионат или квоту с другой программой.',
      'Guía VEX para entrenadores describe VEX IQ y VEX V5, elección de plataforma, equipo y preparación de temporada. Verificar nombre del torneo concreto y reglamento vigente; mismo robot no acredita campeonato ni cupo compartidos con otro programa.'),steps=[T('Выбрать платформу VEX и действующую игру сезона','Elegir plataforma VEX y juego vigente de temporada'),T('Подготовить команду, тренера и оборудование','Preparar equipo, entrenador y material'),T('Найти конкретное событие в RobotEvents','Encontrar evento concreto en RobotEvents'),T('Сверить правила турнира и путь к следующему уровню','Revisar reglas del torneo y acceso al siguiente nivel')],source='https://kb.vex.com/hc/en-us/articles/48968257880596-VEX-Coaches-Start-Here'),
     dict(id='recf-event-route',network='RECF',title=T('RECF: команда, событие и регион квалификации','RECF: equipo, evento y región de clasificación'),summary=T('Сначала выбрать систему и регламент сезона. Найденное на RobotEvents событие нужно проверить по категории, региону и способу допуска. Scrimmage, workshop и участие в турнире сами по себе не означают квалификацию на чемпионат. Региональный support — помощь по программе, а не доказательство местного открытого турнира.',
      'Primero elegir sistema y reglamento de temporada. Evento de RobotEvents debe verificarse por categoría, región y admisión. Scrimmage, workshop y participación en torneo por sí solos no equivalen a clasificación al campeonato. Support regional ayuda con el programa, sin acreditar torneo local abierto.'),steps=[T('Выбрать действующую программу и зарегистрированную команду','Elegir programa vigente y equipo registrado'),T('Найти конкретное событие в RobotEvents','Encontrar evento concreto en RobotEvents'),T('Прочитать условия события и региона команды','Leer condiciones del evento y región del equipo'),T('Проверить qualifying criteria и выделенные места','Verificar qualifying criteria y plazas asignadas')],source=CRITERIA)]
    for p in pathways:p['gate']=gate
    summary=dict(routes=len(routes),countries=len({r['iso']for r in routes}),wro_contacts=sum(r['network']=='WRO'for r in routes),fll_contacts=sum(r['network']=='FIRST LEGO League'for r in routes),fll_country_cards=97,contacts_without_operator_website=sum(not r['url']for r in routes),new_competition_fixtures=0)
    d['national_routes']=dict(version=171,checked=CHECKED,summary=summary,routes=routes,pathways=pathways,gate=gate,
      absence_note=T('Отсутствие контакта в этих двух справочниках не доказывает отсутствие робототехники, клубов или других лиг в стране.',
       'Ausencia de contacto en estos dos directorios no demuestra ausencia de robótica, clubes u otras ligas en el país.'),
      suspension_note=T('Публикация WRO 2022 о приостановке работы с национальными организаторами России и Беларуси относится к организаторам. Она не является подтверждением общего запрета детям с российским или белорусским паспортом участвовать в другой стране; допуск конкретной команды требует отдельного регламента.',
       'Comunicado WRO 2022 sobre suspensión de relaciones con organizadores nacionales de Rusia y Bielorrusia se refiere a organizadores. No acredita prohibición general a niños con pasaporte ruso o bielorruso en otro país; admisión del equipo concreto requiere reglamento propio.'),
      support_links=[dict(title='RobotEvents',url='https://www.robotevents.com/'),dict(title=T('Поддержка RECF по регионам и программам','Soporte RECF por regiones y programas'),url=RECF),dict(title=T('Профили лиг и возрастные требования','Perfiles de ligas y requisitos de edad'),url='#leagues')],
      sources=[dict(title=T('Действующий справочник WRO','Directorio vigente WRO'),url=WRO),dict(title=T('Глобальные партнёры FIRST LEGO League','Socios mundiales FIRST LEGO League'),url=FLL),dict(title=T('Правила национального входа WRO','Reglas de acceso nacional WRO'),url=JOIN),dict(title=T('Поиск поддержки FIRST','Buscador de soporte FIRST'),url=FIRST),dict(title=T('Критерии квалификации RECF','Criterios de clasificación RECF'),url=CRITERIA)])
    d['national_routes']['sources'] += [
      dict(title=T('Руководство VEX для тренеров','Guía VEX para entrenadores'),url='https://kb.vex.com/hc/en-us/articles/48968257880596-VEX-Coaches-Start-Here'),
      dict(title=T('Поддержка RECF по регионам и программам','Soporte RECF por regiones y programas'),url=RECF),
      dict(title=T('Сообщение WRO 2022 о национальных организаторах','Comunicado WRO 2022 sobre organizadores nacionales'),url='https://wro-association.org/important-message-from-wro-association-ltd-on-the-situation-in-ukraine/')]
    for c in d['countries']:
        rr=[r for r in routes if r['iso']==c['iso']];wr=next((r for r in rr if r['network']=='WRO'),None)
        c['network_route_ids']=[r['id']for r in rr];c['wro_checked']=CHECKED
        c['wro_directory_status']='listed'if wr else'not_listed'
        if wr:c.update(wro=wr['provider'],url=wr['url'])
        else:c.update(wro=T('Не найден в проверенном справочнике WRO; другие лиги исследуются отдельно','No localizado en directorio WRO verificado; otras ligas se investigan aparte'),url='')
        c['source']=WRO+' ; https://unstats.un.org/unsd/methodology/m49/'
        has_events=any(c['iso']in e['iso']for e in d['events'])
        c['coverage']=T('Частично: есть записи; полный местный аудит не завершён','Parcial: hay fichas; auditoría local completa pendiente')if has_events else T('Местный календарь ещё не исследован','Calendario local pendiente de investigación')
    d['wro_members']=summary['wro_contacts']
    known={s['url']for s in d['sources']}
    for s in d['national_routes']['sources']:
        if s['url']not in known:d['sources'].append(dict(**s,checked=CHECKED,evidence=gate));known.add(s['url'])
