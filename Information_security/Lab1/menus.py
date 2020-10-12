import os
import sys
import getpass
from db import db_get_user_by_username, db_update_user, db_select
from user import User


def cls():
    os.system('clear')


def show_all_users():
    cls()

    print('========= SHOW ALL USERS =========')
    users = db_select()

    for idx, user in enumerate(users):
        user = User(*user)
        print(f'{idx+1}.', user)

    print()
    _ = input('Press "enter" to continue...')


def print_change_password_menu(user: User, mistakes_cnt=3):
    cls()

    cnt = 0
    username = None
    while cnt < mistakes_cnt:
        if username is not None:
            print(f'We can\'t change password, because you have some mistakes. Please, try again.\n')

        print('========= CHANGE PASSWORD MENU =========')

        old_pass = input('Old password: ')
        new_pass = input('New password: ')
        repeat_new_pass = input('Repeat new password: ')

        if old_pass == user.password and new_pass == repeat_new_pass:
            fields = {'password': new_pass}
            db_update_user(user, fields)
            user.password = new_pass
            print('Password has been changed!\n')
            _ = input('Press "enter" to continue...')
            break
        else:
            cnt += 1
    else:
        _ = input(f'We can\'t change password, because you have some mistakes. Press "enter" to continue...')


def print_admin_menu(user: User):
    cls()
    print('========= ADMIN MENU =========')

    print('1. Change password')
    print('2. Show all users')
    print('3. Add new user')
    print('4. Block user')
    print('5. Edit password constraint')
    print('6. Back to GENERAL MENU')
    print('7. Exit')

    answer = None
    while True:
        if answer is not None:
            print('We can\'t find your input. Please, try again.\n')

        answer = input('Choose one of variant from menu: ')
        if answer == '1':
            print_change_password_menu(user)
            cls()
            break
        elif answer == '2':
            show_all_users()
            cls()
            break
        elif answer == '3':

            cls()
            break
        elif answer == '4':

            cls()
            break
        elif answer == '5':

            cls()
            break
        elif answer == '6':
            print_general_menu()
            cls()
            break
        elif answer == '7':
            sys.exit()

    print_admin_menu(user)


def print_user_menu(user: User):
    cls()
    print('========= USER MENU =========')
    print('1. Change password')
    print('2. Back to GENERAL MENU')
    print('3. Exit')

    answer = None
    while True:
        if answer is not None:
            print('We can\'t find your input. Please, try again.\n')

        answer = input('Choose one of variant from menu: ')
        if answer == '1':
            print_change_password_menu(user)
            cls()
            break
        elif answer == '2':
            print_general_menu()
            cls()
            break
        elif answer == '3':
            sys.exit()

    print_user_menu(user)


def print_login_menu(mistakes_cnt=3):
    cls()

    cnt = 0
    username = None
    while cnt < mistakes_cnt:
        if username is not None:
            print(f'We can\'t find "{username}" user with current password. Please, try again.\n')

        print('========= LOGIN MENU =========')

        username = input('Login: ')
        password = getpass.getpass('Password: ')

        user = db_get_user_by_username(username=username, password=password)

        if user is None:
            cnt += 1
        else:
            user = User(*user)
            if user.role == 'admin':
                print_admin_menu(user)
                cls()
                break
            elif user.role == 'user':
                print_user_menu(user)
                cls()
                break
            break
    else:
        print(f'We can\'t find "{username}" user with current password. Program was aborted!')

    print_general_menu()


def print_general_menu():
    cls()

    print('========= GENERAL MENU =========')
    print('1. Login menu')
    print('2. Exit')
    answer = None
    while True:
        if answer is not None:
            print('We can\'t find your input. Please, try again.\n')
        answer = input('Choose one of variant from menu: ')
        if answer == '1':
            print_login_menu()
            cls()
            break
        elif answer == '2':
            sys.exit()
    print_general_menu()
