# -*- coding: utf-8 -*-
"""
FUNCTIONS FOR SELECTING PYDANTIC MODELS TO VALIDATE DATA
"""
# Import Pydantic models
from activitypubdantic.models import *

# Import other packages
import json
from typing import Union


"""
MAPPING DICTIONARY
"""


# Map type names to their ActivityPub models
_MODEL_MAPPINGS = {
    "Accept": AcceptModel,  # Activity Section
    "Add": AddModel,
    "Accounce": AnnounceModel,
    "Arrive": ArriveModel,
    "Block": BlockModel,
    "Create": CreateModel,
    "Delete": DeleteModel,
    "Dislike": DislikeModel,
    "Flag": FlagModel,
    "Follow": FollowModel,
    "Ignore": IgnoreModel,
    "Invite": InviteModel,
    "Join": JoinModel,
    "Leave": LeaveModel,
    "Like": LikeModel,
    "Listen": ListenModel,
    "Move": MoveModel,
    "Offer": OfferModel,
    "Question": QuestionModel,
    "Read": ReadModel,
    "Reject": RejectModel,
    "Remove": RemoveModel,
    "TentativeAccept": TentativeAcceptModel,
    "TentativeReject": TentativeRejectModel,
    "Travel": TravelModel,
    "Undo": UndoModel,
    "Update": UpdateModel,
    "View": ViewModel,
    "Actor": ActorModel,  # Actor Section
    "Application": ApplicationModel,
    "Group": GroupModel,
    "Organization": OrganizationModel,
    "Person": PersonModel,
    "Service": ServiceModel,
    "Activity": ActivityModel,  # Core Section
    "Collection": CollectionModel,
    "CollectionPage": CollectionPageModel,
    "IntransitiveActivity": IntransitiveActivityModel,
    "Link": LinkModel,
    "Object": ObjectModel,
    "OrderedCollection": OrderedCollectionModel,
    "OrderedCollectionPage": OrderedCollectionPageModel,
    "Mention": MentionModel,  # Link Section
    "Article": ArticleModel,  # Object Section
    "Audio": AudioModel,
    "Document": DocumentModel,
    "Event": EventModel,
    "Image": ImageModel,
    "Note": NoteModel,
    "Page": PageModel,
    "Place": PlaceModel,
    "Profile": ProfileModel,
    "Relationship": RelationshipModel,
    "Tombstone": TombstoneModel,
    "Video": VideoModel,
}


"""
FUNCTIONS
"""


def get_model(
    input_json: dict,
) -> Union[ActivityModel, CollectionModel, LinkModel, ObjectModel]:
    """
    Return the Pydantic model for the input JSON.
    The input JSON must include a type field, which is used to select the right model.
    """
    output = None
    if "type" in input_json and input_json["type"] in _MODEL_MAPPINGS:
        output = _MODEL_MAPPINGS[input_json["type"]](**input_json)

    # If there is no type, throw an error – this is required
    elif "type" not in input_json:
        raise ValueError("Input JSON must include a type.")

    # If there is no output, throw an error – this type is not supported
    if not output:
        raise ValueError(f"This type is not supported.")

    # Return the output model, formatted according to settings
    return output


def get_model_data(
    input_json: dict,
    by_alias: bool = True,
    exclude_none: bool = True,
    verbose: bool = True,
    output_json: bool = False,
) -> dict:
    """
    Return the Pydantic model as a dictionary.
    Formatting may be specified in the keyword arguments.
    """
    model_output = get_model(input_json)

    # Dump the model with settings
    if not output_json:
        output = model_output.model_dump(by_alias=by_alias, exclude_none=exclude_none)
    else:  # Need to execute from Pydantic and then reload for JSON
        output = model_output.model_dump_json(
            by_alias=by_alias, exclude_none=exclude_none
        )
        output = json.loads(output)

    # If not verbose, change all nested data to only represent IDs
    if not verbose:
        for k, v in output.items():
            if isinstance(v, dict) and "id" in v:  # Handle Objects
                output[k] = v["id"]
            elif isinstance(v, dict) and "href" in v:  # Handle Links
                output[k] = v["href"]
            elif isinstance(v, list):  # Handle Collections
                new_lst = []
                for item in v:
                    if isinstance(item, dict) and "id" in item:  # Handle Objects
                        new_lst.append(item["id"])
                    elif isinstance(item, dict) and "href" in item:  # Handle Links
                        new_lst.append(item["href"])
                    else:
                        new_lst.append(item)
                output[k] = new_lst

    # Return the output data
    return output


def get_model_json(
    input_json: dict,
    by_alias: bool = True,
    exclude_none: bool = True,
    verbose: bool = True,
    indent: int = 2,
) -> dict:
    """
    Return the Pydantic model as a JSON string.
    Formatting may be specified in the keyword arguments.
    """
    model_output = get_model_data(
        input_json,
        by_alias=by_alias,
        exclude_none=exclude_none,
        verbose=verbose,
        output_json=True,
    )

    # Dump as a JSON string
    output = json.dumps(model_output, indent=indent)

    # Return the output JSON
    return output
