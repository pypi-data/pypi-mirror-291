# requests-base-url

![Languate - Python](https://img.shields.io/badge/language-python-blue.svg)
![PyPI - License](https://img.shields.io/pypi/l/requests-base-url)
![PyPI](https://img.shields.io/pypi/v/requests-base-url)
![PyPI - Downloads](https://img.shields.io/pypi/dm/requests-base-url)

Http client with base_url base on requests

## Install
```
pip install requests-base-url
```

## Simple Use

```python
from requests_base_url import http

resp = http.get('https://httpbin.org/get?a=1&b=2')
print(resp)
```

Config base_url 

```python
from requests_base_url import HTTP

http = HTTP(basse_url='https://httpbin.org')
resp = http.get('/get?a=1&b=2')
print(resp)

resp = http.post('/post', data=dict(a=1, b=2))
print(resp)
```


Config default Headers, Params or Proxies
```python
from requests_base_url import HTTP

http = HTTP(basse_url='https://httpbin.org', headers={"token": "xxx"})
resp = http.get('/get?a=1&b=2')
print(resp)
```
