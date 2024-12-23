from fastapi import APIRouter, Request
from entity.audio import Audio
from utils.logger import getLogger
from service.denoise import denoiseService
import time


router = APIRouter(prefix="/denoise")


@router.post("/do")
async def denoiseAndSave(request:Request, audio: Audio):
    LOGGER = getLogger()
    LOGGER.info("[%s] - Receive from [%s] - Path[%s]" % (request.method, request.client.host, request.url.path))
    
    start = time.time()  # 记录开始时间
    service = denoiseService()
    _, savePath = service.denoiseFile(path=audio.path, save=True)
    elapse_time = time.time() - start
    LOGGER.debug("Inference Time : %2.2f ms" % (elapse_time * 1000))
    return {"code": "0", "msg": "success", "data": savePath}