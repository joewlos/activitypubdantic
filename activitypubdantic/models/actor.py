# -*- coding: utf-8 -*-
"""
ACTOR PYDANTIC MODELS FOR VALIDATION \n
Documentation: https://www.w3.org/TR/activitystreams-vocabulary/#actor-types
"""
# Import Pydantic models and types
from pydantic import BaseModel, ConfigDict, field_validator, HttpUrl
from typing import List, Literal, Union

# Import core models that are required for the actor definition
# Not all will be directly called
from activitypubdantic.models.core import (
    CollectionModel,
    CollectionPageModel,
    ImageModel,
    LinkModel,
    PlaceModel,
    ObjectModel,
    OrderedCollectionModel,
    _must_be_camel,
    _must_be_collections,
    _must_be_list,
    _must_be_ordered_collections,
    validate_collections,
)


"""
VALIDATORS
"""


# Validate HttpUrl or EndPoints
def validate_httpurls_or_endpoints(v):
    if isinstance(v, str):  # If a string, default to HttpUrl
        return v
    elif isinstance(v, dict):  # If a dictionary, use EndPointsModel
        return EndpointsModel(**v)
    return v


# Validate list of Collections
def validate_list_collections(v):
    v = _must_be_list(v)
    for i, item in enumerate(v):
        if item:
            v[i] = _must_be_collections(item)
    return v


# Validate ordered Collections
def validate_ordered_collections(v):
    return _must_be_ordered_collections(v)


"""
ACTOR DEPENDENCIES
"""


class EndpointsModel(BaseModel):
    """
    A JSON object which maps additional (typically server/domain-wide) endpoints,
    which may be useful either for this actor or someone referencing this actor.
    Documentation: https://www.w3.org/TR/activitypub/#actor-objects
    """

    # Ensure camel case for all aliases
    model_config = ConfigDict(alias_generator=_must_be_camel, populate_by_name=True)

    # Properties
    proxy_url: HttpUrl = None
    oauth_authorization_endpoint: HttpUrl = None
    oauth_token_endpoint: HttpUrl = None
    provide_client_key: HttpUrl = None
    sign_client_key: HttpUrl = None
    shared_inbox: HttpUrl = None


"""
ACTOR TYPES
"""


class ActorModel(ObjectModel):
    """
    Actor types are Object types that are capable of performing activities.
    ActivityPub adds properties: https://www.w3.org/TR/activitypub/#actors
    """

    # Type does not need to be literal for propogation
    type: str = "Actor"

    # Properties
    preferred_username: str = None
    inbox: ObjectModel = None
    outbox: ObjectModel = None
    following: ObjectModel = None
    followers: ObjectModel = None
    liked: ObjectModel = None
    streams: List[ObjectModel] = None
    endpoints: Union[HttpUrl, EndpointsModel] = None

    # Validation
    _actor_collections = field_validator(
        "following", "followers", "liked", mode="before"
    )(validate_collections)
    _actor_list_collections = field_validator("streams", mode="before")(
        validate_list_collections
    )
    _actor_orderedcollections = field_validator("inbox", "outbox", mode="before")(
        validate_ordered_collections
    )
    _actor_httpurls_or_endpoints = field_validator("endpoints", mode="before")(
        validate_httpurls_or_endpoints
    )


class ApplicationModel(ActorModel):
    """
    Describes a software application.
    """

    # Type
    type: Literal["Application"] = "Application"


class GroupModel(ActorModel):
    """
    Represents a formal or informal collective of Actors.
    """

    # Type
    type: Literal["Group"] = "Group"


class OrganizationModel(ActorModel):
    """
    Represents an organization.
    """

    # Type
    type: Literal["Organization"] = "Organization"


class PersonModel(ActorModel):
    """
    Represents an individual person.
    """

    # Type
    type: Literal["Person"] = "Person"


class ServiceModel(ActorModel):
    """
    Represents a service of any kind.
    """

    # Type
    type: Literal["Service"] = "Service"
