class Command:
    def __init__(self, state, text):
        self.state = state
        self.text = text


class State:
    def __init__(self):
        self.commands = []

    def algorithm(self):
        pass

    def get_function(self, text):
        for command in self.commands:
            if command.text == text or command.text == '':
                MainMenu.set_state(command.state)
                return True


class MainState(State):
    def __init__(self):
        super().__init__()
        self.commands = [Command(LoginState, 'login')]        
        
    def start(self):
        print("Здравствуйте! Сейчас вы в главном меню. 1: регистрация, 2: вход, 3: помощь")

        function = None

        while not function:
            command = input()
            function = self.get_function(command)

        return


class LoginState(State):
    def __init__(self):
        super().__init__()

    def start(self):
        print('Введите логин:')
        login = input()
        
        if function := self.get_function(login):
            return
        
        print('Введите пароль:')

        password = input()
        if function := self.get_function(password):
            return

        print('Вы успешно вошли!')
        MainMenu.set_state(LoggedState)


class LoggedState(State):
    def __init__(self):
        super().__init__()
        self.commands.append(Command(MainState, 'logout'))

    def start(self):
        while True:
            command = input()

            if function := self.get_function(command):
                return


class Menu:
    def __init__(self):
        pass

    def set_state(self, state):
        self.state = state()
        
    def start(self):
        while True:
            self.state.start()



MainMenu = Menu()
MainMenu.set_state(MainState)
MainMenu.start()





