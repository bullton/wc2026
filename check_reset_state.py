import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
cursor = conn.cursor()

print("=== What reset_knockout.py sets ===")
placeholder_map = {
    73: ('A2', 'B2'),
    74: ('C1', 'F2'),
    75: ('E1', 'A/B/C/D/F3'),
    76: ('F1', 'C2'),
    77: ('E2', 'I2'),
    78: ('I1', 'C/D/F/G/H3'),
    79: ('A1', 'C/E/F/H/I3'),
    80: ('L1', 'E/H/I/J/K3'),
    81: ('G1', 'A/E/H/I/J3'),
    82: ('D1', 'B/E/F/I/J3'),
    83: ('H1', 'J2'),
    84: ('K2', 'L2'),
    85: ('B1', 'E/F/G/I/J3'),
    86: ('D2', 'G2'),
    87: ('J1', 'H2'),
    88: ('K1', 'D/E/I/J/L3')
}

for mid, (home, away) in placeholder_map.items():
    print(f"Match {mid}: {home} vs {away}")

print("\n=== What the DB currently has (after reset) ===")
cursor.execute('SELECT id, home_team, away_team FROM matches WHERE id BETWEEN 73 AND 88 ORDER BY id')
for row in cursor.fetchall():
    mid, home, away = row
    print(f"Match {mid}: {home} vs {away}")