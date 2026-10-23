"""AI 자막 수집기 — 프로그램 다운로드 사이트 (Streamlit)

GitHub 릴리스 목록(releases)에서 최신 프로그램(v3.0부터 휴대용 .zip, 그 전은 설치파일 .exe)과
버전별 다운로드 목록을 가져와 보여준다.
새 릴리스를 올리면 코드를 고치지 않아도 자동으로 최신 파일로 바뀐다.
"""

from datetime import datetime, timedelta, timezone

from html import escape

import requests
import streamlit as st

# ── 설정 ─────────────────────────────────────────────
# 프로그램이 올라가는 GitHub 저장소 (소유자/이름). 저장소가 바뀌면 여기만 고친다.
GITHUB_REPO = "roba97-web/subtitle-download"
# ─────────────────────────────────────────────────────

API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases?per_page=20"
RELEASES_PAGE = f"https://github.com/{GITHUB_REPO}/releases/latest"
KST = timezone(timedelta(hours=9))

# 파일 끝(확장자)에 따라 목록에 보여줄 설명
FILE_KINDS = {
    ".exe": "설치파일",
    ".pptx": "사용 설명서 (파워포인트)",
    ".pdf": "사용 설명서 (PDF)",
    ".txt": "사용법 (메모장)",
    ".zip": "프로그램 (압축을 풀고 실행)",
}

st.set_page_config(page_title="AI 자막 수집기 다운로드", page_icon="💬", layout="centered")


def _size_text(size_bytes):
    if size_bytes < 100 * 1024:
        return f"약 {max(1, round(size_bytes / 1024))}KB"
    return f"약 {size_bytes / 1024 / 1024:.1f}MB"


# 다운로드 버튼에 연결할 '프로그램' 파일: 휴대용 zip(v3.0~) 또는 설치파일 exe(~v2.4)
def _is_program(name):
    return name.lower().endswith((".zip", ".exe"))


def _file_kind(name):
    lower = name.lower()
    return next((kind for ext, kind in FILE_KINDS.items() if lower.endswith(ext)), "파일")


@st.cache_data(ttl=600, show_spinner=False)
def fetch_releases():
    """버전별 다운로드 목록(최신이 맨 앞). 실패하면 예외(실패는 캐시되지 않음)."""
    resp = requests.get(
        API_URL,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "subtitle-download-site"},
        timeout=10,
    )
    resp.raise_for_status()
    releases = []
    for data in resp.json():
        if data.get("draft") or data.get("prerelease"):
            continue
        files = [
            {
                "name": a.get("label") or a["name"],   # 표시 이름(label)이 있으면 그것을 보여줌
                "file": a["name"],
                "kind": _file_kind(a["name"]),
                "url": a["browser_download_url"],
                "size": _size_text(a.get("size", 0)),
            }
            for a in data.get("assets", [])
            if "ocr" not in a["name"].lower()
        ]
        if not files:
            continue
        files.sort(key=lambda f: not _is_program(f["file"]))  # 프로그램 파일을 맨 위로
        published = datetime.fromisoformat(data["published_at"].replace("Z", "+00:00")).astimezone(KST)
        releases.append({
            "version": data.get("tag_name", ""),
            "date": f"{published.year}년 {published.month}월 {published.day}일",
            "portable": files[0]["file"].lower().endswith(".zip"),
            "files": files,
        })
    if not releases or not _is_program(releases[0]["files"][0]["file"]):
        raise LookupError("최신 릴리스에 프로그램 파일(.zip 또는 .exe)이 없습니다")
    return releases


def file_list_html(files):
    rows = "".join(
        f'''<li class="file">
  <div class="meta"><b>{escape(f["kind"])}</b><span>{escape(f["name"])} · {f["size"]}</span></div>
  <a class="get" href="{escape(f["url"])}" download>받기</a>
</li>'''
        for f in files
    )
    return f'<ul class="files">{rows}</ul>'


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
.files { list-style: none; padding: 0 !important; margin: 0.3rem 0 0.8rem 0 !important; }
.files li.file { margin: 0 0 0.6rem 0 !important; padding: 0.7rem 0.9rem !important; display: flex; align-items: center;
                 gap: 0.8rem; border: 1px solid rgba(74, 111, 165, 0.45); border-radius: 10px; }
