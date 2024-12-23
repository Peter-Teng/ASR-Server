import io

import torch
from utils.logger import getLogger
from utils.singleton import singleton
from models.embeddingExtractor import getExtractor
from utils.speakers import getSpeakers
from utils.audioUtils import load_wav_from_path_sf
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess

@singleton
class transcribeModel:
    def __init__(self, conf) -> None:
        self.LOGGER = getLogger()
        self.speakers = getSpeakers()
        self.LOGGER.info("------------NOW Initializing Model------------")
        self.conf = conf
        self.transcribe_model_id = self.conf["transcribe_model"]
        self.vad_model_id = self.conf["vad_model"]
        self.transcribe_model = AutoModel(
            model=self.transcribe_model_id,
            trust_remote_code=False,
            disable_update=True,
            device="cuda:0",
        )        
        self.vad_model = AutoModel(model=self.vad_model_id, trust_remote_code=False, disable_update=True, device="cuda:0",)
        self.extractor = getExtractor()
        self.LOGGER.info("------------Model Initialized------------")

    def transcribe(self, path):
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
        ret = []
        ret.append({"transcribe_results" : results})
        return ret
    
    
    def get_speaker(self, speech, speakers):
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