from abc import ABC, abstractmethod
from datetime import datetime


class DateProvider(ABC):

    @abstractmethod
    def get_date(self) -> datetime:
        pass