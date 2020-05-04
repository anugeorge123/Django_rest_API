from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import APIException
from rest_framework import status
from accounts.models import Country,State, City, User

class CustomizedValidation(APIException):
    status_code = status.HTTP_200_OK
    default_detail = 'A server error occurred.'

    def __init__(self, detail, status_code):
        if status_code is not None:self.status_code = self.status_code
        if detail is not None:
            self.detail = {'message':detail, 'status':status_code}
        else: self.detail = {'detail': force_text(self.default_detail)}


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('countryName',)

    def validate(self, attrs):
        country = Country.objects.filter(countryName=attrs['countryName']).exists()
        if country == True:
            raise CustomizedValidation(detail="Already exist!",
                                       status_code=status.HTTP_400_BAD_REQUEST)
        return attrs


class StateSerializer(serializers.ModelSerializer):

    class  Meta:
        model = State
        fields = ( "__all__")

    def validate(self, attrs):
        state = State.objects.filter(stateName=attrs['stateName']).exists()
        if state == True:
            raise CustomizedValidation(detail="Already exist!",
                                       status_code=status.HTTP_400_BAD_REQUEST)
        return attrs

class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ( "__all__")

    def validate(self, attrs):
        city = City.objects.filter(cityName=attrs['cityName']).exists()
        if city == True:
            raise CustomizedValidation(detail="Already exist!",
                                       status_code=status.HTTP_400_BAD_REQUEST)
        return attrs

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username','email', 'password','phone', 'countryName','stateName','cityName')

    def validate(self, attrs):
        if len(attrs['password']) < 6:
            raise ValidationError({'message': 'Password should contain atleast 6 characters'})
        elif len(attrs['password']) > 16:
            raise ValidationError({'message': 'Password should not exceed more than 16 characters'})
        mail = User.objects.filter(email=attrs['email']).exists()
        phone_number = User.objects.filter(phone=attrs['phone']).exists()
        if mail == True and phone_number == True:
            raise CustomizedValidation(detail="Phone number and email are already registered",
                                       status_code=status.HTTP_400_BAD_REQUEST)
        if mail == False and phone_number == True:
            raise CustomizedValidation(detail="phone is already registered", status_code=status.HTTP_400_BAD_REQUEST)
        if mail == True and phone_number == False:
            raise CustomizedValidation(detail="email is already registered", status_code=status.HTTP_400_BAD_REQUEST)
        return attrs


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, old_password):
        user = self.context.get('user')
        if not user.check_password(old_password):
            raise serializers.ValidationError("password is incorrect")
        return old_password


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("email is not registered")
        return email


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    token = serializers.CharField()
    def validate(self, attrs):
        try:
            user = User.objects.filter(rp_otp=attrs['token']).first()
        except:
            raise ValidationError({'message': 'User not found'})
        if len(attrs['password']) < 6:
            raise ValidationError({'message': 'Password should contain atleast 6 characters'})
        elif len(attrs['password']) > 16:
            raise ValidationError({'message': 'Password should not exceed more than 16 characters'})
        return attrs
