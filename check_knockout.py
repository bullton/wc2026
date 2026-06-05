import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT id, home_team, away_team FROM matches WHERE id BETWEEN 73 AND 88 ORDER BY id")
for row in cursor.fetchall():
    print(f"{row['id']}: {row['home_team']} | {row['away_team']}")
