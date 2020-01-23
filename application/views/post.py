from application.schemata.post import PostSchema
from application.models.post import Post
from application.models.category import Category
from application import db
from flask import Blueprint, render_template, request, redirect, url_for

post_bp = Blueprint("marshalling", __name__, url_prefix='/post')
post_schema = PostSchema()


@post_bp.route('/main')
def post_main():
    return render_template('post/main.html')


@post_bp.route('/create', methods=['POST'])
def post_create():
    title = request.form['title']
    body = request.form['body']
    category_list = Category.query.all()

    for i in category_list:
        if request.form['category'] == i.get_name():
            post = Post(title=title, body=body, category=i)
            db.session.add(post)
            db.session.commit()
            return render_template('post/create.html', post=post)

    category = Category(name=request.form['category'])
    post = Post(title=title, body=body, category=category)
    db.session.add(post)
    db.session.commit()
    return render_template('post/create.html', post=post)


@post_bp.route('<topic>/input')
def post_input(topic):
    if topic == "create":
        category_list = Category.query.all()
        # category_list = list(map(lambda x: x.get_name(), category_list))
        category_list = [x.get_name() for x in category_list]

        return render_template('post/create_input.html', category_list=category_list)

    if topic == "update":
        post_list = Post.query.all()
        # post_list = list(map(lambda x: x.get_name(), post_list))
        post_list = [x.get_name() for x in post_list]

        return render_template('post/create_input.html', category_list=post_list)


@post_bp.route('/delete/select_title')
@post_bp.route('/read/select_title')
def select_title():
    post_list = Post.query.all()
    result = [x for x in post_list]
    return render_template('post/title.html', title=str(set(result)))


@post_bp.route('/read_all')
def post_read_all():
    post_list = Post.query.all()

    return render_template('post/read_all.html', result=post_list)


@post_bp.route('/read', methods=['POST'])
def post_read():
    post_list = Post.query.filter(Post.title == request.form['title_name']).all()

    if len(post_list) == 0:
        return "Not in the Post", 400

    return post_schema.dumps(post_list, many=True)


@post_bp.route('/update')
def post_update():
    pass


@post_bp.route('/delete', methods=['POST'])
def post_delete():
    post_list = Post.query.filter(Post.title == request.form['title_name']).all()

    for i in post_list:
        db.session.delete(i)
    db.session.commit()

    return render_template('post/delete_result.html', result=Post.query.all())


@post_bp.route('/delete_all')
def post_delete_all():
    post_list = Post.query.all()
    for i in post_list:
        db.session.delete(i)
    db.session.commit()

    return render_template('post/delete_result.html', result=Post.query.all())
