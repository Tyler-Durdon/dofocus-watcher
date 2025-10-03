from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Characteristic:
    name: str
    min_value: int
    max_value: int

    @classmethod
    def from_api(cls, data: dict):
        return cls(
            name=data.get("name", {}).get("fr", "") or "",
            min_value=data.get("from", 0) or 0,
            max_value=data.get("to", 0) or 0
        )

@dataclass
class Item:
    id: int
    name_fr: str
    type_fr: str
    level: int
    coefficient: Optional[float] = None
    price: Optional[float] = None
    characteristics: List[Characteristic] = field(default_factory=list)
    
    @classmethod
    def from_api(cls, data: dict):
        """Crée une instance d'Item à partir des données de l'API"""
        return cls(
            id=data.get("id"),
            name_fr=data.get("name", {}).get("fr", "") or "",
            type_fr=(data.get("type", {}) .get("name", {}) .get("fr", "")) if data.get("type") else "",
            level=data.get("level", 0) or 0,
            characteristics=[
                Characteristic.from_api(c)
                for c in data.get("characteristics", [])
                if (c.get("name", {}).get("fr", "") or "").lower() != "unknown characteristic"
            ]
        )
