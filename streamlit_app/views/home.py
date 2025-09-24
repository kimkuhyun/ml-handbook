# streamlit_app/pages/home.py
from __future__ import annotations
import streamlit as st
from datetime import datetime
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card, hint

class HomePage(BasePage):
    title = "Home"
    slug = "home"
    icon = "🏠"

    def render(self) -> None:
        inject_global_style()

        st.title("📘 우리만의 AI 교과서")
        st.subheader("스마트 해운물류 x AI 미션 챌린지 — 이상신호 감지 기반 비정상 작동 진단")

        badges(["Algorithm", "Anomaly / Fault", "Tabular", "Multi-class Classification", "Metric: Macro-F1"])

        col1, col2 = st.columns([1.4, 1])
        with col1:
            st.markdown("### 🧭 배경")
            st.markdown("""
- 현장 장비는 **온도·압력·진동·전류** 등 여러 센서로 상태를 기록합니다.  
- 작은 이상 패턴을 놓치면 **불필요한 정지·품질 저하·안전 리스크**가 커집니다.  
- 이 프로젝트는 **센서 기반 표형 데이터**만으로 **정상/비정상 작동 유형**을 분류하는 **실전형 진단기**를 만드는 여정입니다.
- 도메인 의미(센서 종류)는 비공개인 **블랙박스 환경**에서, **순수 숫자 특징(X_01~X_52)**만으로 성능을 끌어올립니다.
            """)

        with col2:
            st.markdown("### 💰 대회/운영")
            st.markdown("""
- **주최**: 해양수산부  
- **주관**: 울산항만공사 / 한국정보산업연합회  
- **운영**: 데이콘  
- **상금 상태**: 본선 진출
            """)
            hint("목표: 현장에서 바로 쓸 수 있는 <b>신속·정확</b> 점검 도우미 만들기")

        st.markdown("---")

        st.markdown("### 🧪 데이터 한눈에")
        c1, c2 = st.columns(2)
        with c1:
            card("""
**파일 구성**
- `train.csv`: **ID**, **X_01 ~ X_52**, **target**  
- `test.csv`: **ID**, **X_01 ~ X_52**  
- `sample_submission.csv`: **ID**, **target** 형식 샘플

**중요 포인트**
- **각 행은 한 시점의 스냅샷** (타임스탬프/순서 정보 제공 X)  
- 센서/제어 신호가 **섞여 있지만 비식별화**되어 있음  
- 피처별 **스케일·분포가 제각각** → 전처리 중요  
- **target**: 21개 클래스(정상/비정상 유형 포함, 의미 비공개)
            """)

        with c2:
            card("""
**우리의 작업 기준**
- 입력: **수치형 52개 컬럼**  
- 전처리: **StandardScaler**(신경망/선형 계열), **상관/중요도 기반 Top-K 선택**  
- 모델: LightGBM, MLP, Blending, LDA→SVM(포커스 클래스) 등  
- 평가지표(학습/리더보드): **Macro-F1** (클래스 균형 관점에 유리)
            """)

        st.markdown("---")

        st.markdown("### 🏁 평가 & 리더보드")
        colA, colB = st.columns([1.2, 1])
        with colA:
            st.markdown("**리더보드 구성**")
            st.markdown("""
- **Metric**: Macro-F1  
- **Public score**: 테스트의 약 **30%**  
- **Private score**: 테스트 **100%** (대회 종료 후 공개)
            """)
            st.markdown("**심사 방식(요약)**")
            st.markdown("""
- 1차: **Private Score 100% 순위**  
- 2차: 상위 팀 **코드 검증**(재현성/규칙 준수) → **본선 진출 확정**
            """)

        with colB:
            st.markdown("**제출/규칙 핵심(요약)**")
            st.markdown("""
- **Python** 사용, **외부데이터 금지**  
- **사전학습 모델**: 공개 가중치 + 오픈 라이선스만 사용 가능  
- **API 모델 금지**: 외부 서버 호출형(OpenAI/Gemini 등) 불가, **로컬 실행**만  
- 코드/모델/환경 정보는 검증용으로 **재현 가능**하게 정리
            """)

        st.markdown("### 🗓️ 주요 일정 (KST)")
        s1, s2, s3 = st.columns([1,1,1])
        with s1:
            st.markdown("""
- 대회 기간: **2025-09-08 10:00 ~ 2025-10-02 10:00**  
- 팀 병합 마감: **2025-09-25 23:59**
            """)
        with s2:
            st.markdown("""
- 대회 종료: **2025-10-02 10:00**  
- 코드·PPT 제출 마감: **2025-10-10**
            """)
        with s3:
            st.markdown("""
- 코드 검증: **2025-10-13 ~ 2025-10-17**  
- 본선 발표: **2025-10-20 10:00**
            """)
        st.caption("※ 최종 순위는 Private 점수 및 코드 검증을 모두 통과해야 확정됩니다.")

        st.markdown("---")
        st.markdown("### 🎓 우리 프로젝트는 이렇게 봅니다")
        st.markdown("""
- **교과서 목표**: 모델을 단순 나열하지 않고, *왜 선택했는지 → 어떻게 전처리했는지 → 어떤 하이퍼를 썼는지 → 무엇이 어려웠는지 → 어떻게 확장할지*를 **짧고 명확**하게 기록합니다.  
- **모델별 페이지**: 각 모델은 **한 페이지**로, **중학생도 이해 가능한 어투**로 구성합니다.  
- **실전 지향**: 리더보드 점수뿐 아니라, **재현성·안정성·해석**을 함께 챙깁니다.
        """)

        st.markdown("### 🔗 시작하기")
        st.markdown("""
- 왼쪽 사이드바에서 **모델 페이지**를 선택하세요.  
- 추천 순서: **MLP(Top-30)** → **LightGBM** → **Blending** → **LDA→SVM(포커스 0/3/9/15)**  
- 각 페이지는 *모델 소개 → 왜 선택 → 전처리 → 하이퍼 → 결과 → 어려움 → 확장 아이디어* 순으로 구성되어 있습니다.
        """)

# 레지스트리 등록
PageRegistry.register(HomePage)

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

