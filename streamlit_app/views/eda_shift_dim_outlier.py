# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import streamlit as st

from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style

ROOT = Path(__file__).resolve().parents[1]

def _img(name: str, caption: str = "", width: int = 820):
    st.image(str(ROOT / "assets" / "eda" / name), caption=caption, width=width)

class EDAShiftDimOutlierPage(BasePage):
    title = "Train–Test 비교 · 차원축소 · 아웃라이어 · 결론"
    slug = "eda_shift_dim_outlier"
    icon = "🧭"
    group = "eda"
    section = "EDA"
    order = 40

    def render(self) -> None:
        inject_global_style()
        st.title("Train–Test 비교 · 차원 축소 시각화 · 아웃라이어 · 결론")

        st.markdown("""
## Train-Test 비교 (Train vs Test Comparison)""")
        _img("5_feature_distribution_train_test_top6.png", "Train-Test 분포 비교 (상위 6개)", width=1000)
        st.markdown("""
### 관찰 포인트
1. 대부분 분포는 유사 (train/test 차이 적음)  
2. 일부(X_11, X_19, X_37, X_40) → 극단값 존재  
3. 일부(X_01, X_02) → train/test 분포 차이 → 데이터 쉬프트 가능성

### 데이터 쉬프트 탐지
- Train/Test 합쳐서 `is_train` 분류  
- 분류 성능 AUC = **0.7454**  
- train/test 차이 있음 → 일반화 성능에 영향 가능  
- 불안정 피처 제거/보정 필요
""")
        _img("6_data_shift_detection_top20.png", "데이터 쉬프트 탐지(Top-20)", width=1000)

        st.markdown("""
## 차원 축소 기반 시각화 (Dimensionality Reduction)

### PCA""")
        _img("7_PCA_2d_visualization.png", "PCA 2D", width=1000)
        st.markdown("""
- 분산 큰 일부 클래스만 분리  
- 대부분 클래스는 섞여 있음  
- 선형 모델 단독으로는 한계

### t-SNE""")
        _img("8_t-sne_2d_visualization.png", "t-SNE 2D", width=1000)
        st.markdown("""
- 여러 군집이 원형으로 분리  
- 일부 클래스 구분 가능, 일부는 섞임  
- 국소 구조 파악에 유리

### UMAP""")
        _img("9_umap.png", "UMAP 2D", width=1000)
        st.markdown("""
- 군집이 명확하게 분리  
- 전역+국소 구조 모두 반영  
- 실제로 분리 가능한 신호 존재
""")

        st.markdown("""
## 아웃라이어 탐지 (Outlier Detection)""")
        _img("outlier_scatter.png","outlier 산점도", width=1000)
        _img("outlier_barplot.png","outlier 바플롯", width=1000)
        st.markdown("""
### 결과
- IQR: **13,405개** (과검출 가능)  
- Z-score: **5,718개** (비정규 분포 시사)  
- IsolationForest: **217개** (실질 이상치 가능성 높음)

### 종합 판단
- IQR/Z-score → 과검출 → 참고용  
- IsolationForest → 안정적, 실제 노이즈 가능성 높음  
- Outlier 제거 전략:
  1) IsolationForest 검출치 제거 (안정적)  
  2) IQR/Z-score 교차된 샘플 제거 (보수적)
""")

        st.markdown("""
## ✅ 최종 결론
- **데이터 품질 전반적으로 양호**  
- 일부 피처(X_01, X_09, X_11, X_19, X_20, X_37, X_40) → 제거/보정 필요  
- Train/Test 분포 전반적 유사, 일부 쉬프트 존재 (AUC=0.7454)  
- 비선형 모델(트리 기반, 앙상블, 딥러닝) 적합  
- Outlier 처리: IsolationForest 중심으로 적용 권장
""")

PageRegistry.register(EDAShiftDimOutlierPage)

