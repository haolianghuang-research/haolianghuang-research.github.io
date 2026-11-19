// The same disclosure menu serves touch and keyboard users on small screens.
const siteHeader = document.querySelector('[data-site-navigation]');
if (siteHeader) {
  const toggle = siteHeader.querySelector('.nav-toggle');
  const links = [...siteHeader.querySelectorAll('[data-section]')];
  const mobile = window.matchMedia('(max-width: 640px)');
  siteHeader.dataset.navReady = '';
  toggle.hidden = false;

  function setMenu(open, restoreFocus = false) {
    siteHeader.toggleAttribute('data-menu-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.querySelector('.menu-label').textContent = open ? 'Close' : 'Menu';
    if (restoreFocus) toggle.focus();
  }
  toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') setMenu(false, true);
  });
  document.addEventListener('click', event => {
    if (!siteHeader.contains(event.target)) setMenu(false);
  });
  links.forEach(link => link.addEventListener('click', () => setMenu(false)));
  mobile.addEventListener('change', () => setMenu(false));

  const sections = links.map(link => document.getElementById(link.dataset.section)).filter(Boolean);
  let queued = false;
  function updateCurrent() {
    queued = false;
    if (!sections.length) return;
    const limit = siteHeader.getBoundingClientRect().height + 45;
    let active = sections[0].id;
    for (const section of sections) {
      if (section.getBoundingClientRect().top <= limit) active = section.id;
    }
    links.forEach(link => {
      if (link.dataset.section === active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
  function scheduleUpdate() {
    if (!queued) { queued = true; requestAnimationFrame(updateCurrent); }
  }
  function updateHeaderOffset() {
    document.documentElement.style.setProperty('--header-offset', `${siteHeader.offsetHeight + 24}px`);
    scheduleUpdate();
  }
  new ResizeObserver(updateHeaderOffset).observe(siteHeader);
  window.addEventListener('scroll', scheduleUpdate, {passive:true});
  window.addEventListener('hashchange', scheduleUpdate);
  window.addEventListener('load', scheduleUpdate);
  updateHeaderOffset();
}
