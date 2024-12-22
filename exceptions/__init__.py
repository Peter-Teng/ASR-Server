from fastapi import FastAPI
from .validation import validationExceptionHandler
from .http import httpExceptionHandler
from .sysException import sysExceptionHandler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
 
 
""" 统一注册错误处理器"""
def registerExceptionHandler(app: FastAPI):
    # 注册参数验证错误,并覆盖模式RequestValidationError
    app.add_exception_handler(RequestValidationError, validationExceptionHandler)
    # 错误处理StarletteHTTPException
    app.add_exception_handler(StarletteHTTPException, httpExceptionHandler)
    # 自定义系统全局系统错误
    app.add_exception_handler(Exception, sysExceptionHandler)