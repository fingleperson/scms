import os
import requests
import datetime

API_KEY = os.getenv("OPEN_CLOUD_API_KEY")
ID = os.getenv("ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
DATASTORE_NAME = "analyticsdata"
STAT_KEYS = ["earned", "spent", "casualties"]

def get_stat(stat_name):
    url = f"https://apis.roblox.com/datastores/v1/universes/{ID}/standard-datastores/datastore/entries/entry"
    params = {"datastoreName": DATASTORE_NAME, "entryKey": stat_name}
    headers = {"x-api-key": API_KEY}
    r = requests.get(url, headers=headers, params=params)
    if r.status_code == 200:
        data = r.json()

        if isinstance(data, dict):
            return float(data.get("value", 0))
        elif isinstance(data, (float, int)):
            return float(data)
        else:
            return 0
    else:
        return 0

def set_stat(stat_name, value):
    url = f"https://apis.roblox.com/datastores/v1/universes/{ID}/standard-datastores/datastore/entries/entry"
    params = {"datastoreName": DATASTORE_NAME, "entryKey": stat_name}
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    requests.post(url, headers=headers, params=params, json={"value": value})

def post():
    earned = get_stat("earned")
    spent = get_stat("spent")
    casualties = get_stat("casualties")

    embed = {
        "title": "WEEKLY REPORT",
        "description": f"FROM {datetime.datetime.today().strftime('%d/%m/%Y')}",

        "fields": [
            {
                "name": "EARNED",
                "value": f"${earned:,}",
                "inline": True
            },
            {
                "name": "SPENT",
                "value": f"${spent:,}",
                "inline": True
            },
            {
                "name": "TOTAL",
                "value": f"${round(earned - spent, 2):,}",
                "inline": True
            },
            {
                "name": "CASUALTIES",
                "value": f"{casualties:,}",
                "inline": False
            },
        ],

        "timestamp": datetime.datetime.now(tz=datetime.UTC).isoformat()
    }
    payload = {"embeds": [embed]}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    post()
    for key in STAT_KEYS:
        set_stat(key, 0)
