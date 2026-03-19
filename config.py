import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOOKS_DB = os.getenv('BOOKS_DB', 'books.json')
    FAVORITES_DB = os.getenv('FAVORITES_DB', 'favorites.json')