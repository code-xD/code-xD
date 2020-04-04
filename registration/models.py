from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import uuid
# from django.core.validators import MaxVa

status_choices = (('Approved','Approved'),('Pending','Pending'),('Rejected','Rejected'))
income_range = (('Less than 25L','Less than 25L'),('25L-5Cr','25L-5Cr'),('5Cr-10Cr','5Cr-10Cr'),('Greater than 10Cr','Greater than 10Cr'))

def document_directory_path(instance, filename):
    return f'Documents/{instance.profile.aadhar_no}/{instance.name}'.format(instance.name, filename.split('.')[0])

# Create your models here.
class Profile(models.Model):
    gstin = models.CharField('GST Number',max_length=15)
    aadhar_no = models.BigIntegerField('Aadhar Number',primary_key=True)
    name = models.CharField(max_length=100)
    state = models.CharField('State',max_length=30)
    city = models.CharField('City',max_length=50)
    email = models.EmailField()
    address = models.TextField()
    mobile_number = models.BigIntegerField()
    auth_user = models.ForeignKey(User,on_delete=models.CASCADE)
    static_id = models.UUIDField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    is_registered = models.BooleanField(default=False)
    status = models.CharField(max_length=20,default='Pending',choices=status_choices)

    def __str__(self):
        return str(self.aadhar_no)

class Document(models.Model):
    name = models.CharField(max_length=50)
    document = models.FileField(upload_to=document_directory_path)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)

class DataSet(models.Model):
    sector = models.CharField(max_length=100)
    investment_range = models.CharField(choices=income_range)
        