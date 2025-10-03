class Rune:
    def __init__(self, id, name_fr, characteristic_fr, value, weight, price, date_updated):
        self.id = id
        self.name_fr = name_fr
        self.characteristic_fr = characteristic_fr
        self.value = value
        self.weight = weight
        self.price = price
        self.date_updated = date_updated

    def as_tuple(self):
        return (
            self.id,
            self.name_fr,
            self.characteristic_fr,
            self.value,
            self.weight,
            self.price,
            self.date_updated
        )