import sqlalchemy
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
# Base = declarative_base()
from RasaHost.loggingDatabase.logs import Log, LogRepository
from RasaHost.loggingDatabase.conversations import Conversation, ConversationRepository
from RasaHost.loggingDatabase.metadata import Base


class DbContext(object):
    dbEngine = create_engine('sqlite:///rasa-host.sqlite')  # 数据库引擎
    Base.metadata.create_all(dbEngine)
    # 调用 create_all() 方法来根据 Base 中定义的模型类，在数据库中创建相应的数据表。
    # 通过定义继承自 Base 的类，你可以创建数据库模型类（也称为映射类），用于描述数据库中的表结构。
    # 这些模型类将映射到数据库中的实际表，从而允许你通过这些类来操作数据库。
    # 在这里是Log类（在logs.py中）和Conversation类（在conversations.py中）e.g. class Log(Base):
    dbSessionFactory = scoped_session(sessionmaker(bind=dbEngine))  # 会话工厂

    # sessionmaker函数用于创建会话工厂
    # scoped_session函数用于创建作用域会话对象，它接受一个参数，即会话工厂对象.
    # 它会返回一个新的会话对象，该会话对象具有作用域范围，并可以跟踪当前线程或协程的状态。

    # 作用域会话对象:在每个线程或协程中都是唯一的，因此可以安全地在多线程或异步环境中使用。
    # 它会自动管理会话的生命周期，包括会话的创建、提交或回滚事务、关闭会话以及释放与之相关的资源。
    # 无需手动管理会话的创建和关闭

    # 会话工厂的作用是创建会话对象，并管理会话对象的生命周期。它提供了一种标准化的方式来创建会话对象，并且可以配置一些会话相关的选项
   
    def __init__(self):
        self.session = self.dbSessionFactory()
        # dbSessionFactory是一个会话工厂对象，通过 sessionmaker 创建。
        # 这个工厂对象实际上是一个可调用对象，可以像函数一样调用来创建会话对象。每次调用时，它都会返回一个新的数据库会话对象，该会话对象与特定请求相关联。
        # 会话对象通常用于执行查询、插入、更新和删除等操作
        self.logs = LogRepository(self.session)
        self.conversations = ConversationRepository(self.session)
        # ConversationRepository是一个用于对Conversation模型进行数据库操作的类
      

    def commit(self):
        self.session.commit()  # 提交会话以保存更改
