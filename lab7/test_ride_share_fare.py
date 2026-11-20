from hypothesis import given, strategies as st
from ride_share_fare import parse_trip, fare_average, payable_fare

@given(st.text() | st.none())
def test_parse_trip_no_crash(s):
    try:
        parse_trip(s)
    except ValueError:
        pass

@given(st.text() | st.none())
def test_fare_average_no_crash(s):
    try:
        fare_average(s)
    except ValueError:
        pass

@given(st.text() | st.none())
def test_payable_fare_no_crash(s):
    try:
        payable_fare(s)
    except ValueError:
        pass