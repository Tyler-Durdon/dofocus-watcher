class DofocusItem:
    def __init__(self, id, name_fr, name_en, name_es, type_fr, type_en, type_es, level, price, img):
        self.id = id
        self.name_fr = name_fr
        self.name_en = name_en
        self.name_es = name_es
        self.type_fr = type_fr
        self.type_en = type_en
        self.type_es = type_es
        self.level = level
        self.price = price
        self.img = img

    def as_tuple(self):
        return (
            self.id,
            self.name_fr,
            self.name_en,
            self.name_es,
            self.type_fr,
            self.type_en,
            self.type_es,
            self.level,
            self.price,
            self.img
        )
