import urllib.request
import json
import base64

encoded_key = 'c2stY3AtTVhBbDJJdGY2ZHpBejZjSVo0aDZ5akIyZTg1WHZFcldtbWE1SENuOHl0aldVN3JfbHlTZlVTeDRXMmRYSWVrTGxxM2JuVzVsS3h4SjZ6aTZFdDlrcFBnTnFkTmhHczZFSHc3dFJyVm52ak4tS1cyWXZRQjg='
api_key = base64.b64decode(encoded_key).decode('utf-8')

url = 'https://api.minimaxi.com/v1/chat/completions'
data = {
    'model': 'MiniMax-M3',
    'messages': [{'role': 'user', 'content': 'Hello, respond with JSON: test'}]
}
headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
try:
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        print('Success:', result)
except Exception as e:
    print('Error type:', type(e))
    print('Error:', e)
    if hasattr(e, 'read'):
        err_body = e.read().decode('utf-8')
        print('Response body:', err_body)