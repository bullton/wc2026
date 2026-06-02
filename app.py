from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import json
from database import init_db

app = Flask(__name__)
CORS(app)

FIFA_RANKINGS = {
    '阿根廷': 1, '法国': 2, '巴西': 3, '英格兰': 4, '比利时': 5,
    '葡萄牙': 6, '荷兰': 7, '西班牙': 8, '意大利': 9, '德国': 10,
    '克罗地亚': 11, '乌拉圭': 12, '墨西哥': 13, '哥伦比亚': 14, '美国': 15,
    '瑞士': 16, '厄瓜多尔': 17, '塞内加尔': 18, '威尔士': 19, '伊朗': 20,
    '塞尔维亚': 21, '摩洛哥': 22, '日本': 23, '波兰': 24, '瑞典': 25,
    '澳大利亚': 26, '韩国': 27, '秘鲁': 28, '挪威': 29, '奥地利': 30,
    '科特迪瓦': 31, '阿尔及利亚': 32, '丹麦': 33, '捷克': 34, '喀麦隆': 35,
    '乌克兰': 36, '智利': 37, '尼日利亚': 38, '埃及': 39, '苏格兰': 40,
    '突尼斯': 41, '加拿大': 42, '芬兰': 43, '委内瑞拉': 44, '沙特阿拉伯': 45,
    '希腊': 46, '土耳其': 47, '巴拉圭': 48, '罗马尼亚': 49, '牙买加': 50,
    '爱尔兰': 51, '阿尔巴尼亚': 52, '匈牙利': 53, '南非': 54, '玻利维亚': 55,
    '加纳': 56, '冰岛': 57, '新西兰': 58, '喀麦隆': 59, '萨尔瓦多': 60,
    '波斯尼亚和黑塞哥维那': 61, '黑山': 62, '北马其顿': 63, '菲律宾': 64,
    '越南': 65, '伊拉克': 66, '卡塔尔': 67, '民主刚果': 68, '巴拿马': 69,
    '斯洛伐克': 70, '巴拿马': 71, '中国': 72, '约旦': 73, '保加利亚': 74,
    '库拉索': 75, '佛得角': 76, '斯洛文尼亚': 77, '阿联酋': 78, '乌兹别克斯坦': 79,
    '哈萨克斯坦': 80, '尼泊尔': 81, '黎巴嫩': 82, '白俄罗斯': 83, '洪都拉斯': 84
}

GROUP_TEAMS = {
    'A': ['墨西哥', '南非', '韩国', '捷克'],
    'B': ['加拿大', '波黑', '卡塔尔', '瑞士'],
    'C': ['巴西', '摩洛哥', '海地', '苏格兰'],
    'D': ['美国', '澳大利亚', '土耳其', '巴拉圭'],
    'E': ['德国', '科特迪瓦', '厄瓜多尔', '库拉索'],
    'F': ['荷兰', '日本', '瑞典', '突尼斯'],
    'G': ['比利时', '埃及', '伊朗', '新西兰'],
    'H': ['西班牙', '沙特阿拉伯', '乌拉圭', '佛得角'],
    'I': ['法国', '伊拉克', '挪威', '塞内加尔'],
    'J': ['阿根廷', '奥地利', '约旦', '阿尔及利亚'],
    'K': ['葡萄牙', '哥伦比亚', '乌兹别克斯坦', '民主刚果'],
    'L': ['英格兰', '克罗地亚', '加纳', '巴拿马']
}

