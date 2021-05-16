```python
# json格式化

def json_format(data):
    data = data.replace("'", '"')

    data = json.loads(data)

    return json.dumps(data, indent=4, ensure_ascii=False, separators=(',', ': ')) 
```