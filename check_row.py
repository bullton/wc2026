import sqlite3

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute('SELECT id, home_team FROM matches WHERE id IN (73, 90)')
for row in c.fetchall():
    print(f'ID {row["id"]}: {repr(row["home_team"])}')
    print(f'  bytes: {row["home_team"].encode("utf-8").hex()}')
conn.close()