from menus import print_general_menu
from db import db_creation, db_select


def main():
    db_creation()
    #print(db_select())
    #input()
    print_general_menu()


if __name__ == '__main__':
    main()
