from TimeSeries import TimeSeries
from SeriesValidator import OutlierDetector, ZeroSpikeDetector, TresholdDetector
from datetime import datetime

class SimpleReporter:
    def analyze(self, series:TimeSeries):
        return f"Info: {series.quantity} at {series.code} has mean={series.mean}"


if __name__ == "__main__":
    test_dates = [
        datetime(2023, 1, 1, 0, 5),
        datetime(2023, 1, 1, 1, 6),
        datetime(2023, 1, 1, 2, 8),
        datetime(2023, 1, 1, 3, 10),
        datetime(2023, 1, 1, 4, 11),
        datetime(2023, 1, 1, 5, 16),
        datetime(2023, 1, 1, 5, 19),
        datetime(2023, 1, 1, 5, 22),
        datetime(2023, 1, 1, 5, 26)
    ]
    test_values = [11.4, 18.9, 14.2, 22.7, 19.5, 35.3, None, None, None]
    timeseries_test = TimeSeries("PM25", "STAT001", "24g", test_dates, test_values, "g")
    analyzers_list = [
        OutlierDetector(1),
        ZeroSpikeDetector(),
        TresholdDetector(5),
        SimpleReporter(),
    ]
    for analyzer in analyzers_list:
        print(analyzer.analyze(timeseries_test))
