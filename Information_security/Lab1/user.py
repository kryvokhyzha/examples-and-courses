class User:
    def __init__(self, username, password, role, blocked, pass_constraint):
        self.username = username
        self.password = password
        self.role = role
        self.blocked = blocked
        self.pass_constraint = pass_constraint

    def __repr__(self):
        return f'username={self.username}; password={self.password}; role={self.role}; ' \
               f'blocked={self.blocked}; pass_constraint={self.pass_constraint}'
