import pytz
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken

from api.settings import inProd
from authuser.models import OTP
from authuser.resetPassSerializer import ResetPassSerializer
from authuser.sentOTPSerializer import sentOTPSerializer
from authuser.serializers import AuthUserSerializer
from authuser.validateOTPSerializer import ValidateOTPSerializer
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from utils.ApiResponse import ApiResponse
from utils.Helper import Helper
from utils.Helper2 import Helper2
from django.utils import timezone
from datetime import datetime


class AuthUSer(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = AuthUserSerializer

    def get_serializer_class(self):
        if self.action == 'sendOTP':
            return sentOTPSerializer
        elif self.action == "verifyOTP":
            return ValidateOTPSerializer
        elif self.action == "resetpassword":
            return ResetPassSerializer
        return AuthUserSerializer

    @action(detail=False, methods=['POST'])
    def authUser(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        otpMethod = request.data.get('otpMethod')
        helper = Helper()
        # helper.log(request)
        if username and password:
            try:
                user = CustomUser.objects.get(username=username)
                if user.check_password(password):
                    if user.check_password(password):
                        if not user.is_verified:
                            response = ApiResponse()
                            response.setStatusCode(status.HTTP_401_UNAUTHORIZED)
                            response.setMessage("Account is not verified")
                            return Response(response.toDict(), status=200)
                    serializer = CustomUserSerializer(user)
                    data = serializer.data
                    otp = helper.generate_otp(self)
                    email = serializer.data.get("email")
                    name = serializer.data.get("name")
                    saveOtp = helper.saveotp(otp, email)
                    sent = helper.send_otp_email(name, otp, email)
                    print("Use OTP: " + otp)
                    user_permissions = user.user_permissions.all()
                    roles = [permission.name for permission in user_permissions]
                    data['roles'] = roles
                    response = ApiResponse()
                    response.setStatusCode(status.HTTP_200_OK)
                    response.setMessage("Check for an OTP on your email")
                    response.setEntity(data)
                    return Response(response.toDict(), status=response.status)
                else:
                    response = ApiResponse()
                    response.setStatusCode(status.HTTP_400_BAD_REQUEST)
                    response.setMessage("Incorrect login credentials")
                    return Response(response.toDict(), status=200)
            except CustomUser.DoesNotExist:

                response = ApiResponse()
                response.setStatusCode(status.HTTP_400_BAD_REQUEST)
                response.setMessage("Incorrect login credentials")
                return Response(response.toDict(), status=200)
        else:
            response = ApiResponse()
            response.setStatusCode(400)
            response.setMessage("Email and password are required")
            return Response(response.toDict(), status=response.status)

    @action(detail=False, methods=['POST'])
    def sendOTP(self, request):
        response = ApiResponse()
        helper = Helper()
        # helper.log(request)
        serializer = sentOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            print(email)
            if email:
                try:
                    user = CustomUser.objects.get(email=email)
                    user_serializer = CustomUserSerializer(user)
                    name = user_serializer.data.get('name')
                    otp = helper.generate_otp()
                    try:
                        saveOtp = helper.saveotp(otp, email)
                        if inProd:
                            sent = helper.otp(name, otp, email)
                            if sent == 1:
                                print("Sent OTP: ", otp)
                                response.setMessage("An OTP was sent to your Email.")
                                response.setStatusCode(200)
                                return Response(response.toDict(), 200)
                            else:
                                response.setMessage("Failed to send Email")
                                response.setStatusCode(401)
                                return Response(response.toDict(), 200)

                        print("Sent OTP: ", otp)
                        response.setMessage("An OTP was sent to your Email.")
                        response.setStatusCode(200)
                        return Response(response.toDict(), 200)
                    except Exception as e:
                        response.setMessage(f"Error sending email: {str(e)}")
                        response.setStatusCode(401)
                        return Response(response.toDict(), 200)
                except CustomUser.DoesNotExist:
                    response.setMessage("No record found with this Email")
                    response.setStatusCode(404)
                    return Response(response.toDict(), 200)
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response({"message": "Email parameter is required", "status": status_code})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def verifyOTP(self, request):
        response = ApiResponse()
        helper = Helper()
        # helper.log(request)
        serializer = ValidateOTPSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data.get('otp')
            email = serializer.validated_data.get('email')
            try:
                existing_otp = OTP.objects.filter(email=email).last()
                if existing_otp.otp == otp:
                    current_time = timezone.now()
                    expirydate_str_without_timezone = existing_otp.expirydate.rsplit('.', 1)[0]
                    expiry_time = datetime.strptime(expirydate_str_without_timezone, "%Y-%m-%d %H:%M:%S")
                    # expiry_time = timezone.make_aware(expiry_time, timezone.utc)
                    expiry_time = pytz.utc.localize(expiry_time)
                    if current_time <= expiry_time:
                        user = CustomUser.objects.get(email=email)
                        refresh = RefreshToken.for_user(user)
                        access_token = str(refresh.access_token)
                        response.setMessage("OTP validated")
                        response.setStatusCode(200)
                        response.setEntity({'access': access_token, 'refresh': str(refresh)})
                        return Response(response.toDict(), 200)
                    else:
                        response.setMessage("OTP has expired")
                        response.setStatusCode(400)
                        return Response(response.toDict(), 200)
                else:
                    response.setMessage("Invalid OTP")
                    response.setStatusCode(400)
                    return Response(response.toDict(), 200)
            except OTP.DoesNotExist:
                response.setMessage("OTP does not exist for the provided email")
                response.setStatusCode(404)
                return Response(response.toDict(), 200)

        response.setMessage("Invalid data provided")
        response.setStatusCode(400)
        return Response(response.toDict(), 200)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        response = ApiResponse()
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            response.setMessage("Logged out successfully")
            response.setStatusCode(status.HTTP_205_RESET_CONTENT)
            return Response(response.toDict(), status=response.status)
        except Exception as e:
            response.setMessage(f"Error logging out: {str(e)}")
            response.setStatusCode(status.HTTP_400_BAD_REQUEST)
            return Response(response.toDict(), status=response.status)

    @action(detail=False, methods=['POST'])
    def resetpassword(self, request):
        response = ApiResponse()
        helper2 = Helper2()
        # helper2.log(request)
        serializer = ResetPassSerializer(data=request.data)
        if serializer.is_valid():
            # password = serializer.validated_data.get('password')
            resetpassword = serializer.validated_data.get('resetpassword')
            email = serializer.validated_data.get('email')
            if email:
                try:
                    user = CustomUser.objects.get(email=email)
                    user_serializer = CustomUserSerializer(user)
                    name = user_serializer.data.get('name')
                    resetpassword = helper2.generateresetpassword()
                    try:
                        user.set_password(resetpassword)
                        user.save()
                        sent = helper2.resetpassword(name, resetpassword, email)
                        if sent == 1:
                            print('Sent resetpassword: ', resetpassword)
                            response.setMessage('A new password was sent to your email.')
                            response.setStatusCode(200)
                            return Response(response.toDict(), 200)
                        else:
                            response.setMessage('Failed to send email')
                            response.setStatusCode(401)
                            return Response(response.toDict(), 200)

                    except Exception as e:
                        response.setMessage(f'Error sending email: {str(e)}')
                        response.setStatusCode(401)
                        return Response(response.toDict(), 200)



                except CustomUser.DoesNotExist:
                    response.setMessage('User not found')
                    response.setStatusCode(404)
                    return Response(response.toDict(), 200)

            else:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response({'message': 'Email parameter is recquired', 'status': status_code})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)