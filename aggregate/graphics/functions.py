from dataclasses import dataclass
from typing import Tuple, Optional

import cairo
from typing_extensions import Protocol

from aggregate.graphics.params import (
    PRectangle, Rectangle,
    PColor,
    Color
)


class PColoredRectangle(PRectangle, PColor, Protocol): ...


@dataclass
class ColoredRectangle:
    x: float
    y: float
    width: float
    height: float
    r: float
    g: float
    b: float
    a: float

    @staticmethod
    def combine(rect: PRectangle, color: PColor) -> 'ColoredRectangle':
        return ColoredRectangle(
            rect.x, rect.y, rect.width, rect.height,
            color.r, color.g, color.b, color.a
        )


def draw_rectangles(*rects: PColoredRectangle) -> None:
    with cairo.SVGSurface("example.svg", 200, 200) as surface:
        ctx = cairo.Context(surface)
        ctx.scale(200, 200)
        ctx.set_line_width(0.04)
        for rect in rects:
            draw_one_rect(ctx, rect)


def draw_one_rect(ctx: cairo.Context, rect: PColoredRectangle) -> None:
    ctx.move_to(rect.x, rect.y)
    x2 = rect.x + rect.width
    y2 = rect.y + rect.height
    ctx.line_to(x2, rect.y)
    ctx.line_to(x2, y2)
    ctx.line_to(rect.x, y2)
    ctx.close_path()
    ctx.set_source_rgba(rect.r, rect.g, rect.b, rect.a)
    ctx.fill()


def between(a: float, b: float, x: float) -> bool:
    return a < x < b


def intersect_interval(
        a1: float, b1: float, a2: float, b2: float
) -> Optional[Tuple[float, float]]:
    if between(a1, b1, a2):
        a3 = a2
    elif between(a2, b2, a1):
        a3 = a1
    else:
        return None

    if between(a1, b1, b2):
        b3 = b2
    elif between(a2, b2, b1):
        b3 = b1
    else:
        return None

    return a3, b3


def intersect_rectangle(
        rect_a: PRectangle, rect_b: PRectangle
) -> Optional[Rectangle]:
    """
    Compute the rectangle at the intersection of the given rectangles, if there
    is an intersection. If there is no intersection we return None.
    """
    ax1 = rect_a.x
    ax2 = rect_a.x + rect_a.width
    ay1 = rect_a.y
    ay2 = rect_a.y + rect_a.height

    bx1 = rect_b.x
    bx2 = rect_b.x + rect_b.width
    by1 = rect_b.y
    by2 = rect_b.y + rect_b.height

    x_int = intersect_interval(ax1, ax2, bx1, bx2)
    if x_int is not None:
        cx1, cx2 = x_int
    else:
        return None

    y_int = intersect_interval(ay1, ay2, by1, by2)
    if y_int is not None:
        cy1, cy2 = y_int
    else:
        return None
    return Rectangle(
        x=cx1, y=cy1, width=cy2 - cy1, height=cx2 - cx1
    )


def add_colors(color_a: PColor, color_b: PColor) -> Color:
    r = min(color_a.r + color_b.r, 1)
    g = min(color_a.g + color_b.g, 1)
    b = min(color_a.b + color_b.b, 1)
    a = min(color_a.a + color_b.a, 1)
    return Color(r, g, b, a)
