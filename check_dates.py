import sqlite3
conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
cursor = conn.cursor()
cursor.execute("SELECT id, stage, match_date, match_time, venue FROM matches WHERE stage LIKE '%1/16%' OR stage LIKE '%1/8%' OR stage LIKE '%1/4%' OR stage LIKE '%半决赛%' OR stage LIKE '%决赛%' ORDER BY id")
for row in cursor.fetchall():
    print(row)
conn.close()