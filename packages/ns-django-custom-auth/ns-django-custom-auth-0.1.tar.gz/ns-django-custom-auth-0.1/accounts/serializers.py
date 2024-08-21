from .models import *
from rest_framework.serializers import ModelSerializer



class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name','last_name','email','mobile_code','mobile_no',
                  'age','gender','profile_pic','role_id','social_id','social_type',
                  'is_active','is_staff','is_superuser','created_on','updated_on']
