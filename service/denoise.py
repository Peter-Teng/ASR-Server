import math
import numpy as np
from utils.logger import getLogger
from utils.audioUtils import load_wav_from_path_sf, save_wav
from utils.singleton import singleton
from models.embeddingExtractor import *
from models.zipEnhancer import zipEnhancerModel
from modelscope.utils.audio.audio_utils import audio_norm

@singleton
class DenoiseService:
    def __init__(self, conf) -> None:
        '''
        @description: 初始化音频去噪服务对象
        @param {DenoiseService} self
        @param {*} conf 系统配置
        @return {None}
        '''
        self.LOGGER = getLogger()
        self.conf = conf
        self.sampleRate = 16000
        self.fragmentLength = conf["fragment_length"]
        self.denoised_path = conf["denoised_path"]
        pathlib.Path(self.denoised_path).mkdir(exist_ok=True, parents=True)
        
        self.denoiser = zipEnhancerModel(self.conf)
        
        
    def denoiseFile(self, path, save=False) -> Tuple[np.ndarray, str]:
        '''
        @description: 
        @param {DenoiseService} self
        @param {str} path 去噪音频路径
        @param {boolean} save 是否保存去噪音频
        @return {Tuple[np.ndarray, str]} 去噪numpy对象及保存地址
        '''
        speech = load_wav_from_path_sf(path)
        # 将音频分段处理
        speechLength = speech.shape[0]
        # fragmentSamples-每个片段含有的样本数
        fragmentSamples = math.ceil(self.sampleRate / 1000 * self.fragmentLength)
        fragmentsCount = math.ceil(speechLength / fragmentSamples)
        enhancedSpeech = None
        # 分段增强音频
        for i in range(fragmentsCount):
            fragment = audio_norm(speech[i*fragmentSamples : (i+1)*fragmentSamples]).astype(np.float32)
            noisyFragment = torch.from_numpy(np.reshape(fragment, [1, fragment.shape[0]]))
            enhancedFragment = self.denoiser(noisyFragment)
            enhancedFragment = (enhancedFragment[0]).astype(np.float64)
            enhancedSpeech = enhancedFragment if enhancedSpeech is None else np.concatenate((enhancedSpeech, enhancedFragment))
        savePath = None
        # 保存增强音频
        if save:
            savePath = os.path.join(self.denoised_path, ('%s_enhanced.wav' % (path.split("/")[-1].split(".")[0])))
            save_wav(enhancedSpeech, savePath)
            self.LOGGER.info(f'[INFO]: The denoised speech is saved to {savePath}.')
        
        return enhancedSpeech, savePath
            