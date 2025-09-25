from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class CascadePage(BasePage):
    title = "캐스케이드 (어려운 샘플)"
    slug = "cascade"
    icon = "🔀"
    group = "models"
    section = "모델"

    def render(self) -> None:
        inject_global_style()
        st.title("🔀 캐스케이드: 어려운 샘플만 다시 판정")
        badges(["후처리", "게이팅", "하드 샘플 집중"])

        st.markdown("### 이 방법은?")
        st.markdown(
            "- **1단계**: 전체를 기본 모델로 예측.\n"
            "- **2단계**: **애매한 샘플**만 별도 전문가로 재분류.\n"
        )

        st.markdown("### 왜 선택했나")
        st.markdown(
            "- 계산을 **정말 어려운 구간**(예: {0,9,15})에만 집중.\n"
            "- 쉬운 샘플은 그대로 두어 **안정성 확보**.\n"
        )

        st.markdown("### 전처리/지표")
        st.markdown(
            "- 1단계 확률로 **p_max, margin, entropy** 추출.\n"
            "- **게이트**(보낼지 말지) 기준을 정함.\n"
        )

        st.markdown("### 하이퍼파라미터(예시)")
        card(
            "- 게이트: `top_thr`, `margin`, `entropy_thr`\n"
            "- 전문가: LDA→SVM, 쌍대 로지스틱 등\n"
        )

        st.markdown("### 결과(파일럿)")
        card(
            "- 순진한 캐스케이드: **정확도 ≈ 0.58**(하락).\n"
            "- **게이팅** 적용: 기본과 비슷하거나 소폭 +α.\n"
            "- 최종 판단: **블렌딩이 더 안전**.\n"
        )

        st.markdown("### 어려웠던 점")
        st.markdown(
            "- 과도한 교정으로 **오히려 악화**되기 쉬움.\n"
            "- 게이트 튜닝에 민감, 이득은 데이터 의존.\n"
        )

        st.markdown("### 확장 아이디어")
        card(
            "- **합의 게이트**: 전문가가 1단계 **상위 2순위**와 같을 때만 뒤집기.\n"
            "- 전문가 출력을 **스태킹 메타 피처**로 활용.\n"
        )

PageRegistry.register(CascadePage)

