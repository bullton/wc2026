"""
自动推演脚本 - 逐场填充比赛并检查积分榜和对阵
"""
import sqlite3
import random
import urllib.request
import json

DB_PATH = 'worldcup.db'
API_BASE = 'http://localhost:5000/api'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def generate_score():
    home = random.randint(0, 4)
    away = random.randint(0, 4)
    if abs(home - away) > 3:
        return generate_score()
    return home, away

def generate_penalty_score():
    """生成点球大战比分 - 5轮内必分出胜负"""
    for i in range(5):
        h = random.randint(0, 5)
        a = random.randint(0, 5)
        if h != a:
            return h, a
    # 如果5轮平了，继续直到分出胜负
    while True:
        h = random.randint(0, 1)
        a = random.randint(0, 1)
        if h != a:
            return h, a

def get_all_matches():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM matches WHERE match_date LIKE "2026-%" ORDER BY match_date, match_time')
    matches = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return matches

def get_unplayed_matches():
    matches = get_all_matches()
    return [m for m in matches if m['home_score'] == '' or m['home_score'] is None]

def fill_match_api(match_id):
    """通过API填充一场比赛"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM matches WHERE id = ?', (match_id,))
    match = dict(cursor.fetchone())
    conn.close()
    
    if match['home_score'] != '' and match['home_score'] is not None:
        return False
    
    home_score, away_score = generate_score()
    home_yellow = random.randint(0, 3)
    home_red = random.randint(0, 1) if random.random() < 0.1 else 0
    away_yellow = random.randint(0, 3)
    away_red = random.randint(0, 1) if random.random() < 0.1 else 0
    
    home_penalty = None
    away_penalty = None
    
    # 淘汰赛平局时加点球
    if match['group_name'] == '' and home_score == away_score:
        home_penalty, away_penalty = generate_penalty_score()
    
    conn = get_db()
    cursor = conn.cursor()
    if home_penalty is not None:
        cursor.execute('''
            UPDATE matches
            SET home_score = ?, away_score = ?,
                home_yellow_card = ?, home_red_card = ?,
                away_yellow_card = ?, away_red_card = ?,
                home_penalty_score = ?, away_penalty_score = ?
            WHERE id = ?
        ''', (home_score, away_score, home_yellow, home_red, away_yellow, away_red, home_penalty, away_penalty, match_id))
    else:
        cursor.execute('''
            UPDATE matches
            SET home_score = ?, away_score = ?,
                home_yellow_card = ?, home_red_card = ?,
                away_yellow_card = ?, away_red_card = ?
            WHERE id = ?
        ''', (home_score, away_score, home_yellow, home_red, away_yellow, away_red, match_id))
    conn.commit()
    conn.close()
    
    return (home_score, away_score, home_penalty, away_penalty)

def refresh_knockout_api():
    """调用刷新淘汰赛接口"""
    try:
        req = urllib.request.Request(f'{API_BASE}/refresh-knockout', method='POST')
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"    refresh-knockout failed: {e}")
        return None

def get_group_standings(group):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM matches 
        WHERE group_name = ? AND match_date LIKE "2026-%"
        ORDER BY match_date, match_time
    ''', (group,))
    matches = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    teams = {}
    for m in matches:
        home = m['home_team']
        away = m['away_team']
        if home not in teams:
            teams[home] = {'team': home, 'played': 0, 'won': 0, 'drawn': 0, 'lost': 0, 'gf': 0, 'ga': 0, 'gd': 0, 'points': 0}
        if away not in teams:
            teams[away] = {'team': away, 'played': 0, 'won': 0, 'drawn': 0, 'lost': 0, 'gf': 0, 'ga': 0, 'gd': 0, 'points': 0}
        
        if m['home_score'] == '' or m['home_score'] is None:
            continue
        
        hs = int(m['home_score'])
        as_ = int(m['away_score'])
        teams[home]['played'] += 1
        teams[away]['played'] += 1
        teams[home]['gf'] += hs
        teams[home]['ga'] += as_
        teams[away]['gf'] += as_
        teams[away]['ga'] += hs
        
        if hs > as_:
            teams[home]['won'] += 1
            teams[home]['points'] += 3
            teams[away]['lost'] += 1
        elif as_ > hs:
            teams[away]['won'] += 1
            teams[away]['points'] += 3
            teams[home]['lost'] += 1
        else:
            teams[home]['drawn'] += 1
            teams[home]['points'] += 1
            teams[away]['drawn'] += 1
            teams[away]['points'] += 1
    
    for t in teams.values():
        t['gd'] = t['gf'] - t['ga']
    
    standings = sorted(teams.values(), key=lambda x: (-x['points'], -x['gd'], -x['gf'], x['team']))
    return standings

def get_knockout_status():
    """获取淘汰赛当前状态"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, home_team, away_team, home_score, away_score FROM matches WHERE group_name = "" ORDER BY id')
    ko = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return ko

