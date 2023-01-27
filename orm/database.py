"""定义关于与存放数据的数据库进行交互的操作。使用ORM进行维护。

库中主要由topics表以及不同的以帖子id（tid）命名存储的comment表存储数据。

通常，存储数据有以下几种情况：
    - 首次获取一个帖子的数据（在topics中无记录）
        此时会在topics中添加一条记录，而后创建对应comment表存储comments
    - 帖子主楼未更新，存在新回复
        此时需在对应comment表中插入新添的回复
    - 帖子主楼更新
        此时应在topics中添加新的对应'update_time'不同的记录。
也就是说，对外暴露的接口，应有以下操作：
    - isTopicExist 帖子记录是否存在。可选参数update_time判断是否发生更新
    - isCommentAdded 传入最新记录，根据reply_id判断是否存在回复添加（根据条数进行判断会因为评论删除而产生讹误）

    - addTopicRecord 添加主题帖记录
    - addComments 添加回复记录

    - createCommentsTable 添加一张回复表

    - queryTopic 查询主题帖记录
    - queryTopicWithComments 查询主题帖以及其回复记录

具体实现见下方注释


:Class
    DataBaseConnector:与数据库进行连接的实例类。会在创建时自动加载topics表对应的table model

:Function
    normalCheck(db: DataBaseConnector, result: dict):对createTask返回的结果进行普通处理（不考虑运行效率，只考虑确定性）
"""

from orm.topic import mapper_registry, Topic, get_comment_model
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from logs.TerminalLogger import LOGGER


