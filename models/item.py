class Characteristic:
    def __init__(self, name: str, min_value: int, max_value: int):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value

    def as_dict(self):
        return {
            "Caractéristique": self.name,
            "Min": self.min_value,
            "Max": self.max_value
        }


class Item:
    def __init__(self, id: int, name: str, type_: str, level: int, coefficient: int, price: int, characteristics: list):
        self.id = id
        self.name = name
        self.type = type_
        self.level = level
        self.coefficient = coefficient
        self.price = price
        self.characteristics = characteristics  # List of Characteristic objects

    def as_dict(self):
        return {
            "id": self.id,
            "Nom": self.name,
            "Type": self.type,
            "Niveau": self.level,
            "Coefficient": self.coefficient,
            "Prix": self.price,
            "Caractéristiques": [c.as_dict() for c in self.characteristics]
        }
