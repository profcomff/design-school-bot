from .base import Base
from pydantic import HttpUrl
from enum import Enum


class Year(str, Enum):
    FIRST = "1"
    SECOND = "2"
    THIRD = "3"
    FOURTH = "4"
    FIFTH = "1м"
    SIXTH = "2м"


class Directions(str, Enum):
    PHOTO = "PHOTO"
    CONTENT = "CONTENT"
    SOCIALWEBDESIGN = "SOCIALWEBDESIGN"
    IDENTICDESIGN = "IDENTICDESIGN"


class RequestTypes(str, Enum):
    TEXT = "text"
    VIDEO = "video"
    FILE = "file"


class UserPost(Base):
    union_id: str
    direction_id: int
    first_name: str
    middle_name: str
    last_name: str
    year: Year
    readme: str
    social_web_id: str


class UserPatch(Base):
    union_id: str | None
    direction_id: int | None
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    year: Year | None
    readme: str | None


class UserGet(Base):
    id: int
    union_id: str
    direction_id: int
    first_name: str
    middle_name: str
    last_name: str
    year: Year
    readme: str
    social_web_id: str
    folder_id: str


class SpamPost(Base):
    social_web_id: str


class SpamGet(SpamPost):
    id: int


class SpamGet(SpamPost):
    id: int


class VideoPost(Base):
    link: HttpUrl
    request: str | None
    direction_id: int
    request_type: RequestTypes | None


class VideoGet(VideoPost):
    id: int


class ResponsePost(Base):
    content: str | None


class ResponseGet(ResponsePost):
    id: int


class DirectionPost(Base):
    link: HttpUrl
    name: Directions


class DirectionGet(DirectionPost):
    id: int
