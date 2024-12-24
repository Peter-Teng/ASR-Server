from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from entity.responseObject import response


""" 自定义参数验证异常错误"""
async def validationExceptionHandler(request: Request, exc: RequestValidationError):
    msg = ""
    for error in exc.errors():
        msg += ".".join(error.get("loc")) + ":" + error.get("msg") + ";"
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(response.failure("400", msg))) 