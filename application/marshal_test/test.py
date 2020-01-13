import requests

from application.model import *
from application.schema import *
from marshmallow import post_load
from flask import Blueprint, render_template, request

bp = Blueprint("marshalling", __name__, url_prefix='/marshal', template_folder='templates')


@bp.route('/post/main')
def post_main():
    return render_template('post_main.html')


@bp.route('/post/serialize')
def obj_to_json():
    # object to json

    post_schema = PostSchema(session=db.session)
    posts = Post.query.first()
    result = post_schema.dumps(posts)
    # print(result)
    return render_template('serialize.html', value=str(result), result=result)


@bp.route('/post/deserialize', methods=['POST'])
def json_to_obj():
    # json to object

    post_schema = PostSchema(session=db.session)
    req = request.form['title']
    result = post_schema.loads(req)
    return render_template('deserialize.html', result=result)
