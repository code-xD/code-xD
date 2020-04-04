from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.generics import *
from rest_framework import status
from .mixins import *
from .permissions import *
from rest_framework.response import Response
from django.core.files import File
from django.contrib.auth import authenticate, login, logout
# from django.core.Files import File


# Create your views here.
def check_json(func):
    
    def inner(request, *args, **kwargs):

        try:
            data = request.body
            data = json.loads(request.body.decode('utf8').replace("'", '"'))
            kwargs['data'] = data
        except Exception:
            return JsonResponse({"message": "Invalid JSON format.", "status": 0})

        return func(request, *args, **kwargs)

    return inner

class UserRegisterView(CreateAPIView):
    permission_classes = []
    serializer_class = ProfileSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            static_id = Profile.objects.get(aadhar_no = response.data.get('aadhar_no')).static_id
            return JsonResponse({'message':'Registered Successfully.','idtoken':static_id})
        return response

FILE_FORMATS_SUPPORTED = ('.jpg','pdf','.jpeg','.png')

@csrf_exempt
@require_POST
def AddDocumentView(request):
    data = request.POST
    static_id = request.META.get('HTTP_X_AUTH')
    profile = Profile.objects.get(static_id=static_id,is_registered=True)
    try:
        file = request.FILES["file"]
        if not file.name.endswith(FILE_FORMATS_SUPPORTED):
            return JsonResponse({"message": "File format not supported.", "status": 0})

        if file.multiple_chunks():
            message = "Uploaded file 2 is too big (%.2f MB)." % (
                file.size/(1000*1000),)
            return JsonResponse({"message": message, "status": 0})
    except Exception as e:
        return JsonResponse({'status':0,"message":str(e)})
    try:
        document = Document.objects.get(name=data['name'],profile=profile)
        print(document)
        document.document = file
        document.save()
    except Document.DoesNotExist:
        document = Document.objects.create(name=data['name'],profile=profile)
        document.document = file
        document.save()

    return JsonResponse({'status':1,"message":"file upload successful"})

class DocumentListView(ListAPIView):
    serializer_class = DocumentSerializer
    model = Document

    def get_queryset(self):
        queryset = Document.objects.filter(profile__static_id = self.request.META.get('HTTP_X_AUTH'),profile__is_registered=True)
        return queryset

@csrf_exempt
@require_POST
@check_json
def SetPasswordView(request,data):
    try:
        if data['password']==data['password1']:
            static_id = request.META.get('HTTP_X_AUTH')
            profile = Profile.objects.get(static_id=static_id)
            profile.auth_user.set_password(data['password'])
            profile.is_registered=True
            profile.auth_user.save()
            profile.save()
            return JsonResponse({'message':'Password created Successfully.'})
        return JsonResponse({'message':'fields not matching.'})
    except Exception as e:
        return JsonResponse({'message':str(e)})

@csrf_exempt
@require_POST
@check_json
def LoginUserView(request,data):
    try:
        username = data['username']
        password = data['password']
    except KeyError:
        return HttpResponseBadRequest("Insufficient Request Parameters")

    user = authenticate(username=username, password=password)
    if not user:
        return HttpResponseForbidden("Invalid Credentials!")
    
    try:
        profile = Profile.objects.get(auth_user=user,is_registered=True)
        payload = ProfileSerializer(profile).data
        payload['idtoken'] = profile.static_id
        return JsonResponse(payload)
    except:
        return HttpResponseForbidden("Profile Not Avaiable!") 