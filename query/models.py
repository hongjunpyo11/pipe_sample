from django.db import models
from django.contrib.auth.models import User


class Script(models.Model):
    script_name = models.CharField(max_length=100)
    query_text = models.TextField(null=True)

    reg_dtm = models.DateTimeField(auto_now_add=True, null=True)
    reg_user = models.CharField(max_length=100, null=True)
    udt_dtm = models.DateTimeField(null=True)
    udt_user = models.CharField(max_length=100, null=True)

    last_used_dtm = models.DateTimeField(auto_now=True)

    public_yn = models.BooleanField(default=False)
    use_yn = models.BooleanField(default=True)


class ScriptPermission(models.Model):
    script = models.ForeignKey(Script, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    can_run = models.BooleanField(default=True)

# ScriptPermission 모델은 Script 모델과 User 모델 간의 다대다 관계를 정의합니다.
# 이 모델은 하나의 Script 인스턴스에 대해 여러 User 인스턴스가 연결될 수 있고, 그 반대의 경우도 가능합니다.
# 각각의 ScriptPermission 인스턴스는 연결된 Script 인스턴스와 User 인스턴스에 대한 권한 정보를 저장합니다.
# 이 모델은 Script 모델과 함께 데이터베이스에 생성되어야 하며,
# 스크립트 생성 시에는 해당 스크립트에 대한 ScriptPermission 인스턴스를 적절하게 생성해주어야 합니다.
#
# ScriptPermission 모델에 추가로 필요한 기능이 있다면 언제든지 필드를 추가하거나 메소드를 정의할 수 있습니다.


# class ScriptUser(models.Model):
#     script = models.ForeignKey(Script, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_dtm = models.DateTimeField(auto_now_add=True)
