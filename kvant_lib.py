import json

def create_user(id, fio, birthdate, password, my_id, my_password):
    command = {
        "id": id,
        "fio": fio,
        "birthdate": birthdate,
        "password": password
    }

    return form_command(my_id, my_password, command, "CreateUser")

def delete_user(id, my_id, my_password):
    command = {
        "id": id
    }

    return form_command(my_id, my_password, command, "DeleteUser")

def change_balance(amount, of, for_what, my_id, my_password):
    command = {
        "amount": amount,
        "of": of,
        "for_what": for_what
    }

    return form_command(my_id, my_password, command, "ChangeBalance")

def change_password(of, to, my_id, my_password):
    command = {
        "of": of,
        "to": to
    }

    return form_command(my_id, my_password, command, "ChangePassword")

def form_command(my_id, my_password, command: dict, type_):
    wrapper = {
        "command": {
            type_: command
        },
        "my_id": my_id,
        "my_password": my_password
    }

    return json.dumps(wrapper)
