from fastapi.testclient import TestClient
from service.main import app

client = TestClient(app)

def test_get_all_blogs():
    response = client.get("/blog/all",  params={"id": 10})
    assert response.status_code == 200

def test_auth_error():
    response = client.post(
        url= "/token",
        data= {
            "username": "",
            "password": ""
        }
    )
    access_token = response.json().get("access_token")
    assert access_token == None
    message = response.json().get("detail")[0].get("msg")
    assert message == "Field required"

def test_auth_success():
    response = client.post(
        url= "/token",
        data= {
            "username": "linh",
            "password": "123456789"
        }
    )
    access_token = response.json().get("access_token")
    assert access_token 

def test_post_article():
    auth = client.post(
        url= "/token",
        data= {
            "username": "linh",
            "password": "123456789"
        }
    )
    access_token = auth.json().get("access_token")
    assert access_token


    """
    Dữ liệu truyền vào json (docs api để đọc)
    Request body: application/json
    """
    response = client.post(
        "article/",
        json= {
            "title": "Test_article1",
            "content": "Test Content1",
            "published": True,
            "creator_id": 4
        },
        headers= {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    assert response.status_code == 200


"""
Chạy test bằng thư viện pytest, chạy lệnh pytest service/test_main.py 
"""