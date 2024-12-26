import io
import os
from datetime import datetime

from fastapi import APIRouter
from fastapi import Request
from fastapi import File, Form
from entity.audio import Audio
from entity.responseObject import response
from pydub import AudioSegment
from starlette.websockets import WebSocket, WebSocketDisconnect

from service.transcribe import TranscribeService
from service.denoise import DenoiseService
from utils.logger import getLogger
import time
from typing_extensions import Annotated


router = APIRouter(prefix="/transcribe")


@router.post("/do")
def transcribe(request:Request, audio: Audio):
    '''
    @description: 对以Json格式传入路径下的音频文件进行语音识别（POST方法）
    @param {Request} request 请求基本信息对象
    @param {Audio} audio 音频对象（路径）
    @return {respose} 语音识别内容
    '''
    LOGGER = getLogger()
    LOGGER.info("[%s] - Receive from [%s] - Path[%s]" % (request.method, request.client.host, request.url.path))
    path = audio.path
    transcribeService = TranscribeService()
    start = time.time()  # 记录开始时间
    data = transcribeService.transcribe(path)
    elapse_time = time.time() - start
    LOGGER.debug("Inference Time : %2.2f ms" % (elapse_time * 1000))
    return response.success(data)



@router.post("/denoised")
def denoiseAndTranscribe(request:Request, audio: Audio):
    '''
    @description: 对以Json格式传入路径下的音频文件进行去噪并语音识别（POST方法）
    @param {Request} request 请求基本信息对象
    @param {Audio} audio 音频对象（路径）
    @return {respose} 语音识别内容
    '''
    LOGGER = getLogger()
    LOGGER.info("[%s] - Receive from [%s] - Path[%s]" % (request.method, request.client.host, request.url.path))
    path = audio.path
    start = time.time()  # 记录开始时间
    transcribeService = TranscribeService()
    denoiseService = DenoiseService()
    speech, _ = denoiseService.denoiseFile(path=path, save=False)
    data = transcribeService.transcribe(path=path, speech=speech)
    elapse_time = time.time() - start
    LOGGER.debug("Inference Time : %2.2f ms" % (elapse_time * 1000))
    return response.success(data)


#单个文件语音识别
@router.post("/file")
def audio_to_text(request: Request,  # 获取请求对象
                        file: Annotated[bytes, File(description="wav or mp3 audios in 16KHz")],
                        keys: Annotated[str, Form(description="name of each audio joined with comma")],
                        lang: Annotated[str, Form(description="language of audio content")] = "auto"):
    '''
    @description: 对以FORM格式传入的音频文件进行语音识别（POST方法）
    @return {respose}
    '''
    LOGGER = getLogger()
    transcribeService = TranscribeService()
    current_date = datetime.now()
    if lang == "":
        lang = "auto"
    if keys == "":
        key = [current_date.strftime("%H%M%S"), "wav"]
    else:
        key = keys.split(".")
    # 将音频保存为 wav 文件
    dir_path = os.path.join(transcribeService.conf["file_save_base_dir"], str(current_date.year), str(current_date.month).zfill(2),
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

    data = transcribeService.transcribe(audio_file_name)
    elapse_time = time.time() - start
    LOGGER.info("识别成功，用时 : %2.2f ms" % (elapse_time * 1000))
    LOGGER.debug(str(data))
    return response.success(data)


@router.websocket("/ws/realtime")
async def websocket_realtime(websocket: WebSocket):
    await websocket.accept()
    LOGGER = getLogger()
    current_date = datetime.now()
    transcribeService = TranscribeService()
    # 设置文件保存目录
    dir_path = os.path.join(transcribeService.conf["file_save_base_dir"], str(current_date.year), str(current_date.month).zfill(2),
                            str(current_date.day).zfill(2))
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # 使用一个临时文件名来保存接收到的音频流
    audio_file_name = os.path.join(dir_path, f"{current_date.strftime('%H%M%S')}.wav")
    # 处理接收到的音频数据
    audio_data = io.BytesIO()  # 临时存储音频数据
    try:
        while True:
            # 接收音频流
            data = await websocket.receive_bytes()
            audio_data.write(data)
            audio_data.seek(0)  # 回到文件开始位置
            # 使用 pydub 来处理音频数据
            audio = AudioSegment.from_file(audio_data, format="wav")
            audio.export(audio_file_name, format="wav")
            # 进行语音识别
            result = transcribeService.transcriptBytes(data)
            print(result)
            # 发送识别结果
            await websocket.send_text(f"{result}")

    except WebSocketDisconnect:
        LOGGER.info(f"WebSocket disconnected. Final audio saved as {audio_file_name}")
        # 在断开连接时保存文件
        with open(audio_file_name, 'wb') as f:
            f.write(audio_data.getvalue())
        audio_data.close()
