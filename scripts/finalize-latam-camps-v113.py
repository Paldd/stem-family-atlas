"""Bounded primary research receipt; the worldwide family objective remains active."""
import collections,hashlib,json,subprocess
from camp_latam_v113 import ROOT,BASE,CHECKED,NEW,UPDATED
P=ROOT.parent/'stem-family-atlas-work/camp-latam-primary-v113'
d=json.loads((ROOT/'data/catalog.json').read_text())
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
cp=d['camp_programmes'];old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']}
changed=[k for k in old if old[k]!=now[k]];newids=sorted(now.keys()-old.keys())
assert len(newids)==12 and not changed and len(cp['profiles'])==846
assert d['camp_planning']['offers']==b['camp_planning']['offers']
sources=[]
for f in sorted(P.glob('receipt-*.json')):
 for item in json.loads(f.read_text()):
  q=dict(item,checked=CHECKED,retrieval_method='direct_http',content_scope='Selected public programme/policy clauses or comparison with an existing dossier; not a complete site/country audit.')
  if q.get('status')==200:
   ext='pdf' if (P/(q['key']+'.pdf')).exists() else 'html';raw=(P/(q['key']+'.'+ext)).read_bytes()
   assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
   q.update(raw_filename=q['key']+'.'+ext,body_snapshot_retained=True,content_status='selected_visual_pdf_pages_full_text_extracted' if ext=='pdf' else 'registration_shell_not_price_or_admission' if q['key']=='kaju-registration' else 'selected_html_clauses')
  else:q.update(body_snapshot_retained=False,content_status='retrieval_error_no_body')
  sources.append(q)
