import sqlite3
conn = sqlite3.connect('worldcup.db')
cur = conn.cursor()

knockout_fixes = [
    (73, 'A2', 'B2'),
    (74, 'C1', 'F2'),
    (75, 'E1', 'A/B/C/D/F3'),
    (76, 'F1', 'C2'),
    (77, 'E2', 'I2'),
    (78, 'I1', 'C/D/F/G/H3'),
    (79, 'A1', 'C/E/F/H/I3'),
    (80, 'L1', 'E/H/I/J/K3'),
    (81, 'G1', 'A/E/H/I/J3'),
    (82, 'D1', 'B/E/F/I/J3'),
    (83, 'H1', 'J2'),
    (84, 'K2', 'L2'),
    (85, 'B1', 'E/F/G/I/J3'),
    (86, 'D2', 'G2'),
    (87, 'J1', 'H2'),
    (88, 'K1', 'D/E/I/J/L3'),
]

for match_id, home, away in knockout_fixes:
    cur.execute('''
        UPDATE matches
        SET home_team = ?, away_team = ?
        WHERE id = ?
    ''', (home, away, match_id))

conn.commit()

print("淘汰赛占位符已修复!")
print("\n修复后的淘汰赛对阵:")
cur.execute('SELECT id, home_team, away_team FROM matches WHERE stage="1/16决赛" ORDER BY id')
for row in cur.fetchall():
    print(f"  ID {row[0]}: {row[1]} vs {row[2]}")

conn.close()