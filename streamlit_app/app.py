# streamlit_app/app.py
from __future__ import annotations

from pathlib import Path
import sys
import streamlit as st

# 프로젝트 루트 경로 주입
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from streamlit_app.core.base import App
# ↓ 레지스트리에 등록시키기 위해 임포트 (파일명만 변경)
import streamlit_app.views.home      # noqa: F401
import streamlit_app.views.mlp       # noqa: F401
import streamlit_app.views.lightgbm  # noqa: F401
import streamlit_app.views.blending  # noqa: F401
import streamlit_app.views.lda_svm   # noqa: F401

st.set_page_config(page_title="우리만의 AI 교과서 · Home", page_icon="📘", layout="wide")

def main():
    app = App(project_title="우리만의 AI 교과서", repo_name="ml-handbook")
    app.run()

if __name__ == "__main__":
    main()

