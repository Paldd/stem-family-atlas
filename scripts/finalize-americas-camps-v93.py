"""Bounded Americas progress receipt; keep the expanded worldwide goal active."""
import hashlib,json,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v93'
BASE='b8d62c95ab3e34a15f9e389a957caca9792b3758'
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};op={p['slug']:p for p in b['camp_programmes']['profiles']}
fresh=[p for p in c['profiles'] if p['slug'] not in op];new=[e for e in d['events'] if e['id'] not in old]
assert len(fresh)==10 and len(new)==24 and c['counts']['dossiers']==621 and c['counts']['source_urls']==965
assert all(e==old[e['id']] for e in d['events'] if e['id'] in old)
receipts=[q for f in sorted(PRIMARY.glob('receipt-*.json')) for q in json.loads(f.read_text())]
assert len(receipts)==37 and sum(q.get('status')==200 for q in receipts)==29
scopes={
 'coyote-home':'Direct serverHTML ownpage initially summer7100/5300 andEasterTBD. Rendered dynamicdata differ:8500/6500 and29Mar–3Apr2027. Actual price-year/waitlist/room/packing conflicts retained. Ownpublicprogrammes distinct fromprivategroups.',
 'coyote-autumn-form':'Ownread-onlygenericJSregistrationtemplate, samebodyasWinterform. Nofinalquote/nochildfields/noSubmit; actualfees/dates fromownmainpage andrenderedpricetable.',
 'coyote-winter-form':'Ownread-onlygenericJSform, not a selectedbasket orfinalinvoice. NoSubmit; sourcealone not currentavailabilityproof.',
 'tamarindo-kids':'Owncurrent2027Elementary5–10/10hSpanish/$797 andnineMondaystarts. RelevantFAQ andsource-year boundariesread; hiddenold2026weeks notadmitted. Visiblecurrentprogramme inspected separately. BilingualstaffnotfullENteaching.',
 'tamarindo-terms':'Actualpublishedterms applyNov2025 throughend2026season; $10050percentregistration,deposit/cancel/changefees read. Notconfirmed2027contract orfinalregistrationfee.',
 'tamarindo-services':'Ownadditionalservicescontextread. Optionalparents/course/extraactivitiesseparate; noallservices/prices audited orbooking.',
 'tamarindo-staff':'Ownnamedteachers/nativeSpanish/bilingualsupportcontextread; notguaranteeall-dayEnglishorparticularElementaryteacher.',
 'tamarindo-lodging':'Relevantownfamilyunit155/170/205/265/90night,occupancy/min6nights/discount14+15percent28+30percent read. Year/currency/tax/currentavailabilityunconfirmed. 2-personkitchenettenot4-personfamilyroom.',
 'oaktree-home':'Ownpreschoolidentity/locationread; genericschoolages/language notcampprogramme proof.',
 'oaktree-services':'Ownregularpreschoollevels/playlearn/clubsread; afternoon12–17:30 notChristmascampdailyhours; noactualcampage/foreignintake/fee/EN admitted.',
 'oaktree-calendar':'Actualone-pageCalendar2026 visuallyread:Christmas7–11/14–18Dec2026, Summerstart4Jan2027. Schoolstart1Feb notcampend. Noverifiedprogramme dossier/ICSadmittedwithoutcampprofileconditions.',
 'ciberbots-services':'OwnSummer/Easter Próximo2027 andChristmasDiciembre2026 programme durations/kitsread. Regular4–6/7–8/9–11/11+ notholidaygate. Futuremonthlabels notexactdates;existingdossierdeepened,alloldeventsunchanged.',
 'cube-winter':'Own21–23Dec2026,255/275+HST,112.50careandseparate42mealadd-on; package275foodnotdoublecharged. ActualenteringGrade2asofSep2026, MarchBreak2026exceptionnotWinter. Beginnercurriculum/refund/locationcontextread.',
 'icc-upcoming':'Ownpublicsessionindex144results, relevant11YoungInnovators2027cohortsread. Notall144sessions/programmes/operators audited. Each11techheadingcard retrieved separately; Bollywoodcategory/bodyconflict preserved.',
 'icc-refund':'HTTP200ownrefundpolicybodycontainsheader/footerwithoutactualrefundterms. Notnorefundpromise orpolicyverification.',
 'icc-faq':'HTTP200ownFAQbodywithoutactualanswers. NoFAQsubstanceclaimed.',
 'nr-holidays':'HTTP200actualcurrentReactshell/header/footeronly, rendered same. CacheKidsdates/agesnotadmitted ascurrentprogramme; nofullBraziloperatoraudit.',
 'nr-2027-contract':'Actualown-linked9page2027servicecontractPDF. Relevant2ndweek/payment/accidentinsurance/passport/cancellation clauses read; pages3/6visuallyread. Dobra8617.50/9048.50/9257onlyextra2ndweekafterarrival, notinitialfee. Notall9pagesclausesaudited/accepted; noage/date/teachinglanguageproved.',
 'harmony-camp':'Direct403retainedaserror, cachedweb2025notcurrentproof. Actualrenderedownpage separatelyconfirmsJuly5–16,2027, withoutage/fee/language/dayboarding. Gaprecorded, notverifiedcampdossier.',
 'robotiki-camps':'Direct404; cachedsearchannouncementnotactualfuturecampdate/feeproof. No programme admitted.',
 'snap-roundrock-camps':'Direct403. Cached/primarywebextractobservationsnotpromoted tofullydatedcurrentcohortwithoutyear/registration/feeverification.',
 'nr-kids-legacy':'SelfsignedTLSfailure; certificatevalidationnotbypassed. Staginglegacydatesnotconfirmedcurrentprogramme.'
}
for q in receipts:
 q['retrieval_method']='direct_http'
 q['content_scope']=scopes.get(q['key'],
  'RelevantownICCYoungInnovatorsdetaildates2027/age5–14/429419/70lunch60AM99PM/deadline10AMfirstday/openingsread. TechheadingversusBollydancebodyconflict; exacttechnicalsyllabus/teachinglanguage/refund/foreignadmissionunconfirmed; noform/account/payment.' if q['key'].startswith('icc-') else
  'Directerrorretained; noverifiedbody/programme/currentprice inferred; no guessedalternatepath admitted.')
 if q.get('status')==200:
  f=next(f for f in [PRIMARY/(q['key']+'.pdf'),PRIMARY/(q['key']+'.html')] if f.exists())
  assert hashlib.sha256(f.read_bytes()).hexdigest()==q['sha256'];q.update(raw_filename=f.name,body_snapshot_retained=True)
