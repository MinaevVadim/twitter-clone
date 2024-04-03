from typing import List

from pydantic import BaseModel, Field


class ResultBase(BaseModel):
    result: bool = Field(default=True, example=True)


class ValidatorError(BaseModel):
    result: bool = Field(default=False, example=False)
    type: str = Field(example="type_error.str")
    msg: str = Field(example="str type expected")


class ResponseCreatedTweetBase(ResultBase):
    tweet_id: int = Field(example=1)


class FollowerOrAuthorBase(BaseModel):
    id: int = Field(example=1)
    name: str = Field(title="Follower name", example='Victor', max_length=50)


class TweetCreateBase(BaseModel):
    tweet_data: str = Field(title="Tweet content", example=1, max_length=250)
    tweet_media_ids: list[int] = Field(default=None, example=[3, 4, 5])


class ResponseMediaBase(ResultBase):
    media_id: int = Field(example=1)


class LikeBase(BaseModel):
    user_id: int = Field(example=1)
    name: str = Field(example='Veronika')


class TweetBase(BaseModel):
    id: int = Field(example=1)
    content: str = Field(example="Hello World")
    attachments: list = Field(default=None, example=["link_1", "link_2"])
    author: FollowerOrAuthorBase
    likes: List[LikeBase]


class TweetResponseBase(ResultBase):
    tweets: List[TweetBase]


class UserBase(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example='Alex')
    followers: List[FollowerOrAuthorBase]
    following: List[FollowerOrAuthorBase]


class UserResponseBase(ResultBase):
    user: UserBase


class ResponseErrorBase(BaseModel):
    message: str = Field(example="Error message")
