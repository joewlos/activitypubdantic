# -*- coding: utf-8 -*-
"""
ACTIVITY PYDANTIC MODELS FOR VALIDATION \n
Documentation: https://www.w3.org/TR/activitystreams-vocabulary/#activity-types
"""
# Import Pydantic models and types
from pydantic import field_validator, model_validator
from typing import List, Literal, Union

# Import core models that are required for the actor definition
# Not all will be directly called
from activitypubdantic.models.core import (
    ActivityModel,
    CollectionModel,
    CollectionPageModel,
    ImageModel,
    IntransitiveActivityModel,
    LinkModel,
    PlaceModel,
    ObjectModel,
    must_be_links_or_objects,
    must_be_list,
)


"""
ACTIVITY TYPES
"""


class AcceptModel(ActivityModel):
    """
    Indicates that the actor accepts the object.
    """

    # Type
    type: Literal["Accept"] = "Accept"


class TentativeAcceptModel(ActivityModel):
    """
    A specialization of Accept indicating that the acceptance is tentative.
    """

    # Type
    type: Literal["TentativeAccept"] = "TentativeAccept"


class AddModel(ActivityModel):
    """
    Indicates that the actor has added the object to the target.
    """

    # Type
    type: Literal["Add"] = "Add"


class ArriveModel(IntransitiveActivityModel):
    """
    An IntransitiveActivity that indicates that the actor has arrived at the location.
    """

    # Type
    type: Literal["Arrive"] = "Arrive"


class CreateModel(ActivityModel):
    """
    Indicates that the actor has created the object.
    """

    # Type
    type: Literal["Create"] = "Create"


class DeleteModel(ActivityModel):
    """
    Indicates that the actor has deleted the object.
    """

    # Type
    type: Literal["Delete"] = "Delete"


class FollowModel(ActivityModel):
    """
    Indicates that the actor is "following" the object.
    """

    # Type
    type: Literal["Follow"] = "Follow"


class IgnoreModel(ActivityModel):
    """
    Indicates that the actor is ignoring the object.
    """

    # Type
    type: Literal["Ignore"] = "Ignore"


class JoinModel(ActivityModel):
    """
    Indicates that the actor is joining the object.
    """

    # Type
    type: Literal["Join"] = "Join"


class LeaveModel(ActivityModel):
    """
    Indicates that the actor is leaving the object.
    """

    # Type
    type: Literal["Leave"] = "Leave"


class LikeModel(ActivityModel):
    """
    Indicates that the actor is likes the object.
    """

    # Type
    type: Literal["Like"] = "Like"


class OfferModel(ActivityModel):
    """
    Indicates that the actor is offering the object.
    """

    # Type
    type: Literal["Offer"] = "Offer"


class InviteModel(OfferModel):
    """
    A specialization of Offer in which the actor is extending
    an invitation for the object to the target.
    """

    # Type
    type: Literal["Invite"] = "Invite"


class RejectModel(ActivityModel):
    """
    Indicates that the actor is rejecting the object.
    """

    # Type
    type: Literal["Reject"] = "Reject"


class TentativeRejectModel(RejectModel):
    """
    A specialization of Reject in which the rejection is considered tentative.
    """

    # Type
    type: Literal["TentativeReject"] = "TentativeReject"


class RemoveModel(ActivityModel):
    """
    Indicates that the actor is removing the object.
    """

    # Type
    type: Literal["Remove"] = "Remove"


class UndoModel(ActivityModel):
    """
    Indicates that the actor is undoing the object.
    """

    # Type
    type: Literal["Undo"] = "Undo"


class UpdateModel(ActivityModel):
    """
    Indicates that the actor is updating the object.
    """

    # Type
    type: Literal["Update"] = "Update"


class ViewModel(ActivityModel):
    """
    Indicates that the actor is viewing the object.
    """

    # Type
    type: Literal["View"] = "View"


class ListenModel(ActivityModel):
    """
    Indicates that the actor is listening to the object.
    """

    # Type
    type: Literal["Listen"] = "Listen"


class ReadModel(ActivityModel):
    """
    Indicates that the actor is reading the object.
    """

    # Type
    type: Literal["Read"] = "Read"


class MoveModel(ActivityModel):
    """
    Indicates that the actor is moving the object from origin to target.
    """

    # Type
    type: Literal["Move"] = "Move"


class TravelModel(IntransitiveActivityModel):
    """
    Indicates that the actor is traveling from origin to target.
    """

    # Type
    type: Literal["Travel"] = "Travel"


class AnnounceModel(ActivityModel):
    """
    Indicates that the actor is calling the target's attention to the object.
    """

    # Type
    type: Literal["Announce"] = "Announce"


class BlockModel(IgnoreModel):
    """
    Indicates that the actor is blocking the object. Blocking is a stronger form of Ignore.
    """

    # Type
    type: Literal["Block"] = "Block"


class FlagModel(ActivityModel):
    """
    Flagging is defined in the sense common to many social platforms
    as reporting content as being inappropriate for any number of reasons.
    """

    # Type
    type: Literal["Flag"] = "Flag"


class DislikeModel(ActivityModel):
    """
    Indicates that the actor dislikes the object.
    """

    # Type
    type: Literal["Dislike"] = "Dislike"


class QuestionModel(IntransitiveActivityModel):
    """
    Represents a question being asked.
    Note, in Mastodon, this is an Object, not an Activity, with a "votersCount" property.
    """

    # Type
    type: Literal["Question"] = "Question"

    # Properties
    one_of: List[Union[LinkModel, ObjectModel]] = None
    any_of: List[Union[LinkModel, ObjectModel]] = None
    closed: bool = None
    votersCount: int = None  # In Mastodon

    # Correct to list of Links or Objects
    @field_validator(
        "one_of",
        "any_of",
        mode="before",
    )
    def validate_links_or_objects(cls, v):
        v = must_be_list(v)
        for i, item in enumerate(v):
            if item:
                v[i] = must_be_links_or_objects(item)
        return v

    # Only one of one_of or any_of may be set
    @model_validator(mode="after")
    def validate_one_of_or_any_of(cls, m: "QuestionModel"):
        any_of = m.any_of
        one_of = m.one_of
        if any_of and one_of:
            raise ValueError("Only one of the answer types may be set.")
        return m
