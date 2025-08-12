import os
import requests
import datetime

API_KEY = os.getenv("OPEN_CLOUD_API_KEY")
ID = os.getenv("ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
DATASTORE_NAME = "analyticsdata"
SCOPE = ""
STAT_KEYS = ["GAIN", "LOSS", "TOTAL"]

def get_stat(stat_name):
    url = f"https://apis.roblox.com/datastores/v1/universes/{ID}/standard-datastores/datastore/entries/entry"
    params = {"datastoreName": DATASTORE_NAME, "scope": SCOPE, "entryKey": stat_name}
    headers = {"x-api-key": API_KEY}
    r = requests.get(url, headers=headers, params=params)
    if r.status_code == 200:
        return int(r.json().get("value", 0))
    return 0

def set_stat(stat_name, value):
    url = f"https://apis.roblox.com/datastores/v1/universes/{ID}/standard-datastores/datastore/entries/entry"
    params = {"datastoreName": DATASTORE_NAME, "scope": SCOPE, "entryKey": stat_name}
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    requests.post(url, headers=headers, params=params, json={"value": value})

def post(stats):
    date_str = datetime.datetime.now(tz=datetime.UTC).isoformat()
    
    embed = {
        "title": "WEEKLY REVENUE REPORT",
        "description": f"FROM {date_str} (UTC)",
        "fields": [
            {"name": key, "value": str(value), "inline": True} for key, value in stats.items()
            ],
        "timestamp": datetime.datetime.now(tz=datetime.UTC).isoformat()
    }
    payload = {"embeds": [embed]}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    stats = {key: get_stat(key) for key in STAT_KEYS}
    post(stats)
    for key in STAT_KEYS:
        set_stat(key, 0)
