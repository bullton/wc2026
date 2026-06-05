import urllib.request, json
url = 'http://localhost:5000/api/matches?year=2026'
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    for m in data:
        if m['id'] in range(89, 105):
            print(f"{m['id']}: home={m['home_team']}, away={m['away_team']}")