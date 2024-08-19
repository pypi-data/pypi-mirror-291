import pytest


@pytest.mark.priority('p0')
def test_a():
    pass


@pytest.mark.priority('p1')
def test_b():
    pass


def test_c():
    pass
