import paramiko
import json
from rest_framework import viewsets
from rest_framework.response import Response

from api.settings import *
from utils.ApiResponse import ApiResponse


class ServicesView(viewsets.ModelViewSet):

    def monitor_services(self, ssh_client):
        try:
            # Execute command to monitor services
            command = 'service --status-all'
            stdin, stdout, stderr = ssh_client.exec_command(command)

            # Read the output
            output = stdout.read().decode()

            # Parse the output into a list of dictionaries
            services = []
            for line in output.splitlines():
                parts = line.split()
                service = {
                    'name': parts[3],  # Assuming service name is at a certain position in the output
                    'status': parts[1],  # Assuming status is at a certain position in the output
                }

                services.append(service)

            return services

        except Exception as e:
            print("Error:", str(e))

    def connect_to_server(self):
        try:
            # Create an SSH client instance
            ssh_client = paramiko.SSHClient()

            # Automatically add host keys
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the SSH server
            ssh_client.connect(hostname=HOST_NAME, port=PORT, username=USERNAME, password=SERV_PASSWORD)

            print("Connected to server successfully!")

            # Return the SSH client object for further operations
            return ssh_client

        except paramiko.AuthenticationException:
            print("Authentication failed, please check your credentials.")
        except paramiko.SSHException as e:
            print("Unable to establish SSH connection:", str(e))
        except Exception as e:
            print("Error:", str(e))

        return None

    def read_services(self, request):
        # Connect to the server

        ssh_client = self.connect_to_server()

        # Monitor services
        if ssh_client:
            json_data = self.monitor_services(ssh_client)
            response = ApiResponse()
            response.setMessage("Services retrieved")
            response.setEntity(json_data)
            response.setStatusCode(200)

            # Close the SSH connection
            ssh_client.close()
            print("SSH connection closed.")
            return Response(response.toDict(), 200)
