import numpy as np
from utils.logger import getLogger
from utils.audioUtils import load_wav_from_path_sf, save_wav
from utils.singleton import singleton
from models.embeddingExtractor import *
from models.zipEnhancer import zipEnhancerModel
from modelscope.utils.audio.audio_utils import audio_norm

@singleton
class denoiseService:
    def __init__(self, conf) -> None:
        self.LOGGER = getLogger()
        self.conf = conf
        
        self.denoised_path = conf["denoised_path"]
        pathlib.Path(self.denoised_path).mkdir(exist_ok=True, parents=True)
        
        self.denoiser = zipEnhancerModel(self.conf)
        
        
    def denoiseFile(self, path, save=False):
        speech = load_wav_from_path_sf(path)
        speech = audio_norm(speech).astype(np.float32)
        noisySpeech = torch.from_numpy(np.reshape(speech, [1, speech.shape[0]]))
        enhanceSpeech = self.denoiser(noisySpeech)
        enhanceSpeech = (enhanceSpeech[0] * 32768).astype(np.int16)
        savePath = None
        if save:
            savePath = os.path.join(self.denoised_path, ('%s_enhanced.wav' % (path.split("/")[-1].split(".")[0])))
            save_wav(enhanceSpeech, savePath)
            self.LOGGER.info(f'[INFO]: The denoised speech is saved to {savePath}.')
        
        return enhanceSpeech, savePath
            