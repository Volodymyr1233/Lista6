import datetime
import numpy


class TimeSeries:
    def __init__(self, quantity, code, frequency, timestamps, values, unit):
        self.quantity = quantity
        self.code = code
        self.frequency = frequency
        self.timestamps = timestamps
        self.values = numpy.array(values, dtype=float)
        self.unit = unit

    def __getitem__(self, item):
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

            return result_list
        else:
            raise KeyError("Your key is wrong")

    @property
    def mean(self):
        if numpy.isnan(self.values).all():
            return None
        return float(numpy.nanmean(self.values))

    @property
    def stddev(self):
        if numpy.isnan(self.values).all():
            return None
        return float(numpy.nanstd(self.values))