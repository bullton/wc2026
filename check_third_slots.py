import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
cursor = conn.cursor()

# Check all third place placeholder slots in DB
third_slots = ['A/B/C/D/F3', 'C/D/F/G/H3', 'C/E/F/H/I3', 'E/H/I/J/K3',
               'A/E/H/I/J3', 'B/E/F/I/J3', 'E/F/G/I/J3', 'D/E/I/J/L3']

cursor.execute('SELECT id, home_team, away_team FROM matches WHERE stage = "1/16决赛" ORDER BY id')
for row in cursor.fetchall():
    mid, home, away = row
    third_in_home = home in third_slots
    third_in_away = away in third_slots
    if third_in_home or third_in_away:
        print(f"Match {mid}: {home} vs {away} - third slots: home={third_in_home}, away={third_in_away}")