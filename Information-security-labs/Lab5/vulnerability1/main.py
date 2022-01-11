from menus import print_general_menu
from db import db_creation, db_select
import os
import platform
import getpass
import psutil
import subprocess
import hashlib
import json
import winreg


def prepare_info_about_computer_hash():
    scree_height = os.popen('wmic path Win32_VideoController get CurrentVerticalResolution')

    system_info = {
        "username": getpass.getuser(),
        "device_name": platform.node(),
        "windows_path": os.environ['WINDIR'],
        "windows_system_path": os.environ['WINDIR'] + "\\System\\",
        "additional_info": {
            "keyboard_type": 'common',
            "screen_height": scree_height.read().split('\n\n')[1].strip(),
            "memory": psutil.disk_usage('/').total,
            "hdd_volume": os.getcwd().split(':')[0]
        }
    }

    return hashlib.sha256(json.dumps(system_info).encode()).hexdigest()


def main():
    db_creation()
    print_general_menu()


if __name__ == '__main__':
    try:
        hashed_info = prepare_info_about_computer_hash()

        reg_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            'Software\\Kryvokhyzha'
        )

        with reg_key:
            signature_value = winreg.QueryValueEx(reg_key, 'Signature')[0]

        if signature_value != hashed_info:
            raise Exception('Application is being launched on an external computer!')
    except Exception:
        raise Exception('Application is being launched on an external computer!')

    main()
