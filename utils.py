import json as json_module
import os

cookie_dict = {}  # Contains the cookies for each user
total_tasks = {}  # Needed to keep of how many tasks were added previously
todo_list = {}  # Contains all the tasks per user

root_templates = os.path.join(os.path.dirname(__file__), "static/")

with open(root_templates + 'logins.json') as f:
    data_login = json_module.load(f)  # loads file with login details from logins.json


def get_login_details(username):
    result = filter(lambda details: details['username'] == username, data_login['logins'])
    return list(result)


def create_cookie_dict(username, cookie_secret):
    # logout case
    if cookie_secret == '':
        del cookie_dict[username]

    # after login
    if username in cookie_dict:
        return cookie_dict[username]

    # during login
    if username not in cookie_dict and cookie_secret != "":
        cookie_dict[username] = cookie_secret
        return cookie_secret


def create_todo_list(username, message):
    try:
        if todo_list[username]:
            total_tasks[username] += 1
            todo_list[username][int(total_tasks[username])] = \
                {'username': username, 'message': message, 'completed': False}
            return True

    # will fall to except when there is no task for the username
    except:
        todo_list[username] = {}
        todo_list[username][int(1)] = {'username': username, 'message': message, 'completed': False}
        total_tasks[username] = 1
        return True


def return_todo_list(username):
    try:
        if todo_list[username]:
            return todo_list[username]
    except:
        return False