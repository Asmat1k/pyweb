import { runBenchmark } from './benchmark.js';

const root = document.querySelector('#benchmark-demo');
if (root) {
  const status = root.querySelector('[data-status]');
  const output = root.querySelector('[data-results]');
  const run = root.querySelector('[data-run]');
  const download = root.querySelector('[data-download]');
  let current;

  function table(caption, headers, rows) {
    const wrapper = document.createElement('div');
    wrapper.style.overflowX = 'auto';
    const table = document.createElement('table');
    table.createCaption().textContent = caption;
    const head = table.createTHead().insertRow();
    for (const label of headers) {
      const cell = document.createElement('th');
      cell.scope = 'col';
      cell.textContent = label;
      head.append(cell);
    }
    const body = table.createTBody();
    for (const values of rows) {
      const row = body.insertRow();
      for (const value of values) row.insertCell().textContent = String(value);
    }
    wrapper.append(table);
    return wrapper;
  }

  function render(result, source) {
    if (result.simulated !== true || !Array.isArray(result.connections) ||
        !Array.isArray(result.messages)) throw new Error('Invalid demo results');
    const connections = table('Подключение — случайные значения',
      ['Режим', 'Медиана, мс', 'p95, мс'],
      result.connections.map(r => [r.mode, r.medianMs, r.p95Ms]));
    const messages = table('Обмен сообщениями — случайные значения',
      ['Режим', 'Размер, байт', 'Потери сети, %', 'RTT медиана, мс', 'RTT p95, мс',
        'RTT p99, мс', 'Накладные расходы, %', 'До дедлайна, %'],
      result.messages.map(r => [r.mode, r.payloadBytes, r.lossPercent, r.medianMs,
        r.p95Ms, r.p99Ms, r.overheadPercent, r.deliveredBeforeDeadlinePercent]));
    output.replaceChildren(connections, messages);
    status.textContent = `Симуляция · ${source} · ${result.generatedAt} · дедлайн ${result.deadlineMs} мс`;
    current = result;
    download.disabled = false;
  }

  run.addEventListener('click', () => render(runBenchmark(), 'запуск в браузере'));
  download.addEventListener('click', () => {
    const url = URL.createObjectURL(new Blob([JSON.stringify(current, null, 2)],
      { type: 'application/json' }));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'simulated-results.json';
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });

  // A slow initial fetch must not overwrite a newer browser run.
  fetch(new URL('../demo-results.json', import.meta.url), { cache: 'no-store' })
    .then(response => {
      if (!response.ok) throw new Error('Results unavailable');
      return response.json();
    })
    .then(result => { if (!current) render(result, 'файл последнего CLI-запуска'); })
    .catch(() => {
      if (!current) status.textContent = 'Сохранённые данные недоступны. Нажмите «Запустить демо».';
    });
}
