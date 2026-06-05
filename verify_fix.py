import sqlite3
conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
c = conn.cursor()
c.execute('SELECT id, home_team FROM matches WHERE id IN (89, 90)')
with open('verify.txt', 'w', encoding='utf-8') as f:
    for row in c.fetchall():
        f.write(f'ID {row[0]}: {repr(row[1])}\n')
conn.close()