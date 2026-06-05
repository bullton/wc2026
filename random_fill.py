import sqlite3
import random
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT id, match_date, match_time, group_name, home_team, away_team FROM matches WHERE stage = '小组赛' ORDER BY id LIMIT 60 OFFSET 48")
matches = [dict(row) for row in cursor.fetchall()]

for m in matches:
    home_score = random.randint(0, 4)
    away_score = random.randint(0, 4)
    cursor.execute("UPDATE matches SET home_score = ?, away_score = ? WHERE id = ?", (home_score, away_score, m['id']))
    print(f"{m['group_name']}组 {m['match_date']}: {m['home_team']} {home_score}-{away_score} {m['away_team']}")

conn.commit()
print(f"\n共填充 {len(matches)} 场")
