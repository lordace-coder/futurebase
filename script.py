import requests


# add new item
e = requests.delete(
    "http://127.0.0.1:8000/api/collection-actions/ace/lordace12/2",
    data={"filter": "all"},
)
print(e.status_code)
r = requests.get("http://127.0.0.1:8000/api/collection-data/ace/lordace12/2")
print(r.json())
