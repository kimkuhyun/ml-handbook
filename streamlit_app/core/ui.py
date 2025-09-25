# streamlit_app/core/ui.py
from __future__ import annotations
import streamlit as st
from html import escape

GLOBAL_STYLE = """
<style>
.badge {
  display:inline-block; padding:4px 10px; border-radius:999px;
  background:#EEF2FF; color:#4338CA; font-size:0.85rem; margin-right:6px;
}
.card-box {
  border:1px solid #e5e7eb; border-radius:12px; padding:16px; background:#fff;
}
.hint { background:#F0FDF4; border:1px solid #86efac; padding:10px 12px; border-radius:8px; }
.small { color:#6b7280; font-size:0.9rem; }
.kv { display:flex; gap:8px; flex-wrap:wrap; }
.kv > div { background:#F9FAFB; border:1px solid #e5e7eb; border-radius:8px; padding:10px 12px; }
</style>
"""

def inject_global_style():
    st.markdown(GLOBAL_STYLE, unsafe_allow_html=True)

def badges(items):
    items = items or []
    html_badges = "".join(f'<span class="badge">{escape(str(x))}</span>' for x in items)
    st.markdown(html_badges, unsafe_allow_html=True)

def _supports_bordered_container() -> bool:
    # Streamlit 1.25.0+ 에서 border=True 지원
    try:
        parts = st.__version__.split(".")
        major, minor = int(parts[0]), int(parts[1])
        return (major > 1) or (major == 1 and minor >= 25)
    except Exception:
        return False

def card(md_text: str):
    # ✅ 절대 빈 컨테이너를 미리 만들지 않음
    if _supports_bordered_container():
        with st.container(border=True):
            st.markdown(md_text)
    else:
        # 구버전 폴백: HTML 카드로 감싸되, 줄바꿈만 보존
        html_text = escape(md_text).replace("\n", "<br>")
        st.markdown(f'<div class="card-box">{html_text}</div>', unsafe_allow_html=True)

def hint(md_text: str):
    st.markdown(f'<div class="hint">{md_text}</div>', unsafe_allow_html=True)

def kv(items: list[tuple[str, str]]):
    bits = [f'<div><span class="small">{escape(k)}</span><br><b>{escape(v)}</b></div>' for k, v in items]
    st.markdown(f'<div class="kv">{"".join(bits)}</div>', unsafe_allow_html=True)

def footer(repo_name: str = "ml-handbook"):
    st.markdown("---")
    st.caption(f"© 2025 우리만의 AI 교과서 · Repo: {repo_name}")

