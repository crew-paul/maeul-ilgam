# Video revision — Meta credit budget only

**Latest review cut:** `village-jobs-product-silent-en.mp4` — silent, English captions, actual product footage only. **The requested Korean farmer/youth story scenes are still missing. This is not the completed story film or a submission-ready final.**

The revised cut removes narration and the unrelated Western stock footage. A fictional strawberry-product photography task connects the caption setup to the actual app recording. No audio track, external video service, paid stock, or new model call is used to make this cut.

Budget is limited to the remaining portion of the originally granted **$150 Meta Model API credits**. No additional payment, top-up, vidIQ credits, or paid third-party generation is authorized. The remaining Meta balance was not verified. The account model list inspected during production had no video-generation model.

- `village-jobs-product-silent-en.mp4` — latest product-only review cut.
- `village-jobs-product-silent.en.srt` — English subtitles for this cut.
- `source/korean-story/` — silent renderer, storyboard, timeline and verification.
- `village-jobs-recording-originals.zip` — unedited native browser recordings.

Rebuild with FFmpeg with libass (no API call):

```sh
python3 submission/video/source/korean-story/render.py --raw-dir /path/to/captured-media --ffmpeg /path/to/ffmpeg
```

The directory needs the five take MP4s listed in the storyboard. Rendered media remain local and ignored by Git. Public upload and hackathon submission are pending.

## Previous revision, retained for reference

# Recorded demo — Korean narration, English captions

**Current movie:** `village-jobs-demo-ko-en.mp4` · **2 minutes 31 seconds** · 1920×1080 H.264/AAC.

The UI footage is edited from continuous native browser MP4 recordings of the working app. It is not assembled from screenshots. Two short opening clips provide a clearly labeled fictional illustration of the farmer/young-person problem.

Files available locally:

- `village-jobs-demo-ko-en.mp4` — complete Korean-narrated movie with readable English captions.
- `village-jobs-demo.en.srt` — separate English subtitle file.
- `village-jobs-recording-originals.zip` — five unedited app recordings, timestamp markers and provenance.
- `source/` — storyboard, narration, edit timeline, render script and verification record.
- [Credits and source information](CREDITS.md).

The movie shows text entry, a real Meta Muse Spark response, human correction and review, posting without sign-in, independent applicant discovery, local test verification, consent, application, farmer contact visibility, withdrawal and honest MVP limits. It explicitly distinguishes test authentication, fictional data and memory-only storage from real-world validation.

The old `maeul-ilgam-demo.mp4` is the superseded slideshow first cut. Use the new `village-jobs-demo-ko-en.mp4` for review.

MP4s and the raw archive stay local rather than being committed to Git. Upload the reviewed final movie to a judge-accessible location before submitting. That upload and public link are still pending.

Rebuild with macOS `say` (Yuna) and FFmpeg with libass:

```sh
python3 submission/video/source/render.py --raw-dir /path/to/captured-media --ffmpeg /path/to/ffmpeg
```

The raw directory needs the five take MP4s plus the two credited stock video files. `--only 09-auth` re-renders one scene and rebuilds the master without re-encoding unchanged scenes.
