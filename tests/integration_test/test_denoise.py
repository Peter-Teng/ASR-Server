import json
import os
from fastapi.testclient import TestClient 
from utils.constants import *
from tests.utils.routes import denoise_and_save


def test_denoise(client: TestClient):
    payload = {}
    payload['path'] = os.path.join(os.getcwd(), "examples/noisy.wav")
    response = client.post(denoise_and_save, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == SUCCESS_CODE
    assert response.json()['msg'] == SUCCESS_MSG
    assert 'path' in response.json()['data']
    
def test_denoise_file_not_exists(client: TestClient):
    payload = {}
    payload['path'] = os.path.join(os.getcwd(), "examples/not_exist_file.wav")
    response = client.post(denoise_and_save, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == FILE_NOT_FOUND.code
    assert response.json()['msg'] == FILE_NOT_FOUND.msg
    assert response.json()['data'] is None