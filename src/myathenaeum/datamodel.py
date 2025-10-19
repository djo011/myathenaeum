from attrs import define, field
from datetime import date


@define
class OpenLibAuthorAPI:
    name: str
    bio: dict
    entity_type: str
    birth_date: str
    personal_name: str
    remote_ids: dict
    source_records: list
    photos: list
    death_date: str
    type: dict
    title: str
    alternate_names: list
    role: str
    links: list
    key: str
    latest_revision: int
    revision: int
    created: dict
    last_modified: dict


@define
class OpenLibWorkAPI:
    description: str
    title: str
    covers: list[int]
    subject_places: list[str]
    subjects: list[str]
    subject_people: list[str]
    key: str
    authors: list[dict]
    type: dict
    latest_revision: int
    revision: int
    created: dict
    last_modified: dict
    links: list[dict] = field(default=[])


@define
class OpenLibBookAPI:
    publishers: list[str]
    source_records: list[str]
    title: str
    covers: list[int]
    publish_date: str
    key: str
    authors: list[dict]
    works: list[dict]
    type: dict
    isbn_10: list[str]
    isbn_13: list[str]
    lc_classifications: list[str]
    latest_revision: int
    revision: int
    created: dict
    last_modified: dict
    identifiers: dict = field(default={})
    classifications: dict = field(default={})


@define
class OpenLibBook:
    id: int
    title: str
    author: str
    description: str
    publication_date: date
    publisher: str
