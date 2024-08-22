from requests_base_url import HTTP, http


def test_http():
    resp = http.get('http://httpbin.org/get?a=1&b=2')
    print(resp.text)


def test_http_with_base_url():
    http = HTTP(base_url='http://httpbin.org')
    resp = http.get('/get?a=1&b=2')
    print(resp.text)
    resp = http.post('/post', data={'a': 1, 'b': 2})
    print(resp.text)


def test_http_with_default_headers():
    http = HTTP(base_url='http://httpbin.org', headers={'token': 'xxx'})
    resp = http.get('/get?a=1&b=2')
    print(resp.text)
