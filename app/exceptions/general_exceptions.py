class NoUniqueElement(Exception):
    pass


class ResourceNotFound(Exception):
    pass


class ImmutableFieldError(Exception):
    def __init__(self, field_name: str):
        self.field_name = field_name
        super().__init__(f"Modification not allowed for field: {field_name}")
