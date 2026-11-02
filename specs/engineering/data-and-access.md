# 데이터 모델·권한

## 저장 단위

| 엔터티 | 핵심 필드와 제약 |
|---|---|
| users | id, verified_email, locale, account_status, policy_version, timestamps |
| sessions / login_tokens | user_id, 해시된 토큰, 만료·사용·취소 시각; 원본 토큰 저장 금지 |
| participant_profiles | user_id, 표시명, 자기소개, 역량, 선호 지역; 선택 정보 최소 수집 |
| farms / farm_memberships | farm_id, 공개 이름·지역·소개, owner/member 권한, verification_state |
| verification_requests | farm_id, 증빙 참조, 요청·처리자·사유·시각; 운영자만 증빙 열람 |
| jobs | farm_id, 상태, current_revision, 정원, 모집 마감, version |
| job_revisions | 제목·업무·지역·일정·시간대·보수·지급일·준비물·교통; 게시 조건의 불변 버전 |
| applications | job_id, applicant_id, revision_id, 소개·가능 조건, 상태·시각; 활성 중복 금지 |
| offers | application_id, revision_id, expiry, reserved_slot, 상태; 만료 자리 해제 |
| engagements | 양측 계정, 확정 조건 snapshot, 작업·취소·완료 상태, version |
| change_requests | engagement_id, 제안 조건·양측 응답·시각 |
| time_confirmations | engagement_id, 시간·휴게·금액 산출 근거와 양측 확인 |
| payment_reports | engagement_id, payer_reported, recipient_confirmed, 이견·증빙; 송금 정보 아님 |
| conversations / messages | 일감/신청/작업 참조, 접근 가능한 두 당사자, 본문·시각·신고 상태 |
| notifications / outbox | 수신자·종류·대상·읽음·전송 상태·중복키·재시도 횟수 |
| reports / moderation_actions | 신고자·대상·사유·운영 처리·이의제기·상태 |
| ai_runs | 소유자·초안 참조·모델·상태·사용량·오류 코드; 원문 로그 최소화 |
| uploads | 소유자·저장 키·용도·크기·검사 상태·만료/삭제 시각 |
| audit_events | 행위자·행동·대상·전후 상태·request_id·시각; 비밀/민감 원문 제외 |

외래키와 유일 제약으로 소유관계·중복을 강제한다. `(status, region, start_at)` 등 실제 탐색 쿼리 기준 인덱스를 둔다. 목록은 cursor pagination을 사용한다. 운영자 권한·상태 변경과 조건 확인 기록은 추적 가능해야 한다.

## 권한 표

| 행동 | 방문자 | 참여자 | 농가 구성원 | 운영자 |
|---|---|---|---|---|
| 공개 일감 읽기 | 가능 | 가능 | 가능 | 가능 |
| 신청·철회 | 불가 | 본인만 | 자기 농가에는 불가 | 대리 신청 불가 |
| 초안/게시 관리 | 불가 | 불가 | 권한 있는 농가만 | 검토·정지 가능, 임의 작성 대행 금지 |
| 제안 | 불가 | 불가 | 해당 농가 담당자 | 강제 선정 불가 |
| 제안 수락·수령 확인 | 불가 | 해당 본인 | 상대방 대리 확인 불가 | 대리 확인 불가 |
| 대화 읽기/쓰기 | 불가 | 참여 대화만 | 참여 대화만 | 신고·지원 사유가 있을 때 기록하고 열람 |
| 비공개 증빙 | 불가 | 본인 제출분만 | 본인 제출분만 | 담당 권한 범위 |
| 계정/일감 정지 | 불가 | 불가 | 불가 | 사유·감사 기록 필수 |

한 계정에 농가·참여자 역할을 함께 허용할 수 있으나 API는 작업마다 소유권과 이해관계를 검사한다. URL의 ID만 바꾸어 다른 계정 데이터에 접근할 수 없어야 한다. 수정은 version 또는 ETag로 충돌을 검출하고, 신청·수락·정원은 트랜잭션과 잠금으로 일관성을 유지한다.
