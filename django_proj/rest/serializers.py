from rest_framework import serializers, exceptions

from django.contrib.auth.models import User

from registration.models import Account
from registration.utils import email_to_username


class AccountSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    user_name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    password = serializers.CharField(required=False, allow_blank=True, max_length=100)
    first_name = serializers.CharField(required=True, allow_blank=True, max_length=100)
    middle_name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    last_name = serializers.CharField(required=True, allow_blank=True, max_length=100)
    email = serializers.CharField(required=True, allow_blank=True, max_length=100)
    mobile_no = serializers.CharField(required=True, allow_blank=True, max_length=100)
    
    def create(self, validated_data):
        user_name = validated_data['user_name']
        password = validated_data['password']
        first_name = validated_data['first_name']
        middle_name = validated_data.get('middle_name', '')
        last_name = validated_data['last_name']
        mobile_no = validated_data['mobile_no']
        email = validated_data['email']
        try:
            user = User.objects.get(email=email)
            raise exceptions.ValidationError(detail="email already registered")
        except User.DoesNotExist: 
            user = User.objects.create(email=email,
                                       username=email_to_username(email))    
            user.set_password(password)
            user.save()
            return Account.objects.create(user=user, first_name=first_name, middle_name=middle_name,
                                          last_name=last_name, mobile_no=mobile_no)
