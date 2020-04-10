from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError
from django.db import transaction
import random
from django.template.defaultfilters import slugify
from django.db import IntegrityError
from django.conf import settings
from utils.populate import returnProfileData

def get_or_create_user(username, password=None):
    username = slugify(username)
    try:
        new_user = User.objects.create_user(username=username,password=password)
    except IntegrityError:
        raise ValidationError('Phone number already exists.')
    return new_user

API_URL = 'https://api.data.gov.in/catalog/2c895ab9-8042-4653-bfeb-7dc71281fd57?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&offset=0&limit=10&filters[State]=MAHARASHTRA'

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['aid','pan_number','state','district','address','mobile_number','is_registered','status','name']
        extra_kwargs = {
            'state':{'required':False},
            'district':{'required':False},
            'address':{'required':False},
            'name':{'required':False}
        }    
    def create(self,validated_data):
        number = validated_data.get('mobile_number')
        aid = validated_data.get('aid')
        with transaction.atomic():
            user = get_or_create_user(username=number)
            msme_data = returnProfileData(aid)
            profile = Profile.objects.create(**validated_data,**msme_data,auth_user=user)
        return profile

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance = Profile.objects.select_for_update().get(static_id=instance.static_id)
            is_registered = validated_data.get('is_registered', instance.is_registered)
            status = validated_data.get('status', instance.status)
            # Only pending orders can have status changed.
            if instance.is_registered == False:
                instance.is_registered = validated_data.get('is_registered', instance.is_registered)
                instance.save(update_fields = ['is_registered'])
                return instance                
            if instance.status == 'Pending':
                instance.status = validated_data.get('status', instance.status)
                instance.save(update_fields = ['status'])
                return instance
            raise ValidationError("Status can't be reverted.")

class DocumentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Document
        fields = ['document']