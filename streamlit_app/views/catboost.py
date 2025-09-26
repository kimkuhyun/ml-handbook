from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class CatBoostPage(BasePage):
    title = "CatBoost"
    slug = "catboost"
    icon = "🐈"
    group = "models"
    section = "모델"

    def render(self) -> None:
        inject_global_style()
        st.title("🐈 CatBoost")
        badges(["GBDT", "탭형 강자", "자동 상호작용", "기본값 강함"])

        st.markdown("### 이 모델은?")
        st.markdown(
            "- LightGBM과 유사한 **부스팅 트리** 모델.\n"
            "- **상호작용/노이즈**를 잘 처리하고, 탭형 데이터에서 강력.\n"
        )

        st.markdown("### 왜 선택했나")
        st.markdown(
            "- LGBM/MLP 대비 **추가 상승 여지** 탐색.\n"
        )

        st.markdown("### 전처리")
        st.markdown(
            "- 특별한 스케일링 필요 없음.\n"
            "- **Top-30 vs 전체** 비교 유지.\n"
        )

        st.markdown("### 하이퍼파라미터(예시)")
        card(
            "- `depth`(6~10), `learning_rate`(0.02~0.1), `l2_leaf_reg`\n"
            "- `iterations`, `loss_function='MultiClass'`\n"
            "- 조기종료: `od_type='Iter'`, `od_wait`\n"
        )

        st.markdown("### 결과")
        card(
            "- 아직 본 실험 없음. 유사 탭형에서 **정확도 0.6~0.7대** 보고 사례 다수.\n"
            "- 실제는 **5-Fold OOF**로 검증 예정.\n"
        )

        st.markdown("### 어려웠던 점")
        st.markdown(
            "- 의존성/학습시간 증가.\n"
            "- OOF 설계 중요(과대평가 방지).\n"
        )

        st.markdown("### 확장 아이디어")
        card(
            "- MLP/LGBM과 **3-way 블렌딩**.\n"
            "- **계층 분류 노드** 분류기로 채택(3 → 0 vs {9,15} → 9 vs 15).\n"
        )

PageRegistry.register(CatBoostPage)

