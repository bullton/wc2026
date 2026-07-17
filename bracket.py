"""
Official 2026 FIFA World Cup Round of 32 bracket definition.

Source: FIFA tournament regulations Annex C,
Wikipedia "2026 FIFA World Cup knockout stage" (Combinations of matches in the round of 32).

Each match in the Round of 32 is defined by (home_source, away_source):
- ('W', group): group winner (1st place)
- ('R', group): group runner-up (2nd place)
- ('3', frozenset): third-place team from a pool of groups

For third-place matches, the specific group assigned to each match is determined
by which 8 third-place teams qualify (see COMBINATIONS in combinations.py).

Match IDs follow the official FIFA numbering:
- 73-88: Round of 32 (16 matches)
"""

OFFICIAL_R32_BRACKET = {
    73: (('R', 'A'), ('R', 'B')),
    74: (('W', 'E'), ('3', frozenset(['A', 'B', 'C', 'D', 'F']))),
    75: (('W', 'F'), ('R', 'C')),
    76: (('W', 'C'), ('R', 'F')),
    77: (('W', 'I'), ('3', frozenset(['C', 'D', 'F', 'G', 'H']))),
    78: (('R', 'E'), ('R', 'I')),
    79: (('W', 'A'), ('3', frozenset(['C', 'E', 'F', 'H', 'I']))),
    80: (('W', 'L'), ('3', frozenset(['E', 'H', 'I', 'J', 'K']))),
    81: (('W', 'D'), ('3', frozenset(['B', 'E', 'F', 'I', 'J']))),
    82: (('W', 'G'), ('3', frozenset(['A', 'E', 'H', 'I', 'J']))),
    83: (('R', 'K'), ('R', 'L')),
    84: (('W', 'H'), ('R', 'J')),
    85: (('W', 'B'), ('3', frozenset(['E', 'F', 'G', 'I', 'J']))),
    86: (('W', 'J'), ('R', 'H')),
    87: (('W', 'K'), ('3', frozenset(['D', 'E', 'I', 'J', 'L']))),
    88: (('R', 'D'), ('R', 'G')),
}


def slot_string_for_pool(pool):
    """Build the slot string for a third-place pool, e.g. frozenset(['C','E','F','H','I']) -> 'C/E/F/H/I3'."""
    return '/'.join(sorted(pool)) + '3'


def slot_string_for_match(match_id):
    """Return the third-place slot string for a match_id, or None if not a third-place match."""
    sources = OFFICIAL_R32_BRACKET.get(match_id)
    if not sources:
        return None
    away_src = sources[1]
    if away_src[0] != '3':
        return None
    return slot_string_for_pool(away_src[1])


def pool_groups_for_slot(slot_string):
    """Return the frozenset of groups for a slot string like 'C/E/F/H/I3'."""
    if not slot_string or not slot_string.endswith('3'):
        return None
    return frozenset(slot_string[:-1].split('/'))


def match_id_to_slot():
    """Return dict mapping match_id -> slot_string for third-place matches."""
    return {mid: slot for mid in OFFICIAL_R32_BRACKET if (slot := slot_string_for_match(mid))}


def slot_to_pool_groups():
    """Return dict mapping slot_string -> frozenset of groups."""
    return {slot: pool_groups_for_slot(slot) for slot in match_id_to_slot().values()}