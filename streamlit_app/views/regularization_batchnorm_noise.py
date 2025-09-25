from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class RegWD_ESPage(BasePage):
    title = "Weight Decay & 조기종료"
    slug = "regularization_weightdecay_earlystop"
    icon = "⏳"
    group = "models"
    section = "규제"

    def render(self) -> None:
        inject_global_style()
        st.title("⏳Weight Decay(AdamW) & 조기종료")
        badges(["과적합 방지", "학습안정", "MLP"])

        st.markdown("### Weight Decay (AdamW)")
        card(
            "- 가중치가 **너무 커지지 않게** 살짝 잡아당기는 규제.\n"
            "- **AdamW**를 사용하면 학습률 스케줄과 잘 맞습니다.\n"
            "- 값: 보통 **1e-5 ~ 1e-3** 범위에서 탐색.\n"
        )

        st.markdown("### 조기종료 (EarlyStopping)")
        card(
            "- 검증 성능이 n 에폭 동안 좋아지지 않으면 **멈춤**.\n"
            "- 과적합을 막고, **시간도 절약**합니다.\n"
        )

        st.markdown("### 이번 프로젝트 메모")
        card(
            "- MLP에서 **적당한 WD + 조기종료**가 안정적.\n"
            "- 너무 큰 WD는 **언더핏** 위험 → 로그스케일 탐색 권장.\n"
        )

PageRegistry.register(RegWD_ESPage)

