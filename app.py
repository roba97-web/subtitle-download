"""AI 자막 수집기 — 설치파일 다운로드 사이트 (Streamlit)

GitHub 최신 릴리스(releases/latest)에서 설치파일(.exe) 주소를 가져와 보여준다.
새 릴리스를 올리면 코드를 고치지 않아도 자동으로 최신 파일로 바뀐다.
"""

from datetime import datetime, timedelta, timezone

import requests
import streamlit as st

# ── 설정 ─────────────────────────────────────────────
# 설치파일이 올라가는 GitHub 저장소 (소유자/이름). 저장소가 바뀌면 여기만 고친다.
GITHUB_REPO = "roba97-web/subtitle-download"
# ─────────────────────────────────────────────────────

API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
RELEASES_PAGE = f"https://github.com/{GITHUB_REPO}/releases/latest"
KST = timezone(timedelta(hours=9))

st.set_page_config(page_title="AI 자막 수집기 다운로드", page_icon="💬", layout="centered")


@st.cache_data(ttl=600, show_spinner=False)
def fetch_latest_release():
    """최신 릴리스의 버전·날짜·설치파일 주소. 실패하면 예외(실패는 캐시되지 않음)."""
    resp = requests.get(
        API_URL,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "subtitle-download-site"},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    exe = next(
        (a for a in data.get("assets", [])
         if a["name"].lower().endswith(".exe") and "ocr" not in a["name"].lower()),
        None,
    )
    if exe is None:
        raise LookupError("릴리스에 설치파일(.exe)이 없습니다")
    published = datetime.fromisoformat(data["published_at"].replace("Z", "+00:00")).astimezone(KST)
    return {
        "version": data.get("tag_name", ""),
        "date": f"{published.year}년 {published.month}월 {published.day}일",
        "url": exe["browser_download_url"],
        "size_mb": exe.get("size", 0) / 1024 / 1024,
    }


st.markdown(
    """
<style>
:root { --navy: #1f3a68; --navy-line: #4a6fa5; }
.block-container { max-width: 720px; padding-top: 4.5rem; padding-left: 1rem; padding-right: 1rem; }
.hero { border-left: 6px solid var(--navy-line); padding: 0.2rem 0 0.2rem 1rem; margin-bottom: 1.2rem; }
.hero h1 { font-size: clamp(1.7rem, 6vw, 2.3rem); margin: 0 0 0.4rem 0; padding: 0; }
.hero p { margin: 0; opacity: 0.85; line-height: 1.6; word-break: keep-all; }
.ver { display: inline-block; margin: 0.2rem 0 1rem 0; padding: 0.3rem 0.8rem; border-radius: 999px;
       border: 1px solid var(--navy-line); background: rgba(74, 111, 165, 0.12); font-size: 0.95rem; }
div[data-testid="stLinkButton"] a {
    background: var(--navy) !important; color: #fff !important; border: 2px solid var(--navy-line) !important;
    font-size: 1.25rem !important; font-weight: 700 !important; padding: 0.9rem 1rem !important; border-radius: 12px !important;
}
div[data-testid="stLinkButton"] a:hover { background: #2a4d87 !important; }
div[data-testid="stLinkButton"] a p { font-size: 1.25rem !important; color: #fff !important; }
.small { font-size: 0.85rem; opacity: 0.7; margin-top: 0.4rem; }
.steps { list-style: none; padding: 0 !important; margin: 0.4rem 0 1rem 0 !important; }
.steps li { margin-left: 0 !important; padding-left: 0 !important; display: flex; gap: 0.75rem; align-items: flex-start; margin-bottom: 0.7rem; line-height: 1.6; word-break: keep-all; }
.steps .n { flex: 0 0 1.8rem; height: 1.8rem; border-radius: 50%; background: var(--navy); border: 1px solid var(--navy-line);
            color: #fff; font-weight: 700; display: flex; align-items: center; justify-content: center; font-size: 0.95rem; }
.note { border: 1px solid rgba(74, 111, 165, 0.45); background: rgba(74, 111, 165, 0.08);
        border-radius: 10px; padding: 0.8rem 1rem; line-height: 1.7; word-break: keep-all; }
.note p { margin: 0.15rem 0; }
.law { font-size: 0.85rem; opacity: 0.7; margin-top: 1.5rem; word-break: keep-all; }
</style>
<div class="hero">
  <h1>AI 자막 수집기</h1>
  <p>국회 인터넷의사중계·유튜브 등 영상 화면에 나오는 자막을 모아
     txt 파일로 저장하거나 복사해 주는 윈도우 프로그램입니다.</p>
</div>
""",
    unsafe_allow_html=True,
)

try:
    release = fetch_latest_release()
except Exception:
    release = None

if release:
    st.markdown(
        f'<span class="ver">최신 버전 <b>{release["version"]}</b> · {release["date"]} 올라옴</span>',
        unsafe_allow_html=True,
    )
    st.link_button("⬇  다운로드", release["url"], type="primary", width="stretch")
    st.markdown(
        f'<p class="small">윈도우용 설치파일 · 약 {release["size_mb"]:.1f}MB</p>',
        unsafe_allow_html=True,
    )
else:
    st.warning("지금은 최신 버전 정보를 불러오지 못했습니다. 아래 버튼을 눌러 릴리스 페이지에서 설치파일(.exe)을 받아 주세요.")
    st.link_button("릴리스 페이지 열기", RELEASES_PAGE, type="primary", width="stretch")

step1 = (
    "위의 <b>[다운로드]</b> 버튼을 눌러 설치파일을 받습니다."
    if release
    else "위의 버튼으로 릴리스 페이지를 열고, 끝이 <b>.exe</b>인 파일을 눌러 받습니다."
)
st.markdown(
    f"""
### 설치 방법
<ol class="steps">
  <li><span class="n">1</span><span>{step1}</span></li>
  <li><span class="n">2</span><span>받은 파일을 <b>더블클릭</b>합니다.</span></li>
  <li><span class="n">3</span><span>파란색 <b>"Windows의 PC 보호"</b> 창이 뜨면 <b>[추가 정보]</b>를 누른 뒤 <b>[실행]</b>을 누릅니다.</span></li>
  <li><span class="n">4</span><span><b>[다음]</b>을 눌러 설치를 마칩니다.</span></li>
  <li><span class="n">5</span><span>바탕화면에 생긴 <b>아이콘</b>을 눌러 실행합니다.</span></li>
</ol>

<div class="note">
  <p>⚠️ 프로그램 설치가 막힌 PC에서는 설치가 안 될 수 있습니다.</p>
  <p>⚠️ 회사 VDI는 재부팅하면 설치한 프로그램이 사라지므로 접속할 때마다 다시 설치해야 합니다.</p>
</div>

<p class="law">국회 영상·자막은 국회법 제149조에 따라 상업적 목적으로 사용할 수 없습니다.</p>
""",
    unsafe_allow_html=True,
)
