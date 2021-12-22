import requests

r = requests.get("https://jsonplaceholder.typicode.com/users")

for user in r.json():
    print(f"id: {user['id']}, name: {user['name']}, username: {user['username']}")
