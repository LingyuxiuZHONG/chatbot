"""
Repository of polls that stores data in a MongoDB loggingDatabase.
"""

from bson.objectid import ObjectId, InvalidId
from pymongo import MongoClient

from . import Poll, Choice, PollNotFound
from . import _load_samples_json


def _poll_from_doc(doc):
    """Creates a poll object from the MongoDB poll document."""
    return Poll(str(doc['_id']), doc['text'])  # 在 MongoDB 中，_id 字段是保留字段，用作主键，并且除非显式提供，否则会自动生成。


def _choice_from_doc(doc):
    """Creates a choice object from the MongoDB choice subdocument."""
    return Choice(str(doc['id']), doc['text'], doc['votes'])


class Repository(object):
    """MongoDB repository."""

    def __init__(self, settings):
        """Initializes the repository with the specified settings dict.
        Required settings are:
         - MONGODB_HOST
         - MONGODB_DATABASE
         - MONGODB_COLLECTION
        """
        self.name = 'MongoDB'
        self.host = settings['MONGODB_HOST']  # 表示连接的目标数据库主机
        self.client = MongoClient(self.host)  # 创建一个 MongoDB 客户端对象，用于与 MongoDB 数据库进行交互
        self.database = self.client[settings['MONGODB_DATABASE']]  # 可以通过索引方式获取数据库实例，方法是在方括号中指定数据库名称。
        self.collection = self.database[settings['MONGODB_COLLECTION']]
        # 集合可以看作是一组相关文档的容器，类似于关系型数据库中的表。每个文档可以具有不同的字段和结构，但是它们在同一个集合中。
        # 集合没有固定的结构，这意味着您可以在同一集合中存储具有不同字段和数据结构的文档。

    def get_polls(self):
        """Returns all the polls from the repository."""
        docs = self.collection.find()  # find() 方法返回一个 MongoDB 游标（Cursor），表示查询结果集。游标可以迭代，以逐个获取文档。
        # 游标在处理大量文档时非常有用，因为它允许您逐步加载和处理文档，而不需要一次性将所有文档加载到内存中。
        polls = [_poll_from_doc(doc) for doc in docs]
        return polls

    def get_poll(self, poll_key):
        """Returns a poll from the repository."""
        try:
            doc = self.collection.find_one({"_id": ObjectId(poll_key)})
            if doc is None:
                raise PollNotFound()

            poll = _poll_from_doc(doc)
            poll.choices = [_choice_from_doc(choice_doc)
                            for choice_doc in doc['choices']]
            return poll
        except InvalidId:
            raise PollNotFound()

    def increment_vote(self, poll_key, choice_key):
        """Increment the choice vote count for the specified poll."""
        try:
            self.collection.update(  # 接受两个参数：第一个参数是一个查询条件，表示要更新的文档，第二个参数是一个更新操作。
                {
                    "_id": ObjectId(poll_key),
                    "choices.id": int(choice_key),
                },
                {
                    "$inc": {"choices.$.votes": 1} # "$inc"：这是 MongoDB 更新操作符之一，表示对文档中的指定字段进行增加操作。
                    # {"choices.$.votes": 1}：这是一个字典，表示要增加的字段及其增加的值。
                    # "choices.$.votes" -- $ 符号通常是用于匹配第一个满足查询条件的数组元素，匹配到第一个满足查询条件的 choices 数组元素
                }
            )
        except(InvalidId, ValueError):
            raise PollNotFound()

    def add_sample_polls(self):
        """Adds a set of polls from data stored in a samples.json file."""
        for sample_poll in _load_samples_json():
            choices = []
            choice_id = 0
            for sample_choice in sample_poll['choices']:
                choice_doc = {
                    'id': choice_id,
                    'text': sample_choice,
                    'votes': 0,
                }
                choice_id += 1
                choices.append(choice_doc)

            poll_doc = {
                'text': sample_poll['text'],
                'choices': choices,
            }

            self.collection.insert(poll_doc)
