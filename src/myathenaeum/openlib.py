import requests
import json

from datamodel import OpenLibAuthorAPI, OpenLibBookAPI, OpenLibWorkAPI
from cattrs import structure

class OpenLib:
    """Connection to the OpenLib API/Web page to retrieve information about books."""

    url = "https://openlibrary.org"
    headers = {
        "User-Agent": "MyAthenaeum/1.0 (danielhamj97@gmail.com)",
        # "Accept": "application.json"
    }

    def get_author(self, author_key: str) -> dict | None:
        author_url = self.url + author_key + ".json"
        response = requests.get(url=author_url, headers=self.headers)

        if response.status_code != 200:
            print(
                "Failed to retrieve auhtor! Response was %s with reason %s",
                response.status_code,
                response.reason,
            )
            return None

        author_api_data = json.loads(response.content.decode(encoding="utf-8"))

        return structure(author_api_data, OpenLibAuthorAPI)

    def get_work(self, work_key: str) -> dict | None:
        work_url = self.url + work_key + ".json"
        response = requests.get(url=work_url, headers=self.headers)

        if response.status_code != 200:
            print(
                "Failed to retrieve auhtor! Response was %s with reason %s",
                response.status_code,
                response.reason,
            )
            return None

        work_api_data = json.loads(response.content.decode(encoding="utf-8"))

        return structure(work_api_data, OpenLibWorkAPI)

    def get_book(self, isbn: str) -> dict | None:
        book_url = self.url + "/isbn/" + isbn + ".json"
        response = requests.get(url=book_url, headers=self.headers)

        if response.status_code != 200:
            print(
                "Failed to retrieve auhtor! Response was %s with reason %s",
                response.status_code,
                response.reason,
            )
            return None

        book_api_data = json.loads(response.content.decode(encoding="utf-8"))
        return structure(book_api_data, OpenLibBookAPI)


# OpenLib().get_author(author_key="/authors/OL34221A")
# print(OpenLib().get_work(work_key="/work/OL46347W"))
# print(OpenLib().get_book(isbn="9780008117535"))
