import json
import requests

API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

high_score0 = []
high_score1 = []
high_score2 = []

def sorting(data):
    sentiment = data[0]
    dict0 = sentiment[0]
    dict1 = sentiment[1]
    dict2 = sentiment[2]

    for x in dict0.values():
        high_score0.append(x)
    for x in dict1.values():
        if dict1['score'] >= 0.01:
            high_score1.append(x)
    for x in dict2.values():
        if dict2['score'] >= 0.01:
            high_score2.append(x)
    return high_score0

while True:
    user_input = input("You: ")
    list = query(user_input)
    print("Bot: ",sorting(list))
