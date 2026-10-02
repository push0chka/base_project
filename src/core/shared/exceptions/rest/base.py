import json
from types import EllipsisType
from typing import TypeAlias, Any

DefaultValue: TypeAlias = EllipsisType | Any


class BaseRestException(Exception):
    message: str = "No msg"
    status: int = 400
    err_code: str = "400"

    def __init__(
        self, message: str | None = None, status: int | None = None, **kwargs
    ) -> None:
        self._message = message or self.message
        self._status = status or self.status
        self.details = kwargs or {}
        self.details.setdefault("message", self._message)
        self.details.setdefault("err_code", self.err_code)

        super().__init__(self._message, self._status, self.details)

    def __repr__(self) -> str:
        if self.details:
            return json.dumps(self.details)
        return super().__repr__()

    @classmethod
    def details_fields(cls) -> dict[str, tuple[type, DefaultValue]]:
        # NOTE: If you are using custom pydantic schemas in the exceptions
        # import them in this function (default importing may raise circular
        # error)

        return {}

    @classmethod
    def get_subclasses(cls):
        all_subclasses = []
        for subclass in cls.__subclasses__():
            all_subclasses.append(subclass)
            all_subclasses.extend(subclass.get_subclasses())
        return all_subclasses

    @classmethod
    def check_err_codes_duplicates(cls):
        err_codes = set()
        for subclass in cls.get_subclasses():
            if subclass.err_code in err_codes and subclass.err_code != "400":
                raise ValueError(
                    f"Error code {subclass.err_code} "
                    f"is duplicated in {subclass}"
                )
            err_codes.add(subclass.err_code)
