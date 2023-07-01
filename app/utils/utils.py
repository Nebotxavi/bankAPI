import datetime


class IdGenerator:
    @staticmethod
    def get_id() -> int:
        return int(datetime.datetime.now().timestamp()*100000)
