from modelscope.hub.snapshot_download import snapshot_download


# 下载模型
def downloadModels(conf):
    snapshot_download(model_id='iic/speech_eres2net_large_sv_zh-cn_3dspeaker_16k', revision="v1.0.0", local_dir=conf["embedding_model"])   
    snapshot_download(model_id='iic/SenseVoiceSmall', local_dir=conf["transcribe_model"])
    snapshot_download(model_id='iic/speech_fsmn_vad_zh-cn-16k-common-pytorch', local_dir=conf["vad_model"])
    snapshot_download(model_id='iic/speech_campplus_sv_zh_en_16k-common_advanced', local_dir=conf["diarization_model"])
    

# 清理模型
def clearModels(conf):
    pass