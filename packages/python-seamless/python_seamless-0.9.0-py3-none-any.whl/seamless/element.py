from typing import TYPE_CHECKING, TypeVar, Generic, Unpack

from .internal.utils import to_iter
from .types.html import HTMLElement


if TYPE_CHECKING:
    from .types import ChildrenType, ChildType


PropsType = TypeVar("PropsType", bound=HTMLElement)


class Element(Generic[PropsType]):
    def __init__(
        self,
        *args: "ChildType",
        children: "ChildrenType | None" = None,
        **kwargs: Unpack[PropsType], # type: ignore - until https://github.com/python/typing/issues/1399 is resolved
    ):
        self.children = tuple(to_iter(children or args))
        self.props = kwargs

    tag_name: str

    inline = False

    def __call__(self, *children: "ChildType"):
        self.children = children
        return self
