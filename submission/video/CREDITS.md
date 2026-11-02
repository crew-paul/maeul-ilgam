# Video sources and production

Final movie: `village-jobs-demo-ko-en.mp4` (2:31, 1920×1080).

## Actual product video

Five native browser MP4 recordings captured through CUA using Chrome's `Page.startScreenRecording` API. These are continuous video streams of real interactions, not an image-sequence reconstruction. The local raw archive contains the unedited files and timing markers; hashes are in `source/capture-provenance.json`.

Only waits and pacing were edited. The filmed Meta Muse Spark request returned the structured fields shown. Local authentication uses an on-screen test code and does not send email. The creator and applicant use separate hosts/cookies. All names, work requests and contact data are fictional. No employment or population outcome is claimed.

## Illustrative opening footage

- **Kampus Production** — [Man Harvesting Vegetables / senior couple in a garden](https://www.pexels.com/video/man-harvesting-vegetables-7655564/).
- **Tima Miroshnichenko** — [Frustrated Teenager / person working at a desk](https://www.pexels.com/video/frustrated-teenager-4873113/).
- Footage source terms: [Pexels License](https://www.pexels.com/license/).

These scenes are labeled illustrative stock footage and a fictional scenario. The people shown are not users, interviewees, beneficiaries or endorsers of Village Jobs. Their location and circumstances are not asserted to match the project.

## Narration, captions and editing

- Korean synthetic narration: macOS **Yuna**, 165 words per minute. The authoritative narration text is `source/narration-ko.txt`.
- English captions: 27 timed cues; burned into the movie and provided as `village-jobs-demo.en.srt`.
- FFmpeg renders the native video cuts, caption band and titles; the app itself is not simulated or regenerated.
- The final file has been decoded end to end and key visual frames inspected. The automated Korean speech-transcription check is a language/content check, not a claim of human listening review. See `source/verification.json`.

No public video upload or organizer submission was performed in this task.
