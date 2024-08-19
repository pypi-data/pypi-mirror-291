from typing import Collection, TypeAlias, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..core import Component
    from ..element import Element


Primitive: TypeAlias = str | int | float | bool | None
Renderable: TypeAlias = Union["Element", "Component"]

ChildType: TypeAlias = Renderable | Primitive
ChildrenType: TypeAlias = Collection[ChildType]
RenderResult: TypeAlias = Renderable | Primitive
