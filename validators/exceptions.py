from typing import Any


class ValidationError(Exception):
    def __init__(self, detail: Any):
        self.detail = detail
