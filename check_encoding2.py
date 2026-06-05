import sqlite3
import json

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
c = conn.cursor()
c.execute('SELECT id, home_team FROM matches WHERE id=90')
row = c.fetchone()

# Write to file
with open('check_output.txt', 'w', encoding='utf-8') as f:
    f.write(f'row type: {type(row)}\n')
    f.write(f'row[1] type: {type(row[1])}\n')
    f.write(f'row[1] value: {row[1]}\n')
    f.write(f'row[1] bytes: {row[1].encode("utf-8").hex()}\n')
    f.write(f'decode test: {row[1].encode("raw_unicode_escape").decode("utf-8", errors="replace")}\n')

conn.close()

# Now try to read the API and save
import urllib.request
url = 'http://localhost:5000/api/matches?year=2026'
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    with open('api_output.json', 'w', encoding='utf-8') as f:
        json.dump([m for m in data if m['id'] in [89,90]], f, ensure_ascii=False)

print("Files written")