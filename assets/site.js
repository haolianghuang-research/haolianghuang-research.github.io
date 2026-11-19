const filters = document.querySelector('.filters');
const projects = [...document.querySelectorAll('.project')];
const count = document.querySelector('#project-count');

if (filters && projects.length) {
  filters.hidden = false;
  filters.addEventListener('click', event => {
    const button = event.target.closest('button[data-filter]');
    if (!button) return;
    const category = button.dataset.filter;
    let visible = 0;
    projects.forEach(project => {
      project.hidden = category !== 'all' && project.dataset.category !== category;
      if (!project.hidden) visible += 1;
    });
    filters.querySelectorAll('button').forEach(item => {
      item.setAttribute('aria-pressed', String(item === button));
    });
    count.textContent = `${visible} ${visible === 1 ? 'project' : 'projects'}`;
  });
}

// Keep both approved portraits available without automatically rotating them.
const portraitPicker = document.querySelector('.portrait-picker');
const profilePhoto = document.querySelector('#profile-photo');
if (portraitPicker && profilePhoto) {
  portraitPicker.hidden = false;
  portraitPicker.addEventListener('click', event => {
    const button = event.target.closest('button[data-portrait-src]');
    if (!button) return;
    profilePhoto.src = button.dataset.portraitSrc;
    profilePhoto.alt = button.dataset.portraitAlt;
    portraitPicker.querySelectorAll('button').forEach(item => {
      item.setAttribute('aria-pressed', String(item === button));
    });
  });
}
