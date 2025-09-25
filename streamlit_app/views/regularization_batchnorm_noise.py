from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class RegBNNoisePage(BasePage):
    title = "규제 · 배치정규화 & 입력노이즈"
    slug = "regularization_batchnorm_noise"
    icon = "🧯"
    group = "models"
    section = "규제"
    order = 30

    def render(self) -> None:
        inject_global_style()
        st.title("🧯 규제: 배치정규화(BN) & 입력 노이즈")
        badges(["안정화", "일반화", "주의"])

        st.markdown("### 배치정규화 (BatchNorm)")
        card(
            "- 층마다 분포를 **정돈**해 학습을 안정화합니다.\n"
            "- MLP 블록에 BN을 넣으면 수렴이 **부드러워**집니다.\n"
        )

        st.markdown("### 입력 노이즈")
        card(
            "- 입력에 작은 **가우시안 노이즈**를 더해 **과적합을 완화**하는 방법.\n"
            "- 이번 데이터에서는 **효과가 제한적**이었습니다.\n"
        )

        st.markdown("### 팁")
        card(
            "- BN은 드롭아웃과 **함께** 쓰되, 순서/강도를 조심\n"
            "- 입력 노이즈는 **적게**(예: 0.01~0.05 표준편차) 시도\n"
        )

PageRegistry.register(RegBNNoisePage)

