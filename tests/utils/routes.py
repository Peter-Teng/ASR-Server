prefix = "/v1"

denoise_and_save = f"{prefix}/denoise/do"
register_speaker = f"{prefix}/speaker/register"
list_speakers = f"{prefix}/speaker/list"
transcribe_audio = f"{prefix}/transcribe/do"
denoise_and_transcribe_audio = f"{prefix}/transcribe/denoised"
diarize_and_transcribe_audio = f"{prefix}/transcribe/diarized"

def delete_speaker(name):
    return f"{prefix}/speaker/{name}"