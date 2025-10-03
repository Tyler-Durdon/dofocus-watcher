class BreakResult:
    def __init__(self, item_id, item_name, characteristic, rune_name, runes_generated, rune_price, best_rune):
        self.item_id = item_id
        self.item_name = item_name
        self.characteristic = characteristic
        self.rune_name = rune_name
        self.runes_generated = runes_generated
        self.rune_price = rune_price
        self.best_rune = best_rune  # Boolean or string

    def as_tuple(self):
        return (
            self.item_id,
            self.item_name,
            self.characteristic,
            self.rune_name,
            self.runes_generated,
            self.rune_price,
            self.best_rune
        )
