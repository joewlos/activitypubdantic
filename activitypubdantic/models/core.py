# -*- coding: utf-8 -*-
"""
CORE PYDANTIC MODELS FOR VALIDATION \n
Documentation: https://www.w3.org/TR/activitystreams-vocabulary/#types
"""
# Import Pydantic models and types
from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator, HttpUrl
from typing import get_args, List, Literal, Union

# Import utils
from activitypubdantic.models._utils.language_types import language_types
from activitypubdantic.models._utils.mime_types import image_mime_types, mime_types


"""
DEFAULTS
"""


_DEFAULT_LANGUAGE = "en-US"
_DEFAULT_CONTEXT_URL = "https://www.w3.org/ns/activitystreams"
_DEFAULT_CONTEXT = Field(HttpUrl(_DEFAULT_CONTEXT_URL), alias="@context")


"""
MODEL NAMES & CATEGORIES
"""

_core_collection_models = [
    "CollectionModel",
    "CollectionPageModel",
    "OrderedCollectionModel",
    "OrderedCollectionPageModel",
]

_core_link_models = [
    "LinkModel",
]

_core_object_models = [
    "ObjectModel",
]


"""
VALIDATORS & ALIAS GENERATORS
"""


# Switch to camel case
def must_be_camel(v):
    return "".join(x if i == 0 else x.capitalize() for i, x in enumerate(v.split("_")))


# For certain fields, the keys in their dictionaries must be defined language types
def must_be_language_strings(v):
    if v is not None and v is dict:
        for key in v.keys():
            if key not in list(get_args(language_types)):
                raise ValueError(f"Key {key} is not a defined language type.")
            if type(v[key]) != str:  # TODO: Attempt conversion to string
                raise ValueError(f"Key {key} value {v[key]} is not a string.")
    return v


# Sometimes media must be of the image mime type
def must_be_image_types(v):
    if v is not None:
        if "media_type" in v and v.media_type not in image_mime_types:
            raise ValueError(f"Media type {v.media_type} is not a defined image type.")
    return v


# Link relations must not contain spaces or commas
def must_not_contain_spaces_or_commas(v):
    if v is str and (" " in v or "," in v):
        raise ValueError(f"String {v} contains spaces or commas.")
    return v


# Convert a single value into a list
def must_be_list(v):
    if isinstance(v, list):
        return v
    return [v]


# Try to initialize an ObjectModel with a string or dictionary
def must_be_objects(v):
    if isinstance(v, str):  # If a string, default to ObjectModel
        v = ObjectModel(id=v)

    # If it's a dictionary, unpack into ObjectModel
    elif isinstance(v, dict):
        v = ObjectModel(**v)

    # Return the model data
    return v.model_dump(exclude_none=True)


# Try to initialize one of the Collection models with a string or dictionary
# Choose the model based on its contents
def must_be_collections(v, return_model=False):
    if isinstance(v, str):  # If a string, default to CollectionModel
        v = CollectionModel(id=v)

    # Check if dictionary keys are eligible for CollectionPages
    elif isinstance(v, dict):
        if ("part_of" in v.keys() or "next" in v.keys() or "prev" in v.keys()) or (
            "type" in v.keys()
            and v["type"] in ["CollectionPage", "OrderedCollectionPage"]
        ):
            if (
                "type" in v.keys() and v["type"] == "OrderedCollectionPage"
            ) or "start_index" in v.keys():
                v = OrderedCollectionPageModel(**v)
            else:
                v = CollectionPageModel(**v)

        # Otherwise, assume CollectionModel
        else:
            if "type" in v.keys() and v["type"] == "OrderedCollection":
                v = OrderedCollectionModel(**v)
            else:
                v = CollectionModel(**v)

    # The name now must be one of the four possible models
    if not v.__class__.__name__ in _core_collection_models:
        raise ValueError(
            "Must be one of {}.".format(", ".join(_core_collection_models))
        )

    # Return the model data
    if return_model:
        return v
    else:
        return v.model_dump(exclude_none=True)


