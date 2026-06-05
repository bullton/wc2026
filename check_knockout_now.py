import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
cursor = conn.cursor()
cursor.execute('SELECT id, home_team, away_team FROM matches WHERE id BETWEEN 73 AND 88')
for row in cursor.fetchall():
    print(f"Match {row[0]}: {row[1]} vs {row[2]}")