

from flask import Blueprint
from  forms import TextField, Form
from validators import validate_username


class LoginForm(Form):
    def __init__(self):
        super().__init__(
        'login',
        [
            TextField('username', 'Username', validate_username),
            TextField('password', 'Password')
        ],
        )
    
    def handle_submit(self,form_data):
        print(form_data)
        return 'Login successful!'
    