class DataBaseConnector(object):
    """用于维护与数据库连接的对象类，它通过ORM进行连接与数据维护。

    :Attributes
        db_path:数据库文件存储路径
        engine:数据库连接
        target_topic_schema:当前ORM定义中的Topic表定义

    :Operation
        isTopicExist(self, tid: str, update_time: str = None)->bool:如果指定记录存在，返回True，反之返回False
        isCommentAdded(self,tid:str,reply_id:str)->dict：如果指定帖子存在新回复，在返回字典键'isCommentAdded'值为True。

        addTopicRecord(self, data: list[dict]):添加一条或多条topic记录。支持链式调用.
        addComments(self,tid:str,data:list[dict]):添加指定主题帖的回复记录。支持链式调用。
        createCommentsTable(self,tid:str):创建一张评论表。支持链式调用。

        queryTopic(self,tid:str,update_time:str = None)->list[dict]:查找指定主题帖内容，若不指定update_time，则返回其所有版本记录。
        queryTopicWithComments(self,tid:str)->dict:获取主题帖最新版本内容及其回复记录。

        updateDataBasePath(self, path: str):更新连接的数据库路径。

    """
    db_path = r'sqlite:///C:\Users\LeeWe\Documents\GitHub\doubansaver\Experiment.db'
    engine = create_engine(db_path)
    target_topic_schema = None
    target_comment_class = None
    table_schemas = []

    def __init__(self, db=r'sqlite:///C:\Users\LeeWe\Documents\GitHub\doubansaver\Experiment.db'):
        LOGGER.DEBUG('DataBaseConnector has been create....')
        self.db_path = db

        mapper_registry.metadata.create_all(bind=self.engine)

        self.target_topic_schema = mapper_registry.metadata.tables['topics']

        for key in mapper_registry.metadata.tables:
            self.table_schemas.append(
                mapper_registry.metadata.tables[key]
            )

    def __del__(self):
        LOGGER.DEBUG('DataBaseConnector is deleted')

    def isTopicExist(self, tid: str, update_time: str = None) -> bool:
        """判断主题帖记录是否存在或发生更新。判断是否发生更新时应把update_time一并传入。

        根据Session.scalar(sql)返回是否时None判断记录是否存在

        :Args
            tid:帖子id。
            update_time:帖子更新时间。如果指定，则在判断时添加update_time这一查询条件。更精准查找指定记录是否存在（因为同个主题帖可能在时间线上因为更新存在不同内容）
        """
        with Session(self.engine) as session:

            if update_time is None:
                sql = select(Topic).where(Topic.id == tid)
                # 如果存在结果，那么结果不会是None，以此判断该主题帖记录是否存在
                if session.scalar(sql) is None:
                    return False
                return True

            sql = select(Topic).where(Topic.id == tid, Topic.update_time == update_time)
            if session.scalar(sql) is None:
                return False
            return True

    def isCommentAdded(self, tid: str, reply_id: str) -> dict:
        """判断指定tid的帖子是否存在新回复。reply_id为新获得的回复数据中的最大id。为了减少IO，将同时把储存数据中的最大id和判断结果一同封装在字典中返回。

        :Args
            tid:主题帖的id
            reply_id:回复数据中的最大id。以此大小判断是否存在新id

        :Return
            dict->{
                'isCommentAdded':bool, //判断是否存在新回复
                'storgeId':str //储存的最新回复的id
            }
        """
        with Session(self.engine) as session:
            model = get_comment_model(tid)
            sql = select(model.reply_id).order_by(model.reply_id.desc())
            newly_storge_reply_id = session.scalar(sql)

            # 清除用完的表结构定义，避免不必要的内存开销
            mapper_registry.metadata.remove(
                mapper_registry.metadata.tables[tid]
            )

            if int(reply_id) > int(newly_storge_reply_id):
                return {
                    'isCommentAdded': True,
                    'storgeId': newly_storge_reply_id
                }
            else:
                return {
                    'isCommentAdded': False,
                    'storgeId': newly_storge_reply_id
                }

    def addTopicRecord(self, data: list[dict]):
        """添加一条或多条主题帖记录

        :Args
            data:主题帖记录数据，在mobile返回的结果应该是tid字典中内嵌的以'topic'标识的字典，传入时应将需要传入的记录放在列表中传入。
        """
        with Session(self.engine) as session:
            for ele in data:
                one_data = Topic(
                    id=ele['id'],
                    update_time=ele['update_time'],
                    title=ele['title'],
                    url=ele['url'],
                    create_time=ele['create_time'],
                    content=ele['content'],
                    author_name=ele['author_name'],
                    author_id=ele['author_id'],
                    author_uid=ele['author_uid'],
                    author_url=ele['author_url'],
                    author_true_url=ele['author_true_url'],
                    author_avatar=ele['author_avatar']
                )
                session.add(one_data)
            session.commit()
        return self

    def addComments(self, tid: str, data: list[dict]):
        """添加一条主题帖的回复记录

        :Args
            tid:帖子id
            data:commentsData。格式为[commentsDict]
        """
        model = get_comment_model(tid)
        with Session(self.engine) as session:
            for ele in data:
                ref_id = 'null'
                ref_storge = 'null'
                photo = 'null'
                if 'ref_id' in ele:
                    ref_id = ele['ref_id']
                if 'ref_storge' in ele:
                    ref_storge = str(ele['ref_storge'])
                if 'photo' in ele:
                    photo = ele['photo']
                one_data = model(
                    reply_id=ele['reply_id'],

                    author_name=ele['author_name'],
                    author_avatar=ele['author_avatar'],
                    author_id=ele['author_id'],
                    author_uid=ele['author_uid'],
                    author_url=ele['author_url'],
                    author_true_url=ele['author_true_url'],
                    author_register_time=ele['author_register_time'],
                    reply_text=ele['reply_text'],
                    reply_time=ele['reply_time'],

                    ref_id=ref_id,
                    ref_storge=ref_storge,
                    photo=photo
                )
                session.add(one_data)
            session.commit()

        mapper_registry.metadata.remove(
            mapper_registry.metadata.tables[tid]
        )

        return self

    def createCommentsTable(self, tid: str):
        """创建一张评论表，并自清定义"""
        model = get_comment_model(tid)
        mapper_registry.metadata.create_all(bind=self.engine)
        mapper_registry.metadata.remove(
            mapper_registry.metadata.tables[tid]
        )
        return self

    def queryTopic(self, tid: str, update_time: str = None) -> list[dict]:
        """根据tid查找对应topic记录，可指定update_time进行查找

        如果没有指定update_time,则会查询所有版本记录

        :Return
            list[dict],一个由topic对象字典组成的列表
        """
        with Session(self.engine) as session:
            if update_time is None:
                sql = select(Topic).where(Topic.id == tid)
                results = []
                for ele in session.scalars(sql):
                    results.append(ele.to_dict())
                return results

            sql = select(Topic).where(Topic.id == tid, Topic.update_time == update_time)
            results = []
            for ele in session.scalars(sql):
                results.append(ele.to_dict())
            return results

    def queryTopicWithComments(self, tid: str) -> dict:
        """根据tid获取最新主题帖内容及其回复。

        如要获取储存的所有主题帖版本记录，请使用queryTopic.

        :Return
            {
                'topic':dict,
                'comments':list[dict]
            }
        """
        model = get_comment_model(tid)
        with Session(self.engine) as session:
            sql = select(model)
            comments_result = []
            for ele in session.scalars(sql):
                comments_result.append(ele.to_dict())

            # 根据更新时间倒序查询，获取最近更新记录。
            sql = select(Topic).where(Topic.id == tid).order_by(Topic.update_time.desc()).limit(1)
            # 需通过to_dict()方法将Topic对象转为dict
            topic_results = session.scalar(sql).to_dict()

            mapper_registry.metadata.remove(
                mapper_registry.metadata.tables[tid]
            )

            return {
                'topic': topic_results,
                'comments': comments_result
            }

    def updateDataBasePath(self, path: str):
        self.db_path = path
        self.engine = create_engine(self.db_path)
        return self


if __name__ == "__main__":
    # 276706988,276675253,276423355
    # 魂组公示楼，冷处还号,test
    a = DataBaseConnector()
    b = a.queryTopicWithComments('276423355')
    # c = b['comments'][0].to_dict()
    #
    # # result = createNewTask([276706988,276675253,276423355])
    # # normalCheck(a,result)
    # print(b['topic'].__dict__)

    # g = a.isTopicExist(str(276675253))
    # print(g)
    # a.isCommentAdded(
    #     str(276675253),'123'
    # )
    # a.query_topic(276675253)
    # mapper_registry.metadata.remove(
    #     mapper_registry.metadata.tables['topics']
    # )
    # res = createNewTask([276675253])
    # a.create_comments_table(276675253).insert_comments(res['276675253']['comments'])
    # a.select_new(276675253)
