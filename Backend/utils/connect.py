import paramiko
import time

from utils.ApiResponse import ApiResponse


class SSHCommandExecutor:
    def __init__(self, hostname, username, private_key_path):
        self.hostname = hostname
        self.username = username
        self.private_key_path = private_key_path
        self.sshcon = paramiko.SSHClient()
        self.sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        response = ApiResponse()
        try:
            self.sshcon.connect(self.hostname, username=self.username, key_filename=self.private_key_path)
            if self.sshcon.get_transport().is_active():
                print(f"Connected to {self.hostname} successfully!")
        except paramiko.AuthenticationException:
            print("Authentication failed. Please check your private key and username.")
        except paramiko.SSHException as e:
            print("SSH connection failed:", str(e))

    def disconnect(self):
        self.sshcon.close()

    def execute_command(self, command):
        try:
            self.connect()
            print(f"Executing command: {command}")
            shell = self.sshcon.invoke_shell()
            time.sleep(1)
            shell.send(f"su - finadm\n")
            time.sleep(1)
            shell.send(f"finadm\n")
            time.sleep(1)
            shell.send(f"1\n")
            time.sleep(1)
            shell.send(f"{command}\n")
            time.sleep(1)
            output = shell.recv(65535).decode('utf-8')

            # Split the output into lines
            output_lines = output.splitlines()

            # Initialize stdout and stderr lists
            stdout = []
            stderr = []

            # Iterate through each line of output
            for line in output_lines:
                if not line.startswith("su"):  # Filter out su prompt lines
                    # Check if the line indicates an error (e.g., command not found)
                    if "command not found" in line.lower():
                        stderr.append(line)
                    else:
                        stdout.append(line)

            # Join the stdout and stderr lists into strings
            stdout_output = "\n".join(stdout)
            stderr_output = "\n".join(stderr)

            print(f"Standard Output:\n{stdout_output}")  # Print stdout for debugging
            print(f"Standard Error:\n{stderr_output}")  # Print stderr for debugging

            return stdout_output, stderr_output

        finally:

            self.disconnect()

    def map_directory(self, remote_directory_path, local_directory_path):
        try:
            self.connect()
            print(f"Mapping directory: {remote_directory_path}")

            sftp = self.sshcon.open_sftp()
            sftp.get(remote_directory_path, local_directory_path)
            return local_directory_path
        finally:

            self.disconnect()