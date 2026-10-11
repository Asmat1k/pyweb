// Synthetic values only: no sockets, QUIC sessions or network measurements.
export const modes = ['WebSocket', 'WT streams', 'WT datagrams'];
export const payloads = [64, 256, 1024];
export const losses = [0, 1, 5];

function random(min, max) {
  return Number((min + Math.random() * (max - min)).toFixed(2));
}

export function connectStub() {
  const medianMs = random(5, 60);
  return { medianMs, p95Ms: Number((medianMs + random(1, 30)).toFixed(2)) };
}

export function messageStub() {
  const medianMs = random(5, 80);
  const p95Ms = Number((medianMs + random(1, 40)).toFixed(2));
  return { medianMs, p95Ms, p99Ms: Number((p95Ms + random(1, 30)).toFixed(2)) };
}

export function overheadStub() {
  return random(2, 40);
}

export function deliveryStub() {
  return random(70, 100);
}

export function runBenchmark() {
  return {
    simulated: true,
    generatedAt: new Date().toISOString(),
    deadlineMs: 100,
    connections: modes.map(mode => ({ mode, ...connectStub() })),
    messages: modes.flatMap(mode => payloads.flatMap(payloadBytes =>
      losses.map(lossPercent => ({
        mode, payloadBytes, lossPercent,
        ...messageStub(), overheadPercent: overheadStub(),
        deliveredBeforeDeadlinePercent: deliveryStub(),
      }))
    )),
  };
}
