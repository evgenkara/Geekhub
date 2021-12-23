import requests
import random
import sys


def wrapper(func):
    def wrap(*args, **kwargs):
        size = 60
        result = func(*args, **kwargs)
        print('-' * size)
        return result
    return wrap


def print_json(data, indent=0):
    for key, value in data.items():
        if isinstance(value, dict):
            print('\t' * indent + f"{key}:")
            print_json(value, indent + 1)
        else:
            print("\t" * indent + f"{key}: {value}")


def get_users():
    r = requests.get("https://jsonplaceholder.typicode.com/users")
    for user in r.json():
        print(f"id: {user['id']}, name: {user['name']}, username: {user['username']}")


def validate_user(user_id):
    r = requests.get("https://jsonplaceholder.typicode.com/users")
    max_id = max(r.json(), key=lambda item: item['id'])
    valid = False
    if 1 <= user_id <= max_id["id"]:
        valid = True
    return valid


def user_info(user_id):
    r = requests.get("https://jsonplaceholder.typicode.com/users")
    for user in r.json():
        if user["id"] == user_id:
            print_json(user)


def user_posts(user_id):
    while True:
        option = input("Choose action:\n1. Get user posts\n2. Get post by id\n3. Back to main menu\n: ")
        if option == '1':
            r = requests.get("https://jsonplaceholder.typicode.com/posts", {'userId': user_id})
            for post in r.json():
                print(f"id: {post['id']}  title: {post['title']}")
        elif option == '2':
            post_id = int(input("Enter post id: "))
            posts = requests.get("https://jsonplaceholder.typicode.com/posts", {'id': post_id})
            comments = requests.get("https://jsonplaceholder.typicode.com/comments", {'postId': post_id})
            comment_ids = []
            for post in posts.json():
                for comment in comments.json():
                    comment_ids.append(comment["id"])
                result = {'id': post['id'], 'title': post['title'], 'text': post['body'],
                          'comments': len(comment_ids), 'comment_ids': comment_ids}
                for key, val in zip(result.keys(), result.values()):
                    print(f"{key}: {val}")
        elif option == '3':
            break
        else:
            print("Wrong input")


def todo_list(user_id):
    option = input("Choose action:\n1. Get uncompleted tasks\n2. Get completed tasks\n: ")
    if option == '1':
        uncompleted = []
        req = requests.get("https://jsonplaceholder.typicode.com/todos", {"userId": user_id, "completed": "false"})
        for task in req.json():
            uncompleted.append(task["title"])
        return uncompleted
    elif option == '2':
        completed = []
        req = requests.get("https://jsonplaceholder.typicode.com/todos", {"userId": user_id, "completed": "true"})
        for task in req.json():
            completed.append(task["title"])
        return completed


def get_url(user_id):
    albums = []
    for album in requests.get("https://jsonplaceholder.typicode.com/albums", {"userId": user_id}).json():
        albums.append(album["id"])
    img_ids = []
    imgs = requests.get("https://jsonplaceholder.typicode.com/photos")
    for image in imgs.json():
        if image["albumId"] in albums:
            img_ids.append(image["id"])
    rand_id = random.choice(img_ids)
    for img in imgs.json():
        if img['id'] == rand_id:
            return img['url']


@wrapper
def user_menu(user_id):
    action = input("Choose action:\n1. Get user info\n2. Get posts\n3. Get ToDo list\n4. Get picture URL\n"
                   "5. Exit\n: ")
    if action == "1":
        user_info(user_id)
    elif action == "2":
        user_posts(user_id)
    elif action == "3":
        try:
            count = 1
            for todo in todo_list(user_id):
                print(f"{count}) {todo}")
                count += 1
        except TypeError:
            print("Wrong input")
    elif action == "4":
        print(get_url(user_id))
    elif action == "5":
        sys.exit()
    else:
        print("Wrong input. Please, try again")
        user_menu(user_id)


def start():
    print("Available users: ")
    get_users()
    user = int(input("Enter user id: "))
    if validate_user(user):
        while True:
            user_menu(user)
    else:
        print("Wrong id. Please, try again")
        start()


start()
