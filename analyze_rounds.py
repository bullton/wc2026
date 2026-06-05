from database import init_db
import sqlite3

init_db()

conn = sqlite3.connect('worldcup.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute('SELECT * FROM matches WHERE group_name != "" ORDER BY id')
matches = [dict(row) for row in cursor.fetchall()]
conn.close()

print(f"Total group stage matches: {len(matches)}")
print(f"Match IDs: {matches[0]['id']} to {matches[-1]['id']}")
print()

# Show all matches by ID
print("=== 所有小组赛比赛 ===")
for m in matches:
    print(f"[{m['id']:3d}] {m['match_date']} {m['home_team']:8s} vs {m['away_team']}")
