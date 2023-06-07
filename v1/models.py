from .database import db


class User(db.Model):
    __allow_unmapped__ = True

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(), unique=True)
    email: str = db.Column(db.String(), unique=True)
    password: str = db.Column(db.String())
    posts: str = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, **kwargs) -> None:
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')

    def __repr__(self) -> str:
        return f'User "{self.username}"'


class Post(db.Model):

    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(100), nullable=False)
    body: str = db.Column(db.Text(length=300), nullable=False)
    author: str = db.Column(db.String(), db.ForeignKey('user.username'))

    def __init__(self, **kwargs) -> None:
        self.title: str = kwargs.get('title')
        self.body: str = kwargs.get('body')
        self.author: str = kwargs.get('author')

    def __repr__(self) -> str:
        return f'Post "{self.title}"'
