import sys

import requests


API_KEY = 'dfe957a3'


def insert_to_db():
    raise NotImplementedError("Implement this function by yourself.")


if __name__ == "__main__":
    title='avatar'

    # Check if title is found in argument list. It's a validation.
    if not title:
        raise IndexError("No title entered!")

    # The request itself.
    response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}").json()
    if response:
        print(response)