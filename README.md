## test_vm
Selection process - backend1 exercise

### Setting environment
- Install poetry with $ pip install poetry
- Install dependencies with $ poetry install

### Running tests
- $ activate the environment with $ poetry shell
- Run the tests with - at the root of project $ pytest tests/test_vendor_machine_operations.py

### Athentication

Except by registering new user - all API endpoints require authentication.
The authentication method is basic authentication, it should be inclued in the request headers in the following format: 

The credentials in base 64 should be a conversion of the following format: $ username:password

headers = { "Authorization": "Basic {credentials_in_base_64}" }

e.g, for the user ronaldo.brazilian with password = password, the authentication header should be in the following format.

{"Authorization": "Basic cm9uYWxkby5icmF6aWxpYW4="}
