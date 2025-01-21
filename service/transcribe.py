import io
import soundfile
import torch
from models.Speaker.speakerlab.bin.infer_diarization import Diarization3Dspeaker
from utils.logger import getLogger
from utils.singleton import singleton
from models.embeddingExtractor import getExtractor
from utils.speakers import getSpeakers
from utils.audioUtils import load_wav_from_path_sf
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess

@singleton
class TranscribeService:
    def __init__(self, conf) -> None:
        self.LOGGER = getLogger()
        self.speakers = getSpeakers()
        self.conf = conf
        self.transcribe_model_id = self.conf["transcribe_model"]
        self.vad_model_id = self.conf["vad_model"]
        self.transcribe_model = AutoModel(
            model=self.transcribe_model_id,
            trust_remote_code=False,
            disable_update=True,
            device=conf["device"],
        )     
        self.vad_model = AutoModel(model=self.vad_model_id, trust_remote_code=False, disable_update=True, device=conf["device"])
        self.diarization_model = Diarization3Dspeaker(device=conf["device"], model_cache_dir=conf["modelscope_cache"])
        self.LOGGER.info(f'[INFO]: The diarization model is using {conf["device"]}.')
        self.LOGGER.info(f'[INFO]: The transcribe model is using {conf["device"]}.')
        self.LOGGER.info(f'[INFO]: The vad model is using {conf["device"]}.')
        self.extractor = getExtractor()

    
    def transcribe(self, path, speech=None):
        '''
        @description: 语音识别转录
        @return {*}
        @param {*} self
        @param {str} path 语音文件路径
        @param {np.ndarray} data 若为None，则从path读取；若有数据，则直接使用
        '''
        if speech is None:
            speech = load_wav_from_path_sf(path)
        chuncksInfo = self.vad_model.generate(input=speech, chunk_size=speech.shape[0])
        results = []
        i = 0
        for chunk in chuncksInfo[0]['value']:
            # 计算音频开始和结束的时间（chunk[0]是开始时间，[1]是结束的时间，单位都是毫秒，所以分割点要×16000（采样率）再÷1000）
            start = chunk[0] * 16
            end = chunk[1] * 16
            speaker = self.get_speaker(speech[start:end], self.speakers.getSpeakers())
            sentence = self.transcribe_model.generate(
                input=speech[start:end],
                cache={},
                language="auto",  # "zh", "en", "yue", "ja", "ko", "nospeech"
                use_itn=True,
                batch_size_s=60,
                chunk_size=end-start
            )
            content = rich_transcription_postprocess(sentence[0]["text"])
            results.append({"speaker": speaker, "content": content})
            i += 1 
        ret = {}
        ret["transcribe_results"] = results
        return ret
    
    
    def transcribe_with_diarization(self, path, speech=None):
        '''
        @description: 语音识别转录, 使用diarization模型
        @return {*}
        @param {*} self
        @param {str} path 语音文件路径
        @param {np.ndarray} data 若为None，则从path读取；若有数据，则直接使用
        '''
        if speech is None:
            speech = load_wav_from_path_sf(path)
        chuncksInfo = self.diarization_model(speech)
        results = []
        i = 0
        for chunk in chuncksInfo:
            # 计算音频开始和结束的时间（chunk[0]是开始时间，[1]是结束的时间，单位都是秒，所以分割点要×16000（采样率）
            start = int(chunk[0] * 16000)
            end = int(chunk[1] * 16000)
            speaker = self.get_speaker(speech[start:end], self.speakers.getSpeakers())
            sentence = self.transcribe_model.generate(
                input=speech[start:end],
                cache={},
                language="auto",  # "zh", "en", "yue", "ja", "ko", "nospeech"
                use_itn=True,
                batch_size_s=60,
                chunk_size=end-start
            )
            content = rich_transcription_postprocess(sentence[0]["text"])
            results.append({"speaker": speaker, "content": content})
            i += 1 
        ret = {}
        ret["transcribe_results"] = results
        return ret
    
    
    def get_speaker(self, speech, speakers):
        '''
        @description: 辨认该段音频是哪个人讲的话
        @return {*}
        @param {*} self
        @param {*} speech 音频数组数据
        @param {*} speakers 讲话人列表
        '''
        speaking_embedding, _ = self.extractor.compute_embedding(speech, save=False)
        max_score = 0
        speaking = "unknown"
        for speaker in speakers:
            similarity = torch.nn.CosineSimilarity(dim=-1, eps=1e-6)
            score = similarity(speaking_embedding, speaker["embedding"]).item()
            if score > max_score:
                max_score = score
                speaking = speaker["name"]
        if max_score < self.conf["simularity_threshold"]:
            return "unknown"
        return speaking


    def transcriptBytes(self, data):
        try:
            #speakers = load()
            # 使用 BytesIO 将字节数据转换为类似文件的对象
            audio_io = io.BytesIO(data)
            wav_file, sr = soundfile.read(audio_io)
            #speaker = self.get_speaker(wav_file, speakers)
            speaker = self.get_speaker(wav_file, self.speakers.getSpeakers())
            sentence = self.transcribe_model.generate(
                input=data,
                cache={},
                language="auto",  # "zh", "en", "yue", "ja", "ko", "nospeech"
                use_itn=True,
                batch_size_s=60
                )
            content = rich_transcription_postprocess(sentence[0]["text"])

        except Exception as e:
            self.LOGGER.info("Exception:[%s]" % e)
            #raise InferenceException(description="Description:[%s]" % e)
        return {"speaker": speaker, "content": content}