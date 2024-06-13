import psutil
import subprocess
import time
from datetime import datetime
import json


class Agent():
    def gather_cpu_metrics(self):
        # cpu Usage
        cpu_percent = psutil.cpu_percent(interval=1)
        try:
            cpu_temperature = psutil.sensors_temperatures()['coretemp'][0].current
            cpu_temperature = f'{cpu_temperature}°C'
        except (IndexError, KeyError):
            cpu_temperature = 'N/A'

        # cpu Load Average
        load_avg = psutil.getloadavg()[0]

        return {
            "cpuUsage": f'{cpu_percent}%',
            "temp": cpu_temperature,
            "load": load_avg,
        }
    def gather_sessions_metrics(self):
        sessions = subprocess.check_output(['who']).decode().splitlines()
        session_data = []
        for session in sessions:
            user_info = session.split()
            user = user_info[0]
            login_time = ' '.join(user_info[2:4])
            login_datetime = datetime.strptime(login_time, '%Y-%m-%d %H:%M')
            time_difference = datetime.now() - login_datetime
            session_data.append({
                "user": user,
                "loginTime": login_time,
                "sessionTime": str(time_difference)
            })
        return session_data

    def gather_memory_metrics(self):
        mem = psutil.virtual_memory()
        total_mem = mem.total / (1024 ** 3)  # Convert to GB
        used_mem = mem.used / (1024 ** 3)  # Convert to GB
        available_mem = mem.available / (1024 ** 3)  # Convert to GB
        mem_percent = mem.percent

        processes = [p.info for p in psutil.process_iter(['pid', 'name', 'memory_percent'])]
        process_data = []
        for process in processes:
            process_data.append({
                "pid": process['pid'],
                "name": process['name'],
                "memoryUsage": process['memory_percent']
            })

        return {
            "totalMemory": total_mem,
            "usedMemory": used_mem,
            "availableMemory": available_mem,
            "memoryUsage": f'{mem_percent}%',
            "processes": process_data
        }

    def gather_disk_metrics(self):
        disk = psutil.disk_usage('/')
        total_disk = disk.total / (1024 ** 3)  # Convert to GB
        used_disk = disk.used / (1024 ** 3)  # Convert to GB
        available_disk = disk.free / (1024 ** 3)  # Convert to GB

        # Calculate disk usage percentage
        disk_usage_percent = (used_disk / total_disk) * 100

        return {
            "totalDisk": total_disk,
            "usedDisk": used_disk,
            "availableDisk": available_disk,
            "diskUsage": disk_usage_percent,  # Include disk usage percentage in the returned dictionary
        }

    def get_running_services(self):
        services = []
        output = subprocess.check_output('systemctl list-units --type=service', shell=True).decode()
        lines = output.splitlines()
        for line in lines[1:]:
            columns = line.strip().split(maxsplit=4)
            if len(columns) >= 4:
                service_name = columns[0]
                desc = columns[4] if len(columns) > 4 else ""
                status = columns[3]
                services.append({
                    "name": service_name,
                    "description": desc,
                    "status": status,
                })

        service_count = {}
        for service in services:
            service_count[service['name']] = service_count.get(service['name'], 0) + 1
        for service_name, count in service_count.items():
            if count > 2:
                subprocess.run(f'systemctl stop {service_name}', shell=True)
        return services


