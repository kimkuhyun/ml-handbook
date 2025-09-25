from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class PreprocCorrPrunePage(BasePage):
    title = "상관 피처 가지치기"
    slug = "preprocess_corr_pruning"
    icon = "🌿"
    group = "models"
    section = "전처리"
    order = 40

    def render(self) -> None:
        inject_global_style()
        st.title("🌿상관 피처 가지치기")
        badges(["Correlation", "중복 제거", "단순화"])

        st.markdown("### 왜 했나?")
        card(
            "- 서로 **매우 비슷**하게 움직이는 피처가 많으면, 모델이 **중복 신호**를 과대평가할 수 있어요.\n"
            "- 상관 높은 쌍을 줄이면 **안정성**이 좋아집니다.\n"
        )

        st.markdown("### 어떻게 했나?")
        card(
            "- 피어슨 상관 |r| ≥ 0.9 같은 기준으로 **대표 1개만 남기기**\n"
            "- 최종적으로 **약 10개 제거, 42개 유지** 버전을 실험\n"
        )

        st.markdown("### 결과/메모")
        card(
            "- 단독으론 점수 변화가 크지 않지만, **Top-30 선택**과 함께 쓰면 깔끔해집니다.\n"
            "- 규칙은 **폴드별로 fit**해서 누수 막기.\n"
        )

PageRegistry.register(PreprocCorrPrunePage)

