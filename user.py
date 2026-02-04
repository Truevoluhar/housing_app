class user:
    id = 0
    first_name = ""
    last_name = ""
    failed_attempts = 0
    locked_out = 0
    email = ""
    password = ""
    user_type = ""
    session_time = ""
    active = 0


    def __init__(self,user_data):
        self.id = user_data[0]
        self.first_name = user_data[1]
        self.last_name = user_data[2]
        self.failed_attempts = user_data[3]
        self.locked_out = user_data[4]
        self.email = user_data[5]
        self.password = user_data[6]
        self.user_type = user_data[7]
        self.session_time = user_data[8]
        self.active = user_data[9]
