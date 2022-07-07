## test_vm
Selection process - backend1 exercise

### Setting environment
- Install poetry with $ pip install poetry
- Install dependencies with $ poetry install

### Running the server ( At root level of the project )
- Activate the environment with $ poetry shell
- Run the server with $ uvicorn api.main:app --reload

### Running tests ( At root level of the project )
- activate the environment with $ poetry shell
- Run the tests with $ pytest tests/test_vendor_machine_operations.py

### Athentication
Except by registering new user - all API endpoints require authentication.
The authentication method is basic authentication, it should be inclued in the request headers in the following format: 

The credentials in base 64 should be a conversion of the following format: $ username:password

headers = { "Authorization": "Basic {credentials_in_base_64}" }

e.g, for the user ronaldo.brazilian with password = password, the authentication header should be in the following format.

{"Authorization": "Basic cm9uYWxkby5icmF6aWxpYW4="}
