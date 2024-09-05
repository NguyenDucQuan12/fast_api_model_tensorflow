import requests

url_get_token = "http://172.31.99.42:8000/token"
data = {
    "username": "linh",
    "password": "123456789"
}
response = requests.post(url=url_get_token, data= data)
token = response.json().get("access_token")

print(token)
id = 9
update_user_url = f"http://172.31.99.42:8000/user/{id}/update"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

newname = "linh"
new_email = "linh1@gmail.com"
new_password = "123456789"
data = {
    "username": newname,
    "email": new_email,
    "password": new_password
}

response = requests.put(url= update_user_url, json = data, headers = headers)
if response.status_code == 200:
    print(response.json())