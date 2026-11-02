# API 계약 v2

기준 경로 `/api/v1`. JSON 요청·응답은 공통 스키마로 검증한다. 인증과 소유권은 모든 보호 경로에서 서버가 검사한다. 오류는 `{error:{code,fieldErrors?,requestId}}`; UI가 번역한다. 성공 응답은 자원과 `version`, 목록은 `items,nextCursor`를 반환한다.

## 경로

| 영역 | 명령·조회 |
|---|---|
| 인증 | `POST /auth/email-link`, `POST /auth/verify`, `POST /auth/logout`, `GET /me`, `DELETE /me/sessions/:id` |
| 프로필 | `GET/PATCH /me/profile`, `POST /farms`, `GET/PATCH /farms/:id`, `POST /farms/:id/verification` |
| 일감 | `GET /jobs`, `GET /jobs/:id`, `POST /jobs`, `PATCH /jobs/:id`, `POST /jobs/:id/submit-review`, `POST /jobs/:id/close` |
| 작업함 | `GET /me/farms/:id/jobs`, `GET /me/applications`, `GET /me/engagements` |
| 신청·제안 | `POST /jobs/:id/applications`, `POST /applications/:id/withdraw`, `GET /jobs/:id/applications`, `POST /applications/:id/offers`, `POST /offers/:id/accept`, `POST /offers/:id/decline` |
| 작업 | `GET /engagements/:id`, `POST /engagements/:id/start`, `POST /engagements/:id/completion-request`, `POST /engagements/:id/completion-confirm`, `POST /engagements/:id/cancel-request`, `POST /engagements/:id/cancel-response` |
| 변경·지급 | `POST /engagements/:id/changes`, `POST /changes/:id/respond`, `POST /engagements/:id/payment-report`, `POST /engagements/:id/payment-receipt`, `POST /engagements/:id/dispute` |
| 대화·알림 | `POST /jobs/:id/inquiries`, `GET /conversations`, `GET/POST /conversations/:id/messages`, `GET /notifications`, `POST /notifications/:id/read` |
| AI | `POST /drafts/:id/ai-runs`, `GET /ai-runs/:id`, `POST /transcriptions`, `DELETE /transcriptions/:id` |
| 업로드 | `POST /uploads`, `DELETE /uploads/:id`; 용도·소유권·허용 형식 검사 |
| 운영 | `GET /admin/review-queue`, `POST /admin/farms/:id/decision`, `POST /admin/jobs/:id/decision`, `GET /admin/reports`, `POST /admin/reports/:id/action` |
| 상태 | `GET /health/live`, `GET /health/ready` |

## 변경 명령 규칙

- 생성·신청·수락·확인 명령은 `Idempotency-Key`를 받아 같은 요청의 중복 효과를 막는다.
- 초안 수정은 현재 `version`을 요구한다. 오래된 버전은 409와 최신 버전 정보를 반환하고 입력 복구를 돕는다.
- 게시 검사는 누락 필드 목록을 반환한다. 클라이언트 통과만으로 게시하지 않는다.
- 신청·제안·수락의 상태/정원 변경과 outbox 기록은 같은 트랜잭션으로 커밋한다.
- 메시지 본문은 길이·빈 값·링크·업로드 접근 권한을 검사하고 사용자 HTML을 실행하지 않는다.
- `GET /jobs`는 지역·업무·시작 기간·보수 단위별 필터와 정렬을 허용한다. 보수 단위가 다른 일감을 허위 환산해 비교하지 않는다.
- 상태를 벗어난 요청은 409, 인증 없음 401, 권한 없음 403, 비공개 자원 탐색은 404, 입력 실패 422, 과도 요청 429로 처리한다.

## AI 비동기 처리

작성 중인 자원의 소유자만 실행/조회한다. 긴 음성·모델 호출은 실행 ID와 상태를 반환하며 대기/진행/성공/실패/취소를 구분한다. 실패 시 초안을 덮어쓰지 않는다. 기존 `/api/draft`, `/api/transcribe`는 시제품 경로이며 도메인 저장·권한을 갖춘 새 경로로 이관한다.
