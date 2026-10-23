# CLAUDE.md — 작업 규칙

## 프로젝트
- AI 자막 수집기 팀원 배포 저장소. 팀원은 이 저장소의 첫 화면(`README.md`)과 GitHub Release에서 프로그램을 받는다.
- 프로그램(zip)과 사용법 PPT는 소스 저장소(subtitle-collector)의 GitHub Actions가 이 저장소의 Release에 **고정 이름**(`AI-Subtitle-Portable.zip`, `AI-Subtitle-Guide.pptx`)으로 올린다. README의 받기 링크는 `releases/latest/download/<고정 이름>`이라 늘 최신판을 가리킨다.
- v3.1까지 쓰던 Streamlit 사이트(`app.py`)는 v3.2에서 없앴다(2026-10-23 사용자 결정).

## 공개 저장소
- 이 저장소는 공개(Public)다. 비밀번호·토큰·API 키 등 비밀 정보는 코드·문서·커밋 어디에도 넣지 않는다.
- OCR 포함 판(내 전용)은 이 저장소에 올리지 않는다.

## 사용자
- 사용자는 개발자가 아니다. 쉬운 말로 설명하고, 해야 할 일은 단계별로 안내한다.

## 보고
- 직접 확인하지 못한 것은 확인하지 못했다고 분명히 말한다.
