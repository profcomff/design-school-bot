from .base import Base
from enum import Enum
from pydantic import HttpUrl


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
    union_id: int
    direction_id: int
    first_name: str
    middle_name: str
    last_name: str
    year: Year
    readme: str
    social_web_id: str


class UserGet(UserPost):
    id: int


class SpamPost(Base):
    social_web_id: str


class SpamGet(SpamPost):
    id: int


class VideoPost(Base):
    link: HttpUrl
    request: str | None
    direction_id: int
    request_type: RequestTypes


class VideoGet(VideoPost):
    id: int


class ResponsePost(Base):
    content: str | None
    video_id: int
    user_id: int


class ResponseGet(ResponsePost):
    id: int


class DirectionPost(Base):
    link: HttpUrl
    name: Directions


class DirectionGet(DirectionPost):
    id: int

