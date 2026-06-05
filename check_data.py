import sqlite3
conn = sqlite3.connect('worldcup.db')
cur = conn.cursor()

print('淘汰赛比赛:')
cur.execute('SELECT * FROM matches WHERE stage=? OR stage=? OR stage=?', ('1/16决赛', '1/8决赛', '1/4决赛'))
rows = cur.fetchall()
for row in rows:
    print(row)

print('\n阿尔及利亚比赛:')
cur.execute('SELECT * FROM matches WHERE home_team=? OR away_team=?', ('阿尔及利亚', '阿尔及利亚'))
rows = cur.fetchall()
for row in rows:
    print(row)
    
print('\n小组赛A组所有比赛:')
cur.execute('SELECT * FROM matches WHERE group_name=?', ('A',))
rows = cur.fetchall()
for row in rows:
    print(row)
    
conn.close()