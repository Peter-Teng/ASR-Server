from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

""" 自定义参数验证异常错误"""
async def validationExceptionHandler(request: Request, exc: RequestValidationError):
    ret = {}
    msg = ""
    for error in exc.errors():
        msg += ".".join(error.get("loc")) + ":" + error.get("msg") + ";"
    ret["code"] = -1
    ret["msg"] = msg
    ret["data"] = None
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(ret))