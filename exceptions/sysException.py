from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import JSONResponse
 
 
"""自定义全局系统错误"""
async def sysExceptionHandler(request: Request, exc: Exception):
    ret = {}
    ret["code"] = 500
    ret["msg"] = "Internal system error!"
    ret["data"] = None
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(ret)) 