.files .meta { flex: 1 1 auto; min-width: 0; display: flex; flex-direction: column; line-height: 1.5; }
.files .meta span { font-size: 0.85rem; opacity: 0.7; overflow-wrap: anywhere; }
.files a.get { flex: 0 0 auto; padding: 0.45rem 1.1rem; border-radius: 8px; background: var(--navy);
               border: 1px solid var(--navy-line); color: #fff !important; text-decoration: none !important; font-weight: 700; }
.files a.get:hover { background: #2a4d87; }
.law { font-size: 0.85rem; opacity: 0.7; margin-top: 1.5rem; word-break: keep-all; }
</style>
<div class="hero">
  <h1>AI 자막 수집기</h1>
  <p>국회 인터넷의사중계·유튜브 등 영상 화면에 나오는 자막을 모아
     txt 파일로 저장하거나 복사해 주는 윈도우 프로그램입니다. 설치 없이 압축만 풀면 바로 실행됩니다.</p>
</div>
""",
    unsafe_allow_html=True,
)

try:
    releases = fetch_releases()
except Exception:
    releases = None

if releases:
    latest = releases[0]
    exe = latest["files"][0]
    portable = latest["portable"]
    st.markdown(
        f'<span class="ver">최신 버전 <b>{latest["version"]}</b> · {latest["date"]} 올라옴</span>',
        unsafe_allow_html=True,
    )
    st.link_button("⬇  다운로드", exe["url"], type="primary", width="stretch")
    st.markdown(
        f'<p class="small">윈도우용 {"프로그램 (설치 없이 실행, zip)" if portable else "설치파일"} · {exe["size"]}</p>',
        unsafe_allow_html=True,
    )
else:
    portable = True
    st.warning("지금은 최신 버전 정보를 불러오지 못했습니다. 아래 버튼을 눌러 릴리스 페이지에서 프로그램(Portable이 들어간 .zip)을 받아 주세요.")
    st.link_button("릴리스 페이지 열기", RELEASES_PAGE, type="primary", width="stretch")

if releases:
    st.markdown("### 다운로드 목록")
    st.markdown(
        f'<p class="small">최신 버전 <b>{escape(latest["version"])}</b>에 올라온 파일입니다.</p>'
        + file_list_html(latest["files"]),
        unsafe_allow_html=True,
    )
    if len(releases) > 1:
        with st.expander("이전 버전 보기"):
            for r in releases[1:]:
                st.markdown(
                    f'<p class="small"><b>{escape(r["version"])}</b> · {r["date"]}</p>' + file_list_html(r["files"]),
                    unsafe_allow_html=True,
                )

step1 = (
    "위의 <b>[다운로드]</b> 버튼을 눌러 프로그램(zip)을 받습니다."
    if releases
    else "위의 버튼으로 릴리스 페이지를 열고, 이름에 <b>Portable</b>이 들어간 <b>.zip</b> 파일을 눌러 받습니다."
)
if portable:
    steps_html = f"""
### 실행 방법 (설치하지 않습니다)
<ol class="steps">
  <li><span class="n">1</span><span>{step1}</span></li>
  <li><span class="n">2</span><span>받은 zip 파일을 <b>마우스 오른쪽 버튼</b>으로 누르고 <b>[모두 압축 풀기]</b>를 누릅니다.</span></li>
  <li><span class="n">3</span><span>풀린 <b>AI-Subtitle</b> 폴더 안의 <b>NASubtitle.exe</b>를 더블클릭합니다.</span></li>
  <li><span class="n">4</span><span>파란색 <b>"Windows의 PC 보호"</b> 창이 뜨면 <b>[추가 정보]</b>를 누른 뒤 <b>[실행]</b>을 누릅니다.</span></li>
  <li><span class="n">5</span><span>자주 쓰려면 NASubtitle.exe를 마우스 오른쪽 버튼 → <b>[보내기]</b> → <b>[바탕 화면에 바로 가기 만들기]</b>.</span></li>
</ol>

<div class="note">
  <p>⚠️ zip을 풀지 않고 안에서 바로 실행하면 안 됩니다. 꼭 압축을 푼 뒤 실행하세요.</p>
  <p>⚠️ 모은 기록은 같은 폴더의 <b>data</b> 폴더에 저장됩니다. 폴더를 지우면 기록도 지워집니다.</p>
  <p>⚠️ 회사 VDI는 재부팅하면 받은 파일이 사라지므로 접속할 때마다 다시 받아서 압축을 풀어야 합니다.</p>
  <p>📘 자세한 사용법은 다운로드 목록의 <b>사용법 PPT</b>를 보세요.</p>
</div>
"""
else:
    steps_html = f"""
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
"""
st.markdown(
    steps_html
    + """
<p class="law">국회 영상·자막은 국회법 제149조에 따라 상업적 목적으로 사용할 수 없습니다.</p>
""",
    unsafe_allow_html=True,
)
