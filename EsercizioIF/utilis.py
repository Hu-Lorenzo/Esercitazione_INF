import requests
def get_people_in_space():
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url)
    response.raise_for_status() 
    data = response.json()
    people = [{"name": person["name"], "craft": person["craft"]} for person in data.get("people", [])]
    return people
