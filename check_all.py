import urllib.request
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

url = "http://localhost:5000/api/standings"
with urllib.request.urlopen(url) as response:
    standings = json.loads(response.read().decode('utf-8'))

determined = set()
groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
for g in groups:
    if not standings[g]:
        continue
    for i, s in enumerate(standings[g]):
        if s.get('is_ranking_locked'):
            key = s['team'] + f"({g}{i+1})"
            determined.add(key)
            print(f"Added to determined: {key}")

print(f"\nTotal determined teams: {len(determined)}")

url2 = "http://localhost:5000/api/matches"
with urllib.request.urlopen(url2) as response:
    matches = json.loads(response.read().decode('utf-8'))

print("\nChecking knockout matches:")
for m in matches:
    if 73 <= m['id'] <= 88:
        ht = m['home_team']
        at = m['away_team']
        ht_in = ht in determined
        at_in = at in determined
        print(f"{m['id']}: home={ht} (in determined: {ht_in}), away={at} (in determined: {at_in})")
