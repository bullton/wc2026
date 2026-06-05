import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code\wc2026/worldcup.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('SELECT * FROM matches WHERE group_name = "A" ORDER BY match_date, match_time')
for row in cursor.fetchall():
    print(f"Match {row['id']}: {row['home_team']} vs {row['away_team']}, score={row['home_score']}-{row['away_score']}")