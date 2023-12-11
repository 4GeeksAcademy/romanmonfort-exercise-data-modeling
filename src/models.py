import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String ,Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    Id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)

    # Relación de followers
    followers = relationship('Follower', back_populates='user_to')
    following = relationship('Follower', back_populates='user_from')

    # Relación de posts
    posts = relationship('Post', back_populates='user')

    # Relación de comentarios
    comments = relationship('Comment', back_populates='author')

class Follower(Base):
    __tablename__ = 'follower'

    Id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('user.Id'))
    user_to_id = Column(Integer, ForeignKey('user.Id'))

    # Relaciones inversas
    user_from = relationship('User', back_populates='followers', foreign_keys=[user_from_id])
    user_to = relationship('User', back_populates='following', foreign_keys=[user_to_id])

class Media(Base):
    __tablename__ = 'media'

    ID = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', 'other'))
    url = Column(String)
    post_id = Column(Integer, ForeignKey('post.Id'))

 
    post = relationship('Post', back_populates='media')

class Post(Base):
    __tablename__ = 'post'

    Id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.Id'))


    user = relationship('User', back_populates='posts')


    media = relationship('Media', back_populates='post')

    comments = relationship('Comment', back_populates='post')

class Comment(Base):
    __tablename__ = 'comment'

    Id = Column(Integer, primary_key=True)
    comment_text = Column(String)
    author_id = Column(Integer, ForeignKey('user.Id'))
    post_id = Column(Integer, ForeignKey('post.Id'))

    author = relationship('User', back_populates='comments', foreign_keys=[author_id])
    post = relationship('Post', back_populates='comments')

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
