from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class RegBaggingPage(BasePage):
    title = "시드 배깅(Seed Bagging)"
    slug = "regularization_bagging"
    icon = "🧪"
    group = "models"
    section = "규제"
    order = 40

    def render(self) -> None:
        inject_global_style()
        st.title("🧪시드 배깅 (Seed Bagging)")
        badges(["분산 감소", "안정성", "앙상블"])

        st.markdown("### 아이디어")
        card(
            "- 같은 모델을 **시드만 다르게** 여러 번 학습 → 확률 **평균**\n"
            "- 운(초기값)으로 인한 편차를 줄여 **일반화**를 돕습니다.\n"
        )

        st.markdown("### 적용 팁")
        card(
            "- 3~5개 시드로 충분한 경우가 많습니다.\n"
            "- MLP에서 특히 효과적이었고, **스태킹**에도 이점.\n"
        )

        st.markdown("### 결과 메모")
        card(
            "- MLP의 **폴드 표준편차 감소**, 블렌딩/메타에서 품질 개선.\n"
        )

PageRegistry.register(RegBaggingPage)

