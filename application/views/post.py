from application.schemata.post import PostSchema
from application.models.post import Post
from application.models.category import *
from application import db
from flask import Blueprint, render_template, request, redirect, url_for

post_bp = Blueprint("post", __name__, url_prefix='/post')
post_schema = PostSchema()
session = db.session


@post_bp.route('/main')
def post_main():
    return render_template('post/main.html')


@post_bp.route('/', methods=['POST', 'GET', 'DELETE'])
def post():

    if request.method == "POST":
        category = Category.query.filter(Category.name == request.form['category']).first()

        if not category:
            category = Category(name=request.form['category'])
            session.add(category)

        post = Post(title=request.form['title'], body=request.form['body'], category=category)
        session.add(post)
        session.commit()
        return render_template('post/create_result.html', post=post, result=Post.query.all())

    elif request.method == "GET":
        return render_template('post/read_all.html', result=Post.query.all())

    elif request.method == "DELETE":
        id = [x.get_id() for x in Post.query.all()]
        session.query(Post).delete()
        session.commit()
        return render_template('post/delete_result.html', id=id, result=Post.query.all())


@post_bp.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def post_item(id):
    if request.method == 'GET':
        return render_template('post/read.html', id=id, result=Post.query.get(id))

    elif request.method == 'PUT':
        if not Post.query.get(id):
            new_post = Post(title="put title", body="put body", category=Category(id=id, name="put category"))
            session.add(new_post)
            session.commit()
            return post_schema.dumps(new_post)
        else:
            old_post = str(Post.query.get(id))
            new_post = Post.query.get(id)
            new_post.title = request.form['title']
            new_post.body = request.form['body']
            session.commit()
            return render_template('post/put_result.html', old_post=old_post, new_post=new_post)

    elif request.method == 'DELETE':
        Post.query.filter(Post.id == id).delete()
        session.commit()
        return render_template('post/delete_result.html', id=id, result=Post.query.all())


@post_bp.route('/information')
def input_info():
    return render_template('post/input_info.html', category=[x.get_name() for x in Category.query.all()])


@post_bp.route('/select_id', methods=['POST', 'GET'])
def select_id():

    if request.method == 'POST':
        return redirect(url_for('post.post_item', id=request.form['id']))

    else:
        return render_template('post/select_id.html', id=[x.get_id() for x in Post.query.all()])


