import io
import os

from fastapi import APIRouter, Request, File, Form
from entity.speaker import Speaker
from entity.responseObject import response
from pydub import AudioSegment

from exceptions.application import ApiException
from utils.exceptionConstants import *
from utils.logger import getLogger
import time
from service.speaker import SpeakerService
from typing_extensions import Annotated

router = APIRouter(prefix="/speaker")

@router.post("/register")
def registerSpeaker(request: Request, speaker: Speaker):
    '''
    @description: 使用json传入路径和说话人名称，注册说话人（POST方法）
    @param {Request} request 请求基本信息对象
    @param {Speaker} speaker 说话人对象
    @return {respose} 是否成功
    '''
    LOGGER = getLogger()
    LOGGER.info("[%s] - Receive from [%s] - Path[%s]" % (request.method, request.client.host, request.url.path))
    path = speaker.audioPath
    name = speaker.name
    if not os.path.exists(path):
        raise ApiException(FILE_NOT_FOUND)
    start = time.time()  # 记录开始时间
    speakerService = SpeakerService()
    data = speakerService.register(path, name)
    elapse_time = time.time() - start
    LOGGER.debug("Inference Time : %2.2f ms" % (elapse_time * 1000))
    return response.success(data)


@router.delete("/{speaker}")
def deleteSpeaker(request: Request, speaker: str):
    '''
    @description: 从URL中传入说话人的名称，删除该说话人（DELETE方法）
    @param {Request} request 请求基本信息对象
    @param {str} speaker 说话人名称
    @return {respose} 是否成功
    '''
    LOGGER = getLogger()
    LOGGER.info("[%s] - Receive from [%s] - Path[%s]" % (request.method, request.client.host, request.url.path))
    speakerService = SpeakerService()
    data = speakerService.delete(speaker)
    return response.success(data)


#远程注册说话人
@router.post("/remoteRegister")
def remote_regist_speaker(request: Request,  # 获取请求对象
                                file: Annotated[bytes, File(description="wav or mp3 audios in 16KHz")],
                                speaker: Annotated[str, Form(description="name of speaker")],
                                format: Annotated[str, Form(description="file format")] = "wav"):
    LOGGER = getLogger()
    speakerService = SpeakerService()
    # 将音频保存为 wav 文件
    dir_path = os.path.join(speakerService.conf["file_save_base_dir"], "speaker")
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
    data = speakerService.register(audio_file_name, speaker)
    elapse_time = time.time() - start
    LOGGER.info("说话人注册成功 : %2.2f ms" % (elapse_time * 1000))
    LOGGER.debug(str(data))
    return response.success(data)



@router.get("/list")
def listSpeakers(request: Request):
    '''
    @description: 列举所有已注册说话人列表（GET方法）
    @param {Request} request 请求基本信息对象
    @return {respose} 所有说话人名称、pt文件路径信息
    '''
    LOGGER = getLogger()
    LOGGER.info("[%s] - Receive from [%s] - Path[%s]" % (request.method, request.client.host, request.url.path))
    speakerService = SpeakerService()
    speakers = speakerService.list()
    return response.success(speakers)
