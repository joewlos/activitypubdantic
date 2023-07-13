# -*- coding: utf-8 -*-
"""
The classes in this package are designed to enable interactions with ActivityPub data.
To make a class instance for your data, call get_class() with your input JSON as the argument. \n
The functions for retrieving Pydantic models are designed to validate class data. \n
The Pydantic models may be used independently of the functions and classes to validate data 
in your own custom functions, classes, or FastAPI routes. \n
The ActivityPub protocol is cited throughout this documentation and is available here: 
https://www.w3.org/TR/activitypub/ \n
The GitHub repo containing this project, which includes examples and licensing information,
is available here: https://github.com/joewlos/activitypubdantic
"""
from activitypubdantic.get_class import get_class, get_class_from_model
from activitypubdantic.get_model import get_model, get_model_data, get_model_json
