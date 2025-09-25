# streamlit_app/core/base.py
from __future__ import annotations
import streamlit as st
from dataclasses import dataclass, field
from typing import Type, Dict, List, Optional
from streamlit_app.core.ui import inject_global_style, footer

@dataclass
class PageMeta:
    title: str
    slug: str
    icon: str
    group: str = "models"        # "home" | "eda" | "models"
    section: str = "모델"         # models 그룹일 때: "모델" | "전처리" | "규제"

class BasePage:
    # 서브클래스에서 오버라이드
    title: str = "Untitled"
    slug: str = "untitled"
    icon: str = "📄"
    group: str = "models"     # 기본값: 모델 그룹
    section: str = "모델"      # 기본값: 모델 섹션

    def meta(self) -> PageMeta:
        return PageMeta(
            title=self.title, slug=self.slug, icon=self.icon,
            group=self.group, section=self.section
        )

    def render(self) -> None:
        raise NotImplementedError

class PageRegistry:
    _pages: Dict[str, Type[BasePage]] = {}

    @classmethod
    def register(cls, page_cls: Type[BasePage]):
        slug = page_cls.slug
        cls._pages[slug] = page_cls

    @classmethod
    def get(cls, slug: str) -> Type[BasePage]:
        return cls._pages[slug]

    @classmethod
    def list(cls) -> List[Type[BasePage]]:
        return list(cls._pages.values())

    @classmethod
    def list_by(cls, group: Optional[str] = None, section: Optional[str] = None) -> List[Type[BasePage]]:
        pages = list(cls._pages.values())
        if group:
            pages = [p for p in pages if p.group == group]
        if section:
            pages = [p for p in pages if p.section == section]
        # 홈/EDA는 섹션 정렬 불필요, 모델 그룹은 제목순 정렬
        return sorted(pages, key=lambda p: (p.group, p.section, p.title))

class App:
    def __init__(self, project_title: str, repo_name: str):
        self.project_title = project_title
        self.repo_name = repo_name

    def run(self) -> None:
        st.set_page_config(
            page_title=f"{self.project_title} · Home",
            page_icon="📘",
            layout="wide",
        )
        inject_global_style()

        # 1) 최상위 그룹 선택
        top_group = st.sidebar.radio("섹션", ["Home", "EDA", "모델", "결과"], index=0, horizontal=False)

        if top_group == "Home":
            pages = PageRegistry.list_by(group="home")
            page_cls = pages[0] if pages else None

        elif top_group == "EDA":
            pages = PageRegistry.list_by(group="eda")
            # EDA는 페이지가 여러 개일 수 있으니 선택박스 제공
            titles = [f"{p.icon} {p.title}" for p in pages]
            idx = st.sidebar.selectbox("EDA 페이지", list(range(len(pages))), format_func=lambda i: titles[i]) if pages else None
            page_cls = pages[idx] if pages else None

        elif top_group == "모델":  # "모델들"
            sub = st.sidebar.radio("분류", ["모델", "전처리", "규제"], index=0)
            pages = PageRegistry.list_by(group="models", section=sub)
            titles = [f"{p.icon} {p.title}" for p in pages]
            idx = st.sidebar.selectbox(f"{sub} 페이지", list(range(len(pages))), format_func=lambda i: titles[i]) if pages else None
            page_cls = pages[idx] if pages else None

        else:
            pages = PageRegistry.list_by(group='results')
            titles = [f"{p.icon} {p.title}" for p in pages]
            idx = st.sidebar.selectbox("결과 페이지", list(range(len(pages))), format_func=lambda i: titles[i]) if pages else None
            page_cls = pages[idx] if pages else None

        if page_cls is None:
            st.warning("표시할 페이지가 없습니다. 파일 임포트/등록을 확인해주세요.")
        else:
            page = page_cls()
            page.render()

        footer(self.repo_name)

