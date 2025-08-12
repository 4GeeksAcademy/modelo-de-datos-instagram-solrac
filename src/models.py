from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

#las tablas de asociacion se crean antes de las clases.
# follower_table= Table(
#     "follower_table",#declaramos el nombre de la tabla
#     db.model.metadata,
#     Column("Followed", ForeignKey("user.id")),#columna de como se llamara y lo que ira dentro.
#     Column("Follower", ForeignKey("user.id"))#columna de como se llamara y lo que ira dentro.
# )

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]= mapped_column(String(120), unique= True, nullable=False)
    firstname: Mapped[str]= mapped_column(String(65), nullable=False)
    lastname: Mapped[str]= mapped_column(String(65), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    # follower_table: Mapped[list["User"]] = relationship(
    #     "User",
    #     secondary= follower_table,
    #     backref= "user"
    #)
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            #"follower_table": [User.serialize() for user in self.follower_table]#a esto se le llama lista de compresión
            # do not serialize the password, its a security breach
        }

class follower(db.Model):
    user_from_id: Mapped[int] = mapped_column(primary_key=True)
    user_to_id: Mapped[int] = mapped_column(primary_key=True)

class comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    comment_text: Mapped[str]= mapped_column(String(250), nullable=False)
    author_id: Mapped[int] = mapped_column(unique=True)
    post_id: Mapped[int] = mapped_column(foraignKey="Post")

    def serialize(self):
        return{
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }


class post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[list["Media","comment"]] = relationship()

    def serialeze(self):{
        "id": self.id,
        "user_id": self.user_id
    }

class Media(db.Model):    
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[int] = mapped_column()
    url: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    post: Mapped[int] = mapped_column()
    
    def serialize(self):{
        "id": self.id,
        "type": self.type,
        "url": self.url,
        "post": self.post
    }
