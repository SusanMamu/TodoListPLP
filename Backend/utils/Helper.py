import os
import random
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from api import settings
from authuser.models import OTP
from datetime import timedelta, datetime

from utils.ApiResponse import ApiResponse

from api.settings import *


class Helper:

    @staticmethod
    def send_otp_email(name, otp, email):
        try:
            email_content = f"""
            <html>
                <head>
                    <style>
                        font-size: 12px;
                    </style>
                </head>
                <body>
                    <p>Hello {name},</p>
                    <p tyle="font-size: 20px, color: black;">Use: <span class="otp" >{otp}</span></p>
                    <p>If you did not request this, please ignore. Do not share OTP with anyone.</p>
                </body>
            </html>
            """
            sent = send_mail(
                'Verification OTP',
                '',
                'no-reply@gmail.com',
                [email],
                fail_silently=False,
                html_message=email_content,
            )
            return sent

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return 0

    # @staticmethod
    #
    # def generate_otp():
    #     characters = "0123456789"
    #     otp = ''.join(random.choice(characters) for _ in range(4))

    @staticmethod
    def generate_otp(self):
        characters = "0123456789"
        otp = ''.join(random.choice(characters) for _ in range(4))

        return otp

    @staticmethod
    def saveotp(otp, email):
        expiry_time = timezone.now() + timedelta(minutes=5)
        otp_data = OTP(
            otp=otp,
            expirydate=expiry_time,
            email=email
        )
        otp_data.save()

    @staticmethod
    def log(request):
        current_date = datetime.now().strftime('%Y.%m.%d')
        log_file_name = f"{current_date}-request.log"
        log_file_path = os.path.join(BASE_DIR, f'utils/logs/{log_file_name}')
        log_string = f"[{datetime.now().strftime('%Y.%m.%d %I.%M.%S %p')}] => method: {request.method} uri: {request.path} queryString: {request.GET.urlencode()} protocol: {request.scheme} remoteAddr: {request.META.get('REMOTE_ADDR')} remotePort: {request.META.get('REMOTE_PORT')} userAgent: {request.META.get('HTTP_USER_AGENT')}"
        mode = 'a' if os.path.exists(log_file_path) else 'w'
        with open(log_file_path, mode) as log_file:
            log_file.write(log_string + '\n')