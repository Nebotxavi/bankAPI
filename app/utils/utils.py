import datetime

# TODO: consider adding encryption if that respects the sequentiallity


class IdGenerator:
    @classmethod
    def get_id(cls):
        return str(int(datetime.datetime.now().timestamp()*100000))
