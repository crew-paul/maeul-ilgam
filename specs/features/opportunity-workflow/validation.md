# Validation

- Run a production build and exercise server health and missing-key behavior.
- Verify English default, Korean switching, typed input, unknown fields, manual edit, approval and comparison.
- Verify audio refuses to claim success without a configured API; inspect the server path and perform a live test only when credentials exist.
- Check responsive views, keyboard focus and no horizontal overflow where a browser is available.
- Confirm sample labels, no invented user evidence, no API keys in source, and public repository access before submission.

## Run 2026-11-02

- Production build and TypeScript check passed; focused no-invention unit test passed.
- Browser exercised English sample input, manual draft, unknown fields and approval to the youth view.
- Meta transcription and generation remain unverified without an API key. Live deployment, Korean switch and mobile visual checks remain to be verified.
- Deviation: audio input is WAV upload, not microphone recording. Missing terms are shown as editable fields, not a multi-turn spoken interview. The youth view displays user-entered conditions without automated compatibility evaluation.
- Additional checks: Korean language switching preserved the active opportunity and inputs. Health and manual-draft HTTP routes returned expected no-key results. Taste skill source lint reports no failures and four warnings for app-section labels; those labels identify the current workflow and are retained. Full skill inspector could not be run under the installed Node 20 (it requires Node 22+); a desktop screenshot was visually reviewed, but mobile inspection remains open.
