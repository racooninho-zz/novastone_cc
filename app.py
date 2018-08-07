from flask import Flask, request, json, render_template, jsonify
import json as json_module
import uuid

import os

root_templates = os.path.join(os.path.dirname(__file__), "static/")

with open(root_templates + 'logins.json') as f:
    data_login = json_module.load(f)  # loads file with login details from logins.json

cookie_dict = {}  # Contains the cookies for each user
total_tasks = {}  # Needed to keep of how many tasks were added previously
todo_list = {}  # Contains all the tasks per user

app = Flask(__name__)
app.url_map.strict_slashes = False


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


@app.route('/login/', methods=['POST'])
def login():
    if request.method == 'POST':
        login_username = request.json['username']
        login_password = request.json['password']

        login_details = get_login_details(login_username)[0]

        if login_username == login_details['username'] and login_password == login_details['password']:
            my_id = uuid.uuid1()
            existing_cookie = create_cookie_dict(login_username, str(my_id))

            success_true = jsonify({"success": True})
            success_true.set_cookie('cookie_key', existing_cookie)

            return success_true
        else:
            return jsonify({"success": False})


@app.route('/logout/', methods=['GET'])
def logout():
    if request.method == 'GET':
        user_cookie = request.cookies.get('cookie_key')
        try:
            username = list(cookie_dict.keys())[list(cookie_dict.values()).index(user_cookie)]
            if username:
                success_true = jsonify({"success": True,
                                        "message": "logout successful"})
                create_cookie_dict(username, "")
                return success_true
        except:
            return jsonify({"success": False,
                            "message": "you are not an active user"})


@app.route("/<user>/todo/", methods=["GET"])
def todo(user):
    user_cookie = request.cookies.get('cookie_key')
    try:
        username = list(cookie_dict.keys())[list(cookie_dict.values()).index(user_cookie)]
    except:
        username = False

    if username == user:
        response = return_todo_list(username)
        if response:
            return jsonify(response)
        else:
            return jsonify({"message": "you have no tasks in the todo list"})
    else:
        success_false = jsonify({"success": False, "message": "please login first"})
        return success_false


@app.route("/<user>/todo/add/", methods=["POST"])
def todo_add(user):
    message = request.json['message']
    user_cookie = request.cookies.get('cookie_key')
    try:
        username = list(cookie_dict.keys())[list(cookie_dict.values()).index(user_cookie)]
    except:
        username = False

    if username == user:
        create_todo_list(username, message)

        response = jsonify({"success": True, "message": "task created"})
        return response
    else:
        response = jsonify({"success": False, "message": "please login"})
        return response


@app.route("/<user>/todo/complete/<id>", methods=["GET"])
def todo_complete(user, id):
    user_cookie = request.cookies.get('cookie_key')
    try:
        username = list(cookie_dict.keys())[list(cookie_dict.values()).index(user_cookie)]
    except:
        username = False

    if username == user:
        try:
            todo_list[username][int(id)]['completed'] = True
            response = jsonify({"success": True, "message": "task updated"})
            return response
        except:
            response = jsonify(
                {"success": False, "message": f"we could not find the comment id {id} for user {username}"})
            return response
    else:
        response = jsonify({"success": False, "message": "please login"})
        return response


@app.route("/<user>/todo/delete/<id>", methods=["GET"])
def todo_delete(user, id):
    user_cookie = request.cookies.get('cookie_key')
    try:
        username = list(cookie_dict.keys())[list(cookie_dict.values()).index(user_cookie)]
    except:
        username = False

    if username == user:
        try:
            del todo_list[username][int(id)]
            response = jsonify({"success": True, "message": "task deleted"})
            return response
        except:
            response = jsonify(
                {"success": False, "message": f"we could not find the comment id {id} for user {username}"})
            return response
    else:
        response = jsonify({"success": False, "message": "please login"})
        return response


if __name__ == '__main__':
    app.run(debug=True)
