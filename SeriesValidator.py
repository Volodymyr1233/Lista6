import abc
import math
from abc import ABC
from numbers import Number

from TimeSeries import TimeSeries

class SeriesValidator(abc.ABC):
    @abc.abstractmethod
    def analyze(self, series:TimeSeries)->str:
        pass




class OutlierDetector(SeriesValidator):
    """OutlierDetector, która wykrywa wartości oddalone o więcej niż k odchyleń
standardowych od średniej, gdzie k jest parametrem klasy"""
    def __init__(self, k:int):
        if k <=0:
            raise ValueError("k must be positive")
        self.k = k
    def analyze(self, series: TimeSeries)->str:
        mean  = series.mean
        std = series.stddev

        if mean is None or std is None:
            raise ValueError("Cannot get mean/stddev for series")
        for value in series.values:
            if (not math.isnan(value)) and abs(mean - value) > self.k* std:
                return "OutlierDetector anomaly"
        return ""



class ZeroSpikeDetector(SeriesValidator):

    def analyze(self, series: TimeSeries) -> str:
        counter_zeroes = 0
        counter_nonevalues = 0
        for value in series.values:
            if math.isnan(value):
                counter_nonevalues +=1
            elif value == 0:
                counter_zeroes+=1
        return f"ZeroSpikeDetector anomaly" if (counter_zeroes >= 3 or counter_nonevalues >= 3) else ""

class TresholdDetector(SeriesValidator):
    def __init__(self, treshold:float):
        self.treshold = treshold
    def analyze(self, series: TimeSeries)->str:
        for value in series.values:
            if math.isnan(value):
                continue
            elif value > self.treshold:
                return "Treshold anomaly"
        return ""

class CompositeValidator(SeriesValidator):
    def __init__(self, *validators:SeriesValidator,mode:str='OR'):
        """modes: OR AND"""
        if mode not in ('OR','AND'):
            raise ValueError("Invalid mode")
        self.validators = validators
        self.mode = mode

    def analyze(self, series: TimeSeries) -> str:
        match(self.mode):
            case 'OR':
                b= self._OR(series)
            case 'AND':
                b = self._AND(series)
        return "Composite anomaly" if b else ""

    def _AND(self,series:TimeSeries)->bool:
        b = True
        for validator in self.validators:
            try:
                temp = validator.analyze(series)
                if temp == "":
                    b = False
                    break
            except ValueError as e:
                raise ValueError(f'Failed to get analyze from {validator}: {e}')
        return b
    def _OR(self,series:TimeSeries)->bool:

        for validator in self.validators:
            try:
                temp = validator.analyze(series)
                if temp != "":
                    b = True
                    break
            except ValueError as e:
                raise ValueError(f'Failed to get analyze from {validator}: {e}')
        return b




if __name__ == '__main__':
    from datetime import datetime, date
    daty = [
        datetime(2024, 1, 1, 8),
        datetime(2024, 1, 1, 9),
        datetime(2024, 1, 1, 10),
        datetime(2024, 1, 2, 11),
        datetime(2024, 1, 2, 12),
        datetime(2024, 1, 2, 13),
        datetime(2024, 1, 2, 14),
        datetime(2024, 1, 2, 15),
        datetime(2024, 1, 2, 16),
        datetime(2024, 1, 2, 17)
    ]

    wartosci = [15.2, 16.8, None, 18.0,15.0,9999.0,12.0,0,0,0]

    ts = TimeSeries(0, 0, 0, daty, wartosci, 0)

    print('-',OutlierDetector(1).analyze(ts))#Powinno być OutlierDetector
    print('-',OutlierDetector(3).analyze(ts))#Nic nie powinno byc
    print('-',ZeroSpikeDetector().analyze(ts))#Powinno być ZeroSpikeDetector
    print('-',TresholdDetector(20).analyze(ts))#Powinno być Treshold
    print('-',CompositeValidator(OutlierDetector(1),OutlierDetector(3),ZeroSpikeDetector(),TresholdDetector(20),mode="AND").analyze(ts)) #NIe powinno nic byc
    print('-',CompositeValidator(OutlierDetector(1),OutlierDetector(3),ZeroSpikeDetector(),TresholdDetector(20),mode="OR").analyze(ts)) #Powinno być