# Try to initialize an OrderedCollection with a string or dictionary
def must_be_ordered_collections(v):
    if isinstance(v, str):  # If a string, default to OrderedCollectionModel
        v = OrderedCollectionModel(id=v)

    # If it's a dictionary, unpack into ObjectModel
    elif isinstance(v, dict):
        v = OrderedCollectionModel(**v)

    # The name now must be OrderedCollectionModel
    if v.__class__.__name__ != "OrderedCollectionModel":
        raise ValueError(f"Must be OrderedCollectionModel.")

    # Return the model data
    return v.model_dump(exclude_none=True)


# Try to determine if a value is a Link or Object, and then initialize that model
def must_be_links_or_objects(v):
    if isinstance(v, str):  # If a string, default to ObjectModel
        v = ObjectModel(id=v)

    # Check if dictionary keys are eligible for LinkModel
    elif isinstance(v, dict):
        if "href" in v.keys():  # Use LinkModel if there's an href
            v = LinkModel(**v)
        else:
            v = ObjectModel(**v)  # Otherwise, use ObjectModel

    # The name now must be one of the two possible models
    allowable_names = _core_link_models + _core_object_models
    if not v.__class__.__name__ in allowable_names:
        raise ValueError("Must be one of {}.".format(", ".join(allowable_names)))

    # Return the model data
    return v.model_dump(exclude_none=True)


# Try to determine if a value is a Link or Collection, and then initialize that model
def must_be_links_or_collections(v):
    if isinstance(v, str):  # If a string, default to CollectionModel
        v = must_be_collections(v, return_model=True)

    # Check if dictionary keys are eligible for LinkModel
    elif isinstance(v, dict):
        if "href" in v.keys():
            v = LinkModel(**v)  # Use LinkModel if there's an href
        else:
            v = must_be_collections(
                v, return_model=True
            )  # Otherwise, use CollectionModel

    # The name now must be one of the two possible models
    allowable_names = _core_collection_models + _core_link_models
    if not v.__class__.__name__ in allowable_names:
        raise ValueError("Must be one of {}.".format(", ".join(allowable_names)))

    # Return the model data
    return v.model_dump(exclude_none=True)


# Try to determine if a value is a Link or CollectionPage, and then initialize that model
def must_be_links_or_collectionpages(v):
    if isinstance(v, str):  # If a string, default to CollectionPageModel
        return CollectionPageModel(id=v)

    # Check if dictionary keys are eligible for LinkModel
    elif isinstance(v, dict):
        if "href" in v.keys():
            v = LinkModel(**v)  # Use LinkModel if there's an href
        else:
            v = CollectionPageModel(**v)  # Otherwise, use CollectionPageModel

    # The name now must be one of the two possible models
    allowable_names = ["CollectionPageModel"] + _core_link_models
    if not v.__class__.__name__ in allowable_names:
        raise ValueError("Must be one of {}.".format(", ".join(allowable_names)))

    # Return the model data
    return v.model_dump(exclude_none=True)


# Try to determine if a value is a Link or Image, and then initialize that model
def must_be_links_or_images(v):
    if isinstance(v, str):  # If a string, default to ImageModel
        v = ImageModel(id=v)

    # Check if dictionary keys are eligible for LinkModel
    elif isinstance(v, dict):
        if "href" in v.keys():
            v = LinkModel(**v)  # Use LinkModel if there's an href
        else:
            v = ImageModel(**v)  # Otherwise, use ImageModel

    # The name now must be one of the two possible models
    allowable_names = ["ImageModel"] + _core_link_models
    if not v.__class__.__name__ in allowable_names:
        raise ValueError("Must be one of {}.".format(", ".join(allowable_names)))

    # Return the model data
    return v.model_dump(exclude_none=True)


# Try to initialize a Link, otherwise, assume HttpUrl
def must_be_links_or_urls(v):
    if isinstance(v, str):  # If a string, assume HttpUrl
        return v

    # Check if dictionary keys are eligible for LinkModel
    elif isinstance(v, dict) and "href" in v.keys():
        return LinkModel(**v)

    # Because not always returning a model, perform no further validation
    return v