observ=PRIMARY/'rendered-observations.json';o=json.loads(observ.read_text())
additional=[dict(key=q['key'],url=q['url'],retrieval_method='rendered_primary_observation',raw_filename=observ.name,sha256=hashlib.sha256(observ.read_bytes()).hexdigest(),bytes=observ.stat().st_size,body_snapshot_retained=False,content_scope=q['scope']+' Manuallytranscribedrelevantexcerpts fromactualCUAAXoutputs; notfullDOM/HTMLcapture.') for q in o['observations']]
oldurls={s['url'] for p in op.values() for s in p['sources']};added=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-oldurls);assert len(added)==24
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False)
byiso={s:sum(p['iso']==s for p in c['profiles']) for s in ['CHE','FRA','ESP','GBR','DEU','AUT','NLD','TWN','SGP','JPN','KOR','MYS','PHL','AUS','USA','CAN','CRI','MEX','BRA','CHL']}
checks=[
 '10newdossiers across3newoperatorgroups:Explornatura1/Coyote3/ICC5 plusCube1existingoperatornewWintertrack.1Ciberbotsdeepened;all611priorIDs/order/all610otherprofiles/all3097priorevents unchanged.24newfutureprogrammerows and11actualregistrationdeadlineICS produce35newfamilyICS; exhibition104unchanged.',
 'TamarindoElementary5–10/10hSpanish/$797/nineexplicitMondaystarts2027,M–F08–14. Fridayendscalculatedpublishedrule; hiddenold2026weeksnotcurrentcalendar. ENstaff/website notENcampteaching; ESrolelanguage_lessons. Unit155/170/205/min6nights optionalfamilyhousing separate, provisional2kids+6nights155=2524assumingcurrencyequal excludesfees/tax/registration; notfinalall-in. Terms2026 not2027contract;10050percentregistrationnotdefinitivefullfee.',
 'Coyote actualrenderedupdates8500/6500 andEaster29Mar–3Apr2027 againstinitialHTML7100/5300/TBD; ref2026/waitlistretained. SummerJuly/Augustunknownexactdaysnotinvented. Short4000/3300/early2805until20Nov,2siblings7200/5940notstackearly;deposits1200/990priceparts. Room4–6vs3–4/packingconflict and30percentretained/excessvoucher6mo included. Individual6–14notprivategroup5–18;Oscar2026needs6birthday. EN/ESactualteachingunconfirmed.',
 'ICC11directdetailcards:fiveowntechheadings,all5–14,429/419 and70+60+99optional=658/weekchild;noautomaticdouble10siblingsdiscount. OwnBollydancebody/category conflict meansactualtechnicalsyllabus/projects/hardwareunknown;notverified15hrobotics/toprecommendation. PortalUIEnglish/Spanishnotinstruction. Emptyrefund/FAQnotpolicy. Ownopeningsnotacceptedchild/guaranteedplace. Actualdeadline10AMfirstdayagainstcamp09:30 recorded,notUTCinferred.',
 'CubeWinter21–23Dec2026/Beaches65GlenManor/notoldJulyWesleyfooter.255/275+112.50+HST,fullmealcare387.50+HST;42mealaddonnotagainon275. Grade2asofSep2026notbirthyear;March2026exceptionnotWinter. Allbeginnersnotadvancedindividualcurriculum; languageunknown; refunds65fee and10/20dayboundariesretained.',
 'CiberbotsChristmasmonth2026/SummerEaster2027 labelsnotexactdates;holidaydurations/contentadded,regularschoolagegatesnotcampintake;bothFITunknown. HarmonyactualrenderJuly5–16,2027butmissingage/price/format/teaching;OaktreePDFdates/startonlywithoutcampconditions;recordedgapsnotverifiedprofiles. NRcontractDobraonlysecondweekextra notcampbaseprice;currentholidaysshell/cache/TLSfail/notwholeBrazilcovered.',
 '37directattempts/29HTTP200/8errors;3separaterenderedprimaryobservationswithmethodexplicit;2actualPDFs/relevantsectionsread/3visualpagechecks/3renders. Rawoutsidecheckout,publiconlyparaphrases/URLs/hashes/errors; noform/account/message/payment/subscription/automation. FailedDOMlocatornotcontentreadclaim; CoyoteactualFAQdiscount/cancelexpanded,packingnotexpanded.',
 '621dossiers/37countries/965distinctdossierURLs,140familycomparisons;3121events/1790camp-learningrows/2382familyICS/104exhibitICS.1327manageddated/69legacyreuse/39seasonwindows.249worldcountries/82withrecords/0fullyaudited. Expandedworldwidegoal remainsactive;league/competition/exhibit/school/history/familyroute scopeunchanged.'
]
audit=dict(asof='2026-10-05',version=93,status='progress',scope='DeeperCostaRica/Mexico/USA/Canada programmes2026–27 and boundedBrazil/Argentina evidence gaps; priorEurope/Asia/worldwideworkpreserved, notglobalcompletion.',new_dossiers=10,new_operator_groups=3,existing_operator_new_tracks=1,new_calendar_rows=24,new_family_ics=35,new_registration_deadline_ics=11,updated_dossiers=['ciberbots'],corrected_existing_event_ids=[],programme_dossiers=621,countries_with_dossiers=37,official_dossier_urls=965,country_dossier_counts=byiso,programme_slugs=[p['slug'] for p in fresh],findings=c['gaps'][-4:],calendar=dict(events=3121,learning_records=1790,family_ics=2382,exhibition_ics=104,managed_dated_rows=1327,reused_legacy_events=69,season_windows=39),primary_retrievals=dict(direct_attempts=37,http200=29,errors=8,additional_rendered_primary_observations=3,actual_pdfs=2,visual_page_checks=3,retained_page_renders=3),fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,next_priority='ContinueSwitzerland/France/Spain/Europe andTaiwan/Singapore/Korea/Japan/Asia,USA/Canada/CostaRica/Mexico/LatinAmerica/allworld2026–27 general/technical/boarding/day/familycamps: primaryprogrammes/currentseasoncontracts/fullinvoice/age/actualgrade/teachinglanguage/foreignintake/currentplaces. League/competition/exhibitadmission/schools/results5–10years/familyroutes preserved;0countriesfullyaudited.')
def write(stem,value):
 t=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(t);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(t)
