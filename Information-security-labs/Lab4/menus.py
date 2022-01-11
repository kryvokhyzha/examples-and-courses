# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.5 (default, Apr 19 2020, 20:18:17) 
# [GCC 9.2.1 20191008]
# Embedded file name: menus.py
import os, sys, getpass, re
from math import fabs
from db import db_get_user_by_username, db_update_user, db_select, db_add_new_user
from user import User
from draw_table import top_rule, fmt_row, bot_rule, mid_rule

def cls():
    command = 'clear' if sys.platform == 'linux' else 'cls'
    os.system(command)


def print_edit_pass_constr_menu():
    cls()
    print('========= ADD/REMOVE PASSWORD CONSTRAINTS =========')
    while 1:
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
    while 1:
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
    while 1:
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
    print('\n**Please, use full-screen**\n')
    users = db_select()
    users.insert(0, ('username', 'password', 'role', 'blocked', 'pass_constraint'))
    num_cols = len(users[0])
    length_list = [len(str(element)) for row in users for element in row]
    column_width = max(length_list) + 2
    print(top_rule(column_width, num_cols))
    for row in users[:-1]:
        print(fmt_row(row, column_width, 1))
        print(mid_rule(column_width, num_cols))

    print(fmt_row(users[(-1)], column_width, 1))
    print(bot_rule(column_width, num_cols))
    print()
    _ = input('Press "enter" to continue...')


def check_password_constraints(password):
    if len(re.sub('[a-zA-Z]', '', password)) < len(password):
        if len(re.sub('[а-яА-ЯёЁіІ]', '', password)) < len(password):
            if len(re.sub('[+-/*/]', '', password)) < len(password):
                return False
    return True


def print_change_password_menu(user: User, mistakes_cnt=3):
    cls()
    print('========= CHANGE PASSWORD MENU =========')
    cnt = 0
    while cnt < mistakes_cnt:
        if cnt > 0:
            answer = input('We can\'t change password, because you have some mistakes. Press "enter" to try again or "q" to quite...')
            print()
            if answer.lower() == 'q':
                return
        else:
            if user.pass_constraint == 1:
                print('Your password constraints: Latin letters, Cyrillic symbols and signs of arithmetic operations')
            old_pass = input('Old password: ')
            new_pass = input('New password: ')
            repeat_new_pass = input('Repeat new password: ')
            if check_password_constraints(new_pass):
                if user.pass_constraint == 1:
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
        _ = input('We can\'t change password, because you have some mistakes. Press "enter" to continue...')


def print_admin_menu(user: User):
    cls()
    print('========= ADMIN MENU =========')
    print('1. Change password')
    print('2. Show all users')
    print('3. Add new user')
    print('4. Block/Unblock user')
    print('5. Add/remove password constraints')
    print('6. Back to GENERAL MENU')
    print('7. Exit')
    answer = None
    while 1:
        if answer is not None:
            print("We can't find your input. Please, try again.\n")
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
        else:
            if answer == '5':
                print_edit_pass_constr_menu()
                cls()
                break
            else:
                if answer == '6':
                    print_general_menu()
                    cls()
                    break
                else:
                    if answer == '7':
                        sys.exit()

    print_admin_menu(user)


def print_user_menu(user: User):
    cls()
    print('========= USER MENU =========')
    print('1. Change password')
    print('2. Back to GENERAL MENU')
    print('3. Exit')
    answer = None
    while 1:
        if answer is not None:
            print("We can't find your input. Please, try again.\n")
        answer = input('Choose one of variant from menu: ')
        if answer == '1':
            print_change_password_menu(user)
            cls()
            break
        else:
            if answer == '2':
                print_general_menu()
                cls()
                break
            else:
                if answer == '3':
                    sys.exit()

    print_user_menu(user)


def print_login_menu(mistakes_cnt=3):
    cls()
    print('========= LOGIN MENU =========')
    cnt = 0
    username = None
    
    while cnt < mistakes_cnt:
        # модифікована частина
        cnt = 0
        if username is not None:
            answer = input(f"""We can\'t find "{username}" user with current password. Press "enter" to try again or "q" to quite... """)
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
        print(f"""We can\'t find "{username}" user with current password. Program was aborted!""")

    print_general_menu()


def print_information_about_author():
    cls()
    print('========= INFORMATION ABOUT AUTHOR =========')
    print()
    print('Author: Roman Kryvokhyzha')
    print('Group: IS-72')
    print('Individual task 11: Latin letters, Cyrillic symbols and signs of arithmetic operations')
    print('Admin username: ADMIN')
    print()
    _ = input('Press "enter" to continue...')


def print_general_menu():
    cls()
    print('========= GENERAL MENU =========')
    print('1. Login menu')
    print('2. README')
    print('3. Exit')
    answer = None
    while 1:
        if answer is not None:
            print("We can't find your input. Please, try again.\n")
        answer = input('Choose one of variant from menu: ')
        if answer == '1':
            print_login_menu()
            cls()
            break
        else:
            if answer == '2':
                print_information_about_author()
                cls()
                break
            else:
                if answer == '3':
                    sys.exit()

    print_general_menu()
# okay decompiling menus.pyc
