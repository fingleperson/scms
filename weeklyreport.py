import os
import requests
import datetime

API_KEY = os.getenv("OPEN_CLOUD_API_KEY")
ID = os.getenv("ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
DATASTORE_NAME = "analyticsdata"
WORLD_DATASTORE = "worlddata"
STAT_KEYS = ["earned", "spent", "casualties"]
CUTOFF_DAYS = 30

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
    casualties = int(get_stat("casualties"))

    embed = {
        "title": "WEEKLY REPORT",
        "description": f"FROM {datetime.datetime.today().strftime('%m/%d/%Y')}",

        "fields": [
            {
                "name": "**REVENUE**",
                "value": "",
                "inline": False
            },
            {
                "name": "EARNED",
                "value": f"${round(earned, 2):,}",
                "inline": True
            },
            {
                "name": "SPENT",
                "value": f"${round(spent, 2):,}",
                "inline": True
            },
            {
                "name": "TOTAL",
                "value": f"${round(earned - spent, 2):,}",
                "inline": True
            },
            {
                "name": "**EMPLOYEES**",
                "value": "",
                "inline": False
            },
            {
                "name": "CASUALTIES",
                "value": f"{casualties:,}",
                "inline": False
            },
        ],

        "color": 0x3d5f3e,
        "timestamp": datetime.datetime.now(tz=datetime.UTC).isoformat()
    }
    payload = {"content": "<@&1405580107992662136>", "embeds": [embed]}
    r = requests.post(DISCORD_WEBHOOK_URL, json=payload, verify=True)
    print(r.status_code, r.text)

def cleanup_worlddata():
    url_list = f"https://apis.roblox.com/datastores/v1/universes/{ID}/standard-datastores/datastore/entries"
    params_list = {"datastoreName": WORLD_DATASTORE}
    headers = {"x-api-key": API_KEY}

    r = requests.get(url_list, headers=headers, params=params_list)
    if r.status_code != 200:
        print("failed listing worlddata keys:", r.text)
        return

    entries = r.json().get("data", [])
    cutoff = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=CUTOFF_DAYS)

    for entry in entries:
        key = entry.get("key")
        if not key:
            continue

        entry_url = f"https://apis.roblox.com/datastores/v1/universes/{ID}/standard-datastores/datastore/entries/entry"
        entry_params = {"datastoreName": WORLD_DATASTORE, "entryKey": key}

        r2 = requests.get(entry_url, headers=headers, params=entry_params)
        if r2.status_code != 200:
            print("failed getting key:", r.text)
            continue

        print("ughhh")
        print(r2.json())
        
        body = r2.json()
        attrs = body.get("attributes", {})

        ts = attrs.get("timestamp")
        if not ts:
            # requests.delete(entry_url, headers=headers, params=entry_params)
            continue
        
        ts_dt = datetime.datetime.fromtimestamp(ts, tz=datetime.UTC)

        # if ts_dt < cutoff:
            # requests.delete(entry_url, headers=headers, params=entry_params)

if __name__ == "__main__":
    # post()
    cleanup_worlddata()
    # for key in STAT_KEYS:
        # set_stat(key, 0)
