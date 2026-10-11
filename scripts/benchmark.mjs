import { writeFile } from 'node:fs/promises';
import { runBenchmark } from '../docs/assets/javascripts/benchmark.js';

const result = runBenchmark();
const output = new URL('../docs/assets/demo-results.json', import.meta.url);
await writeFile(output, JSON.stringify(result, null, 2) + '\n');
console.log('SIMULATED DATA — not network measurements.');
console.table(result.connections);
console.table(result.messages);
console.log(`Saved ${output.pathname}. Open the landing page with npm start.`);
