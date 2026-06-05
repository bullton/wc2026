import urllib.request
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

url = "http://localhost:5000/api/standings"
with urllib.request.urlopen(url) as response:
    standings = json.loads(response.read().decode('utf-8'))

groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
for g in groups:
    if not standings[g]:
        continue
    print(f"\n=== {g}组 ===")
    for i, s in enumerate(standings[g]):
        locked = s.get('is_ranking_locked', False)
        qual = s.get('is_qualified', False)
        print(f"  {i+1}. {s['team']}: pts={s['points']}, GD={s['gd']}, locked={locked}, qualified={qual}")
