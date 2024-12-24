import onnxruntime
import torch
from modelscope.models.audio.ans.zipenhancer import mag_pha_stft, mag_pha_istft


class zipEnhancerModel:
    '''
    @description: ZipEnhancer音频去噪模型（试用模型）
    '''
    def __init__(self, conf, providers=None):
        self.conf = conf
        self.onnx_model = onnxruntime.InferenceSession(conf["denoise_model"], providers=providers)

    def to_numpy(self, tensor):
        return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

    def __call__(self, noisy_wav):
        n_fft = 400
        hop_size = 100
        win_size = 400

        norm_factor = torch.sqrt(noisy_wav.shape[1] / torch.sum(noisy_wav ** 2.0))
        
        noisy_audio = (noisy_wav * norm_factor)

        noisy_amp, noisy_pha, _ = mag_pha_stft(
            noisy_audio,
            n_fft,
            hop_size,
            win_size,
            compress_factor=0.3,
            center=True)

        ort_inputs = {
            self.onnx_model.get_inputs()[0].name: self.to_numpy(noisy_amp),
            self.onnx_model.get_inputs()[1].name: self.to_numpy(noisy_pha),
        }
        ort_outs = self.onnx_model.run(None, ort_inputs)

        amp_g = torch.from_numpy(ort_outs[0])
        pha_g = torch.from_numpy(ort_outs[1])
        
        wav = mag_pha_istft(amp_g, pha_g, n_fft, hop_size, win_size, compress_factor=0.3, center=True)
        wav = wav / norm_factor
        wav = self.to_numpy(wav)

        return wav