from src.books.models import Book
from src.core.dao import BaseDAO


class BookDAO(BaseDAO[Book]):
    def __init__(self) -> None:
        super().__init__(Book)


book_dao = BookDAO()
