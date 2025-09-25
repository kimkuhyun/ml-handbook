from __future__ import annotations
import io
import re
from typing import List

import altair as alt
import pandas as pd
import streamlit as st

from streamlit_app.core.base import PageRegistry, BasePage
from streamlit_app.core.ui import inject_global_style, badges

DARK_BLUE = "#00008b"
MAGENTA = "#ff00ff"

def _detect_prob_cols(df: pd.DataFrame) -> List[str]:
    cols = [c for c in df.columns if re.fullmatch(r"\d+", str(c))]
    if cols:
        return cols
    cols = [c for c in df.columns if re.fullmatch(r"(class|target)_(\d+)", str(c))]
    if cols:
        return cols
    float_cols = [c for c in df.columns if pd.api.types.is_float_dtype(df[c])]
    if float_cols:
        return float_cols
    return []

def _to_class_labels(columns: List[str]) -> List[str]:
    labels = []
    for c in columns:
        m = re.fullmatch(r"(?:class|target)_(\d+)", str(c))
        labels.append(m.group(1) if m else str(c))
    return labels

def _dist_from_prob(df: pd.DataFrame) -> pd.DataFrame:
    prob_cols = _detect_prob_cols(df)
    if not prob_cols:
        raise ValueError("확률 컬럼을 찾을 수 없습니다. (예: '0'..'20' 또는 'target_0'.. 형태)")
    probs = df[prob_cols].astype(float).copy()
    probs.columns = _to_class_labels(list(probs.columns))
    pct = probs.mean(axis=0) * 100.0
    out = pd.DataFrame({"class": pct.index, "pct": pct.values})
    out["class"] = out["class"].astype(str)
    return out

def _class_sort_key(x: str):
    try:
        return (0, int(x))
    except ValueError:
        return (1, x)

def _bar_chart(df: pd.DataFrame, ymax: float, height: int = 320, x_order: List[str] | None = None) -> alt.Chart:
    x_enc = alt.X("class:N", title="class",
                  scale=alt.Scale(domain=x_order) if x_order else alt.Undefined)
    y_scale = alt.Scale(domain=[0, ymax])
    base = (
        alt.Chart(df)
        .mark_bar(color=DARK_BLUE)
        .encode(
            x=x_enc,
            y=alt.Y("pct:Q", title="%", scale=y_scale),
            tooltip=[alt.Tooltip("class:N", title="class"),
                     alt.Tooltip("pct:Q", title="%", format=".2f")],
        )
        .properties(height=height)
    )
    txt = (
        alt.Chart(df)
        .mark_text(align="center", baseline="bottom", dy=-3, color=DARK_BLUE)
        .encode(
            x=x_enc,
            y=alt.Y("pct:Q", scale=y_scale),
            text=alt.Text("pct:Q", format=".1f"),
        )
        .properties(height=height)
    )
    return base + txt

class PredictDistPage(BasePage):
    title = "예측 분포"
    slug = "predict-dist"
    icon = "📊"
    group = "results"
    section = ""

    def render(self) -> None:
        inject_global_style()
        st.title("📊 예측 분포")
        badges(["확률 CSV", "다중 모델", "분포 비교"])
        st.markdown("---")

        st.markdown("**CSV 형식**: 컬럼에 클래스 확률이 있어야 합니다. (예: `0..20` 또는 `target_0..target_20`)")

        files = st.file_uploader(
            "모델 확률 CSV 선택(최대 5개)",
            type=["csv"],
            accept_multiple_files=True
        )

        col_a, col_b = st.columns([1, 1])
        with col_a:
            ymax = st.slider("Y축 최대(%)", min_value=5, max_value=20, value=10, step=2)
        with col_b:
            chart_h = st.slider("차트 높이(px)", min_value=300, max_value=520, value=400, step=20)

        run = st.button("예측 분포 그리기", type="primary")

        if not (run and files):
            return

        # 1) 모든 파일을 먼저 파싱해서 (이름, 분포DF) 리스트 생성
        dists: list[tuple[str, pd.DataFrame]] = []
        for f in files:
            try:
                df = pd.read_csv(io.BytesIO(f.read()))
                dist = _dist_from_prob(df)
                dists.append((f.name, dist))
            except Exception as e:
                st.error(f"{f.name}: 파싱 실패 - {e}")

        if not dists:
            return

        # 2) 평균 분포 계산 (클래스 정렬은 숫자 우선)
        all_classes = sorted({c for _, d in dists for c in d["class"].tolist()}, key=_class_sort_key)
        aligned = [d.set_index("class")["pct"] for _, d in dists]
        mean_series = pd.concat(aligned, axis=1).mean(axis=1)
        mean_df = mean_series.reindex(all_classes).reset_index()
        mean_df.columns = ["class", "pct"]

        # 3) 각 탭에서: 바(해당 모델) + 평균 꺾은선(마젠타) 오버레이
        tabs = st.tabs([f"모델 {i+1}: {name}" for i, (name, _) in enumerate(dists)])
        for (name, dist), tab in zip(dists, tabs):
            with tab:
                show = dist.sort_values("class", key=lambda s: s.map(str))
                with st.expander(f"📋 {name} 표 보기", expanded=False):
                    st.dataframe(show, hide_index=True, width="stretch")

                # x 순서 고정(모든 모델 동일), y스케일 통일
                bar = _bar_chart(dist.sort_values("class", key=lambda s: s.map(_class_sort_key)),
                                 ymax=ymax, height=chart_h, x_order=all_classes)
                line = (
                    alt.Chart(mean_df)
                    .mark_line(color=MAGENTA, strokeWidth=2)
                    .encode(
                        x=alt.X("class:N", scale=alt.Scale(domain=all_classes), title="class"),
                        y=alt.Y("pct:Q", scale=alt.Scale(domain=[0, ymax]), title="%"),
                        tooltip=[alt.Tooltip("class:N", title="class"),
                                 alt.Tooltip("pct:Q", title="평균%", format=".2f")],
                    )
                    .properties(height=chart_h)
                )

                st.altair_chart(bar + line)  # 가로폭은 컨테이너에 맞춤 (경고 피하려고 width 인자 미사용)

PageRegistry.register(PredictDistPage)