write('americas-camp-audit-v93',audit)
write('americas-camp-source-receipts-v93',dict(asof='2026-10-05',version=93,scope='37directattempts/29HTTP200/8errors,3actualrenderedprimaryobservations,2actualPDFs/relevantclauses/3visualpages;notwholeoperator/countryaudit.',sources=receipts,additional_retrieval_methods=additional,dossier_source_urls_added=added,external_actions=external,notes=['RawHTML/PDF/rendersoutsidecheckout. Publicexports paraphrases/URLs/hashes/errors; manuallytranscribedbrowserobservationsnotfullDOMcapture.','Publisheddate/tuition/currentplace/teachinglanguage/actualadmission/seasoncontract aredistinct. DynamicCoyotevaluesoverrideinitialdefaultHTMLbutpriceyear/waitlistconflictsretained.','NoEnglishteachingfromwebsite/portaltranslation, actualschoolgradesnotinferred; noallcountry/worldwidecompletionclaim.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=93:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',evidence='v92nativepublication succeeded;commitb8d62c95ab3e34a15f9e389a957caca9792b3758;deploymentappgdep_6ac4342eb9d8819192978519ead8001f. Expandedworldwidescopepreserved.')
plan['latest_validation']=dict(version=93,asof='2026-10-05',status='Independentprimary/preservation/calendarverification;nativepublicationreceiptseparate',events=3121,camp_learning_records=1790,programme_dossiers=621,countries_with_dossiers=37,official_dossier_urls=965,family_ical=2382,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=byiso)
plan['americas_camp_programme_audit_v93']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=621,countries=37,swiss=85,generated_calendar_entries=1327,reused_legacy_events=69)
for q in plan['requirements']:
 if q['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:q['evidence']='v93:621programme/venue/formatdossiers37countries;10new+1deepened,24newfutureprogrammerows+11deadlines/35familyICS,965dossierURLs. Ownage/language/fees/seasoncontracts/dynamicdata/readonlydetailcards;allcountry/worldwidecompletionnotachieved.'
entry=dict(version=93,asof='2026-10-05',status='progress',scope=audit['scope'],new_dossiers=10,deepened_dossiers=1,new_calendar_rows=24,new_family_ics=35,official_primary_sources=24,not_complete_worldwide=True)
plan.setdefault('research_passes',[])[:]=[q for q in plan.get('research_passes',[]) if q.get('version')!=93]+[entry]
plan['next_research']=[audit['next_priority']];plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05';write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=92','?v=93').replace('data-ui-version="92"','data-ui-version="93"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_americas_camp_audit_v93.json" download>Америка: новые сезоны и подробный прайс ↓</a> · <a href="downloads/STEM_americas_camp_source_receipts_v93.json" download>Первичные источники и расхождения ↓</a> · '
anchor='<a href="downloads/STEM_asia_camp_audit_v92.json"'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
s=s.replace("!['closed','not_open_yet'].includes(p.availability?.status)","!['closed','not_open_yet','waitlist'].includes(p.availability?.status)")
s=s.replace("p.availability?.status==='not_open_yet'?'Набор ещё не открыт':statusLabels", "p.availability?.status==='not_open_yet'?'Набор ещё не открыт':p.availability?.status==='waitlist'?'Лист ожидания':statusLabels")
p.write_text(s)
print(json.dumps(dict(dossiers=621,new_dossiers=10,deepened_dossiers=1,new_calendar_rows=24,new_family_ics=35,source_urls=965,goal='active')))
