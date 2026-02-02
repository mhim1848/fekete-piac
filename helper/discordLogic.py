import requests
import configuration as conf

def post_to_discord(message):
    payload = {"content": message}
    r = requests.post(conf.DISCORD_WEBHOOK_URL, json=payload)
    r.raise_for_status()

