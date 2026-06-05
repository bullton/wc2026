import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('SELECT * FROM knockout_matrix WHERE qualifier_groups = \'["A", "B", "C", "D", "E", "F", "G", "H"]\' LIMIT 1')
row = cursor.fetchone()
if row:
    print("qualifier_groups:", row['qualifier_groups'])
    print("third_places:", row['third_places'])

print("\n=== Third place details ===")
for m in cursor.execute('SELECT * FROM third_place_teams ORDER BY rank'):
    print(f"  {m['third_code']}: {m['team']} ({m['group']})")