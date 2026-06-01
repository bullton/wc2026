import sqlite3
conn = sqlite3.connect('worldcup.db')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM matches')
print(f'数据库比赛总数: {cur.fetchone()[0]}')
cur.execute('SELECT COUNT(*) FROM matches WHERE home_score != "" AND away_score != ""')
print(f'已有比分的比赛数: {cur.fetchone()[0]}')
cur.execute('SELECT * FROM matches LIMIT 3')
rows = cur.fetchall()
print('\n前3场比赛数据:')
for row in rows:
    print(row)
conn.close()
