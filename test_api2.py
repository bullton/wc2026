import urllib.request
import json
import base64

# Use the original key from user message
original_key = 'sk-cp-MXAl2Itf6dzAj6cIZ4h6yjB2e85XvErWmmaYHCn8ytjW5Gr_l6ySfUSx4W2dXJekxLqi3bnW5lK1xnJ4zei6Et9kpPgNqdNjGy6EH7tTrVnvjN-KW2YvQB8'

url = 'https://api.minimaxi.com/v1/chat/completions'
data = {
    'model': 'MiniMax-M3',
    'messages': [{'role': 'user', 'content': 'Hello'}]
}
headers = {'Authorization': f'Bearer {original_key}', 'Content-Type': 'application/json'}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
try:
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        print('Success:', result)
except Exception as e:
    print('Error:', e)
    if hasattr(e, 'read'):
        err_body = e.read().decode('utf-8')
        print('Response body:', err_body)