assert len(sources)==19 and sum(q.get('status')==200 for q in sources)==18
visual=json.loads((P/'visual-review.json').read_text());assert visual['new_visual_pdf_checks']==39
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
sm=json.loads((ROOT/'dist/downloads/STEM_database_download.json').read_text());jm=json.loads((ROOT/'dist/downloads/STEM_database_json_download.json').read_text())
family=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT');expo=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
assert family==2651 and expo==104
blocks=collections.Counter(q['block'] for q in now.values());country_counts=dict(collections.Counter(q['iso'] for q in cp['profiles']))
urls=len({s['url'] for p in cp['profiles'] for s in p['sources']});assert urls==1309
checks=[
 'Seven new dossiers: five genuinely different Kajuyali venues/curricula under one operator (four Colombia/one Panama), plus two Talenttec SanRamon technical workshops under one operator. One existing Programable dossier materially deepened. Not seven independent providers or an objective global ranking.',
 'All3421 old event IDs and complete event objects retained unchanged. All839 old programme IDs retained,838 complete old programme objects unchanged; only Programable updated.3433 total events,846 dossiers/39countries/1309dossierURLs/200editorialscenarios/213coveragegaps.',
 'Kajuyali Summer2027 exact12 shifts: KuitaJun30–Jul12/Jul14–26/Jul28–Aug9;KiribatiJun26–Jul8/Jul10–22;AlunaJun27–Jul9/Jul11–23;YubarkaJun29–Jul11/Jul13–25/Jul27–Aug8;YakaroJun28–Jul10/Jul12–24. Each13calendar days,paidnightsunknown. N/A not extra shift. Exactvenues Colombia/Panama,not operatorheadquarters.',
 'Kuita7–17:Oscar conditional7byfirstday. Kiribati9–17:Matvey conditional/Oscar later. Aluna/Yubarka11–17:bothlater. Yakaro ownwebsite11–17 versus allfive2027PDFagecharts9–17:Matvey unknown/Oscar later;conflictkept,notassumedadmission.',
 'Kajuyali own2027 tables: Kuita10552300programme+1200000tiquete=11752300;Kiribati/Aluna12296000+1200000=13496000;Yubarka12084000+1400000=13484000;Yakaro12720000+3600000=16320000. Symbol$only,ISOcurrencycode absent:confirmCOP,do not convertUSD or create verifiedfullfamilybudget. Kuita2identicaltotal23504600 is conditionalarithmetic,notconfirmedtwochildinvoice.',
 'Kuita groupprivatebusfromBogota06departure/12return;otherfour groupflights plusboat/bus. Tiq uete inKuita notairfare. FamilytoBogota/localentry/internationalinsurance/taxes/withdrawal/refund/personaldiscountamount/deadline unspecified. English/Spanishwebsite not teacherlanguage,foreignindividualintake/placesunknown.',
 'Ownboarding5–7children+counselor,optionalCIT,cabinsseparatedbysex/coldshowers,physician24h/kitchen/laundry ownclaimsnotindependentaudit. Day07:20wake/21:30bed androtatingfouractivities. Childphoneshelduntilend,threeletterexchangesdays3/7/11,dailygeneralphotos/email;parentcustomerservicenotdailychildphoneguarantee.',
 'Kuita culture/horsecare/cooking/bike/wakeboard;optionalKamunitzali14+notyoungerchildren. Kiribati coralrestoration/marineecologygeneralcampnotSTEMlab. Aluna communityculture/cooking/weaving/surf. Yubarka whales/birds/snorkel/apnea;webBuceoPanama copy notColombiaintensive. Yakaro wood/cooking/wateractivities;divecertification/certifieddives explicitlyextra/nofeeorunderageadmissionproof.',
 'TalenttecSanRamon explicitJuly7–10,2026pastarchive,noinvented2027rows. Robotgroups4–5/6–8/9–12,CRC14000/16000/16000 and1h/1.5h/1.5hdaily;3D9–12CRC16000/1hdaily,max12. Kit/softwareownership/insurance/refund/teacherlanguageunknown;older3DnotOscareligible.',
 'Programable existingCP046/legacyL147,L148 preserved withoutcalendar duplicates. SixJan/Feb2027weeks/15h/max12/two80minblocks:MakeyMakey/microbit/mBot/EV3andgames;SeniorArduino/multimeter/protoboard/MLX90614I2C/encoders/color-sensor. InternalBronze–PlatinumbadgesandNASAmissionmatnotinternationalmedal/NASAadmission. W5–W6 sequentialgameversusindependentweeks needsclarification.',
 'FreshRoboTecnia/Ciberbots bodysamepreviousprogramme,no duplicatecamporunprovednewwinterdates/age/price. GlobalYouthMexicanoperatorTorontoEnglishlanguagecourse/purchaseflightservicebutflightsnotincluded;2027Drivebrochureunread/ageunknown,notnewvalidatedcamp. Robotiki404 despitefreshsearchsnippet. CPIC12+Julyarchiveoneday/MEPpublicschoolinfrastructure notnewopenholidayintake.',
 'All17 prior familypriceoffers exactly retained. FamilyICS2651:sevennewtentativeideasKuita3/Kiribati2/Yakaro2withage/language/foreignadmissiongates;allold2644UID/content retained except buildDTSTAMP. FiveAluna/Yubarkabothlater excluded. CompleteJSON/SQLiteZIP withouttruncation,filecaps checked.',
 '19directHTTPattempts/18HTTP200 (13HTML/5PDF),one404. FivePDF90pages text extracted;39fullselectedpages visuallyinspected,4renderedhistorypagesexcludedfromcount. Nativepublicationseparate. Noforms/messages/accounts/payments/consents/automations. Worldwidegoalactive,0fullyauditedcountries.'
]
priority='Continue deep Switzerland/France/Spain/Europe,Taiwan/Singapore/SouthKorea/Japan,USA/Canada,CostaRica/Mexico/LatinAmerica: all general/thematic/STEM camps2026–27,day/boarding/family and EN/ES/RU. Verify curriculum,actual teacher language,foreign individual intake,full two-child pricing/equipment/nightcare/insurance/refunds,quality shortlist and routes. Preserve worldwide competitions/leagues/exhibitions and permanent schools/5–10yearresults. No country/worldwide completion claim from a bounded pass.'
audit=dict(version=113,asof=CHECKED,status='progress',scope='Selected own Kajuyali2027 boarding brochures in Colombia/Panama, TalenttecCostaRica archive, deeper ProgramableArgentina syllabus and comparisons of existing Mexican holiday operators; not a complete country/world audit.',new_dossiers=len(NEW),new_dossier_slugs=NEW,updated_dossier_slugs=UPDATED,new_event_ids=newids,updated_event_ids=changed,events=len(now),camp_learning_records=blocks['Лагеря'],programme_dossiers=len(cp['profiles']),countries_with_dossiers=len(cp['countries']),official_dossier_urls=urls,editorial_scenarios=len(cp['shortlist']),coverage_gaps=len(cp['gaps']),country_dossier_counts=country_counts,competition_records=blocks['Соревнования'],exhibition_records=blocks['События'],league_profiles=len(d['league_guide']['profiles']),budget_scenarios=17,budget_providers=10,new_budget_scenarios=0,family_ical=family,exhibition_ical=expo,new_visual_pdf_checks=39,pdf_pages_text_extracted=90,external_actions=external,goal='active',worldwide_complete=False,fully_audited_countries=0,checks=checks,next_research=priority)
def write(stem,value):
 s=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(s);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(s)
