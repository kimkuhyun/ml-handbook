# -*- coding: utf-8 -*-
from __future__ import annotations
import pandas as pd
import altair as alt
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style

ALT_COLOR = "#00008b"

class ResultsSubmissionsPage(BasePage):
    title  = "실제 제출 결과"
    slug   = "results-submissions"
    icon   = "📈"
    group  = "results"
    section = "results"
    order = 60

    def _data(self) -> pd.DataFrame:
        rows = [
            ("2025-09-17 09:10:25", 0.0043841041),
            ("2025-09-17 09:12:19", 0.0043841041),
            ("2025-09-17 09:43:34", 0.7023614873),
            ("2025-09-17 12:22:25", 0.7458999716),
            ("2025-09-17 14:27:45", 0.0043841041),
            ("2025-09-17 17:35:42", 0.8000639391),
            ("2025-09-18 09:33:14", 0.8003233472),
            ("2025-09-18 10:39:49", 0.7612666200),
            ("2025-09-18 10:42:17", 0.7596912103),
            ("2025-09-18 11:44:50", 0.7510646106),
            ("2025-09-18 14:29:18", 0.7561282062),
            ("2025-09-18 15:47:57", 0.7574520094),
            ("2025-09-18 16:02:57", 0.8080912253),
            ("2025-09-19 11:29:41", 0.7629987690),
            ("2025-09-19 12:33:05", 0.7588796603),
            ("2025-09-19 14:02:26", 0.6991731099),
            ("2025-09-19 15:18:39", 0.8007203052),
            ("2025-09-19 15:54:10", 0.6560541537),
            ("2025-09-19 18:00:29", 0.7573602162),
            ("2025-09-19 18:21:46", 0.8059250862),
            ("2025-09-20 06:06:28", 0.7654696796),
            ("2025-09-20 06:36:57", 0.7583682846),
            ("2025-09-20 09:07:34", 0.7556507935),
            ("2025-09-20 16:09:07", 0.7573469895),
            ("2025-09-21 14:58:06", 0.7131814697),
            ("2025-09-21 23:49:04", 0.7892156729),
            ("2025-09-23 12:11:23", 0.7127557926),
            ("2025-09-23 18:32:41", 0.7507008097),
            ("2025-09-23 20:39:19", 0.8051365039),
            ("2025-09-23 20:40:12", 0.8051365039),
            ("2025-09-24 10:27:51", 0.8002121131),
            ("2025-09-24 10:51:19", 0.8051365039),
            ("2025-09-24 14:40:16", 0.8002121131),
            ("2025-09-24 16:34:02", 0.8017826599),
        ]

        df = pd.DataFrame(rows, columns=["제출시각", "점수"])
        df["제출시각"] = pd.to_datetime(df["제출시각"])
        df = df.sort_values("제출시각").reset_index(drop=True)
        return df

    def render(self) -> None:
        inject_global_style()
        st.title(f"{self.icon} 실제 제출 결과")

        df = self._data()

        # 상단 요약
        c1, c2, c3 = st.columns([1,1,1])
        with c1:
            st.metric("제출 수", f"{len(df)}")
        with c2:
            st.metric("최고 점수", f"{df['점수'].max():.10f}")
        with c3:
            st.metric("최신 점수", f"{df.iloc[-1]['점수']:.10f}")

        # ---- 메인 추세 그래프 (0.7 미만 제외, y 시작 0.5, 높이 300) ----
        df_plot = df[df["점수"] >= 0.7].copy()
        hi = float(df_plot["점수"].max()) if not df_plot.empty else 1.0
        pad = max(0.002, (hi - 0.5) * 0.10)
        y_dom = [0.5, min(1.0, hi + pad)]

        base = alt.Chart(df_plot).encode(
            x=alt.X("제출시각:T", title="제출 시각",
                    axis=alt.Axis(format="%m-%d %H:%M", labelAngle=0)),
            y=alt.Y("점수:Q", title="점수",
                    scale=alt.Scale(domain=y_dom, zero=False, nice=False),
                    axis=alt.Axis(format=".3f")),
            tooltip=[
                alt.Tooltip("제출시각:T", title="제출시각", format="%Y-%m-%d %H:%M:%S"),
                alt.Tooltip("점수:Q", title="점수", format=".10f"),
            ],
        ).properties(height=300)

        st.altair_chart(
            base.mark_line(color=ALT_COLOR, strokeWidth=2, clip=True)
                + base.mark_point(color=ALT_COLOR, size=45, clip=True),
            use_container_width=True
        )

        # ---- 하단 탭: 그래프만 ----
        tabs = st.tabs([
            "기본 표",
            "날짜별 제출 수",
            "시간대별 제출 수",
            "점수 구간 분포",
        ])

        # 기본 표(유지)
        with tabs[0]:
            show_df = df[["제출시각", "점수"]].sort_values("제출시각", ascending=False).reset_index(drop=True)
            st.dataframe(show_df, hide_index=True, width="stretch")

        # 추가 1: 날짜별 제출 수 (문자열 라벨로 집계 → 중복 라벨 방지)
        with tabs[1]:
            day_df = (df.assign(일자=df["제출시각"].dt.strftime("%Y-%m-%d"))
                        .groupby("일자", as_index=False)
                        .size()
                        .rename(columns={"size": "제출수"}))
            day_chart = (
                alt.Chart(day_df)
                .mark_bar(color=ALT_COLOR)
                .encode(
                    x=alt.X("일자:N", title="일자", sort=None, axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("제출수:Q", title="제출 수"),
                    tooltip=[alt.Tooltip("일자:N", title="일자"), alt.Tooltip("제출수:Q", title="제출 수")],
                )
                .properties(height=300)
            )
            st.altair_chart(day_chart, use_container_width=True)

        # 추가 2: 시간대별 제출 수 (0~23시, 빠진 시간은 0으로)
        with tabs[2]:
            hour_df = (df.assign(시간=df["제출시각"].dt.hour)
                         .groupby("시간", as_index=False).size()
                         .set_index("시간").reindex(range(24), fill_value=0)
                         .reset_index().rename(columns={"size": "제출수"}))
            hour_chart = (
                alt.Chart(hour_df)
                .mark_bar(color=ALT_COLOR)
                .encode(
                    x=alt.X("시간:O", title="시간(시)", sort=list(range(24)), axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("제출수:Q", title="제출 수"),
                    tooltip=[alt.Tooltip("시간:O", title="시간"), alt.Tooltip("제출수:Q", title="제출 수")],
                )
                .properties(height=300)
            )
            st.altair_chart(hour_chart, use_container_width=True)

        # 추가 3: 점수 구간 분포 (명시적 bin → x/x2 사용, 오른쪽 여백 확보)
        with tabs[3]:
            # bins: 0.50~1.01까지 0.01 간격
            hist_chart = (
                alt.Chart(df)
                .transform_bin(
                    field="점수",
                    bin=alt.Bin(step=0.01, extent=[0.50, 1.01]),
                    as_=["bin_start", "bin_end"],
                )
                .mark_bar(color=ALT_COLOR)
                .encode(
                    x=alt.X("bin_start:Q", title="점수",
                            scale=alt.Scale(domain=[0.50, 1.01], nice=False)),
                    x2="bin_end:Q",
                    y=alt.Y("count():Q", title="빈도"),
                    tooltip=[
                        alt.Tooltip("bin_start:Q", title="구간 시작", format=".2f"),
                        alt.Tooltip("bin_end:Q",   title="구간 끝",   format=".2f"),
                        alt.Tooltip("count():Q",   title="빈도"),
                    ],
                )
                .properties(height=300)
            )
            st.altair_chart(hist_chart, use_container_width=True)


PageRegistry.register(ResultsSubmissionsPage)

