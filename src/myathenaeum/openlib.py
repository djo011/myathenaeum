import requests
import json

from myathenaeum.datamodel import OpenLibAuthorAPI, OpenLibBookAPI, OpenLibWorkAPI, OpenLibBook
from cattrs import structure, Converter
from datetime import datetime, date


class OpenLib:
    """Connection to the OpenLib API/Web page to retrieve information about books."""

    url = "https://openlibrary.org"
    headers = {
        "User-Agent": "MyAthenaeum/1.0 (danielhamj97@gmail.com)",
        # "Accept": "application.json"
    }

    def get_author(self, author_key: str) -> OpenLibAuthorAPI | None:
        """
        Fetch author information using key value for author.

        The method fetches information about the author, structures the incoming json data to attrs class.

        Args:
            author_key (str): key value used by the openlib API.

        Returns:
            representation of author data using attrs class OpenLibAuthorAPI

            None if fetching data fails.
        """
        author_url = self.url + author_key + ".json"
        response = requests.get(url=author_url, headers=self.headers)

        if response.status_code != 200:  # TODO: Add more elegant exception handling.
            print(
                "Failed to retrieve auhtor! Response was %s with reason %s",
                response.status_code,
                response.reason,
            )
            return None

        author_api_data = json.loads(response.content.decode(encoding="utf-8"))

        return structure(author_api_data, OpenLibAuthorAPI)

    def get_work(self, work_key: str) -> OpenLibWorkAPI | None:
        """
        Fetch work information using key value for work.

        The method fetches information about the literary work, structures the incoming json data to attrs class.

        Args:
            work_key (str): key value for work used by the openlib API.

        Returns:
            representation of work data using attrs class OpenLibWorkAPI

            None if fetching data fails.
        """
        work_url = self.url + work_key + ".json"
        response = requests.get(url=work_url, headers=self.headers)

        if response.status_code != 200:  # TODO: Add more elegant exception handling.
            print(
                "Failed to retrieve auhtor! Response was %s with reason %s",
                response.status_code,
                response.reason,
            )
            return None

        work_api_data = json.loads(response.content.decode(encoding="utf-8"))

        return structure(work_api_data, OpenLibWorkAPI)

    def get_book(self, isbn: str) -> dict | None:
        """
        Fetch book information from OpenLib API using ISBN.

        The method fetches information about the book, structures the incoming json data to attrs class.

        Args:
            isbn (str): ISBN value for the book you would like to look up.

        Returns:
            representation of work data using attrs class OpenLibBookAPI

            None if fetching data fails.
        """
        book_url = self.url + "/isbn/" + isbn + ".json"
        response = requests.get(url=book_url, headers=self.headers)

        if response.status_code != 200:  # TODO: Add more elegant exception handling.
            print(
                "Failed to retrieve auhtor! Response was %s with reason %s",
                response.status_code,
                response.reason,
            )
            return None

        book_api_data = json.loads(response.content.decode(encoding="utf-8"))
        return structure(book_api_data, OpenLibBookAPI)

    def get_full_book_info(self, isbn: str) -> dict | None:
        """
        Fetch complete book information from OpenLib API using ISBN.

        The method fetches information about the book, using the previous methods.
        Different information is available at different routes in the API. Retrieves author and work key from the initial lookup using ISBN.
        Finally structures all information into attrs class representing data model used in database.

        Args:
            isbn (str): ISBN value for the book you would like to look up.

        Returns:
            representation of work data using attrs class OpenLibBook

        """
        book = self.get_book(isbn=isbn)

        author_key = book.authors[0]["key"]
        author = self.get_author(author_key=author_key)

        work_key = book.works[0]["key"]
        work = self.get_work(work_key=work_key)

        ol_book = {
            "id": book.isbn_10[0],
            "title": book.title,
            "author": author.name,
            "description": work.description,
            "publication_date": book.publish_date,
            "publisher": book.publishers[0],
        }

        c = Converter()
        c.register_structure_hook(date, lambda s, _: datetime.strptime(s, "%b %d, %Y").date())

        return c.structure(ol_book, OpenLibBook)
