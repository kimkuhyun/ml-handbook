# streamlit_app/pages/lda_svm.py
from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

class LDASVMPage(BasePage):
    title = "LDA → SVM (focus 0/3/9/15)"
    slug = "lda_svm"
    icon = "🎯"

    def render(self) -> None:
        inject_global_style()
        st.title("🎯 LDA → SVM (포커스: 0/3/9/15)")
        badges(["Focus Classes", "Dim Reduction", "RBF-SVM"])

        st.markdown("### 이 모델은 뭘까?")
        st.markdown("""
- **LDA**는 클래스를 잘 구분하는 **새 축**을 만들어 잡음을 줄여요.  
- 그 축(1~2D)에서 **SVM(RBF)**이 구불구불한 경계를 그려요.  
- 즉, “**잘 보이게(LDA)** + **정밀 분리(SVM)**” 조합이에요.
        """)

        st.markdown("### 왜 선택했나")
        st.markdown("""
- **0/9/15**가 많이 섞여서 직접 분류가 어려웠어요.  
- 먼저 잘 보이게 만들고, 그 위에서 정밀하게 나누려는 전략이에요.
        """)

        st.markdown("### 전처리")
        st.markdown("""
- **StandardScaler**(필수) → LDA(`shrinkage='auto'`) → SVM  
- 모든 전처리는 **train-fold 기준**으로만 학습(누수 방지)
        """)

        st.markdown("### 하이퍼파라미터(예시)")
        card("""
- LDA 차원: 1~2D 권장  
- SVM: kernel='rbf', C≈1e3, gamma≈1e-3, class_weight='balanced'
        """)

        st.markdown("### 결과(4클래스 5-Fold OOF)")
        card("""
- Baseline: Logistic/SVM/MLP ≈ 0.46~0.47, RF ≈ 0.33, KNN ≈ 0.27  
- **LDA→LogReg ≈ 0.48**, **LDA→SVM ≈ 0.53 (최고)**
        """)

        st.markdown("### 어려웠던 점")
        st.markdown("""
- **0↔9**, **9↔15**는 여전히 겹침  
- SVM 파라미터 과대는 과적합 위험
        """)

        st.markdown("### 확장 아이디어")
        card("""
- **Two-Stage**: 3 vs 나머지 → {0,9,15} 재분류 → (선택) 0 vs {9,15} → 9 vs 15  
- **쌍대 전문가**(0↔9, 0↔15, 9↔15)를 **애매할 때만** 소프트 블렌딩  
- 클래스별 **bias/임계치** 후처리
        """)

PageRegistry.register(LDASVMPage)

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

