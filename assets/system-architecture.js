// Focus the explanatory diagram; this does not run the robot system.
document.querySelectorAll('.system-architecture').forEach((diagram) => {
  const controls = diagram.querySelector('.architecture-controls');
  const buttons = [...diagram.querySelectorAll('[data-architecture-view]')];
  const panels = [...diagram.querySelectorAll('[data-architecture-panel]')];
  const selectView = (view) => {
    diagram.dataset.architectureFocus = view;
    buttons.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.architectureView === view)));
    panels.forEach((panel) => { panel.hidden = panel.dataset.architecturePanel !== view; });
  };
  buttons.forEach((button) => button.addEventListener('click', () => selectView(button.dataset.architectureView)));
  controls.hidden = false;
});
