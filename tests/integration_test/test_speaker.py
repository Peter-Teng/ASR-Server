import json
import os
from fastapi.testclient import TestClient 
from utils.constants import *
from tests.utils.routes import register_speaker, delete_speaker, list_speakers


def test_register_speaker(client: TestClient):
    payload = {}
    payload['audioPath'] = os.path.join(os.getcwd(), "examples/staff.wav")
    payload['name'] = "staff_test"
    response = client.post(register_speaker, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == SUCCESS_CODE
    assert response.json()['msg'] == SUCCESS_MSG
    assert response.json()['data'] == SUCCESS_DATA
    
    
def test_register_speaker_exists(client: TestClient):
    payload = {}
    payload['audioPath'] = os.path.join(os.getcwd(), "examples/staff.wav")
    payload['name'] = "staff_test"
    response = client.post(register_speaker, data=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['code'] == SPEAKER_ALREADY_EXISTS.code
    assert response.json()['msg'] == SPEAKER_ALREADY_EXISTS.msg
    assert response.json()['data'] is None
    
    
def test_register_speaker_file_not_exists(client: TestClient):
    payload = {}
    payload['audioPath'] = os.path.join(os.getcwd(), "examples/not_exist_file.wav")
    payload['name'] = "staff_test"
    response = client.post(register_speaker, data=json.dumps(payload))
    assert response.status_code == 200  
    assert response.json()['code'] == FILE_NOT_FOUND.code
    assert response.json()['msg'] == FILE_NOT_FOUND.msg
    assert response.json()['data'] is None


def test_delete_speaker(client: TestClient):
    response = client.delete(delete_speaker("staff_test"))
    assert response.status_code == 200
    assert response.json()['code'] == SUCCESS_CODE
    assert response.json()['msg'] == SUCCESS_MSG
    assert response.json()['data'] == SUCCESS_DATA


def test_delete_speaker_not_exists(client: TestClient):
    response = client.delete(delete_speaker("staff_test_not_exists"))
    assert response.status_code == 200
    assert response.json()['code'] == SPEAKER_NOT_FOUND.code
    assert response.json()['msg'] == SPEAKER_NOT_FOUND.msg
    assert response.json()['data'] is None


def test_speaker_list(client: TestClient):
    response = client.get(list_speakers)
    assert response.status_code == 200
    assert response.json()['code'] == SUCCESS_CODE
    assert response.json()['msg'] == SUCCESS_MSG
    assert response.json()['data'] is not None