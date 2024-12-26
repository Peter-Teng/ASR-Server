from fastapi import APIRouter, Request
from entity.audio import Audio
from entity.responseObject import response
from utils.logger import getLogger
from service.denoise import DenoiseService
import time


router = APIRouter(prefix="/denoise")


@router.post("/do")
def denoiseAndSave(request:Request, audio: Audio):
    '''
    @description: 对传入路径的音频文件进行去噪并保存（POST方法）
    @param {Request} request 请求基本信息对象
    @param {Audio} audio 音频文件（主要提取其路径参数）
    @return {respose}
    '''
    LOGGER = getLogger()
    LOGGER.info("[%s] - Receive from [%s] - Path[%s]" % (request.method, request.client.host, request.url.path))
    
    start = time.time()  # 记录开始时间
    denoiseService = DenoiseService()
    _, savePath = denoiseService.denoiseFile(path=audio.path, save=True)
    data = {}
    data["path"] = savePath
    elapse_time = time.time() - start
    LOGGER.debug("Inference Time : %2.2f ms" % (elapse_time * 1000))
    return response.success(data)