# User class, Changed name from User to Register
class Register:
    count_id = 0

    # initializer method
    def __init__(self, email_address, username, password, confirm_password):
        Register.count_id += 1
        self.__register_id = Register.count_id
        self.__email_address = email_address
        self.__username = username
        self.__password = password
        self.__confirm_password = confirm_password


    # accessor methods
    def get_register_id(self):
        return self.__register_id

    def get_email_address(self):
        return self.__email_address

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_confirm_password(self):
        return self.__confirm_password


    # mutator methods
    def set_register_id(self, register_id):
        self.__register_id = register_id

    def set_email_address(self, email_address):
        self.__email_address = email_address

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

    def set_confirm_password(self, confirm_password):
        self.__confirm_password = confirm_password


