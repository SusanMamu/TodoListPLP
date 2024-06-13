import os
import random

import paramiko
from django.core.mail import send_mail

from api.settings import BASE_DIR
from users.models import CustomUser
from datetime import timedelta, datetime
from django.utils import timezone




class Helper2():
    def resetpassword(self, name, resetpassword, email):
        # verification_link = f"https://3c97-2c0f-fe38-2102-f942-62c5-78b8-6e43-79e6.ngrok-free.app/spinner/account/verify/{email}"
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
                    <p style="font-size: 20px, color: black;">Use: <span class="otp" >{resetpassword}</span></p>
                    <p>Use this password to login and change immediately after successful login. Do not share password with anyone.</p>
                </body>
            </html>
            """
            sent = send_mail(
                'reset password',
                '',
                'no-reply@gmail.com',
                [email],
                fail_silently=False,
                html_message=email_content,
            )
            return sent

        except Exception as e:
            # response.setMessage(f"Error sending email: {str(e)}")
            sent = 0
            print(f"Error sending email: {str(e)}")
        return sent

    def generateresetpassword(self):
        characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
        resetpassword = ''.join(random.choice(characters) for _ in range(8))
        return resetpassword

    def saveresetpassword(self, resetpassword, email):
        expiry_time = timezone.now() + timedelta(hours=24)
        resetpasswordData = CustomUser(
            resetpassword=resetpassword,
            email=email,
            expirydate=expiry_time
        )
        resetpasswordData.save()
        return None

    def log(self, request):
        current_date = datetime.now().strftime('%Y.%m.%d')
        log_file_name = f"{current_date}-request.log"
        log_file_path = os.path.join(BASE_DIR, f'utils/logs/{log_file_name}')
        log_string = f"[{datetime.now().strftime('%Y.%m.%d %I.%M.%S %p')}] => method: {request.method} uri: {request.path} queryString: {request.GET.urlencode()} protocol: {request.scheme} remoteAddr: {request.META.get('REMOTE_ADDR')} remotePort: {request.META.get('REMOTE_PORT')} userAgent: {request.META.get('HTTP_USER_AGENT')}"
        if os.path.exists(log_file_path):
            mode = 'a'
        else:
            mode = 'w'
        with open(log_file_path, mode) as log_file:
            log_file.write(log_string + '\n')

    # def connect_to_server(self, ipAddress):
    #     try:
    #         # Fetch server configuration from the database
    #         server = ServerConfiguration.objects.get(ip_address=ipAddress)
    #         ssh_client = paramiko.SSHClient()
    #         ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #
    #         ssh_client.connect(hostname=server.ip_address, port=22,
    #                            username=server.username, password=server.password)
    #         print("Connected to server successfully!")
    #         return ssh_client
    #
    #     except ServerConfiguration.DoesNotExist:
    #         print("Server configuration not found for IP address:", ipAddress)
    #     except paramiko.AuthenticationException:
    #         print("Authentication failed, please check your credentials.")
    #     except paramiko.SSHException as e:
    #         print("Unable to establish SSH connection:", str(e))
    #     except Exception as e:
    #         print("Error:", str(e))
