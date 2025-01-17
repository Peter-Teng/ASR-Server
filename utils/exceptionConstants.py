from fastapi import status


class ExceptionConstants:
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = "-1"
    msg = "Unknown Error"

    def __init__(self, status_code, code, msg):
        self.status_code = status_code
        self.code = code
        self.msg = msg


FILE_NOT_FOUND = ExceptionConstants(status.HTTP_200_OK, "-404", "文件不存在")