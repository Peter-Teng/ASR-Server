import onnxruntime
import numpy as np
from utils.logger import getLogger

class DenoiseModel:
    '''
    @description: 音频去噪模型（试用模型）
    '''
    def __init__(self, conf):
        self.conf = conf
        self.LOGGER = getLogger()
        self.onnx_model = onnxruntime.InferenceSession(conf["denoise_model"])
        if self.conf["device"].startswith("cuda"):
            gpu_id = self.conf["device"].split(":")[-1]
            self.onnx_model.set_providers(['CUDAExecutionProvider'], provider_options=[{'device_id': int(gpu_id)}])
        if 'CUDAExecutionProvider' in self.onnx_model.get_providers():
            self.LOGGER.info(f'[INFO]: The Denoiser is using GPU.')
        else:
            self.LOGGER.info(f'[INFO]: The Denoiser is using cpu.')

    def __call__(self, speech):
        '''
        @description: 模型推理
        @param {*} speech: 输入噪声音频
        @return {*} enhancedSpeech: 输出去噪音频
        '''
        speech = np.expand_dims(speech, axis=0).astype(np.float32)
        input_name = self.onnx_model.get_inputs()[0].name
        outputs = self.onnx_model.run(None, {input_name: speech})
        output_data = outputs[0]
        enhancedSpeech = output_data[0, :, 0]
        enhancedSpeech = enhancedSpeech / np.abs(enhancedSpeech).max() * 0.5
        enhancedSpeech = enhancedSpeech[np.newaxis, :]
        enhancedSpeech = (enhancedSpeech).astype(np.float32).tobytes()
        return np.frombuffer(enhancedSpeech, dtype=np.float32)