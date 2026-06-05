import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute('SELECT * FROM matches WHERE match_date LIKE "2026-%" ORDER BY match_date, match_time')
all_matches = [dict(row) for row in cursor.fetchall()]
print(f"Total matches: {len(all_matches)}")

group_matches = [m for m in all_matches if m.get('group_name')]
print(f"Group matches: {len(group_matches)}")
for m in group_matches[:6]:
    print(f"  Match {m['id']}: group={m['group_name']}, {m['home_team']} vs {m['away_team']}")