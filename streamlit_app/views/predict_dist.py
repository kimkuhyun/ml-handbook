from __future__ import annotations
import io
import os
import re
import random
from typing import List

import altair as alt
import pandas as pd
import streamlit as st

from streamlit_app.core.base import PageRegistry, BasePage
from streamlit_app.core.ui import inject_global_style, badges

DARK_BLUE = "#00008b"
MAGENTA = "#ff00ff"

# 샘플 CSV 경로(있으면 읽고, 없으면 코드로 생성)
SAMPLE_DIR = "data/samples"
SAMPLE_FILES = {
    "LGBM": os.path.join(SAMPLE_DIR, "test_proba_lgbm.csv"),
    "XGB" : os.path.join(SAMPLE_DIR, "test_proba_xgb.csv"),
    "RF"  : os.path.join(SAMPLE_DIR, "test_proba_rf.csv"),
    "SVC" : os.path.join(SAMPLE_DIR, "test_proba_svc.csv"),
    "MLP" : os.path.join(SAMPLE_DIR, "test_proba_mlp.csv"),
}

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

# ===== 샘플 데이터 로딩/생성 =====
@st.cache_data(show_spinner=False)
def _load_sample_csv(path: str) -> pd.DataFrame | None:
    if os.path.exists(path):
        try:
            return pd.read_csv(path)
        except Exception:
            return None
    return None

def _make_synthetic_probs(n_rows: int = 200, n_classes: int = 21, seed: int = 42, peaked: bool = False) -> pd.DataFrame:
    rnd = random.Random(seed)
    classes = [str(i) for i in range(n_classes)]
    rows = []
    for _ in range(n_rows):
        vals = [rnd.random() for _ in classes]
        if peaked:
            # 하나의 클래스에 살짝 가중치 부여 (피크형)
            j = rnd.randrange(n_classes)
            vals[j] *= 3.0
        s = sum(vals) or 1.0
        row = {c: v / s for c, v in zip(classes, vals)}
        rows.append(row)
    return pd.DataFrame(rows, columns=classes)

@st.cache_data(show_spinner=False)
def get_sample_dataframe(name: str) -> pd.DataFrame:
    """이름으로 샘플 DF를 반환. 파일 있으면 읽고, 없으면 생성."""
    path = SAMPLE_FILES.get(name, "")
    df = _load_sample_csv(path)
    if df is not None:
        return df
    # 파일이 없으면 즉석 생성
    if "피크" in name:
        return _make_synthetic_probs(seed=7, peaked=True)
    return _make_synthetic_probs(seed=3, peaked=False)

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

        # ▶ 샘플 사용 옵션
        use_samples = st.toggle("샘플 CSV 사용(업로드가 없으면 자동 사용)", value=True)
        if use_samples:
            selected_samples = st.multiselect(
                "샘플 선택",
                list(SAMPLE_FILES.keys()),
                default=list(SAMPLE_FILES.keys()),
            )

        # 사용자 업로드
        files = st.file_uploader(
            "모델 확률 CSV 선택(최대 5개)",
            type=["csv"],
            accept_multiple_files=True
        )

        col_a, col_b = st.columns([1, 1])
        with col_a:
            ymax = st.slider("Y축 최대(%)", min_value=5, max_value=30, value=12, step=1)
        with col_b:
            chart_h = st.slider("차트 높이(px)", min_value=280, max_value=520, value=380, step=20)

        run = st.button("예측 분포 그리기", type="primary")

        if not run:
            return

        # ===== 1) 데이터 소스 구성: 업로드 우선, 없으면 샘플 =====
        dists: list[tuple[str, pd.DataFrame]] = []

        if files:
            for f in files:
                try:
                    df = pd.read_csv(io.BytesIO(f.read()))
                    dist = _dist_from_prob(df)
                    dists.append((f.name, dist))
                except Exception as e:
                    st.error(f"{f.name}: 파싱 실패 - {e}")

        if not dists and use_samples and selected_samples:
            for name in selected_samples:
                df = get_sample_dataframe(name)
                dist = _dist_from_prob(df)
                dists.append((name, dist))

        if not dists:
            st.warning("업로드 파일이 없고 샘플도 선택되지 않았습니다. 파일을 올리거나 샘플을 선택하세요.")
            return

        # ===== 2) 평균 분포 계산 및 x순서 고정 =====
        all_classes = sorted({c for _, d in dists for c in d["class"].tolist()}, key=_class_sort_key)
        aligned = [d.set_index("class")["pct"] for _, d in dists]
        mean_series = pd.concat(aligned, axis=1).mean(axis=1)
        mean_df = mean_series.reindex(all_classes).reset_index()
        mean_df.columns = ["class", "pct"]

        # ===== 3) 각 탭에 바(해당 모델) + 평균 라인(마젠타) 오버레이 =====
        tabs = st.tabs([f"모델 {i+1}: {name}" for i, (name, _) in enumerate(dists)])
        for (name, dist), tab in zip(dists, tabs):
            with tab:
                # 표는 expander로
                show = dist.sort_values("class", key=lambda s: s.map(str))
                with st.expander(f"📋 {name} 표 보기", expanded=False):
                    st.dataframe(show, hide_index=True, width="stretch")

                bar = _bar_chart(
                    dist.sort_values("class", key=lambda s: s.map(_class_sort_key)),
                    ymax=ymax,
                    height=chart_h,
                    x_order=all_classes,
                )
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

                st.altair_chart(bar + line)  # width 인자 없이 컨테이너 폭 사용

PageRegistry.register(PredictDistPage)

