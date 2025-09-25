# streamlit_app/pages/blending.py
from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class BlendingPage(BasePage):
    title = "Blending (DNN 0.85 + LGBM 0.15)"
    slug = "blending"
    icon = "⚗️"
    group = "models"
    section = "모델"

    def render(self) -> None:
        inject_global_style()
        st.title("⚗️ Blending: DNN 0.85 + LGBM 0.15")
        badges(["Ensemble", "Stability", "Soft Voting"])

        st.markdown("### 이 방법은 뭘까?")
        st.markdown("""
- 서로 다른 모델의 **예측 확률을 섞는 방법**이에요.  
- MLP는 **곡선 패턴**, LGBM은 **규칙성**에 강해서 성격이 달라요.  
- 합치면 **안정성**이 올라가고, **소폭의 성능 이득**도 기대돼요.
        """)

        st.markdown("### 왜 선택했나")
        st.markdown("""
- MLP가 최고였지만 폴드별 편차를 줄이고 싶었어요.  
- LGBM을 살짝 섞어 **흔들림을 완화**했어요.
        """)

        st.markdown("### 전처리")
        st.markdown("""
- 각 모델은 자기 전처리(MlP=스케일링, LGBM=기본)  
- 두 모델의 **확률**을 받아 **가중 평균**
        """)

        st.markdown("### 하이퍼파라미터(예시)")
        card("""
- 가중치: **MLP 0.85 / LGBM 0.15**  
- (옵션) 로짓 블렌딩: 확률 대신 로그확률(로짓)을 섞기
        """)

        st.markdown("### 결과(5-Fold OOF)")
        card("**Accuracy 0.8544 / Macro-F1 0.8570**  (안정성↑, 점수는 MLP Top-30와 비슷)")

        st.markdown("### 어려웠던 점")
        st.markdown("""
- 가중치를 잘못 잡으면 오히려 하락  
- 모델/파일 관리가 2배로 복잡
        """)

        st.markdown("### 확장 아이디어")
        card("""
- **seed 배깅 MLP** + LGBM → 소규모 앙상블  
- (여유) **CatBoost** 추가로 3-way
        """)

PageRegistry.register(BlendingPage)

# --- bootstrap for Streamlit native multipage ---
if __name__ == "__main__":
    # 이 파일이 독립 페이지로 실행될 때를 대비한 루트 경로 주입
    from pathlib import Path
    import sys
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    import streamlit as st
    st.set_page_config(page_title=f"우리만의 AI 교과서 · {getattr(type(globals().get(list(globals().values())[0]), '__name__', 'Page'), 'title', 'Page')}", page_icon="📘", layout="wide")

    # 현재 파일의 Page 클래스를 직접 인스턴스화하여 렌더
    # 예: HomePage().render()
    try:
        # 현재 모듈에 정의된 BasePage 서브클래스를 찾아 실행
        from streamlit_app.core.base import BasePage
        page_cls = next(
            cls for cls in globals().values()
            if isinstance(cls, type) and issubclass(cls, BasePage) and cls is not BasePage
        )
        page_cls().render()
        st.markdown("---")
        st.caption("© 2025 우리만의 AI 교과서 · Repo: ml-handbook")
    except StopIteration:
        st.error("No page class found to render.")

