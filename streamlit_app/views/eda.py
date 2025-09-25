# streamlit_app/views/eda.py
from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class EDAPage(BasePage):
    title = "EDA (데이터 분석)"
    slug = "eda_main"
    icon = "🔎"
    group = "eda"         # ✅ EDA 그룹
    section = "EDA"

    def render(self) -> None:
        inject_global_style()
        st.title("🔎 EDA (데이터 분석)")
        badges(["분포", "스케일", "상관", "특징 선택"])

        st.markdown("### 데이터 한 눈에")
        card(
            "- 입력: **52개 숫자 피처** (`X_01 ~ X_52`)\n"
            "- 라벨: **21개 클래스** (의미 비공개)\n"
            "- 각 행: **동일 시점 스냅샷** (타임스탬프 없음)\n"
        )

        st.markdown("### 핵심 관찰")
        card(
            "- 피처마다 **스케일/분포가 제각각** → 표준화가 유리\n"
            "- **상관 높은 피처** 존재 → Top-30 선별이 성능에 도움\n"
            "- 일부 클래스 간 **분포 겹침**(특히 0/9/15)\n"
        )

        st.markdown("### 시사점")
        card(
            "- **StandardScaler** + **Top-30 피처**로 모델에 입력\n"
            "- 0/9/15 혼동 완화를 위해 **감독 축소(LDA)**나\n"
            "  **전문가/게이팅** 전략이 유효\n"
        )

PageRegistry.register(EDAPage)

