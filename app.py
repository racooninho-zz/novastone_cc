from flask import Flask, request, jsonify
import uuid
import utils


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/login/', methods=['POST'])
def login():
    if request.method == 'POST':
        login_username = request.json['username']
        login_password = request.json['password']

        login_details = utils.get_login_details(login_username)[0]

        if login_username == login_details['username'] and login_password == login_details['password']:
            my_id = uuid.uuid1()
            existing_cookie = utils.create_cookie_dict(login_username, str(my_id))

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
            username = list(utils.cookie_dict.keys())[list(utils.cookie_dict.values()).index(user_cookie)]
            if username:
                success_true = jsonify({"success": True,
                                        "message": "logout successful"})
                utils.create_cookie_dict(username, "")
                return success_true
        except:
            return jsonify({"success": False,
                            "message": "you are not an active user"})


@app.route("/<user>/todo/", methods=["GET"])
def todo(user):
    user_cookie = request.cookies.get('cookie_key')
    try:
        username = list(utils.cookie_dict.keys())[list(utils.cookie_dict.values()).index(user_cookie)]
    except:
        username = False

    if username == user:
        response = utils.return_todo_list(username)
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
        username = list(utils.cookie_dict.keys())[list(utils.cookie_dict.values()).index(user_cookie)]
    except:
        username = False

    if username == user:
        utils.create_todo_list(username, message)

        response = jsonify({"success": True, "message": "task created"})
        return response
    else:
        response = jsonify({"success": False, "message": "please login"})
        return response


@app.route("/<user>/todo/complete/<id>", methods=["GET"])
def todo_complete(user, id):
    user_cookie = request.cookies.get('cookie_key')
    try:
        username = list(utils.cookie_dict.keys())[list(utils.cookie_dict.values()).index(user_cookie)]
    except:
        username = False

    if username == user:
        try:
            utils.todo_list[username][int(id)]['completed'] = True
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
        username = list(utils.cookie_dict.keys())[list(utils.cookie_dict.values()).index(user_cookie)]
    except:
        username = False

    if username == user:
        try:
            del utils.todo_list[username][int(id)]
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
