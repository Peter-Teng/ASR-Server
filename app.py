from fastapi import FastAPI
from contextlib import asynccontextmanager
import argparse
import uvicorn
import yaml
from service.transcribe import TranscribeService
from service.speaker import SpeakerService
from service.denoise import DenoiseService
from utils.speakers import initSpeakers
from utils.logger import *
from models.embeddingExtractor import *
from utils.modelsUtils import *
from apis.v1 import router
from exceptions import registerExceptionHandler

# 读取命令行参数
parser = argparse.ArgumentParser()
# 基础参数
parser.add_argument('--host', type=str, help='The IP address of server', default="localhost")
parser.add_argument('--port', type=int, help='The port of the service', default=8000)
parser.add_argument('--download', help='To download the reqired models', action='store_true', default=False)
parser.add_argument('--workers', type=int, help='The numbers of workers for the application', default=1)

args = parser.parse_args()


# 初始化应用   
@asynccontextmanager
async def init(app: FastAPI):
    # 加载配置文件
    with open('config.yaml', 'r', encoding='utf-8') as file:
        conf = yaml.load(file, Loader=yaml.FullLoader)
    os.environ["MODELSCOPE_CACHE"] = conf["modelscope_cache"]
    
    # 初始化路由
    app.include_router(router=router)

    # 初始化单例类（Logger等）
    initLogger()
    if args.download:
        downloadModels(conf)
    initExtractor(conf)
    initSpeakers()
    LOGGER = getLogger()
    LOGGER.info("------------正在初始化------------")

    
    # 初始化服务类
    LOGGER.info("------------NOW Initializing Model------------")
    TranscribeService(conf)
    SpeakerService(conf)
    DenoiseService(conf)
    LOGGER.info("------------Model Initialized------------")
    
    LOGGER.info("------------服务初始化成功------------")
    
    yield
    
    # 清理系统资源
    LOGGER.info("------------资源清理开始------------")
    clearModels(conf)
    LOGGER.info("------------资源清理完毕------------")


app = FastAPI(lifespan=init)
registerExceptionHandler(app)


# 应用入口
if __name__ == '__main__':
    print("------------正在开始------------")
    uvicorn.run(app="app:app", host=args.host, port=args.port, workers=args.workers)