from pydantic import BaseModel, Field
from typing import Generic, Optional, TypeVar

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    data: Optional[T] = Field(
        default={},
        description="The output data of an api call"
    )

    message: Optional[str] = Field(
        default=None,
        description="Message describing the response"
    )


class Response(APIResponse[T]):

    def __init__(
        self,
        data: Optional[T] = {},
        message: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            data=data,
            message=message or "Operation successfull"
        )


def success_response(
    data: Optional[T] = {},
    message: Optional[str] = None
) -> APIResponse[T]:
    """"""
    return Response(data=data if data else {}, message=message)
