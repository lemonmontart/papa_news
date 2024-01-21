from django.db import models


class NewsData(models.Model):
    id = models.AutoField(primary_key=True)  # 자동으로 생성되는 AutoField를 사용
    keyword = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    url = models.URLField()
    press = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
