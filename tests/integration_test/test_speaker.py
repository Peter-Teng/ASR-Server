import json
import os
from fastapi.testclient import TestClient 
from tests.utils.routes import register_speaker, delete_speaker, list_speakers


def test_register_speaker(client: TestClient):
    payload = {}
    payload['audioPath'] = os.path.join(os.getcwd(), "examples/staff.wav")
    payload['name'] = "staff_test"
    response = client.post(register_speaker, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == '0'
    assert response.json()['msg'] == 'success'
    assert response.json()['data'] == "OK"
    
    
def test_register_speaker_exists(client: TestClient):
    payload = {}
    payload['audioPath'] = os.path.join(os.getcwd(), "examples/staff.wav")
    payload['name'] = "staff_test"
    response = client.post(register_speaker, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == '-200'
    assert response.json()['msg'] == '讲话人已存在'
    assert response.json()['data'] is None
    
    
def test_register_speaker_file_not_exists(client: TestClient):
    payload = {}
    payload['audioPath'] = os.path.join(os.getcwd(), "examples/not_exist_file.wav")
    payload['name'] = "staff_test"
    response = client.post(register_speaker, data=json.dumps(payload))
    assert response.status_code == 200  
    assert response.json()['code'] == '-404'
    assert response.json()['msg'] == '文件不存在'
    assert response.json()['data'] is None


def test_delete_speaker(client: TestClient):
    response = client.delete(delete_speaker("staff_test"))
    assert response.status_code == 200
    assert response.json()['code'] == '0'
    assert response.json()['msg'] == 'success'
    assert response.json()['data'] == "OK"


def test_delete_speaker_not_exists(client: TestClient):
    response = client.delete(delete_speaker("staff_test_not_exists"))
    assert response.status_code == 200
    assert response.json()['code'] == '-404'
    assert response.json()['msg'] == '讲话人不存在'
    assert response.json()['data'] is None


def test_speaker_list(client: TestClient):
    response = client.get(list_speakers)
    assert response.status_code == 200
    assert response.json()['code'] == '0'
    assert response.json()['msg'] == 'success'
    assert response.json()['data'] is not None