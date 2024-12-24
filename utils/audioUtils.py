import soundfile
import librosa
import torch
import torchaudio
import numpy as np



def load_wav_from_path_sf(path, target_sample_rate=16000):
    '''
    @description: 使用soundfile库读取wav文件
    @param {*} path wav文件路径
    @param {*} target_sample_rate 目标采样率
    @return {np.ndarray} 返回的wav文件数组
    '''
    speech, sample_rate = soundfile.read(path)
    # 对双声道的音频不支持，降为单声道
    if speech.ndim == 2 and speech.shape[1] == 2:
        speech = np.mean(speech, axis=1)
    # resample audio to 16kHz(模型仅支持16KHz的音频的分割)
    if sample_rate != 16000:
        speech = librosa.resample(speech, orig_sr = sample_rate, target_sr = target_sample_rate)
    return speech


def load_wav_from_path_torch(path, target_sample_rate=16000):
    '''
    @description: 使用torchaudio库读取wav文件
    @param {*} path wav文件路径
    @param {*} target_sample_rate 目标采样率
    @return {np.ndarray} 返回的wav文件数组
    '''
    speech, sample_rate = torchaudio.load(path)
    # 对双声道的音频不支持，降为单声道
    if speech.ndim == 2 and speech.shape[0] == 2:
        speech = torch.mean(speech, dim=0).unsqueeze(0)
    # resample audio to 16kHz
    if sample_rate != target_sample_rate:
        resampler = torchaudio.transforms.Resample(sample_rate, target_sample_rate, dtype=speech.dtype)
        speech = resampler(speech)
    return speech


def save_wav(data, path, sample_rate=16000):
    soundfile.write(path, data, sample_rate)
    

def create_wav_header(dataflow, sample_rate=16000, num_channels=1, bits_per_sample=16):
    """
    @description 创建WAV文件头的字节串。
    @param dataflow: 音频bytes数据（以字节为单位）。
    @param sample_rate: 采样率，默认16000。
    @param num_channels: 声道数，默认1（单声道）。
    @param bits_per_sample: 每个样本的位数，默认16。
    @return: WAV文件头的字节串和音频bytes数据。
    """
    total_data_len = len(dataflow)
    byte_rate = sample_rate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8
    data_chunk_size = total_data_len
    fmt_chunk_size = 16
    riff_chunk_size = 4 + (8 + fmt_chunk_size) + (8 + data_chunk_size)

    # 使用 bytearray 构建字节串
    header = bytearray()

    # RIFF/WAVE header
    header.extend(b'RIFF')
    header.extend(riff_chunk_size.to_bytes(4, byteorder='little'))
    header.extend(b'WAVE')

    # fmt subchunk
    header.extend(b'fmt ')
    header.extend(fmt_chunk_size.to_bytes(4, byteorder='little'))
    header.extend((1).to_bytes(2, byteorder='little'))  # Audio format (1 is PCM)
    header.extend(num_channels.to_bytes(2, byteorder='little'))
    header.extend(sample_rate.to_bytes(4, byteorder='little'))
    header.extend(byte_rate.to_bytes(4, byteorder='little'))
    header.extend(block_align.to_bytes(2, byteorder='little'))
    header.extend(bits_per_sample.to_bytes(2, byteorder='little'))

    # data subchunk
    header.extend(b'data')
    header.extend(data_chunk_size.to_bytes(4, byteorder='little'))

    return bytes(header) + dataflow