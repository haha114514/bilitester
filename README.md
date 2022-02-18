# BiliTester
## 修改自akamTester（https://github.com/miyouzi/akamTester）

批量测试B站直播推流（live-push.bilivideo.com）节点延迟，找出最低延迟的节点。

在之后在Hosts中追加：
```
最低延迟的IP live-push.bilivideo.com
```
或者直接在OBS内将“服务器”替换为
```
rtmp://你抓取的低延迟IP/live-bvc/
```


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
执行结果参考
![2B7D382F-3D8C-4F9E-9BFB-72C927595F2F](https://user-images.githubusercontent.com/47912037/154753637-d76f691d-b40b-4d7d-9068-a97baef54cbb.png)


### 4.测试到节点的速度

在OBS内将“服务器”替换为
```
rtmp://你抓取的低延迟IP/live-bvc/
```

例如

![06FA45DB-CDB9-43FC-8573-89E12B95B6C1](https://user-images.githubusercontent.com/47912037/154753999-b71d1d6d-ff60-4115-bc46-3bf9b4581613.png)


然后直接推流测试即可。

如果长时间稳定无丢帧，这个IP即可作为备选之一。

### 常见问题

#### Q1:为什么抓出来的IP过一段时间就不能用了

#### A1:可能只是IP失效了，直接重新抓取最新IP之后再测试一次。

#### Q2:为什么白天好用，晚上就开始卡了，丢帧了

#### A2:国内晚高峰时间（国内时间晚上8-12点左右），国际线路拥堵，可能质量下降。建议国内晚高峰时间测试，这样结果最精确。

#### Q3:测试出来的IP都不好用？

#### A3:你网络太炸了，建议购买其他有本地接入的回国代理软件。




