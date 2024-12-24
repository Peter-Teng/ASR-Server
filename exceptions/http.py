from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from entity.responseObject import response

 
"""自定义处理HTTPException"""
async def httpExceptionHandler(request, exc: HTTPException):
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        # 处理404错误
        msg = "Not Found"
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(response.failure("404", msg))) 
    elif exc.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
        # 处理405错误
        msg = "Method Not Allowed"
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(response.failure("405", msg))) 
    else:
        msg = "See logs for more detail"
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(response.failure("-2", msg))) 