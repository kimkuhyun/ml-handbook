# streamlit_app/views/results_stage.py
from __future__ import annotations
import streamlit as st
import pandas as pd
import altair as alt

from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style, badges, card

ALT_COLOR = "#00008b"

# 전문가 모델명 단축(축 라벨용)
_ABBR = {
    "Triplet-Hardest": "Tri-H",
    "Triplet-BatchAll": "Tri-BA",
    "SupCon": "SupCon",
    "SupCon+CE": "SC+CE",
    "SupCon (balanced)": "SC (b)",
    "SupCon+CE (balanced)": "SC+CE (b)",
}
def short_expert(name: str) -> str:
    if name in _ABBR:
        return _ABBR[name]
    s = name.replace(" ", "")
    return s if len(s) <= 10 else (s[:9] + "…")


class ResultsStagePage(BasePage):
    title = "Stage-1 / 2-Stage 결과"
    slug = "results_stage"
    icon = "🧩"
    group = "results"
    section = "results"
    order = 30

    def _stage1(self) -> pd.DataFrame:
        return pd.DataFrame([{
            "구분":"Stage-1",
            "모델/조합":"XGB + MLP 스태킹 + 로지스틱 메타",
            "Accuracy":0.8559,
            "Macro-F1":0.8563,
            "코멘트":"현재 베스트, 안정적",
        }])

    def _experts(self) -> pd.DataFrame:
        rows = [
            ["Triplet-Hardest",0.2882,0.2817,"랜덤(0.25)보다 약간"],
            ["Triplet-BatchAll",0.4189,0.4157,"SupCon 다음"],
            ["SupCon",0.4320,0.4235,"가장 높지만 한계"],
            ["SupCon+CE",0.2502,0.2443,"거의 랜덤"],
            ["SupCon (balanced)",0.4102,0.4030,"약간 낮음"],
            ["SupCon+CE (balanced)",0.2982,0.2911,"조금 나음"],
        ]
        return pd.DataFrame([{
            "전문가모델":r[0], "Accuracy":r[1], "Macro-F1":r[2], "메모":r[3]
        } for r in rows])

    def _two_stage(self) -> pd.DataFrame:
        rows = [
            ["무조건 Stage-2 덮기",0.8449,0.8464,"Stage-1보다 하락"],
            ["게이팅 적용",0.8515,0.8517,"Stage-1 근접"],
            ["게이팅 + 블렌딩",0.8541,0.8541,"Stage-1과 동급"],
        ]
        return pd.DataFrame([{
            "전략":r[0], "Accuracy":r[1], "Macro-F1":r[2], "메모":r[3]
        } for r in rows])

    def render(self) -> None:
        inject_global_style()
        st.title("🧩 Stage-1 / 2-Stage 결과")
        badges(["스태킹", "전문가", "게이팅/블렌딩"])

        tabs = st.tabs(["Stage-1", "Stage-2 전문가(0/3/9/15)", "2-Stage 통합"])

        # --- 탭 0: Stage-1 (표 + 설명만; 차트 없음) ---
        with tabs[0]:
            st.markdown("#### Stage-1 (전체 21클래스)")
            df = self._stage1()
            st.dataframe(df, width="stretch", hide_index=True)
            card("- 스택: **XGB + MLP → 로지스틱 메타**\n- 해석: 단일 대비 **안정성과 성능** 모두 좋음")

        # --- 탭 1: 전문가(4클래스) — 라벨 단축 + Altair 최소 옵션 (차트 밖, 표는 expander) ---
        with tabs[1]:
            st.markdown("#### 전문가(4클래스)")

            # 표는 expander 안에
            with st.expander("📋 표 보기", expanded=False):
                df_tbl = self._experts().sort_values("Macro-F1", ascending=False)
                st.dataframe(df_tbl, width="stretch", hide_index=True)

            # 차트는 밖에 크게
            d = self._experts().sort_values("Macro-F1", ascending=False).copy()
            d["전문가(단축)"] = d["전문가모델"].apply(short_expert)

            chart = (
                alt.Chart(d)
                .mark_bar(color=ALT_COLOR)
                .encode(
                    x=alt.X("전문가(단축):N", sort="-y", axis=alt.Axis(labelAngle=0), title=None),
                    y=alt.Y("Macro-F1:Q", title="Macro-F1"),
                    tooltip=["전문가모델","Accuracy","Macro-F1","메모"],
                )
                .properties(height=280)
            )
            st.altair_chart(chart, use_container_width=True)

            card("- **SupCon**이 최고였지만 **0.43대**로 구조적 한계 존재")

        # --- 탭 2: 2-Stage 통합 — 차트 밖, 표는 expander ---
        with tabs[2]:
            st.markdown("#### 2-Stage 통합 (21 → 4)")

            # 표는 expander 안에
            with st.expander("📋 표 보기", expanded=False):
                df_tbl = self._two_stage().sort_values("Macro-F1", ascending=False)
                st.dataframe(df_tbl, width="stretch", hide_index=True)

            # 차트는 밖에 크게 (tab1과 동일한 안정 스펙)
            df = self._two_stage().sort_values("Macro-F1", ascending=False)

            chart2 = (
                alt.Chart(df)
                .mark_bar(color=ALT_COLOR)
                .encode(
                    x=alt.X("전략:N", sort="-y", axis=alt.Axis(labelAngle=0), title=None),
                    y=alt.Y("Macro-F1:Q", title="Macro-F1"),
                    tooltip=["전략","Accuracy","Macro-F1","메모"],
                )
                .properties(height=260)
            )
            st.altair_chart(chart2, use_container_width=True)

            card("- **게이팅/블렌딩**을 보수적으로 쓰면 Stage-1과 **동급 안정성** 확보")

PageRegistry.register(ResultsStagePage)

