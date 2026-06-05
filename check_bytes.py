import sqlite3
conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
conn.text_factory = bytes
c = conn.cursor()
c.execute('SELECT id, home_team FROM matches WHERE id IN (73, 90)')
for row in c.fetchall():
    try:
        decoded = row[1].decode('utf-8')
        print(f'ID {row[0]}: {row[1].hex()} = {decoded}')
    except Exception as e:
        print(f'ID {row[0]}: {row[1].hex()} = DECODE ERROR: {e}')
conn.close()