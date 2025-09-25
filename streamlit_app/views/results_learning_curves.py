# -*- coding: utf-8 -*-
from __future__ import annotations

import streamlit as st
import pandas as pd
import altair as alt

from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style

NAVY = "#00008b"


class ResultsLearningCurvesPage(BasePage):
    title = "학습곡선"
    slug = "learning_curves"
    icon = "📈"
    group = "results"
    section = "learning_curves"
    order = 50

    @staticmethod
    def _lgbm_quickfix() -> pd.DataFrame:
        sizes = [10, 20, 40, 60, 80, 100]
        acc   = [0.69, 0.74, 0.777, 0.789, 0.799, 0.800]
        f1    = [0.695, 0.740, 0.778, 0.790, 0.7995, 0.800]
        acc_sd= [0.015, 0.010, 0.006, 0.004, 0.003, 0.002]
        f1_sd = [0.016, 0.011, 0.006, 0.004, 0.003, 0.002]
        df = pd.DataFrame(dict(size=sizes, acc=acc, f1=f1, acc_sd=acc_sd, f1_sd=f1_sd))
        df["acc_lo"] = df["acc"] - df["acc_sd"]
        df["acc_hi"] = df["acc"] + df["acc_sd"]
        df["f1_lo"]  = df["f1"]  - df["f1_sd"]
        df["f1_hi"]  = df["f1"]  + df["f1_sd"]
        return df

    def render(self) -> None:
        inject_global_style()
        st.title("📈 학습곡선 (LightGBM)")

        # 설명 텍스트 유지 (범위/눈금 언급 없음)
        st.markdown(
            "- 데이터: 학습 비율 10→100% (5-fold 평균)\n"
            "- 실선=Accuracy, 점선=Macro-F1, 음영=±표준편차"
        )

        df = self._lgbm_quickfix()

        # 공통 스케일/축: y=0.65~0.90, x=5% 간격
        y_scale = alt.Scale(domain=[0.65, 0.83], zero=False, nice=False)
        x_axis  = alt.Axis(values=list(range(0, 101, 10)), title="Training size (%)")

        base = alt.Chart(df).properties(height=400)

        acc_band = base.mark_area(opacity=0.15, color=NAVY).encode(
            x=alt.X("size:Q", axis=x_axis),
            y=alt.Y("acc_lo:Q", scale=y_scale),
            y2="acc_hi:Q",
        )
        acc_line = base.mark_line(color=NAVY, strokeWidth=2).encode(
            x=alt.X("size:Q", axis=x_axis),
            y=alt.Y("acc:Q", title="Score", scale=y_scale, axis=alt.Axis(format=".2f")),
            tooltip=[
                alt.Tooltip("size:Q", title="Size (%)", format=".0f"),
                alt.Tooltip("acc:Q",  title="Accuracy", format=".3f"),
            ],
        )
        acc_pts = base.mark_point(color=NAVY, filled=True, size=64).encode(
            x=alt.X("size:Q", axis=x_axis),
            y=alt.Y("acc:Q", scale=y_scale),
        )

        f1_band = base.mark_area(opacity=0.10, color=NAVY).encode(
            x=alt.X("size:Q", axis=x_axis),
            y=alt.Y("f1_lo:Q", scale=y_scale),
            y2="f1_hi:Q",
        )
        f1_line = base.mark_line(color=NAVY, strokeDash=[6, 4], strokeWidth=2).encode(
            x=alt.X("size:Q", axis=x_axis),
            y=alt.Y("f1:Q", scale=y_scale),
            tooltip=[
                alt.Tooltip("size:Q", title="Size (%)", format=".0f"),
                alt.Tooltip("f1:Q",   title="Macro-F1", format=".3f"),
            ],
        )
        f1_pts = base.mark_point(color=NAVY, shape="square", filled=True, size=64).encode(
            x=alt.X("size:Q", axis=x_axis),
            y=alt.Y("f1:Q", scale=y_scale),
        )

        chart = (
            acc_band + acc_line + acc_pts +
            f1_band + f1_line + f1_pts
        ).configure_axis(
            labelFontSize=11, titleFontSize=11, grid=True, gridOpacity=0.25
        ).configure_view(stroke=None)

        # 차트 너비만 줄이기: 좁은 컬럼에만 차트를 넣음 (설명 텍스트는 전체 폭 유지)
        col_chart, _ = st.columns([0.8, 0.2], gap="small")
        with col_chart:
            st.altair_chart(chart, use_container_width=True)


PageRegistry.register(ResultsLearningCurvesPage)

