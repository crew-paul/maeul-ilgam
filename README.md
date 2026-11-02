# Village Jobs · 마을일감

Local work, a conversation away. English by default, with Korean throughout.

A farmer fills in a text form with all fields visible, then reviews the date, time and pay before posting. Voice input and Meta-assisted extraction are optional. Posting and viewing details do not require sign-in. A young person can discover the opportunity and share a phone number or email with that farmer. Arrangements and payment happen directly between people.

## Storage

**Application data is held only in the server process memory**, as requested. PGlite runs without a file path; no remote database or disk database is used. Accounts, anonymous posting owners, verification challenges, sessions, jobs and interests reset when the server restarts. An anonymous working draft is held in a server Map for up to one hour and survives refresh and sign-in while that server is running. Separate users share the same running server's published listings. A private browser cookie lets a farmer manage their anonymous posts; clearing it loses management access. Browser cookies hold opaque tokens; only the language preference is stored in localStorage.

`SEED_DEMO_DATA=1` creates 10 labeled fictional jobs when the server starts. The examples use future dates relative to startup, contain no personal contacts, and are marked Sample / 예시. Other records still reset on restart. Set the flag to `0` for an empty server.

Run one server instance for this hackathon. Multiple instances have independent memory. This configuration intentionally does not preserve real service records across restarts.

## Run

Requires Node.js 20 or newer.

```sh
npm ci
cp .env.example .env
# Add your Meta key to .env; never commit it.
npm run build
npm start
```

Open http://127.0.0.1:3001. For development use `npm run dev` and the Vite URL. The server loads `.env` and accepts `META_API_KEY` (or `MODEL_API_KEY`). Keys stay on the server.

`AUTH_MODE=development` is a **local test mode**: codes are displayed on screen, not sent. For real verification, set `AUTH_MODE=provider` and configure Resend email and/or Twilio Verify SMS credentials. Production rejects development authentication and requires an HTTPS `APP_ORIGIN`. Real message delivery and public deployment have not been verified with provider accounts.

## Seven screens

| Route | Purpose |
|---|---|
| `/` | Local opportunities and region search |
| `/jobs/:id` | Opportunity details and contact-sharing consent |
| `/sign-in` | Phone or email code verification |
| `/farmer/jobs` | Own jobs, shared contacts, close recruitment |
| `/farmer/jobs/new` | Text-first posting, all fields visible; optional voice |
| `/farmer/jobs/:id/edit` | Edit own opportunity |
| `/my/interests` | Own interests and withdrawal |

Anonymous posting and viewing work without authentication providers. Applying and sharing contact details still use the existing sign-in flow.

The server enforces ownership, required fields, future dates, version conflicts, contact privacy and duplicate-interest protection. Withdrawing hides the contact from subsequent farmer requests. There is no applicant screening, automated hiring decision, chat, payment processing or payment ledger.

## Meta and validation

- Muse Spark (`muse-spark-1.3`) through Meta Model API extracts structured work details and updates the answered field. Unknown details remain empty for review.
- Muse Voice Transcribe (`muse-voice-transcribe-1.0`) transcribes supported WAV audio. The browser converts recordings to mono 16-bit 24 kHz WAV. Audio is processed in memory and is not stored by the app.
- Failed model calls are shown as errors with a manual writing path. There is no fake AI response. Summary read-aloud uses the device's speech synthesis.

`npm run build` checks TypeScript and builds the UI. `node --test server/role-journeys.test.js` checks the independent creator/applicant journey and the ten demo records. `node --test server/app.test.js` runs the focused integration checks for memory storage, authentication, ownership, publishing, interests and withdrawal. See [verification status](specs/release/implementation-status.md) for what was actually observed, including remaining limitations.

## Specification and submission

[SDD v3](specs/README.md) is the current source of truth. Each feature has plan, requirements and validation documents. [Submission materials](submission/) include draft form answers and the demo script. The current MP4 is a locally generated draft, excluded from Git; it must match the final product before submission. No employment or population-retention outcome has been measured, and no older-adult user study has been completed.

## Design credit

Design guidance: [design-taste-frontend](https://github.com/Leonxlnx/taste-skill) and [Unslop](https://github.com/heydamir/unslop) by Damir Sokolovsky ([@heydamir](https://x.com/heydamir)), CC BY 4.0.