def get_db_connection():
    conn = sqlite3.connect('worldcup.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_match_result(home_score, away_score):
    if home_score == '' or away_score == '' or home_score is None or away_score is None:
        return None
    try:
        h = int(home_score)
        a = int(away_score)
        if h > a:
            return 'win'
        elif h < a:
            return 'lose'
        else:
            return 'draw'
    except:
        return None

def calculate_head_to_head_stats(teams, matches):
    h2h_stats = {}
    for team in teams:
        h2h_stats[team] = {'gd': 0, 'gf': 0, 'played': 0}

    for match in matches:
        if match['home_score'] == '' or match['away_score'] == '':
            continue
        if match['home_team'] in teams and match['away_team'] in teams:
            try:
                h_score = int(match['home_score'])
                a_score = int(match['away_score'])
                h2h_stats[match['home_team']]['gf'] += h_score
                h2h_stats[match['home_team']]['gd'] += h_score - a_score
                h2h_stats[match['away_team']]['gf'] += a_score
                h2h_stats[match['away_team']]['gd'] += a_score - h_score
                h2h_stats[match['home_team']]['played'] += 1
                h2h_stats[match['away_team']]['played'] += 1
            except:
                pass

    return h2h_stats

def calculate_fair_play_score(yellow, red):
    return yellow * 1 + red * 4

def get_fifa_ranking(team):
    for country, rank in FIFA_RANKINGS.items():
        if team == country:
            return rank
    return 999

def calculate_theoretical_max_points(team, group_matches):
    current_points = 0
    remaining_matches = 0
    
    for m in group_matches:
        if m['home_team'] != team and m['away_team'] != team:
            continue
        
        if m['home_score'] == '' or m['away_score'] == '':
            remaining_matches += 1
        else:
            is_home = m['home_team'] == team
            try:
                home_score = int(m['home_score'])
                away_score = int(m['away_score'])
                if home_score > away_score:
                    current_points += 3 if is_home else 0
                elif home_score == away_score:
                    current_points += 1
            except:
                remaining_matches += 1
    
    return current_points + (remaining_matches * 3)

def calculate_max_possible_points_for_others(team, group_matches, teams):
    max_points = {}
    for t in teams:
        if t == team:
            continue
        t_matches = [m for m in group_matches if m['home_team'] == t or m['away_team'] == t]
        t_points = 0
        t_remaining = 0
        for m in t_matches:
            if m['home_score'] == '' or m['away_score'] == '':
                t_remaining += 1
            else:
                is_home = m['home_team'] == t
                try:
                    if is_home:
                        if int(m['home_score']) > int(m['away_score']):
                            t_points += 3
                        elif int(m['home_score']) == int(m['away_score']):
                            t_points += 1
                    else:
                        if int(m['away_score']) > int(m['home_score']):
                            t_points += 3
                        elif int(m['away_score']) == int(m['home_score']):
                            t_points += 1
                except:
                    t_remaining += 1
        max_points[t] = t_points + (t_remaining * 3)
    return max_points

def is_team_ranked(team, group_name, matches, target_position):
    teams = GROUP_TEAMS.get(group_name, [])
    group_matches = [m for m in matches if m['group_name'] == group_name]
    
    team_matches = [m for m in group_matches if m['home_team'] == team or m['away_team'] == team]
    team_current_points = 0
    team_remaining = 0
    
    for m in team_matches:
        if m['home_score'] == '' or m['away_score'] == '':
            team_remaining += 1
        else:
            is_home = m['home_team'] == team
            try:
                hs = int(m['home_score'])
                as_ = int(m['away_score'])
                if is_home:
                    if hs > as_: team_current_points += 3
                    elif hs == as_: team_current_points += 1
                else:
                    if as_ > hs: team_current_points += 3
                    elif as_ == hs: team_current_points += 1
            except:
                team_remaining += 1
    
    team_min = team_current_points
    
    teams_that_could_be_ahead = 0
    for other in teams:
        if other == team:
            continue
        other_matches = [m for m in group_matches if m['home_team'] == other or m['away_team'] == other]
        other_current_points = 0
        other_remaining = 0
        other_unplayed_vs_team = False
        
        for m in other_matches:
            involves_team = (m['home_team'] == team or m['away_team'] == team)
            is_unplayed = m['home_score'] == '' or m['away_score'] == ''
            
            if involves_team:
                if is_unplayed:
                    other_unplayed_vs_team = True
                    other_remaining += 1
                else:
                    is_home = m['home_team'] == other
                    try:
                        hs = int(m['home_score'])
                        as_ = int(m['away_score'])
                        if is_home:
                            if hs > as_: other_current_points += 3
                            elif hs == as_: other_current_points += 1
                        else:
                            if as_ > hs: other_current_points += 3
                            elif as_ == hs: other_current_points += 1
                    except:
                        other_remaining += 1
            else:
                if is_unplayed:
                    other_remaining += 1
                else:
                    is_home = m['home_team'] == other
                    try:
                        hs = int(m['home_score'])
                        as_ = int(m['away_score'])
                        if is_home:
                            if hs > as_: other_current_points += 3
                            elif hs == as_: other_current_points += 1
                        else:
                            if as_ > hs: other_current_points += 3
                            elif as_ == hs: other_current_points += 1
                    except:
                        other_remaining += 1
        
        other_max = other_current_points + (other_remaining * 3)
        
        if other_max > team_min:
            teams_that_could_be_ahead += 1
        elif other_max == team_min:
            h2h_gd, h2h_gf = calculate_h2h_gd(team, other, group_matches)
            if h2h_gd < 0:
                teams_that_could_be_ahead += 1
            elif other_unplayed_vs_team and h2h_gd <= 0:
                teams_that_could_be_ahead += 1
    
    if target_position == 1:
        return teams_that_could_be_ahead == 0
    elif target_position == 2:
        return teams_that_could_be_ahead <= 1
    else:
        return False

def calculate_h2h_gd(team1, team2, group_matches):
    gd = 0
    gf = 0
    for m in group_matches:
        if (m['home_team'] == team1 and m['away_team'] == team2) or \
           (m['home_team'] == team2 and m['away_team'] == team1):
            if m['home_score'] != '' and m['away_score'] != '':
                try:
                    if m['home_team'] == team1:
                        gd += int(m['home_score']) - int(m['away_score'])
                        gf += int(m['home_score'])
                    else:
                        gd += int(m['away_score']) - int(m['home_score'])
                        gf += int(m['away_score'])
                except:
                    pass
    return gd, gf

def calculate_total_gd(team, group_matches):
    gd = 0
    gf = 0
    for m in group_matches:
        if m['home_team'] == team:
            if m['home_score'] != '' and m['away_score'] != '':
                try:
                    gd += int(m['home_score']) - int(m['away_score'])
                    gf += int(m['home_score'])
                except:
                    pass
        elif m['away_team'] == team:
            if m['home_score'] != '' and m['away_score'] != '':
                try:
                    gd += int(m['away_score']) - int(m['home_score'])
                    gf += int(m['away_score'])
                except:
                    pass
    return gd, gf

def is_team_ranked_for_position(group_name, matches, position):
    teams = GROUP_TEAMS.get(group_name, [])
    if not teams:
        return False
    
    group_matches = [m for m in matches if m['group_name'] == group_name]
    
    for team in teams:
        team_matches = [m for m in group_matches if m['home_team'] == team or m['away_team'] == team]
        team_current_points = 0
        team_remaining = 0
        
        for m in team_matches:
            if m['home_score'] == '' or m['away_score'] == '':
                team_remaining += 1
            else:
                is_home = m['home_team'] == team
                try:
                    hs = int(m['home_score'])
                    as_ = int(m['away_score'])
                    if is_home:
                        if hs > as_: team_current_points += 3
                        elif hs == as_: team_current_points += 1
                    else:
                        if as_ > hs: team_current_points += 3
                        elif as_ == hs: team_current_points += 1
                except:
                    team_remaining += 1
        
        team_max = team_current_points + (team_remaining * 3)
        
        teams_above = 0
        for other in teams:
            if other == team:
                continue
            other_matches = [m for m in group_matches if m['home_team'] == other or m['away_team'] == other]
            other_points = 0
            other_remaining = 0
            for m in other_matches:
                if m['home_score'] == '' or m['away_score'] == '':
                    other_remaining += 1
                else:
                    is_home = m['home_team'] == other
                    try:
                        hs = int(m['home_score'])
                        as_ = int(m['away_score'])
                        if is_home:
                            if hs > as_: other_points += 3
                            elif hs == as_: other_points += 1
                        else:
                            if as_ > hs: other_points += 3
                            elif as_ == hs: other_points += 1
                    except:
                        other_remaining += 1
            
            other_max = other_points + (other_remaining * 3)
            if other_max > team_max:
                teams_above += 1
            elif other_max == team_max:
                h2h_gd, h2h_gf = calculate_h2h_gd(team, other, group_matches)
                if h2h_gd < 0:
                    teams_above += 1
                elif h2h_gd == 0:
                    total_gd, total_gf = calculate_total_gd(team, group_matches)
                    other_total_gd, other_total_gf = calculate_total_gd(other, group_matches)
                    if total_gd < other_total_gd:
                        teams_above += 1
                    elif total_gd == other_total_gd and total_gf < other_total_gf:
                        teams_above += 1
        
        if teams_above < position:
            return True
    
    return False

def calculate_group_standings(group_name, matches):
    teams = GROUP_TEAMS.get(group_name, [])
    if not teams:
        return []

    group_matches = [m for m in matches if m['group_name'] == group_name]
    
    team_stats = []
    for team in teams:
        team_matches = [m for m in group_matches if m['home_team'] == team or m['away_team'] == team]

        win = draw = lose = gf = ga = points = yellow = red = 0

        for m in team_matches:
            is_home = m['home_team'] == team
            try:
                home_score = int(m['home_score']) if m['home_score'] and str(m['home_score']).strip() else 0
                away_score = int(m['away_score']) if m['away_score'] and str(m['away_score']).strip() else 0
            except (ValueError, TypeError):
                home_score = 0
                away_score = 0
            scored = home_score if is_home else away_score
            conceded = away_score if is_home else home_score
            my_yellow = m['home_yellow_card'] if is_home else m['away_yellow_card']
            my_red = m['home_red_card'] if is_home else m['away_red_card']

            gf += scored
            ga += conceded
            yellow += my_yellow if my_yellow else 0
            red += my_red if my_red else 0

            if m['home_score'] != '' and m['away_score'] != '':
                if scored > conceded:
                    win += 1
                    points += 3
                elif scored == conceded:
                    draw += 1
                    points += 1
                else:
                    lose += 1

        fair_play = calculate_fair_play_score(yellow, red)
        team_stats.append({
            'team': team,
            'win': win,
            'draw': draw,
            'lose': lose,
            'gf': gf,
            'ga': ga,
            'gd': gf - ga,
            'points': points,
            'yellow': yellow,
            'red': red,
            'fair_play': fair_play,
            'fifa_rank': get_fifa_ranking(team)
        })

    h2h_stats = calculate_head_to_head_stats(teams, group_matches)

    team_stats.sort(key=lambda x: (
        -x['points'],
        -(h2h_stats[x['team']]['gd']),
        -(h2h_stats[x['team']]['gf']),
        -x['gd'],
        -x['gf'],
        x['fair_play'],
        x['fifa_rank']
    ))

    return team_stats

def calculate_all_third_place_teams(matches):
    third_place_teams = []
    for group in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:
        standings = calculate_group_standings(group, matches)
        if len(standings) >= 3:
            third_team = standings[2].copy()
            third_team['group'] = group
            third_place_teams.append(third_team)

    third_place_teams.sort(key=lambda x: (
        -x['points'],
        -x['gd'],
        -x['gf'],
        x['fair_play'],
        x['fifa_rank']
    ))

    return third_place_teams[:8]

def is_team_eliminated(team, group_name, matches):
    group_matches = [m for m in matches if m['group_name'] == group_name]
    team_matches = [m for m in group_matches if m['home_team'] == team or m['away_team'] == team]
    team_remaining = sum(1 for m in team_matches if m['home_score'] == '' or m['away_score'] == '')
    if team_remaining > 0:
        return False
    return is_team_qualified(team, group_name, matches) == False and is_team_ranked_for_position(group_name, matches, 2) == False

def is_team_ranking_locked(team, group_name, matches):
    if is_team_ranked(team, group_name, matches, 1):
        return True
    if is_team_ranked(team, group_name, matches, 2):
        group_matches = [m for m in matches if m['group_name'] == group_name]
        teams = GROUP_TEAMS.get(group_name, [])
        team_matches = [m for m in group_matches if m['home_team'] == team or m['away_team'] == team]
        team_current_points = 0
        team_remaining = 0
        for m in team_matches:
            if m['home_score'] == '' or m['away_score'] == '':
                team_remaining += 1
            else:
                is_home = m['home_team'] == team
                try:
                    hs = int(m['home_score'])
                    as_ = int(m['away_score'])
                    if is_home:
                        if hs > as_: team_current_points += 3
                        elif hs == as_: team_current_points += 1
                    else:
                        if as_ > hs: team_current_points += 3
                        elif as_ == hs: team_current_points += 1
                except:
                    team_remaining += 1
        team_max = team_current_points + (team_remaining * 3)
        for other in teams:
            if other == team:
                continue
            other_matches = [m for m in group_matches if m['home_team'] == other or m['away_team'] == other]
            other_current_points = 0
            other_remaining = 0
            for m in other_matches:
                involves_team = (m['home_team'] == team or m['away_team'] == team)
                is_unplayed = m['home_score'] == '' or m['away_score'] == ''
                if involves_team:
                    if is_unplayed:
                        other_remaining += 1
                    else:
                        is_home = m['home_team'] == other
                        try:
                            hs = int(m['home_score'])
                            as_ = int(m['away_score'])
                            if is_home:
                                if hs > as_: other_current_points += 3
                                elif hs == as_: other_current_points += 1
                            else:
                                if as_ > hs: other_current_points += 3
                                elif as_ == hs: other_current_points += 1
                        except:
                            other_remaining += 1
                else:
                    if is_unplayed:
                        other_remaining += 1
                    else:
                        is_home = m['home_team'] == other
                        try:
                            hs = int(m['home_score'])
                            as_ = int(m['away_score'])
                            if is_home:
                                if hs > as_: other_current_points += 3
                                elif hs == as_: other_current_points += 1
                            else:
                                if as_ > hs: other_current_points += 3
                                elif as_ == hs: other_current_points += 1
                        except:
                            other_remaining += 1
            other_max = other_current_points + (other_remaining * 3)
            if other_max > team_max:
                return True
    if is_group_completed(group_name, matches):
        return True
    return False

def is_team_qualified(team, group_name, matches):
    group_matches = [m for m in matches if m['group_name'] == group_name]
    team_matches = [m for m in group_matches if m['home_team'] == team or m['away_team'] == team]
    
    team_played = sum(1 for m in team_matches if m['home_score'] != '' and m['away_score'] != '')
    if team_played == 0:
        return False
    
    all_played = all(m['home_score'] != '' and m['away_score'] != '' for m in team_matches)
    if not all_played:
        return is_team_ranked(team, group_name, matches, 1) or is_team_ranked(team, group_name, matches, 2)
    
    standings = calculate_group_standings(group_name, matches)
    team_idx = next((i for i, t in enumerate(standings) if t['team'] == team), None)
    
    if team_idx is not None and team_idx <= 1:
        return True
    
    if team_idx == 2:
        all_groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        all_third = []
        for g in all_groups:
            g_standings = calculate_group_standings(g, matches)
            if len(g_standings) >= 3:
                third = g_standings[2].copy()
                third['group'] = g
                all_third.append(third)
        all_third.sort(key=lambda x: (-x['points'], -x['gd'], -x['gf'], x['fair_play'], x['fifa_rank']))
        best_8 = all_third[:8]
        return any(t['team'] == team and t['group'] == group_name for t in best_8)
    
    return False

def is_group_completed(group_name, matches):
    group_matches = [m for m in matches if m['group_name'] == group_name]
    for m in group_matches:
        if m['home_score'] == '' or m['away_score'] == '':
            return False
    return True

def match_knockout_matrix(qualifier_groups, third_place_teams):
    conn = get_db_connection()
    cursor = conn.cursor()

    best_match = None
    best_score = -1

    cursor.execute('SELECT * FROM knockout_matrix')
    for row in cursor.fetchall():
        matrix_qualifiers = json.loads(row['qualifier_groups'])
        match_count = len(set(qualifier_groups) & set(matrix_qualifiers))
        if match_count > best_score:
            best_score = match_count
            best_match = row

    conn.close()

    if not best_match:
        return []

    third_places = json.loads(best_match['third_places'])
    result = []

    for i, third in enumerate(third_place_teams[:8]):
        group = third['group']
        result.append({
            'rank': i + 1,
            'team': third['team'],
            'group': group,
            'third_code': third_places[i]
        })

    return result

def update_knockout_matches(matches):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    knockout_mapping = {
        73: ('A', 2), 74: ('C', 1), 75: ('E', 1), 76: ('F', 1),
        77: ('E', 2), 78: ('I', 1), 79: ('A', 1), 80: ('L', 1),
        81: ('G', 1), 82: ('D', 1), 83: ('H', 1), 84: ('K', 2),
        85: ('B', 1), 86: ('D', 2), 87: ('J', 1), 88: ('K', 1)
    }
    
    for match_id, (group, position) in knockout_mapping.items():
        if is_team_ranked_for_position(group, matches, position):
            standings = calculate_group_standings(group, matches)
            if len(standings) >= position:
                team = standings[position - 1]['team']
                cursor.execute('UPDATE matches SET home_team = ? WHERE id = ?', (team, match_id))

    second_place_mapping = {
        73: ('B', 2), 74: ('F', 2), 76: ('C', 2), 77: ('I', 2),
        83: ('J', 2), 84: ('L', 2), 87: ('H', 2), 86: ('G', 2)
    }
    
    for match_id, (group, position) in second_place_mapping.items():
        if is_team_ranked_for_position(group, matches, position):
            standings = calculate_group_standings(group, matches)
            if len(standings) >= position:
                team = standings[position - 1]['team']
                cursor.execute('UPDATE matches SET away_team = ? WHERE id = ?', (team, match_id))

    third_place_teams = calculate_all_third_place_teams(matches)
    if third_place_teams:
        qualifier_groups = []
        for group in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:
            standings = calculate_group_standings(group, matches)
            if len(standings) >= 2 and standings[0]['points'] > 0:
                qualifier_groups.append(group)

        matched_thirds = match_knockout_matrix(qualifier_groups, third_place_teams)

        third_by_code = {}
        for t in matched_thirds:
            third_by_code[t['third_code']] = t

        third_by_rank = {t['rank']: t for t in matched_thirds}

        for match in matches:
            if match['stage'] != '1/16决赛':
                continue

            home = match['home_team']
            away = match['away_team']

            if home in ['A/B/C/D/F3', 'C/D/F/G/H3', 'C/E/F/H/I3', 'E/H/I/J/K3',
                       'A/E/H/I/J3', 'B/E/F/I/J3', 'E/F/G/I/J3', 'D/E/I/J/L3']:
                slot = home
            elif away in ['A/B/C/D/F3', 'C/D/F/G/H3', 'C/E/F/H/I3', 'E/H/I/J/K3',
                         'A/E/H/I/J3', 'B/E/F/I/J3', 'E/F/G/I/J3', 'D/E/I/J/L3']:
                slot = away
            else:
                continue

            possible_thirds = []
            for code, data in third_by_code.items():
                if slot.startswith('A') and code == '3A':
                    possible_thirds.append(data)
                elif slot.startswith('B') and code == '3B':
                    possible_thirds.append(data)
                elif slot.startswith('C') and code == '3C':
                    possible_thirds.append(data)
                elif slot.startswith('D') and code == '3D':
                    possible_thirds.append(data)
                elif slot.startswith('E') and code == '3E':
                    possible_thirds.append(data)
                elif slot.startswith('F') and code == '3F':
                    possible_thirds.append(data)
                elif slot.startswith('H') and code == '3H':
                    possible_thirds.append(data)
                elif slot.startswith('I') and code == '3I':
                    possible_thirds.append(data)
                elif slot.startswith('J') and code == '3J':
                    possible_thirds.append(data)
                elif slot.startswith('K') and code == '3K':
                    possible_thirds.append(data)
                elif slot.startswith('L') and code == '3L':
                    possible_thirds.append(data)

            if possible_thirds:
                best = min(possible_thirds, key=lambda x: x['rank'])
                team_name = best['team']
                if home in ['A/B/C/D/F3', 'C/D/F/G/H3', 'C/E/F/H/I3', 'E/H/I/J/K3',
                           'A/E/H/I/J3', 'B/E/F/I/J3', 'E/F/G/I/J3', 'D/E/I/J/L3']:
                    cursor.execute('UPDATE matches SET home_team = ? WHERE id = ?', (team_name, match['id']))
                else:
                    cursor.execute('UPDATE matches SET away_team = ? WHERE id = ?', (team_name, match['id']))

    conn.commit()
    conn.close()

def apply_knockout_winners():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM matches WHERE stage = "1/16决赛"')
    r16_matches = [dict(row) for row in cursor.fetchall()]

    bracket_mapping = {
        73: (90, 'home'), 74: (89, 'home'), 75: (90, 'away'), 76: (91, 'home'),
        77: (89, 'away'), 78: (91, 'away'), 79: (92, 'home'), 80: (92, 'away'),
        81: (94, 'home'), 82: (94, 'away'), 83: (93, 'home'), 84: (93, 'away'),
        85: (96, 'home'), 86: (95, 'home'), 87: (96, 'away'), 88: (95, 'away')
    }

    for match in r16_matches:
        if not match['home_score'] or not match['away_score']:
            continue
        try:
            h = int(match['home_score'])
            a = int(match['away_score'])
            winner = match['home_team'] if h > a else match['away_team']
            target_id, slot = bracket_mapping.get(match['id'], (None, None))
            if target_id and slot:
                if slot == 'home':
                    cursor.execute('UPDATE matches SET home_team = ? WHERE id = ?', (winner, target_id))
                else:
                    cursor.execute('UPDATE matches SET away_team = ? WHERE id = ?', (winner, target_id))
        except:
            pass

    conn.commit()
    conn.close()

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/api/matches', methods=['GET'])
def get_matches():
    conn = get_db_connection()
    cursor = conn.cursor()

    year = request.args.get('year', '2026')
    cursor.execute('''
        SELECT * FROM matches
        WHERE match_date LIKE ?
        ORDER BY match_date, match_time
    ''', (f'{year}-%',))

    matches = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify(matches)

@app.route('/api/matches/<int:match_id>', methods=['PUT'])
def update_match(match_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM matches WHERE id = ?', (match_id,))
    match = cursor.fetchone()

    if not match:
        conn.close()
        return jsonify({'error': 'Match not found'}), 404

    data = request.get_json()
    home_score = data.get('home_score', '')
    away_score = data.get('away_score', '')
    home_yellow = data.get('home_yellow_card', 0)
    home_red = data.get('home_red_card', 0)
    away_yellow = data.get('away_yellow_card', 0)
    away_red = data.get('away_red_card', 0)

    cursor.execute('''
        UPDATE matches
        SET home_score = ?, away_score = ?,
            home_yellow_card = ?, home_red_card = ?,
            away_yellow_card = ?, away_red_card = ?
        WHERE id = ?
    ''', (home_score, away_score, home_yellow, home_red, away_yellow, away_red, match_id))

    conn.commit()
    conn.close()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM matches ORDER BY match_date, match_time')
    all_matches = [dict(row) for row in cursor.fetchall()]
    conn.close()

    update_knockout_matches(all_matches)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM matches WHERE id = ?', (match_id,))
    updated_match = dict(cursor.fetchone())
    conn.close()

    group_name = updated_match.get('group_name', '')
    standings = []
    if group_name:
        group_standings = calculate_group_standings(group_name, all_matches)
        for s in group_standings:
            s['is_ranking_locked'] = is_team_ranking_locked(s['team'], group_name, all_matches)
            s['is_qualified'] = is_team_qualified(s['team'], group_name, all_matches)
            s['is_eliminated'] = is_team_eliminated(s['team'], group_name, all_matches)
        standings = group_standings

    return jsonify({
        'success': True,
        'updated_match': updated_match,
        'group_name': group_name,
        'standings': standings
    })

@app.route('/api/groups', methods=['GET'])
def get_groups():
    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    return jsonify(groups)

@app.route('/api/refresh-knockout', methods=['POST'])
def refresh_knockout():
    later_placeholders = {
        89: ('73胜者', '75胜者'),
        90: ('74胜者', '77胜者'),
        91: ('76胜者', '78胜者'),
        92: ('79胜者', '80胜者'),
        93: ('83胜者', '84胜者'),
        94: ('81胜者', '82胜者'),
        95: ('86胜者', '88胜者'),
        96: ('85胜者', '87胜者'),
        97: ('89胜者', '90胜者'),
        98: ('93胜者', '94胜者'),
        99: ('91胜者', '92胜者'),
        100: ('95胜者', '96胜者'),
        101: ('97胜者', '98胜者'),
        102: ('99胜者', '100胜者'),
        104: ('101胜者', '102胜者'),
    }
    
    conn = get_db_connection()
    cursor = conn.cursor()
    for mid, (home, away) in later_placeholders.items():
        cursor.execute('UPDATE matches SET home_team = ?, away_team = ? WHERE id = ?', (home, away, mid))
    conn.commit()
    conn.close()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM matches WHERE match_date LIKE "2026-%" ORDER BY match_date, match_time')
    all_matches = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    update_knockout_matches(all_matches)
    apply_knockout_winners()
    
    return jsonify({'success': True, 'message': '淘汰赛晋级已重算'})

@app.route('/api/standings', methods=['GET'])
def get_standings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM matches WHERE match_date LIKE "2026-%" ORDER BY match_date, match_time')
    matches = [dict(row) for row in cursor.fetchall()]
    conn.close()

    standings = {}
    for group in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:
        group_standings = calculate_group_standings(group, matches)
        for s in group_standings:
            s['is_ranking_locked'] = is_team_ranking_locked(s['team'], group, matches)
            s['is_qualified'] = is_team_qualified(s['team'], group, matches)
            s['is_eliminated'] = is_team_eliminated(s['team'], group, matches)
        standings[group] = group_standings
    
    all_groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    all_third = []
    for g in all_groups:
        if len(standings[g]) >= 3:
            third = standings[g][2].copy()
            third['group'] = g
            third['is_ranking_locked'] = standings[g][2].get('is_ranking_locked', False)
            third['is_qualified'] = standings[g][2].get('is_qualified', False)
            all_third.append(third)
    all_third.sort(key=lambda x: (-x['points'], -x['gd'], -x['gf'], x['fair_play'], x['fifa_rank']))
    best_8_third = all_third[:8]
    best_8_groups = {t['group'] for t in best_8_third}
    
    for group in all_groups:
        if len(standings[group]) >= 2:
            first_locked = standings[group][0].get('is_ranking_locked', False)
            second_locked = standings[group][1].get('is_ranking_locked', False)
            standings[group][0]['is_determined'] = first_locked
            standings[group][1]['is_determined'] = second_locked
        if len(standings[group]) >= 3:
            third_determined = standings[group][2].get('is_ranking_locked', False) and group in best_8_groups
            standings[group][2]['is_determined'] = third_determined

    return jsonify(standings)

@app.route('/api/third-place-teams', methods=['GET'])
def get_third_place_teams():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM matches WHERE match_date LIKE "2026-%" ORDER BY match_date, match_time')
    matches = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify(calculate_all_third_place_teams(matches))

@app.route('/api/reset-test-data', methods=['POST'])
def reset_test_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE matches
        SET home_score = '',
            away_score = '',
            home_yellow_card = 0,
            home_red_card = 0,
            away_yellow_card = 0,
            away_red_card = 0
    ''')
    
    knockout_teams = [
        (73, 'A2', 'B2'), (74, 'C1', 'F2'), (75, 'E1', 'A/B/C/D/F3'), (76, 'F1', 'C2'),
        (77, 'E2', 'I2'), (78, 'I1', 'C/D/F/G/H3'), (79, 'A1', 'C/E/F/H/I3'), (80, 'L1', 'E/H/I/J/K3'),
        (81, 'G1', 'A/E/H/I/J3'), (82, 'D1', 'B/E/F/I/J3'), (83, 'H1', 'J2'), (84, 'K2', 'L2'),
        (85, 'B1', 'E/F/G/I/J3'), (86, 'D2', 'G2'), (87, 'J1', 'H2'), (88, 'K1', 'D/E/I/J/L3')
    ]
    for mid, home, away in knockout_teams:
        cursor.execute('UPDATE matches SET home_team = ?, away_team = ? WHERE id = ?', (home, away, mid))
    
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': '测试数据已重置'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)