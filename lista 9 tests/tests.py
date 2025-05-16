
from SeriesValidator import *
from TimeSeries import TimeSeries
import pytest


def detector_result(detector,values)->bool:
    ts = TimeSeries(0, 0, 0, [], values, 0)
    return detector.analyze(ts)!=''

def test_outlier():
    k = 3
    detector = OutlierDetector(k)
    wartosci = [1]*30 + [100]
    assert detector_result(detector,wartosci)
    detector = OutlierDetector(k+5)
    assert(not detector_result(detector,wartosci))


def test_zerospike():
    detector = ZeroSpikeDetector()
    wartosci = [1] * 15 + [100]
    assert(not detector_result(detector,wartosci))
    wartosci += [0]*2
    assert(not detector_result(detector,wartosci))
    wartosci += [0]*5
    assert(detector_result(detector,wartosci))
    wartosci = [1]*5 + [None]*3
    assert(detector_result(detector,wartosci))

def test_treshold():
    wartosci = [1] * 15
    detector = TresholdDetector(5)
    assert not detector_result(detector,wartosci)
    wartosci += [5]
    assert not detector_result(detector, wartosci)
    wartosci += [100]
    assert detector_result(detector,wartosci)
    wartosci = [1]*15 + [None]*3
    assert not detector_result(detector,wartosci)

@pytest.mark.parametrize("analyzers,inp,out",[
    ([OutlierDetector(1),ZeroSpikeDetector(),TresholdDetector(200)],[0]*30+[100],[1,1,0])

])


def test_detect_all_anomalies(analyzers,inp,out): # out [1,0,1,0 ,0 znaczy ze nie ma anomali
    ts = TimeSeries(0, 0, 0, [], inp, 0)
    for analyzer,o in zip(analyzers,out):
        try:
            assert ((analyzer.analyze(ts)=='' and o==0) or o==1)
        except AttributeError as e:
            raise e