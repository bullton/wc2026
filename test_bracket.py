"""
Tests for the official R32 bracket definition and third-place assignment logic.

Verifies the rewrite against the official FIFA 2026 World Cup rules:
1. OFFICIAL_R32_BRACKET has 16 matches (73-88) with correct slot assignments.
2. The 8 third-place slots and their pools match Wikipedia/Annex C exactly.
3. The 495-entry combinations table is complete.
4. For each of the 495 third-place qualifiers combinations, the assignment pattern
   places each group into a match whose pool actually contains that group.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bracket import (
    OFFICIAL_R32_BRACKET,
    slot_string_for_match,
    slot_to_pool_groups,
)
from combinations import COMBINATIONS as FIFA_COMBINATIONS


def test_bracket_has_16_matches():
    assert len(OFFICIAL_R32_BRACKET) == 16, f"Expected 16 matches, got {len(OFFICIAL_R32_BRACKET)}"
    assert set(OFFICIAL_R32_BRACKET.keys()) == set(range(73, 89)), "Match IDs should be 73-88"


def test_bracket_has_eight_third_place_matches():
    third_place_matches = [mid for mid, (_, away) in OFFICIAL_R32_BRACKET.items() if away[0] == '3']
    expected = {74, 77, 79, 80, 81, 82, 85, 87}
    assert set(third_place_matches) == expected, (
        f"Third-place matches should be {expected}, got {set(third_place_matches)}"
    )


def test_slot_strings_match_official_pools():
    expected_slots = {
        74: 'A/B/C/D/F3',
        77: 'C/D/F/G/H3',
        79: 'C/E/F/H/I3',
        80: 'E/H/I/J/K3',
        81: 'B/E/F/I/J3',
        82: 'A/E/H/I/J3',
        85: 'E/F/G/I/J3',
        87: 'D/E/I/J/L3',
    }
    for mid, expected_slot in expected_slots.items():
        actual_slot = slot_string_for_match(mid)
        assert actual_slot == expected_slot, (
            f"Match {mid}: expected slot {expected_slot}, got {actual_slot}"
        )


def test_slot_pool_groups_consistent():
    pools = slot_to_pool_groups()
    expected_pools = {
        'A/B/C/D/F3': frozenset(['A', 'B', 'C', 'D', 'F']),
        'C/D/F/G/H3': frozenset(['C', 'D', 'F', 'G', 'H']),
        'C/E/F/H/I3': frozenset(['C', 'E', 'F', 'H', 'I']),
        'E/H/I/J/K3': frozenset(['E', 'H', 'I', 'J', 'K']),
        'B/E/F/I/J3': frozenset(['B', 'E', 'F', 'I', 'J']),
        'A/E/H/I/J3': frozenset(['A', 'E', 'H', 'I', 'J']),
        'E/F/G/I/J3': frozenset(['E', 'F', 'G', 'I', 'J']),
        'D/E/I/J/L3': frozenset(['D', 'E', 'I', 'J', 'L']),
    }
    assert pools == expected_pools, (
        f"Slot pools mismatch:\n  got {pools}\n  exp {expected_pools}"
    )


def test_combinations_table_has_495_entries():
    assert len(FIFA_COMBINATIONS) == 495, f"Expected 495 combinations, got {len(FIFA_COMBINATIONS)}"


def test_combinations_assignment_valid_for_all_scenarios():
    """For every one of the 495 combinations, each match_id's assigned group
    must belong to that match's pool."""
    invalid = []
    for qualifiers, pattern in FIFA_COMBINATIONS.items():
        for match_id, group in pattern.items():
            if match_id not in OFFICIAL_R32_BRACKET:
                invalid.append(f"Match {match_id} not in bracket")
                continue
            away_src = OFFICIAL_R32_BRACKET[match_id][1]
            if away_src[0] != '3':
                invalid.append(f"Match {match_id} is not a third-place match")
                continue
            if group not in away_src[1]:
                invalid.append(
                    f"Combination {set(qualifiers)} assigns group {group} to match "
                    f"{match_id} (pool {set(away_src[1])})"
                )
    assert not invalid, (
        f"Found {len(invalid)} invalid assignments:\n" + "\n".join(invalid[:10])
    )


