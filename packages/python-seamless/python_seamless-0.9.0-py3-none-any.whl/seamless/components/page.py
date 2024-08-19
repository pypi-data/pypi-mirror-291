from typing import Iterable, Literal, TypedDict, overload

from ..internal.utils import to_iter
from ..html import (
    Fragment,
    Html,
    Head,
    Title,
    Body,
    Meta,
)
from ..types import Primitive, Renderable, ChildrenType, ChildType

from ..core.component import Component


class _HtmlProps(TypedDict):
    lang: str


class _HeadProps(TypedDict): ...


class _BodyProps(TypedDict):
    dir: Literal["ltr", "rtl"]


class Page(Component, name="SeamlessBasePage"):
    @overload
    def __init__(self, *children: ChildType, title: str | None = None, html_props: _HtmlProps | None = None, head_props: _HeadProps | None = None, body_props: _BodyProps | None = None): ...
    @overload
    def __init__(self, *, children: ChildrenType, title: str | None = None, html_props: _HtmlProps | None = None, head_props: _HeadProps | None = None, body_props: _BodyProps | None = None): ...
    def __init__( # type: ignore
        self,
        *,
        title: str | None = None,
        html_props: _HtmlProps | None = None,
        head_props: _HeadProps | None = None,
        body_props: _BodyProps | None = None,
    ):
        self.title = title
        self._html_props = html_props or {"lang": "en"}
        self._head_props = head_props or {}
        self._body_props = body_props or {"dir": "ltr"}

    def head(self) -> Iterable[Renderable | Primitive]:
        """
        The children that will be inside the `head` tag.
        """
        return (
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Title(self.title),
        )

    def body(self) -> Iterable[Renderable | Primitive]:
        """
        The children that will be inside the `body` tag.
        """
        return self.children

    def render(self):
        return Fragment(
            "<!DOCTYPE html>",
            Html(**self._html_props)(
                Head(**self._head_props)(*to_iter(self.head())),
                Body(**self._body_props)(*to_iter(self.body())),
            ),
        )

    def __init_subclass__(cls, title: str | None = None, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        if title is None:
            return

        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            kwargs["title"] = kwargs.get("title", title)
            original_init(self, *args, **kwargs)

        cls.__init__ = __init__
