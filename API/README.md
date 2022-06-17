# README

> 目前只是简单写了几个API，之后如果我个人有空的话会重写一个前后端分离的前端（至少一个月后）。如果您有意愿重写前端，欢迎提交Issue与pr。
>
> 暂定API的测试端口为:asoul.otterdaily.cn:9000 。暂时没有访问限制。
>
> 下面是我暂时写的几个API，如果您觉得有必要加新的，务必发Issue反馈。

### [GET] /api/getLatest

> 获取最近存档的十条记录，按时间倒序排序（最近的在前边）。
>
> 它将返回一个JSON数组，其中每一个JSON对象都代表一条记录，它包括以下几个键值：

```
{
	"id":xxx,  //标识该记录的唯一id，将用它来获取帖子内容。
	”title“:xxx //原帖标题
	"topicNo":xxx //原帖在豆瓣的标识号，即`topic/`之后的数字
	"author":xxxx //原帖发帖人，即楼主
}
```

返回示例：

```
"[{'id': 65, 'title': '唉，对贝拉梁木 ', 'topicNo': '269063044', 'author': 'Deft'}]"
```

### [GET]/api/getmailInfo/:mailkey

> 获取指定存档记录的内容。它将返回一个html串。
>
> mailkey为上一节的"id"

示例：

`[GET]/api/getmailInfo/65`

返回：

```html
 <link rel=\"stylesheet\" href=\"https://img3.doubanio.com/f/group/8a7bfaa234ca077efdfb8240bdbff091a1eb6c97/css/group/editor/runtime.css\"/>    <h1>    唉，对贝拉梁木    <div class=\"event-labels\">    </div> 
 ....
 即原帖的html内容
```

## [GET]/api/search/:searchkey

> 搜索标题含有指定内容的的记录。按时间倒序进行排序。
>
> searchkey即为指定内容。
>
> 它将返回一个JSON数组，其中每一个JSON对象都代表一条记录，它包括以下几个键值：

```
{
	"id":xxx，  //标识该记录的唯一id，将用它来获取帖子内容。
	”title“:xxx //原帖标题
}
```

示例：

`/api/search/李问道`

返回：

```json
[{'id': 51, 'title': '转发：Zeitgeist 在小组讨论 ✓东西，和你锯跌一起带节... 的回复中@李问道'}, {'id': 19, 'title': '[268802576/]测试 来自: 李问道(燃烧对生活的热爱)'}]
```

