// Open optional implementation notes when navigating to their anchor.
function revealAnchor() {
  const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
  if (target?.tagName === 'DETAILS') target.open = true;
}
window.addEventListener('hashchange', revealAnchor);
revealAnchor();
