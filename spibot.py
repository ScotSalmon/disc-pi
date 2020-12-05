import requests
import base64
import json

API_ENDPOINT = 'https://discord.com/api'

with open(".tokens") as f:
    j = json.load(f)
    bot = j["discord-spibot"]
    snowflakes = j["discord-snowflakes"]

headers = { 'Authorization': f'Bot {bot["token"]}' }

channel = snowflakes['family-general']
r = requests.get(f'{API_ENDPOINT}/channels/{channel}/messages', headers=headers)
j = json.loads(r.content)
for message in j:
    if "hello" in message['content']:
        print("got it!")
