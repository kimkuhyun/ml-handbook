from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class RegGatingPage(BasePage):
    title = "게이팅/임계값(결정 보정)"
    slug = "regularization_gating"
    icon = "🚦"
    group = "models"
    section = "규제"
    order = 60

    def render(self) -> None:
        inject_global_style()
        st.title("🚦게이팅/임계값 (결정 보정)")
        badges(["후처리", "안전장치", "전문가 결합"])

        st.markdown("### 왜 쓰나?")
        card(
            "- 모델이 **애매**할 때만, 전문가/보조모델의 판단을 **부분 적용**해 실수를 줄입니다.\n"
            "- 전체를 뒤집지 않으니 **리스크가 낮습니다**.\n"
        )

        st.markdown("### 대표 규칙")
        card(
            "- `top_thr`: 상위 클래스 확률 합이 높을 때만 개입\n"
            "- `margin`: 1등-2등 차이가 **작을 때만** 개입\n"
            "- **합의(Consensus)**: 전문가가 1단계 **2순위**와 **같을 때만** 덮기\n"
        )

        st.markdown("### 메모")
        card(
            "- 과도한 개입은 **오히려 악화** → 보수적으로!\n"
            "- 전문가 출력은 **스태킹 메타 피처**로 쓰면 더 안전합니다.\n"
        )

PageRegistry.register(RegGatingPage)

