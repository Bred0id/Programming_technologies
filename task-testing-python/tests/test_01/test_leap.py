import pytest
from simple_library_01.functions import is_leap

def test_zero():
    with pytest.raises(AttributeError) as exc_info:
        is_leap(0)

    assert str(exc_info.value) == "Year must be greater than 0"

def test_minus():
    with pytest.raises(AttributeError) as exc_info:
        is_leap(-100)

    assert str(exc_info.value) == "Year must be greater than 0"

def test_simple_primary():
    assert is_leap(16) == True

def test_difficult_primary():
    assert is_leap(400) == True

def test_almost_prime():
    assert is_leap(100) == False

def test_not_prime():
    assert is_leap(11) == False
