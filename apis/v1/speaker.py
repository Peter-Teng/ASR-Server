import io
import os

from fastapi import APIRouter, Request, File, Form
from pydantic import BaseModel
from pydub import AudioSegment

from utils.logger import getLogger
import time
from service.speaker import speakerService
from typing_extensions import Annotated

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


#远程注册说话人
@router.post("/remoteRegister")
async def remote_regist_speaker(request: Request,  # 获取请求对象
                                file: Annotated[bytes, File(description="wav or mp3 audios in 16KHz")],
                                speaker: Annotated[str, Form(description="name of speaker")],
                                format: Annotated[str, Form(description="file format")] = "wav"):
    LOGGER = getLogger()
    service = speakerService()
    # 将音频保存为 wav 文件
    dir_path = os.path.join(service.conf["file_save_base_dir"], "speaker")
    # 如果目录不存在，则创建
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    audio_file_name = os.path.join(dir_path, f"{speaker}.{format}")
    # 将处理过的数组转成为文件
    # 使用 io.BytesIO 将 bytes 数据转换为文件对象
    audio_file = io.BytesIO(file)
    # 使用 pydub 读取音频数据
    audio = AudioSegment.from_file(audio_file, format=format)
    # 导出到本地
    audio.export(audio_file_name, format=format)
    LOGGER.info("[%s] - [%s] 开始注册说话人 - 保存到 [%s]" % (request.client.host, request.url.path, audio_file_name))
    start = time.time()  # 记录开始时间
    data = service.register(audio_file_name, speaker)
    elapse_time = time.time() - start
    LOGGER.info("说话人注册成功 : %2.2f ms" % (elapse_time * 1000))
    LOGGER.debug(str(data))
    return {"code": "0", "describe": "success", "data": data}

#获取已注册列表
@router.get("/list")
async def listSpeakers(request: Request):
    service = speakerService()
    speakers = service.list()
    return {"code": "0", "describe": "success", "data": speakers}
