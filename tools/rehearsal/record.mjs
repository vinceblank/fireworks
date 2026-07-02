#!/usr/bin/env node
/* Headless rehearsal recorder — runs the show in rehearsal.html and captures
   frames an AI (or human) can review without a browser session.

   Usage:
     node tools/rehearsal/record.mjs shows/2026-july-4/cobra.csv \
         [shows/2026-july-4/effects.json] [--out DIR] [--interval 20]

   Captures a screenshot ~1.2 s after every cue fires (mid-burst) plus a
   wide-interval sweep, and writes index.json mapping each frame to its
   show-clock time and the cues in the air. Review by reading the PNGs in
   order: look for dead air (empty sky between cues), texture clustering,
   and whether the finale visibly out-scales the rest.

   First-time setup:  cd tools/rehearsal && npm install && npx playwright install chromium
*/

import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const argv = process.argv.slice(2);
const flags = {};
const files = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === "--out") flags.out = argv[++i];
  else if (argv[i] === "--interval") flags.interval = +argv[++i];
  else files.push(argv[i]);
}
const [csvPath, effectsPath] = files;
if (!csvPath) {
  console.error("usage: node record.mjs <script.csv> [effects.json] [--out DIR] [--interval SECONDS]");
  process.exit(1);
}
const outDir = flags.out || path.join(path.dirname(csvPath), "rehearsal-captures");
const interval = flags.interval || 20;
fs.mkdirSync(outDir, { recursive: true });

const htmlPath = path.join(path.dirname(fileURLToPath(import.meta.url)), "rehearsal.html");
const csvText = fs.readFileSync(csvPath, "utf8");
const effectsText = effectsPath ? fs.readFileSync(effectsPath, "utf8") : null;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
await page.goto(pathToFileURL(htmlPath).href);
await page.evaluate(t => window.rehearsal.loadScript(t), csvText);
if (effectsText) await page.evaluate(t => window.rehearsal.loadEffects(t), effectsText);

const events = await page.evaluate(() => window.rehearsal.getEvents());
const duration = (await page.evaluate(() => window.rehearsal.getState())).duration;
console.log(`${events.length} events, ~${Math.round(duration)}s show — capturing to ${outDir}`);

// Capture plan: every event +1.2 s (mid-burst), plus a sweep every `interval` s.
const shots = new Map(); // time -> label
for (const ev of events) {
  const t = +(ev.t + 1.2).toFixed(1);
  shots.set(t, `${ev.clock.replace(":", "m")} ch${ev.ch} c${ev.cue} ${ev.desc}`);
}
for (let t = interval; t < duration; t += interval) {
  const k = +t.toFixed(1);
  if (![...shots.keys()].some(s => Math.abs(s - k) < 3)) shots.set(k, "sweep");
}
const plan = [...shots.entries()].sort((a, b) => a[0] - b[0]);

const index = [];
let i = 0;
for (const [t, label] of plan) {
  await page.evaluate(t => window.rehearsal.stepTo(t), t);
  const st = await page.evaluate(() => window.rehearsal.getState());
  const slug = label.slice(0, 60).replace(/[^\w.-]+/g, "_");
  const file = `${String(i++).padStart(3, "0")}_${slug}.png`;
  await page.screenshot({ path: path.join(outDir, file) });
  index.push({ file, t, clock: fmt(t), label, particlesInAir: st.particles });
  process.stdout.write(`\r${i}/${plan.length} frames`);
}
console.log();

fs.writeFileSync(path.join(outDir, "index.json"),
  JSON.stringify({ script: path.basename(csvPath), capturedAt: new Date().toISOString(),
                   duration, events, frames: index }, null, 2));
await browser.close();
console.log(`done: ${index.length} frames + index.json in ${outDir}`);

// Quick dead-air heuristic from particle counts on sweep frames:
const dead = index.filter(f => f.label === "sweep" && f.particlesInAir === 0);
if (dead.length) {
  console.log("possible dead air (empty sky) at: " + dead.map(f => f.clock).join(", "));
}

function fmt(t) {
  const m = Math.floor(t / 60), s = Math.floor(t % 60);
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}
