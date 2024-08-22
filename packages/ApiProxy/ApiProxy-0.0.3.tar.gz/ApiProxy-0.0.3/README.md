# 快捷使用
## 安装库
- pip install ApiProxy

## 编译库
- python ./setup.py sdist bdist_wheel 
- pip install .\ApiProxy-1.0-py3-none-any.whl

## 上传库
- twine upload dist/*

## 卸载库
- pip uninstall ApiProxy

## 场景1-设置dp代理

```
from DrissionPage import ChromiumPage,ChromiumOptions

from ApiProxy import Proxy

a=Proxy(8993,8996)

data=a.setdynamicProxy("socks://127.0.0.1:10808")

proxyurl=data["url"]

print("proxyurl:",proxyurl)

co=ChromiumOptions()

co.set_proxy(proxyurl)

page=ChromiumPage(addr_or_opts=co)

page.get("https://www.baidu.com")

input("等待输入")
```

## 场景2-使用dp动态代理切换

```
from DrissionPage import ChromiumPage,ChromiumOptions

from ApiProxy import Proxy

a=Proxy(8993,8996)

data=a.setdynamicProxy("socks://127.0.0.1:10808")

proxyurl=data["url"]

print("proxyurl:",proxyurl)

co=ChromiumOptions()

co.set_proxy(proxyurl)

page=ChromiumPage(addr_or_opts=co)

page.get("https://www.baidu.com")

page.ele("#kw").input("测试")

\# 再次切换代理

a.setdynamicProxy("http://36.27.90.34:40005")

page.ele("#su").click()

input("等待输入")
```

