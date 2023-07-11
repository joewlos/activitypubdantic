# -*- coding: utf-8 -*-
"""
RUN TESTS FOR ACTIVITYPUBDANTIC USING JSON EXAMPLES
"""
# Import functions and models
import activitypubdantic as ap

# Import other packages
import json


class TestActivityPub:
    """
    TESTS FOR ACTIVITYPUB
    Check that models are able to load examples from the ActivityPub spec.
    Check that classes also load examples and perform expected functions.
    All examples are available here: https://www.w3.org/TR/activitypub/#Overview
    """

    def test_person(self):
        """
        Test that the Person model can load the example from the spec.
        """
        with open("json/activitypub/person.json", "r") as f:
            person_json = json.load(f)

        # Load the model for a person
        person_model = ap.get_model(person_json)
        person_verbose = ap.get_model_json(person_json, verbose=True, indent=0)
        person_short = ap.get_model_json(person_json, verbose=False, indent=0)

        # Outputs for comparisons
        output_verbose = json.dumps(
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "Person",
                "id": "https://social.example/alyssa/",
                "name": "Alyssa P. Hacker",
                "summary": "Lisp enthusiast hailing from MIT",
                "preferredUsername": "alyssa",
                "inbox": {
                    "@context": "https://www.w3.org/ns/activitystreams",
                    "type": "OrderedCollection",
                    "id": "https://social.example/alyssa/inbox/",
                },
                "outbox": {
                    "@context": "https://www.w3.org/ns/activitystreams",
                    "type": "OrderedCollection",
                    "id": "https://social.example/alyssa/outbox/",
                },
                "following": {
                    "@context": "https://www.w3.org/ns/activitystreams",
                    "type": "Collection",
                    "id": "https://social.example/alyssa/following/",
                },
                "followers": {
                    "@context": "https://www.w3.org/ns/activitystreams",
                    "type": "Collection",
                    "id": "https://social.example/alyssa/followers/",
                },
                "liked": {
                    "@context": "https://www.w3.org/ns/activitystreams",
                    "type": "Collection",
                    "id": "https://social.example/alyssa/liked/",
                },
            },
            indent=0,
        )
        output_short = json.dumps(
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "Person",
                "id": "https://social.example/alyssa/",
                "name": "Alyssa P. Hacker",
                "summary": "Lisp enthusiast hailing from MIT",
                "preferredUsername": "alyssa",
                "inbox": "https://social.example/alyssa/inbox/",
                "outbox": "https://social.example/alyssa/outbox/",
                "following": "https://social.example/alyssa/following/",
                "followers": "https://social.example/alyssa/followers/",
                "liked": "https://social.example/alyssa/liked/",
            },
            indent=0,
        )

        # Load the class
        person_class = ap.get_class(person_json)

        # Assert that the data is the same
        assert person_model.name == person_class.model.name == person_json["name"]
        assert person_model.type == person_json["type"] == "Person"
        assert person_verbose == output_verbose
        assert person_short == output_short


class TestActivityStreams:
    """
    TESTS FOR ACTIVITYSTREAMS
    Check that models are able to load examples from the ActivityStreams spec.
    Check that classes also load examples and perform expected functions.
    All examples are available here: https://www.w3.org/TR/activitystreams-vocabulary
    """

    def test_person(self):
        """
        Test that the Person model and class can load the example from the spec.
        """
        with open("json/activitystreams/person.json", "r") as f:
            person_json = json.load(f)

        # Load the model for a person
        person_model = ap.get_model(person_json)
        person_verbose = ap.get_model_json(person_json, verbose=True, indent=0)
        person_short = ap.get_model_json(person_json, verbose=False, indent=0)

        # Outputs for comparisons
        output_verbose = json.dumps(
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "Person",
                "name": "Sally Smith",
            },
            indent=0,
        )
        output_short = json.dumps(
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "Person",
                "name": "Sally Smith",
            },
            indent=0,
        )

        # Load the class
        person_class = ap.get_class(person_json)

        # Assert that the data is valid
        assert person_model.name == person_class.model.name == person_json["name"]
        assert person_model.type == person_json["type"] == "Person"
        assert person_verbose == output_verbose
        assert person_short == output_short
