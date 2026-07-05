import sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')

expected = {
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
    88: ('D2', 'G2'),
    89: ('74胜者', '77胜者'),
    90: ('73胜者', '75胜者'),
}

con = sqlite3.connect('D:/Code/wc2026/worldcup.db')
con.row_factory = sqlite3.Row
rows = con.execute('SELECT id, home_team, away_team FROM matches WHERE id BETWEEN 73 AND 90 ORDER BY id').fetchall()
ok = True
for r in rows:
    mid = r['id']
    exp = expected.get(mid)
    if exp is None: continue
    if (r['home_team'], r['away_team']) != exp:
        print(f"MISMATCH ID {mid}: got ({r['home_team']!r}, {r['away_team']!r}) expected {exp}")
        ok = False

print('✅ 全部一致' if ok else '❌ 仍有不一致')
con.close()
