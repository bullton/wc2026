import sqlite3

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')

# Test 1: bytes factory
conn.text_factory = bytes
c = conn.cursor()
c.execute('SELECT id, home_team FROM matches WHERE id=90')
row = c.fetchone()
print(f'bytes factory: id={row[0]}, home_team={row[1]}')
print(f'  decoded utf-8: {row[1].decode("utf-8")}')
conn.close()

# Test 2: str factory (default)
conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
conn.text_factory = str
c = conn.cursor()
c.execute('SELECT id, home_team FROM matches WHERE id=90')
row = c.fetchone()
print(f'str factory: id={row[0]}, home_team={repr(row[1])}')
print(f'  home_team bytes: {row[1].encode("utf-8").hex() if isinstance(row[1], str) else "N/A"}')
conn.close()

# Test 3: default (no factory)
conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
c = conn.cursor()
c.execute('SELECT id, home_team FROM matches WHERE id=90')
row = c.fetchone()
print(f'default factory: id={row[0]}, home_team={repr(row[1])}')
conn.close()