import json
import os
from fastapi.testclient import TestClient 
from tests.utils.routes import denoise_and_save


def test_denoise(client: TestClient):
    payload = {}
    payload['path'] = os.path.join(os.getcwd(), "examples/noisy.wav")
    response = client.post(denoise_and_save, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == '0'
    assert response.json()['msg'] == 'success'
    assert 'path' in response.json()['data']
    
def test_denoise_file_not_exists(client: TestClient):
    payload = {}
    payload['path'] = os.path.join(os.getcwd(), "examples/not_exist_file.wav")
    response = client.post(denoise_and_save, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == '-404'
    assert response.json()['msg'] == '文件不存在'
    assert response.json()['data'] is None