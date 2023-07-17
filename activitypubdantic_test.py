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
        Also test that the JSON matches the expected output for verbose true or false.
        """
        with open("json/activitypub/person.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_verbose = ap.get_model_json(input_json, verbose=True, indent=0)
        output_short = ap.get_model_json(input_json, verbose=False, indent=0)
        output_class = ap.get_class(input_json)

        # Outputs for comparisons
        match_verbose = json.dumps(
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
        match_short = json.dumps(
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

        # Assert that the data is the same
        assert output_model.name == output_class.model.name == input_json["name"]
        assert output_model.type == input_json["type"] == "Person"
        assert output_verbose == match_verbose
        assert output_short == match_short

    def test_note(self):
        """
        Test that the Note model can load the example from the spec.
        """
        with open("json/activitypub/note.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_class = ap.get_class(input_json)

        # Assert that the data is the same
        assert (
            output_model.content == output_class.model.content == input_json["content"]
        )
        assert output_model.type == input_json["type"] == "Note"

    def test_create(self):
        """
        Test that the Create model can load the example from the spec.
        """
        with open("json/activitypub/create.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_class = ap.get_class(input_json)
        output_data = output_class.data()

        # Assert that the data is the same
        assert str(output_data["id"]) == input_json["id"]
        assert (
            output_model.type == input_json["type"] == output_data["type"] == "Create"
        )

    def test_like(self):
        """
        Test that the Like model can load the example from the spec.
        """
        with open("json/activitypub/like.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_class = ap.get_class(input_json)
        output_data = output_class.data()

        # Assert that the data is the same
        assert len(output_data["to"]) == len(input_json["to"])
        assert set(output_class.deliver_to()) == set(
            [
                "https://rhiaro.co.uk/#amy",
                "https://dustycloud.org/followers",
                "https://e14n.com/evan",
                "https://rhiaro.co.uk/followers/",
            ]
        )
        assert output_model.type == input_json["type"] == output_data["type"] == "Like"

    def test_article(self):
        """
        Test that the Article model can load the example from the spec.
        """
        with open("json/activitypub/article.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_class = ap.get_class(input_json)
        output_data = output_class.data()

        # Assert that the data is the same
        assert output_data["name"] == input_json["name"]
        assert set(output_class.deliver_to()) == set(
            [
                "https://e14n.com/evan",
                "https://rhiaro.co.uk/followers/",
            ]
        )
        assert output_data["content"] == input_json["content"]
        assert (
            output_model.type == input_json["type"] == output_data["type"] == "Article"
        )


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
        Also test that the JSON matches the expected output for verbose true or false.
        """
        with open("json/activitystreams/person.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_verbose = ap.get_model_json(input_json, verbose=True, indent=0)
        output_short = ap.get_model_json(input_json, verbose=False, indent=0)
        output_class = ap.get_class(input_json)

        # Outputs for comparisons
        match_verbose = json.dumps(
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "Person",
                "name": "Sally Smith",
            },
            indent=0,
        )
        match_short = json.dumps(
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "Person",
                "name": "Sally Smith",
            },
            indent=0,
        )

        # Assert that the data is valid
        assert output_model.name == output_class.model.name == input_json["name"]
        assert output_model.type == input_json["type"] == "Person"
        assert output_verbose == match_verbose
        assert output_short == match_short

    def test_accept(self):
        """
        Test that the Accept model can load the example from the spec.
        """
        with open("json/activitystreams/accept.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_class = ap.get_class(input_json)
        output_data = output_class.data()

        # Assert that the data is the same
        assert output_data["summary"] == input_json["summary"]
        assert (
            output_model.type == input_json["type"] == output_data["type"] == "Accept"
        )

    def test_article(self):
        """
        Test that the Article model can load the example from the spec.
        """
        with open("json/activitystreams/article.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_class = ap.get_class(input_json)
        output_data = output_class.data()

        # Assert that the data is the same
        assert output_data["content"] == input_json["content"]
        assert (
            output_model.type == input_json["type"] == output_data["type"] == "Article"
        )

    def test_image(self):
        """
        Test that the Image model can load the example from the spec.
        """
        with open("json/activitystreams/image.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_class = ap.get_class(input_json)
        output_data = output_class.data()

        # Assert that the data is the same
        assert output_data["name"] == input_json["name"]
        assert len(output_data["url"]) == len(input_json["url"])
        assert output_model.type == input_json["type"] == output_data["type"] == "Image"

    def test_place(self):
        """
        Test that the Place model can load the example from the spec.
        """
        with open("json/activitystreams/place.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_class = ap.get_class(input_json)
        output_data = output_class.data()

        # Assert that the data is the same
        assert output_data["name"] == input_json["name"]
        assert output_data["latitude"] == input_json["latitude"]
        assert output_model.type == input_json["type"] == output_data["type"] == "Place"

    def test_tombsone(self):
        """
        Test that the Tombstone model can load the example from the spec.
        """
        with open("json/activitystreams/tombstone.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_class = ap.get_class(input_json)
        output_data = output_class.data()

        # Assert that the data is the same
        assert output_data["name"] == input_json["name"]
        assert output_data["totalItems"] == input_json["totalItems"]
        assert len(output_data["orderedItems"]) == len(input_json["orderedItems"])
        assert (
            output_model.type
            == input_json["type"]
            == output_data["type"]
            == "OrderedCollection"
        )  # TODO: Why is this OrderedCollection?

    def test_collection(self):
        """
        Test that the Collection model can load the example from the spec.
        """
        with open("json/activitystreams/collection.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_class = ap.get_class(input_json)
        output_data = output_class.data()

        # Assert that the data is the same
        assert output_data["summary"] == input_json["summary"]
        assert len(output_data["items"]) == len(input_json["items"])
        assert (
            output_model.type
            == input_json["type"]
            == output_data["type"]
            == "Collection"
        )

    def test_question(self):
        """
        Test that the Question model can load the example from the spec.
        """
        with open("json/activitystreams/question.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_class = ap.get_class(input_json)
        output_data = output_class.data()

        # Assert that the data is the same
        assert output_data["content"] == input_json["content"]
        assert output_data["replies"]["type"] == input_json["replies"]["type"]
        assert len(output_data["oneOf"]) == len(input_json["oneOf"])
        assert (
            output_model.type == input_json["type"] == output_data["type"] == "Question"
        )

    def test_add(self):
        """
        Test that the Add model can load the example from the spec.
        """
        with open("json/activitystreams/add.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_class = ap.get_class(input_json)
        output_data = output_class.data()

        # Assert that the data is the same
        assert output_data["summary"] == input_json["summary"]
        assert output_data["actor"][0]["type"] == input_json["actor"]["type"]
        assert output_data["target"][0]["name"] == input_json["target"]["name"]
        assert output_model.type == input_json["type"] == output_data["type"] == "Add"

    def test_move(self):
        """
        Test that the Move model can load the example from the spec.
        """
        with open("json/activitystreams/move.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_class = ap.get_class(input_json)
        output_data = output_class.data()

        # Assert that the data is the same
        assert output_data["summary"] == input_json["summary"]
        assert output_data["target"][0]["type"] == input_json["target"]["type"]
        assert output_data["target"][0]["name"] == input_json["target"]["name"]
        assert output_model.type == input_json["type"] == output_data["type"] == "Move"


class TestMastodon:
    """
    TESTS FOR MASTODON
    Check that models are able to load examples from the Mastodon.
    Check that classes also load examples and perform expected functions.
    All examples are available here: https://www.w3.org/TR/activitystreams-vocabulary
    """

    def test_poll(self):
        """
        Test that the Question model and class can load the poll example from the spec.
        """
        with open("json/mastodon/poll.json", "r") as f:
            poll_json = json.load(f)

        # Load the model and class
        poll_model = ap.get_model(poll_json)
        poll_verbose = ap.get_model_json(poll_json, verbose=True, indent=0)
        poll_short = ap.get_model_json(poll_json, verbose=False, indent=0)
        poll_class = ap.get_class(poll_json)

        # Outputs for comparisons
        match_verbose = json.dumps(
            {
                "@context": [
                    "https://www.w3.org/ns/activitystreams",
                    {
                        "toot": "http://joinmastodon.org/ns#",
                        "votersCount": "toot:votersCount",
                    },
                    "https://w3id.org/security/v1",
                ],
                "type": "Question",
                "id": "https://polls.example.org/users/sally/statuses/1234",
                "attributedTo": [
                    {
                        "@context": "https://www.w3.org/ns/activitystreams",
                        "type": "Object",
                        "id": "https://polls.example.org/users/sally",
                    }
                ],
                "content": "<p>What is your favorite starter pokemon?</p>",
                "endTime": "2023-01-01T20:04:45Z",
                "published": "2023-01-01T01:00:00Z",
                "url": ["https://polls.example.org/@sally/1234"],
                "oneOf": [
                    {
                        "@context": "https://www.w3.org/ns/activitystreams",
                        "type": "Note",
                        "name": "Charmander",
                        "replies": {
                            "@context": "https://www.w3.org/ns/activitystreams",
                            "type": "Collection",
                            "total_items": 5,
                        },
                    },
                    {
                        "@context": "https://www.w3.org/ns/activitystreams",
                        "type": "Note",
                        "name": "Bulbasaur",
                        "replies": {
                            "@context": "https://www.w3.org/ns/activitystreams",
                            "type": "Collection",
                            "total_items": 2,
                        },
                    },
                    {
                        "@context": "https://www.w3.org/ns/activitystreams",
                        "type": "Note",
                        "name": "Squirtle",
                        "replies": {
                            "@context": "https://www.w3.org/ns/activitystreams",
                            "type": "Collection",
                            "total_items": 3,
                        },
                    },
                ],
                "closed": "2023-01-01T20:04:45Z",
                "votersCount": 10,
            },
            indent=0,
        )
        match_short = json.dumps(
            {
                "@context": [
                    "https://www.w3.org/ns/activitystreams",
                    {
                        "toot": "http://joinmastodon.org/ns#",
                        "votersCount": "toot:votersCount",
                    },
                    "https://w3id.org/security/v1",
                ],
                "type": "Question",
                "id": "https://polls.example.org/users/sally/statuses/1234",
                "attributedTo": ["https://polls.example.org/users/sally"],
                "content": "<p>What is your favorite starter pokemon?</p>",
                "endTime": "2023-01-01T20:04:45Z",
                "published": "2023-01-01T01:00:00Z",
                "url": ["https://polls.example.org/@sally/1234"],
                "oneOf": [
                    {
                        "@context": "https://www.w3.org/ns/activitystreams",
                        "type": "Note",
                        "name": "Charmander",
                        "replies": {
                            "@context": "https://www.w3.org/ns/activitystreams",
                            "type": "Collection",
                            "total_items": 5,
                        },
                    },
                    {
                        "@context": "https://www.w3.org/ns/activitystreams",
                        "type": "Note",
                        "name": "Bulbasaur",
                        "replies": {
                            "@context": "https://www.w3.org/ns/activitystreams",
                            "type": "Collection",
                            "total_items": 2,
                        },
                    },
                    {
                        "@context": "https://www.w3.org/ns/activitystreams",
                        "type": "Note",
                        "name": "Squirtle",
                        "replies": {
                            "@context": "https://www.w3.org/ns/activitystreams",
                            "type": "Collection",
                            "total_items": 3,
                        },
                    },
                ],
                "closed": "2023-01-01T20:04:45Z",
                "votersCount": 10,
            },
            indent=0,
        )

        # Assert that the data is valid
        assert poll_model.content == poll_class.model.content == poll_json["content"]
        assert poll_model.type == poll_json["type"] == "Question"
        assert poll_verbose == match_verbose
        assert poll_short == match_short

    def test_person(self):
        """
        Test that the Person model can load the example from the spec.
        """
        with open("json/mastodon/person.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_class = ap.get_class(input_json)
        output_data = output_class.data()

        # Assert that the data is the same
        assert output_data["preferredUsername"] == input_json["preferredUsername"]
        assert (
            output_model.type == input_json["type"] == output_data["type"] == "Person"
        )

    def test_create(self):
        """
        Test that the Create model can load the example from the spec.
        """
        with open("json/mastodon/create.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_class = ap.get_class(input_json)
        output_data = output_class.data()

        # Assert that the data is the same
        assert output_data["object"]["type"] == input_json["object"]["type"] == "Note"
        assert (
            output_model.type == input_json["type"] == output_data["type"] == "Create"
        )

    def test_follow(self):
        """
        Test that the Follow model can load the example from the spec.
        """
        with open("json/mastodon/follow.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_class = ap.get_class(input_json)
        output_data = output_class.data()

        # Assert that the data is the same
        assert output_data["object"]["type"] == "Object"
        assert (
            output_model.type == input_json["type"] == output_data["type"] == "Follow"
        )

    def test_accept(self):
        """
        Test that the Accept model can load the example from the spec.
        """
        with open("json/mastodon/accept.json", "r") as f:
            input_json = json.load(f)

        # Load the model and class
        output_model = ap.get_model(input_json)
        output_class = ap.get_class(input_json)
        output_data = output_class.data()

        # Assert that the data is the same
        assert output_data["actor"][0]["type"] == "Object"
        assert set(output_class.deliver_to()) == set(
            ["https://activitypub.academy/users/dibutus_godorviol"]
        )
        assert len(output_data["to"]) == len(input_json["to"]) == 1
        assert (
            output_model.type == input_json["type"] == output_data["type"] == "Accept"
        )
