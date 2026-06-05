import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

from app import (calculate_all_third_place_teams, match_knockout_matrix,
                 has_group_matches_played, calculate_group_standings,
                 is_team_ranked_for_position)

def test_third_place_optimal_order():
    conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM matches WHERE match_date LIKE "2026-%" ORDER BY match_date, match_time')
    all_matches = [dict(row) for row in cursor.fetchall()]

    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    third_place_teams = calculate_all_third_place_teams(all_matches)

    print("=== 第三名球队（按排名）===")
    for i, t in enumerate(third_place_teams):
        print(f"  {i+1}. {t['team']} (组{t['group']})")

    qualifier_groups = []
    for group in groups:
        if not has_group_matches_played(group, all_matches):
            continue
        standings = calculate_group_standings(group, all_matches)
        if len(standings) >= 2:
            if is_team_ranked_for_position(group, all_matches, 1) and is_team_ranked_for_position(group, all_matches, 2):
                qualifier_groups.append(group)

    print(f"\n=== 确认排名的组: {qualifier_groups} ===")

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

    print("\n=== 按唯一性排序的槽位 ===")
    def count_unique_eligible(slot):
        eligible = slot_groups[slot]
        available = [g for g in eligible if g in third_by_group]
        return len(available)

    slot_list = list(slot_groups.items())
    slot_list.sort(key=lambda x: count_unique_eligible(x[0]))

    for slot, eligible in slot_list:
        available = [g for g in eligible if g in third_by_group]
        print(f"  {slot}: {len(available)}个候选 -> {available}")

    print("\n=== 最优匹配（优先处理受限槽位）===")
    filled = {}
    used_groups = set()

    for slot, eligible in slot_list:
        available = [g for g in eligible if g in third_by_group]
        best = None
        best_rank = 999

        for g in available:
            if g not in used_groups:
                t = third_by_group[g]
                if t['rank'] < best_rank:
                    best_rank = t['rank']
                    best = t

        if best:
            filled[slot] = best
            used_groups.add(best['group'])
            print(f"  {slot} -> {best['team']} (组{best['group']}, 排名{best['rank']})")
        else:
            print(f"  {slot} -> 无法填充! eligible={eligible}, used={list(used_groups)}")

    print(f"\n填充: {len(filled)}/8")

    if len(filled) < 8:
        print("\n=== 匈牙利算法或回溯 needed ===")
        print("当前已填充:")
        for slot, team in filled.items():
            print(f"  {slot} = {team['team']}")
        print("未填充的槽位及其候选:")
        for slot, eligible in slot_groups.items():
            if slot not in filled:
                available = [g for g in eligible if g in third_by_group and g not in used_groups]
                print(f"  {slot}: 可用={available}")

    conn.close()

if __name__ == '__main__':
    test_third_place_optimal_order()