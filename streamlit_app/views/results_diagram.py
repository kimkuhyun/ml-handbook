# streamlit_app/views/results_diagram.py
# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
import streamlit as st
from streamlit_app.core.base import BasePage, PageRegistry
from streamlit_app.core.ui import inject_global_style

class ResultsDiagramPage(BasePage):
    title   = "데이터 다이어그램"
    slug    = "results-diagram"
    icon    = "🖼️"
    group   = "results"
    section = "results"
    order = 10

    def _diagram_path(self) -> Path | None:
        # 1순위: 프로젝트 루트 기준
        p1 = Path("assets/eda/diagram.png")
        if p1.exists():
            return p1
        # 2순위: streamlit_app 하위 실행 환경 대비
        p2 = Path(__file__).resolve().parents[1] / "assets" / "eda" / "diagram.png"
        if p2.exists():
            return p2
        return None

    def render(self) -> None:
        inject_global_style()
        st.title(f"{self.icon} {self.title}")

        path = self._diagram_path()
        if path is None:
            st.error("`assets/eda/diagram.png` 파일을 찾을 수 없습니다. 파일을 해당 경로에 추가해주세요.")
            return

        width_px = st.slider("이미지 너비(px)", min_value=480, max_value=1600, value=1000, step=20)
        with path.open("rb") as f:
            img_bytes = f.read()

        st.image(img_bytes, caption="diagram.png", width=width_px)

PageRegistry.register(ResultsDiagramPage)

