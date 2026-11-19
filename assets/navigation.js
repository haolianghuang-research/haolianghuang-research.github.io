// A persistent desktop outline becomes a native modal drawer on smaller screens.
const outline = document.querySelector('#page-outline');
const contentsToggle = document.querySelector('.contents-toggle');
const siteHeader = document.querySelector('[data-site-navigation]');
if (outline && contentsToggle && siteHeader) {
  document.body.dataset.navReady = '';
  contentsToggle.hidden = false;
  const wide = matchMedia('(min-width: 1480px)');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const closeButton = outline.querySelector('.outline-close');
  const links = [...outline.querySelectorAll('[data-outline-target]')];
  const targets = links.map(link => document.getElementById(link.dataset.outlineTarget)).filter(Boolean);
  const primaryLinks = [...siteHeader.querySelectorAll('[data-nav-section]')];
  const progress = outline.querySelector('progress');
  const percent = outline.querySelector('[data-reading-percent]');
  const preferenceKey = 'haoliang.portfolio.outline';
  let queued = false;

  function wantsPinned() {
    try { return sessionStorage.getItem(preferenceKey) !== 'closed'; } catch { return true; }
  }
  function rememberPinned(open) {
    if (!wide.matches) return;
    try { sessionStorage.setItem(preferenceKey, open ? 'open' : 'closed'); } catch {}
  }
  function syncLayout() {
    contentsToggle.setAttribute('aria-expanded', String(outline.open));
    document.body.toggleAttribute('data-outline-pinned', wide.matches && outline.open);
    scheduleUpdate();
  }
  function openContents() {
    if (outline.open) return;
    const readingY = scrollY;
    outline.classList.toggle('is-pinned', wide.matches);
    if (wide.matches) {
      // A modeless outline should not steal keyboard focus during page load.
      outline.setAttribute('open', '');
    } else {
      outline.showModal();
    }
    if (!reducedMotion.matches) outline.animate([
      {transform:'translateX(-30px)',opacity:0},
      {transform:'translateX(0)',opacity:1}
    ], {duration:220,easing:'cubic-bezier(.22,1,.36,1)'});
    syncLayout();
    // Preserve the page position when the browser anchors a newly opened dialog.
    requestAnimationFrame(() => { scrollTo({top:readingY,behavior:'auto'}); scheduleUpdate(); });
  }
  function closeContents(restoreFocus = false, remember = true) {
    if (remember) rememberPinned(false);
    outline.close();
    syncLayout();
    if (restoreFocus) contentsToggle.focus({preventScroll:true});
  }
  contentsToggle.addEventListener('click', () => {
    if (outline.open) closeContents(true);
    else { rememberPinned(true); openContents(); }
  });
  closeButton.addEventListener('click', () => closeContents(true));
  outline.addEventListener('cancel', event => { event.preventDefault(); closeContents(true); });
  outline.addEventListener('close', syncLayout);
  outline.addEventListener('click', event => {
    if (event.target !== outline || wide.matches) return;
    const box = outline.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) closeContents(true);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && wide.matches && outline.open) { event.preventDefault(); closeContents(true); }
  });
  links.forEach(link => link.addEventListener('click', () => {
    if (!wide.matches) {
      closeContents(false, false);
      const target = document.getElementById(link.dataset.outlineTarget);
      requestAnimationFrame(() => {
        if (!target) return;
        const hadTabindex = target.hasAttribute('tabindex');
        if (!hadTabindex) target.setAttribute('tabindex','-1');
        target.focus({preventScroll:true});
        if (!hadTabindex) target.addEventListener('blur',()=>target.removeAttribute('tabindex'),{once:true});
      });
    }
  }));
  wide.addEventListener('change', () => {
    if (outline.open) closeContents(false, false);
    if (wide.matches && wantsPinned()) openContents();
    syncLayout();
  });

  function updateCurrent() {
    queued = false;
    const limit = siteHeader.offsetHeight + 54;
    let active = targets[0]?.id;
    let nearestTop = -Infinity;
    let hashTarget = '';
    try { hashTarget = decodeURIComponent(location.hash.slice(1)); } catch {}
    for (const target of targets) {
      const top = target.getBoundingClientRect().top;
      if (top <= limit && (top > nearestTop + 1 || (Math.abs(top - nearestTop) <= 1 && target.id === hashTarget))) {
        active = target.id;
        nearestTop = top;
      }
    }
    if (scrollY > 0 && scrollY + innerHeight >= document.documentElement.scrollHeight - 2) active = targets.at(-1)?.id;
    links.forEach(link => {
      if (link.dataset.outlineTarget === active) link.setAttribute('aria-current','location');
      else link.removeAttribute('aria-current');
      link.toggleAttribute('data-current-group', active?.startsWith('research-') && link.dataset.outlineTarget === 'featured');
    });
    if (outline.dataset.outlineContext === 'home') {
      const group = active?.startsWith('research-') || active === 'awards' ? 'featured'
        : ['education','skills'].includes(active) ? 'experience' : active === 'contact' ? 'cv' : active;
      primaryLinks.forEach(link => {
        if (link.dataset.navSection === group) link.setAttribute('aria-current','location');
        else link.removeAttribute('aria-current');
      });
    }
    const total = document.documentElement.scrollHeight - innerHeight;
    const value = total > 0 ? Math.round(Math.max(0, Math.min(100, scrollY / total * 100))) : 100;
    progress.value = value;
    percent.textContent = `${value}%`;
    siteHeader.classList.toggle('is-scrolled', scrollY > 8);
  }
  function scheduleUpdate() { if (!queued) { queued = true; requestAnimationFrame(updateCurrent); } }
  function updateOffset() {
    document.documentElement.style.setProperty('--site-header-height', `${siteHeader.offsetHeight}px`);
    document.documentElement.style.setProperty('--header-offset', `${siteHeader.offsetHeight + 24}px`);
    scheduleUpdate();
  }
  new ResizeObserver(updateOffset).observe(siteHeader);
  addEventListener('scroll',scheduleUpdate,{passive:true});
  addEventListener('hashchange',scheduleUpdate);
  addEventListener('load',scheduleUpdate);
  addEventListener('resize',scheduleUpdate);
  if (wide.matches && wantsPinned()) openContents();
  updateOffset();
}
