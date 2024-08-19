from typing import TYPE_CHECKING
from uuid import uuid4 as uuid

from ..context import Context, get_context
from ..context.request import request as _request
from ..errors import RenderError
from ..core.component import Component
from ..element import Element
from .props import render_props, transform_props

if TYPE_CHECKING:
    from ..types import Renderable, Primitive


def render(element: "Renderable | Primitive", *, pretty=False, tab_indent=1, context: "Context | None" = None) -> str:
    """
    Renders the given element into an HTML string.

    Args:
        element (Renderable | Primitive): The element to be rendered.
        pretty (bool, optional): Whether to format the HTML string with indentation and line breaks. Defaults to False.
        tab_indent (int, optional): The number of spaces to use for indentation when pretty is True. Defaults to 1.

    Returns:
        str: The rendered HTML string.
    """
    request = _request()
    if request is not None:
        request.id = str(uuid())
    return _render(element, pretty=pretty, tab_indent=tab_indent, context=get_context(context))


def _render(element: "Renderable | Primitive", *, pretty=False, tab_indent=1, context: "Context") -> str:
    if isinstance(element, Component):
        element = _render(element.render(), pretty=pretty, tab_indent=tab_indent, context=context)

    if not isinstance(element, Element):
        return str(element) if element is not None else ""

    tag_name = getattr(element, "tag_name", None)

    props = {k: v for k, v in transform_props(element.props, context=context).items() if v not in [None, False]}

    props_string = render_props(props)
    open_tag = f"{tag_name} {props_string}".strip()

    if element.inline:
        if len(element.children) > 0:
            # Maybe this should be a warning instead of an error?
            raise RenderError("Inline components cannot have children")
        return f"<{open_tag}>"

    tab = "  " * tab_indent if pretty else ""
    children_join_string = f"\n{tab}" if pretty else ""
    children = [
        _render(child, pretty=pretty, tab_indent=tab_indent + 1, context=context)
        for child in element.children
    ]
    if pretty:
        children.insert(0, "")

    children = children_join_string.join(children)

    if pretty:
        children += f"\n{tab[:-2]}"

    if not tag_name:
        return children

    return f"<{open_tag}>{children}</{tag_name}>"
