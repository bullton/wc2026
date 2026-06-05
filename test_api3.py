import urllib.request
import json
import base64
import sys
sys.stdout.reconfigure(encoding='utf-8')

api_key = base64.b64decode('c2stY3AtTVhBbDJJdGY2ZHpBajZjSVo0aDZ5akIyZTg1WHZFcldtbWFZSENuOHl0alc1R3JfbDZ5U2ZVU3g0VzJkWEpla3hMcWkzYm5XNWxLMXhuSjR6ZWk2RXQ5a3BQZ05xZE5qR3k2RUg3dFRyVm52ak4tS1cyWXZRQjg=').decode('utf-8')

url = "https://api.minimaxi.com/v1/chat/completions"
prompt = """作为足球分析师，预测以下比赛的比分：

主队：墨西哥 (FIFA排名: 13)
客队：南非 (FIFA排名: 54)

请根据：
1. 两队的FIFA排名差距
2. 近期表现和历史战绩
3. 球队状态和人员情况

给出比分预测。预测需要包括：
- 预测比分（如：2-1）
- 预测理由（2-3句话）

请以JSON格式回复，格式如下：
{"prediction": "2-1", "reason": "..."}
只返回JSON，不要其他内容。"""

data = {
    "model": "MiniMax-M3",
    "messages": [{"role": "user", "content": prompt}]
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
try:
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        content = result['choices'][0]['message']['content']
        print('AI Response:', content)
        parsed = json.loads(content)
        print('Parsed:', parsed)
except Exception as e:
    print('Error:', e)
    if hasattr(e, 'read'):
        err_body = e.read().decode('utf-8')
        print('Response body:', err_body)