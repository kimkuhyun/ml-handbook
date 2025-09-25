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


class PreprocessExperimentsPage(BasePage):
    title = "전처리 & 규제 실험"
    slug = "preprocess_experiments"
    icon = "🧪"
    group = "models"
    section = "전처리"
    order = 80

    @staticmethod
    def _decision_tree() -> pd.DataFrame:
        rows = [
            ("X","X","X","X","X",0.70615349,"-",""),
            ("O","X","X","X","X",0.70709464,"-",""),
            ("X","O","X","X","X",0.71076284,"-","{'max_depth': 100, 'min_samples_split': 20}"),
            ("O","X","min-max","X","X",0.70225894,"-",""),
            ("X","O","min-max","X","X",0.71076284,"-","{'max_depth': 100, 'min_samples_split': 20}"),
            ("O","X","standard","X","X",0.70214370,"-",""),
            ("X","O","standard","X","X",0.71076284,"-","{'max_depth': 100, 'min_samples_split': 20}"),
            ("X","X","X","2","X",0.25743258,"-",""),
            ("O","X","X","2","X",0.25273753,"-",""),
            ("X","O","X","2","X",0.29569025,"-","{'max_depth': 10, 'min_samples_split': 50}"),
            ("X","X","X","0.9","X",0.41069370,"-",""),
            ("O","X","X","0.9","X",0.40025354,"-",""),
            ("X","O","X","0.9","X",0.42383037,"-","{'max_depth': 50, 'min_samples_split': 50}"),
            ("O","X","X","X","O",0.70764757,"-",""),
            ("O","X","O","X","O",0.70810855,"-",""),
            ("X","O","O","X","O",0.71237612,"-","{'clf__max_depth': 100, 'clf__min_samples_split': 30, 'smote__k_neighbors': 5}"),
        ]
        return pd.DataFrame(rows, columns=["교차","gridCV","표준화","차원축소","smote","score","실제","param"])

    @staticmethod
    def _logreg() -> pd.DataFrame:
        rows = [
            ("X","X","X","X","X",0.41645540,"-",""),
            ("O","X","X","X","X",0.41442934,"-",""),
            ("X","O","X","X","X",0.56833372,"-",""),
        ]
        return pd.DataFrame(rows, columns=["교차","gridCV","표준화","차원축소","smote","score","실제","param"])

    def render(self) -> None:
        inject_global_style()
        st.title("전처리 & 규제 실험")

        # ===== Decision Tree =====
        dt = self._decision_tree()
        st.dataframe(dt, hide_index=True, width="stretch")

        d = dt.copy()
        d["score"] = pd.to_numeric(d["score"])
        d["실험"] = (
            d["gridCV"].astype(str) + " | " + d["표준화"].astype(str) + " | "
            + d["차원축소"].astype(str) + " | " + d["smote"].astype(str)
        )

        # y도메인 및 막대 기준선(y2)
        dom1 = ydomain(d, "score")
        d["baseline"] = dom1[0]
        yscale1 = alt.Scale(domain=dom1, zero=False, nice=False)

        bars1 = (
            alt.Chart(d)
            .mark_bar(color=ALT_COLOR, clip=True)
            .encode(
                x=alt.X("실험:N", title=None, sort="-y", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("score:Q", title="score", scale=yscale1, axis=alt.Axis(format=".3f")),
                y2="baseline:Q",
                tooltip=["교차","gridCV","표준화","차원축소","smote","score","param"],
            )
            .properties(height=320)
        )

        labels1 = (
            alt.Chart(d)
            .mark_text(align="center", baseline="bottom", dy=-5, color=ALT_COLOR)
            .encode(
                x=alt.X("실험:N", sort="-y", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("score:Q", scale=yscale1),
                text=alt.Text("score:Q", format=".4f"),
            )
            .properties(height=320)
        )

        st.altair_chart(bars1 + labels1, use_container_width=True)

        # ===== Logistic Regression =====
        lr = self._logreg()
        st.dataframe(lr, hide_index=True, width="stretch")

        d2 = lr.copy()
        d2["score"] = pd.to_numeric(d2["score"])
        # 하나의 축 라벨만 쓰면 중복이 합쳐질 수 있어 실험 라벨을 간단히 구성
        d2["실험"] = d2["gridCV"].astype(str) + " | " + d2["표준화"].astype(str)

        dom2 = ydomain(d2, "score")
        d2["baseline"] = dom2[0]
        yscale2 = alt.Scale(domain=dom2, zero=False, nice=False)

        bars2 = (
            alt.Chart(d2)
            .mark_bar(color=ALT_COLOR, clip=True)
            .encode(
                x=alt.X("실험:N", title=None, sort="-y", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("score:Q", title="score", scale=yscale2, axis=alt.Axis(format=".3f")),
                y2="baseline:Q",
                tooltip=["교차","gridCV","표준화","차원축소","smote","score","param"],
            )
            .properties(height=320)
        )

        labels2 = (
            alt.Chart(d2)
            .mark_text(align="center", baseline="bottom", dy=-5, color=ALT_COLOR)
            .encode(
                x=alt.X("실험:N", sort="-y", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("score:Q", scale=yscale2),
                text=alt.Text("score:Q", format=".4f"),
            )
            .properties(height=320)
        )

        st.altair_chart(bars2 + labels2, use_container_width=True)


PageRegistry.register(PreprocessExperimentsPage)

