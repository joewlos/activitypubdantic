# -*- coding: utf-8 -*-
"""
FUNCTIONS FOR SELECTING CLASSES TO PERFORM ACTIONS
"""
# Import Pydantic models and their functions
from activitypubdantic.models import *
from activitypubdantic.get_model import get_model, get_model_data, get_model_json

# Import other packages
from datetime import datetime
import json
from typing import Union


"""
DEFAULTS
"""


_DEFAULT_LANGUAGES = ["en", "en-US"]
_DEFAULT_MAP_FIELDS = {
    "content_map": "content",
    "summary_map": "summary",
    "name_map": "name",
}
_DEFAULT_PROTECTED_FIELDS = ["data", "model", "input_json", "_data", "json"]


"""
CLASSES
"""


class Base:
    """
    Base extends default functions to all other classes.
    """

    def __init__(
        self,
        model: Union[
            ActivityModel, ActorModel, CollectionModel, LinkModel, ObjectModel
        ],
        input_json: dict,  # TODO: There's no way this could be a list, right?
        default_languages: list = _DEFAULT_LANGUAGES,
    ):
        self.model = model
        self.input_json = input_json
        self._data = self.data(
            exclude_none=False, by_alias=False, use_input_json=True
        )  # Use underscore to avoid conflict with data() function

        # For each key,value pair in the input_json, set the class attribute
        for k, v in self._data.items():
            if k not in _DEFAULT_PROTECTED_FIELDS:
                setattr(self, k, v)

        # For mapped fields, update their corresponding value with the default language
        for k, v in _DEFAULT_MAP_FIELDS.items():
            if k in self._data:
                for language in default_languages:
                    if self._data[k] and language in self._data[k]:
                        setattr(self, v, self._data[k][language])
                        break

    def _internal_data(self):
        """
        Get the internal data dictionary of unprotected and not null fields.
        """
        clean_data = {}
        for k, v in self.__dict__.items():
            if k not in _DEFAULT_PROTECTED_FIELDS and v:
                clean_data[k] = v
        return clean_data

    def data(
        self,
        by_alias: bool = True,
        exclude_none: bool = True,
        verbose: bool = True,
        use_input_json: bool = False,
    ):
        """
        Return the class input_json as a Python dictionary or list with settings.
        """
        return get_model_data(
            self.input_json if use_input_json else self._internal_data(),
            by_alias=by_alias,
            exclude_none=exclude_none,
            verbose=verbose,
        )

    def json(
        self,
        by_alias: bool = True,
        exclude_none: bool = True,
        verbose: bool = True,
        indent: int = 2,
        use_input_json: bool = False,
    ):
        """
        Return the class input_json as a JSON string with settings.
        """
        return get_model_json(
            self.input_json if use_input_json else self._internal_data(),
            by_alias=by_alias,
            exclude_none=exclude_none,
            verbose=verbose,
            indent=indent,
        )


class Link(Base):
    """
    Link data and associated functions.
    """

    # Core type
    core_type = "Link"


class Object(Base):
    """
    Object data and associated functions.
    """

    # Core type
    core_type = "Object"

    def make_public(self):
        """
        Remove any fields (bto and bcc) that should not be public.
        """
        self.bto = None
        self.bcc = None

    def create(self):
        """
        Produce a new Activity of type Create with this Object.
        """
        if self._internal_data() == {}:
            raise ValueError("Cannot Create an empty Object.")
        return get_class(
            {
                "type": "Create",
                "object": self._internal_data(),
                "to": self.to,
                "bto": self.bto,
                "cc": self.cc,
                "bcc": self.bcc,
                "audience": self.audience,
                "published": datetime.now(),
            }
        )

    def delete(self):
        """
        Produce a new Tombstone of this Object.
        """
        return get_class(
            {
                "type": "Tombstone",
                "id": self.id,
                "published": self.published,
                "updated": datetime.now(),
                "deleted": datetime.now(),
            }
        )


class Activity(Object):
    """
    Activity data and associated functions.
    """

    # Core type
    core_type = "Activity"

    def undo(self):
        """
        Produce a new Undo of this Activity.
        """
        return get_class(
            {
                "type": "Undo",
                "object": self._internal_data(),
            }
        )


class Actor(Object):
    """
    Actor data and associated functions.
    """

    # Core type
    core_type = "Actor"

    def act(self, action_type: str, object: Object):
        """
        Produce a new Activity of the given type with this Actor as the actor
        and the given Object as the object of the activity.
        IntransitiveActivity will result in a validation failure.
        """
        return get_class(
            {
                "type": action_type,
                "actor": self._internal_data(),
                "object": object.data(),
            }
        )


class Collection(Object):
    """
    Collection data and associated functions.
    """

    # Core type
    core_type = "Collection"


"""
MAPPING DICTIONARY
"""


# Map type names to their classes
_CLASS_MAPPINGS = {
    "Accept": Activity,  # Activity Section
    "Add": Activity,
    "Accounce": Activity,
    "Arrive": Activity,
    "Block": Activity,
    "Create": Activity,
    "Delete": Activity,
    "Dislike": Activity,
    "Flag": Activity,
    "Follow": Activity,
    "Ignore": Activity,
    "Invite": Activity,
    "Join": Activity,
    "Leave": Activity,
    "Like": Activity,
    "Listen": Activity,
    "Move": Activity,
    "Offer": Activity,
    "Question": Activity,
    "Read": Activity,
    "Reject": Activity,
    "Remove": Activity,
    "TentativeAccept": Activity,
    "TentativeReject": Activity,
    "Travel": Activity,
    "Undo": Activity,
    "Update": Activity,
    "View": Activity,
    "Application": Actor,  # Actor Section
    "Group": Actor,
    "Organization": Actor,
    "Person": Actor,
    "Service": Actor,
    "Activity": Activity,  # Core Section
    "Collection": Collection,
    "CollectionPage": Collection,
    "IntransitiveActivity": Activity,
    "Link": Link,
    "Object": Object,
    "OrderedCollection": Collection,
    "OrderedCollectionPage": Collection,
    "Mention": Link,  # Link Section
    "Article": Object,  # Object Section
    "Audio": Object,
    "Document": Object,
    "Event": Object,
    "Image": Object,
    "Note": Object,
    "Page": Object,
    "Place": Object,
    "Profile": Object,
    "Relationship": Object,
    "Tombstone": Object,
    "Video": Object,
}


"""
FUNCTIONS
"""


def get_class(
    input_json: Union[dict, str]  # If string, assume it is JSON
) -> Union[Activity, Actor, Collection, Link, Object]:
    """
    Get a class for manipulating the input ActivityPub JSON.
    This function assumes any input string is JSON and parses it.
    """
    if isinstance(input_json, str):
        input_json = json.loads(input_json)

    # Load a model from the input JSON
    output_model = get_model(input_json)

    # Return a class which includes possible actions for the ActivityPub JSON
    output_class = _CLASS_MAPPINGS[output_model.type]
    return output_class(output_model, input_json)


def get_class_from_model(
    input_model: Union[
        ActivityModel, CollectionModel, LinkModel, ObjectModel
    ]  # Must be a Pydantic model
) -> Union[Activity, Actor, Collection, Link, Object]:
    """
    Get a class for manipulating the input ActivityPub JSON.
    This function assumes any input is a Pydantic model, with no further validation required.
    """
    output_class = _CLASS_MAPPINGS[input_model.type]
    return output_class(
        input_model,
        json.loads(input_model.model_dump_json(by_alias=True, exclude_none=True)),
    )
