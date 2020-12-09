import requests
import base64
import json
import gpiozero
import time
import webbrowser

API_ENDPOINT = 'https://discord.com/api'

def print_to_channel(message):
    data = {
        "content" : message
    }
    requests.post(f'{API_ENDPOINT}/webhooks/{webhook["id"]}/{webhook["token"]}', headers=headers, data=data)

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
            print_to_channel("lighting LED")
            led.on()
        if "spibot: turn off LED" in content:
            print_to_channel("de-activating LED")
            led.off()
        if "spibot: youtube" in content:
            webbrowser.open("youtube.com")
        last_viewed = message['id']
        if "Q&A" in content:
            print_to_channel("How old are you?")
        if "hello bot,hello world" in content:
            print_to_channel("hi r u doing well today?")
        if "i am doing well thank you" in content:
            print_to_channel("I hope you have a good rest of the day and keep it up.you can do it! :D")
        if "im felling down" in content:
            print_to_channel("i hope u feel better soon!")
        if "test" in content:
            print_to_channel("I am working i hope you see this or i may not be working")
        if "hello world" in content:
            print_to_channel("hello!")
        if "how many digits of pi do you know?" in content:
            print_to_channel("I was made using rasberry pi, so as far as i know, 10!")
        if "hi spibot" in content:
            print_to_channel("hi")
        if "what is the longest river?" in content:
            print_to_channel("the nile river is the longest river in the world,at around 4,130 miles long!")
        if "how tall is the tallest building?" in content:
            print_to_channel("the burj khalifa is the tallest building in the world, at a looming 2,717 feeet!")
        if "how many spaceships have made it to mars?" in content:
            print_to_channel("63 missins have flown by/landed and explored some where unsucsesfull")
        if "what day is it" in content:
            import datetime
            x = datetime.datetime.now()
            x.replace(tzinfo=datetime.timezone.utc)
            print_to_channel(x)
        if "what is the best animal?" in content:
            print_to_channel("birds obviestly this is a easter egg and was made possible by sethi boi")