def test_combinations_cover_each_match_exactly_once():
    """For every combination, each of the 8 third-place match slots must be filled
    exactly once (no duplicates, no omissions)."""
    bad = []
    for qualifiers, pattern in FIFA_COMBINATIONS.items():
        if len(pattern) != 8:
            bad.append(f"{set(qualifiers)}: pattern has {len(pattern)} entries, expected 8")
            continue
        if set(pattern.keys()) != {74, 77, 79, 80, 81, 82, 85, 87}:
            bad.append(f"{set(qualifiers)}: pattern keys mismatch")
        if len(set(pattern.values())) != 8:
            bad.append(f"{set(qualifiers)}: duplicate group in pattern")
        if set(pattern.values()) != set(qualifiers):
            bad.append(f"{set(qualifiers)}: pattern values != qualifiers")
    assert not bad, "Pattern integrity issues:\n" + "\n".join(bad[:10])


def test_wikipedia_option_67_exact_match():
    """Wikipedia Option #67 for B,D,E,F,I,J,K,L qualifiers:
       1A vs 3E (match 79), 1B vs 3J (match 85), 1D vs 3B (match 81), 1E vs 3D (match 74),
       1G vs 3I (match 82), 1I vs 3F (match 77), 1K vs 3L (match 87), 1L vs 3K (match 80)
    """
    pattern = FIFA_COMBINATIONS[frozenset(['B', 'D', 'E', 'F', 'I', 'J', 'K', 'L'])]
    expected = {79: 'E', 85: 'J', 81: 'B', 74: 'D', 82: 'I', 77: 'F', 87: 'L', 80: 'K'}
    assert pattern == expected, (
        f"B,D,E,F,I,J,K,L pattern mismatch:\n  got {pattern}\n  exp {expected}"
    )


def test_no_team_plays_itself():
    """No R32 match should pit a team against itself (i.e., no match where the home
    group source equals the away group source)."""
    issues = []
    for mid, (home_src, away_src) in OFFICIAL_R32_BRACKET.items():
        if home_src[0] in ('W', 'R') and away_src[0] in ('W', 'R'):
            if home_src[1] == away_src[1] and home_src[0] == away_src[0]:
                issues.append(f"Match {mid}: same group+rank on both sides ({home_src})")
        elif home_src[0] == '3' and away_src[0] == '3':
            if home_src[1] == away_src[1]:
                issues.append(f"Match {mid}: same third-place pool on both sides")
    assert not issues, "Self-match issues: " + "; ".join(issues)


if __name__ == '__main__':
    import traceback
    tests = [
        ('bracket_has_16_matches', test_bracket_has_16_matches),
        ('bracket_has_eight_third_place_matches', test_bracket_has_eight_third_place_matches),
        ('slot_strings_match_official_pools', test_slot_strings_match_official_pools),
        ('slot_pool_groups_consistent', test_slot_pool_groups_consistent),
        ('combinations_table_has_495_entries', test_combinations_table_has_495_entries),
        ('combinations_assignment_valid_for_all_scenarios',
         test_combinations_assignment_valid_for_all_scenarios),
        ('combinations_cover_each_match_exactly_once',
         test_combinations_cover_each_match_exactly_once),
        ('wikipedia_option_67_exact_match', test_wikipedia_option_67_exact_match),
        ('no_team_plays_itself', test_no_team_plays_itself),
    ]
    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f'PASS  {name}')
            passed += 1
        except Exception:
            print(f'FAIL  {name}')
            traceback.print_exc()
            failed += 1
    print(f'\n{passed}/{len(tests)} tests passed')
    sys.exit(0 if failed == 0 else 1)