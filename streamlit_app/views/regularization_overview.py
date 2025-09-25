# streamlit_app/views/regularization_overview.py
from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class RegularizationOverviewPage(BasePage):
    title = "드롭아웃/라벨 스무딩"
    slug = "regularization_overview"
    icon = "🛡️"
    group = "models"
    section = "규제"
    order = 10

    def render(self) -> None:
        inject_global_style()
        st.title("🛡️ 드롭아웃 & 라벨 스무딩")
        badges(["과적합 방지", "안정화", "확률 품질"])

        st.markdown("### 드롭아웃 (Dropout)")
        card(
            "- 학습 중 일부 뉴런을 무작위로 끊어 **과적합**을 줄입니다.\n"
            "- MLP에서 0.2~0.5 범위로 탐색; 너무 크면 **언더핏** 위험.\n"
        )

        st.markdown("### 라벨 스무딩 (Label Smoothing)")
        card(
            "- 정답 확률을 1.0 대신 **1-ε**로, 나머지에 ε를 조금씩 분배.\n"
            "- 과신을 줄여 **일반화/확률 캘리브레이션**에 도움.\n"
        )

        st.markdown("### 이번 프로젝트에서의 메모")
        card(
            "- 드롭아웃 0.4 내외가 안정적.\n"
            "- 라벨 스무딩은 **과하면** 성능 하락 → 0.05 전후로 보수 적용.\n"
        )

PageRegistry.register(RegularizationOverviewPage)