write('latam-camps-audit-v113',audit)
write('latam-camps-source-receipts-v113',dict(version=113,asof=CHECKED,scope=audit['scope'],sources=sources,visual_review=visual,external_actions=external,primary_reader_limits='Public reader independently read Kajuyali/Programable. Talenttec reader timeout while directHTTP200bodyread. GlobalYouth linkedDrivebrochure not read. Additional CPIC/MEP facts are previous primary-reader comparisons, not claimed as new retainedHTTP bodies.'))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=113:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Native112 succeeded;commit '+BASE+';deployment appgdep_6ac4a5892ca88191ba7e0063ad918dc2. Worldwide objective remains active.')
plan['latest_validation']=dict(version=113,asof=CHECKED,status='Selected primary programme/visual sources and complete portable database checks; native publication separate',events=len(now),camp_learning_records=blocks['Лагеря'],programme_dossiers=846,countries_with_dossiers=39,official_dossier_urls=urls,editorial_scenarios=200,budget_scenarios=17,budget_providers=10,family_ical=family,exhibition_ical=expo,league_profiles=audit['league_profiles'],worldwide_complete=False,fully_audited_countries=0)
plan['latam_camp_programme_audit_v113']=audit;plan['complete_database_download']=sm;plan['complete_json_download']=jm
for q in plan['requirements']:
 if q['id']=='unified_database':q['evidence']='v113:3433cards/846dossiers/39countries;7newprofiles/12new2027boardingrows,oneProgramable syllabusdeepened;all3421prior eventobjects unchanged/all839priorprofileIDsretained. CompleteJSON/SQLiteZIPwithouttruncation.'
 elif q['id']=='camp_full_pricing':q['evidence']='v113:17priorfamilyestimatesunchanged. Kajuyali2027programme/tiquete/totalseparated;currency$codeabsent,fullforeignfamilyinvoice/insurance/refundunknown. TalenttecCRCJuly2026archivesnot2027quote. No newverifiedfullfamilybudget.'
 elif q['id']=='camp_calendar_2026_2027':q['evidence']='v113:12exactnewSummer2027boardingrows,sevennewtentativefamilyICSwithgates. FamilyICS2651/expo104;alloldUID/contentretained. No2027inventionfromTalenttec2026archive,Robotiki404 orMexicogeneralholidaypages.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=113]+[dict(version=113,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=7,updated_dossiers=1,new_calendar_rows=12,updated_calendar_rows=[],official_primary_retrieval_attempts=19,pdfs_downloaded=5,new_visual_pdf_checks=39,not_complete_worldwide=True)]
plan['next_research']=[priority];plan['status']=plan['native_goal_status']='active';plan['updated']=CHECKED;write('research-plan',plan)
p=ROOT/'dist/index.html';s=p.read_text().replace('?v=112','?v=113').replace('data-ui-version="112"','data-ui-version="113"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_latam_camps_audit_v113.json" download>Латинская Америка · пансионы 2027, цены, возраст и местная техника</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text();anchor='<a href="downloads/STEM_asia_camps_audit_v112.json"'
link='<a href="downloads/STEM_latam_camps_audit_v113.json" download>Латинская Америка: новые пансионы и возрастные условия ↓</a> · <a href="downloads/STEM_latam_camps_source_receipts_v113.json" download>Первичные страницы и проверенные брошюры ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(status='progress',version=113,new_dossiers=7,updated_dossiers=1,new_calendar_rows=12,dossiers=846,events=len(now),budget_scenarios=17,goal='active')))
