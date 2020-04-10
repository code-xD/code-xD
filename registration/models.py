from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import uuid
# from django.core.validators import MaxVa

status_choices = (('Approved','Approved'),('Pending','Pending'),('Rejected','Rejected'),('Under Review','Under Review'))
income_range = (('Less than 25L','Less than 25L'),('25L-5Cr','25L-5Cr'),('5Cr-10Cr','5Cr-10Cr'),('Greater than 10Cr','Greater than 10Cr'))

def document_directory_path(instance, filename):
    filename = filename.split('/')[-1]
    return f'Documents/{instance.profile.aid}/{filename}'

# Create your models here.
class Profile(models.Model):
    pan_number = models.CharField('PAN Number',max_length=15)
    aid = models.CharField('AID', max_length = 12, primary_key=True)
    name = models.CharField(max_length=100)
    state = models.CharField('State',max_length=30)
    district = models.CharField('District',max_length=50)
    address = models.TextField()
    mobile_number = models.BigIntegerField()
    auth_user = models.ForeignKey(User,on_delete=models.CASCADE)
    static_id = models.UUIDField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    is_registered = models.BooleanField(default=False)
    status = models.CharField(max_length=20,default='Pending',choices=status_choices)

    def __str__(self):
        return str(self.aid)

class Document(models.Model):
    document = models.FileField(upload_to=document_directory_path)
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.aid

class ITRDataset(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE)
    total_tax = models.BigIntegerField()
    tax_paid = models.BigIntegerField()
    total_income = models.BigIntegerField()
    loss = models.BigIntegerField()
    reported_loss = models.BigIntegerField(default=0)
    deemed_income = models.BigIntegerField()