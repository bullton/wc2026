"""
AI推演脚本 - 使用MiniMax AI预测比赛结果
小组赛按轮提交预测，淘汰赛按阶段提交预测
"""
import sqlite3
import json
import time
import random
import base64
import urllib.request
import urllib.error

DB_PATH = 'worldcup.db'
API_BASE = 'http://localhost:5000/api'

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
    '加纳': 56, '冰岛': 57, '新西兰': 58, '萨尔瓦多': 60,
    '波斯尼亚和黑塞哥维那': 61, '黑山': 62, '北马其顿': 63, '菲律宾': 64,
    '越南': 65, '伊拉克': 66, '卡塔尔': 67, '民主刚果': 68, '巴拿马': 69,
    '斯洛伐克': 70, '中国': 72, '约旦': 73, '保加利亚': 74,
    '库拉索': 75, '佛得角': 76, '斯洛文尼亚': 77, '阿联酋': 78, '乌兹别克斯坦': 79,
    '哈萨克斯坦': 80, '尼泊尔': 81, '黎巴嫩': 82, '白俄罗斯': 83, '洪都拉斯': 84
}

def get_ai_api_key():
    encoded_key = "c2stY3AtTVhBbDJJdGY2ZHpBajZjSVo0aDZ5akIyZTg1WHZFcldtbWFZSENuOHl0alc1R3JfbDZ5U2ZVU3g0VzJkWEpla3hMcWkzYm5XNWxLMXhuSjR6ZWk2RXQ5a3BQZ05xZE5qR3k2RUg3dFRyVm52ak4tS1cyWXZRQjg="
    return base64.b64decode(encoded_key).decode('utf-8')

def get_prediction_from_ai(home_team, away_team):
    api_key = get_ai_api_key()
    url = "https://api.minimaxi.com/v1/chat/completions"

    home_rank = FIFA_RANKINGS.get(home_team, 100)
    away_rank = FIFA_RANKINGS.get(away_team, 100)

    prompt = f"""作为足球分析师，预测以下比赛的比分：

主队：{home_team} (FIFA排名: {home_rank})
客队：{away_team} (FIFA排名: {away_rank})

请根据：
1. 两队的FIFA排名差距
2. 近期表现和历史战绩
3. 球队状态和人员情况

给出比分预测。预测需要包括：
- 预测比分（如：2-1）
- 预测理由（2-3句话）

请以JSON格式回复，格式如下：
{{"prediction": "2-1", "reason": "..."}}
只返回JSON，不要其他内容。"""

    data = {
        "model": "MiniMax-M3",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result['choices'][0]['message']['content']
            import re
            json_match = re.search(r'\{[^{}]*\}', content)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(content)
    except Exception as e:
        print(f"      AI预测失败: {e}")
        return {"prediction": None, "reason": str(e)}

def parse_score(prediction):
    if not prediction:
        return None, None
    try:
        parts = prediction.split('-')
        if len(parts) == 2:
            home = int(parts[0].strip())
            away = int(parts[1].strip())
            return home, away
    except:
        pass
    return None, None

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

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

def fill_match_api(match_id, home_score, away_score, home_penalty=None, away_penalty=None):
    conn = get_db()
    cursor = conn.cursor()

    home_yellow = random.randint(0, 3)
    home_red = random.randint(0, 1) if random.random() < 0.1 else 0
    away_yellow = random.randint(0, 3)
    away_red = random.randint(0, 1) if random.random() < 0.1 else 0

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

def refresh_knockout_api():
    try:
        req = urllib.request.Request(f'{API_BASE}/refresh-knockout', method='POST')
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"    refresh-knockout failed: {e}")
        return None

def get_group_matches_by_round():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM matches
        WHERE group_name != "" AND group_name IS NOT NULL AND match_date LIKE "2026-%"
        ORDER BY match_date, match_time
    ''')
    matches = [dict(row) for row in cursor.fetchall()]
    conn.close()

    rounds = {}
    for m in matches:
        date = m['match_date']
        if date not in rounds:
            rounds[date] = []
        rounds[date].append(m)

    return rounds

def get_knockout_matches_by_stage():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM matches
        WHERE (group_name = "" OR group_name IS NULL) AND match_date LIKE "2026-%"
        ORDER BY id
    ''')
    matches = [dict(row) for row in cursor.fetchall()]
    conn.close()

    stages = {
        '1/16决赛': [],
        '1/8决赛': [],
        '1/4决赛': [],
        '半决赛': [],
        '决赛': [],
        '三四名决赛': []
    }

    for m in matches:
        stage = m['stage']
        if stage in stages:
            stages[stage].append(m)

    return stages

def get_champion():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM matches WHERE id = 104')
    final = dict(cursor.fetchone())
    conn.close()

    if final['home_score'] == '' or final['home_score'] is None:
        return None, None

    hs = int(final['home_score'])
    as_ = int(final['away_score'])

    winner = None
    loser = None

    if hs > as_:
        winner = final['home_team']
        loser = final['away_team']
    elif as_ > hs:
        winner = final['away_team']
        loser = final['home_team']
    else:
        hp = final.get('home_penalty_score')
        ap = final.get('away_penalty_score')
        if hp and ap and hp != '' and ap != '':
            if int(hp) > int(ap):
                winner = final['home_team']
                loser = final['away_team']
            else:
                winner = final['away_team']
                loser = final['home_team']

    return winner, loser

