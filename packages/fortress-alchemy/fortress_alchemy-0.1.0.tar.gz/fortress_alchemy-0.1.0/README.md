# Fortress Alchemy

## Installation

You can install the client using pip. Simply run the following command:

```bash
pip install fortress-alchemy
```

## Quick Start

Here is a quick example to get you started with the client:

```python
from fortress_alchemy import FortressAlchemy

# Initialize the client with your API key
client = FortressAlchemy(org_id='your_org_id', api_key='your_api_key')

# Create an engine
engine = fortress_alchemy.create_engine("client1", echo=True)

# Create a database
```

## Documentation

Below is a list of the available functionality in the client. The client allows you to create SQLAlchemy engines to use with your existing SQLAlchemy infrastructure. You can also easily route data requests based on tenant names. For more detailed information, please refer to the [Fortress API documentation](https://docs.fortress.build).

- `create_engine(tenant_id: str, **kwargs: Any)`: Creates a new SQLAlchemy engine for the given tenant. The tenant ID is used to route data requests to the correct database.

## Configuration

To use the client, generate an API key from the Fortress dashboard. Also, provide the organization ID, which is available under the API Keys page on the platform website.

## License

This client is licensed under the MIT License.

## Support

If you have any questions or need help, don't hesitate to get in touch with our support team at founders@fortress.build.
