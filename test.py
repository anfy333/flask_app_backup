import json
with open("Bot.json", "r") as f:
        file = json.load(f)
for i in file["user_input"]:
    print(i)
