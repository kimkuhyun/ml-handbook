from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class SVMPage(BasePage):
    title = "SVM (RBF)"
    slug = "svm"
    icon = "🧩"
    group = "models"
    section = "모델"

    def render(self) -> None:
        inject_global_style()
        st.title("🧩 SVM (RBF 커널)")
        badges(["마진 최대화", "비선형", "스케일 필요", "튜닝 중요"])

        st.markdown("### 이 모델은?")
        st.markdown(
            "- 두 클래스 사이 **여유폭(마진)**이 가장 크게 되도록 경계를 찾습니다.\n"
            "- **RBF 커널**로 **구부러진 경계**도 학습합니다.\n"
        )

        st.markdown("### 왜 선택했나")
        st.markdown(
            "- 중소 규모 탭형 데이터에서 **강력한 비선형 분류기**로 자주 통합니다.\n"
        )

        st.markdown("### 전처리")
        st.markdown(
            "- **StandardScaler 필수**.\n"
            "- 폴드 내에서만 스케일링 적합(누수 방지).\n"
        )

        st.markdown("### 하이퍼파라미터(예시)")
        card(
            "- `C`: 1e2 ~ 1e4\n"
            "- `gamma`: 'scale' 또는 ~1e-3\n"
            "- `class_weight='balanced'`(옵션)\n"
        )

        st.markdown("### 결과(5-Fold OOF)")
        card(
            "**전체 21클래스 정확도 ≈ 0.46**, "
            "**포커스(0/3/9/15) 정확도 ≈ 0.38**"
        )

        st.markdown("### 어려웠던 점")
        st.markdown(
            "- 학습 시간이 길어질 수 있음.\n"
            "- **0/9/15** 혼동을 끝내 해소하지 못함.\n"
        )

        st.markdown("### 확장 아이디어")
        card(
            "- **LDA → SVM** 파이프라인(감독 축소 후 분류).\n"
            "- **랜덤→그리드 2단계 탐색**으로 `C/γ` 좁히기.\n"
            "- **확률 캘리브레이션**으로 메타/블렌딩 품질 향상.\n"
        )

PageRegistry.register(SVMPage)

