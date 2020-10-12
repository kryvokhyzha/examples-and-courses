import sqlite3 as sql
from typing import Dict
from user import User


def db_table_exists(db='users'):
    conn = sql.connect(f'{db}.db')
    cur = conn.cursor()

    cur.executescript(f'''
        SELECT name FROM sqlite_master 
        WHERE type = 'table' AND name = '{db}';
    ''')

    rows = cur.fetchall()

    conn.commit()
    conn.close()

    return True if rows else False


def db_creation(db='users'):
    if not db_table_exists():
        return

    conn = sql.connect(f'{db}.db')
    cur = conn.cursor()

    cur.executescript('''
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            blocked INTEGER NOT NULL,
            pass_constraint INTEGER NOT NULL 
        );
    ''')

    cur.executescript('''
            INSERT OR REPLACE INTO users (username, password, role, blocked, pass_constraint) 
            VALUES ('ADMIN', '', 'admin', 0, 0);
        ''')

    conn.commit()
    conn.close()


def db_select(db='users'):
    conn = sql.connect(f'{db}.db')
    cur = conn.cursor()

    cur.execute('''SELECT u.username, u.password, u.role, u.blocked, u.pass_constraint
                    FROM users as u''')
    rows = cur.fetchall()

    conn.commit()
    conn.close()

    return rows


def db_get_user_by_username(username='ADMIN', password='', db='users'):
    conn = sql.connect(f'{db}.db')
    cur = conn.cursor()

    cur.execute(f'''SELECT u.username, u.password, u.role, u.blocked, u.pass_constraint 
                   FROM users as u
                   WHERE u.username="{username}" and u.password="{password}"''')
    row = cur.fetchone()

    conn.commit()
    conn.close()

    return row


def db_update_user(user: User, fields: Dict, db='users'):
    conn = sql.connect(f'{db}.db')
    cur = conn.cursor()

    cur.execute(f'''UPDATE users
                    SET password = "{fields['password'] if 'password' in fields else user.password}",
                        role = "{fields['role'] if 'role' in fields else user.role}",
                        blocked = {fields['blocked'] if 'blocked' in fields else user.blocked},
                        pass_constraint = {fields['pass_constraint'] if 'pass_constraint' in fields else user.pass_constraint}
                    WHERE username="{user.username}" and password="{user.password}"''')

    conn.commit()
    conn.close()
