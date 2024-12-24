import os
import torch
from utils.logger import getLogger
from utils.singleton import singleton
from models.embeddingExtractor import getExtractor

SPEAKERS = None

def initSpeakers():
    global SPEAKERS
    SPEAKERS = Speakers()

def getSpeakers():
    global SPEAKERS
    return SPEAKERS


@singleton
class Speakers:
    def __init__(self):
        '''
        @description: 初始化Speakers工具
        @return {None}
        '''
        self.data = []
        self.map = {}
        self.logger = getLogger()
        self.embeddings_dir = getExtractor().embedding_dir
        if os.path.exists(self.embeddings_dir):
            for embedding in os.listdir(self.embeddings_dir):
                speaker = {}
                speaker["name"] = embedding.split(".")[0]
                speaker["file"] = os.path.join(self.embeddings_dir, embedding)
                speaker["embedding"] = torch.load(speaker["file"])
                self.data.append(speaker)
                self.map[speaker["name"]] = speaker

                
    def getSpeakers(self):
        '''
        @description: 获取讲话人数据
        @param {self}
        @return {List} 讲话人的所有数据
        '''
        return self.data

    
    def addSpeaker(self, name, embedding, savePath):
        '''
        @description: 添加讲话人
        @return {None}
        @param {*} self
        @param {str} name 讲话人名字
        @param {torch.Tensor} embedding 讲话人的embedding
        @param {str} savePath 保存路径
        '''
        if name in self.map:
            self.logger.warning(f"Speaker {name} already exists.")
            return
        speaker = {}
        speaker["name"] = name
        speaker["embedding"] = embedding
        speaker["file"] = savePath
        self.data.append(speaker)
        self.map[name] = speaker
        
     
    def deleteSpeaker(self, name):
        '''
        @description: 删除讲话人
        @return {dist} 被删除的讲话人dist
        @param {*} self
        @param {str} name 拟删除的讲话人姓名
        '''
        if name not in self.map:
            return None
        deleted = self.map[name]
        self.data.remove(deleted)
        self.map.pop(name)
        os.remove(deleted["file"])
        return deleted