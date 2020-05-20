import os

class ConfigData:
    def __init__(self):
        self.client_id = os.environ["CLIENT_ID"]
        self.secret_id = os.environ["SECRET_ID"]
        self.username = os.environ["USERNAME"]
        self.password = os.environ["PASSWORD"]
        print(f"{self.client_id=} {self.secret_id=} {self.username=} {self.password=}")