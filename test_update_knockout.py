import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute('SELECT * FROM matches WHERE match_date LIKE "2026-%" ORDER BY match_date, match_time')
all_matches = [dict(row) for row in cursor.fetchall()]

print(f"总比赛数: {len(all_matches)}")

from app import (calculate_all_third_place_teams, match_knockout_matrix,
                 has_group_matches_played, calculate_group_standings,
                 is_team_ranked_for_position, is_group_completed)

groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

third_place_teams = calculate_all_third_place_teams(all_matches)
print(f"第三名球队数: {len(third_place_teams)}")

qualifier_groups = []
for group in groups:
    if not has_group_matches_played(group, all_matches):
        continue
    standings = calculate_group_standings(group, all_matches)
    if len(standings) >= 2:
        first_locked = is_team_ranked_for_position(group, all_matches, 1)
        second_locked = is_team_ranked_for_position(group, all_matches, 2)
        if first_locked and second_locked:
            qualifier_groups.append(group)

print(f"已确认排名的组: {qualifier_groups}")

matched_thirds = match_knockout_matrix(qualifier_groups, third_place_teams)
third_by_group = {t['group']: t for t in matched_thirds}

print(f"third_by_group: {list(third_by_group.keys())}")

slot_groups = {
    'A/B/C/D/F3': ['A', 'B', 'C', 'D', 'F'],
    'C/D/F/G/H3': ['C', 'D', 'F', 'G', 'H'],
    'C/E/F/H/I3': ['C', 'E', 'F', 'H', 'I'],
    'E/H/I/J/K3': ['E', 'H', 'I', 'J', 'K'],
    'A/E/H/I/J3': ['A', 'E', 'H', 'I', 'J'],
    'B/E/F/I/J3': ['B', 'E', 'F', 'I', 'J'],
    'E/F/G/I/J3': ['E', 'F', 'G', 'I', 'J'],
    'D/E/I/J/L3': ['D', 'E', 'I', 'J', 'L']
}

third_slots = ['A/B/C/D/F3', 'C/D/F/G/H3', 'C/E/F/H/I3', 'E/H/I/J/K3',
               'A/E/H/I/J3', 'B/E/F/I/J3', 'E/F/G/I/J3', 'D/E/I/J/L3']

print("\n=== 测试模拟更新所有淘汰赛 ===")

conn2 = sqlite3.connect('D:/Code/wc2026/worldcup.db')
cursor2 = conn2.cursor()

knockout_mapping = {
    73: ('A', 2), 74: ('C', 1), 75: ('E', 1), 76: ('F', 1),
    77: ('E', 2), 78: ('I', 1), 79: ('A', 1), 80: ('L', 1),
    81: ('G', 1), 82: ('D', 1), 83: ('H', 1), 84: ('K', 2),
    85: ('B', 1), 86: ('D', 2), 87: ('J', 1), 88: ('K', 1)
}

print("第一步：填充第一名")
for match_id, (group, position) in knockout_mapping.items():
    if is_group_completed(group, all_matches):
        standings = calculate_group_standings(group, all_matches)
        if len(standings) >= position:
            team = standings[position - 1]['team']
            team_with_pos = f"{team}({group}{position})"
            cursor2.execute('UPDATE matches SET home_team = ? WHERE id = ?', (team_with_pos, match_id))
            print(f"  Match {match_id}: set home to {team_with_pos}")

conn2.commit()

second_place_mapping = {
    73: ('B', 2), 74: ('F', 2), 76: ('C', 2), 77: ('I', 2),
    83: ('J', 2), 84: ('L', 2), 87: ('H', 2), 86: ('G', 2)
}

print("\n第二步：填充第二名")
for match_id, (group, position) in second_place_mapping.items():
    if is_group_completed(group, all_matches):
        standings = calculate_group_standings(group, all_matches)
        if len(standings) >= position:
            team = standings[position - 1]['team']
            team_with_pos = f"{team}({group}{position})"
            cursor2.execute('UPDATE matches SET away_team = ? WHERE id = ?', (team_with_pos, match_id))
            print(f"  Match {match_id}: set away to {team_with_pos}")

conn2.commit()

print("\n第三步：填充第三名")
filled_slots = {}
used_third_groups = set()

for match in all_matches:
    if match['stage'] != '1/16决赛':
        continue

    home = match['home_team']
    away = match['away_team']

    current_slot = None
    if home in third_slots:
        current_slot = home
    elif away in third_slots:
        current_slot = away
    else:
        continue

    if current_slot in filled_slots:
        team_data = filled_slots[current_slot]
        team_name = f"{team_data['team']}({team_data['third_code']})"
        if home == current_slot:
            cursor2.execute('UPDATE matches SET home_team = ? WHERE id = ?', (team_name, match['id']))
        else:
            cursor2.execute('UPDATE matches SET away_team = ? WHERE id = ?', (team_name, match['id']))
        print(f"  Match {match['id']}: {home} vs {away} -> already filled {team_name}")
        continue

    eligible_groups = slot_groups.get(current_slot, [])
    best_team = None
    best_rank = float('inf')

    for group in eligible_groups:
        if group in third_by_group and group not in used_third_groups:
            team_data = third_by_group[group]
            if team_data['rank'] < best_rank:
                best_rank = team_data['rank']
                best_team = team_data

    if best_team:
        filled_slots[current_slot] = best_team
        used_third_groups.add(best_team['group'])
        team_name = f"{best_team['team']}({best_team['third_code']})"
        if home == current_slot:
            cursor2.execute('UPDATE matches SET home_team = ? WHERE id = ?', (team_name, match['id']))
        else:
            cursor2.execute('UPDATE matches SET away_team = ? WHERE id = ?', (team_name, match['id']))
        print(f"  Match {match['id']}: {home} vs {away} -> filled with {team_name}")
    else:
        print(f"  Match {match['id']}: {home} vs {away} -> NO TEAM! eligible={eligible_groups}, used={list(used_third_groups)}")

conn2.commit()
conn2.close()

print(f"\n填充了 {len(filled_slots)}/8 个第三名位置槽")

print("\n=== 最终数据库状态 ===")
cursor.execute('SELECT id, home_team, away_team FROM matches WHERE id BETWEEN 73 AND 88 ORDER BY id')
for row in cursor.fetchall():
    mid, home, away = row
    print(f"Match {mid}: {home} vs {away}")

conn.close()