# streamlit_app/views/results_postprocess.py
from __future__ import annotations
import streamlit as st
import pandas as pd
import altair as alt

from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

ALT_COLOR = "#00008b"

class ResultsPostprocessPage(BasePage):
    title = "후처리 (디코딩) 결과"
    slug = "results_postprocess"
    icon = "🧩"
    group = "results"
    section = "postprocess"

    def _ranking(self) -> pd.DataFrame:
        rows = [
            ["Viterbi (free + A) — 튠", 0.7963, 0.8023, "α=2.0, β=0.05 (게이팅 동일 지표)"],
            ["Viterbi (free + A) — 기본", 0.7937, 0.7998, "전이행렬 A 학습"],
            ["Potts(λ=0.244)", 0.7935, 0.7998, "이웃 동일라벨 가중"],
            ["Potts(λ=0.122)", 0.7935, 0.7998, ""],
            ["Potts(λ=0.061)", 0.7928, 0.7992, ""],
            ["Base argmax", 0.7928, 0.7991, "후처리 없음"],
            ["Potts(λ=0.367)", 0.7926, 0.7990, ""],
            ["Potts(λ=0.489)", 0.7921, 0.7988, ""],
        ]
        return pd.DataFrame([{"방법":r[0],"Accuracy":r[1],"Macro-F1":r[2],"메모":r[3]} for r in rows])

    def render(self) -> None:
        inject_global_style()
        st.title("🧩 후처리 (디코딩) 결과")
        badges(["Viterbi / Potts", "수직 막대", "네이비 컬러"])

        df = self._ranking()
        st.dataframe(df, use_container_width=True, hide_index=True)

        col1, col2 = st.columns(2)
        with col1:
            d = df.sort_values("Accuracy", ascending=False)
            chart = alt.Chart(d).mark_bar().encode(
                x=alt.X("방법:N", title=None, sort=d["방법"].tolist()),
                y=alt.Y("Accuracy:Q", title="Accuracy"),
                tooltip=list(df.columns),
                color=alt.value(ALT_COLOR),
            ).properties(height=360)
            st.altair_chart(chart, use_container_width=True)

        with col2:
            d = df.sort_values("Macro-F1", ascending=False)
            chart = alt.Chart(d).mark_bar().encode(
                x=alt.X("방법:N", title=None, sort=d["방법"].tolist()),
                y=alt.Y("Macro-F1:Q", title="Macro-F1"),
                tooltip=list(df.columns),
                color=alt.value(ALT_COLOR),
            ).properties(height=360)
            st.altair_chart(chart, use_container_width=True)

        card("- **Viterbi (free+A, 튠)**가 베이스 대비 **소폭↑**\n"
             "- 강한 제약(Adjacent/Monotone)은 성능 급락 → 제외")
PageRegistry.register(ResultsPostprocessPage)

