from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class XGBPage(BasePage):
    title = "XGBoost"
    slug = "xgboost"
    icon = "⚡"
    group = "models"
    section = "모델"

    def render(self) -> None:
        inject_global_style()
        st.title("⚡ XGBoost")
        badges(["GBDT", "탭형 강자", "강한 베이스라인"])

        st.markdown("### 이 모델은?")
        st.markdown(
            "- **트리를 순차적으로 개선**하는 부스팅 방식.\n"
            "- 규제가 잘 되어 있고 **효율적**입니다.\n"
        )

        st.markdown("### 왜 선택했나")
        st.markdown(
            "- 단일 모델로 **강력한 성능**.\n"
            "- **스태킹/블렌딩**의 좋은 베이스.\n"
        )

        st.markdown("### 전처리")
        st.markdown(
            "- 특별한 스케일링 불필요.\n"
            "- 결측/상수 피처 처리 정도.\n"
        )

        st.markdown("### 하이퍼파라미터(예시)")
        card(
            "- `max_depth`(6~8), `eta`(0.03~0.1)\n"
            "- `subsample`(0.7~0.9), `colsample_bytree`(0.7~0.9)\n"
            "- `lambda`, `alpha`, `n_estimators`\n"
            "- `objective='multi:softprob'`\n"
        )

        st.markdown("### 결과(5-Fold OOF)")
        card("**정확도 ~0.79 ~ 0.80** (LightGBM과 유사)")

        st.markdown("### 어려웠던 점")
        st.markdown(
            "- 깊이/학습률에 민감, 과적합 위험.\n"
            "- 확률이 **메타에서 과신**될 수 있어 캘리브레이션 고려.\n"
        )

        st.markdown("### 확장 아이디어")
        card(
            "- **MLP와 블렌딩**(이번 베스트 듀오).\n"
            "- **OOF 스태킹**으로 로지스틱 메타 결합.\n"
        )

PageRegistry.register(XGBPage)

