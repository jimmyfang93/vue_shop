from rest_framework.validators import UniqueValidator

import re
from datetime import datetime,timedelta
from vue_shop.settings import REGEX_MOBILE
from users.models import VerifyCode
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self,mobile):
        """
        验证手机号密码（函数名必须为validate_ + 字段名）
        :param mobile:
        :return:
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise  serializers.ValidationError("用户名已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE,mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_mintes_ago = datetime.now() -timedelta(hours=0,minutes=1,seconds=0)
        # 添加时间大于一分钟以前，也就是距离离现在还不足一分钟
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago,mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过一个60s")

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    pass
