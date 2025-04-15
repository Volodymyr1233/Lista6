class Station:
    def __init__(self, code, title, city, address, latitude, longitude):
        self.code = code
        self.title = title
        self.city = city
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        code_string = f"Kod stacji: {self.code}"
        title_string = f"Nazwa stacji: {self.title}"
        city_string = f"Misto: {self.city}"
        address_string = f"Adres: {self.address}"
        latitude_string = f"Szerokość geograficzna: {self.latitude}"
        longitude_string = f"Długość geograficzna: {self.longitude}"

        result_string = f"{code_string}\n{title_string}\n{city_string}\n{address_string}\n{latitude_string}\n{longitude_string}"
        return result_string

    def __repr__(self):
        return f"Station('{self.code}', '{self.title}', '{self.city}', '{self.address}', {self.latitude}, {self.longitude})"

    def __eq__(self, other):
        if isinstance(other, Station):
            return self.code == other.code
        return False
