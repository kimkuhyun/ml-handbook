# streamlit_app/pages/lightgbm.py
from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class LightGBMPage(BasePage):
    title = "LightGBM"
    slug = "lightgbm"
    icon = "🌳"

    def render(self) -> None:
        inject_global_style()
        st.title("🌳 LightGBM (Baseline)")
        badges(["GBDT", "Tabular", "Fast", "Feature Importance"])

        st.markdown("### 이 모델은 뭘까?")
        st.markdown("""
- **결정나무 여러 개를 이어 붙여** 점점 더 똑똑하게 만드는 모델이에요(부스팅).  
- 숫자 크기 차이나 결측값에 강하고, 학습이 빠른 편이에요.  
- 어떤 특성이 중요한지 살펴보기 쉬워요.  
- 아주 미세한 곡선 패턴은 신경망만큼 세밀하지 않을 수 있어요.
        """)

        st.markdown("### 왜 선택했나")
        st.markdown("""
- 표형 데이터에서 **빠르고 튼튼한 기준선**을 주기 때문이에요.  
- 전처리 부담이 적고, 실험 속도를 높여줘요.
        """)

        st.markdown("### 전처리")
        st.markdown("""
- 큰 전처리 없이도 가능하지만, **상관 높은 특성 정리**와 기본 결측 처리 권장  
- 스케일링은 필수 아님
        """)

        st.markdown("### 하이퍼파라미터(예시)")
        card("""
- 복잡도: num_leaves, max_depth  
- 규제/샘플링: min_data_in_leaf, feature_fraction, bagging_fraction  
- 학습: learning_rate, n_estimators, early_stopping
        """)

        st.markdown("### 결과(5-Fold OOF)")
        card("**Accuracy 0.7918 / Macro-F1 0.7951**")

        st.markdown("### 어려웠던 점")
        st.markdown("""
- 하이퍼파라미터에 민감  
- **0/9/15**처럼 미세 경계는 어려움
        """)

        st.markdown("### 확장 아이디어")
        card("""
- **Top-30 특성**으로 재학습 비교  
- **MLP와 블렌딩**으로 안정성↑  
- Optuna로 자동 탐색
        """)

PageRegistry.register(LightGBMPage)

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

