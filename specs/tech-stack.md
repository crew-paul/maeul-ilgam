# Technical constitution

- TypeScript, React, Vite, and a small Node HTTP server.
- Meta Model API calls occur only on the server. API keys never enter source code or the browser. Audio transcription uses the official file endpoint, and structured analysis uses Muse Spark via a compatible chat endpoint.
- No remote database or accounts in the hackathon MVP. Sample data is explicitly labeled. User-entered state is session-only.
- A no-key demo fallback is deterministic, clearly labeled as simulated, and never represented as Meta output. Real mode is available only when configured.
- English is default; Korean is selectable. Interface strings live in a translation dictionary.
- Accessible forms, explicit status messages, keyboard access and responsive layout are required.
- Validate the production build, API error paths, and the core workflow. Never publish credentials, real personal information or unlicensed assets.
