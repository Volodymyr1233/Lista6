import csv
import os
import re
from datetime import datetime
from TimeSeries import TimeSeries
from SeriesValidator import *

def read_csv(path:str):
    if not (os.path.exists(path) and os.access(path, os.R_OK) and os.path.isfile(path) and path.lower().endswith(".csv")):
        raise ValueError("Cannot read CSV file")
    else:
        return list(csv.reader(open(path, "r")))




class Measurements:
    def __init__(self,csv_dir):
        self.csv_dir = csv_dir
        self.__len=0
        self._dTimeSeries:dict[str,list[tuple[TimeSeries,str]]] | dict[str,[TimeSeries]] = dict() #[code,[TimeSeries]] or [code,[(preTimeSeries,path,index)]]
        self._preload() #laduje TimeSerie leniwie
    def __len__(self):
        return self.__len
    def _preload(self):
        for item in os.scandir(self.csv_dir):
           if self._validate_path(item.path):
               features = self._get_features_measure_name(item.name)
               if features is None:
                   continue
               self._add_preTimeStamps(item.path)

    def _add_preTimeStamps(self,path:str):
        reader = csv.reader(open(path,"r",encoding="utf-8"))
        data = []
        for i,row in enumerate(reader):
            if i < 6:
                data.append(row)
            else:
                break
        if len(data) != 6:
            raise ValueError(f"Data is not correct in {path}")

        for x in range(1, len(data[0])):
            Kod = data[1][x]  # 1
            Wskaznik = data[2][x]  # 2
            Czestotliwosc = data[3][x]  # 3  # czas usredniania
            Jednostka = data[4][x]
            t = TimeSeries(Wskaznik,Kod,Czestotliwosc,[],[],Jednostka)
            if Kod not in self._dTimeSeries:
                self._dTimeSeries[Kod] = [(t, path,x)]
            else:
                self._dTimeSeries[Kod].append((t, path,x))
            self.__len+=1

    def __contains__(self,parameter_name: str):
        for lst in self._dTimeSeries.values():
            for t in lst:
                if isinstance(t,tuple):
                    timeSerie = t[0]
                else:
                    timeSerie = t
                if timeSerie.quantity == parameter_name:
                    return True
        return False

    def _full_load_serie(self,code:str):
        """Load all TimeSerie from dict[code]"""
        if code not in self._dTimeSeries:
            raise ValueError(f"code is not in self._dTimeSeries")
        new_list = []
        for ts in self._dTimeSeries[code]:
            if isinstance(ts,tuple):
                new_list.append(self._full_load_TimeSeries(ts[0],ts[1],ts[2]))
            else:
                new_list.append(ts)
        self._dTimeSeries[code] = new_list
        return new_list

    def _full_load_TimeSeries(self,s:TimeSeries,path:str,index:int)->TimeSeries:
        """:returns Full Loaded TimeSerie"""
        reader = csv.reader(open(path, "r", encoding="utf-8"))
        times = []
        values = []
        for i, row in enumerate(reader):
            if i < 6:
                continue
            t = row[0]
            v = row[index]
            if v != "":
                try:
                    values.append(float(v))
                except ValueError:
                    raise ValueError(f"Value {v} is not float in {path},line: {i+1}")
                try:
                    times.append(datetime.strptime(t, '%m/%d/%y %H:%M'))
                except ValueError:
                    raise ValueError(f"Timestamp {t} is not correct in {path},line: {i+1}")
                times.append(t)
                values.append(v)
        return TimeSeries(s.quantity,s.code,s.frequency,times,values,s.unit)


    def get_by_parameter(self,param_name: str):
        result = []
        for b in self._dTimeSeries.values():
            for t in b:
                if isinstance(t,tuple):
                    ts= t[0]
                else:
                    ts= t
                if ts.quantity == param_name or ts.code==param_name or  ts.frequency==param_name  or ts.unit==param_name:
                        if isinstance(t,tuple):
                            result.append(self._full_load_TimeSeries(t[0],t[1],t[2]))
                        else:
                            result.append(ts)
        return result
    def get_by_station(self,station_code: str) -> list[TimeSeries]:
        if station_code in self._dTimeSeries:
            self._full_load_serie(station_code)
            return self._dTimeSeries[station_code]
        else:
            return []
    def detect_all_anomalies(self,validators:list[SeriesValidator], preload: bool = False)->dict:
        result = dict()
        # [code,[TimeStamps]] or [code,[(preTimeStamp,path,index)]]
        if not preload:
            for code,items in self._dTimeSeries.items():
                for item in items:
                    if isinstance(item,tuple):
                        continue
                    for v in validators:
                        a = v.analyze(item)
                        if a != '':
                            if not code in result:
                                result[code] = [a]
                            else:
                                result[code].append(a)
        else:
            for code in self._dTimeSeries:
                self._full_load_serie(code)
            for code, items in self._dTimeSeries.items():
                for item in items:
                    for v in validators:
                        a = v.analyze(item)
                        if a != '':
                            if not code in result:
                                result[code] = [a]
                            else:
                                result[code].append(a)
        return result
    def _validate_path(self,path:str)->bool:
        return os.path.exists(path) and os.access(path, os.R_OK) and os.path.isfile(path) and path.lower().endswith(".csv")
    def _get_features_measure_name(self, csv_name:str)->tuple | None:
        year = re.findall('\d{4}', csv_name)
        name = re.findall('_(.+)_', csv_name)
        freq = re.findall('_(\d+g)', csv_name)
        if year != [] and name != [] and freq != []:
            year = year[0]
            name = name[0]
            freq = freq[0]
            return year,name,freq
        else:
            return None



if __name__ == "__main__":
    path = "test_5"
    x = Measurements(path)
    print(len(x))
    print(x.__contains__('BkF(PM10)'))
    print(x.__contains__('asdasasd'))
    for item in x.get_by_parameter('ng/m3'):
        print(item.quantity,item.code,item.frequency,item.unit,len(item.values),len(item.timestamps)) #jesli len nie jest zerem to znaczy ze zaladowalo values
    counter = 0
    x._full_load_serie('PmLebaRabka1')
    for k,item in x._dTimeSeries.items():
        counter +=len(item)
        print(f'{k}: {item}')
    print('czy zgadza sie ilosc TimeSeries: ',counter == len(x),len(x))
    assert (counter == len(x)) #jesli przejdzie to dziala
    print('x.get_by_station(DsLegAlRzecz):',x.get_by_station('DsLegAlRzecz'))
    print("not_preloaded:")
    not_preload = x.detect_all_anomalies([OutlierDetector(1),ZeroSpikeDetector(),TresholdDetector(0.1)],False)
    for k,v in not_preload.items():
        print(f'{k}: {v}')
    print()
    print("preloaded:")
    preload = x.detect_all_anomalies([OutlierDetector(1),ZeroSpikeDetector(),TresholdDetector(0.1)],True)
    for k,v in preload.items():
        print(f'{k}: {v}')
