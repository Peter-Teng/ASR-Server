import os
import sys
import pathlib
from typing import Tuple
import torch

from utils.audioUtils import load_wav_from_path_torch
from utils.logger import getLogger
sys.path.append('%s/../Models/Speaker'%os.path.dirname(__file__))
from models.Speaker.speakerlab.process.processor import FBank
from models.Speaker.speakerlab.utils.builder import dynamic_import


# Extractor class, only one instantialization
extractor = None

def initExtractor(conf):
    global extractor
    extractor = Extractor(conf)

def getExtractor():
    global extractor
    return extractor

class Extractor:
    def __init__(self, config) -> None:   
        '''
        @description: 初始化embedding提取器
        @param {*} self
        @param {*} config 提取器的配置文件
        @return {None}
        '''   
        self.LOGGER = getLogger()
        self.device = config["device"]
        self.ERes2Net_Large_3D_Speaker = {
        'obj': 'speakerlab.models.eres2net.ERes2Net.ERes2Net',
        'args': {
                'feat_dim': 80,
                'embedding_size': 512,
                'm_channels': 64,
            }
        }

        self.conf = {
            'revision': 'v1.0.0', 
            'model': self.ERes2Net_Large_3D_Speaker,
            'model_pt': 'eres2net_large_model.ckpt',
        }
        
        self.base_dir = config["embedding_model"]
        pathlib.Path(self.base_dir).mkdir(exist_ok=True, parents=True)

        self.embedding_dir = config["embedding_path"]
        pathlib.Path(self.embedding_dir).mkdir(exist_ok=True, parents=True)

        pretrained_model_dir = os.path.join(self.base_dir, self.conf['model_pt'])
        pretrained_state = torch.load(pretrained_model_dir, map_location='cpu')


        # load model
        self.model = self.conf['model']
        self.embedding_model = dynamic_import(self.model['obj'])(**self.model['args'])
        self.embedding_model.load_state_dict(pretrained_state)
        self.embedding_model.to(self.device)
        self.embedding_model.eval()
        self.feature_extractor = FBank(80, sample_rate=16000, mean_nor=True)
        # confirm the device
        for param in self.embedding_model.parameters():
            self.LOGGER.info(f'[INFO]: The embedding extractor is using {param.device}.')
            break

    

    
    def compute_embedding(self, wav_file, speaker="unknown", save=True) -> Tuple[torch.Tensor, str]:
        '''
        @description: 计算音频文件的embedding
        @param {*} self
        @param {str} wav_file 音频文件（路径或NumPy数组）
        @param {str} speaker 说话人名称
        @param {boolean} save 是否保存
        @return {Tuple[torch.Tensor, str]} embedding及其保存地址
        '''
        if isinstance(wav_file, str):
            # load wav
            wav = load_wav_from_path_torch(wav_file)
        else:
            wav = torch.from_numpy(wav_file).to(torch.float32)
        # compute feat
        feat = self.feature_extractor(wav).unsqueeze(0).to(self.device)
        # compute embedding
        with torch.no_grad():
            embedding = self.embedding_model(feat).detach().squeeze(0).cpu()
        savePath = None
        if save:
            savePath = os.path.join(self.embedding_dir, ('%s.pt' % (speaker)))
            torch.save(embedding, savePath)
            self.LOGGER.info(f'[INFO]: The extracted embedding from {wav_file} is saved to {savePath}.')
        
        return embedding, savePath
