import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('http://localhost:5000/api/knockout')
data = r.json()

print("=== 淘汰赛数据 ===")
for match in data[:16]:
    print(f"Match {match['id']}: {match['home_team']} vs {match['away_team']}")