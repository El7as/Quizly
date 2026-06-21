from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


from .serializers import RegisterSerializer, LoginSerializer



class RegisterView(APIView):
    """
    Handles user registration requests.

    This endpoint accepts POST requests containing user registration data.
    It validates the incoming payload using the RegisterSerializer and,
    if valid, creates a new user account in the system.
    """


    def post(self, request):
        """
        Create a new user account.
        """

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'User created succesfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    """
    Handles user login and JWT token creation.

    This endpoint validates the provided credentials using the LoginSerializer.
    If authentication is successful, it generates a refresh token and access token
    using SimpleJWT and stores both tokens in HTTP-only cookies.
    """


    def post(self, request):
        """
        Authenticate a user and return JWT tokens in cookies.
        """

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            response = Response({'detail': 'Login successfully!', 'user': {'id':user.id, 'username': user.username, 'email': user.email,}}, status=status.HTTP_200_OK)
            response.set_cookie(key='access_token', value=str(refresh.access_token), httponly=True, secure=True, samesite='Lax')
            response.set_cookie(key='refresh_token', value=str(refresh), httponly=True, secure=True, samesite='Lax')

            return response
        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    """
    Handles user logout by invalidating the refresh token and
    removing authentication cookies.

    This endpoint requires the user to be authenticated.
    """
    

    def post(self, request):
        """
        Log out the authenticated user.
        """

        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            response = Response({'detail': 'Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid.'}, status=status.HTTP_200_OK)

            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')

            return response
        
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RefreshTokenView(APIView):
    """
    Issues a new access token using a valid refresh token stored in cookies.

    This endpoint does not require a request body. It reads the refresh token
    from the user's cookies, validates it, and returns a new access token.
    """


    def post(self, request):
        """
        Refresh the access token.
        """

        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token missing or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)

            response = Response({'detail': 'Token refreshed'}, status=status.HTTP_200_OK)
            response.set_cookie(key='access_token', value=new_access, httponly=True, secure=True, samesite='Lax')

            return response
        
        except TokenError:
            return Response({'detail': 'Refresh token invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
