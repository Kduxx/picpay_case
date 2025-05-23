from pydantic import BaseModel, Field
from typing import Generic, Optional, TypeVar
from enum import Enum

T = TypeVar('T')


class ResponseStatus(str, Enum):
    """Standardize the response types"""
    SUCCESS = "success"
    FAIL = "fail"
    ERROR = "error"


class APIResponse(BaseModel, Generic[T]):
    status: ResponseStatus = Field(
        default=None,
        description="Response status of the api call"
    )

    data: Optional[T] = Field(
        default={},
        description="The output data of an api call"
    )

    message: Optional[str] = Field(
        default=None,
        description="Message describing the response"
    )


class SuccessResponse(APIResponse[T]):

    def __init__(
        self,
        data: Optional[T] = {},
        message: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
                status=ResponseStatus.SUCCESS,
                data=data,
                message=message or "Operation successfull"
        )


class FailResponse(APIResponse[T]):

    def __init__(
        self,
        message: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
                status=ResponseStatus.FAIL,
                message=message or "Unhandled error"
        )


class ErrorResponse(APIResponse[T]):
    status: ResponseStatus = ResponseStatus.ERROR

    def __init__(
        self,
        message: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
                status=ResponseStatus.ERROR,
                message=message or "Internal Server Error"
        )


def success_response(
    data: Optional[T] = {},
    message: Optional[str] = None
) -> APIResponse[T]:
    """"""
    return SuccessResponse(data=data if data else {}, message=message)


def fail_response(
    message: Optional[str] = "Unhandled error"
) -> APIResponse[T]:
    return FailResponse(message=message)


def error_response(
        data: Optional[T] = {},
        message: Optional[str] = None
) -> APIResponse[T]:
    """"""
    return ErrorResponse(data=data if data else {}, message=message)
