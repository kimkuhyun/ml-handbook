from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class PreprocLDAPage(BasePage):
    title = "LDA 감독 축소"
    slug = "preprocess_lda"
    icon = "🎯"
    group = "models"
    section = "전처리"
    order = 50

    def render(self) -> None:
        inject_global_style()
        st.title("🎯 LDA(Linear Discriminant) 감독 축소")
        badges(["감독 차원축소", "분리 축", "SVM/LogReg 시너지"])

        st.markdown("### 왜 했나?")
        card(
            "- 라벨을 이용해 **클래스가 잘 갈라지는 축**을 만듭니다.\n"
            "- 축 소수(1~3)로 압축하면 **경계가 또렷**해져, 단순 분류기가 유리해집니다.\n"
        )

        st.markdown("### 파이프라인")
        card(
            "- `StandardScaler → LDA(shrinkage 권장) → 분류기(SVM/LogReg)`\n"
            "- 모든 단계는 **폴드 내부 fit**\n"
        )

        st.markdown("### 결과(예시)")
        card(
            "- **LDA→SVM**: 정확도 **~0.53** (이번 LDA류 중 최고)\n"
            "- **LDA→LogReg**: 정확도 **~0.48**\n"
        )

        st.markdown("### 팁/주의")
        card(
            "- LDA 가정(가우시안/공분산)이 크게 틀리면 이득이 제한적\n"
            "- **shrinkage**(수축) 옵션으로 수치 안정성↑\n"
        )

PageRegistry.register(PreprocLDAPage)

