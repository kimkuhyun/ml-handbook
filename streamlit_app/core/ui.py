# streamlit_app/core/ui.py
import streamlit as st
from html import escape  # ← 추가

GLOBAL_STYLE = """
<style>
.badge {display:inline-block; padding:4px 10px; border-radius:999px;
        background:#EEF2FF; color:#4338CA; font-size:0.85rem; margin-right:6px;}
.card {border:1px solid #e5e7eb; border-radius:12px; padding:16px; background:#fff;}
.kv {display:flex; gap:8px; flex-wrap:wrap;}
.kv > div {background:#F9FAFB; border:1px solid #e5e7eb; border-radius:8px; padding:10px 12px;}
.small {color:#6b7280; font-size:0.9rem;}
.hint {background:#F0FDF4; border:1px solid #86efac; padding:10px 12px; border-radius:8px;}
</style>
"""

def inject_global_style():
    st.markdown(GLOBAL_STYLE, unsafe_allow_html=True)

def badges(items):
    # items가 None이거나 비어있을 때도 안전하게
    items = items or []
    html_badges = "".join(
        f'<span class="badge">{escape(str(x))}</span>'
        for x in items
    )
    st.markdown(html_badges, unsafe_allow_html=True)

def card(md: str):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(md)
    st.markdown('</div>', unsafe_allow_html=True)

def hint(md: str):
    st.markdown(f'<div class="hint">{md}</div>', unsafe_allow_html=True)

