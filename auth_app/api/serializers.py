from rest_framework import serializers

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password



User = get_user_model()



class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer used for user registration.

    Validates the incoming registration data, ensures that the password
    meets Django's password validation rules, and checks that the
    password confirmation matches.
    """
        
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirmed_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']

    
    def validate(self, attrs):
        """
        Ensure that the password and confirmed_password fields match.

        Raises:
            serializers.ValidationError: If the passwords do not match.
        """
                
        if attrs['password'] != attrs['confirmed_password']:
            raise serializers.ValidationError({'password': 'Passwörter stimmen nicht überein'})
        return attrs
    

    def create(self, validated_data):
        """
        Create a new user instance using Django's built-in create_user method.

        The confirmed_password field is removed before creating the user.
        """
                
        validated_data.pop('confirmed_password')
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'], 
                                        password=validated_data['password'])

        return user



class LoginSerializer(serializers.Serializer):
    """
    Serializer used for user authentication.

    Validates the provided username and password by using Django's
    built-in `authenticate()` function. If authentication succeeds,
    the authenticated user object is added to the validated data.
    """
        
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """
        Validate the username and password combination.

        Raises:
            serializers.ValidationError: If authentication fails.

        Returns:
            dict: The validated data including the authenticated user.
        """
                
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({'detail': 'Ungültige Anmeldedaten'})
        attrs['user'] = user
        return attrs
    