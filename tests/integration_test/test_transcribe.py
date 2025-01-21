import json
import os
from fastapi.testclient import TestClient
from utils.constants import *
from tests.utils.routes import transcribe_audio, denoise_and_transcribe_audio, diarize_and_transcribe_audio

def test_transcribe(client: TestClient):
    payload = {}
    payload['path'] = os.path.join(os.getcwd(), "examples/customer.wav")
    response = client.post(transcribe_audio, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == SUCCESS_CODE
    assert response.json()['msg'] == SUCCESS_MSG
    
def test_transcribe_file_not_exists(client: TestClient):
    payload = {}
    payload['path'] = os.path.join(os.getcwd(), "examples/not_exist_file.wav")
    response = client.post(transcribe_audio, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == FILE_NOT_FOUND.code
    assert response.json()['msg'] == FILE_NOT_FOUND.msg
    assert response.json()['data'] is None
    
def test_denoise_and_transcribe(client: TestClient):
    payload = {}
    payload['path'] = os.path.join(os.getcwd(), "examples/noisy.wav")
    response = client.post(denoise_and_transcribe_audio, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == SUCCESS_CODE
    assert response.json()['msg'] == SUCCESS_MSG

def test_denoise_and_transcribe_file_not_exists(client: TestClient):
    payload = {}
    payload['path'] = os.path.join(os.getcwd(), "examples/not_exist_file.wav")
    response = client.post(denoise_and_transcribe_audio, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == FILE_NOT_FOUND.code
    assert response.json()['msg'] == FILE_NOT_FOUND.msg
    assert response.json()['data'] is None
    
def test_diarize_and_transcribe(client: TestClient):
    payload = {}
    payload['path'] = os.path.join(os.getcwd(), "examples/customer.wav")
    response = client.post(diarize_and_transcribe_audio, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == SUCCESS_CODE
    assert response.json()['msg'] == SUCCESS_MSG
    
def test_diarize_and_transcribe_with_speaker_num(client: TestClient):
    payload = {}
    payload['path'] = os.path.join(os.getcwd(), "examples/customer.wav")
    payload['speaker_num'] = 2
    response = client.post(diarize_and_transcribe_audio, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == SUCCESS_CODE
    assert response.json()['msg'] == SUCCESS_MSG
    
def test_diarize_and_transcribe_file_not_exists(client: TestClient):
    payload = {}
    payload['path'] = os.path.join(os.getcwd(), "examples/not_exist_file.wav")
    response = client.post(diarize_and_transcribe_audio, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == FILE_NOT_FOUND.code
    assert response.json()['msg'] == FILE_NOT_FOUND.msg
    assert response.json()['data'] is None