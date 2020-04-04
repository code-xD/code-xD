from rest_framework.generics import GenericAPIView
from django.http import HttpResponseBadRequest,HttpResponseNotFound,JsonResponse,HttpResponseForbidden
from rest_framework.response import Response
# from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ListSerializer
from rest_framework.generics import get_object_or_404
import json

# Use this for Updating and Creating Items only
class QueryParamLookupMixin(object):

    lookup_fields_dict = None
 
    def get_object(self):
            queryset = self.filter_queryset(self.get_queryset())

            # Perform the lookup filtering.

            filter_kwargs = {}

            if self.lookup_fields_dict:
                data = self.request.query_params
                print(data)
                for kwarg, field in self.lookup_fields_dict.items():
    
                    try:
                        filter_kwargs[field] =  data[kwarg]
                    except KeyError:
                        return HttpResponseBadRequest("Insufficient Parameters.")

            print(filter_kwargs)

            obj = get_object_or_404(queryset, **filter_kwargs)
            print(obj)
            # May raise a permission denied
            self.check_object_permissions(self.request, obj)

            return obj
