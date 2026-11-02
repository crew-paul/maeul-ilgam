> 이전 시제품 기록. 현재 출시 구현 기준은 [SDD v2](../../README.md)를 따른다. 이 문서의 기존 범위·검증은 당시 시제품에만 적용된다.

# Validation

Run build and focused audio/draft tests. Exercise follow-up with English and Korean data and confirm missing fields remain missing. Verify recording permission handling and actual Meta Voice behavior where environment permits.

## 2026-11-02

- Production build and TypeScript check passed; existing focused test passed.
- With live Meta API, fictional English additional details populated location, time and pay without modifying the task; browser exercised the same update and approved card.
- Browser microphone permission and recording have not been exercised; real Korean/dialect speech and a live Korean follow-up remain untested.
- A separate live Korean Muse Spark request returned the expected task, location, time and pay. This was a text test, not a dialect or microphone test.
