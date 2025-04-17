from Station import Station
from TimeSeries import TimeSeries
from datetime import datetime, date

def test():
    daty = [
        datetime(2024, 1, 1, 8),
        datetime(2024, 1, 1, 9),
        datetime(2024, 1, 1, 10),
        datetime(2024, 1, 2, 8)
    ]

    wartosci = [15.2, 16.8, None, 18.0]

    ts = TimeSeries(0, 0, 0, daty, wartosci, 0)
    print("Test 1:", ts[1])  # powinno dać: (2024-01-01 09:00:00, 16.8)

    # Test 2 – slice
    print("Test 2:", ts[1:3])
    # powinno dać: [(2024-01-01 09:00:00, 16.8), (2024-01-01 10:00:00, None)]

    # Test 3 – datetime.date
    print("Test 3:", ts[date(2024, 1, 2)])  # powinno dać: 18.0

    # Test 4 – datetime.datetime
    print("Test 4:", ts[datetime(2024, 1, 1, 9)])  # powinno dać: 16.8

    # Test 5 – data nie istnieje
    print("Test 5:", ts[date(2024, 1, 3)])  # powinno dać: None


if __name__ == '__main__':
    test()

