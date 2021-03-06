from aggregate.graphics.functions import (
    draw_rectangles, intersect_rectangle,
    add_colors,
    ColoredRectangle
)

rect1 = ColoredRectangle(
    x=0, y=0, width=0.7, height=0.7,
    r=1, g=0, b=0, a=1
)
rect2 = ColoredRectangle(
    x=0.3, y=0.3, width=1, height=1,
    r=0, g=0, b=1, a=1
)
# The following function only wants rectangles, but we can pass in any superset
# of the rectangle protocol and mypy won't complain about it.
rect_int = intersect_rectangle(rect1, rect2)
if rect_int is not None:
    rect3 = ColoredRectangle.combine(rect_int, add_colors(rect1, rect2))

    # Here we need the full ColoredRectangle type.
    draw_rectangles(
        rect1, rect2, rect3
    )
else:
    draw_rectangles(
        rect1, rect2
    )

