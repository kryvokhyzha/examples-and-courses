import os
import getpass


def cls():
    os.system('clear')


def print_login_menu():
    cls()
    print('========= LOGIN MENU =========')
    username = input('Login: ')
    password = getpass.getpass('Password: ')

    print(username, password)


def print_general_menu(mistakes_cnt=3):
    print('========= MENU =========')
    print('1. Login menu')
    print('2. Exit')
    cnt = 0
    while cnt < mistakes_cnt:
        answer = input('Choose one of variant from menu: ')
        if answer == '1':
            print_login_menu()
            break
        elif answer == '2':
            break
        else:
            cnt += 1
            print('We can\'t find your answer. Please, try again.')
