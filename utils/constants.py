from fastapi import status

# Ordinary Constants here
SUCCESS_CODE = 0
SUCCESS_MSG = "success"
SUCCESS_DATA = "OK"

# Exception Constants here
class ExceptionConstants:
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = "-1"
    msg = "Unknown Error"

    def __init__(self, status_code, code, msg):
        self.status_code = status_code
        self.code = code
        self.msg = msg


FILE_NOT_FOUND = ExceptionConstants(status.HTTP_200_OK, "-404", "文件不存在")
SPEAKER_ALREADY_EXISTS = ExceptionConstants(status.HTTP_200_OK, "-200", "讲话人已存在")
SPEAKER_NOT_FOUND = ExceptionConstants(status.HTTP_200_OK, "-404", "讲话人不存在")
EMPTY_AUDIO_REQUEST = ExceptionConstants(status.HTTP_200_OK, "-400", "音频为空")