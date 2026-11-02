import express from 'express';
import multer from 'multer';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { extractDraft } from './logic.js';

const app = express();
const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 12 * 1024 * 1024 } });
app.use(express.json({ limit: '32kb' }));
const apiKey = () => process.env.MODEL_API_KEY || '';
app.get('/api/health', (_req, res) => res.json({ configured: !!apiKey() }));
app.post('/api/draft', async (req, res) => {
  const text = typeof req.body?.text === 'string' ? req.body.text.trim() : '';
  if (!text || text.length > 4000) return res.status(400).json({ error: 'Request must be between 1 and 4000 characters.' });
  if (!apiKey()) return res.json({ mode: 'demo', draft: extractDraft(text) });
  try {
    const response = await fetch('https://api.meta.ai/v1/chat/completions', { method: 'POST', headers: { Authorization: `Bearer ${apiKey()}`, 'Content-Type': 'application/json' }, body: JSON.stringify({ model: 'muse-spark-1.3', messages: [{ role: 'system', content: 'Extract a rural work request. Return only JSON with string fields task, location, timing, compensation. Use only information explicitly in the user message, preserve its language, and use an empty string for any unspecified field. Do not invent pay or dates. No markdown.' }, { role: 'user', content: text }], max_tokens: 500 }) });
    if (!response.ok) throw new Error(`Meta API returned ${response.status}`);
    const data = await response.json();
    const raw = data.choices?.[0]?.message?.content || '';
    const json = JSON.parse(raw.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/, ''));
    const draft = Object.fromEntries(['task','location','timing','compensation'].map(k => [k, typeof json[k] === 'string' ? json[k].slice(0, 500) : '']));
    return res.json({ mode: 'meta', draft });
  } catch (error) { return res.status(502).json({ error: 'Meta could not create a draft. Your request is still available to edit.' }); }
});
app.post('/api/transcribe', upload.single('audio'), async (req, res) => {
  if (!apiKey()) return res.status(503).json({ error: 'Meta API key is not configured. Use text input instead.' });
  if (!req.file || req.file.buffer.toString('ascii',0,4) !== 'RIFF' || req.file.buffer.toString('ascii',8,12) !== 'WAVE') return res.status(400).json({ error: 'Upload a mono 16-bit PCM WAV at 16 kHz or 24 kHz.' });
  try {
    const form = new FormData();
    form.append('request', new Blob([JSON.stringify({ mode: 'PUSH_TO_TALK', model: 'muse-voice-transcribe-1.0', audioEncoding: 'WAV' })], { type: 'application/json' }));
    form.append('audio', new Blob([req.file.buffer], { type: 'audio/wav' }), 'recording.wav');
    const response = await fetch('https://api.meta.ai/v1/asr/transcribe', { method: 'POST', headers: { Authorization: `Bearer ${apiKey()}` }, body: form });
    if (!response.ok) throw new Error('transcription failed');
    const data = await response.json();
    if (typeof data.transcript !== 'string') throw new Error('no transcript');
    res.json({ transcript: data.transcript });
  } catch { res.status(502).json({ error: 'Transcription failed. Please check the WAV format or use text input.' }); }
});
app.use(express.static(path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../dist')));
app.get('*', (_req, res) => res.sendFile(path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../dist/index.html')));
app.listen(process.env.PORT || 3001, '127.0.0.1', () => console.log(`Ma-eul Ilgam running on port ${process.env.PORT || 3001}`));
