# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import streamlit as st
import pandas as pd
import altair as alt

from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style

ALT_COLOR = "#00008b"


class ResultsStackingVariantsPage(BasePage):
    title = "스태킹 변종"
    slug = "results_stacking_variants"
    icon = "🧱"
    group = "results"
    section = "stacking"

    @staticmethod
    def _variants() -> pd.DataFrame:
        rows = [
            ("2-base (XGB+MLP, basic)", None, 0.8628, ""),
            ("2-base (bagging, C=5, soft OFF)", 0.8656, 0.8671, ""),
            ("3-base (XGB+MLP+ET)", None, 0.8648, ""),
            ("3-base (XGB+MLP+LR)", None, 0.8641, ""),
            ("4-base (XGB+MLP+ET+LR)", None, 0.8657, ""),
            ("4-base (soft ON)", None, 0.8680, ""),
            ("4-base (bagging, C=5, soft OFF)", 0.8667, 0.8681, ""),
            ("Blend 0.45·4b + 0.55·2b", 0.8675, None, ""),
        ]
        return pd.DataFrame(rows, columns=["조합", "OOF Accuracy", "OOF Macro-F1", "메모"])

    def render(self) -> None:
        inject_global_style()
        st.title("🧱 스태킹/블렌딩 변종")

        # 표: 원본 그대로
        df = self._variants()
        st.dataframe(df, hide_index=True, width="stretch")

        # ===== Macro-F1만 안전하게 그리기 =====
        d = (
            df.rename(columns={"OOF Macro-F1": "F1", "OOF Accuracy": "Acc"})
              .assign(F1=lambda x: pd.to_numeric(x["F1"], errors="coerce"),
                      Acc=lambda x: pd.to_numeric(x["Acc"], errors="coerce"))
              .dropna(subset=["F1"])
              .copy()
        )
        if d.empty:
            st.info("표시할 Macro-F1 데이터가 없습니다.")
            return

        # x 라벨 단축: 맨 앞의 '숫자-base ' 제거
        def strip_x_base(s: str) -> str:
            return re.sub(r"^\d+-base\s*", "", s)

        d["Label"] = d["조합"].apply(strip_x_base)
        d["baseline"] = 0.80  # 막대 기준선(y2) 고정
        d = d.sort_values("F1", ascending=False)

        y_scale = alt.Scale(domain=[0.80, 0.90], zero=False, nice=False)

        # 막대: y=F1, y2=baseline(0.80) → 그리드 안에서만 그려짐
        chart = (
            alt.Chart(d)
            .mark_bar(color=ALT_COLOR, clip=True)
            .encode(
                x=alt.X("Label:N", sort="-y", axis=alt.Axis(labelAngle=0), title=None),
                y=alt.Y("F1:Q", title="OOF Macro-F1",
                        scale=y_scale, axis=alt.Axis(format=".3f")),
                y2="baseline:Q",
                tooltip=[
                    alt.Tooltip("조합:N", title="조합(원본)"),
                    alt.Tooltip("Acc:Q", title="OOF Accuracy", format=".4f"),
                    alt.Tooltip("F1:Q",  title="OOF Macro-F1", format=".4f"),
                    alt.Tooltip("메모:N",  title="메모"),
                ],
            )
            .properties(height=280)
            .configure_axis(labelFontSize=11, titleFontSize=11, grid=True, gridOpacity=0.25)
            .configure_view(stroke=None)
        )

        st.altair_chart(chart, use_container_width=True)


PageRegistry.register(ResultsStackingVariantsPage)

