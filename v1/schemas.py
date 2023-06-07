from flask_marshmallow import Marshmallow
from .models import Post, User

ma = Marshmallow()


class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "author", "title", "body")


class UserSchema(ma.Schema):
    class Meta:
        fields = ("username", "email", "password", "posts")


post_schema = PostSchema()
posts_schema = PostSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)


