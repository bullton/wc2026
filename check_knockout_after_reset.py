import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
cursor = conn.cursor()

print("=== After reset_knockout.py ===")
cursor.execute('SELECT id, home_team, away_team FROM matches WHERE id BETWEEN 73 AND 88 ORDER BY id')
for row in cursor.fetchall():
    mid, home, away = row
    if '3' in home or '3' in away:
        print(f"Match {mid}: {home} vs {away} *** HAS THIRD PLACE ***")
    elif 'A/' in home or 'A/' in away or 'B/' in home or 'B/' in away or 'C/' in home or 'C/' in away or 'D/' in home or 'D/' in away or 'E/' in home or 'E/' in away or 'F/' in home or 'F/' in away:
        print(f"Match {mid}: {home} vs {away} *** PLACEHOLDER ***")
    else:
        print(f"Match {mid}: {home} vs {away}")