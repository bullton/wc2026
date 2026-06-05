import sqlite3
conn = sqlite3.connect('worldcup.db')
cur = conn.cursor()

print("淘汰赛 73-88 的详细数据 (包括 group_name):")
cur.execute('SELECT id, group_name, home_team, away_team, stage FROM matches WHERE id BETWEEN 73 AND 88')
for row in cur.fetchall():
    print(f"ID {row[0]}: group_name='{row[1]}', {row[2]} vs {row[3]}, stage={row[4]}")

conn.close()