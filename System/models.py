from django.db import models
from django.contrib.auth.models import User
# Create your models here.





class profile(models.Model):
    email = models.ForeignKey(User,to_field="username",on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=10)
    state = models.CharField(max_length=20)
    shift = models.CharField(max_length=10)
    ssc = models.CharField(max_length=4)
    hsc = models.CharField(max_length=4)
    ug = models.CharField(max_length=4)
    pg = models.CharField(max_length=4)
    year = models.CharField(max_length=4)

    class Meta:
        db_table = 'profile'


