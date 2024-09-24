# Unity Proxy 
This tool will allow you to quickly start using proxies in your projects. The main task of this library is to solve problems of parsing proxies of different formats and their subsequent conversion to the required format. 

## Install
### From PYPI
`pip install unityproxy`

## Using
### Import
```python
from unityproxy import UnityProxy


unity = UnityProxy()
```
### Parse
```python
unity.from_.txt_file("proxies.txt", "http")
unity.from_.json_file("proxies.json", "http")
```

### Convert
```python
unity.to.list()
unity.to.queue()
```

### Iter
```python
proxy: unityproxy.Proxy = unity[0]

for proxy in unity:
    proxy: unityproxy.Proxy
```

### Convert proxy
Create enhancement issue to add new conver
```python
prx.to.aiohttp_line()
prx.to.httpx_dict()
prx.to.httpx_line()
prx.to.pyrogram()
prx.to.telethon()
prx.to.requests()
# etc
```
