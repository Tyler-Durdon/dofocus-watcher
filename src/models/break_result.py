from dataclasses import dataclass


@dataclass
class BreakResult:
    item_id: int
    item_name: str
    characteristic: str
    rune_name: str
    runes_generated: int
    rune_price: float
    best_rune: str  # "yes" ou "no"

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
