from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class PreprocAEPage(BasePage):
    title = "오토인코더 잠재벡터"
    slug = "preprocess_ae_latent"
    icon = "🧬"
    group = "models"
    section = "전처리"
    order = 60

    def render(self) -> None:
        inject_global_style()
        st.title("🧬오토인코더(자동표현) 잠재벡터")
        badges(["표현학습", "노이즈완화", "스택 피처"])

        st.markdown("### 아이디어")
        card(
            "- 입력 52차원을 **압축/복원**하도록 학습 → **잠재벡터 z** 획득\n"
            "- 원 피처에 **z를 덧붙여** 모델에 입력 (정보 보강)\n"
        )

        st.markdown("### 중요한 규칙(누수 방지)")
        card(
            "- 각 폴드에서 **train으로만 AE 학습**, val/test는 **그 AE로만 인코딩**\n"
            "- 즉, 항상 **OOF 방식**으로 만드세요.\n"
        )

        st.markdown("### 결과/메모")
        card(
            "- 데이터 의존적입니다(상황 따라 +α 또는 무효).\n"
            "- 이번엔 **Top-30 + MLP**가 주력이라 **옵션**으로 유지했습니다.\n"
        )

PageRegistry.register(PreprocAEPage)

