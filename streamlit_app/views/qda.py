from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class QDAPage(BasePage):
    title = "QDA"
    slug = "qda"
    icon = "🌀"
    group = "models"
    section = "모델"

    def render(self) -> None:
        inject_global_style()
        st.title("🌀 QDA (Quadratic Discriminant Analysis)")
        badges(["확률 모델", "클래스별 공분산", "빠름"])

        st.markdown("### 이 모델은?")
        st.markdown(
            "- 각 클래스가 **자기 모양(공분산)**을 가진 **가우시안 구름**이라고 가정.\n"
            "- 경계가 **곡선(2차)**으로 나옵니다.\n"
        )

        st.markdown("### 왜 선택했나")
        st.markdown(
            "- 클래스별 퍼짐이 다를 수 있다고 볼 때 **빠르게 시도**할 수 있는 모델.\n"
        )

        st.markdown("### 전처리")
        st.markdown(
            "- 가벼운 스케일링 권장.\n"
            "- **수축(shrinkage)**로 안정성 보강.\n"
        )

        st.markdown("### 하이퍼파라미터(예시)")
        card("- `reg_param`/shrinkage (구현별 상이)")

        st.markdown("### 결과(5-Fold OOF)")
        card("**정확도 ≈ 0.48** (LDA+LR과 비슷)")

        st.markdown("### 어려웠던 점")
        st.markdown(
            "- 공분산 추정이 **불안정**하면 성능이 흔들림.\n"
            "- **0/9/15** 심한 겹침 구간은 여전히 어렵습니다.\n"
        )

        st.markdown("### 확장 아이디어")
        card(
            "- **LDA → SVM** 조합으로 분리 축 강화.\n"
            "- **Top-30 피처** 선별 후 재학습.\n"
        )

PageRegistry.register(QDAPage)

