import pytest
from .solution import sum_two


def test_valid_types():
    """Тесты для валидных типов."""
    assert sum_two(1, 2) == 3
    assert sum_two(10, 20) == 30


def test_invalid_types():
    """Тесты для невалидных типов."""
    with pytest.raises(TypeError):
        sum_two(1, 2.4)
    with pytest.raises(TypeError):
        sum_two(1, "2")
