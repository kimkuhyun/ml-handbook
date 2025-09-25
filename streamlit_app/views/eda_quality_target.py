# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import streamlit as st

from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style

ROOT = Path(__file__).resolve().parents[1]

def _img(name: str, caption: str = "", width: int = 820):
    st.image(str(ROOT / "assets" / "eda" / name), caption=caption, width=width)

class EDAQualityTargetPage(BasePage):
    title = "구조/품질 점검 & 타겟"
    slug = "eda_quality_target"
    icon = "🧩"
    group = "eda"
    section = "EDA"
    order = 20

    def render(self) -> None:
        inject_global_style()
        st.title("데이터 구조 및 품질 점검 · 타겟 변수 분석")

        st.markdown("""
## 데이터 구조 및 품질 점검 (Data Structure & Quality Check)

### 📂 train.csv
- 크기: (21693, 54)  
- 컬럼: `ID`, `X_01 ~ X_52`, `target`  
- `target`: 정답 (int64, 범주형 레이블)  
- 결측치 없음

### 📂 test.csv
- 크기: (15004, 53)  
- 컬럼: `ID`, `X_01 ~ X_52`  
- 결측치 없음

### 📂 sample_submission.csv
- 크기: (15004, 2)  
- 컬럼: `ID`, `target`  
- 제출 양식 확인용

#### 🟦 Train 데이터
| Feature | Null Count |
|---------|------------|
| X_01    | 0 |
| X_02    | 0 |
| X_03    | 0 |
| ...     | ... |
| X_51    | 0 |
| X_52    | 0 |

#### 🟧 Test 데이터
| Feature | Null Count |
|---------|------------|
| X_01    | 0 |
| X_02    | 0 |
| X_03    | 0 |
| ...     | ... |
| X_51    | 0 |
| X_52    | 0 |
""")

        st.markdown("""
## 타겟 변수 분석 (Target Analysis)

### 타겟 분포 확인
- 각 클래스가 **동일한 개수(1033개)**로 분포  
- → **완전히 균형 잡힌 다중분류 데이터셋**  
- 클래스 불균형 문제 고려 불필요
""")
        _img("1_target_disturibution.png", "타겟 분포", width=1000)

PageRegistry.register(EDAQualityTargetPage)

