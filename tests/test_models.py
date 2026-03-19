import pytest
from models import Book

def test_book_creation():
    """Тест создания книги"""
    book = Book("Война и мир", "Толстой", "Роман", 1869, "Описание")
    assert book.title == "Война и мир"
    assert book.author == "Толстой"
    assert book.genre == "Роман"
    assert book.year == 1869
    assert book.description == "Описание"
    assert book.status == "не прочитана"
    assert book.id is not None

def test_book_to_dict():
    """Тест преобразования книги в словарь"""
    book = Book("Война и мир", "Толстой", "Роман", 1869, "Описание", id=1)
    data = book.to_dict()
    assert data['title'] == "Война и мир"
    assert data['author'] == "Толстой"
    assert data['id'] == 1

def test_book_from_dict():
    """Тест создания книги из словаря"""
    data = {
        'title': 'Война и мир',
        'author': 'Толстой',
        'genre': 'Роман',
        'year': 1869,
        'description': 'Описание',
        'status': 'прочитана',
        'id': 1
    }
    book = Book.from_dict(data)
    assert book.title == 'Война и мир'
    assert book.status == 'прочитана'
    assert book.id == 1