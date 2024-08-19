import pytest


@pytest.mark.parametrize(
    "summand_1, summand_2, sum_1",
    [
        (-1, 1, 0),
        (0, 0, 0),
        (-1j, 1, 1 - 1j),
    ],
)
def test_addition(summand_1, summand_2, sum_1):
    assert summand_1 + summand_2 == sum_1
