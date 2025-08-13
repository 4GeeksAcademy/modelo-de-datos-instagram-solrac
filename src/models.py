from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

#las tablas de asociacion se crean antes de las clases.
follower_table= Table(
     "follower_table",#declaramos el nombre de la tabla
     db.Model.metadata,
     Column("followed_id", ForeignKey("user.id")),
     Column("follower_id", ForeignKey("user.id"))
 )

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]= mapped_column(String(120), unique= True, nullable=False)
    firstname: Mapped[str]= mapped_column(String(65), nullable=False)
    lastname: Mapped[str]= mapped_column(String(65), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    posts: Mapped[list["Post"]] = relationship( back_populates="author")
    followers: Mapped[list["User"]] = relationship(
        "User", 
        secondary=follower_table, 
        primaryjoin= id == follower_table.c.followed_id, 
        secondaryjoin= id == follower_table.c.follower_id,
        back_populates="following"
    )
    following: Mapped[list["User"]] = relationship(
        "User",
        secondary=follower_table,
        primaryjoin= id == follower_table.c.follower_id,
        secondaryjoin = id == follower_table.c.followed_id,
        back_populates= "followers"
    )
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    comment_text: Mapped[str]= mapped_column(String(250), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post_comment:Mapped["Post"]= relationship(back_populates="comments")
    def serialize(self):
        return{
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post_comment")
    medias:Mapped[list["Media"]] = relationship(back_populates="post_media")

    def serialeze(self):{
        "id": self.id,
        "user_id": self.user_id
    }

class Media(db.Model):    
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[int] = mapped_column()
    url: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post_media: Mapped["Post"] = relationship(back_populates="medias")
    
    def serialize(self):{
        "id": self.id,
        "type": self.type,
        "url": self.url,
        "post": self.post
    }
