import json

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from .db_test import get_db_test, get_record_table_test, engine_test, metadata_test
from ..api.auth_manager import get_current_user
from ..api.db import get_db, get_record_table, dummy_record_db
from ..main import app


def skip_auth():
    pass


# To Skip Authentication for Test
app.dependency_overrides[get_current_user] = skip_auth

# To override test DB
app.dependency_overrides[get_db] = get_db_test
app.dependency_overrides[get_record_table] = get_record_table_test

client = TestClient(app)


@pytest_asyncio.fixture
async def db_fixer():
    metadata_test.drop_all(engine_test)
    metadata_test.create_all(engine_test)
    await get_db_test().connect()
    for rec in dummy_record_db:
        query = get_record_table_test().insert().values(**rec)
        await get_db_test().execute(query)
    yield
    await get_db_test().disconnect()


def test_01_get_records(db_fixer):
    response = client.get("/")
    assert response.status_code == 200
    assert len(response.json()) == 9


def test_02_get_summary(db_fixer):
    response = client.get("/summary")
    assert response.status_code == 200
    assert (response.json())["mean"] == "22295010.0"
    assert (response.json())["min"] == "30"
    assert (response.json())["max"] == "200000000"


def test_03_get_on_contract_summary(db_fixer):
    response = client.get("/on_contract/summary")
    assert response.status_code == 200
    assert (response.json())["mean"] == "100000.0"
    assert (response.json())["min"] == "90000"
    assert (response.json())["max"] == "110000"


def test_04_get_department_summary(db_fixer):
    response = client.get("/department/summary")
    assert_response = [
        {
            "department": "Banking",
            "summary": {
                "mean": "90000.0",
                "min": "90000",
                "max": "90000"
            }
        },
        {
            "department": "Engineering",
            "summary": {
                "mean": "40099006.0",
                "min": "30",
                "max": "200000000"
            }
        },
        {
            "department": "Administration",
            "summary": {
                "mean": "30.0",
                "min": "30",
                "max": "30"
            }
        },
        {
            "department": "Operations",
            "summary": {
                "mean": "35015.0",
                "min": "30",
                "max": "70000"
            }
        }
    ]
    assert response.status_code == 200
    for i in response.json():
        assert i in assert_response


def test_05_get_department_summary_nested(db_fixer):
    response = client.get("/department/summary/nested")
    assert_response = [
        {
            "department": "Banking",
            "summary": [
                {
                    "sub_department": "Loan",
                    "summary": {
                        "mean": "90000.0",
                        "min": "90000",
                        "max": "90000"
                    }
                }
            ]
        },
        {
            "department": "Engineering",
            "summary": [
                {
                    "sub_department": "Platform",
                    "summary": {
                        "mean": "40099006.0",
                        "min": "30",
                        "max": "200000000"
                    }
                }
            ]
        },
        {
            "department": "Administration",
            "summary": [
                {
                    "sub_department": "Agriculture",
                    "summary": {
                        "mean": "30.0",
                        "min": "30",
                        "max": "30"
                    }
                }
            ]
        },
        {
            "department": "Operations",
            "summary": [
                {
                    "sub_department": "CustomerOnboarding",
                    "summary": {
                        "mean": "35015.0",
                        "min": "30",
                        "max": "70000"
                    }
                }
            ]
        }
    ]
    assert response.status_code == 200
    for i in response.json():
        assert i in assert_response


def test_06_add_record_invalid(db_fixer):
    payloadIn = {
        "name": "Test",
        "salary": "10000",
        "department": "Engineering"
    }
    response = client.post("/add", content=json.dumps(payloadIn))
    assert response.status_code == 422

    payloadIn = {
        "name": "Test",
        "salary": "10000",
        "sub_department": "Platform"
    }
    response = client.post("/add", content=json.dumps(payloadIn))
    assert response.status_code == 422

    payloadIn = {
        "name": "Test",
        "department": "Engineering",
        "sub_department": "Platform"
    }
    response = client.post("/add", content=json.dumps(payloadIn))
    assert response.status_code == 422

    payloadIn = {
        "salary": "10000",
        "department": "Engineering",
        "sub_department": "Platform"
    }
    response = client.post("/add", content=json.dumps(payloadIn))
    assert response.status_code == 422


def test_07_add_record_valid(db_fixer):
    payloadIn = {
        "name": "Test",
        "salary": "10000",
        "department": "Test Dept",
        "sub_department": "Test Sub Dept"
    }
    payloadResp = {
        "id": 10,
        "name": "Test",
        "salary": "10000",
        "currency": "USD",
        "department": "Test Dept",
        "sub_department": "Test Sub Dept",
        "on_contract": None,
    }
    response = client.post("/add", content=json.dumps(payloadIn))
    assert response.status_code == 201
    assert json.dumps(response.json()) == json.dumps(payloadResp)


def test_08_delete_record_invalid(db_fixer):
    response = client.delete("/remove/11")
    assert response.status_code == 404


def test_09_delete_record_valid(db_fixer):
    response = client.get("/")
    assert len(response.json()) == 9

    response = client.delete("/remove/9")
    assert response.status_code == 200

    response = client.get("/")
    assert len(response.json()) == 8
