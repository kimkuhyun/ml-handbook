from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class LogRegPage(BasePage):
    title = "로지스틱 회귀"
    slug = "logreg"
    icon = "📈"
    group = "models"
    section = "모델"
    order = 60

    def render(self) -> None:
        inject_global_style()
        st.title("📈 로지스틱 회귀 (Logistic Regression)")
        badges(["선형 모델", "빠름", "기준선", "해석 용이"])

        st.markdown("### 이 모델은?")
        st.markdown(
            "- **직선/평면 경계**로 클래스를 나눕니다.\n"
            "- 학습이 **빠르고 안정적**이며, 결과(확률)를 **이해하기 쉽습니다.\n"
        )

        st.markdown("### 왜 선택했나")
        st.markdown(
            "- 데이터/파이프라인 점검용 **기준선** 확보.\n"
            "- 빠르게 **정상 동작 여부** 확인.\n"
        )

        st.markdown("### 전처리")
        st.markdown(
            "- **StandardScaler** 필수(스케일에 민감).\n"
            "- 상관 높은 피처 일부 제거는 선택.\n"
        )

        st.markdown("### 하이퍼파라미터(예시)")
        card(
            "- `C`(규제 강도): 0.1 ~ 10\n"
            "- `penalty`: 'l2'\n"
            "- `multi_class`: 'multinomial'\n"
            "- `solver`: 'lbfgs'\n"
        )

        st.markdown("### 결과(5-Fold OOF)")
        card("**정확도 ≈ 0.47** (Macro-F1 유사)")

        st.markdown("### 어려웠던 점")
        st.markdown(
            "- 경계가 **직선**이라 **구부러진 패턴**을 놓칩니다.\n"
            "- **스케일**에 매우 민감합니다.\n"
        )

        st.markdown("### 확장 아이디어")
        card(
            "- **다항/상호작용** 피처 추가로 비선형 흉내.\n"
            "- **확률 캘리브레이션**(온도/클래스 바이어스) 적용.\n"
            "- **스태킹 메타 모델**로 활용.\n"
        )

PageRegistry.register(LogRegPage)

