import datetime


class IdGenerator:
    @classmethod
    def get_id(cls) -> int:
        return int(datetime.datetime.now().timestamp()*100000)
