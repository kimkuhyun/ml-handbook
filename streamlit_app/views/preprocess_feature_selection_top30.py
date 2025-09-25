from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class PreprocTop30Page(BasePage):
    title = "Top-30 특징 선택"
    slug = "preprocess_top30"
    icon = "🧲"
    group = "models"
    section = "전처리"

    def render(self) -> None:
        inject_global_style()
        st.title("🧲Top-30 특징 선택")
        badges(["Feature Selection", "속도↑", "잡음↓"])

        st.markdown("### 왜 했나?")
        card(
            "- 52개 전부 쓰면 **잡음**도 함께 학습될 수 있어요.\n"
            "- 성능에 기여도가 높은 **상위 30개**만 골라 쓰면, 학습이 **빠르고** 일반화가 **안정**됩니다.\n"
        )

        st.markdown("### 어떻게 골랐나?")
        card(
            "- 기본: **모델 중요도(예: LightGBM)** 순위\n"
            "- 대안: **Mutual Information(상호정보량)**, 혹은 **permutation 중요도**\n"
            "- 폴드마다 **훈련셋으로만** 피처 선택 → 누수 방지\n"
        )

        st.markdown("### 결과(요약)")
        card(
            "- **MLP(전체 52개) → Macro-F1 ≈ 0.856**\n"
            "- **MLP(Top-30) → Macro-F1 ≈ 0.861** ⬆️\n"
            "- 속도도 단축, 튜닝 반복이 쉬워졌습니다.\n"
        )

        st.markdown("### 주의/팁")
        card(
            "- 꼭 **폴드 내부에서 fit** → 다른 폴드/테스트에 영향 주지 않기\n"
            "- 너무 적게 고르면 **정보 손실** 위험 → 20~35개 구간에서 탐색\n"
        )

PageRegistry.register(PreprocTop30Page)

