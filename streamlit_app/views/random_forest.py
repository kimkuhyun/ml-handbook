from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class RFPage(BasePage):
    title = "랜덤 포레스트"
    slug = "random_forest"
    icon = "🌲"
    group = "models"
    section = "모델"

    def render(self) -> None:
        inject_global_style()
        st.title("🌲 랜덤 포레스트 (Random Forest)")
        badges(["트리 앙상블", "배깅", "튼튼함", "중요도 제공"])

        st.markdown("### 이 모델은?")
        st.markdown(
            "- 여러 **결정나무**가 투표해서 최종 예측.\n"
            "- 잡음에 비교적 **강하고**, 탭형 데이터의 **빠른 베이스라인**.\n"
            "- **피처 중요도**로 해석이 쉬움.\n"
        )

        st.markdown("### 왜 선택했나")
        st.markdown(
            "- 빠르게 **준수한 기준선** 확인.\n"
            "- 스케일링 민감도 낮아 **준비가 간단**.\n"
        )

        st.markdown("### 전처리")
        st.markdown(
            "- **스케일링 불필요**.\n"
            "- 결측/이상치 간단 처리 정도.\n"
        )

        st.markdown("### 하이퍼파라미터(예시)")
        card(
            "- `n_estimators`: 300–1000\n"
            "- `max_depth`, `min_samples_leaf`\n"
            "- `max_features`: 'sqrt'/'log2'\n"
            "- `class_weight`: 'balanced'(옵션)\n"
        )

        st.markdown("### 결과(5-Fold OOF)")
        card("**정확도 ≈ 0.33** (이번 데이터에선 낮음)")

        st.markdown("### 어려웠던 점")
        st.markdown(
            "- **비스듬한/연속적 경계**에 약함.\n"
            "- 복잡한 패턴에서 **부스팅/MLP** 대비 한계.\n"
        )

        st.markdown("### 확장 아이디어")
        card(
            "- **GBDT**(LightGBM/XGBoost)로 전환.\n"
            "- **Top-30 피처**로 잡음 감소.\n"
            "- **스태킹의 약한 학습기**로 다양성 제공.\n"
        )

PageRegistry.register(RFPage)

