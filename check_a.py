import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT id, home_team, home_score, away_score, away_team FROM matches WHERE group_name = 'A' ORDER BY id")
for row in cursor.fetchall():
    print(f"id={row['id']} {row['home_team']} {row['home_score']}-{row['away_score']} {row['away_team']}")
