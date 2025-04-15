from Station import Station

def test(name):
    station1 = Station("DsBialka", "Białka", "Białka", "", 51.197783, 16.11739)
    print(station1.__repr__())

if __name__ == '__main__':
    test('PyCharm')

