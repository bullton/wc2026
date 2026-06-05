import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

from app import (calculate_all_third_place_teams, match_knockout_matrix,
                 has_group_matches_played, calculate_group_standings,
                 is_team_ranked_for_position)

def test_third_place_with_matching():
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
    print("\n=== 矩阵匹配结果 ===")
    for t in matched_thirds:
        print(f"  {t['team']} (组{t['group']}) -> {t['third_code']}, 排名{t['rank']}")

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

    print("\n=== 各位置槽位分析 ===")
    for slot in third_slots:
        eligible = slot_groups[slot]
        available = []
        for g in eligible:
            if g in third_by_group:
                available.append((g, third_by_group[g]['team'], third_by_group[g]['rank']))
        available.sort(key=lambda x: x[2])
        print(f"  {slot}:")
        for g, team, rank in available:
            print(f"    - {team} (组{g}, 排名{rank})")

    print("\n=== 贪心匹配结果 ===")
    filled = {}
    used_groups = set()

    for slot in third_slots:
        eligible = slot_groups[slot]
        best = None
        best_rank = 999

        for g in eligible:
            if g in third_by_group and g not in used_groups:
                t = third_by_group[g]
                if t['rank'] < best_rank:
                    best_rank = t['rank']
                    best = t

        if best:
            filled[slot] = best
            used_groups.add(best['group'])
            print(f"  {slot} -> {best['team']} (组{best['group']}, 排名{best['rank']})")
        else:
            print(f"  {slot} -> 无可用球队! eligible={eligible}, used={list(used_groups)}")

    print(f"\n填充: {len(filled)}/8")

    print("\n=== 问题分析 ===")
    if len(filled) < 8:
        print("问题：某些槽位找不到合适的第三名球队")
        for slot in third_slots:
            if slot not in filled:
                print(f"  {slot} 无法填充:")
                eligible = slot_groups[slot]
                available = []
                for g in eligible:
                    if g in third_by_group:
                        status = "已使用" if g in used_groups else "未使用"
                        available.append(f"组{g}({third_by_group[g]['team']},{status})")
                    else:
                        available.append(f"组{g}(无第三名球队)")
                print(f"    候选: {available}")

    conn.close()

if __name__ == '__main__':
    test_third_place_with_matching()