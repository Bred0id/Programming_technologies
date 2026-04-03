import pytest
from simple_library_01.functions import get_month_days


def test_exceptional_year_with_minus_month():
    assert get_month_days(1930, -2) == 30

def test_exceptional_year_with_normal_month():
    assert get_month_days(1930, 2) == 30

def test_exceptional_year_with_very_big_month():
    assert get_month_days(1930, 13) == 30

def test_if_year_not_1984_but_month_is_2():
    assert get_month_days(2007, 2) == 28

def test_if_year_1984_but_month_is_2():
    assert get_month_days(1984, 2) == 29

def test_normal_year_minus_month():
    with pytest.raises(AttributeError) as exc_info:
        get_month_days(1000, -2)

    assert str(exc_info.value) == "Month should be in range [1-12]"

def test_normal_year_big_month():
    with pytest.raises(AttributeError) as exc_info:
        get_month_days(1000, 113)

    assert str(exc_info.value) == "Month should be in range [1-12]"

def test_normal_year_month_4():
    assert get_month_days(1000, 4) == 30

def test_normal_year_month_6():
    assert get_month_days(1000, 6) == 30

def test_normal_year_month_9():
    assert get_month_days(1000, 9) == 30

def test_normal_year_month_11():
    assert get_month_days(1000, 11) == 30

def test_normal_year_month_1():
    assert get_month_days(1000, 1) == 31

def test_normal_year_month_3():
    assert get_month_days(1000, 3) == 31

def test_normal_year_month_5():
    assert get_month_days(1000, 5) == 31

def test_normal_year_month_7():
    assert get_month_days(1000, 7) == 31

def test_normal_year_month_8():
    assert get_month_days(1000, 8) == 31

def test_normal_year_month_10():
    assert get_month_days(1000, 10) == 31

def test_normal_year_month_12():
    assert get_month_days(1000, 12) == 31