import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

from app import (calculate_all_third_place_teams, match_knockout_matrix,
                 has_group_matches_played, calculate_group_standings,
                 is_team_ranked_for_position)

def find_optimal_matching():
    """使用回溯算法找到最优匹配"""
    conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM matches WHERE match_date LIKE "2026-%" ORDER BY match_date, match_time')
    all_matches = [dict(row) for row in cursor.fetchall()]

    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    third_place_teams = calculate_all_third_place_teams(all_matches)

    qualifier_groups = []
    for group in groups:
        if not has_group_matches_played(group, all_matches):
            continue
        standings = calculate_group_standings(group, all_matches)
        if len(standings) >= 2:
            if is_team_ranked_for_position(group, all_matches, 1) and is_team_ranked_for_position(group, all_matches, 2):
                qualifier_groups.append(group)

    matched_thirds = match_knockout_matrix(qualifier_groups, third_place_teams)
    third_by_group = {t['group']: t for t in matched_thirds}

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

    third_slots = list(slot_groups.keys())
    third_groups = list(third_by_group.keys())

    print("=== 问题定义 ===")
    team_list = [(g, third_by_group[g]['team'], f"rank={third_by_group[g]['rank']}") for g in third_groups]
    print(f"第三名球队: {team_list}")
    print(f"\n槽位约束:")
    for slot in third_slots:
        eligible = slot_groups[slot]
        available = [g for g in eligible if g in third_by_group]
        print(f"  {slot}: 可用 {available}")

    def solve(assignment, used_groups, depth):
        if len(assignment) == len(third_slots):
            return assignment

        slot = third_slots[len(assignment)]
        eligible = slot_groups[slot]
        available = [g for g in eligible if g in third_by_group and g not in used_groups]

        if not available:
            return None

        available.sort(key=lambda g: third_by_group[g]['rank'])

        for g in available:
            new_assignment = assignment.copy()
            new_assignment[slot] = third_by_group[g]
            new_used = used_groups.copy()
            new_used.add(g)
            result = solve(new_assignment, new_used, depth + 1)
            if result:
                return result

        return None

    print("\n=== 使用回溯算法查找最优匹配 ===")
    result = solve({}, set(), 0)

    if result:
        print("找到完美匹配!")
        for slot, team_data in result.items():
            print(f"  {slot} -> {team_data['team']} (组{team_data['group']}, rank={team_data['rank']})")
        print(f"\n总计: {len(result)}/8 个槽位被填充")
    else:
        print("未找到完美匹配!")

    conn.close()

if __name__ == '__main__':
    find_optimal_matching()