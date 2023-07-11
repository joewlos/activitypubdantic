# -*- coding: utf-8 -*-
"""
The classes in this package are designed to enable interactions with ActivityPub data.
To use a class, call get_class() with your input JSON to return a class instance. \n
The functions for retrieving Pydantic models are designed to validate class data. \n
The Pydantic models may be used independently of the functions and classes to validate data 
in your own custom functions or FastAPI routes. \n
The ActivityPub protocol is cited throughout this documentation and is available here: 
https://www.w3.org/TR/activitypub/
"""
from activitypubdantic.get_class import get_class
from activitypubdantic.get_model import get_model, get_model_data, get_model_json
