from django.db import models
from django.contrib.auth.models import User
# Create your models here.





class profile(models.Model):
    email = models.ForeignKey(User,to_field="username",on_delete=models.CASCADE,unique=True)
    ssc = models.CharField(max_length=6)
    hsc = models.CharField(max_length=6)
    ug = models.CharField(max_length=6)
    ug_stream = models.CharField(max_length=6)
    mca_sem1 = models.CharField(max_length=6,blank=True,null=True)
    mca_sem2 = models.CharField(max_length=6,blank=True,null=True)
    mca_sem3 = models.CharField(max_length=6,blank=True,null=True)
    mca_sem4 = models.CharField(max_length=6,blank=True,null=True)
    mca_sem5 = models.CharField(max_length=6,blank=True,null=True)
    year = models.CharField(max_length=4)
    shift = models.CharField(max_length=50)

    class Meta:
        db_table = 'profile'

class personal(models.Model):
    email = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE,unique=True)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    dob = models.DateField()
    gender = models.CharField(max_length=7)
    contact = models.CharField(max_length=10)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    class Meta:
        db_table = 'personal'



class placement(models.Model):
    email = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE, unique=True)
    placement=models.CharField(max_length=40)
    ppackage=models.CharField(max_length=40)
    dojp=models.DateField()
    hrname=models.CharField(max_length=40)
    hrcontact=models.CharField(max_length=40)
    hremail=models.CharField(max_length=40)
    status=models.CharField(max_length=40)

    class Meta:
        db_table = 'placement'




class internship(models.Model):
    email = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE, unique=True)
    internship=models.CharField(max_length=40)
    ipackage=models.CharField(max_length=40)
    projectname=models.CharField(max_length=40)
    seminar=models.CharField(max_length=40)
    doji=models.DateField()
    hrname=models.CharField(max_length=40)
    hrcontact=models.CharField(max_length=40)
    hremail=models.CharField(max_length=40)
    status=models.CharField(max_length=40)

    class Meta:
        db_table = 'internship'