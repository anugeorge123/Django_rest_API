import pyotp
from accounts import utils as ut
from rest_framework import viewsets
from accounts.models import Country,State, City, User
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .serializers import CountrySerializer, StateSerializer, CitySerializer, \
    UserSerializer, UserLoginSerializer, ChangePasswordSerializer, PasswordResetSerializer,\
    PasswordResetConfirmSerializer

class CountryView(viewsets.ModelViewSet):
    http_method_names = ['post', ]
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self,request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        countryName = serializer.data.get('countryName')
        countryObj = Country()
        countryObj.countryName=countryName
        countryObj.save()
        return Response(data={'status':status.HTTP_200_OK},
                        status=status.HTTP_200_OK)


class StateView(viewsets.ModelViewSet):
    http_method_names = ['post', ]
    serializer_class = StateSerializer
    queryset = State.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self,request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        stateName = serializer.data.get('stateName')
        countryId = serializer.data.get('countryName')
        stateObj = State()
        stateObj.stateName = stateName
        country_name = Country.objects.get(id=countryId)
        stateObj.countryName = country_name
        stateObj.save()
        return Response(data={'status':status.HTTP_200_OK},
                        status=status.HTTP_200_OK)


class CityView(viewsets.ModelViewSet):
    http_method_names = ['post', ]
    serializer_class = CitySerializer
    queryset = City.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        cityName = serializer.data.get('cityName')
        stateId = serializer.data.get('stateName')
        cityObj = City()
        cityObj.cityName = cityName
        state_name = State.objects.get(id=stateId)
        cityObj.stateName = state_name
        cityObj.save()
        return Response(data={'status': status.HTTP_200_OK},
                        status=status.HTTP_200_OK)


class SignupView(viewsets.ModelViewSet):
    http_method_names = ['post', ]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        phone = serializer.data.get('phone')
        email = serializer.data.get('email')
        user = User()
        user.set_password(serializer.data.get('password'))
        user.email = email
        user.username = username
        user.phone = phone
        countryId = serializer.data.get('countryName')
        country_name = Country.objects.get(id=countryId)
        stateId = serializer.data.get('stateName')
        state_name = State.objects.get(id=stateId)
        cityId = serializer.data.get('cityName')
        city_name = City.objects.get(id=cityId)
        user.countryName = country_name
        user.stateName = state_name
        user.cityName = city_name
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response(data={'status': status.HTTP_200_OK,'token': token.key},
                        status=status.HTTP_200_OK)

class LoginView(viewsets.ModelViewSet):
        permission_classes = (permissions.AllowAny,)
        http_method_names = ['post']
        serializer_class = UserLoginSerializer

        def create(self, *args, **kwargs):
            serializer = self.serializer_class(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            uname = serializer.data.get('username')
            username = User.objects.get(username = uname)
            pwd = serializer.data.get('password')
            user = authenticate(username=username, password=pwd)
            if not user:
                return Response({'message': 'Invalid credentials'},
                                status=status.HTTP_401_UNAUTHORIZED)
            else :
                return Response(data={'message': 'Success'},status=status.HTTP_200_OK)


class ChangePasswordView(viewsets.ViewSet):
    serializer_class = ChangePasswordSerializer
    http_method_names = ['post']
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(data={'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


class PasswordResetView(viewsets.ViewSet):
    serializer_class = PasswordResetSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        ut.password_reset_link_email(email, request)
        return Response(data={"message": "Password reset email has been sent."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    def get(self, request, format=None):
        token = request.GET.get('token')
        user = User.objects.filter(rp_otp=token).first()
        if user:
            return Response(data={'message': 'Success', 'token': token}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.data.get('password')
        token = serializer.data.get('token')
        user = User.objects.filter(rp_otp=token).first()
        if user:
            user.set_password(password)
            user.rp_otp = ''
            user.save()
            return Response(data={"message": "Your password has been reset successfully."}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)



