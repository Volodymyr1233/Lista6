import datetime
import numpy
from typing import Union

from numpy import ndarray


class TimeSeries:
    def __init__(self, quantity: str, code: str, frequency: str, timestamps: list[datetime.datetime], values: list[float], unit: str) -> None:
        self.quantity: str = quantity
        self.code: str = code
        self.frequency: str = frequency
        self.timestamps: list[datetime.datetime] = timestamps
        self.values: ndarray[float] = numpy.array(values, dtype=float)
        self.unit: str = unit

    def __getitem__(self, item: int | slice | datetime.datetime | datetime.date) -> list[tuple[datetime.datetime, float]] | tuple[datetime.datetime, float] | float | ndarray[float]:
        if isinstance(item, int):
            try:
                return self.timestamps[item], self.values[item]
            except:
                raise KeyError("Your key is too high")
        elif (isinstance(item, slice)):
            result_list = []
            values_slice = self.values[item]
            timestamps_slice = self.timestamps[item]

            for i in range(0, len(values_slice)):
                result_list.append((timestamps_slice[i], values_slice[i]))

            return result_list
        elif (isinstance(item, datetime.datetime) or isinstance(item, datetime.date)):
            index_list = []
            for i in range(0, len(self.timestamps)):

                if (isinstance(item, datetime.date) and (self.timestamps[i].date() == item)):
                    index_list.append(i)

                elif (self.timestamps[i] == item):
                    index_list.append(i)
            result_list = []
            for index in index_list:
                result_list.append(self.values[index])

            if (len(result_list) == 0):
                raise KeyError("Nie ma danych")
            return result_list
        else:
            raise KeyError("Your key is wrong")

    @property
    def mean(self) -> float | None:
        if numpy.isnan(self.values).all():
            return None
        return float(numpy.nanmean(self.values))

    @property
    def stddev(self) -> float | None:
        if numpy.isnan(self.values).all():
            return None
        return float(numpy.nanstd(self.values))

if __name__ == "__main__":
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

    print("test_getitem_index:", ts_test[0])
    print("test_getitem_slice:", ts_test[1:3])

    dt = datetime.date(2023, 1, 3)
    print("test_getitem_date_exact:", ts_test[dt])

    dt = datetime.date(2022, 12, 31)
    print("test_getitem_date_not_found:", ts_test[dt])

    print("test_mean:", ts_test.mean)
    print("test_stddev:", ts_test.stddev)

