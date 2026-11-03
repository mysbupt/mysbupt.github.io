(() => {
  const root = document.documentElement;
  const toggle = document.querySelector('.theme-toggle');
  let saved;
  try { saved = localStorage.getItem('theme'); } catch (_) {}
  const system = matchMedia('(prefers-color-scheme: dark)');
  function setTheme(theme) {
    root.dataset.theme = theme;
    toggle.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`);
    toggle.setAttribute('aria-pressed', String(theme === 'dark'));
  }
  setTheme(saved || (system.matches ? 'dark' : 'light'));
  toggle.addEventListener('click', () => {
    saved = root.dataset.theme === 'dark' ? 'light' : 'dark';
    setTheme(saved);
    try { localStorage.setItem('theme', saved); } catch (_) {}
  });
  system.addEventListener('change', () => { if (!saved) setTheme(system.matches ? 'dark' : 'light'); });
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav');
  function closeMenu() { nav.classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); }
  menu.addEventListener('click', () => {
    const expanded = nav.classList.toggle('open');
    menu.setAttribute('aria-expanded', String(expanded));
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
  document.querySelector('[data-print]')?.addEventListener('click', () => window.print());
  const search = document.querySelector('#publication-search');
  if (!search) return;
  const year = document.querySelector('#publication-year');
  const domain = document.querySelector('#publication-domain');
  const params = new URLSearchParams(location.search);
  search.value = params.get('q') || '';
  if ([...domain.options].some(option => option.value === params.get('domain'))) domain.value = params.get('domain');
  const publications = [...document.querySelectorAll('.pub[data-search]')];
  function filter() {
    const query = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let count = 0;
    publications.forEach(pub => {
      const matches = (!year.value || pub.dataset.year === year.value) && (!domain.value || pub.dataset.domains.split('|').includes(domain.value)) && query.every(term => pub.dataset.search.includes(term));
      pub.hidden = !matches;
      if (matches) count++;
    });
    document.querySelectorAll('.publication-group').forEach(group => {
      group.hidden = ![...group.querySelectorAll('.pub')].some(pub => !pub.hidden);
    });
    document.querySelector('#result-count').textContent = `${count} publication${count === 1 ? '' : 's'}`;
    document.querySelector('#empty-results').hidden = count > 0;
  }
  search.addEventListener('input', filter);
  year.addEventListener('change', filter);
  domain.addEventListener('change', filter);
  filter();
})();