# Try to initialize a Place
def must_be_places(v):
    if isinstance(v, str):  # If a string, default to PlaceModel
        v = PlaceModel(id=v)

    # Unpack a dictionary into PlaceModel
    elif isinstance(v, dict):
        v = PlaceModel(**v)

    # The name now must be one possible model
    if v.__class__.__name__ != "PlaceModel":
        raise ValueError(f"Must be a PlaceModel.")

    # Return the model data
    return v.model_dump(exclude_none=True)


"""
CORE DEPENDENCIES
"""


class CoreModel(BaseModel):
    """
    Always use the same context and alias generator for core models.
    """

    # Ensure camel case for all aliases
    model_config = ConfigDict(
        alias_generator=must_be_camel,
        populate_by_name=True,
        extra="allow",  # Allow extra fields for flexibility
    )

    # Context
    context: Union[HttpUrl, List] = _DEFAULT_CONTEXT


"""
LINK
"""


class LinkModel(CoreModel):
    """
    A Link is an indirect, qualified reference to a resource identified by a URL.
    """

    # Type does not need to be literal for propogation
    type: str = "Link"

    # Required properties
    href: HttpUrl

    # Properties
    rel: List[str] = None
    media_type: mime_types = None
    name: str = None
    name_map: dict = (
        None  # Dictionary of language keys and name values, validated below
    )
    hreflang: language_types = _DEFAULT_LANGUAGE
    height: int = Field(None, ge=0)
    width: int = Field(None, ge=0)
    preview: List[Union[LinkModel, ObjectModel]] = None

    # Validation of name_map for language keys
    @field_validator("name_map")
    def validate_language_strings(cls, v):
        return must_be_language_strings(v)

    # Validtion of list of compliant strings for rel
    @field_validator("rel", mode="before")
    def validate_spaces_or_commas(cls, v):
        v = must_be_list(v)
        for i, item in enumerate(v):
            if item:
                v[i] = must_not_contain_spaces_or_commas(item)
        return v

    # Validation of preview for Link or Object
    @field_validator("preview", mode="before")
    def validate_links_or_objects(cls, v):
        v = must_be_list(v)
        for i, item in enumerate(v):
            if item:
                v[i] = must_be_links_or_objects(item)
        return v

    # Initialize with an optional positional argument for id
    def __init__(self, href: HttpUrl = None, **kwargs) -> None:
        if href:
            super(LinkModel, self).__init__(href=href, **kwargs)
        else:
            super(LinkModel, self).__init__(**kwargs)


"""
OBJECTS
"""


