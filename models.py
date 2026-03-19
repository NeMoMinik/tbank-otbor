from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


@dataclass
class Book:
    """Модель книги"""
    title: str
    author: str
    genre: str
    year: int
    description: str
    status: str = "не прочитана"
    id: Optional[int] = None

    def __post_init__(self):
        if self.id is None:
            self.id = id(self)  # Временный ID, будет заменен при сохранении

    def to_dict(self):
        """Преобразование книги в словарь для сохранения"""
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data):
        """Создание книги из словаря"""
        return cls(**data)

    def __str__(self):
        return f"[{self.id}] {self.title} - {self.author} ({self.year}) - {self.status}"