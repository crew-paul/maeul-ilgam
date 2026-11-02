# Current film: Korean photo story + actual product video

**Use `village-jobs-photo-story-fast-en.mp4`**: approximately 1:52, 1920×1080 H.264, silent with continuous English captions.

The opening 32.4 seconds tell a fictional Korean farmer/youth story through eight Meta Muse Image photos, eased camera moves and seven dissolves. The farmer has strawberries to sell but needs product photos. A young adult relaxing on a rural porch discovers a nearby paid task, meets the farmer, and helps photograph the produce. The opening is visibly labeled AI-generated photos / fictional scenario.

The app demo was tightened from 137 to 80 seconds by cutting waits, accelerating interactions, and shortening captions. The original 32.4-second photo intro is unchanged. This pacing revision made no new generation/API calls.

The remaining 80 seconds are edited from the five continuous native browser MP4 recordings of the actual app. This section shows text entry, real Meta extraction, human correction, publishing, discovery, test verification, consent, contact sharing, withdrawal and current MVP limits. It is not a screenshot reconstruction. There is no narration, dialogue, music or audio track. English captions cover the entire film without timing gaps.

Local deliverables:

- `village-jobs-photo-story-fast-en.mp4` — current film.
- `village-jobs-photo-story-fast.en.srt` — 30 English subtitle cues, also burned into the film.
- `village-jobs-photo-story-fast-originals.zip` — eight original photos, five raw app recordings and production sources.
- `raw/photo-story/` — original generated photos and generation ledger.
- `source/photo-story/` — exact photo prompts, storyboards, renderer and verification.
- [Credits](CREDITS.md).

Only Meta generated new AI assets. Eight successful outputs at the published $0.01/image price imply $0.08 estimated generation cost, within the original $150 Meta credit authorization. Two initial requests failed HTTP 400 size validation; this is not a verified account billing statement. No paid external service, separate credits, purchase or top-up was used.

Re-render locally without another API call:

```sh
python3 submission/video/source/photo-story/render.py --raw-dir /path/to/five-browser-takes --ffmpeg /path/to/ffmpeg
python3 submission/video/source/photo-story/verify.py --ffmpeg /path/to/ffmpeg
```

The five browser take files are named in `source/photo-story/storyboard.json`; generated photos must be in `raw/photo-story/`. `generate.mjs` is for reproducing missing images through Meta with a locally configured API key; it skips existing files and does not retry automatically. Its exact prompts are in `photos.json` plus the shared character/style prompt in the script.

Previous movies are retained locally for reference and are superseded. Media remain ignored by Git. Public upload and hackathon submission have not been performed.
