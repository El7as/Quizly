from rest_framework import serializers

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password



User = get_user_model()



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirmed_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']

    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirmed_password']:
            raise serializers.ValidationError({'password': 'Passwörter stimmen nicht überein'})
        return attrs
    

    def create(self, validated_data):
        validated_data.pop('confirmed_password')
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'], password=validated_data['password'])

        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({'detail': 'Ungültige Anmeldedaten'})
        attrs['user'] = user
        return attrs
    
    