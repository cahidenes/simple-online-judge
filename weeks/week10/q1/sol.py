class Saat:
    def __init__(self, saat=0, dakika=0):
        self.saat = saat
        self.dakika = dakika

    def __repr__(self):
        return f"{self.saat:02}:{self.dakika:02}"
