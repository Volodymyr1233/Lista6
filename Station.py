class Station:
    def __init__(self, code: str, title: str, city: str, address:str, latitude:float, longitude:float) -> None:
        self.code = code
        self.title = title
        self.city = city
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self) -> str:
        code_string = f"Kod stacji: {self.code}"
        title_string = f"Nazwa stacji: {self.title}"
        city_string = f"Misto: {self.city}"
        address_string = f"Adres: {self.address}"
        latitude_string = f"Szerokość geograficzna: {self.latitude}"
        longitude_string = f"Długość geograficzna: {self.longitude}"

        result_string = f"{code_string}\n{title_string}\n{city_string}\n{address_string}\n{latitude_string}\n{longitude_string}"
        return result_string

    def __repr__(self) -> str:
        return f"Station('{self.code}', '{self.title}', '{self.city}', '{self.address}', {self.latitude}, {self.longitude})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Station):
            return self.code == other.code
        return False

if __name__ == "__main__":
    #__str__ and __repr__ method
    station1 = Station("123", "Stacja Główna", "Warszawa", "ul. Długa 1", 52.2297, 21.0122)
    print("--- __str__ method ---")
    print(station1)
    print("--- __repr__ method ---")
    print(repr(station1))

    #__eq__ method
    print("--- __eq__ method ---")
    s1 = Station("789", "Stacja 1", "Gdańsk", "ul. Zielona 3", 54.3520, 18.6466)
    s2 = Station("789", "Stacja 2", "Poznań", "ul. Czerwona 7", 52.4064, 16.9252)
    print(f"s1 and s2 are the same: {s1 == s2}")
