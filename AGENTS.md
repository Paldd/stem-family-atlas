# STEM Family Atlas — working and publication instructions

The user's canonical repository is `Paldd/stem-family-atlas`. The production host is GitHub Pages. The user explicitly requested that this repository hold the latest atlas and that updates be published there. After completing an authorized atlas change, commit and push the reviewed source to `origin/main`, then check the `Publish STEM Atlas` workflow and the production URL. Report a failed deployment plainly; a push alone is not publication.

Use `data/catalog.json` as the source of truth. `data/camp-programmes-deep-2026-2027.json` and the existing integration scripts supply detailed camp records. Run `python3 scripts/build-database.py` and `python3 scripts/verify-site.py`; JavaScript syntax and meaningful changed interactions must pass before pushing. The workflow rebuilds full exports and publishes `dist/`. Do not discard full records to fit a hosting limit.

Keep competitions, exhibitions, camps/learning, schools and league profiles distinct. Dossiers, variants, providers, confirmed dates, old seasons, pending enrollment and actual acceptance are different states. Preserve family language/age conditions and each source's verification date. The worldwide audit is unfinished; never call the inventory a complete world ranking.

Use the supported Cua browser surface for UI testing. Check the affected behavior and a representative mobile/desktop view when presentation changes. Preserve reduced-motion support. Browser-local plans are not synchronized accounts or registrations.

The older Sites history is retained locally on `sites-local-v137`; `.openai/` is local metadata and is ignored by this GitHub branch. Do not attempt Sites publication or create a replacement Sites project unless the human specifically requests it.

Do not publish credentials, private organizer forms, raw private browser snapshots or local account configuration. Do not contact organizers, enroll children, accept agreements or make payments without a specific human instruction.
