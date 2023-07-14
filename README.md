# ActivityPubdantic

### Validate and Interact with ActivityPub JSON

[GitHub Repository](https://github.com/joewlos/activitypubdantic)

[ActivityPubdantic Documentation](https://www.joewlos.com/activitypubdantic/)

[ActivityPub Protocol](https://www.w3.org/TR/activitypub/)

[ActivityStreams Specification](https://www.w3.org/TR/activitystreams-vocabulary/)

## Development Note

The current version of **ActivityPubdantic** available on PyPi is still undergoing testing and upgrades. If you plan to use **ActivityPubdantic** in your project, please keep in mind that its features and capabilities are likely to evolve and grow. Please see the [contributing](#contributing) section of this README for further information about **ActivityPubdantic**'s development.

## What Is ActivityPubdantic?

**ActivityPubdantic** is a suite of tools for validating ActivityPub JSON and constructing consistent representations of ActivityPub notifications and content. [Pydantic](https://docs.pydantic.dev/latest/) models enable the validation logic and can be imported for use in custom-coded classes or FastAPI routes.

## Why Does ActivityPub JSON Require Validation?

[ActivityPub](https://www.w3.org/TR/activitypub/) is a protocol for decentralized social networking. It defines client-to-server and server-to-server interactions and relies on [ActivityStreams](https://www.w3.org/TR/activitystreams-vocabulary/#dfn-orderedcollection) for its vocabulary. Many of the protocol's definitions are purposefully unrestrictive, giving developers the freedom to implement only the features relevant to their products or to adjust to meet their particular requirements.

However, that flexibility presents challenges for assessing data validity and simplifying developers' code. **ActivityPubdantic** helps solve those challenges by using ActivityPub's "type" field to identify proper checks for other fields and standardize their structures. [Examples](#examples) are available in the sections below.

[Mastodon](https://docs.joinmastodon.org/spec/activitypub/) supports ActivityPub, and Meta's [Threads](https://apps.apple.com/us/app/threads-an-instagram-app/id6446901002) app plans to conform to the protocol sometime in the [near future](https://techcrunch.com/2023/07/05/adam-mosseri-says-metas-threads-app-wont-have-activitypub-support-at-launch/). **ActivityPubdantic** includes a test suite, which uses examples from ActivityPub, ActivityStreams, and Mastodon to test its parsing and validation. As Threads and other platforms implement ActivityPub, those tests (and more broadly, this package) will be updated to stay current.

## Installation

Install the package with `pip`:

```console
pip install activitypubdantic
```

Most developer use cases will use one or both of the following import statements:

```python
# Use classes for validation and common operations
import activitypubdantic as ap

# Use models in FastAPI routes
from activitypubdantic.models import *
```

## Examples

The following examples include simple use cases and code snippets for **ActivityPubdantic**. For a more thorough listing of **ActivityPubdantic's** classes, functions, and models, check out its [documentation](https://www.joewlos.com/activitypubdantic/).

### Parsing Activity, Collection, Link, and Object JSON

`Activities`, `Collections`, `Links`, and `Objects` are the core concepts around which ActivityPub and ActivityStreams are built. By reducing their complexity and standardizing their representation, **ActivityPubdantic** helps resolve potential pain points for developers.

ActivityPub's protocol includes an [example](https://www.w3.org/TR/activitypub/#client-to-server-interactions) of a `Like` activity. The example's `to` field is a list, while its `cc` field is a string. Both formats are valid, but they require slightly different handling in subsequent lines of code. To resolve that difference, **ActivityPubdantic** rewrites it, so those fields are always presented as lists of dictionaries.

```python
import activitypubdantic as ap

# Example JSON from ActivityPub documentation
example_json = {
  "@context": ["https://www.w3.org/ns/activitystreams",
               {"@language": "en"}],
  "type": "Like",
  "actor": "https://dustycloud.org/chris/",
  "name": "Chris liked 'Minimal ActivityPub update client'",
  "object": "https://rhiaro.co.uk/2016/05/minimal-activitypub",
  "to": ["https://rhiaro.co.uk/#amy",
         "https://dustycloud.org/followers",
         "https://rhiaro.co.uk/followers/"],
  "cc": "https://e14n.com/evan"
}

# Get the appropriate class, which is determined by the type field
output_class = ap.get_class(example_json)

# Produce the parsed and validated JSON string
output_json = output_class.json()
print(output_json)  # See JSON below
```

`get_class()` reads the `example_json` and uses its type to select the applicable Pydantic model. It then uses Pydantic validators for each field to assert they comply with the protocol and then restructures them.

The `output_json` is longer and, at first glance, more complex. But because it contains types for each item in its fields and it standardizes the structures of similar fields – like `to` and `cc` – it is more descriptive and easier to consistently manipulate.

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    {
      "@language": "en"
    }
  ],
  "type": "Like",
  "name": "Chris liked 'Minimal ActivityPub update client'",
  "to": [
    {
      "@context": "https://www.w3.org/ns/activitystreams",
      "type": "Object",
      "id": "https://rhiaro.co.uk/#amy"
    },
    {
      "@context": "https://www.w3.org/ns/activitystreams",
      "type": "Object",
      "id": "https://dustycloud.org/followers"
    },
    {
      "@context": "https://www.w3.org/ns/activitystreams",
      "type": "Object",
      "id": "https://rhiaro.co.uk/followers/"
    }
  ],
  "cc": [
    {
      "@context": "https://www.w3.org/ns/activitystreams",
      "type": "Object",
      "id": "https://e14n.com/evan"
    }
  ],
  "actor": [
    {
      "@context": "https://www.w3.org/ns/activitystreams",
      "type": "Object",
      "id": "https://dustycloud.org/chris/"
    }
  ],
  "object": {
    "@context": "https://www.w3.org/ns/activitystreams",
    "type": "Object",
    "id": "https://rhiaro.co.uk/2016/05/minimal-activitypub"
  }
}
```

However, not every project requires this degree of granularity. For example, some servers may already have logic that ignores additional fields and only iterates through `id` URLs in the JSON.

```python
# Use the verbose keyword argument
short_output_json = output_class.json(verbose=False)
print(short_output_json)  # See JSON below
```

Setting `verbose=False` shortens the output, retaining consistency but eliminating unneeded data for simpler implementations.

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    {
      "@language": "en"
    }
  ],
  "type": "Like",
  "name": "Chris liked 'Minimal ActivityPub update client'",
  "to": [
    "https://rhiaro.co.uk/#amy",
    "https://dustycloud.org/followers",
    "https://rhiaro.co.uk/followers/"
  ],
  "cc": ["https://e14n.com/evan"],
  "actor": ["https://dustycloud.org/chris/"],
  "object": "https://rhiaro.co.uk/2016/05/minimal-activitypub"
}
```

### Validating FastAPI Request Bodies

[FastAPI](https://fastapi.tiangolo.com/) uses Pydantic models to validate [request bodies](https://fastapi.tiangolo.com/tutorial/body/). After importing **ActivityPubdantic** models directly, developers can automatically validate requests and then use the `get_class_from_model()` function to smoothly interact with the ActivityPub JSON.

When the same `Like` activity is sent in the POST request to `/outbox`, the request body is validated by FastAPI and loaded into an **ActivityPubdantic** class to produce clean JSON.

```python
import activitypubdantic as ap
from activitypubdantic.models import *
from fastapi import FastAPI, Response

app = FastAPI()

# Route for an ActivityPub outbox
@app.post("/outbox", status_code=201)
async def outbox(activity: ActivityModel, response: Response):

    # Initialize the class and perform relevant operations
    activity_class = ap.get_class_from_model(activity)
    activity_class.make_public()

    # Save the JSON in this user's outbox collection in the database
    print(activity_class.json())

    # Use the class's type to set the header
    response.headers["Location"] = "https://example.com/{0}/{1}".format(
        activity_class.type.lower(),
        1,  # ID should come from the database
    )

    # Return with header and status code
    return
```

Methods – like `make_public()` – perform common operations on the data. In this case, `make_public()` removes the `bto` and `bcc` attributes from the class instance, if they exist. Additionally, the class instance helps specify a location in the response header, per the ActivityPub [documentation](https://www.w3.org/TR/activitypub/#client-to-server-interactions) for client-to-server interactions.

## Contributing

**ActivityPubdantic** is still a work in progress. If you find it valuable for your project but notice bugs, need changes, or require additional features or support for other ActivityPub platforms, [open an issue](https://github.com/joewlos/activitypubdantic/issues) or fork to [start a PR](https://github.com/joewlos/activitypubdantic/pulls).

The `developer_requirements.txt` file includes all of the packages your virtual environment needs to start, including `pdoc3` for generating new documentation and `pytest` for unit tests.

Keep in mind, all PRs require GitHub to successfully run the test suite, so if you significantly change **ActivityPubdantic**'s structure, be sure to add, alter, or remove relevant tests.

Thank you for your interest!
