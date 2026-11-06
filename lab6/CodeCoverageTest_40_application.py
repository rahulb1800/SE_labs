
import pytest
from ride_share_fare import (
    extra_distance_fare,
    seats_and_bags_ok,
    pickup_status,
)


def test_extra_distance_invalid_cab():
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare("bike", 10, "city", False)


def test_extra_distance_negative():
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("mini", -1, "city", False)


def test_extra_distance_included():
    assert extra_distance_fare("sedan", 8, "city", False) == 0


def test_subscriber_discount_included_km():
    assert extra_distance_fare("mini", 7, "city", True) == 0


def test_suv_subscriber():
    assert extra_distance_fare("suv", 12, "city", True) == 0


def test_city_extra_fare():
    assert extra_distance_fare("mini", 10, "city", False) == 60


def test_non_city_extra_fare():
    assert extra_distance_fare("mini", 10, "outstation", False) == 90


def test_large_city_extra_fare():
    assert extra_distance_fare("mini", 30, "city", False) == 500


def test_large_outstation_extra_fare():
    assert extra_distance_fare("mini", 30, "outstation", False) == 750


def test_wheelchair_passengers_allowed():
    assert seats_and_bags_ok(2, 5, True) is True


def test_wheelchair_too_many_passengers():
    assert seats_and_bags_ok(3, 1, True) is False


def test_too_many_passengers():
    assert seats_and_bags_ok(5, 1, False) is False


def test_bags_allowed():
    assert seats_and_bags_ok(4, 2, False) is True


def test_too_many_bags():
    assert seats_and_bags_ok(4, 3, False) is False


def test_pickup_on_time():
    assert pickup_status(10, True, False) == "on_time"


def test_pickup_delayed():
    assert pickup_status(0, False, False) == "delayed"


def test_pickup_missed():
    assert pickup_status(-20, False, False) == "missed"
