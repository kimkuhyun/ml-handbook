from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class KNNPage(BasePage):
    title = "KNN"
    slug = "knn"
    icon = "👥"
    group = "models"
    section = "모델"

    def render(self) -> None:
        inject_global_style()
        st.title("👥 KNN (K-Nearest Neighbors)")
        badges(["사례 기반", "거리", "간단"])

        st.markdown("### 이 모델은?")
        st.markdown(
            "- **가까운 K개 이웃**의 다수결로 클래스를 정합니다.\n"
            "- 학습은 거의 없고, 예측 시 계산이 많습니다.\n"
        )

        st.markdown("### 왜 선택했나")
        st.markdown(
            "- **아주 단순한 기준선**으로 비교용.\n"
            "- 작은 문제에선 직관적입니다.\n"
        )

        st.markdown("### 전처리")
        st.markdown(
            "- **StandardScaler 중요**.\n"
            "- **차원(52)**이 높으면 거리 개념이 약해집니다.\n"
        )

        st.markdown("### 하이퍼파라미터(예시)")
        card(
            "- `n_neighbors`: 3~31\n"
            "- `weights`: 'uniform' / 'distance'\n"
            "- `metric`: 'euclidean'\n"
        )

        st.markdown("### 결과(5-Fold OOF)")
        card("**정확도 ≈ 0.27** (가장 낮음)")

        st.markdown("### 어려웠던 점")
        st.markdown(
            "- **차원의 저주** 영향 큼.\n"
            "- 데이터가 크면 예측이 **느림**.\n"
        )

        st.markdown("### 확장 아이디어")
        card(
            "- **감독 차원 축소**(LDA/NCA) 후 KNN.\n"
            "- **아주 작은 서브셋** 전용 전문가로 제한 사용.\n"
        )

PageRegistry.register(KNNPage)

