# BiliTester
批量测试B站直播推流（live-push.bilivideo.com）节点延迟，找出最低延迟的节点。

修改自akamTester（https://github.com/miyouzi/akamTester）

在之后在Hosts中追加：
```
最低延迟的IP live-push.bilivideo.com
```
或者直接在OBS内将“服务器”替换为
```
rtmp://你抓取的低延迟IP/live-bvc/
```

:warning: 在Win7上需要使用管理员权限运行! :warning:


## 源码运行

### 1.安装依赖:

For Windows cmd:
```
pip3 install requests beautifulsoup4 lxml termcolor pythonping dnspython
```
For Linux (tested on Arch Linux):
```
sudo pip install -r requirements.txt
```

### 2.获取额外的CDN IP
前往以下网址
```
https://ping.chinaz.com/live-push.bilivideo.com
```
等待所有节点解析完毕，复制所有获取到的IP并且覆盖保存到根目录的```ip_list.txt```文本文档中

![17FE5351-EEC2-475A-A63F-8764F6A95F75](https://user-images.githubusercontent.com/47912037/154753260-3b88862b-94dc-4c8b-8490-966fd90bb595.png)

<img width="1072" alt="EBCE95E5-9929-4276-AC05-FF0CED26ED0F" src="https://user-images.githubusercontent.com/47912037/154753323-4c0f823d-fdf0-49ce-8e81-96192d515629.png">



### 3.执行 ```bilitester.py```
```
python3 bilitester.py
```


## 关于轮子

### GlobalDNS
```GlobalDNS``` 是个对域名进行全球解析的类, 使用 www.whatsmydns.net 的 API 进行解析，额外包含本地、谷歌、腾讯、阿里 DNS 的解析结果。

**导入**
```
from GlobalDNS import GlobalDNS
```

**使用**
```
akam = GlobalDNS('upos-hz-mirrorakam.akamaized.net')
ip_list = akam.get_ip_list()  # 取得全球解析结果, 返回一个 set
akam.renew()  # 重新解析
ip_list = akam.get_ip_list()  # 将返回最近一次全球解析的结果
```

### ColorPrinter
```ColorPrinter``` 染色输出工具, 可输出红绿及默认颜色(一般终端为白色), 可跨平台, 包括pyCharm中的运行窗口

**导入**
```
from ColorPrinter import color_print
```

**使用**
```
color_print('Hello World')  # 默认输出颜色
color_print('Hello World', status=1)  # 输出红色
color_print('Hello World', status=2)  # 输出绿色
```
