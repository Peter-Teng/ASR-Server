from fastapi import APIRouter, Request
from pydantic import BaseModel
from utils.logger import getLogger
import time
from service.speaker import speakerService


router = APIRouter(prefix="/speaker")


class Speaker(BaseModel):
    audioPath: str
    name: str


@router.post("/register")
async def registerSpeaker(request: Request, speaker: Speaker):
    LOGGER = getLogger()
    LOGGER.info("[%s] - Receive from [%s] - Path[%s]" % (request.method, request.client.host, request.url.path))
    path = speaker.audioPath
    name = speaker.name
    
    start = time.time()  # 记录开始时间
    service = speakerService()
    data = service.register(path, name)
    elapse_time = time.time() - start
    LOGGER.debug("Inference Time : %2.2f ms" % (elapse_time * 1000))
    return {"code": "0", "msg": "success", "data": data}


@router.delete("/{speaker}")
async def deleteSpeaker(request: Request, speaker: str):
    LOGGER = getLogger()
    LOGGER.info("[%s] - Receive from [%s] - Path[%s]" % (request.method, request.client.host, request.url.path))

    service = speakerService()
    data = service.delete(speaker)
    return {"code": "0", "msg": "success", "data": data}