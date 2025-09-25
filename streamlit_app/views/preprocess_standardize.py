# streamlit_app/views/preprocess_standardize.py
from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class PreprocStandardizePage(BasePage):
    title = "표준화(StandardScaler)"
    slug = "preprocess_standardize"
    icon = "🎚️"
    group = "models"
    section = "전처리"
    order = 20

    def render(self) -> None:
        inject_global_style()
        st.title("🎚️ 표준화 (StandardScaler)")
        badges(["스케일 정규화", "선형/커널 민감", "필수"])

        st.markdown("### 왜 필요한가?")
        card(
            "- 피처마다 크기(스케일)가 다르면, 거리/마진 기반 모델(SVM/로지스틱)이 **왜곡**됩니다.\n"
            "- 평균 0, 표준편차 1로 맞춰 **학습 안정**과 **수렴**을 돕습니다.\n"
        )

        st.markdown("### 적용 팁")
        card(
            "- **교차검증 폴드 내부**에서만 fit 후 transform (데이터 누수 방지)\n"
            "- 트리/부스팅 계열(LGBM/XGB)은 필수는 아님\n"
        )

PageRegistry.register(PreprocStandardizePage)

