# AI 자막 수집기 다운로드 사이트

AI 자막 수집기(윈도우 프로그램) 설치파일을 받는 Streamlit 사이트입니다.

- 이 저장소의 **GitHub 최신 릴리스**에 올린 설치파일(.exe)을 자동으로 찾아 [다운로드] 버튼에 연결합니다.
  새 릴리스를 올리면 코드를 고치지 않아도 됩니다. (버전 정보는 약 10분마다 새로 가져옵니다.)
- **다운로드 목록**: 최신 버전에 올린 파일(설치파일, 사용 설명서 등)을 모두 보여주고 하나씩 받을 수 있습니다.
  예전 버전 파일은 [이전 버전 보기]를 누르면 나옵니다.
- 정보를 못 가져오면 릴리스 페이지 링크를 대신 보여줍니다.
- 저장소 주소는 `app.py` 맨 위의 `GITHUB_REPO` 한 곳에서 바꿉니다.

## 파일

| 파일 | 역할 |
|---|---|
| `app.py` | 사이트 화면 |
| `requirements.txt` | 필요한 라이브러리(버전 고정) |
| `.gitignore` | 올리지 않을 파일 목록 |
| `CLAUDE.md` | Claude 작업 규칙 |

## 내 컴퓨터에서 실행

```
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud에 올리기

1. https://share.streamlit.io 에 GitHub 계정으로 로그인
2. [Create app] → 이 저장소, 브랜치 `main`, 파일 `app.py` 선택 → [Deploy]

비밀번호·토큰은 필요 없습니다. 공개 저장소이므로 넣지 마세요.
