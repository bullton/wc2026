import urllib.request
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

url = "http://localhost:5000/api/matches"
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode('utf-8'))

for m in data:
    if 73 <= m['id'] <= 88:
        print(f"{m['id']}: {m['home_team']} | {m['away_team']}")
