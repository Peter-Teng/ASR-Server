import pyaudio
import wave
import asyncio
import aiohttp
import base64
import json

# wav configuration
TEMP_WAV_FILE = "./outputs/temp.wav"
ELAPSE_TIME = 5
CHANNELS = 1
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_RATE = 16000
FRAMES_PER_BUFFER = 1024
# network configuration
URL = 'http://localhost:8000/v1/transcribe/diarize'
HEADERS = {'Content-Type': 'application/json'}

# 定义一个异步函数用于从麦克风录制音频并保存到文件
async def record_audio():
    # 创建 PyAudio 对象
    p = pyaudio.PyAudio()
    # 打开音频流，设置格式、声道数、采样率等参数
    stream = p.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, input=True, frames_per_buffer=FRAMES_PER_BUFFER)
    # 创建一个空列表用于存储录制的音频数据
    frames = []
    # 打印提示信息，表示开始录制
    print("Recording...")
    # 记录开始时间
    start_time = asyncio.get_event_loop().time()
    # 尝试录制音频，直到用户按下 Ctrl+C 键中断
    try:
        while True:
            # 从音频流中读取数据样本
            data = stream.read(FRAMES_PER_BUFFER)
            # 将数据添加到 frames 列表中
            frames.append(data)
            if asyncio.get_event_loop().time() - start_time >= ELAPSE_TIME:
                # 重置开始时间
                start_time = asyncio.get_event_loop().time()
                # 异步发送POST请求
                await send_audio(frames)
                # 清空 frames 列表
                frames = []
    # 如果用户按下 Ctrl+C 键，则跳过异常处理块
    except KeyboardInterrupt:
        pass
    # 打印提示信息，表示录制已停止
    print("Recording stopped.")
    # 停止音频流
    stream.stop_stream()
    # 关闭音频流
    stream.close()
    # 终止 PyAudio 对象
    p.terminate()
    # 如果 frames 列表不为空，则发送剩余的音频数据
    if frames:
        await send_audio(frames)
    # 打印提示信息，表示录制已完成
    print("Done")

# 定义一个异步函数用于发送音频数据到服务器
async def send_audio(frames):
    # 将 frames 列表中的所有数据连接成一个字节串
    audio_data = b''.join(frames)
    # 将音频数据保存为WAV文件
    with wave.open(TEMP_WAV_FILE, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(audio_data)
    # 读取WAV文件并转换为Base64编码
    with open(TEMP_WAV_FILE, 'rb') as f:
        audio_base64 = base64.b64encode(f.read()).decode('utf-8')
    # 创建 JSON 数据
    json_data = json.dumps({'base64Str': audio_base64})
    # 创建一个 aiohttp 客户端会话
    async with aiohttp.ClientSession() as session:
        # 发送POST请求到服务器
        async with session.post(URL, data=json_data, headers=HEADERS) as resp:
            # 打印服务器的响应
            print(await resp.text())


if __name__ == "__main__":
    # 获取事件循环
    loop = asyncio.get_event_loop()
    # 运行异步函数
    loop.run_until_complete(record_audio())