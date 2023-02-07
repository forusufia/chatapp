from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    #ユーザー名、メールアドレス、パスワードのシンプルなデフォルト構成を使う
    pass

#とーくるーむ用のモデル
class Talk(models.Model):
    #メッセージ
    message = models.CharField(max_length=500)

    #送信者
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_talk"
    )

    #受信者
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_talk"
    )

    #時刻
    # auto_now_add=True とすると、
    # そのフィールドの値には、オブジェクトが
    # 生成されたときの時刻が保存されます。
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} -> {}".format(self.sender, self.receiver)


