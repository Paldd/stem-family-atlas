'use strict';

window.initAtlasLinks = function initAtlasLinks(state, leagueProfiles) {
  const supportedViews = new Set(['catalog', 'exhibitions']);
  const selects = {
    kid: 'kid', region: 'region', country: 'country', theme: 'theme',
    language: 'language', languageMode: 'language-mode', scope: 'scope',
    participation: 'participation', admission: 'admission', evidence: 'evidence',
    visitorPolicy: 'visitor-policy', dates: 'date', sort: 'sort'
  };
  const choices = new Map(Object.entries(selects).map(([key, id]) => [
    key, new Map(Array.from(document.getElementById(id + '-filter').options,
      option => [option.dataset.atlasValue ?? option.value, option.value]))
  ]));
  choices.set('block', new Map(Array.from(document.querySelectorAll('.block-tabs [data-atlas-value]'),
    button => [button.dataset.atlasValue, button.dataset.block])));
  choices.set('league', new Map(leagueProfiles.map(league => [league.id, league.id])));
  const booleanKeys = ['best', 'campProjects', 'online', 'priority'];
  const maxQuery = document.getElementById('search').maxLength;
  const shareButton = document.getElementById('share-filters');
  const eventDialog = document.getElementById('event-dialog');
  const dialog = document.getElementById('atlas-share-dialog');
  const input = document.getElementById('atlas-share-url');
  const status = document.getElementById('atlas-share-status');
  const param = key => 'atlas_' + key;

  function publicURL() {
    if (['localhost', '127.0.0.1', '[::1]'].includes(location.hostname)) {
      const base = 'https://paldd.github.io/stem-family-atlas/';
      return new URL(document.documentElement.lang === 'es' ? 'es/' : './', base);
    }
    return new URL('./', location.href);
  }

  function filterURL() {
    const url = publicURL();
    url.hash = state.view;
    url.searchParams.set(param('view'), state.view);
    for (const [key, values] of choices) {
      const stable = Array.from(values).find(([, value]) => value === state[key])?.[0];
      if (stable) url.searchParams.set(param(key), stable);
    }
    for (const key of booleanKeys) if (state[key]) url.searchParams.set(param(key), '1');
    if (!state.excluded) url.searchParams.set(param('excluded'), '0');
    if (state.query) url.searchParams.set(param('query'), state.query.slice(0, maxQuery));
    if (Array.isArray(state.routeIsos) && state.routeIsos.length) {
      url.searchParams.set(param('route'), state.routeIsos.join(','));
    }
    return url;
  }

  function restore(view) {
    const params = new URL(location.href).searchParams;
    if (!supportedViews.has(view) || params.get(param('view')) !== view) return false;
    for (const [key, values] of choices) {
      const fallback = key === 'sort' ? (view === 'exhibitions' ? 'date' : 'priority') : '';
      state[key] = values.get(params.get(param(key))) ?? fallback;
    }
    for (const key of booleanKeys) state[key] = params.get(param(key)) === '1';
    state.excluded = params.get(param('excluded')) !== '0';
    state.query = (params.get(param('query')) ?? '').slice(0, maxQuery);
    state.routeIsos = [...new Set((params.get(param('route')) ?? '').split(',')
      .filter(iso => iso && choices.get('country').has(iso)))];
    return true;
  }

  function navigate(view) {
    if (location.hash === '#' + view) return;
    const url = new URL(location.href);
    for (const key of [...url.searchParams.keys()]) {
      if (key.startsWith('atlas_')) url.searchParams.delete(key);
    }
    url.hash = view;
    history.pushState(null, '', url);
  }

  function show(url) {
    input.value = url.href;
    status.textContent = '';
    dialog.showModal();
    input.focus();
    input.select();
  }

  shareButton.onclick = () => show(filterURL());
  eventDialog.addEventListener('click', event => {
    if (!event.target.closest('[data-share-event]') || !eventDialog.dataset.eventId) return;
    const url = publicURL();
    url.hash = state.view === 'exhibitions' ? 'exhibitions' : 'catalog';
    url.searchParams.set(param('event'), eventDialog.dataset.eventId);
    show(url);
  });
  document.getElementById('atlas-copy-link').onclick = async () => {
    try {
      await navigator.clipboard.writeText(input.value);
      status.textContent = status.dataset.copied;
    } catch {
      input.focus();
      input.select();
      status.textContent = status.dataset.manual;
    }
  };

  return {
    restore,
    navigate,
    syncButton() { shareButton.hidden = !supportedViews.has(state.view); },
    openSharedEvent(view, openEvent, notify) {
      const id = new URL(location.href).searchParams.get(param('event'));
      if (!supportedViews.has(view) || !id || (eventDialog.open && eventDialog.dataset.eventId === id)) return;
      if (!openEvent(id)) notify(dialog.dataset.missingEvent);
    }
  };
};
