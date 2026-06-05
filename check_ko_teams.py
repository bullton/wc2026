import sqlite3
conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
c = conn.cursor()
c.execute('SELECT id, home_team, away_team FROM matches WHERE id >= 89 AND id <= 104 ORDER BY id')
with open('ko_check.txt', 'w', encoding='utf-8') as f:
    for row in c.fetchall():
        f.write(f'ID {row[0]}: home={row[1]}, away={row[2]}\n')
conn.close()