# Ma-eul Ilgam

A bilingual prototype for turning a rural farmer's request into a reviewable local work opportunity. English is the default interface; 한국어 is available from the language switcher.

## What it does

A farmer enters a request, optionally recording audio or transcribing a supported WAV with Meta Voice. Meta Muse Spark can draft structured fields when a server-side API key is configured. The farmer reviews and edits the draft before approving it for a youth-facing review. A young person can enter skills and availability and inspect the details. This is an in-session prototype: it does not publish listings, connect people, screen applicants, or guarantee employment.

**Demo data is fictional.** Without a key, the app clearly labels a manual demo that copies the request into the task field and leaves the rest blank. It is not a simulated AI response and is not eligible evidence of Meta integration.

## Run locally

Requires Node.js 20 or newer.

```sh
npm install
npm run build
MODEL_API_KEY=your_key npm start
```

Open http://127.0.0.1:3001. For UI development use `npm run dev` and open the Vite URL. Never put your key in a repository, a browser variable, or client code. The server reads `MODEL_API_KEY` or `META_API_KEY` from the environment or a local `.env` file.

When enabled, the server sends user-provided text and uploaded audio to Meta. Use only material you have permission to share. The transcription endpoint accepts mono 16-bit PCM WAV at 16 kHz or 24 kHz; the app limits uploads to 12 MB. Unsupported audio fails rather than pretending it was transcribed.

## Meta products

- `muse-spark-1.3` through Meta Model API chat completions: extracts a draft with task, location, timing and compensation.
- `muse-voice-transcribe-1.0` through Meta Model API file transcription: transcribes a supported WAV upload.

Live Meta draft generation was tested with a fictional English request. Voice transcription was tested with synthesized speech; recognition quality and real Korean dialects remain unvalidated. The browser can record microphone audio and convert it to WAV, and users can provide follow-up details for Meta to update the draft. Microphone recording has not yet been verified in a browser with a real microphone. The youth screen does not automatically assess compatibility.

## Tests

`npm run build` runs TypeScript and builds the client. `npm test` runs the targeted manual-draft test. See `specs/features/opportunity-workflow/validation.md` for the actual verification record.

## Specification and hackathon scope

The constitution is in `specs/mission.md`, `specs/tech-stack.md`, and `specs/roadmap.md`. Each feature has a plan, requirements and validation document under `specs/features/`. See `submission/` for draft answers and a three-minute recording plan. All project-specific material in this repository was created during the hackathon; the repository uses third-party dependencies under their respective licenses.

The problem is based on rural youth out-migration and the challenge of discovering local opportunities. We have not validated outcomes with users or demonstrated that the prototype changes employment or population retention.

## Design credit

The interface redesign was guided by [Unslop](https://github.com/heydamir/unslop), created by Damir Sokolovsky ([@heydamir](https://x.com/heydamir)), licensed under CC BY 4.0.
