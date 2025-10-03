class DofusItem:
    def __init__(self, id, name_fr, type_fr, level):
        self.id = id
        self.name_fr = name_fr
        self.type_fr = type_fr
        self.level = level

    def as_tuple(self):
        return (self.id, self.name_fr, self.type_fr, self.level)
