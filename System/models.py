from django.db import models

# Create your models here.


class register(models.Model):
    email = models.EmailField(primary_key=True,blank=False)
    first_name = models.CharField(max_length=10,blank=False)
    middle_name = models.CharField(max_length=10,blank=False)
    last_name = models.CharField(max_length=10,blank=False)
    year = models.CharField(max_length=10,blank=False)
    password = models.CharField(max_length=10,blank=False)

    class Meta:
        db_table = 'register'


class profile(models.Model):
    email = models.ForeignKey(register,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=10)
    state = models.CharField(max_length=20)
    pin = models.CharField(max_length=6)
    ssc = models.CharField(max_length=4)
    hsc = models.CharField(max_length=4)
    ug = models.CharField(max_length=4)
    pg = models.CharField(max_length=4)

    class Meta:
        db_table = 'profile'


