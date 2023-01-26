import json
import requests

# defines the URL and API token for a Hugging Face API for an "emotion-english-distilroberta-base" model,
# and sets the authorization header for the API call using the token.
API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# This code makes a POST request to the API_URL
# the request then converts the response into json and returns it.
def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

#create 2 lists
high_score0 = []
high_score1 = []

# assign first 2 dictionaries in the list to variables dict0 and dict1
def sorting(data):
    sentiment = data[0]
    dict0 = sentiment[0]
    dict1 = sentiment[1]

#clear the lists so that when the request is sent again, the list would not hold the old information
    high_score0.clear()
    high_score1.clear()

    for x in dict0.values():
        high_score0.append(x)
    for x in dict1.values():
        if dict1['score'] >= 0.01:
            high_score1.append(x)

#  opens a file "Bot.json" in read mode and loads its contents into a variable "file" using the json module
    with open("Bot.json", "r") as f:
        file = json.load(f)

# looks for the corresponding "sentiment" ion the file and returns a URL if found
    if file[0]["sentiment"] == high_score0[0] or file[0]["sentiment"] == high_score1[0]:
        return "I understand you are feeling "+ file[0]["feeling"]+". Please check out this meditation video "+ file[0]["URL"]
    elif user_input in file[1]["user_input"]:
        return file[1]["response"]
    elif file[2]["sentiment"] == high_score0[0] or file[2]["sentiment"] == high_score1[0]:
        return "I understand you are feeling "+ file[2]["feeling"]+". Please check out this meditation video "+ file[2]["URL"]
    else:
        return "Sorry, I don't understand this yet"

while True:
    user_input = input("You: ")
    list = query(user_input)
    #print("Bot:", list)
    print("Bot:",sorting(list))
