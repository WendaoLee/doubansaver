# 枝江存档姬
豆瓣小组自动存档bot。
目前仅上传了bot监听通知爬取内容的源码，之后会陆续上传其他代码与文档。
因为是出于兴趣一时兴起写的小玩具，
## 使用说明
在**豆瓣小组**的帖子下艾特枝江存档姬，她将帖子当前内容以**邮件**的形式备份到[存档站](http://asoul.otterdaily.cn:9900)上。

相关数据接口会在不久后更新。欢迎重写Web端页面提交PR。

详细简介请见:[[简陋风慎入] 豆瓣存档bot枝江存档姬（测试版）使用指南及说明 ](https://www.douban.com/group/topic/268799808)

## 原理
枝江存档姬本质上只是一个爬取网页内容进行分析的脚本，这一块我不多说。主要讲一下豆瓣的消息推送机制。

豆瓣主要采用SSE（Server-Sent Events）进行消息推送，即推送一个数据流进行服务器到浏览器端的单方面消息推送。因此只要监听数据流中是否有event推送过来，便能判断是否有收到新消息。从而进行之后的行为。

如ZhiJiangSaver.py，您可见到我们用了第三方的SSE包：

```python
sendUrl = ""
messages = SSEClient(sendUrl)
for msg in messages:
```

其实它更加表义的写法应该为：
```python
async with sse_client.EventSource(
    sendUrl
) as event_source:
    try:
        async for event in event_source:
            # do something here
    except ConnectionError:
        pass
```

不过因为只是出于兴趣写的小玩具，就没有认真整了。如果您有意愿改写代码，欢迎提交PR。
