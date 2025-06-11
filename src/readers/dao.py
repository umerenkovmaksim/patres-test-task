from src.core.dao import BaseDAO
from src.readers.models import Reader


class ReaderDAO(BaseDAO[Reader]):
    def __init__(self) -> None:
        super().__init__(Reader)


reader_dao = ReaderDAO()
