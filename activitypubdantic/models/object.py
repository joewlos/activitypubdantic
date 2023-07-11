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
    must_be_list,
    must_be_links_or_objects,
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
    subject: List[Union[LinkModel, ObjectModel]] = None
    object: List[Union[LinkModel, ObjectModel]] = None
    relationship: List[ObjectModel] = None

    # Validators for Links and Objects
    @field_validator("subject", "object", mode="before")
    def validate_links_or_objects(cls, v):
        v = must_be_list(v)
        for i, item in enumerate(v):
            if item:
                v[i] = must_be_links_or_objects(item)
        return v


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
    describes: ObjectModel = None


class TombstoneModel(ObjectModel):
    """
    A Tombstone represents a content object that has been deleted.
    """

    # Type
    type: Literal["Tombstone"] = "Tombstone"

    # Properties
    former_type: ObjectModel = None
    deleted: datetime = None