class ObjectModel(CoreModel):
    """
    Describes an Object of any kind.
    Accept a positional argument for id to handle different ActivityPub implementations.
    """

    # Type does not need to be literal for propogation
    type: str = "Object"

    # All objects distributed by the ActivityPub protocol MUST have unique global identifiers.
    # Unless they are intentionally transient.
    # (Such as some kinds of chat messages or game notifications).
    id: HttpUrl = None

    # Properties
    attachment: List[Union[LinkModel, ObjectModel]] = None
    attributed_to: List[Union[LinkModel, ObjectModel]] = None
    audience: List[Union[LinkModel, ObjectModel]] = None
    content: str = None
    content_map: dict = None  # Dictionary of language keys and content values
    name: str = None
    name_map: dict = None  # Dictionary of language keys and name values
    end_time: datetime = None
    generator: List[Union[LinkModel, ObjectModel]] = None
    icon: List[Union[LinkModel, ImageModel]] = None
    image: List[Union[LinkModel, ImageModel]] = None
    in_reply_to: List[Union[LinkModel, ObjectModel]] = None
    location: PlaceModel = None
    preview: List[Union[LinkModel, ObjectModel]] = None
    published: datetime = None
    replies: ObjectModel = (
        None  # For performance, use ObjectModel, but validate as Collection
    )
    start_time: datetime = None
    summary: str = None
    summary_map: dict = None  # Dictionary of language keys and summary values
    tag: List[Union[LinkModel, ObjectModel]] = None
    updated: datetime = None
    url: List[Union[HttpUrl, LinkModel]] = None
    to: List[Union[LinkModel, ObjectModel]] = None
    bto: List[Union[LinkModel, ObjectModel]] = None
    cc: List[Union[LinkModel, ObjectModel]] = None
    bcc: List[Union[LinkModel, ObjectModel]] = None
    media_type: mime_types = None
    duration: str = None  # TODO: Validate the duration string.

    # Necessary for ActivityPub but not ActivityStreams
    # Documentation: https://www.w3.org/TR/activitypub/#source-property
    source: ObjectModel = None

    # Validation of content_map for language keys
    @field_validator("content_map", "name_map", "summary_map")
    def validate_language_strings(cls, v):
        return must_be_language_strings(v)

    # Validation of icon 1x1 ratio
    @field_validator("icon")
    def validate_1x1(cls, v):
        for pic in v:
            if pic is not None:
                if "width" in pic or "height" in pic:
                    if (pic.width and not pic.height) or (pic.height and not pic.width):
                        raise ValueError("Icon must have both width and height.")
                    if pic.width != pic.height:
                        raise ValueError("Icon must be 1x1 ratio.")
        return v

    # Images and icons must be links or images with correct mime type in a list
    @field_validator("icon", "image", mode="before")
    def validate_links_or_images(cls, v):
        v = must_be_list(v)
        for i, item in enumerate(v):
            if item:
                v[i] = must_be_links_or_images(item)
                must_be_image_types(v[i])
        return v

    # Correct to CollectionModel
    @field_validator("replies", mode="before")
    def validate_collections(cls, v):
        return must_be_collections(v)

    # Correct to PlaceModel
    @field_validator("location", mode="before")
    def validate_places(cls, v):
        return must_be_places(v)

    # Correct to list of Links or Objects
    @field_validator(
        "attachment",
        "attributed_to",
        "audience",
        "generator",
        "in_reply_to",
        "preview",
        "tag",
        "bto",
        "cc",
        "bcc",
        mode="before",
    )
    def validate_links_or_objects(cls, v):
        v = must_be_list(v)
        for i, item in enumerate(v):
            if item:
                v[i] = must_be_links_or_objects(item)
        return v

    # Correct to list of Links or HttpUrls
    @field_validator(
        "url",
        mode="before",
    )
    def validate_links_or_urls(cls, v):
        v = must_be_list(v)
        for i, item in enumerate(v):
            if item:
                v[i] = must_be_links_or_urls(item)
        return v

    # Initialize with an optional positional argument for id
    def __init__(self, id: HttpUrl = None, **kwargs) -> None:
        if id:
            super(ObjectModel, self).__init__(id=id, **kwargs)
        else:
            super(ObjectModel, self).__init__(**kwargs)


class DocumentModel(ObjectModel):
    """
    Represents a document of any kind. Inherits all properties from Object. \n
    (Not actually core, but it is the base of Image, which is nested in Object.)
    """

    # Type does not need to be literal for propogation
    type: str = "Document"


class ImageModel(DocumentModel):
    """
    An image document of any kind. Inherits all properties from Document. \n
    (Not actually core, but it is nested in Object.)
    """

    # Type
    type: Literal["Image"] = "Image"


class PlaceModel(ObjectModel):
    """
    Extends the Object to describe geographic information. \n
    (Not actually core, but it is nested in Object.)
    """

    # Type
    type: Literal["Place"] = "Place"

    # Properties
    accuracy: float = None
    altitude: float = None
    longitude: float = None
    latitude: float = None
    radius: float = None
    units: str = None


"""
COLLECTIONS
"""


