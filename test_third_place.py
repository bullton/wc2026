import sqlite3
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

def test_third_place_bracket():
    conn = sqlite3.connect('D:/Code/wc2026/worldcup.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM matches WHERE match_date LIKE "2026-%" ORDER BY match_date, match_time')
    all_matches = [dict(row) for row in cursor.fetchall()]

    from app import (calculate_all_third_place_teams, match_knockout_matrix,
                     has_group_matches_played, calculate_group_standings,
                     is_team_ranked_for_position)

    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

    third_place_teams = calculate_all_third_place_teams(all_matches)
    print("=== 第三名球队（按排名）===")
    for i, t in enumerate(third_place_teams):
        print(f"  {i+1}. {t['team']} (组{t['group']}) - {t['points']}分, GD={t['gd']}")

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

    print(f"\n=== 已确认排名的组: {qualifier_groups} ===")

    matched_thirds = match_knockout_matrix(qualifier_groups, third_place_teams)
    print("\n=== 匹配结果 ===")
    for t in matched_thirds:
        print(f"  {t['team']} (组{t['group']}) -> 位置码{t['third_code']}, 排名{t['rank']}")

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

    third_by_group = {t['group']: t for t in matched_thirds}

    print("\n=== 各位置槽位候选球队 ===")
    for slot, eligible in slot_groups.items():
        candidates = []
        for g in eligible:
            if g in third_by_group:
                t = third_by_group[g]
                candidates.append((t['team'], f"组{g}", t['rank']))
        candidates.sort(key=lambda x: x[2])
        print(f"  {slot}: {candidates}")

    print("\n=== 贪心填充结果 ===")
    filled = {}
    used = set()
    for m in all_matches:
        if m['stage'] != '1/16决赛':
            continue
        home, away = m['home_team'], m['away_team']
        third_slots = list(slot_groups.keys())
        current_slot = None
        for slot in third_slots:
            if home == slot or away == slot:
                current_slot = slot
                break
        if not current_slot:
            continue
        if current_slot in filled:
            print(f"  赛事{m['id']}: {home} vs {away} -> {filled[current_slot]['team']} (已填充)")
            continue
        eligible = slot_groups.get(current_slot, [])
        best = None
        best_rank = 999
        for g in eligible:
            if g in third_by_group and g not in used:
                t = third_by_group[g]
                if t['rank'] < best_rank:
                    best_rank = t['rank']
                    best = t
        if best:
            filled[current_slot] = best
            used.add(best['group'])
            print(f"  赛事{m['id']}: {home} vs {away} -> {best['team']} (组{best['group']})")
        else:
            print(f"  赛事{m['id']}: {home} vs {away} -> 无球队可选!")

    print(f"\n=== 填充了 {len(filled)}/{len(slot_groups)} 个位置槽 ===")

    conn.close()

if __name__ == '__main__':
    test_third_place_bracket()