# 핵심 API 계약

JSON 입력·AI 출력은 스키마 검사. 오류는 code·fieldErrors·requestId로 반환하고 UI가 쉬운 영어/한국어로 표시한다.

| 영역 | 경로 |
|---|---|
| 인증 | POST /api/auth/code, POST /api/auth/verify, POST /api/auth/logout, GET /api/me |
| 일감 | GET /api/jobs, GET /api/jobs/:id, POST /api/jobs, PATCH /api/jobs/:id, POST /api/jobs/:id/publish, POST /api/jobs/:id/close |
| 농가 | GET /api/me/jobs, GET /api/jobs/:id/interests |
| 청년 | POST /api/jobs/:id/interests, GET /api/me/interests, POST /api/interests/:id/withdraw |
| AI | POST /api/draft, POST /api/transcribe |
| 상태 | GET /api/health |

목록은 published만 노출하고 지역 검색·페이지네이션만 제공한다. 소유자 초안과 관심 연락처는 목록 응답에 섞지 않는다. 미로그인/권한 없음/마감/입력 부족/중복·오래된 버전을 구별한다. 재시도에 신청이 중복되지 않게 유일 제약과 idempotency key를 사용한다.

익명 작성은 개인 브라우저에 연결된 임시 초안만 접근하며 로그인 시 안전하게 소유권을 이관한다. 인증·게시 실패에도 화면 입력을 보존한다. Meta 전사는 형식·길이·크기를 검사하고 성공/실패를 실제 결과로 표시한다.
