# FIFA World Cup 2026 - Schedule Calendar

美加墨世界杯赛程日历应用

## 功能特性

- **赛程日历** - 按日期展示完整赛程
- **积分榜** - 12个小组的实时积分排名
- **淘汰赛对阵图** - 使用 jquery-bracket 展示的树状对阵结构
- **出线判断** - 根据 2026 规则（8个最佳第3名出线）计算排名和资格
- **实时占位符** - 未确定排名的队伍显示 A1、B2 等原始占位符

## 技术栈

- 前端：HTML5 + CSS3 + JavaScript + jQuery + jQuery Bracket
- 后端：Python + Flask
- 数据库：SQLite

## 安装运行

```bash
pip install -r requirements.txt
python app.py
```

访问 http://localhost:5000

## 部署

```bash
# 指定端口（默认5000）
PORT=8080 python app.py
```

## 项目结构

```
wc2026/
├── index.html          # 前端页面
├── app.py             # Flask 后端 API
├── database.py        # 数据库初始化
├── worldcup.db        # SQLite 数据库
└── requirements.txt   # Python 依赖
```

## 2026 出线规则

- 每组前2名直接晋级16强
- 8个成绩最好的第3名球队晋级16强
- 排名判断优先级：积分 → 净胜球 → 进球数 → 公平竞赛分 → FIFA排名
- 积分榜标记：绿色背景 = 排名已锁定，Q = 已晋级

## 数据来源

2026 FIFA World Cup 美加墨世界杯完整赛程数据