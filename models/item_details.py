class ItemDetails:
    def __init__(self, id, name_fr, type_fr, level, coefficient, price, characteristics):
        self.id = id
        self.name_fr = name_fr
        self.type_fr = type_fr
        self.level = level
        self.coefficient = coefficient
        self.price = price
        self.characteristics = characteristics  # List of dicts: {"Caractéristique": ..., "Min": ..., "Max": ...}

    def as_tuple(self):
        return (self.id, self.name_fr, self.type_fr, self.level, self.coefficient, self.price)

    def characteristics_tuples(self):
        return [(self.id, c["Caractéristique"], c["Min"], c["Max"]) for c in self.characteristics]
