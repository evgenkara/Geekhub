import requests
from pprint import pprint


def user_info(user_id):
    r = requests.get("https://jsonplaceholder.typicode.com/users")
    max_id = max(r.json(), key=lambda item: item['id'])
    if 1 <= user_id <= max_id["id"]:
        for user in r.json():
            if user["id"] == user_id:
                pprint(user, sort_dicts=False)
    else:
        print("Wrong id")


inp_id = int(input("Enter id: "))
user_info(inp_id)
