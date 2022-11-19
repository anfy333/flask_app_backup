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

    high_score0.clear()
    high_score1.clear()
    high_score2.clear()

    for x in dict0.values():
        high_score0.append(x)
    for x in dict1.values():
        if dict1['score'] >= 0.01:
            high_score1.append(x)
    for x in dict2.values():
        if dict2['score'] >= 0.01:
            high_score2.append(x)

    with open("Bot.json", "r") as f:
        file = json.load(f)
        
   if file[0]["sentiment"] == high_score0[0] or file[0]["sentiment"] == high_score1[0]:
        return "I understand you are feeling "+ file[0]["feeling"]+". Please check out this video "+ file[0]["URL"]
    elif user_input in file[1]["user_input"]:
        return file[1]["response"]
    else:
        return "Sorry, I don't understand this yet"
        
while True:
    user_input = input("You: ")
    list = query(user_input)
    print("Bot:",sorting(list))
