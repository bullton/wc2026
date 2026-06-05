import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
cursor = conn.cursor()

print("=== 重置后的占位符状态 ===")
cursor.execute('SELECT id, home_team, away_team FROM matches WHERE id BETWEEN 73 AND 88 ORDER BY id')
for row in cursor.fetchall():
    mid, home, away = row
    print(f"Match {mid}: home='{home}' vs away='{away}'")