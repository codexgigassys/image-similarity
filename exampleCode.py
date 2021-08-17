import requests
import json


filesDictionary = {
    '01.jpeg': open('images/01.jpeg', 'rb'),
    '02.jpeg': open('images/02.jpeg', 'rb'),
    '05.jpeg': open('images/05.jpeg', 'rb'),
}

response = requests.post("http://localhost:9082/api/imageSimilarityByHash", files=filesDictionary, params={'similarity_grade': 0.75})

hashes = json.loads(response.text)['lists']
print(hashes)
