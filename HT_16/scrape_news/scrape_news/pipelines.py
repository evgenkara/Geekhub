"""
Переробити попереднє домашнє завдання: зберігати результати в базу, використовуючи pipelines.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import Session
import os


Base = declarative_base()


class DataTable(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    date = Column(String)
    title = Column(String)
    text = Column(String)
    tags = Column(String)
    url = Column(String)

    def __init__(self, date, title, text, tags, url):
        self.date = date
        self.title = title
        self.text = text
        self.tags = tags
        self.url = url

    def __repr__(self):
        return f"<Data {self.date} {self.title}, {self.text}, {self.tags}, {self.url}>"


class ScrapeNewsPipeline(object):
    def __init__(self):
        basename = 'News'
        self.engine = create_engine("sqlite:///%s" % basename, echo=False)
        if not os.path.exists(basename):
            Base.metadata.create_all(self.engine)

    def process_item(self, item, spider):
        dt = DataTable(item['date'], item['title'], item['text'], item['tags'], item['url'])
        self.session.add(dt)
        return item

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def open_spider(self, spider):
        self.session = Session(bind=self.engine)
