from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from entity.responseObject import response


class ApiException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = "-1"
    msg = "Unknown Error"

    def __init__(self, ExceptionConstants):
        self.status_code = ExceptionConstants.status_code
        self.code = ExceptionConstants.code
        self.msg = ExceptionConstants.msg


"""自定义处理HTTPException"""
async def apiExceptionHandler(request, exc: ApiException):
    return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(response.failure(exc.code, exc.msg))) 