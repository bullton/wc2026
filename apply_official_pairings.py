import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
cur = conn.cursor()

placements = [
    (73, 'A2', 'B2'),
    (74, 'E1', 'A/B/C/D/F3'),
    (75, 'F1', 'C2'),
    (76, 'C1', 'F2'),
    (77, 'I1', 'C/D/F/G/H3'),
    (78, 'E2', 'I2'),
    (79, 'A1', 'C/E/F/H/I3'),
    (80, 'L1', 'E/H/I/J/K3'),
    (81, 'D1', 'B/E/F/I/J3'),
    (82, 'G1', 'A/E/H/I/J3'),
    (83, 'K2', 'L2'),
    (84, 'H1', 'J2'),
    (85, 'B1', 'E/F/G/I/J3'),
    (86, 'J1', 'H2'),
    (87, 'K1', 'D/E/I/J/L3'),
    (88, 'D2', 'G2'),
]
for mid, home, away in placements:
    cur.execute('UPDATE matches SET home_team=?, away_team=? WHERE id=?', (home, away, mid))

later = {
    89: ('74胜者', '77胜者'),
    90: ('73胜者', '75胜者'),
}
for mid, (home, away) in later.items():
    cur.execute('UPDATE matches SET home_team=?, away_team=? WHERE id=?', (home, away, mid))

conn.commit()
cur.execute("SELECT id, match_date, match_time, venue, home_team, away_team FROM matches WHERE id BETWEEN 73 AND 104 ORDER BY id")
for row in cur.fetchall():
    print(f"ID {row[0]:3d} {row[1]} {row[2]} {row[3]:<12}  {row[4]} vs {row[5]}")
conn.close()
