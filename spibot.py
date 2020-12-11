import requests
import base64
import json
import gpiozero
import time
import webbrowser
import websockets
import asyncio

API_ENDPOINT = 'https://discord.com/api'

# Discord gateway handshake, see https://discord.com/developers/docs/topics/gateway
async def websocket_connect(uri):
    async with websockets.connect(uri) as websocket:
        received_json = await websocket.recv()
        hello = json.loads(received_json)
        assert(hello["op"] == 10)
        interval = hello["d"]["heartbeat_interval"]

        heartbeat = {
            "op": 1,
            "d": hello["s"]
        }
        ret = await websocket.send(json.dumps(heartbeat))

        received_json = await websocket.recv()
        heartbeat_ack = json.loads(received_json)
        assert(heartbeat_ack["op"] == 11)

        identify = {
            "op": 2,
            "d": {
                "token": bot["token"],
                "intents": 0, # I don't actually want any events, I'm just connecting
                "properties": {
                    "$os": "linux",
                    "$browser": "disc_pi",
                    "$device": "disc_pi"
                }
            }
        }
        await websocket.send(json.dumps(identify))

        received_json = await websocket.recv()
        ready = json.loads(received_json)

# we have to connect to the gateway once to send messages (unless we want to use the webhook),
# but we won't bother keeping the connection alive after the initial handshake
def discord_gateway_connect():
    response = requests.get(f'{API_ENDPOINT}/gateway/bot', headers=headers)
    gateway_endpoint = json.loads(response.content)
    websocket_url = gateway_endpoint['url']
    asyncio.get_event_loop().run_until_complete(websocket_connect(websocket_url))

# this is way simpler with the webhook, but then you need two bot-ish things instead of just one
def print_to_channel(message):
    data = {
        "content" : message
    }
    #requests.post(f'{API_ENDPOINT}/webhooks/{webhook["id"]}/{webhook["token"]}', headers=headers, data=data)
    requests.post(f'{API_ENDPOINT}/channels/{channel}/messages', headers=headers, data=data)

with open(".tokens") as f:
    tokens = json.load(f)
    bot = tokens["discord-spibot"]
    snowflakes = tokens["discord-snowflakes"]

headers = { 'Authorization': f'Bot {bot["token"]}' }

channel = snowflakes['family-general']
print_to_channel("spibot here!")

params = "?limit=1"
r = requests.get(f'{API_ENDPOINT}/channels/{channel}/messages{params}', headers=headers)
latest_message = json.loads(r.content)
last_viewed = latest_message[0]['id']

try:
    led = gpiozero.LED(17)
except gpiozero.exc.BadPinFactory:
    led = None # probably not running on the Pi, but that's okay

while True:
    # now that we have the gateway set up, we could make this smarter and actually respond to
    # events on the websocket instead of polling once a second, but this is simpler for now...
    # we'd have to handle disconnects, regular heartbeat, etc.
    time.sleep(1)
    params = f"?after={last_viewed}"
    r = requests.get(f'{API_ENDPOINT}/channels/{channel}/messages{params}', headers=headers)
    latest_messages = json.loads(r.content)
    for message in latest_messages:
        content = message['content']
        if "spibot: light LED" in content and led:
            print_to_channel("lighting LED")
            led.on()
        if "spibot: turn off LED" in content and led:
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
