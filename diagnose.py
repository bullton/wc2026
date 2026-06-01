import sqlite3
import json

print("=== 数据库诊断 ===\n")

conn = sqlite3.connect('worldcup.db')
cursor = conn.cursor()

# 检查比赛总数
cursor.execute('SELECT COUNT(*) FROM matches')
total_matches = cursor.fetchone()[0]
print(f"✓ 总比赛数: {total_matches}")

# 检查小组赛数量
cursor.execute('SELECT COUNT(*) FROM matches WHERE stage = "小组赛"')
group_matches = cursor.fetchone()[0]
print(f"✓ 小组赛数量: {group_matches}")

# 检查有比分的比赛
cursor.execute('SELECT COUNT(*) FROM matches WHERE home_score != "" AND away_score != ""')
scored_matches = cursor.fetchone()[0]
print(f"✓ 已有比分的比赛: {scored_matches}")

# 检查各组比赛数
print("\n各组比赛数:")
for group in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:
    cursor.execute('SELECT COUNT(*) FROM matches WHERE group_name = ?', (group,))
    count = cursor.fetchone()[0]
    print(f"  第{group}组: {count}场")

# 显示前3场比赛样本
print("\n前3场比赛样本:")
cursor.execute('''
    SELECT match_date, match_time, group_name, home_team, away_team,
           home_score, away_score, stage
    FROM matches
    LIMIT 3
''')
rows = cursor.fetchall()
for row in rows:
    print(f"  {row[0]} {row[1]} | {row[2]}组 | {row[3]} vs {row[4]} | 比分: {row[5]}-{row[6]} | {row[7]}")

conn.close()

print("\n=== 前端数据结构检查 ===")
print("\n前端预期的球队配置:")
teams = {
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

for group, team_list in teams.items():
    print(f"第{group}组: {', '.join(team_list)}")

print("\n诊断完成!")
