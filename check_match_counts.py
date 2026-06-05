import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM matches WHERE group_name IS NOT NULL AND group_name != ""')
print('Group matches:', cursor.fetchone()[0])
cursor.execute('SELECT COUNT(*) FROM matches WHERE stage = "1/16决赛"')
print('Knockout matches:', cursor.fetchone()[0])
cursor.execute('SELECT COUNT(*) FROM matches')
print('Total matches:', cursor.fetchone()[0])