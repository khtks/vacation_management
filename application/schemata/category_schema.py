from flask_marshmallow import Marshmallow
from application import ma
from application.models.category_model import *


class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category

    # @post_load()
    # def make_category(self, data, **kwargs):
    #     return Category(**data)
