from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.encoding import force_str


class CustomAPIException(APIException):
    def __init__(
        self, detail=None, field=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        if field and detail:
            detail = {field: force_str(detail), "status": status_code}
        elif detail:
            detail = {"detail": force_str(detail), "status": status_code}
        else:
            detail = {"detail": "A server error occurred.", "status": status_code}

        self.status_code = status_code
        self.detail = detail


class HashMismatchException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
