import requests
import json
response_API = requests.get('http://127.0.0.1:5000/api/attractions').text
data = json.loads(response_API)
print(data)

def filterId(id):
    for d in data:
        if d["id"] != id:
            return "A"
        else:
            return "B"
print(filterId(1))
