from application import ma
from application.models.user_info import *


class UserInfoSchema(ma.ModelSchema):
    class Meta:
        model = UserInfo
