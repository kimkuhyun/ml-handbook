# streamlit_app/views/model_references.py
from __future__ import annotations
import streamlit as st
from streamlit_app.core.base import PageRegistry, BasePage
from streamlit_app.core.ui import inject_global_style, badges, card

class ModelReferencesPage(BasePage):
    title = "참고 논문 모음"
    slug = "model_references"
    icon = "📚"
    group = "models"   # 상단 그룹: 모델
    section = "모델"    # 좌측 섹션: 모델
    order = 110

    def render(self) -> None:
        inject_global_style()
        st.title(f"{self.icon} {self.title}")
        badges(["GBDT", "딥/탭러", "AutoML", "공정/고장탐지"])

        # GBDT 계열
        st.header("🌳 GBDT 계열")
        with st.expander("LightGBM: A Highly Efficient Gradient Boosting Decision Tree — Guolin Ke", expanded=False):
            st.markdown("""
- 부제: 고속·고정확 GBDT  
- 목적: 대용량·고차원 데이터에서 학습/추론 가속  
- 설명: 히스토그램 기반·리프-와이즈 성장, GOSS/EFB로 메모리·시간 절감하며 정확도 유지.
            """)
        with st.expander("XGBoost: A Scalable Tree Boosting System — Tianqi Chen", expanded=False):
            st.markdown("""
- 부제: 확장성 최적화 트리 부스팅  
- 목적: 분산/병렬 최적화로 대규모 데이터 효율 학습  
- 설명: 희소성 인식 분할·정규화·분산 학습을 결합해 빠르고 견고한 성능 제공.
            """)
        with st.expander("CatBoost: Unbiased Boosting with Categorical Features — Liudmila Prokhorenkova", expanded=False):
            st.markdown("""
- 부제: 범주형 친화 부스팅  
- 목적: 카테고리 처리 편향 최소화·일반화 향상  
- 설명: Ordered boosting과 타깃 통계 인코딩으로 누설/편향을 줄여 실전 성능 개선.
            """)
        with st.expander("Why do tree-based models still outperform deep learning on tabular data? — Léo Grinsztajn", expanded=False):
            st.markdown("""
- 부제: 표형 데이터에서 트리 우세성 분석  
- 목적: 언제/왜 GBDT가 유리한지 근거 제시  
- 설명: 45개 데이터셋 벤치마크로 중·소규모 표형에서 트리가 일관되게 우수함을 보고.
            """)

        # 딥/탭러 계열
        st.header("🧠 딥/탭러 계열")
        with st.expander("TabNet: Attentive Interpretable Tabular Learning — Sercan Ö. Arik", expanded=False):
            st.markdown("""
- 부제: 주의집중 기반 해석 가능한 표형 학습  
- 목적: 중요 피처 선택으로 정확도·설명력 동시 달성  
- 설명: 스텝별 마스크로 특성 선택/억제, sparsity 가중으로 효율적 학습과 국소적 해석 제공.
            """)
        with st.expander("Neural Oblivious Decision Ensembles — Sergei Popov", expanded=False):
            st.markdown("""
- 부제: 미분가능 트리 앙상블  
- 목적: 트리 귀납편향 + 딥러닝 최적화 결합  
- 설명: ODT를 신경망으로 구현해 엔드-투-엔드 학습과 강한 표형 성능을 양립.
            """)

        # AutoML
        st.header("🤖 AutoML")
        with st.expander("AutoGluon-Tabular: Robust and Accurate AutoML for Structured Data — Nick Erickson", expanded=False):
            st.markdown("""
- 부제: 표형 데이터용 스태킹·배깅 AutoML  
- 목적: 수동 튜닝 없이 높은 정확도/재현성 확보  
- 설명: 다계층 스태킹·반복 배깅·자동 전처리로 분류/회귀 성능을 안정적으로 끌어올림.
            """)

        # 공정/고장 탐지 특화
        st.header("🏭 공정/고장 탐지 특화")
        with st.expander("Fault Detection and Diagnosis in Tennessee Eastman Process with Deep Autoencoder — Zhongying Xiao", expanded=False):
            st.markdown("""
- 부제: 공정 이상·고장 탐지용 딥 오토인코더  
- 목적: PCA 대비 탐지력↑·원인분석성 확보  
- 설명: 정상 재구성오차 기반 탐지 + 변수 중요도로 다양한 Fault에서 성능 향상.
            """)
        with st.expander("Deep Compression of Neural Networks for Fault Detection on TEP — Mingxuan Li", expanded=False):
            st.markdown("""
- 부제: 실시간 고장탐지용 모델 경량화  
- 목적: 정확도 유지하며 배포/추론 비용 절감  
- 설명: 프루닝·클러스터링·양자화로 대폭 압축하면서 TEP 분류 정확도 유지.
            """)
        with st.expander("Condition Monitoring & Multi-Fault Classification of Hydraulic Systems — C. Yildirim", expanded=False):
            st.markdown("""
- 부제: 함수형 데이터 기반 다중 고장 분류  
- 목적: 센서 시계열을 함수 표현으로 변환해 진단력 향상  
- 설명: MFPCA로 신호를 저차표현화하고 상태감시·다중 고장 분류 정확도 개선.
            """)

PageRegistry.register(ModelReferencesPage)

