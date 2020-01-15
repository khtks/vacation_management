from flask_marshmallow import Marshmallow
from application import ma
from application.models.model import *


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
