import requests


r = requests.get("http://127.0.0.1:8000/api/collection-data/ace/lordace12/2")
print(r.json())
