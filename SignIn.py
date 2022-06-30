import json


def sign_in(username, password):
    with open('User/User.json', 'r') as json_file:
        data = json.loads(json_file.read())
    length = len(data)
    i = 0
    while i < length:
        if (data[i]['user_name'] == username):
            if (data[i]['password'] == password):
                return True
            return False
        i += 1
    return False
