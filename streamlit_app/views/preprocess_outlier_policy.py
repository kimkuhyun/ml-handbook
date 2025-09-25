from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class PreprocOutlierPage(BasePage):
    title = "이상치 정책(IQR/Z-score)"
    slug = "preprocess_outlier_policy"
    icon = "🚧"
    group = "models"
    section = "전처리"

    def render(self) -> None:
        inject_global_style()
        st.title("🚧 이상치 정책 (IQR / Z-score)")
        badges(["Outlier", "클리핑", "주의"])

        st.markdown("### 실험에서의 관찰")
        card(
            "- 강한 **제거/클리핑**은 점수 **하락** 경향.\n"
            "- 이 데이터는 극단값도 **의미 신호**일 수 있습니다.\n"
        )

        st.markdown("### 정책")
        card(
            "- **하드 제거 금지**(권장): 모델이 스스로 견디게\n"
            "- 필요시 **winsorize**(상하 퍼센타일 경계로 완만 클리핑)\n"
        )

        st.markdown("### 팁")
        card(
            "- 먼저 **모델 기반 중요도**로 해당 피처가 정말 문제인지 확인\n"
            "- 제거/클리핑은 항상 **OOF로 재검증**\n"
        )

PageRegistry.register(PreprocOutlierPage)

