from src.books.models import Book, BorrowedBook
from src.core.dao import BaseDAO


class BookDAO(BaseDAO[Book]):
    def __init__(self) -> None:
        super().__init__(Book)


class BorrowedBookDAO(BaseDAO[BorrowedBook]):
    def __init__(self) -> None:
        super().__init__(BorrowedBook)


book_dao = BookDAO()
borrowed_book_dao = BorrowedBookDAO()
