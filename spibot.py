import requests
import base64
import json
import gpiozero
import time
import webbrowser

API_ENDPOINT = 'https://discord.com/api'

def askquestion():
    data = {
        "content" : "How old are you?"
    }
    r = requests.post(f'{API_ENDPOINT}/webhooks/{webhook["id"]}/{webhook["token"]}', headers=headers, data=data)

with open(".tokens") as f:
    j = json.load(f)
    bot = j["discord-spibot"]
    snowflakes = j["discord-snowflakes"]
    webhook = j["discord-webhook"]

headers = { 'Authorization': f'Bot {bot["token"]}' }

channel = snowflakes['family-general']
params = "?limit=1"
r = requests.get(f'{API_ENDPOINT}/channels/{channel}/messages{params}', headers=headers)
j = json.loads(r.content)
last_viewed = j[0]['id']
led = gpiozero.LED(17)
while True:
    time.sleep(1)
    params = f"?after={last_viewed}"
    r = requests.get(f'{API_ENDPOINT}/channels/{channel}/messages{params}', headers=headers)
    j = json.loads(r.content)
    for message in j:
        content = message['content']
        if "spibot: light LED" in content:
            print("lighting LED")
            led.on()
        if "spibot: turn off LED" in content:
            print("lighting LED")
            led.off()
        if "spibot: youtube" in content:
            webbrowser.open("youtube.com")
        last_viewed = message['id']
        if "Q&A" in content:
            askquestion()
