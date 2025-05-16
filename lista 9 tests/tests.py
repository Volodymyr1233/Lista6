from SeriesValidator import OutlierDetector, ZeroSpikeDetector, TresholdDetector
from TimeSeries import TimeSeries
import numpy as np
import pytest


def detector_result(detector,values)->bool:
    TimeSeries(0, 0, 0, [], values, 0)
    return detector.analyze(values)!=''

def test_outlier():
    k = 3
    detector = OutlierDetector(k)
    wartosci = [1]*30 + [100]

    assert(detector_result(detector,wartosci))
    detector = OutlierDetector(k+1)
    assert(detector_result(detector,wartosci)==False)

def test_zerospike():
    detector = ZeroSpikeDetector()
    wartosci = [1] * 15 + [100]
    assert(detector_result(detector,wartosci)==False)
    wartosci += [0]*2
    assert(detector_result(detector,wartosci))
    wartosci += [0]*5
    assert(detector_result(detector,wartosci))
    wartosci = [1]*5 + [None]*3
    assert(detector_result(detector,wartosci))

def test_treshold():
    wartosci = [1] * 15
    ts = TimeSeries(0, 0, 0, [], wartosci, 0)
    detector = TresholdDetector(5)
    assert(detector.analyze(ts)=='')
    wartosci += [5]
    ts = TimeSeries(0, 0, 0, [], wartosci, 0)
    assert(detector.analyze(ts)=='')
    wartosci += [100]
    ts = TimeSeries(0, 0, 0, [], wartosci, 0)
    assert(detector.analyze(ts)!='')

    wartosci = [1]*15 + [None]*3
    ts = TimeSeries(0, 0, 0, [], wartosci, 0)
    assert(detector.analyze(ts)=='')

