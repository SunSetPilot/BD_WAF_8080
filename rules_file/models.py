from django.db import models

# Create your models here.
class rule_files_list(models.Model):
    id = models.AutoField(primary_key=True)
    f_name = models.CharField(max_length=50)
    f_type = models.CharField(max_length=20)
    f_date = models.DateField()
    f_discription = models.TextField()

