from flask import request, Blueprint, jsonify, session as sess
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from .database import db
from .models import User, Post
from .schemas import post_schema, posts_schema, users_schema, user_schema
from .services import hash_password, sha256_crypt

api = Blueprint('api', __name__, url_prefix='/api/v1')

jwt = JWTManager()

session = db.session


@api.get('/posts')
@jwt_required()
def post_list() -> jsonify:
    posts: dict = Post.query.all()
    return posts_schema.jsonify(posts)


@api.get('/posts/<int:post_id>')
@jwt_required()
def post_detail(post_id: int) -> jsonify:
    post = Post.query.filter_by(id=post_id).first()
    return post_schema.jsonify(post)


@api.post('/posts')
@jwt_required()
def post_add() -> jsonify:
    title: str = request.json['title']
    body: str = request.json['body']
    author: str = sess['username']
    post = Post(title=title, body=body, author=author)
    session.add(post)
    session.commit()

    return post_schema.jsonify(post)


@api.put('/posts/<int:post_id>')
@jwt_required()
def post_update(post_id: int) -> jsonify:
    post = Post.query.filter_by(id=post_id).first()
    if sess['username'] == post.author:
        title: str = request.json['title']
        body: str = request.json['body']
        post.title = title
        post.body = body

        session.commit()

        return post_schema.jsonify(post)
    return jsonify({'status': 403, 'message': 'Only the content author or site administrator can change content.'})


@api.delete('/posts/<int:post_id>')
@jwt_required()
def post_delete(post_id: int) -> jsonify:
    post = Post.query.filter_by(id=post_id).first()
    if sess['username'] == post.author:
        session.delete(post)
        session.commit()

        return jsonify({'status': 204, 'message': 'post deleted successfully.'})
    return jsonify({'status': 403, 'message': 'Only the content author or site administrator can delete content.'})


@api.post('/users/register')
def register() -> jsonify:
    username: str = request.json['username']
    email: str = request.json['email']
    password: str = request.json['password']
    hash_pass: str = hash_password(password)
    user = User.query.filter_by(username=username, email=email).first()
    if user is None:

        user = User(username=username, email=email, password=hash_pass)
        session.add(user)
        session.commit()

        response: dict = {
            'status': 201,
            'message': f'Successfully registered, {username}. Go to login for get the access token',
        }

        return jsonify(response)
    else:
        return jsonify({'status': 400, 'message': 'user already exists'})


@api.post('/users/login')
def login() -> jsonify:
    email: str = request.json['email']
    password: str = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user is not None and sha256_crypt.verify(password, user.password):
        auth_token: str = create_access_token(identity=email)

        sess['username'] = user.username

        response = {
            'status': 200,
            'message': 'Successfully logged in',
            'auth_token': auth_token
        }
        return jsonify(response)
    else:
        response = {
            'status': 400,
            'message': 'User does not exist or password is wrong'
        }
        return jsonify(response)

