# import pyotp
import os
import requests
import urllib.request
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
    PasswordResetConfirmSerializer, EditProfileSerializer, SocialLoginSerializer

class CountryView(viewsets.ModelViewSet):
    http_method_names = ['post', 'get']
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    permission_classes = (permissions.AllowAny,)

    def list(self, request, **kwargs):
        countryObj = Country.objects.all()
        country_name = countryObj.values('countryName')
        return Response(data={'data': country_name, "status" :status.HTTP_200_OK},status=status.HTTP_200_OK)

    # def create(self,request, *args, **kwargs):
    #     serializer = self.serializer_class(data=self.request.data)
    #     serializer.is_valid(raise_exception=True)
    #     countryName = serializer.data.get('countryName')
    #     countryObj = Country()
    #     countryObj.countryName=countryName
    #     countryObj.save()
    #     return Response(data={'status':status.HTTP_200_OK},
    #                     status=status.HTTP_200_OK)


class StateView(viewsets.ModelViewSet):
    http_method_names = ['post','get' ]
    serializer_class = StateSerializer
    queryset = State.objects.all()
    permission_classes = (permissions.AllowAny,)

    def list(self, request, **kwargs):
        stateObj = State.objects.all()
        state_name = stateObj.values('stateName')
        return Response(data={'data': state_name, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

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
    http_method_names = ['post', 'get']
    serializer_class = CitySerializer
    queryset = City.objects.all()
    permission_classes = (permissions.AllowAny,)

    def list(self, request, **kwargs):
        cityObj = City.objects.all()
        city_name = cityObj.values('cityName')
        return Response(data={'data': city_name, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

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
        ut.confirmation_email(email, user)
        user.save()
        token, created = Token.objects.get_or_create(user=user)

        return Response(data={'status': status.HTTP_200_OK,'token':token.key},
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
            token, created = Token.objects.get_or_create(user=user)
            if not user:
                return Response({'message': 'Invalid credentials'},
                                status=status.HTTP_401_UNAUTHORIZED)
            else :
                return Response(data={'status': status.HTTP_200_OK,'message': 'Success','token': token.key},status=status.HTTP_200_OK)


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


class EditProfileView(viewsets.ViewSet):
    serializer_class = EditProfileSerializer
    http_method_names = ['get','post']
    permission_classes = (permissions.IsAuthenticated, )

    def list(self, request, **kwargs):
        user = self.request.user
        userObj = User.objects.get(username=user)
        username = userObj.username
        phone = userObj.phone
        email = userObj.email
        countryId = userObj.countryName_id
        country_name = Country.objects.filter(id=countryId).values('countryName')
        countryName = country_name[0]['countryName']
        stateId = userObj.stateName_id
        state_name = State.objects.filter(id=stateId).values('stateName')
        stateName = state_name[0]['stateName']
        cityId = userObj.cityName_id
        city_name = City.objects.filter(id=cityId).values('cityName')
        cityName = city_name[0]['cityName']
        return Response(data={'username':username , 'phone':phone,\
                              'email':email,'country':countryName,'state':stateName,\
                              'city':cityName,"status": status.HTTP_200_OK}, status=status.HTTP_200_OK,)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        email = serializer.data.get('email')
        phone = serializer.data.get('phone')
        country = serializer.data.get('country')
        state = serializer.data.get('state')
        city = serializer.data.get('city')
        userObj = User.objects.get(username=user)
        userObj.email = email
        userObj.username = username
        userObj.phone = phone
        countryObj = Country.objects.filter(countryName = country)
        userObj.countryName_id = countryObj[0].id
        stateObj = State.objects.filter(stateName=state)
        userObj.stateName_id = stateObj[0].id
        cityObj = City.objects.filter(cityName=city)
        userObj.cityName_id = cityObj[0].id
        userObj.save()
        return Response(data={'message': 'success','status':status.HTTP_200_OK}, status=status.HTTP_200_OK)

class PasswordResetView(viewsets.ViewSet):
    serializer_class = PasswordResetSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        ut.password_reset_link_email(email, request)
        return Response(data={'status': status.HTTP_200_OK,"message": "Password reset email has been sent."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    def get(self, request, format=None):
        token = request.GET.get('token')
        user = User.objects.filter(rp_otp=token).first()
        if user:
            return Response(data={'message': 'Success', 'token': 748875}, status=status.HTTP_200_OK)
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

class SocialLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SocialLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        signup_method = serializer.data.get('signup_method')

        # Facebook
        if signup_method == 'facebook':
            url = 'https://graph.facebook.com/v3.2/me?fields=id,name,email,picture&access_token=' + serializer.data["access_token"]
            data = requests.get(url).json()
            print("data ====>>>",data)
            # check data values
            email = data["email"]
            username = data['name']
            user = User.objects.filter(email=email)
            if not user.exists():
                user = User(email=email)
                if len(username.split(' ')) > 1:
                    user.first_name = username.split(' ')[0]
                    user.last_name = username.split(' ')[1]
                else:
                    user.first_name = username

                image_url = 'https://graph.facebook.com/' + data['id'] + '/picture?type=large'
                img = urllib.request.urlretrieve(image_url, user.first_name + ".jpg")
                user.userImage = img[0]
                r = requests.get(image_url)
                with open('media/'+ user.first_name + ".jpg", 'wb') as f:
                    f.write(r.content)
                os.remove(user.first_name + ".jpg")
                user.username = email.split('@')[0].lower() + '_facebook'
                user.email_verified = True
                user.signup_method = signup_method
                user.save()
            else:
                user = user[0]

        # Google
        if signup_method == 'google':
            url = 'https://www.googleapis.com/oauth2/v1/userinfo?scope=email&access_token=' + serializer.data["access_token"]
            s = 'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='+ serializer.data["access_token"]
            r = requests.get(url).json()
            print("dataaaa",r)
            email = r["email"]
            username = r['name']
            user = User.objects.filter(email=email)
            if not user.exists():
                user = User(email=email)
                if len(username.split(' ')) > 1:
                    user.first_name = username.split(' ')[0]
                    user.last_name = username.split(' ')[1]
                else:
                    user.first_name = username
                image_url = r['picture']
                img = urllib.request.urlretrieve(image_url, user.first_name + ".jpg")
                user.profile_image = img[0]
                r = requests.get(image_url)
                with open('media/' + user.first_name + ".jpg", 'wb') as f:
                    f.write(r.content)
                user.username = email.split('@')[0].lower() + '_google'
                user.email_verified = True
                user.signup_method = signup_method
                user.save()
            else:
                user = user[0]

        token, created = Token.objects.get_or_create(user=user)

        return Response(data={'response':{'access_token': token.key, "userId":user.id,},
                              "message": "Login Successful",
                              }, status=status.HTTP_200_OK)



