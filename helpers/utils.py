import getpass
import os
import platform
import socket


def system_information():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    proc = platform.processor()
    system = platform.system()
    os_name = os.name
    machine = platform.machine()
    username = getpass.getuser()

    si = {
        'hostname': hostname,
        'ip': ip,
        'proc': proc,
        'system': system,
        'os_name': os_name,
        'machine': machine,
        'username': username
    }

    return si


