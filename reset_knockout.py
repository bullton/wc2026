import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
cursor = conn.cursor()

placeholder_map = {
    73: ('A2', 'B2'),
    74: ('E1', 'A/B/C/D/F3'),
    75: ('F1', 'C2'),
    76: ('C1', 'F2'),
    77: ('I1', 'C/D/F/G/H3'),
    78: ('E2', 'I2'),
    79: ('A1', 'C/E/F/H/I3'),
    80: ('L1', 'E/H/I/J/K3'),
    81: ('D1', 'B/E/F/I/J3'),
    82: ('G1', 'A/E/H/I/J3'),
    83: ('K2', 'L2'),
    84: ('H1', 'J2'),
    85: ('B1', 'E/F/G/I/J3'),
    86: ('J1', 'H2'),
    87: ('K1', 'D/E/I/J/L3'),
    88: ('D2', 'G2')
}

for mid, (home, away) in placeholder_map.items():
    cursor.execute('UPDATE matches SET home_team = ?, away_team = ? WHERE id = ?', (home, away, mid))

conn.commit()
print("Reset knockout matches to placeholders")
