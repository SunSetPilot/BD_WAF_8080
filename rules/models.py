from django.db import models

# Create your models here.
class Rules(models.Model):
    r_id = models.CharField(max_length=7,primary_key=True)
    r_name = models.CharField(max_length=70)
    r_type = models.CharField(max_length=20)
    r_date = models.DateField()
    r_discription = models.TextField()
    r_file = models.TextField()
    r_selected = models.IntegerField(default=0)

