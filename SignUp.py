import json


def validate_name(name, password):
    with open('User/User.json', 'r') as json_file:
        data = json.loads(json_file.read())
    length = len(data)
    i = 0
    while i < length:
        if (data[i]['user_name'] == name):
            return False
        i += 1
    return True


def sign_up(name, password):
    if validate_name(name, password) == False:
        return False
    else:
        data = []
        with open('User/User.json', 'r') as json_file:
            data = json.loads(json_file.read())

        data.append(dict([("user_name", name), ("password", password)]))
        with open('User/User.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        return True
