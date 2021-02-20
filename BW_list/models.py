from django.db import models

# Create your models here.
class IP_list(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=15)
    ip = models.CharField(max_length=20)
    status = models.CharField(max_length=5)

class URL_list(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=15)
    url = models.URLField()
    remark = models.TextField()