from realscreenPy.main import Real
import math
import pytest


def test_16_by_9():
    real = Real(10, "16:9")
    dimensions = real.get_dimensions()
    expected_width = (10 / math.sqrt(16**2 + 9**2)) * 16
    expected_height = (10 / math.sqrt(16**2 + 9**2)) * 9
    expected_area = expected_width * expected_height
    assert pytest.approx(dimensions["width"], 0.01) == expected_width
    assert pytest.approx(dimensions["height"], 0.01) == expected_height
    assert pytest.approx(dimensions["area"], 0.01) == expected_area


def test_4_by_3():
    real = Real(10, "4:3")
    dimensions = real.get_dimensions()
    expected_width = (10 / math.sqrt(4**2 + 3**2)) * 4
    expected_height = (10 / math.sqrt(4**2 + 3**2)) * 3
    expected_area = expected_width * expected_height
    assert pytest.approx(dimensions["width"], 0.01) == expected_width
    assert pytest.approx(dimensions["height"], 0.01) == expected_height
    assert pytest.approx(dimensions["area"], 0.01) == expected_area
