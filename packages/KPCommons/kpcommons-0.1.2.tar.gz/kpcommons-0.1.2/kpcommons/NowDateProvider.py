from datetime import datetime

from kpcommons.DateProvider import DateProvider


class NowDateProvider(DateProvider):

    # overriding abstract method
    def get_date(self) -> datetime:
        return datetime.now()