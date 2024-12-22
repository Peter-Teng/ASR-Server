from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
 
"""自定义处理HTTPException"""
async def httpExceptionHandler(request, exc: HTTPException):
    ret = {}
    ret["code"] = -1
    ret["data"] = None
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        # 处理404错误
        ret["msg"] = "Not Found"
        return JSONResponse(
            content=jsonable_encoder(ret),
            status_code=status.HTTP_200_OK,
        )
    elif exc.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
        # 处理405错误
        ret["msg"] = "Method Not Allowed"
        return JSONResponse(
            content=jsonable_encoder(ret),
            status_code=status.HTTP_200_OK,
        )
    else:
        ret["msg"] = "See logs for more detail"
        return JSONResponse(
            content=jsonable_encoder(ret),
            status_code=status.HTTP_200_OK,
        )