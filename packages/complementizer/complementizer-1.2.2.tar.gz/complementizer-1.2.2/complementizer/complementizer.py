import requests
from complementizer import Form

class Complementizer:
    
    def __init__(self, url_base: str, username: str, password: str, has_token: bool = False, path_auth: str = ''):
        self.url_base: str = url_base
        self.username: str = username
        self.password: str = password
        self.has_token: bool = has_token
        
        if self.has_token:
            response = requests.post(url_base + path_auth, data = {
                'username': username,
                'password': password,
            })
            self.token = response.json()['token']        
        
    def createForm(self, table: str):
        self.form = Form(table,complementizer=self)
        return self.form
            
    def populate(self, endpoint):
        generate = self.form.generate()
        print(self.form.table.upper(), '=>' , generate)
        response = requests.post(self.url_base + endpoint, data = generate, headers = { 'Authorization': 'Token ' + self.token })
        print('\nRESPONSE')
        print(response.json())
        print('========\n')