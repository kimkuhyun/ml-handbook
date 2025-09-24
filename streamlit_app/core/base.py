# streamlit_app/core/base.py
from __future__ import annotations
import streamlit as st
from typing import Dict, Type, List, Optional

class BasePage:
    """모든 페이지가 상속할 베이스 클래스."""
    title: str = "Untitled"
    slug: str = "untitled"
    icon: str = "📄"  # 사이드바 표시용

    def render(self) -> None:
        raise NotImplementedError("Each page must implement render().")

class PageRegistry:
    """페이지 클래스를 등록/조회하는 레지스트리."""
    _pages: Dict[str, Type[BasePage]] = {}

    @classmethod
    def register(cls, page_cls: Type[BasePage]) -> None:
        if not issubclass(page_cls, BasePage):
            raise TypeError("Page must inherit from BasePage")
        cls._pages[page_cls.slug] = page_cls

    @classmethod
    def list(cls) -> List[Type[BasePage]]:
        # 정렬: slug 순서 대신 title 알파벳/커스텀 정렬 가능
        return sorted(cls._pages.values(), key=lambda c: c.title)

    @classmethod
    def get(cls, slug: str) -> Optional[Type[BasePage]]:
        return cls._pages.get(slug)

class App:
    """사이드바 네비게이션 + 페이지 렌더링."""
    def __init__(self, project_title: str, repo_name: str):
        self.project_title = project_title
        self.repo_name = repo_name

    def run(self) -> None:
        st.set_page_config(
            page_title=f"{self.project_title} · Home",
            page_icon="📘",
            layout="wide",
        )
        # 사이드바: 페이지 선택
        pages = PageRegistry.list()
        titles = [f"{p.icon} {p.title}" for p in pages]
        slugs = [p.slug for p in pages]
        default_idx = slugs.index("home") if "home" in slugs else 0
        st.sidebar.title("📑 Pages")
        choice = st.sidebar.selectbox("Go to", titles, index=default_idx)
        slug = slugs[titles.index(choice)]

        page_cls = PageRegistry.get(slug)
        page = page_cls()  # 인스턴스화
        page.render()

        # 전역 푸터
        st.markdown("---")
        st.caption(f"© 2025 우리만의 AI 교과서 · Repo: {self.repo_name}")

