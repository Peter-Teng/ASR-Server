import logging
from logging.handlers import TimedRotatingFileHandler
import os
from utils.singleton import singleton


level_relations = {'DEBUG':logging.DEBUG,'INFO':logging.INFO,'WARNING':logging.WARNING,'ERROR':logging.ERROR,'CRITICAL':logging.CRITICAL}#日志级别关系映射

# Logger class, only one instantialization
LOGGER = None

def initLogger():
    global LOGGER
    LOGGER = Logger(level="INFO")

def getLogger():
    global LOGGER
    return LOGGER.logger

@singleton
class Logger():
    def __init__(self, level="INFO", when='w4', backCount=25, fmt=' [%(levelname)s][%(asctime)s] - %(message)s'):
        logPath = os.path.join(os.getcwd(), 'outputs', 'logs')
        if not os.path.exists(logPath):
            os.makedirs(logPath)
        logName = logPath + '/' + 'detector.log'
        self.logger = logging.getLogger(logName)

        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(level_relations[level])  # 设置日志级别

        th = TimedRotatingFileHandler(filename=logName, when=when, backupCount=backCount,
                                      encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一） w4
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(th)
        self.logger.info("------------Logger Initialized!------------")