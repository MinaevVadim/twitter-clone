import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

from db import Base


class Tweet(Base):
    __tablename__ = 'tweet'

    id = Column(Integer, primary_key=True)
    content = Column(String(250), nullable=True)
    author = Column(Integer, ForeignKey('user.id'))
    tweet_date = Column(DateTime, default=datetime.datetime.utcnow())

    attachments = relationship('Media', lazy='selectin')

    users = relationship('User', back_populates='tweets')

    likes = relationship('Like', lazy="selectin")

    def to_json(self):
        return {
            "id": self.id,
            "content": self.content,
            "attachments": [i.to_json() for i in self.attachments],
            "author": self.users.to_json(),
            "likes": [i.to_json() for i in self.likes],
        }

    def __repr__(self):
        return f'{self.id} | {self.content} | {self.author}'


user_following = Table(
    'user_following', Base.metadata,
    Column('followers', Integer, ForeignKey('user.id'), primary_key=True),
    Column('following', Integer, ForeignKey('user.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    api_key = Column(String(50), index=True)
    name = Column(String(50))

    following = relationship(
        'User', lambda: user_following, lazy='selectin',
        primaryjoin=lambda: User.id == user_following.c.followers,
        secondaryjoin=lambda: User.id == user_following.c.following,
        backref=backref('followers')
    )

    tweets = relationship('Tweet', back_populates='users')
    likes = relationship('Like', back_populates='users')

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def get_user_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "followers": [i.to_json() for i in self.following],
        }

    def __repr__(self):
        return f'{self.id} | {self.api_key} | {self.name}'


class Like(Base):
    __tablename__ = 'like'

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    tweet_id = Column(Integer, ForeignKey('tweet.id'), primary_key=True)

    users = relationship('User', lazy='selectin', back_populates='likes')

    def to_json(self):
        return {
            "user_id": self.user_id,
            "name": self.users.name,
        }

    def __repr__(self):
        return f'{self.user_id} | {self.tweet_id}'


class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    media = Column(String(150))

    tweet_id = Column(Integer, ForeignKey('tweet.id'))

    def to_json(self):
        return {
            "image": self.media,
        }

    def __repr__(self):
        return f'{self.id} | {self.media}'
