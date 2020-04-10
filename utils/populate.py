import requests
from rest_framework.exceptions import ValidationError

API_URL = 'https://api.data.gov.in/catalog/2c895ab9-8042-4653-bfeb-7dc71281fd57?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&offset=0&limit=10&filters[State]=MAHARASHTRA'

def returnProfileData(AID):
    r = requests.get(API_URL)
    dataset = r.json()['records']
    output_dict = {}
    for data in dataset:
        if data['AID'] == AID:
            output_dict['name'] = data['EnterpriseName']
            output_dict['district']= data['District']
            output_dict['address'] = data['Address']
            output_dict['state'] = data['State']
            return output_dict
    raise ValidationError('You are not registered as a MSME.')
