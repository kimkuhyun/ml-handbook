# streamlit_app/pages/mlp.py
from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card, hint

class MLPPage(BasePage):
    title = "MLP (Top-30)"
    slug = "mlp"
    icon = "🧠"
    group = "models"
    section = "모델"
    order = 30

    def render(self) -> None:
        inject_global_style()
        st.title("🧠 MLP (Top-30 Features)")
        badges(["Neural Network", "Tabular", "Nonlinear", "Standardization", "Top-30"])

        st.markdown("### 이 모델은 뭘까?")
        st.markdown("""
- MLP는 ‘완전연결 신경망’이에요. 여러 층을 거치며 데이터를 점점 똑똑하게 바꿔요.  
- 직선으로 못 나누는 **복잡한 경계**를 배울 수 있어요.  
- 숫자의 **스케일(크기)**에 민감해서 **StandardScaler**가 중요해요.  
- 너무 복잡해지면 외우듯 학습(과적합)할 수 있어 **적당한 규제**가 필요해요.
        """)

        st.markdown("### 왜 선택했나")
        st.markdown("""
- 우리 데이터는 비선형 패턴이 있고, **Top-30 중요 특성**으로 잡음을 줄였더니 성능이 더 좋아졌어요.  
- 신경망의 표현력이 이런 상황에 잘 맞았어요.
        """)

        st.markdown("### 전처리")
        st.markdown("""
- `StandardScaler`(폴드 안에서만 fit), 상관 높은 특성 정리, **Top-30 특성 선택**  
- 누수 방지를 위해 모든 전처리는 **train-fold 기준**으로만 학습
        """)

        st.markdown("### 하이퍼파라미터(예시)")
        card("""
- 구조: Dense(384, ReLU) × 3 → Dense(21, Softmax)  
- 규제: Dropout 0.4, Weight Decay(L2)=1e-4  
- 학습: AdamW(lr=1e-3), batch 128~256, epochs 60~120, EarlyStopping  
- 보강: **seed 배깅(3회)** → 확률 평균(안정성↑)
        """)

        st.markdown("### 결과(5-Fold OOF)")
        card("""
- 52 특성: **Accuracy 0.8534 / Macro-F1 0.8563**  
- **Top-30 특성**: **Accuracy ≈ 0.861 / Macro-F1 ≈ 0.861**  ← 단일 최고
        """)

        st.markdown("### 어려웠던 점")
        st.markdown("""
- 스케일링을 빼먹으면 성능 급락  
- Dropout/학습률 조절이 까다로움  
- **0/9/15** 같은 헷갈리는 클래스는 여전히 어려움
        """)

        st.markdown("### 확장 아이디어")
        card("""
- **Temperature scaling + 클래스별 bias**로 확률 보정(미세 상승)  
- seed 배깅 확대, Cosine LR 스케줄로 안정성↑  
- {0,9,15} 전용 **작은 보조 모델**(게이팅) 추가
        """)

        st.subheader("📚 참고: 실제 적용 논문")
        card("""
**MLP for Critical Infrastructure Anomaly Detection**

- 데이터: 유량·압력 등 센서 시계열 → 정형 특징.
- 모델: MLP + CUSUM.
- 결과: F1 80~90%, 오탐 적음.
- 의미: 단순 구조 + 통계 결합으로 실용성 높음.
        """)

PageRegistry.register(MLPPage)

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

