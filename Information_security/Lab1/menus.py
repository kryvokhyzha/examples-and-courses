import os
import sys
import getpass
import re
from db import db_get_user_by_username, db_update_user, db_select, db_add_new_user
from user import User
from math import fabs


def cls():
    os.system('clear')


def print_edit_pass_constr_menu():
    cls()

    print('========= ADD/REMOVE PASSWORD CONSTRAINTS =========')

    while True:
        username = input('Enter username: ')

        user = db_get_user_by_username(username)

        print()
        if user:
            user = User(*user)
            db_update_user(user, {'pass_constraint': fabs(user.pass_constraint - 1)})
            user.pass_constraint = fabs(user.pass_constraint - 1)
            if user.pass_constraint == 0:
                _ = input('Constraint has been removed! Press "enter" to continue...')
            else:
                _ = input('Constraint has been added! Press "enter" to continue...')
            break
        else:
            answer = input('User doesn`t exist! Press "enter" to try again or "q" to quite... ')
            print()
            if answer.lower() == 'q':
                return


def print_block_user_menu():
    cls()

    print('========= BLOCK/UNBLOCK USER =========')
    while True:
        username = input('Enter username: ')

        user = db_get_user_by_username(username)

        print()
        if user:
            user = User(*user)
            if user.role == 'admin':
                print('You can`t block admin user! Please, try again.\n')
                continue
            db_update_user(user, {'blocked': fabs(user.blocked - 1)})
            user.blocked = fabs(user.blocked - 1)
            if user.blocked == 0:
                _ = input('User has been unblocked! Press "enter" to continue...')
            else:
                _ = input('User has been blocked! Press "enter" to continue...')
            break
        else:
            answer = input('User doesn`t exist! Press "enter" to try again or "q" to quite... ')
            print()
            if answer.lower() == 'q':
                return


def print_add_new_user_menu():
    cls()

    print('========= ADD NEW USER =========')
    while True:
        username_new = input('Enter username for new user: ')

        res = db_add_new_user(User(username=username_new))

        print()
        if res:
            _ = input('User has been created! Press "enter" to continue...')
            break
        else:
            answer = input('Username is empty or user already exists! Press "enter" to try again or "q" to quite... ')
            print()
            if answer.lower() == 'q':
                return


def print_show_all_users_menu():
    cls()

    print('========= SHOW ALL USERS =========')
    users = db_select()

    for idx, user in enumerate(users):
        user = User(*user)
        print(f'{idx+1}.', user)

    print()
    _ = input('Press "enter" to continue...')


def check_password_constraints(password):
    return False if len(password) == len(re.sub(r'[^a-zA-Zа-яА-ЯёЁіІ+-/*/]', '', password)) else True


def print_change_password_menu(user: User, mistakes_cnt=3):
    cls()

    print('========= CHANGE PASSWORD MENU =========')

    cnt = 0
    while cnt < mistakes_cnt:
        if cnt > 0:
            answer = input(f'We can\'t change password, because you have some mistakes. '
                           f'Press "enter" to try again or "q" to quite...')
            print()
            if answer.lower() == 'q':
                return

        if user.pass_constraint == 1:
            print('Your password constraints: Latin letters, Cyrillic symbols and signs of arithmetic operations')
        old_pass = input('Old password: ')
        new_pass = input('New password: ')
        repeat_new_pass = input('Repeat new password: ')

        if check_password_constraints(new_pass) and user.pass_constraint == 1:
            cnt += 1
            continue

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
            print_show_all_users_menu()
            cls()
            break
        elif answer == '3':
            print_add_new_user_menu()
            cls()
            break
        elif answer == '4':
            print_block_user_menu()
            cls()
            break
        elif answer == '5':
            print_edit_pass_constr_menu()
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

    print('========= LOGIN MENU =========')

    cnt = 0
    username = None
    while cnt < mistakes_cnt:
        if username is not None:
            answer = input(f'We can\'t find "{username}" user with current password.'
                           f' Press "enter" to try again or "q" to quite... ')
            print()
            if answer.lower() == 'q':
                return

        username = input('Login: ')
        password = getpass.getpass('Password: ')

        user = db_get_user_by_username(username=username)

        if user is None:
            cnt += 1
            continue

        user = User(*user)
        if user.password != password:
            cnt += 1
            continue

        if user.blocked == 1:
            answer = input(f'User "{username}" has been blocked! Press "enter" to try again or "q" to quite... ')
            username = None
            print()
            if answer.lower() == 'q':
                return
            else:
                continue

        if user.role == 'admin':
            print_admin_menu(user)
            cls()
            break
        elif user.role == 'user':
            print_user_menu(user)
            cls()
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
