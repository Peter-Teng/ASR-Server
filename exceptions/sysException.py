from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from entity.responseObject import response
 
 
 
"""自定义全局系统错误"""
async def sysExceptionHandler(request: Request, exc: Exception):
    msg = f"Internal system error! [{repr(exc)}]"
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(response.failure("-1", msg))) 