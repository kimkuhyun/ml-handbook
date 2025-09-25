# -*- coding: utf-8 -*-
from __future__ import annotations

import streamlit as st
import pandas as pd
import altair as alt

from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style

ALT_COLOR = "#00008b"


def ydomain(df: pd.DataFrame, col: str) -> list[float]:
    vals = pd.to_numeric(df[col])
    lo, hi = float(vals.min()), float(vals.max())
    span = max(hi - lo, 1e-9)
    pad = max(0.002, span * 0.20)
    lo, hi = max(0.0, lo - pad), min(1.0, hi + pad)
    if hi - lo < 0.01:
        mid = (lo + hi) / 2
        lo, hi = max(0.0, mid - 0.01), min(1.0, mid + 0.01)
    return [lo, hi]


class PreprocessIQRPage(BasePage):
    title = "IQR"
    slug = "preprocess_iqr"
    icon = "🧹"
    group = "models"
    section = "전처리"

    @staticmethod
    def _iqr_tbl() -> pd.DataFrame:
        rows = [
            ("1.5","TOP30",0.4789),
            ("2","TOP30",0.5201),
            ("2.5","TOP30",0.5995),
            ("3","TOP30",0.6696),
            ("1.5","ALL",0.4934),
            ("2","ALL",0.5220),
            ("2.5","ALL",0.5957),
            ("3","ALL",0.6504),
            ("None","TOP30",0.8536),
            ("None","ALL",0.8542),
        ]
        return pd.DataFrame(rows, columns=["IQR","mode","accuracy"])

    def render(self) -> None:
        inject_global_style()
        st.title("🧹 IQR(아웃라이어 클리핑)")

        df = self._iqr_tbl()
        # 표는 expander로 접기
        with st.expander("📋 표 보기", expanded=False):
            st.dataframe(df, hide_index=True, width="stretch")

        for mode in ["TOP30", "ALL"]:
            d = df[df["mode"] == mode].copy()
            d["accuracy"] = pd.to_numeric(d["accuracy"])
            d["IQR"] = pd.Categorical(
                d["IQR"], categories=["1.5", "2", "2.5", "3", "None"], ordered=True
            )
            d = d.sort_values("IQR")

            # y도메인 하한을 막대 기준선으로 사용 → 그리드 밖으로 안 튐
            dom = ydomain(d, "accuracy")
            y0 = dom[0]
            d["baseline"] = y0
            yscale = alt.Scale(domain=dom, zero=False, nice=False)

            bars = (
                alt.Chart(d)
                .mark_bar(color=ALT_COLOR, clip=True)
                .encode(
                    x=alt.X("IQR:N", title="IQR factor", axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("accuracy:Q", title="Accuracy", scale=yscale),
                    y2="baseline:Q",
                    tooltip=["IQR", "mode", "accuracy"],
                )
                .properties(height=320)  # ← 높이 320px
            )

            labels = (
                alt.Chart(d)
                .mark_text(align="center", baseline="bottom", dy=-5, color=ALT_COLOR)
                .encode(
                    x=alt.X("IQR:N", axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("accuracy:Q", scale=yscale),
                    text=alt.Text("accuracy:Q", format=".4f"),
                )
                .properties(height=320)  # ← 높이 320px
            )

            # 가운데 정렬 & 크게 보이는 타이틀
            title_str = "Top30" if mode == "TOP30" else "All"
            chart = (bars + labels).properties(
                title=alt.TitleParams(text=title_str, anchor="middle", fontSize=16)
            )

            st.altair_chart(chart, use_container_width=True)


PageRegistry.register(PreprocessIQRPage)

