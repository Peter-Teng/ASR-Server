from utils.logger import getLogger
from utils.speakers import getSpeakers
from utils.singleton import singleton
from models.embeddingExtractor import *

@singleton
class speakerService:
    def __init__(self, conf) -> None:
        self.LOGGER = getLogger()
        self.speakers = getSpeakers()
        self.conf = conf
        self.extractor = getExtractor()


    def register(self, path, speaker):
        embedding, savePath = self.extractor.compute_embedding(wav_file=path, speaker=speaker)
        self.speakers.addSpeaker(speaker, embedding, savePath)
        return "OK"
    
    
    def delete(self, speaker):
        delete = self.speakers.deleteSpeaker(speaker)
        if delete is None:
            return f"Speaker {speaker} does not exist!"
        return "OK" 