def get_champion():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM matches WHERE id = 104')
    final = dict(cursor.fetchone())
    conn.close()
    
    if final['home_score'] == '' or final['home_score'] is None:
        return None
    
    hs = int(final['home_score'])
    as_ = int(final['away_score'])
    
    if hs > as_:
        return final['home_team']
    elif as_ > hs:
        return final['away_team']
    else:
        hp = final.get('home_penalty_score')
        ap = final.get('away_penalty_score')
        if hp and ap and hp != '' and ap != '':
            if int(hp) > int(ap):
                return final['home_team']
            else:
                return final['away_team']
    return None

def print_standings_summary():
    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    for g in groups:
        standings = get_group_standings(g)
        top = standings[0] if standings else None
        second = standings[1] if len(standings) > 1 else None
        if top:
            print(f"  {g}: 1.{top['team']}({top['points']}分) 2.{second['team'] if second else '?'}({second['points'] if second else 0}分)")

def print_knockout_summary():
    ko = get_knockout_status()
    r16 = [m for m in ko if 73 <= m['id'] <= 88]
    r8 = [m for m in ko if 89 <= m['id'] <= 96]
    r4 = [m for m in ko if 97 <= m['id'] <= 100]
    sf = [m for m in ko if m['id'] in [101, 102]]
    final = [m for m in ko if m['id'] in [103, 104]]
    
    r16_done = len([m for m in r16 if m['home_score'] != ''])
    r8_done = len([m for m in r8 if m['home_score'] != ''])
    r4_done = len([m for m in r4 if m['home_score'] != ''])
    sf_done = len([m for m in sf if m['home_score'] != ''])
    final_done = len([m for m in final if m['home_score'] != ''])
    
    print(f"\n  1/16: {r16_done}/16 | 1/8: {r8_done}/8 | 1/4: {r4_done}/4 | 半决赛: {sf_done}/2 | 决赛: {final_done}/1")

def run():
    print("=" * 60)
    print("  世界冠军推演开始")
    print("=" * 60)
    
    # 先重置数据
    print("\n[重置数据...]")
    try:
        req = urllib.request.Request('http://localhost:5000/api/reset-test-data', method='POST')
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"  重置结果: {json.loads(resp.read().decode('utf-8'))['message']}")
    except Exception as e:
        print(f"  重置失败: {e}")
        return
    
    step = 0
    while True:
        unplayed = get_unplayed_matches()
        if not unplayed:
            print("\n没有未完成的比赛!")
            break
        
        next_match = unplayed[0]
        step += 1
        
        print(f"\n[{step}] {next_match['home_team']} vs {next_match['away_team']}")
        print(f"    {next_match['stage']} | {next_match['match_date']} {next_match['match_time']}")
        
        result = fill_match_api(next_match['id'])
        if result:
            home_score, away_score, home_penalty, away_penalty = result
            if home_penalty is not None:
                print(f"    比分: {home_score} - {away_score} (点球 {home_penalty} - {away_penalty})")
            else:
                print(f"    比分: {home_score} - {away_score}")
        
        # 每次填充后都刷新淘汰赛对阵
        refresh_knockout_api()
        
        # 检查冠军
        champion = get_champion()
        if champion:
            print(f"\n*** 冠军产生: {champion} ***")
            print_knockout_summary()
            break
        
        # 每10步打印一次状态
        if step % 10 == 0:
            print_standings_summary()
            print_knockout_summary()
        
        if step > 150:
            print("达到最大步数")
            break
    
    print("\n" + "=" * 60)
    print("  最终状态")
    print("=" * 60)
    print_standings_summary()
    print_knockout_summary()
    
    ko = get_knockout_status()
    print("\n淘汰赛对阵:")
    for m in ko:
        score = f"{m['home_score']}-{m['away_score']}" if m['home_score'] != '' else "vs"
        penalty = ""
        if m['home_score'] != '' and m['away_score'] != '' and m['home_score'] == m['away_score']:
            hp = m.get('home_penalty_score')
            ap = m.get('away_penalty_score')
            if hp and hp != '' and ap and ap != '':
                penalty = f" (pk {hp}-{ap})"
        print(f"  {m['id']:3d}. {m['home_team']} {score}{penalty} {m['away_team']}")

if __name__ == '__main__':
    run()
