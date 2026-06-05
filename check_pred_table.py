import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="match_predictions"')
print('Table exists:', cursor.fetchone() is not None)

try:
    cursor.execute('SELECT * FROM match_predictions LIMIT 5')
    for row in cursor.fetchall():
        print(row)
except Exception as e:
    print('Error:', e)

conn.close()