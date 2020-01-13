from flask_marshmallow import Marshmallow, pprint
from marshmallow import post_load
from application.model import *

ma = Marshmallow()


class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post

    # @post_load
    # def make_post(self, data, **kwargs):
    #     return Post(**data)


class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category

    # @post_load()
    # def make_category(self, data, **kwargs):
    #     return Category(**data)
