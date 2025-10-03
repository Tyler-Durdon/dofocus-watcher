from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

@dataclass
class Rune:
    id: int
    name_fr: str
    characteristic_fr: str
    value: int
    weight: int
    price: Optional[float]
    date_updated: Optional[datetime]
    
    @classmethod
    def from_api(cls, data: dict):
        """Crée une instance de Rune à partir des données de l'API"""
        price_info = next(
            (p for p in data.get("latestPrices", []) if p.get("serverName") == "Salar"),
            None
        )
        date_updated = None
        if price_info and price_info.get("dateUpdated"):
            try:
                date_updated = datetime.fromisoformat(price_info["dateUpdated"].replace('Z', '+00:00'))
            except Exception:
                date_updated = None
        return cls(
            id=data.get("id"),
            name_fr=data.get("name", {}).get("fr", "") or "",
            characteristic_fr=data.get("characteristicName", {}).get("fr", "") or "",
            value=data.get("value", 0) or 0,
            weight=data.get("weight", 0) or 0,
            price=price_info.get("price") if price_info else None,
            date_updated=date_updated
        )

    def as_tuple(self) -> Tuple:
        """Tuple compatible avec la table runes"""
        return (
            self.id,
            self.name_fr,
            self.characteristic_fr,
            self.value,
            self.weight,
            self.price,
            self.date_updated.isoformat() if self.date_updated else None
        )