def get_third_place():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM matches WHERE id = 103')
    third = dict(cursor.fetchone())
    conn.close()

    if third['home_score'] == '' or third['home_score'] is None:
        return None

    hs = int(third['home_score'])
    as_ = int(third['away_score'])

    if hs > as_:
        return third['home_team']
    elif as_ > hs:
        return third['away_team']
    else:
        hp = third.get('home_penalty_score')
        ap = third.get('away_penalty_score')
        if hp and ap and hp != '' and ap != '':
            if int(hp) > int(ap):
                return third['home_team']
            else:
                return third['away_team']
    return None

def predict_and_fill_match(match):
    home_team = match['home_team']
    away_team = match['away_team']
    stage = match['stage']

    print(f"      预测: {home_team} vs {away_team}")

    result = get_prediction_from_ai(home_team, away_team)
    prediction = result.get('prediction', '')
    reason = result.get('reason', '')

    if prediction:
        print(f"      AI预测: {prediction}")
        home_score, away_score = parse_score(prediction)

        if home_score is None:
            print(f"      解析预测失败，使用随机分数")
            home_score = random.randint(0, 3)
            away_score = random.randint(0, 3)
    else:
        print(f"      AI预测失败，使用随机分数")
        home_score = random.randint(0, 3)
        away_score = random.randint(0, 3)

    home_penalty = None
    away_penalty = None

    is_knockout = not match['group_name'] or match['group_name'] == ''
    if is_knockout and home_score == away_score:
        print(f"      平局，进行点球大战...")
        for i in range(5):
            h = random.randint(0, 5)
            a = random.randint(0, 5)
            if h != a:
                home_penalty = h
                away_penalty = a
                break
        if home_penalty is None:
            while True:
                h = random.randint(0, 1)
                a = random.randint(0, 1)
                if h != a:
                    home_penalty = h
                    away_penalty = a
                    break

    fill_match_api(match['id'], home_score, away_score, home_penalty, away_penalty)

    penalty_str = f" (点球 {home_penalty}-{away_penalty})" if home_penalty else ""
    print(f"      结果: {home_score} - {away_score}{penalty_str}")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO match_predictions (match_id, prediction, reason)
        VALUES (?, ?, ?)
    ''', (match['id'], prediction, reason))
    conn.commit()
    conn.close()

    return home_score, away_score, home_penalty, away_penalty

def simulate_group_stage():
    print("\n" + "=" * 60)
    print("  小组赛阶段 - 按轮预测")
    print("=" * 60)

    rounds = get_group_matches_by_round()
    round_names = sorted(rounds.keys())

    for round_date in round_names:
        matches = rounds[round_date]
        unplayed = [m for m in matches if m['home_score'] == '' or m['home_score'] is None]

        if not unplayed:
            print(f"\n[轮次 {round_date}] 所有比赛已完成")
            continue

        print(f"\n{'='*50}")
        print(f"  第 {round_date} 轮")
        print(f"{'='*50}")

        for match in unplayed:
            print(f"\n  {match['home_team']} vs {match['away_team']}")
            print(f"  {match['stage']} | {match['group_name']}组")
            predict_and_fill_match(match)
            time.sleep(1)

        print(f"\n  >> 第 {round_date} 轮完成 <<")

    print("\n小组赛全部完成!")

def simulate_knockout_stage():
    print("\n" + "=" * 60)
    print("  淘汰赛阶段 - 按阶段预测")
    print("=" * 60)

    stages = get_knockout_matches_by_stage()
    stage_order = ['1/16决赛', '1/8决赛', '1/4决赛', '半决赛', '决赛', '三四名决赛']

    for stage_name in stage_order:
        matches = stages.get(stage_name, [])
        if not matches:
            continue

        unplayed = [m for m in matches if m['home_score'] == '' or m['home_score'] is None]

        if not unplayed:
            print(f"\n[{stage_name}] 已完成")
            continue

        print(f"\n{'='*50}")
        print(f"  {stage_name}")
        print(f"{'='*50}")

        for match in unplayed:
            print(f"\n  {match['home_team']} vs {match['away_team']}")
            predict_and_fill_match(match)
            time.sleep(1)

        refresh_knockout_api()
        print(f"\n  >> {stage_name} 完成 <<")

    print("\n淘汰赛全部完成!")

def run():
    print("=" * 60)
    print("  AI世界冠军推演开始")
    print("  使用MiniMax-M3进行比分预测")
    print("=" * 60)

    print("\n[重置数据...]")
    try:
        req = urllib.request.Request('http://localhost:5000/api/reset-test-data', method='POST')
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            print(f"  重置结果: {result.get('message', 'OK')}")
    except Exception as e:
        print(f"  重置失败: {e}")
        return

    simulate_group_stage()

    simulate_knockout_stage()

    champion, runner_up = get_champion()
    third_place = get_third_place()

    print("\n" + "=" * 60)
    print("  推演结果")
    print("=" * 60)

    if champion:
        print(f"\n  🥇 冠军: {champion}")
    if runner_up:
        print(f"  🥈 亚军: {runner_up}")
    if third_place:
        print(f"  🥉 季军: {third_place}")

    if not champion:
        print("\n  决赛尚未完成!")

    print("\n推演完成!")

if __name__ == '__main__':
    run()