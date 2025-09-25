from __future__ import annotations

import streamlit as st
import pandas as pd
import altair as alt

from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style

ALT_COLOR = "#00008b"


def ydomain(df: pd.DataFrame, col: str) -> list[float]:
    # (참고) 지금은 사용하지 않지만, 남겨둠
    vals = pd.to_numeric(df[col])
    lo, hi = float(vals.min()), float(vals.max())
    span = max(hi - lo, 1e-9)
    pad = max(0.002, span * 0.20)
    lo, hi = max(0.0, lo - pad), min(1.0, hi + pad)
    if hi - lo < 0.01:
        mid = (lo + hi) / 2
        lo, hi = max(0.0, mid - 0.01), min(1.0, mid + 0.01)
    return [lo, hi]


class ResultsOverviewPage(BasePage):
    title = "결과 개요"
    slug = "results_overview"
    icon = "📊"
    group = "results"
    section = "overview"

    @staticmethod
    def _summary() -> pd.DataFrame:
        rows = [
            ("Logistic Regression", 0.584, 0.576, ""),
            ("Random Forest", 0.771, 0.773, ""),
            ("XGBoost", 0.795, 0.796, ""),
            ("LightGBM", 0.801, 0.805, ""),
            ("MLP", 0.800, 0.797, ""),
            ("Stacking(LGBM+XGB+MLP→LR)", 0.820, 0.818, ""),
            ("Stage-1 Best (XGB+MLP→LR)", 0.8559, 0.8563, ""),
        ]
        return pd.DataFrame(rows, columns=["이름", "Accuracy", "Macro-F1", "메모"])

    def render(self) -> None:
        inject_global_style()
        st.title("📊 결과 개요")

        df = self._summary()

        # 표는 expander 안에
        st.dataframe(df, hide_index=True, width="stretch")

        # ---- Macro-F1만 차트로 (두 개 항목만 축 라벨 단축) ----
        d = df.copy()
        short_map = {
            "Stacking(LGBM+XGB+MLP→LR)": "Stack (L/X/M→LR)",
            "Stage-1 Best (XGB+MLP→LR)": "Stg1 Best (X+M→LR)",
        }
        d["Label"] = d["이름"].replace(short_map)
        d = d.sort_values("Macro-F1", ascending=False)
        d["Macro-F1"] = pd.to_numeric(d["Macro-F1"])

        chart = (
            alt.Chart(d)
            .mark_bar(color=ALT_COLOR)
            .encode(
                x=alt.X("Label:N", sort="-y", axis=alt.Axis(labelAngle=0), title=None),
                y=alt.Y("Macro-F1:Q", title="Macro-F1"),
                tooltip=["이름", "Accuracy", "Macro-F1", "메모"],  # 툴팁엔 원래 전체 이름 노출
            )
            .properties(height=340)  # ← 세로로 조금 더 길게
        )

        st.altair_chart(chart, use_container_width=True)


PageRegistry.register(ResultsOverviewPage)

