---
title: 修改`宝塔面板`部分功能
date: 2025-05-29 16:50:44
tags:
---

# 一、修改获取登录`IP`的功能

修改`/www/server/panel/class/public.py`中`GetClientIp()`函数：

```python
def GetClientIp():
    from flask import request
    headers = ["X-Real-IP", "X-Forwarded-For", "Proxy-Client-IP", "WL-Proxy-Client-IP", "HTTP_CLIENT_IP", "HTTP_X_FORWARDED_FOR"]
    ipaddr = None
    for header in headers:
        ipaddr = request.headers.get(header, None)
        if ipaddr is not None:
            break
    if ipaddr is None:
        ipaddr = request.remote_addr.replace('::ffff:', '')
    if not check_ip(ipaddr):
        ipaddr = '未知IP地址'
    return ipaddr
```

修改之后，使用`Nginx`反向代理**宝塔面板**链接时，可以正确获取到登录`IP`。

{% folding green::这里是反向代理的配置 %}

```nginx
location ^~ / {
	proxy_pass http://127.0.0.1:12321;
	proxy_set_header Host $http_host;
	proxy_set_header X-Real-IP $remote_addr;
	proxy_set_header X-Real-Port $remote_port;
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	proxy_set_header X-Forwarded-Proto $scheme;
	proxy_set_header X-Forwarded-Host $host;
	proxy_set_header X-Forwarded-Port $server_port;
	proxy_set_header REMOTE-HOST $remote_addr;
	proxy_ssl_server_name on;
	proxy_connect_timeout 60s;
	proxy_send_timeout 600s;
	proxy_read_timeout 600s;
	proxy_http_version 1.1;
	proxy_set_header Upgrade $http_upgrade;
	proxy_set_header Connection $connection_upgrade;
}
```

{% endfolding %}



# 二、修改DNS和SSL中Clouflare的身份验证方式

1、修改文件`/www/server/panel/class/panelDnsapi.py`中`CloudFlareDns`类的私有方法`_get_auth_headers`为：

```python
    def _get_auth_headers(self) -> dict:
        if (self.CLOUDFLARE_EMAIL is None or not self.CLOUDFLARE_EMAIL) and isinstance(self.CLOUDFLARE_API_KEY, str):
            return {"Authorization": "Bearer " + self.CLOUDFLARE_API_KEY}
        else:
            return {"X-Auth-Email": self.CLOUDFLARE_EMAIL, "X-Auth-Key": self.CLOUDFLARE_API_KEY}
```

修改后，在配置`Cloudflare`的`DNS`接口时，`E-Mail`输入空格 ` `，`API Key`输入`API Token`，这样可以避免使用 `Global API Key`。

------

2、修改文件`/www/server/panel/class/sslModel/cloudflareModel.py`中`main`类的私有方法`__init_data`为：

```python
def __init_data(self, data):
        self.CLOUDFLARE_EMAIL = data['E-Mail'].strip()
        self.CLOUDFLARE_API_KEY = data['API Key']
        self.CLOUDFLARE_API_BASE_URL = 'https://api.cloudflare.com/client/v4/'
        self.HTTP_TIMEOUT = 65  # seconds
        
        if (self.CLOUDFLARE_EMAIL is None or not self.CLOUDFLARE_EMAIL) and isinstance(self.CLOUDFLARE_API_KEY, str):
            self.headers = {"Authorization": f"Bearer {self.CLOUDFLARE_API_KEY}"}
        else:
            self.headers = {"X-Auth-Email": self.CLOUDFLARE_EMAIL, "X-Auth-Key": self.CLOUDFLARE_API_KEY}
```

修改后，在用`Cloudflare`的`DNS`申请证书时，可以使用`API Token`的方式申请。

