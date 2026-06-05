import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM matches WHERE stage = '小组赛' AND (home_score = '' OR away_score = '')")
print('未填分数:', cursor.fetchone()[0])
cursor.execute("SELECT COUNT(*) FROM matches WHERE stage = '小组赛'")
print('总小组赛:', cursor.fetchone()[0])
