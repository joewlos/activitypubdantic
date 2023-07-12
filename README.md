# ActivityPubdantic

### Validate and Interact with ActivityPub JSON

[ActivityPubdantic Documentation](https://www.joewlos.com/activitypubdantic/)

[ActivityPub Protocol](https://www.w3.org/TR/activitypub/)

[ActivityStreams Specification](https://www.w3.org/TR/activitystreams-vocabulary/)

## What Is ActivityPubdantic?

**ActivityPubdantic** is a suite of tools for validating ActivityPub JSON and constructing consistent representations of ActivityPub notifications and content. [Pydantic](https://docs.pydantic.dev/latest/) models enable the validation logic and can be imported for use in custom-coded classes or FastAPI routes.

## Why Does ActivityPub JSON Require Validation?

[ActivityPub](https://www.w3.org/TR/activitypub/) is a protocol for decentralized social networking. It defines client-to-server and server-to-server interactions and relies on [ActivityStreams](https://www.w3.org/TR/activitystreams-vocabulary/#dfn-orderedcollection) for its vocabulary. Many of the protocol's definitions are purposefully broad, giving developers the freedom to implement only the features relevant to their products or to adjust to meet their particular requirements.

However, that flexibility presents challenges for assessing data validity and simplifying developers' code. **ActivityPubdantic** helps solve those challenges by using ActivityPub's "type" field to identify proper checks for other fields and standardize their structures. [Examples](#examples) are available in the sections below.

[Mastodon](https://docs.joinmastodon.org/spec/activitypub/) supports ActivityPub, and Meta's [Threads](https://apps.apple.com/us/app/threads-an-instagram-app/id6446901002) app plans to conform to the protocol sometime in the [near future](https://techcrunch.com/2023/07/05/adam-mosseri-says-metas-threads-app-wont-have-activitypub-support-at-launch/). **ActivityPubdantic** includes a test suite, which uses examples from ActivityPub, ActivityStreams, and Mastodon to test its parsing and validation. As Threads and other platforms implement ActivityPub, those tests (and more broadly, this package) will be updated to stay current.

## Examples

The following examples present use cases for **ActivityPubdantic** and simple code snippets for those use cases. For a more thorough listing of the package's classes, functions, and models, check out its [documentation](https://www.joewlos.com/activitypubdantic/).

### Validating and Parsing Activities

`Activities` are core concepts around which ActivityPub and ActivityStreams are both built. By reducing their complexity and standardizing their representation, **ActivityPubdantic** helps resolve potential pain points for developers.

ActivityPub includes an [example](https://www.w3.org/TR/activitypub/#client-to-server-interactions) of a `Like` activity. The example's `to` field is a list, while the `cc` field is a string. While both formats are valid, they require slightly different handling in subsequent lines of code. After validating this JSON, **ActivityPubdantic** rewrites it, so that those fields are always presented as lists of dictionaries.

```python
import activitypubdantic as ap
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
output_class = ap.get_class(example_json)
print(output_class.json())
```

The output JSON is longer and, at first glance, more complex. But because it contains types for each item in its fields and it standardizes the structures of similar fields – like `to` and `cc` – it is more descriptive and easier to manipulate.

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
