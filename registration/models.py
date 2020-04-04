from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import uuid
# from django.core.validators import MaxVa


def document_directory_path(instance, filename):
    return f'Documents/{instance.profile.aadhar_no}/{instance.name}'.format(instance.name, filename.split('.')[0])

# Create your models here.
class Profile(models.Model):
    gstin = models.CharField('GST Number',max_length=15)
    aadhar_no = models.BigIntegerField('Aadhar Number',primary_key=True)
    state = models.CharField('State',max_length=30)
    city = models.CharField('City',max_length=50)
    email = models.EmailField()
    address = models.TextField()
    mobile_number = models.BigIntegerField()
    auth_user = models.ForeignKey(User,on_delete=models.CASCADE)
    static_id = models.UUIDField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.aadhar_no)

class Document(models.Model):
    name = models.CharField(max_length=50)
    document = models.FileField(upload_to=document_directory_path)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)