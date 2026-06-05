import urllib.request, json
url = 'http://localhost:5000/api/matches?year=2026'
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    with open('api_verify.json', 'w', encoding='utf-8') as f:
        json.dump([m for m in data if m['id'] in [89,90]], f, ensure_ascii=False)
print("Done")