from fastapi import APIRouter
from fastapi import Request
from pydantic import BaseModel
from service.transcribe import transcribeModel
from utils.logger import getLogger
import time


router = APIRouter(prefix="/transcribe")


class Audio(BaseModel):
    path: str


@router.post("/do")
async def transcribe(request:Request, audio: Audio):
    LOGGER = getLogger()
    LOGGER.info("[%s] - Receive from [%s] - Path[%s]" % (request.method, request.client.host, request.url.path))
    path = audio.path
    
    start = time.time()  # 记录开始时间
    service = transcribeModel()
    data = service.transcribe(path)
    elapse_time = time.time() - start
    LOGGER.debug("Inference Time : %2.2f ms" % (elapse_time * 1000))
    LOGGER.debug(str(data))
    return {"code": "0", "msg": "success", "data": data}