class CollectionModel(ObjectModel):
    """
    A Collection is a subtype of Object that represents ordered or unordered Links or Objects.
    """

    # Type does not need to be literal for propogation
    type: str = "Collection"

    # Collection properties
    total_items: int = Field(None, ge=0)
    current: Union[CollectionPageModel, LinkModel] = None
    first: Union[CollectionPageModel, LinkModel] = None
    last: Union[CollectionPageModel, LinkModel] = None
    items: List[Union[LinkModel, ObjectModel]] = None

    # Correct to list of Links or Objects
    @field_validator(
        "items",
        mode="before",
    )
    def validate_links_or_objects(cls, v):
        v = must_be_list(v)
        for i, item in enumerate(v):
            if item:
                v[i] = must_be_links_or_objects(item)
        return v

    # Correct to Links or CollectionPages
    @field_validator(
        "current",
        "first",
        "last",
        mode="before",
    )
    def validate_links_or_collectionpages(cls, v):
        return must_be_links_or_collectionpages(v)


class OrderedCollectionModel(CollectionModel):
    """
    A subtype of Collection in which members of the collection are assumed to always be ordered.
    """

    # Type
    type: Literal["OrderedCollection"] = "OrderedCollection"

    # Properties
    items: None = None  # No items, only orderedItems
    ordered_items: List[Union[LinkModel, ObjectModel]] = None

    # Correct to list of Links or Objects
    @field_validator(
        "ordered_items",
        mode="before",
    )
    def validate_links_or_objects(cls, v):
        v = must_be_list(v)
        for i, item in enumerate(v):
            if item:
                v[i] = must_be_links_or_objects(item)
        return v


class CollectionPageModel(CollectionModel):
    """
    Used to represent distinct subsets of items from a Collection.
    """

    # Type does not need to be literal for propogation
    type: str = "CollectionPage"

    # Properties
    part_of: Union[LinkModel, CollectionModel] = None
    next: Union[LinkModel, CollectionPageModel] = None
    prev: Union[LinkModel, CollectionPageModel] = None

    # Correct to Links or Collections
    @field_validator(
        "part_of",
        mode="before",
    )
    def validate_links_or_collections(cls, v):
        return must_be_links_or_collections(v)

    # Correct to Links or CollectionPages
    @field_validator(
        "next",
        "prev",
        mode="before",
    )
    def validate_links_or_collectionpages(cls, v):
        return must_be_links_or_collectionpages(v)


class OrderedCollectionPageModel(CollectionPageModel):
    """
    Used to represent ordered subsets of items from an OrderedCollection.
    """

    # Type
    type: Literal["OrderedCollectionPage"] = "OrderedCollectionPage"

    # Properties
    start_index: int = Field(None, ge=0)
    items: None = None  # No items, only orderedItems
    ordered_items: List[Union[LinkModel, ObjectModel]] = None

    # Correct to list of Links or Objects
    @field_validator(
        "ordered_items",
        mode="before",
    )
    def validate_links_or_objects(cls, v):
        v = must_be_list(v)
        for i, item in enumerate(v):
            if item:
                v[i] = must_be_links_or_objects(item)
        return v


"""
ACTIVITIES
"""


class ActivityModel(ObjectModel):
    """
    An Activity is a subtype of Object that describes some form of action that may happen,
    is currently happening, or has already happened.
    """

    # Type does not need to be literal for propogation
    type: str = "Activity"

    # Properties
    actor: List[Union[LinkModel, ObjectModel]] = None
    object: ObjectModel = None
    target: List[Union[LinkModel, ObjectModel]] = None
    result: List[Union[LinkModel, ObjectModel]] = None
    origin: List[Union[LinkModel, ObjectModel]] = None
    instrument: List[Union[LinkModel, ObjectModel]] = None

    # Correct to Object
    @field_validator("object", mode="before")
    def validate_objects(cls, v):
        return must_be_objects(v)

    # Correct to list of Links or Objects
    @field_validator(
        "actor",
        "target",
        "result",
        "origin",
        "instrument",
        mode="before",
    )
    def validate_links_or_objects(cls, v):
        v = must_be_list(v)
        for i, item in enumerate(v):
            if item:
                v[i] = must_be_links_or_objects(item)
        return v


class IntransitiveActivityModel(ActivityModel):
    """
    Instances of IntransitiveActivity are a subtype of Activity representing intransitive actions.
    Lacks the object property.
    """

    # Type does not need to be literal for propogation
    type: str = "IntransitiveActivity"

    # Properties
    object: None = None
