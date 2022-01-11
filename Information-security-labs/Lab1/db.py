import sqlite3 as sql
from typing import Dict
from user import User


def db_creation(db='users'):
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

    cur.execute(f'''
        SELECT username FROM users 
        WHERE username = "ADMIN";
    ''')

    row = cur.fetchone()

    if not row:
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


def db_get_user_by_username(username='ADMIN', db='users'):
    conn = sql.connect(f'{db}.db')
    cur = conn.cursor()

    cur.execute(f'''SELECT u.username, u.password, u.role, u.blocked, u.pass_constraint 
                   FROM users as u
                   WHERE u.username="{username}"''')
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


def db_add_new_user(user: User, db='users'):
    conn = sql.connect(f'{db}.db')
    cur = conn.cursor()

    cur.execute(f'''
        SELECT username FROM users 
        WHERE username = "{user.username}";
    ''')

    row = cur.fetchone()

    if row is not None or user.username == '':
        conn.commit()
        conn.close()
        return False

    cur.execute('''
            INSERT OR REPLACE INTO users (username, password, role, blocked, pass_constraint) 
            VALUES (?, ?, ?, ?, ?);
        ''', user.get_params())

    conn.commit()
    conn.close()
    return True
