> 이전 시제품 기록. 현재 출시 구현 기준은 [SDD v2](../../README.md)를 따른다. 이 문서의 기존 범위·검증은 당시 시제품에만 적용된다.

# Record and clarify requirements

- Users can record audio in the browser and send mono PCM WAV to Meta Voice, with an explicit permission request and stop control.
- English and Korean interface and voice language hints remain available; transcription must remain editable.
- After extracting an initial draft, a user can provide more details and ask Meta to update it. Existing values are included and user-approved fields remain editable; unknowns remain blank.
- Keep the server key secret, handle microphone/API failures, and do not claim that work is published or matched.
- Document live AI use accurately and preserve the manual demo when no key is configured.
