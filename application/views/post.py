from application.schemata.schema import *
from flask import Blueprint, render_template, request, redirect, url_for

post_bp = Blueprint("marshalling", __name__, url_prefix='/post')
post_schema = PostSchema()


@post_bp.route('/main')
def post_main():
    return render_template('post_main.html')


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
            return render_template('post_create.html', post=post_schema.dumps(post))

    category = Category(name=request.form['category'])
    post = Post(title=title, body=body, category=category)
    db.session.add(post)
    db.session.commit()
    return render_template('post_create.html', post=post_schema.dumps(post))


@post_bp.route('<topic>/input')
def post_create_input(topic):
    if topic == "create":
        category_list = Category.query.all()
        result = []
        for i in category_list:
            result.append(i.get_name())
        return render_template('post_create_input.html', category_list=result)

    if topic == "update":
        post_list = Post.query.all()
        result = []
        for i in post_list:
            result.append(i.get_name())
        return render_template('post_create_input.html', category_list=result)


@post_bp.route('/delete/select_title')
@post_bp.route('/read/select_title')
def select_title():
    post_list = Post.query.all()
    result = []
    for i in post_list:
        result.append(i.get_title())
    return render_template('post_title.html', title=list(set(result)))


@post_bp.route('/read_all')
def post_read_all():
    count = Post.query.count()
    post_list = Post.query.all()
    # if count == 1:
    #     return render_template('post_read_all.html', result=post_schema.dumps(post_list[0]))
    # else:
    #     # result = post_schema.dumps(post_list, many=True)
    return render_template('post_read_all.html', result=post_list, hello="world", post_list_str=post_schema.dumps(post_list, many=True))


@post_bp.route('/read', methods=['POST'])
def post_read():
    title_name = request.form['title_name']
    post_list = db.session.query(Post).filter(Post.title == title_name).all()

    if len(post_list) == 0:
        return "ERROR", 400

    result = post_schema.dumps(post_list, many=True)
    return result


@post_bp.route('/update')
def post_update():
    pass




@post_bp.route('/delete', methods=['POST'])
def post_delete():
    post_list = db.session.query(Post).filter(Post.title == request.form['title_name']).all()
    for i in post_list:
        db.session.delete(i)
    db.session.commit()

    return render_template('post_delete_result.html', result=post_schema.dumps(Post.query.all(), many=True))


@post_bp.route('/delete_all')
def post_delete_all():
    post_list = Post.query.all()
    for i in post_list:
        db.session.delete(i)
    db.session.commit()

    return render_template('post_delete_result.html', result=post_schema.dumps(Post.query.all(), many=True))

@post_bp.route('<test>/id')
def test(test):
    return test
