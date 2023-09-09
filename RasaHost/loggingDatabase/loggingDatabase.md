在Flask中，通常使用会话工厂来创建数据库连接和会话对象，以便更好地管理数据库操作。会话工厂是一种模式，它可以帮助在每个请求处理时创建一个数据库会话，并在请求结束后自动提交或回滚事务，从而提高数据库操作的可维护性和安全性。
### __init__.py
定义公共接口（模块中对外可见的类和函数
### db_context.py
创建一个绑定到数据引擎的会话工厂，调用它来得到一个会话对象，并使用该会话对象初始化两个不同的`仓库对象`，仓库对象通常用于将有关的数据库操作封装在一个特定的类中，以提供更高级别的接口和抽象，使代码更具可维护性。

将不同类型的数据库操作封装到不同的仓库类中，然后在应用的其他部分中使用这些仓库对象来执行数据库操作。

每个仓库都共享同一个数据库会话，以维护事务的一致性。
### metadata.py
Conversation和Log模型类的父类，每个模型类对应一张数据库表
### conversations.py
- class Conversation：Conversation 模型类
- class ConversationRepository：处理Conversation 模型类
### logs.py
- class Log: Log 模型类
- class LogRepository：处理Log 模型类



