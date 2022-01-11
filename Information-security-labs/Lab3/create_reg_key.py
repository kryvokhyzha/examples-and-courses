import winreg
from main import prepare_info_about_computer_hash


reg_key = winreg.CreateKey(
    winreg.HKEY_CURRENT_USER,
    'Software\\Kryvokhyzha'
)

with reg_key:
    winreg.SetValueEx(reg_key, 'Signature', 0, winreg.REG_SZ, prepare_info_about_computer_hash())
