import json
import os
from fastapi.testclient import TestClient
from tests.utils.routes import transcribe_audio, denoise_and_transcribe_audio, diarize_and_transcribe_audio


def test_transcribe(client: TestClient):
    payload = {}
    payload['path'] = os.path.join(os.getcwd(), "examples/customer.wav")
    response = client.post(transcribe_audio, data=json.dumps(payload))
    expected = json.loads(open(os.path.join(os.getcwd(), "tests/json/transcribe.json"), "r", encoding="utf-8").read())
    assert response.status_code == 200
    assert response.json() == expected
    
def test_transcribe_file_not_exists(client: TestClient):
    payload = {}
    payload['path'] = os.path.join(os.getcwd(), "examples/not_exist_file.wav")
    response = client.post(transcribe_audio, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == '-404'
    assert response.json()['msg'] == '文件不存在'
    assert response.json()['data'] is None
    
def test_denoise_and_transcribe(client: TestClient):
    payload = {}
    payload['path'] = os.path.join(os.getcwd(), "examples/noisy.wav")
    response = client.post(denoise_and_transcribe_audio, data=json.dumps(payload))
    expected = json.loads(open(os.path.join(os.getcwd(), "tests/json/denoised.json"), "r", encoding="utf-8").read())
    assert response.status_code == 200
    assert response.json() == expected

def test_denoise_and_transcribe_file_not_exists(client: TestClient):
    payload = {}
    payload['path'] = os.path.join(os.getcwd(), "examples/not_exist_file.wav")
    response = client.post(denoise_and_transcribe_audio, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == '-404'
    assert response.json()['msg'] == '文件不存在'
    assert response.json()['data'] is None
    
def test_diarize_and_transcribe(client: TestClient):
    payload = {}
    payload['path'] = os.path.join(os.getcwd(), "examples/customer.wav")
    response = client.post(diarize_and_transcribe_audio, data=json.dumps(payload))
    expected = json.loads(open(os.path.join(os.getcwd(), "tests/json/transcribe.json"), "r", encoding="utf-8").read())
    assert response.status_code == 200
    assert response.json() == expected
    
def test_diarize_and_transcribe_file_not_exists(client: TestClient):
    payload = {}
    payload['path'] = os.path.join(os.getcwd(), "examples/not_exist_file.wav")
    response = client.post(diarize_and_transcribe_audio, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == '-404'
    assert response.json()['msg'] == '文件不存在'
    assert response.json()['data'] is None