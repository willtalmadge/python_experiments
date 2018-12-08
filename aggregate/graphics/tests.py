from aggregate.graphics.functions import intersect_interval


def test_intersect_interval():
    assert (1, 2) == intersect_interval(
        0, 2, 1, 4
    )
    assert None == intersect_interval(
        0, 1, 2, 3
    )

