/* Interactive motion is presentation only; it never completes family tasks. */
(() => {
  'use strict';
  const q = s => document.querySelector(s);
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const fine = matchMedia('(hover: hover) and (pointer: fine)');
  const stages = [
    ['Идея', 'Выбрать задачу и понять, кому пригодится решение.'],
    ['Сборка', 'Собрать прототип и написать собственный код.'],
    ['Испытание', 'Измерить результат, найти ошибку и повторить тест.'],
    ['Объяснение', 'Показать работу и объяснить свои решения.']
  ];
  let paused = false;
  try { paused = localStorage.getItem('stemAtlasMotion.v1') === 'paused'; } catch {}
  let scene, path, token, trace, eyes, stage = 0, progress = 0, tween = null;
  let stops = [0, 1 / 3, 2 / 3, 1];
  let playing = false, visible = false, frame = 0, last = 0, refreshFrame = 0;
  let ringValue = null, ringContext = '', ringAnimation = null;
  const pendingReveal = new Set();
  const watchedRegions = new Set();
  const enabled = () => !paused && !reduced.matches && !document.hidden;

  const reveal = new IntersectionObserver(entries => {
    for (const entry of entries) if (entry.isIntersecting) {
      entry.target.classList.add('motion-revealed');
      reveal.unobserve(entry.target); pendingReveal.delete(entry.target);
    }
  }, {threshold: .06});
  const sceneObserver = new IntersectionObserver(entries => {
    for (const entry of entries) if (entry.target === scene) {
      visible = entry.isIntersecting;
      scene.dataset.onscreen = String(visible);
      if (visible) resume(); else stopFrame();
    }
  }, {threshold: .08});
  const regionObserver = new IntersectionObserver(entries => {
    for (const entry of entries) entry.target.dataset.motionOnscreen = String(entry.isIntersecting);
  }, {threshold: .05});

  function stopFrame() { cancelAnimationFrame(frame); frame = 0; last = 0; }
  function paint(value) {
    progress = Math.max(0, Math.min(1, value));
    if (!path || !token) return;
    const length = path.getTotalLength(), point = path.getPointAtLength(length * progress);
    token.setAttribute('transform', `translate(${point.x} ${point.y})`);
    trace.setAttribute('stroke-dasharray', `${length * progress} ${length}`);
    scene.dataset.progress = progress.toFixed(3);
  }
  function updateStage(i) {
    stage = i;
    if (!scene) return;
    scene.dataset.stage = String(i);
    scene.querySelectorAll('[data-motion-stage]').forEach(b => b.setAttribute('aria-pressed', String(Number(b.dataset.motionStage) === i)));
    scene.querySelector('.motion-stage-title').textContent = `${String(i + 1).padStart(2, '0')} · ${stages[i][0]}`;
    scene.querySelector('.motion-stage-copy').textContent = stages[i][1];
    scene.querySelectorAll('.motion-node').forEach((node, n) => node.classList.toggle('active', n === i));
  }
  function updatePlay() {
    const button = scene?.querySelector('[data-motion-play]');
    if (!button) return;
    button.textContent = playing ? 'Ⅱ Остановить цикл' : '▷ Показать цикл';
    button.setAttribute('aria-pressed', String(playing));
    button.disabled = !enabled();
    button.title = reduced.matches ? 'Системная настройка уменьшает движение. Можно выбирать этапы.' : paused ? 'Сначала включите движение в верхней панели.' : '';
  }
  function resume() {
    if (!frame && tween && visible && enabled()) frame = requestAnimationFrame(tick);
  }
  function tick(now) {
    frame = 0;
    if (!scene?.isConnected || !enabled() || !visible || !tween) { last = 0; return; }
    tween.elapsed += last ? Math.min(now - last, 50) : 0; last = now;
    const t = Math.min(1, tween.elapsed / tween.duration), ease = t * t * (3 - 2 * t);
    paint(tween.from + (tween.to - tween.from) * ease);
    if (t === 1) {
      tween = null;
      if (playing && stage < 3) {
        updateStage(stage + 1);
        tween = {from: progress, to: stops[stage], elapsed: 0, duration: 1700};
      } else { playing = false; updatePlay(); }
    }
    resume();
  }
  function selectStage(i) {
    playing = false; updateStage(i); updatePlay();
    if (enabled()) tween = {from: progress, to: stops[i], elapsed: 0, duration: 850};
    else { tween = null; paint(stops[i]); }
    resume();
  }
  function syncMotion() {
    const on = enabled();
    document.body.classList.toggle('motion-paused', !on);
    document.body.dataset.motion = reduced.matches ? 'reduced' : paused ? 'paused' : 'on';
    const button = q('[data-motion-toggle]');
    if (button) {
      button.setAttribute('aria-pressed', String(!paused));
      button.setAttribute('aria-label', reduced.matches ? 'Системное уменьшение движения включено' : paused ? 'Включить анимации' : 'Поставить анимации на паузу');
      button.querySelector('span').textContent = reduced.matches ? 'Движение: минимум' : paused ? 'Движение: пауза' : 'Движение: вкл';
      button.querySelector('b').textContent = on ? 'Ⅱ' : '▷';
      button.disabled = reduced.matches;
    }
    if (!on) {
      stopFrame();
      document.querySelectorAll('.motion-card').forEach(resetCard);
      if (ringAnimation) { ringAnimation.cancel(); ringAnimation = null; }
      if (reduced.matches && tween) { paint(tween.to); tween = null; playing = false; }
    } else resume();
    updatePlay();
  }
  function initializeScene() {
    const next = q('.motion-lab');
    if (next === scene) return;
    if (scene) sceneObserver.unobserve(scene);
    stopFrame(); playing = false; tween = null; visible = false;
    scene = next;
    if (!scene) return;
    path = scene.querySelector('.ux-drawn-path');
    const partial = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    partial.setAttribute('d', 'M55 175C150 175 125 66 230 66');
    const first = partial.getTotalLength();
    partial.setAttribute('d', 'M55 175C150 175 125 66 230 66S295 183 385 183');
    stops = [0, first / path.getTotalLength(), partial.getTotalLength() / path.getTotalLength(), 1];
    trace = scene.querySelector('.motion-route-trace');
    token = scene.querySelector('.motion-token');
    eyes = Array.from(scene.querySelectorAll('.motion-eye'));
    updateStage(stage); paint(stops[stage]); updatePlay();
    sceneObserver.observe(scene);
  }
  function refresh() {
    refreshFrame = 0; initializeScene();
    for (const node of pendingReveal) if (!node.isConnected) { reveal.unobserve(node); pendingReveal.delete(node); }
    for (const node of watchedRegions) if (!node.isConnected) { regionObserver.unobserve(node); watchedRegions.delete(node); }
    document.querySelectorAll('.ux-task,.ux-choice,.ux-region-card,.ux-start-card,.event-card,.school-card').forEach((card, i) => {
      if (card.dataset.motionReady) return;
      card.dataset.motionReady = 'true'; card.classList.add('motion-card');
      card.style.setProperty('--motion-delay', `${Math.min(i % 6, 3) * 45}ms`);
      card.classList.add('motion-enter'); pendingReveal.add(card); reveal.observe(card);
      if (card.matches('.ux-region-card')) { watchedRegions.add(card); regionObserver.observe(card); }
    });
  }
  function scheduleRefresh() { if (!refreshFrame) refreshFrame = requestAnimationFrame(refresh); }
  function resetCard(card) {
    card.style.removeProperty('--motion-rx'); card.style.removeProperty('--motion-ry');
    card.classList.remove('motion-tracking');
  }
  document.addEventListener('pointermove', e => {
    if (!enabled() || !fine.matches || e.pointerType === 'touch') return;
    const lab = e.target.closest('.motion-lab');
    if (lab === scene && eyes) {
      const bounds = lab.getBoundingClientRect();
      const x = Math.max(-3, Math.min(3, ((e.clientX - bounds.left) / bounds.width - .5) * 6));
      const y = Math.max(-2, Math.min(2, ((e.clientY - bounds.top) / bounds.height - .5) * 4));
      eyes.forEach(eye => eye.setAttribute('transform', `translate(${x} ${y})`));
    }
    const card = e.target.closest('.motion-card');
    if (!card) return;
    const rect = card.getBoundingClientRect(), x = (e.clientX - rect.left) / rect.width, y = (e.clientY - rect.top) / rect.height;
    card.style.setProperty('--motion-rx', `${(y - .5) * -3}deg`);
    card.style.setProperty('--motion-ry', `${(x - .5) * 3}deg`);
    card.style.setProperty('--motion-light-x', `${x * 100}%`);
    card.style.setProperty('--motion-light-y', `${y * 100}%`);
    card.classList.add('motion-tracking');
  }, {passive:true});
  document.addEventListener('pointerout', e => {
    const card = e.target.closest('.motion-card');
    if (card && !card.contains(e.relatedTarget)) resetCard(card);
    if (scene && scene.contains(e.target) && !scene.contains(e.relatedTarget)) eyes?.forEach(eye => eye.removeAttribute('transform'));
  }, {passive:true});
  document.addEventListener('click', e => {
    const stageButton = e.target.closest('[data-motion-stage]');
    if (stageButton) selectStage(Number(stageButton.dataset.motionStage));
    if (e.target.closest('[data-motion-play]')) {
      if (playing) { playing = false; tween = null; stopFrame(); }
      else if (enabled()) {
        playing = true; updateStage(0); paint(0);
        tween = {from:0,to:0,elapsed:0,duration:900}; resume();
      }
      updatePlay();
    }
    if (e.target.closest('[data-motion-toggle]')) {
      paused = !paused;
      try { localStorage.setItem('stemAtlasMotion.v1', paused ? 'paused' : 'on'); } catch {}
      syncMotion();
    }
    const button = e.target.closest('button');
    if (button && enabled() && button.animate) {
      button.animate([{scale:'1'},{scale:'.96'},{scale:'1'}],{duration:220,easing:'ease-out'});
    }
  });
  document.addEventListener('change', e => {
    if (!e.target.matches('[data-ux-task]')) return;
    const id = e.target.dataset.uxTask, checked = e.target.checked;
    const ring = q('.ux-progress-ring');
    if (ring && enabled()) {
      ring.animate([{scale:'.94'},{scale:'1.06'},{scale:'1'}],{duration:550,easing:'ease-out'});
      const value = parseFloat(ring.style.getPropertyValue('--progress'));
      if (ringValue !== null && ringContext === context()) {
        ringAnimation?.cancel();
        ringAnimation = ring.animate([{'--progress':`${ringValue}deg`},{'--progress':`${value}deg`}],{duration:650,easing:'cubic-bezier(.2,.8,.2,1)'});
      }
      ringValue = value; ringContext = context();
      if (checked) q(`[data-ux-task="${id}"]`)?.closest('.ux-task')?.animate([{boxShadow:'0 0 0 0 #f28b5660'},{boxShadow:'0 0 0 12px #f28b5600'}],{duration:700,easing:'ease-out'});
    }
  });
  function context() { return Array.from(document.querySelectorAll('.ux-child-tabs [aria-pressed=true],.ux-goal-grid [aria-pressed=true],#ux-track-select,#ux-base-select')).map(n=>n.value||n.dataset.uxChild||n.dataset.uxGoal).join('|'); }
  const journey = q('#journey-content');
  if (journey) new MutationObserver(() => {
    scheduleRefresh();
    if (context() !== ringContext) { ringContext = context(); ringValue = parseFloat(q('.ux-progress-ring')?.style.getPropertyValue('--progress') || '0'); }
  }).observe(journey,{childList:true});
  document.addEventListener('stem:render',scheduleRefresh);
  document.addEventListener('visibilitychange',syncMotion);
  reduced.addEventListener('change',syncMotion);
  ringContext = context(); ringValue = parseFloat(q('.ux-progress-ring')?.style.getPropertyValue('--progress') || '0');
  syncMotion(); refresh();
})();
