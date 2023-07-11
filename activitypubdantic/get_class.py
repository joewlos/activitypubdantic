# -*- coding: utf-8 -*-
"""
FUNCTIONS FOR SELECTING CLASSES TO PERFORM ACTIONS
"""
# Import Pydantic models and their functions
from activitypubdantic.models import *
from activitypubdantic.get_model import get_model, get_model_data, get_model_json

# Import other packages
import json
from typing import Union


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
        input_json: Union[dict, list],
    ):
        self.model = model
        self.input_json = input_json

    def data(
        self,
        by_alias: bool = True,
        exclude_none: bool = True,
        verbose: bool = True,
    ):
        """
        Return the class input_json as a Python dictionary or list.
        """
        return get_model_data(
            self.input_json,
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
    ):
        """
        Return the class input_json as a JSON string.
        """
        return get_model_json(
            self.input_json,
            by_alias=by_alias,
            exclude_none=exclude_none,
            verbose=verbose,
            indent=indent,
        )


class Activity(Base):
    """
    Activity data and associated functions.
    """


class Actor(Base):
    """
    Actor data and associated functions.
    """


class Collection(Base):
    """
    Collection data and associated functions.
    """


class Link(Base):
    """
    Link data and associated functions.
    """


class Object(Base):
    """
    Object data and associated functions.
    """


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
    input_json: Union[dict, str, list]  # If string, assume it is JSON
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
