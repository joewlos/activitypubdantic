# -*- coding: utf-8 -*-
"""
LINK PYDANTIC MODELS FOR VALIDATION \n
Documentation: https://www.w3.org/TR/activitystreams-vocabulary/#object-types
"""
# Import Pydantic models and types
from typing import Literal

# Import core models that are required for the actor definition
# Not all will be directly called
from activitypubdantic.models.core import LinkModel, ObjectModel

"""
OBJECT TYPES
"""


class MentionModel(LinkModel):
    """
    A specialized Link that represents an @mention.
    """

    # Type
    type: Literal["Mention"] = "Mention"
