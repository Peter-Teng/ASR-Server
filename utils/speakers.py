import os
import torch
from utils.logger import getLogger
from utils.singleton import singleton
from utils.embeddingExtractor import getExtractor

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
        return self.data

    
    def addSpeaker(self, name, embedding, savePath):
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
        if name not in self.map:
            return None
        deleted = self.map[name]
        self.data.remove(deleted)
        self.map.pop(name)
        os.remove(deleted["file"])
        return deleted