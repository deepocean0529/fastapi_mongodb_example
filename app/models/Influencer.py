from typing import Annotated, List, Optional
from pydantic import BaseModel, BeforeValidator, Field

TABLE_NAME_INFLUENCER = "influencers"

PydanticObjectId = Annotated[str, BeforeValidator(str)]


class Influencer(BaseModel):
    """
    Influencer create model
    """

    id: Optional[PydanticObjectId] = Field(
        default_factory=PydanticObjectId, alias="_id"
    )
    name: str
    avatar: str
    followers: int = 0
    engage: int = 0
    field_str: str
    field_bool: bool
    field_int: int
    field_float: float
    field_list_str: List[str]
    field_list_int: List[int]
    optional_field_str: Optional[str] = None
    optional_field_bool: Optional[bool] = None
    optional_field_int: Optional[int] = None
    optional_field_float: Optional[float] = None
    optional_field_list_str: Optional[List[str]] = None
    optional_field_list_int: Optional[List[int]] = None


class Influencer_Update(BaseModel):
    """
    Influencer update model
    """

    name: Optional[str] = None
    avatar: Optional[str] = None
    followers: Optional[str] = None
    engage: Optional[str] = None
    field_str: Optional[str] = None
    field_bool: Optional[bool] = None
    field_int: Optional[int] = None
    field_float: Optional[float] = None
    field_list_str: Optional[List[str]] = None
    field_list_int: Optional[List[int]] = None
    optional_field_str: Optional[str] = None
    optional_field_bool: Optional[bool] = None
    optional_field_int: Optional[int] = None
    optional_field_float: Optional[float] = None
    optional_field_list_str: Optional[List[str]] = None
    optional_field_list_int: Optional[List[int]] = None
