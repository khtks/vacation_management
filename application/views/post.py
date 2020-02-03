# from application.schemata.post import PostSchema
# from application.models.post import Post
# from application.models.category import Category
# from application import db, api
# from flask_restful import Resource
# from flask import Blueprint, render_template, request
#
# post_bp = Blueprint("post", __name__, url_prefix='/post')
# post_schema = PostSchema()
# session = db.session
# api = api(post_bp)
#
#
# class Posts(Resource):
#     def get(self):
#         # return post_schema.dumps(Post.query.all(), many=True)
#         return render_template('post/posts_result.html', result=Post.query.all())
#
#     def post(self):
#         category = Category.query.filter(Category.name == request.form['category']).first()
#
#         if not category:
#             category = Category(name=request.form['category'])
#             session.add(category)
#
#         post = Post(title=request.form['title'], body=request.form['body'], category=category)
#         session.add(post)
#         session.commit()
#         return render_template('post/posts_result.html', result=Post.query.all())
#
#     def delete(self):
#         session.query(Post).delete()
#         session.commit()
#         return render_template('post/posts_result.html', result=Post.query.all())
#
#
# class PostItem(Resource):
#     def get(self, id):
#         return render_template('post/post_item_result.html', verb="Get", result=Post.query.get(id))
#
#     def delete(self, id):
#         result = Post.query.get(request.form['id'])
#         Post.query.filter(Post.id == request.form['id']).delete()
#         session.commit()
#         return render_template('post/post_item_result.html', verb='Delete', result=result)
#
#     def put(self, id):
#         post = Post.query.get(id)
#         data = request.form
#
#         if not post:
#             post = Post(title=data['title'], body=data['body'], category=Category.query.get(data['category']))
#             session.add(post)
#             session.commit()
#             return render_template('post.post_item_result.html', verb='Put', result=post)
#
#         post.title = data['title'] if data['title'] else post.title
#         post.body = data['body'] if data['body'] else post.body
#         post.category = Category.query.filter(Category.name == data['category']).first() if Category.query.filter(Category.name == data['category']).first() else post.category
#         post.pub_date = data['pub_date'] if data['pub_date'] else post.pub_date
#         session.commit()
#         return render_template('post/post_item_result.html', verb='Put', result=post.get_info())
#
#
# api.add_resource(Posts, '/')
# api.add_resource(PostItem, '/<int:id>')
