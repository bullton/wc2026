# FIFA World Cup 2026 - Schedule Calendar

美加墨世界杯赛程日历应用

## 功能特性

- **赛程日历** - 按日期展示完整赛程
- **积分榜** - 12个小组的实时积分排名
- **淘汰赛对阵图** - 使用 jquery-bracket 展示的树状对阵结构

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

## 项目结构

```
wc2026/
├── index.html          # 前端页面
├── app.py             # Flask 后端 API
├── database.py        # 数据库初始化
├── worldcup.db        # SQLite 数据库
└── requirements.txt   # Python 依赖
```

## 数据来源

2026 FIFA World Cup 美加墨世界杯完整赛程数据