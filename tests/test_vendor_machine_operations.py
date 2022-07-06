import sys, os, requests
import base64
from typing import Tuple
import pytest

parentdir = os.path.dirname(os.getcwd() + "/tests")
sys.path.insert(0, parentdir)

from database import sql_connection

URL_BASE = "http://127.0.0.1:8000"
sql_connection._cleaning_db()


def _defining_user_sample() -> Tuple[str, str]:
    return "kennedy.bacelar", "password"


def _return_product_sample():
    sample_product = {
        "id": "prod-1",
        "name": "pencil",
        "cost": 35,
        "amount_available": 17,
    }
    return sample_product


def _registering_user(username: str, password: str, role: str = "buyer"):
    url = URL_BASE + "/users"
    headers = {"Content-type": "application/json"}
    new_user = {
        "username": username,
        "password": password,
        "role": role,
    }
    return requests.post(url=url, json=new_user, headers=headers)


def _get_authentication_credentials_in_base_64(username: str, password: str) -> str:
    f_string = f"{username}:{password}"
    return base64.b64encode(f_string.encode("utf-8")).decode("utf-8")


def _expected_user(
    username_sample: str = "kennedy.bacelar",
    password: str = "$2b$12$K5hateacQGNRWmgpyG1Jo.8WQI7ezuLHAGZ4/jEoCZbrAY3Ndt86K",
):
    expected_user = {
        "username": username_sample,
        "password": password,  # Password hash
        "role": "buyer",
        "balance": 0,
    }
    return expected_user


def test_registering_new_user():
    username_sample, password_sample = _defining_user_sample()
    _registering_user(username=username_sample, password=password_sample)

    expected_user = _expected_user()

    # credentials in base64 corresponding to kennedy.bacelar:password
    credentials_in_base_64 = _get_authentication_credentials_in_base_64(
        username=username_sample, password=password_sample
    )

    headers = {"Authorization": f"Basic {credentials_in_base_64}"}

    final_url = f"{URL_BASE}/users/me"

    retrieved_user = requests.get(final_url, headers=headers).json()
    assert retrieved_user == expected_user


def test_deposit():
    username_sample, password_sample = _defining_user_sample()
    final_url = final_url = f"{URL_BASE}/deposit"

    credentials_in_base_64 = _get_authentication_credentials_in_base_64(
        username=username_sample, password=password_sample
    )

    headers = {"Authorization": f"Basic {credentials_in_base_64}"}
    body = {"value": "50"}

    expected_balance = {"user": "kennedy.bacelar", "balance": 50}

    retrieved_balance = requests.post(final_url, headers=headers, json=body).json()

    assert expected_balance == retrieved_balance


def test_add_product():
    username_sample = "ronaldo.brazilian"
    password_sample = "password"

    _registering_user(username=username_sample, password=password_sample, role="seller")
    final_url = final_url = f"{URL_BASE}/products"
    product = _return_product_sample()

    credentials_in_base_64 = _get_authentication_credentials_in_base_64(
        username=username_sample, password=password_sample
    )
    headers = {"Authorization": f"Basic {credentials_in_base_64}"}

    assert requests.post(final_url, json=product, headers=headers).json() == True


def test_buy_product():

    username_sample = "kennedy.bacelar"
    password_sample = "password"
    final_url = URL_BASE + "/buy"

    credentials_in_base_64 = _get_authentication_credentials_in_base_64(
        username=username_sample, password=password_sample
    )
    headers = {"Authorization": f"Basic {credentials_in_base_64}"}
    body = {"product_id": "prod-1", "amount": 1}

    purchase_response = requests.post(final_url, headers=headers, json=body).json()
    expected_response = {"message": "Purchase_succssesful", "change": [[1, 10], [1, 5]]}

    assert purchase_response == expected_response
