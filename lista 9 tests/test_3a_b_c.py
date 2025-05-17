import pytest

from Station import Station
from TimeSeries import TimeSeries
import datetime
import math

def test_station_eq_objects():
    s1 = Station("789", "Stacja 1", "Gdańsk", "ul. Zielona 3", 54.3520, 18.6466)
    s2 = Station("789", "Stacja 2", "Poznań", "ul. Czerwona 7", 52.4064, 16.9252)
    s3 = Station("784", "Stacja 3", "Wroclaw", "ul. Pilna 1", 51.3520, 23.6466)
    assert (s1 == s2) == True
    assert (s1 == s3) == False

def test_timeseries_getItem():
    dates = [
        datetime.datetime(2023, 1, 1),
        datetime.datetime(2023, 1, 2),
        datetime.datetime(2023, 1, 3),
        datetime.datetime(2023, 1, 4),
        datetime.datetime(2023, 1, 5),
        datetime.datetime(2023, 1, 6),
        datetime.datetime(2023, 1, 7),
        datetime.datetime(2023, 1, 8),
        datetime.datetime(2023, 1, 9),
        datetime.datetime(2023, 1, 10),
    ]

    values = [
        15.0,
        None,
        22.0,
        18.0,
        25.0,
        None,
        30.0,
        28.0,
        27.0,
        26.0
    ]

    ts_test = TimeSeries("PM10", "12345", "1d", dates, values, "µg/m³")

    assert ts_test[0] == (datetime.datetime(2023, 1, 1), 15.0)
    result = ts_test[1:3]
    assert result[0][0] == datetime.datetime(2023, 1, 2)
    assert math.isnan(result[0][1])
    assert result[1] == (datetime.datetime(2023, 1, 3), 22.0)

    dt = datetime.date(2023, 1, 7)
    assert ts_test[dt] == [30.0]

    error_date = datetime.datetime(2025, 5, 17)
    with pytest.raises(KeyError):
        x = ts_test[error_date]

def test_timeseries_mean_and_stddev():
    dates_with_none = [
        datetime.datetime(2023, 1, 1),
        datetime.datetime(2023, 1, 2),
        datetime.datetime(2023, 1, 3),
        datetime.datetime(2023, 1, 4),
        datetime.datetime(2023, 1, 5),
        datetime.datetime(2023, 1, 6),
        datetime.datetime(2023, 1, 7),
        datetime.datetime(2023, 1, 8),
        datetime.datetime(2023, 1, 9),
        datetime.datetime(2023, 1, 10),
    ]

    values_with_none = [
        15.0,
        None,
        22.0,
        18.0,
        25.0,
        None,
        30.0,
        28.0,
        27.0,
        26.0
    ]

    ts_test_with_none = TimeSeries("PM10", "12345", "1d", dates_with_none, values_with_none, "µg/m³")

    assert ts_test_with_none.mean == 23.875
    assert round(ts_test_with_none.stddev, 2) == 4.83

    dates_without_none = [
        datetime.datetime(2023, 1, 1),
        datetime.datetime(2023, 1, 2),
        datetime.datetime(2023, 1, 3),
        datetime.datetime(2023, 1, 4),
        datetime.datetime(2023, 1, 5),
        datetime.datetime(2023, 1, 6),
        datetime.datetime(2023, 1, 7),
        datetime.datetime(2023, 1, 8)
    ]
    values_without_none = [
        15.0,
        22.0,
        18.0,
        25.0,
        30.0,
        28.0,
        27.0,
        26.0
    ]

    ts_test_without_none = TimeSeries("PM10", "12345", "1d", dates_without_none, values_without_none, "µg/m³")

    assert ts_test_without_none.mean == 23.875
    assert round(ts_test_without_none.stddev, 2) == 4.83