import sqlalchemy
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Base = declarative_base()
from RasaHost.loggingDatabase.metadata import Base


class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    module = Column(String)
    filename = Column(String)
    line_no = Column(Integer)
    log_level = Column(String)
    message = Column(String)
    exception = Column(String)
    created = Column(DateTime)
    sender_id = Column(String)
    request_id = Column(String)


class LogRepository:
    def __init__(self, session):
        self.session = session

    def find(self, query, page, pageCount):
        # query 是一个查询条件列表
        # page 和 pageCount 用于分页查询
        # query = [
        #     {'message': 'error'},  # 消息中包含 "error"
        #     {'module': 'app'},     # 模块名中包含 "app"
        #     'john_doe',            # 通用条件，包含 "john_doe"
        # ]
        findLogs = self.session.query(Log)

        for part in query:
            if isinstance(part, dict):
                key = next(iter(part.keys()))
                value = part[key]
                findLogs = findLogs.filter(self.like(key, value))
            else:
                findLogs = findLogs.filter(self.like(None, str(part)))

        return findLogs \
            .order_by(Log.created.desc()) \
            .limit(pageCount).offset((page - 1) * pageCount)
        # .limit(pageCount)：这一部分使用 limit() 方法来限制查询结果的数量，即每页查询的数量。
        # .offset((page - 1) * pageCount)：这一部分使用 offset() 方法来指定从查询结果中的哪个位置开始获取数据，实现分页查询。
        # page 表示页码，pageCount 表示每页的记录数。
        # 因为页码从 1 开始计数，而偏移量是从 0 开始计数的。所以在计算偏移量时，需要将页码减去 1，然后乘以每页记录数。
        # 例如，如果你想获取第 3 页的数据，每页有 10 条记录，那么偏移量就是 (3 - 1) * 10 = 20，意味着你需要从第 21 条记录开始获取数据。
        # 这个计算方式可以帮助你在分页查询中准确定位要获取的数据的起始位置。

    def find_rasa(self, query, page, pageCount):

        requests_ids = self.session.query(Log.request_id).filter(Log.sender_id.isnot(None))

        for part in query:
            if isinstance(part, dict):
                key = next(iter(part.keys()))
                value = part[key]
                requests_ids = requests_ids.filter(self.like(key, value))
            else:
                requests_ids = requests_ids.filter(self.like(None, str(part)))

        requests_ids = requests_ids.group_by(Log.request_id) \
            .order_by(Log.created.desc()) \
            .limit(pageCount).offset((page - 1) * pageCount)

        return self.session.query(Log) \
            .filter(Log.request_id.in_(requests_ids)) \
            .order_by(Log.created.desc())

    def like(self, name, value):
        like = "%" + value + "%"  # 构建了模糊匹配的字符串，以实现在数据库中进行模糊匹配。 %匹配任意个字符
        if name == "message":
            return Log.message.like(like) | Log.exception.like(like)
        if name == "module":
            return Log.module.like(like)
        if name == "sender":
            return Log.sender_id.like(like)
        if name == "request":
            return Log.request_id.like(like)
        return Log.name.like(like) | \
               Log.module.like(like) | \
               Log.filename.like(like) | \
               Log.log_level.like(like) | \
               Log.message.like(like) | \
               Log.exception.like(like) | \
               Log.sender_id.like(like) | \
               Log.request_id.like(like) \


    def save(self, log):
        self.session.add(log)
        pass
