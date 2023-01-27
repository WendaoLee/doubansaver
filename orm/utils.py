from orm.database import DataBaseConnector


def normalCheck(db: DataBaseConnector, result: dict):
    """通用数据处理函数。可通过这个函数完成对数据的添加与更新。

    :Args
        db:连接数据库的对象实例
        result:由createTask返回的数据结果
            结构为：{
                'tid':{
                    'topic':dict,
                    'comments':list[dict]
                }
            }
    """
    for key, value in result.items():

        # 嵌套if，很糟糕的写法。之后可能会考虑改写
        # 首先判断帖子记录是否存在，如果记录存在，还需考虑原主题帖是否有更新
        if db.isTopicExist(tid=key):

            # 判断主题帖是否存在更新。因为如果不存在更新，那么传进来数据的update_time会与数据库中记录相同，返回True
            if db.isTopicExist(tid=key, update_time=value['topic']['update_time']):

                # 此时帖子不存在更新，需要判断是否有新回复。如果有，则需添加回复。
                # 传入的reply_id如此写法是因为移动API返回的数据总是把最新回复放在列表末尾
                respones = db.isCommentAdded(tid=key,
                                             reply_id=value['comments'][len(value['comments']) - 1]['reply_id']
                                             )

                # 如果存在新回复，则截取回复数据中reply_id大于储存的id的数据，而后把存入数据库中,之后continue即可
                if respones['isCommentAdded']:
                    storge_id = int(respones['storgeId'])
                    result_data = [ele for ele in value['comments'] if int(ele['reply_id']) > storge_id]
                    db.addComments(tid=key, data=result_data)
                    continue

            # 若是存在更新，则需把记录写入topic表中，而后开始判断是否有新回复
            else:
                db.addTopicRecord(data=[value['topic']])
                respones = db.isCommentAdded(tid=key,
                                             reply_id=value['comments'][len(value['comments']) - 1]['reply_id']
                                             )
                # 如果存在新回复，则截取回复数据中reply_id大于储存的id的数据，而后把存入数据库中,之后continue即可
                if respones['isCommentAdded']:
                    storge_id = int(respones['storgeId'])
                    result_data = [ele for ele in value['comments'] if int(ele['reply_id']) > storge_id]
                    db.addComments(tid=key, data=result_data)
                    continue

        # 如果帖子不存在，则照常建表、添加记录即可
        else:
            db.addTopicRecord(data=[value['topic']])
            db.createCommentsTable(tid=key).addComments(tid=key, data=value['comments'])
