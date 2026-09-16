import firebase


class User:
    def __init__(self):
        self.name = ""
        self.password = ""
        self.authorized = False

    def auth_try(self, name, password):
        """Authenticate user by his name and password. if True user is authenticated, else False

        Args:
            name (string): user name
            password (string): user password

        Returns:
            bool: True if user is authenticated, False otherwise
        """
        userF = firebase.find_user_by_name(name)

        if userF and userF.get("name") == name and userF.get("password") == password:
            self.name = name
            self.password = password
            self.authorized = True
            return True
        else:
            return False


    def register_user(self, name, password, confirm_password):
        """Register user by his name and password. if True user is registered, else False

        Args:
            name (string): user name
            password (string): user password
            confirm_password (string): confirm password

        Returns:
            bool: True if user is registered, False otherwise
        """
        if password != confirm_password:
            return "Password and confirm password do not match"

        userF = firebase.find_user_by_name(name)
        if userF:
            return "User already exists"
            

        firebase.create_user(name, password)
        self.name = name
        self.password = password
        self.authorized = True
        return True
    