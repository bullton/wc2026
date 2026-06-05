import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('SELECT * FROM matches WHERE match_date LIKE "2026-%" ORDER BY match_date, match_time')
all_matches = [dict(row) for row in cursor.fetchall()]
print(f"Matches with 2026 date: {len(all_matches)}")

cursor.execute('SELECT * FROM matches WHERE match_date IS NULL OR match_date = ""')
null_dates = cursor.fetchall()
print(f"Matches with NULL/empty date: {len(null_dates)}")
for row in null_dates:
    print(f"  Match {row['id']}: date={row['match_date']}, {row['home_team']} vs {row['away_team']}")