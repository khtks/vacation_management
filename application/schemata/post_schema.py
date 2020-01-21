from application import ma
from application.models.post import *


class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post

    # @post_load
    # def make_post(self, data, **kwargs):
    #     return Post(**data)