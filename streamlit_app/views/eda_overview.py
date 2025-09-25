# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import streamlit as st

from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style

ROOT = Path(__file__).resolve().parents[1]  # streamlit_app

def _img(name: str, caption: str = "", width: int = 820):
    path = ROOT / "assets" / "eda" / name
    st.image(str(path), caption=caption, width=width)

class EDAOverviewPage(BasePage):
    title = "개요 & 데이터 소개"
    slug = "eda_overview"
    icon = "📘"
    group = "eda"      # ← 사이드바 상단 그룹
    section = "EDA"    # 정렬용 라벨
    order = 10

    def render(self) -> None:
        inject_global_style()
        st.title("📝 EDA (Exploratory Data Analysis)")

        st.markdown("""
## 📑 목차
1. 개요 (Overview)  
   - 분석 목적  
   - 데이터 소개  
""")

        st.markdown("""
## 개요 (Overview)

### 분석 목적
주어진 데이터를 기반으로 효율적인 분류 모델을 구축하기 위해, 데이터 전처리 및 피처 엔지니어링 방향을 결정하기 위함.

- 결측치, 이상치, 중복 등 데이터 품질 문제를 파악  
- 타겟 분포 및 피처 특성을 확인하여 학습 전략 수립  
- Train/Test 분포 차이를 점검하여 일반화 성능 확보  

### 데이터 소개
**train.csv**
- ID : 샘플별 고유 ID  
- X_01 ~ X_52 : 센서/제어 신호가 혼재되어 있으나, 구체적 매핑은 비공개. 스케일·분포는 피처별로 상이할 수 있음  
- target : 고장 진단 target (각 라벨의 의미는 비공개)

**test.csv**
- ID : 샘플별 고유 ID  
- X_01 ~ X_52

**sample_submission.csv**
- ID : 샘플별 고유 ID  
- target : 고장 진단 target

※ 각 행은 동일 시점의 상태를 의미하며, 타임스탬프·시퀀스 정보는 제공되지 않음.
""")

PageRegistry.register(EDAOverviewPage)

