class User:
    def __init__(self, username, password='', role='user', blocked=0, pass_constraint=0):
        self.username = username
        self.password = password
        self.role = role
        self.blocked = blocked
        self.pass_constraint = pass_constraint

    def get_params(self):
        return self.username, self.password, self.role, self.blocked, self.pass_constraint

    def __repr__(self):
        return f'username={self.username}; password={self.password}; role={self.role}; ' \
               f'blocked={self.blocked}; pass_constraint={self.pass_constraint}'
