#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Author(Base):
    __tablename__ = 'Author'
    id = Column(Integer, primary_key=True)
    author = Column(String(128), index=True)
    description = Column(Text)
    dynasty = Column(String(512), index=True)

    def __init__(self, author, description, dynasty):
        self.author = author
        self.description = description
        self.dynasty = dynasty

    def __repr__(self):
        return '%s %s %s' % (self.author, self.description, self.dynasty)


class Poetry(Base):
    __tablename__ = 'Poetry'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), index=True)
    author = Column(String(255), index=True)
    dynasty = Column(String(512), index=True)
    paragraphs = Column(Text)
    strains = Column(Text)
    words = relationship('Word')

    def __init__(self, title, author, dynasty, paragraphs, strains):
        self.title = title
        self.author = author
        self.dynasty = dynasty
        self.paragraphs = paragraphs
        self.strains = strains

    def __repr__(self):
        return '%s %s %s %s %s' % (self.title, self.author, self.dynasty, self.paragraphs, self.strains)


class Word(Base):
    __tablename__ = 'Word'
    id = Column(Integer, primary_key=True)
    word = Column(String(255), index=True)
    poetry_id = Column(Integer, ForeignKey('Poetry.id'))

    def __init__(self, word, poetry_id):
        self.word = word
        self.poetry_id = poetry_id

    def __repr__(self):
        return '%s %s' % (self.word, self.poetry_id)


if __name__ == "__main__":
    #    engine = create_engine('mysql+pymysql://root:jiwenxuan@114.113.126.247/poetry')
    engine = create_engine('postgresql+psycopg2://jiwenxuan:jiwenxuan@114.113.126.247:5432/poetry')
    Base.metadata.create_all(engine)
