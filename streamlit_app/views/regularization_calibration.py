from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class RegCalibPage(BasePage):
    title = "확률 캘리브레이션(Temperature/Bias)"
    slug = "regularization_calibration"
    icon = "🌡️"
    group = "models"
    section = "규제"

    def render(self) -> None:
        inject_global_style()
        st.title("🌡️확률 캘리브레이션 (Temperature / Bias)")
        badges(["확률 품질", "안정화", "후처리"])

        st.markdown("### Temperature Scaling")
        card(
            "- 로짓을 **T로 나눠** 확률의 뾰족함을 조절합니다.\n"
            "- 일반적으로 **T>1**이면 확률이 덜 과신됩니다.\n"
        )

        st.markdown("### 클래스 Bias 튜닝")
        card(
            "- 클래스별로 작은 가산점(**bias**)을 더해 **macro-F1**을 맞춥니다.\n"
            "- 재학습 없이 **후처리로 빠르게** 개선 가능.\n"
        )

        st.markdown("### 이번 프로젝트 메모")
        card(
            "- 온도(T) ≈ 1.1 전후가 안정적이었고,\n"
            "- Bias 튠으로 **+0.2~0.4p** 소폭 이득을 봤습니다(OOF 기준).\n"
        )

PageRegistry.register(RegCalibPage)

