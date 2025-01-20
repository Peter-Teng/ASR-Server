import copy
from exceptions.application import ApiException
from models.embeddingExtractor import getExtractor
from utils.constants import SPEAKER_ALREADY_EXISTS, SUCCESS, SPEAKER_NOT_FOUND
from utils.logger import getLogger
from utils.speakers import getSpeakers
from utils.singleton import singleton


@singleton
class SpeakerService:
    def __init__(self, conf) -> None:
        '''
        @description: 初始化讲话人服务对象
        @return {None}
        @param {*} self
        @param {*} conf 系统配置文件
        '''
        self.LOGGER = getLogger()
        self.speakers = getSpeakers()
        self.conf = conf
        self.extractor = getExtractor()


    def register(self, path, speaker):
        '''
        @description: 注册讲话人
        @return {str} 是否成功
        @param {*} self
        @param {*} path 音频路径
        @param {*} speaker 讲话人名字
        '''
        if self.speakers.consists(speaker):
            raise ApiException(SPEAKER_ALREADY_EXISTS)
        embedding, savePath = self.extractor.compute_embedding(wav_file=path, speaker=speaker)
        self.speakers.addSpeaker(speaker, embedding, savePath)
        return SUCCESS
    
    
    def delete(self, speaker):
        '''
        @description: 删除讲话人
        @return {str} 是否成功
        @param {*} self
        @param {*} speaker 删除的讲话人名字
        '''
        if not self.speakers.consists(speaker):
            raise ApiException(SPEAKER_NOT_FOUND)
        self.speakers.deleteSpeaker(speaker)
        return SUCCESS

    
    def list(self):
        '''
        @description: 获取讲话人列表
        @return {List} 讲话人列表数据
        @param {*} self
        '''
        # 深拷贝一份数据再进行处理
        data = copy.deepcopy(self.speakers.getSpeakers())
        for speaker in data:
            speaker.pop("embedding")
        return data
