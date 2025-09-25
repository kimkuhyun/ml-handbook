# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import streamlit as st

from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style

ROOT = Path(__file__).resolve().parents[1]

def _img(name: str, caption: str = "", width: int = 820):
    st.image(str(ROOT / "assets" / "eda" / name), caption=caption, width=width)

class EDAFeaturesCorrPage(BasePage):
    title = "피처 탐색 & 상관관계"
    slug = "eda_features_corr"
    icon = "🔬"
    group = "eda"
    section = "EDA"
    order = 30

    def render(self) -> None:
        inject_global_style()
        st.title("피처 탐색 · 상관관계 분석")

        st.markdown("""
## 피처 탐색 (Feature Exploration)

### 📊 기본 통계량
| Feature | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|---------|------:|-----:|----:|----:|----:|----:|----:|----:|
| X_01 | 21693.0 | 0.017989 | 0.004794 | -0.003 | 0.015000 | 0.018000 | 0.021000 | 0.037 |
| X_02 | 21693.0 | 0.258061 | 0.064098 | 0.000 | 0.244223 | 0.247364 | 0.251002 | 1.000 |
| X_03 | 21693.0 | 0.533411 | 0.057962 | 0.000 | 0.510506 | 0.535398 | 0.560651 | 1.000 |
| X_04 | 21693.0 | 0.510776 | 0.082500 | 0.000 | 0.507370 | 0.520045 | 0.533285 | 1.000 |
| X_05 | 21693.0 | 0.421508 | 0.168995 | 0.000 | 0.363789 | 0.378157 | 0.393900 | 1.000 |
| ...  |   ...   |   ...    |   ...    |  ...  |   ...    |   ...    |   ...    |  ...  |
| X_51 | 21693.0 | 0.491238 | 0.103482 | 0.000 | 0.450000 | 0.480000 | 0.520000 | 1.000 |
| X_52 | 21693.0 | 0.505871 | 0.097134 | 0.000 | 0.470000 | 0.500000 | 0.540000 | 1.000 |

### 피처 분포 시각화
- 대부분 0~1 값 → 정규화된 값  
- 뾰족하게 몰린 분포 많음 → 정보량 적음  
- 일부 넓거나 이산적인 분포 존재 → 모델에서 유용할 수 있음

### 정보량에 따른 피처 분류
- X_01: 평균 0.018, 거의 상수 → 제거 후보  
- X_05: 분산 크고 분포 넓음 → 핵심 피처 가능  
- 전체적으로 값 범위 0~1 → 이미 정규화된 상태일 가능성

### 그룹별 분류
1) **상수형/편향된 피처**: X_01, X_09, X_11, X_19, X_20, X_37, X_40 → 제거 가능  
2) **정규/균등 분포 피처**: X_05, X_18, X_45 → 중요 피처 가능  
3) **이산형 피처**: X_10, X_19, X_37, X_40 → 카테고리형 처리 고려  
4) **분산 낮은 피처**: X_02 ~ X_08 → 단독 영향 적으나 조합 의미 가능
""")
        _img("2_feature_distribution_1_train_test_top6.png", "피처 분포 (상위 6개)", width=1000)

        st.markdown("""
## 상관관계 분석 (Correlation Analysis)

### 전체 히트맵
- 대부분 상관 낮음  
- 일부 피처는 중복 정보 존재 (다중공선성 가능)  
- 타깃과 뚜렷한 상관 없음 → 단일 피처로는 한계

### Target vs Feature 상관계수
- X_28, X_48: 음의 상관 (~ -0.3)  
- X_33, X_19: 양의 상관 (~ +0.2)  
- 전체적으로 절댓값 ≤ 0.3 → 단일 피처 예측력 낮음 → 트리/비선형 모델 필요
""")
        _img("3_feture_exploation.png", "피처 간 상관 히트맵", width=1000)
        _img("4_feature_correlation.png", "Target vs Feature 상관", width=1000)

PageRegistry.register(EDAFeaturesCorrPage)

