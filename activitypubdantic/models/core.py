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
VALIDATORS & ALIAS GENERATORS & THEIR HELPERS
"""


# Switch to camel case
def _must_be_camel(v):
    return "".join(x if i == 0 else x.capitalize() for i, x in enumerate(v.split("_")))


# For certain fields, the keys in their dictionaries must be defined language types
def _must_be_language_keys(v):
    if v is not None and v is dict:
        for key in v.keys():
            if key not in list(get_args(language_types)):
                raise ValueError(f"Key {key} is not a defined language type.")
            if type(v[key]) != str:  # TODO: Attempt conversion to string
                raise ValueError(f"Key {key} value {v[key]} is not a string.")
    return v


# Sometimes media must be of the image mime type
def _must_be_image_types(v):
    if v is not None:
        if "media_type" in v and v["media_type"] not in image_mime_types:
            raise ValueError(f"Media type {v.media_type} is not a defined image type.")
    return v


# Link relations must not contain spaces or commas
def _must_be_no_spaces_or_commas(v):
    if v is str and (" " in v or "," in v):
        raise ValueError(f"String {v} contains spaces or commas.")
    return v


# Convert a single value into a list
def _must_be_list(v):
    if isinstance(v, list):
        return v
    return [v]


# Try to initialize an Object with a string or dictionary
def _must_be_objects(v):
    if isinstance(v, str):  # If a string, default to ObjectModel
        v = ObjectModel(id=v)

    # If it's a dictionary, unpack into ObjectModel
    elif isinstance(v, dict):
        v = ObjectModel(**v)

    # Return the model data
    return v.model_dump(exclude_none=True)


# Try to initialize one of the Collection models with a string or dictionary
# Choose the model based on its contents
def _must_be_collections(v, return_model=False):
    if isinstance(v, str):  # If a string, default to Collection
        v = CollectionModel(id=v)

    # Check if dictionary keys are eligible for CollectionPage
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

        # Otherwise, assume Collection
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
def _must_be_ordered_collections(v):
    if isinstance(v, str):  # If a string, default to OrderedCollection
        v = OrderedCollectionModel(id=v)

    # If it's a dictionary, unpack into OrderedCollection
    elif isinstance(v, dict):
        v = OrderedCollectionModel(**v)

    # The name now must be OrderedCollection
    if v.__class__.__name__ != "OrderedCollectionModel":
        raise ValueError(f"Must be OrderedCollectionModel.")

    # Return the model data
    return v.model_dump(exclude_none=True)


# Try to determine if a value is a Link or Object, and then initialize that model
def _must_be_links_or_objects(v):
    if isinstance(v, str):  # If a string, default to Object
        v = ObjectModel(id=v)

    # Check if dictionary keys are eligible for Link
    elif isinstance(v, dict):
        if "href" in v.keys():  # Use Link if there's an href
            v = LinkModel(**v)
        else:
            v = ObjectModel(**v)  # Otherwise, use Object

    # The name now must be one of the two possible models
    allowable_names = _core_link_models + _core_object_models
    if not v.__class__.__name__ in allowable_names:
        raise ValueError("Must be one of {}.".format(", ".join(allowable_names)))

    # Return the model data
    return v.model_dump(exclude_none=True)


# Try to determine if a value is a Link or Collection, and then initialize that model
def _must_be_links_or_collections(v):
    if isinstance(v, str):  # If a string, default to Collection
        v = _must_be_collections(v, return_model=True)

    # Check if dictionary keys are eligible for Link
    elif isinstance(v, dict):
        if "href" in v.keys():
            v = LinkModel(**v)  # Use Link if there's an href
        else:
            v = _must_be_collections(v, return_model=True)  # Otherwise, use Collection

    # The name now must be one of the two possible models
    allowable_names = _core_collection_models + _core_link_models
    if not v.__class__.__name__ in allowable_names:
        raise ValueError("Must be one of {}.".format(", ".join(allowable_names)))

    # Return the model data
    return v.model_dump(exclude_none=True)


# Try to determine if a value is a Link or CollectionPage, and then initialize that model
def _must_be_links_or_collectionpages(v):
    if isinstance(v, str):  # If a string, default to CollectionPage
        return CollectionPageModel(id=v)

    # Check if dictionary keys are eligible for Link
    elif isinstance(v, dict):
        if "href" in v.keys():
            v = LinkModel(**v)  # Use Link if there's an href
        else:
            v = CollectionPageModel(**v)  # Otherwise, use CollectionPage

    # The name now must be one of the two possible models
    allowable_names = ["CollectionPageModel"] + _core_link_models
    if not v.__class__.__name__ in allowable_names:
        raise ValueError("Must be one of {}.".format(", ".join(allowable_names)))

    # Return the model data
    return v.model_dump(exclude_none=True)


# Try to determine if a value is a Link or Image, and then initialize that model
def _must_be_links_or_images(v):
    if isinstance(v, str):  # If a string, default to Image
        v = ImageModel(id=v)

    # Check if dictionary keys are eligible for Link
    elif isinstance(v, dict):
        if "href" in v.keys():
            v = LinkModel(**v)  # Use Link if there's an href
        else:
            v = ImageModel(**v)  # Otherwise, use Image

    # The name now must be one of the two possible models
    allowable_names = ["ImageModel"] + _core_link_models
    if not v.__class__.__name__ in allowable_names:
        raise ValueError("Must be one of {}.".format(", ".join(allowable_names)))

    # Return the model data
    return v.model_dump(exclude_none=True)


# Try to initialize a Link or assume HttpUrl
def _must_be_links_or_urls(v):
    if isinstance(v, str):  # If a string, assume HttpUrl
        return v

    # Check if dictionary keys are eligible for Link
    elif isinstance(v, dict) and "href" in v.keys():
        return LinkModel(**v)

    # Because not always returning a model, perform no further validation
    return v


# Try to initialize a Place
def _must_be_places(v):
    if isinstance(v, str):  # If a string, default to Place
        v = PlaceModel(id=v)

    # Unpack a dictionary into Place
    elif isinstance(v, dict):
        v = PlaceModel(**v)

    # The name now must be one possible model
    if v.__class__.__name__ != "PlaceModel":
        raise ValueError(f"Must be a PlaceModel.")

    # Return the model data
    return v.model_dump(exclude_none=True)


# Validate list of Links or Objects
def validate_list_links_or_objects(v):
    v = _must_be_list(v)
    for i, item in enumerate(v):
        if item:
            v[i] = _must_be_links_or_objects(item)
        else:
            v.pop(i)
    return v if v else None


# Validate that the keys of a dictionary are languages
def validate_language_keys(v):
    if v:
        return _must_be_language_keys(v)
    else:
        return v


# Validate list of strings with no spaces or commas
def validate_list_no_spaces_or_commas(v):
    v = _must_be_list(v)
    for i, item in enumerate(v):
        if item:
            v[i] = _must_be_no_spaces_or_commas(item)
        else:
            v.pop(i)
    return v if v else None


# Validate that icon ratios are 1x1
def validate_icons_1x1(v):
    if v is not None:
        for pic in v:
            if v is not None:
                if "width" in pic or "height" in pic:
                    if (pic.width and not pic.height) or (pic.height and not pic.width):
                        raise ValueError("Icon must have both width and height.")
                    if pic.width != pic.height:
                        raise ValueError("Icon must be 1x1 ratio.")
    return v


# Validate list of Links or Images
def validate_list_links_or_images(v):
    v = _must_be_list(v)
    for i, item in enumerate(v):
        if item:
            v[i] = _must_be_links_or_images(item)
            _must_be_image_types(v[i])
        else:
            v.pop(i)
    return v if v else None


# Validate Collections
def validate_collections(v):
    if v:
        return _must_be_collections(v)
    else:
        return v


# Validate list of Collections
def validate_list_collections(v):
    v = _must_be_list(v)
    for i, item in enumerate(v):
        if item:
            v[i] = _must_be_collections(item)
        else:
            v.pop(i)
    return v if v else None


# Validate Places
def validate_places(v):
    if v:
        return _must_be_places(v)
    else:
        return v


# Validate Objects
def validate_objects(v):
    if v:
        return _must_be_objects(v)
    else:
        return v


# Validate list of Objects
def validate_list_objects(v):
    v = _must_be_list(v)
    for i, item in enumerate(v):
        if item:
            v[i] = _must_be_objects(item)
        else:
            v.pop(i)
    return v if v else None


# Validate list of Links or HttpUrls
def validate_list_links_or_urls(v):
    v = _must_be_list(v)
    for i, item in enumerate(v):
        if item:
            v[i] = _must_be_links_or_urls(item)
        else:
            v.pop(i)
    return v if v else None


# Validate Links or CollectionPages
def validate_links_or_collectionpages(v):
    if v:
        return _must_be_links_or_collectionpages(v)
    else:
        return v


# Validate Links or Collections
def validate_links_or_collections(v):
    if v:
        return _must_be_links_or_collections(v)
    else:
        return v


"""
CORE DEPENDENCIES
"""


class CoreModel(BaseModel):
    """
    Always use the same context and alias generator for core models.
    """

    # Ensure camel case for all aliases
    model_config = ConfigDict(
        alias_generator=_must_be_camel,
        populate_by_name=True,
        extra="allow",  # Allow extra fields for flexibility
    )

    # Context
    context: Union[HttpUrl, List, dict] = _DEFAULT_CONTEXT


"""
LINK
"""


class LinkModel(CoreModel):
    """
    A Link is an indirect, qualified reference to a resource identified by a URL.
    """

    # Type
    type: str = "Link"  # Should be overridden by subclasses

    # Required property, cannot be null (otherwise, what's the point of a Link?)
    href: HttpUrl

    # Properties
    rel: Union[None, List[Union[None, str]]] = None
    media_type: Union[None, mime_types] = None
    name: Union[None, str] = None
    name_map: Union[
        None, dict
    ] = None  # Dictionary of language keys and name values, validated below
    hreflang: Union[None, language_types] = _DEFAULT_LANGUAGE
    height: Union[None, int] = Field(None, ge=0)
    width: Union[None, int] = Field(None, ge=0)
    preview: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None

    # Validation
    _link_language_strings = field_validator("name_map")(validate_language_keys)
    _link_list_no_spaces_or_commas = field_validator("rel", mode="before")(
        validate_list_no_spaces_or_commas
    )
    _link_list_links_or_objects = field_validator("preview", mode="before")(
        validate_list_links_or_objects
    )

    # Initialize with an optional positional argument for href
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

    # Type
    type: str = "Object"  # Should be overridden by subclasses

    # All objects distributed by the ActivityPub protocol MUST have unique global identifiers.
    # Unless they are intentionally transient, such as chat messages or game notifications.
    # For that reason, IDs may be either a valid URL or None. They are not technically required.
    id: Union[None, HttpUrl] = None

    # Properties
    attachment: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None
    attributed_to: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None
    audience: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None
    content: Union[None, str] = None
    content_map: Union[
        None, dict
    ] = None  # Dictionary of language keys and content values
    name: Union[None, str] = None
    name_map: Union[None, dict] = None  # Dictionary of language keys and name values
    end_time: Union[None, datetime] = None
    generator: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None
    icon: Union[None, List[Union[None, LinkModel, ImageModel]]] = None
    image: Union[None, List[Union[None, LinkModel, ImageModel]]] = None
    in_reply_to: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None
    location: Union[None, PlaceModel] = None
    preview: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None
    published: Union[None, datetime] = None
    replies: Union[
        None, ObjectModel
    ] = None  # For performance, use Object, but validate as Collection
    start_time: Union[None, datetime] = None
    summary: Union[None, str] = None
    summary_map: Union[
        None, dict
    ] = None  # Dictionary of language keys and summary values
    shares: Union[None, ObjectModel] = None  # Collection in ActivityPub
    tag: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None
    updated: Union[None, datetime] = None
    url: Union[None, List[Union[None, HttpUrl, LinkModel]]] = None
    to: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None
    bto: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None
    cc: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None
    bcc: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None
    media_type: Union[None, mime_types] = None
    duration: Union[None, str] = None  # TODO: Validate the duration string.

    # Necessary for ActivityPub but not ActivityStreams
    # Documentation: https://www.w3.org/TR/activitypub/#source-property
    source: Union[None, ObjectModel] = None

    # Validation
    _object_language_strings = field_validator(
        "content_map", "name_map", "summary_map"
    )(validate_language_keys)
    _object_icon_ratios = field_validator("icon")(validate_icons_1x1)
    _object_list_links_or_images = field_validator("image", "icon", mode="before")(
        validate_list_links_or_images
    )
    _object_collections = field_validator("replies", "shares", mode="before")(
        validate_collections
    )
    _object_places = field_validator("location", mode="before")(validate_places)
    _object_list_links_or_objects = field_validator(
        "attachment",
        "attributed_to",
        "audience",
        "generator",
        "in_reply_to",
        "preview",
        "tag",
        "to",
        "bto",
        "cc",
        "bcc",
        mode="before",
    )(validate_list_links_or_objects)
    _object_list_links_or_urls = field_validator("url", mode="before")(
        validate_list_links_or_urls
    )

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

    # Type
    type: Literal["Document"] = "Document"


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
    accuracy: Union[None, float] = None
    altitude: Union[None, float] = None
    longitude: Union[None, float] = None
    latitude: Union[None, float] = None
    radius: Union[None, float] = None
    units: Union[None, str] = None


"""
COLLECTIONS
"""


class CollectionModel(ObjectModel):
    """
    A Collection is a subtype of Object that represents ordered or unordered Links or Objects.
    """

    # Type
    type: Literal["Collection"] = "Collection"

    # Collection properties
    total_items: Union[None, int] = Field(None, ge=0)
    current: Union[None, CollectionPageModel, LinkModel] = None
    first: Union[None, CollectionPageModel, LinkModel] = None
    last: Union[None, CollectionPageModel, LinkModel] = None
    items: Union[
        None, List[Union[None, LinkModel, ObjectModel]]
    ] = None  # May be an empty list

    # Validation
    _collection_list_links_or_objects = field_validator("items", mode="before")(
        validate_list_links_or_objects
    )
    _collection_links_or_collectionpages = field_validator(
        "current",
        "first",
        "last",
        mode="before",
    )(validate_links_or_collectionpages)


class OrderedCollectionModel(CollectionModel):
    """
    A subtype of Collection in which members of the collection are assumed to always be ordered.
    """

    # Type
    type: Literal["OrderedCollection"] = "OrderedCollection"

    # Properties
    items: None = None  # No items, only orderedItems
    ordered_items: Union[
        None, List[Union[None, LinkModel, ObjectModel]]
    ] = None  # May be an empty list

    # Validation
    _orderedcollection_list_links_or_objects = field_validator(
        "ordered_items", mode="before"
    )(validate_list_links_or_objects)


class CollectionPageModel(CollectionModel):
    """
    Used to represent distinct subsets of items from a Collection.
    """

    # Type
    type: Literal["CollectionPage"] = "CollectionPage"

    # Properties
    part_of: Union[None, LinkModel, CollectionModel] = None
    next: Union[None, LinkModel, CollectionPageModel] = None  # May not be a next page
    prev: Union[None, LinkModel, CollectionPageModel] = None  # May not be a prev page

    # Validation
    _collectionpage_links_or_collections = field_validator("part_of", mode="before")(
        validate_links_or_collections
    )
    _collectionpage_links_or_collectionpages = field_validator(
        "next",
        "prev",
        mode="before",
    )(validate_links_or_collectionpages)


class OrderedCollectionPageModel(CollectionPageModel):
    """
    Used to represent ordered subsets of items from an OrderedCollection.
    """

    # Type
    type: Literal["OrderedCollectionPage"] = "OrderedCollectionPage"

    # Properties
    start_index: Union[None, int] = Field(None, ge=0)
    items: None = None  # No items, only orderedItems
    ordered_items: Union[
        None, List[Union[None, LinkModel, ObjectModel]]
    ] = None  # May be an empty list

    # Validation
    _orderedcollectionpage_list_links_or_objects = field_validator(
        "ordered_items", mode="before"
    )(validate_list_links_or_objects)


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
    actor: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None
    object: Union[None, ObjectModel] = None
    target: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None
    result: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None
    origin: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None
    instrument: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None

    # Validation
    _activity_objects = field_validator("object", mode="before")(validate_objects)
    _activity_list_links_or_objects = field_validator(
        "actor",
        "target",
        "result",
        "origin",
        "instrument",
        mode="before",
    )(validate_list_links_or_objects)


class IntransitiveActivityModel(ActivityModel):
    """
    Instances of IntransitiveActivity are a subtype of Activity representing intransitive actions.
    Lacks the object property.
    """

    # Type does not need to be literal for propogation
    type: str = "IntransitiveActivity"

    # Properties
    object: None = None  # No object
