
class Address:
    full = ""
    pref = ""
    city = ""
    town = ""
    extra1 = ""
    extra2 = ""
    zip7 = None

    def __init__(self, address):
        self.full = address