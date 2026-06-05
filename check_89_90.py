import sqlite3
conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
c = conn.cursor()
c.execute('SELECT id, home_team FROM matches WHERE id IN (89, 90)')
for row in c.fetchall():
    print(f'ID {row[0]}: {repr(row[1])}')
conn.close()

# Check what the app.py would return
import sys
sys.path.insert(0, 'D:/Code/wc2026')
# Can't import app due to Flask dependencies, just check DB directly