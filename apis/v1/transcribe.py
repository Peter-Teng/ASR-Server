import io
import os
from datetime import datetime

from fastapi import APIRouter
from fastapi import Request
from fastapi import File, Form
from pydantic import BaseModel
from pydub import AudioSegment

from service.transcribe import transcribeModel
from utils.logger import getLogger
import time
from typing_extensions import Annotated


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

#单个文件语音识别
@router.post("/file")
async def audio_to_text(request: Request,  # 获取请求对象
                        file: Annotated[bytes, File(description="wav or mp3 audios in 16KHz")],
                        keys: Annotated[str, Form(description="name of each audio joined with comma")],
                        lang: Annotated[str, Form(description="language of audio content")] = "auto"):
    LOGGER = getLogger()
    service = transcribeModel()
    current_date = datetime.now()
    if lang == "":
        lang = "auto"
    if keys == "":
        key = [current_date.strftime("%H%M%S"), "wav"]
    else:
        key = keys.split(".")
    # 将音频保存为 wav 文件
    dir_path = os.path.join(service.conf["file_save_base_dir"], str(current_date.year), str(current_date.month).zfill(2),
                             str(current_date.day).zfill(2))
    # 如果目录不存在，则创建它
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    audio_file_name = os.path.join(dir_path, f"{key[0]}.{key[1]}")
    # 将处理过的数组转成为文件
    audio_file = io.BytesIO(file)
    # 使用 pydub 读取音频数据
    audio = AudioSegment.from_file(audio_file, format=key[1])
    audio.export(audio_file_name, format=key[1])
    LOGGER.info("[%s] - [%s] 开始语音识别 [%s]" % (request.client.host, request.url.path, audio_file_name))
    start = time.time()  # 记录开始时间

    data = service.transcribe(audio_file_name)
    elapse_time = time.time() - start
    LOGGER.info("识别成功，用时 : %2.2f ms" % (elapse_time * 1000))
    LOGGER.debug(str(data))
    return {"code": "0", "describe": "success", "data": data}
