import requests
import json


def registration(domen, name, phone: str, telegram):
    """ Registration in the system (allow any) """

    url = domen + 'api/registration'
    data = {
        'first_name': name,
        'phone': phone,
        'telegram': telegram
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=url, headers=headers, data=json.dumps(data))
    if response:
        return json.loads(response.content)
    else:
        return json.loads(response.content)


def delete_user(domen, phone, telegram, del_username):
    """ Delete user (admin only) """

    user_list = get_student_list(domen, phone, telegram)
    for user in user_list:
        if user['username'] == del_username:
            user_id = user['id']
            break
    if 'user_id' not in locals():
        return ('User id not found')
    url = domen + 'api/delete-user/' + f"{user_id}/"
    token = 'Token ' + get_token(domen, phone, telegram)
    headers = {'Authorization': token}
    response = requests.delete(url=url, headers=headers)
    if response:
        return True
    else:
        return False


def get_token(domen, phone, telegram):
    """ Get token (authorized only) """

    url = domen + 'api/get-token'
    data = {
        'phone': phone,
        'telegram': telegram
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=url, headers=headers, data=json.dumps(data))
    if response:
        token = json.loads(response.content)['access']
        return token
    else:
        return "Username or password is not correct"


def get_student_list(domen, phone, telegram):
    """ Get list of all student (admin only) """

    url = domen + 'api/get-users'
    token = 'Token ' + get_token(domen, phone, telegram)
    headers = {'Authorization': token}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 401:
        return "Username or password is not correct"
    elif response.status_code == 403:
        return "You don't have access"
    elif response:
        users_list = json.loads(response.content)
        return users_list
    else:
        return "Error"


def get_all_lessons(domen, phone, telegram):
    """ Get list of all lessons including past ones (admin only) """

    url = domen + 'api/all-lessons'
    token = 'Token ' + get_token(domen, phone, telegram)
    headers = {'Authorization': token}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 401:
        return "Username or password is not correct"
    elif response.status_code == 403:
        return "You don't have access"
    elif response:
        all_lessons = json.loads(response.content)
        return all_lessons
    else:
        return "Error"


def get_relevant_lessons(domen):
    """ Get list of relevant lessons (allow any) """

    url = domen + 'api/get-relevant-lessons'
    response = requests.get(url=url)
    if response:
        all_relevant_lessons = json.loads(response.content)
        return all_relevant_lessons
    else:
        return 'Error'


def convert_lessons_to_dict(lesson_list: list) -> dict:
    """ Convert a list of lessons to a dict (allow any) """

    lesson_dict = {}
    for lesson in lesson_list:
        if lesson['date'] in lesson_dict:
            lesson_dict[lesson['date']].append(lesson)
        else:
            lesson_dict[lesson['date']] = [lesson]
    return lesson_dict


def create_lesson(domen, phone, telegram, data: dict, admin: bool):
    """ Create new lesson (authorized or admin only) """

    if admin:
        url = domen + 'api/all-relevant-lessons/'
        # data = {'student': *, 'theme': *,
        #         'salary': *, 'time': *, 'date': *}
    else:
        url = domen + 'api/set-my-lessons/'
        # data = {'theme': *, 'salary': *, 'time': *, 'date': *}
    token = 'Token ' + get_token(domen, phone, telegram)
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    response = requests.post(url=url, headers=headers, data=json.dumps(data))
    return json.loads(response.content)


def update_lesson(domen, phone, telegram, data: dict, admin: bool):
    """ Update lesson (authorized or admin only) """

    if admin:
        url = domen + 'api/all-relevant-lessons/' + f"{data['id']}/"
        # data = {'id': *, 'student': *, 'theme': *,
        #         'salary': *, 'time': *, 'date': *}
    else:
        url = domen + 'api/set-my-lessons/' + f"{data['id']}/"
        # data = {'id': *, 'theme': *, 'salary': *, 'time': *, 'date': *}
    token = 'Token ' + get_token(domen, phone, telegram)
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    response = requests.put(url=url, headers=headers, data=json.dumps(data))
    return json.loads(response.content)


def delete_lesson(domen, phone, telegram, data: dict, admin: bool):
    """ Delete lesson (authorized or admin only) """

    if admin:
        url = domen + 'api/all-relevant-lessons/' + f"{data['id']}/"
        # data = {'id': *, 'student': *, 'theme': *,
        #         'salary': *, 'time': *, 'date': *}
    else:
        url = domen + 'api/set-my-lessons/' + f"{data['id']}/"
        # data = {'id': *, 'theme': *, 'salary': *, 'time': *, 'date': *}
    token = 'Token ' + get_token(domen, phone, telegram)
    headers = {'Authorization': token}
    response = requests.delete(url=url, headers=headers, data=json.dumps(data))
    if response:
        return True
    else:
        return False


def get_my_lessons(domen, phone, telegram):
    """ Get list of own relevant lesson (authorized only) """

    url = domen + 'api/set-my-lessons'
    token = 'Token ' + get_token(domen, phone, telegram)
    headers = {'Authorization': token}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 401:
        return "Username or password is not correct"
    elif response:
        onw_relevant_lessons = json.loads(response.content)
        return onw_relevant_lessons
    else:
        return "Error"


def get_timeblock_list(domen):
    """ Getting timeblock list (allow any) """

    url = domen + 'api/get-timeblocks'
    response = requests.get(url=url)
    if response:
        timeblocks = json.loads(response.content)
        return timeblocks
    else:
        return 'Error'
