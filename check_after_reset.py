import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
cursor = conn.cursor()

print("=== After reset_knockout.py ===")
cursor.execute('SELECT id, home_team, away_team FROM matches WHERE id BETWEEN 73 AND 88 ORDER BY id')
for row in cursor.fetchall():
    mid, home, away = row
    is_third = '3' in home or '3' in away
    marker = " *** THIRD ***" if is_third else ""
    print(f"Match {mid}: {home} vs {away}{marker}")