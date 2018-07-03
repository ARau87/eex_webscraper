class Config():

    def __init__(self, path, **kwargs):
        
        self.path = path

        self.read(self.path)

    def read(self, path):

        with open(path, 'r') as file:
            data = file.read()
            data = data.split('\n')
            
            for option in data:
                option = option.split('=')
                option = (option[0].strip(), option[1].strip())

                if option[0] == 'driver':
                    self.driver = option[1]

                if option[0] == 'driver_executable':
                    self.driver_executable = option[1]

                if option[0] == 'time':
                    self.time = option[1]
                
                if option[0] == 'os':
                    self.os = option[1]

                if option[0] == 'save_path':
                    self.save_path = option[1]

                if option[0] == 'email_server':
                        self.email_server = option[1]

                if option[0] == 'email_server_port':
                        self.email_server_port = int(option[1])

                if option[0] == 'email_user':
                    self.email_user = option[1]
                
                if option[0] == 'email_password':
                    self.email_password = option[1]

                if option[0] == 'email_receiver':
                    self.email_receiver = option[1]

                if option[0] == 'weather_api_key':
                    self.weather_api_key = option[1]

    def print_options(self):

        print('Driver:', self.driver)
        print('Driver Executable', self.driver_executable)
        print('Time:', self.time)
        print('OS:', self.os)
        print('Save Path:', self.save_path)