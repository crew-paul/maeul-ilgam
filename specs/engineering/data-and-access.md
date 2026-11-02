# 최소 데이터와 권한

| 자원 | 필드·제약 |
|---|---|
| users | id, 인증된 전화/이메일, channel, created_at |
| sessions / auth_challenges | 토큰 해시·만료·일회성·재전송 제한 |
| jobs | id, owner_id, draft/published/closed, data JSON의 task, location, 날짜/시간·한국 시간대, 보수·단위·통화, 인원, version, timestamps |
| interests | id, job_id, user_id, name, memo, contact_type, contact_value, consent_at, active/withdrawn; 활성 중복 방지 |
| workingDrafts Map | 브라우저 비밀 토큰·내용·1시간 만료; 인증 후 작성 내용을 본인 일감으로 저장 |

방문자는 공개 일감만 읽는다. 로그인 사용자는 본인 관심을 만들고 철회한다. 농가는 자기 일감만 수정·마감하고 해당 일감의 활성 관심자 연락처만 읽는다. 자기 일감에 관심을 보내는 것은 막는다. 관리자 권한과 운영 화면은 이번 범위에 없다.

개인 연락처는 인증 정보와 연락 공유 정보로 구분한다. 관심에서 선택한 연락처만 농가에 공유하며 인증 전화/이메일을 자동 공개하지 않는다. 연락처를 AI로 평가하지 않는다. 서버 권한·필수 필드·상태·version·중복을 검사한다. 새로고침 후 저장된 데이터가 복구돼야 한다.

계정·세션·일감·관심은 파일 경로 없는 PGlite 메모리에, 작성 중 초안은 서버 Map에 저장한다. 새로고침에는 유지되지만 서버 재시작 시 모두 초기화된다. 브라우저에는 불투명 토큰 쿠키만 저장하며 localStorage는 언어 설정에만 사용한다.
