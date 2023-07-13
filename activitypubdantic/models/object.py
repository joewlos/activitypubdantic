# -*- coding: utf-8 -*-
"""
OBJECT PYDANTIC MODELS FOR VALIDATION \n
Documentation: https://www.w3.org/TR/activitystreams-vocabulary/#object-types
"""
# Import Pydantic models and types
from datetime import datetime
from pydantic import field_validator
from typing import List, Literal, Union

# Import core models that are required for the actor definition
# Not all will be directly called
from activitypubdantic.models.core import (
    DocumentModel,
    ImageModel,
    LinkModel,
    ObjectModel,
    PlaceModel,
    validate_list_links_or_objects,
    validate_list_objects,
)

"""
OBJECT TYPES
"""


class RelationshipModel(ObjectModel):
    """
    Describes a relationship between two individuals.
    """

    # Type
    type: Literal["Relationship"] = "Relationship"

    # Properties
    subject: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None
    object: Union[None, List[Union[None, LinkModel, ObjectModel]]] = None
    relationship: Union[None, List[Union[None, ObjectModel]]] = None

    # Validators
    _relationship_list_links_or_objects = field_validator(
        "subject", "object", mode="before"
    )(validate_list_links_or_objects)
    _relationship_list_objects = field_validator("relationship", mode="before")(
        validate_list_objects
    )


class ArticleModel(ObjectModel):
    """
    Represents any kind of multi-paragraph written work.
    """

    # Type
    type: Literal["Article"] = "Article"


class AudioModel(DocumentModel):
    """
    Represents an audio document of any kind.
    """

    # Type
    type: Literal["Audio"] = "Audio"


class VideoModel(DocumentModel):
    """
    Represents a video document of any kind.
    """

    # Type
    type: Literal["Video"] = "Video"


class NoteModel(ObjectModel):
    """
    Represents a short written work typically less than a single paragraph in length.
    """

    # Type
    type: Literal["Note"] = "Note"


class PageModel(DocumentModel):
    """
    Represents a Web Page.
    """

    # Type
    type: Literal["Page"] = "Page"


class EventModel(ObjectModel):
    """
    Represents any kind of event.
    """

    # Type
    type: Literal["Event"] = "Event"


class ProfileModel(ObjectModel):
    """
    A Profile is a content object that describes another Object.
    Typically used to describe Actor Type objects.
    """

    # Type
    type: Literal["Profile"] = "Profile"

    # Properties
    describes: Union[None, ObjectModel] = None


class TombstoneModel(ObjectModel):
    """
    A Tombstone represents a content object that has been deleted.
    """

    # Type
    type: Literal["Tombstone"] = "Tombstone"

    # Properties
    former_type: Union[None, ObjectModel] = None
    deleted: Union[None, datetime] = None
