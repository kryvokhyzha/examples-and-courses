from menus import print_general_menu
from db import db_creation, db_check_admin
import os
import platform
import getpass
import psutil
import atexit
import hashlib
import json
import winreg
import string
import random
from Crypto.Cipher import AES
from Crypto.Hash import MD4


iv = b'1234567890123456'


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, length))


def encrypt_data(key, data):
    encryptor = AES.new(key, AES.MODE_CFB, iv)
    return encryptor.encrypt(data)


def decrypt_data(key, data):
    decryptor = AES.new(key, AES.MODE_CFB, iv)
    return decryptor.decrypt(data)


def encrypt_db(db='users', length=2**3):
    db_file = f'{db}.db'
    exists = os.path.exists(db_file)
    if not exists or not db_check_admin():
        if exists:
            os.remove(db_file)
        return

    with open(db_file, 'rb') as file:
        password = input('Enter the password to encrypt DB file: ')
        key = password + get_random_string(length)

        print(f'Your generated password is {key}')

        _ = input('Press "enter" to continue... ')

        hashed_key = MD4.new(key.encode()).digest()
        # hashed_key = hashlib.md5(key.encode()).digest()
        encoded_data = encrypt_data(hashed_key, file.read())

        with open('encrypted_sample_db', 'wb') as encrypt_db_file:
            encrypt_db_file.write(encoded_data)
    os.remove(db_file)


def decrypt_db(key, db='users'):
    db_file = f'{db}.db'
    with open('encrypted_sample_db', 'rb') as encrypted_db_file:
        hashed_key = MD4.new(key.encode()).digest()
        # hashed_key = hashlib.md5(key.encode()).digest()
        decode_data = decrypt_data(hashed_key, encrypted_db_file.read())

        with open(db_file, 'wb') as db_file:
            db_file.write(decode_data)


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
    database_path = 'encrypted_sample_db'
    if os.path.exists(database_path):
        key = input('Enter the password to decrypt the DB file: ')
        decrypt_db(key)
    else:
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

    atexit.register(encrypt_db)
    main()
