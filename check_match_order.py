import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute('SELECT * FROM matches WHERE match_date LIKE "2026-%" ORDER BY match_date, match_time')
all_matches = [dict(row) for row in cursor.fetchall()]

third_slots = ['A/B/C/D/F3', 'C/D/F/G/H3', 'C/E/F/H/I3', 'E/H/I/J/K3',
               'A/E/H/I/J3', 'B/E/F/I/J3', 'E/F/G/I/J3', 'D/E/I/J/L3']

print("=== Match order in all_matches ===")
for i, m in enumerate(all_matches):
    if m['stage'] == '1/16决赛':
        home = m['home_team']
        away = m['away_team']
        for slot in third_slots:
            if home == slot or away == slot:
                print(f"{i}: Match {m['id']}: {home} vs {away}")