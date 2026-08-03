from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from app.core.exceptions import register_exception_handlers
from app.main import app
from app.shared.responses import ERROR_RESPONSES


class Payload(BaseModel):
    amount: int = Field(gt=0)


def build_test_app() -> FastAPI:
    test_app = FastAPI(responses=ERROR_RESPONSES)
    register_exception_handlers(test_app)

    @test_app.post("/payload")
    def payload(value: Payload) -> Payload:
        return value

    @test_app.get("/errors/{status_code}")
    def error(status_code: int) -> None:
        headers = (
            {"WWW-Authenticate": "Bearer"}
            if status_code == 401
            else {"Retry-After": "60"}
            if status_code == 429
            else None
        )
        raise HTTPException(
            status_code=status_code,
            detail=f"Error {status_code}",
            headers=headers,
        )

    @test_app.get("/unexpected")
    def unexpected() -> None:
        raise RuntimeError("sensitive internal detail")

    return test_app


def test_http_errors_use_standard_envelope_and_preserve_headers() -> None:
    client = TestClient(build_test_app())
    expected_codes = {
        401: "unauthorized",
        403: "forbidden",
        409: "conflict",
        429: "rate_limit_exceeded",
    }

    for status_code, code in expected_codes.items():
        response = client.get(f"/errors/{status_code}")
        assert response.status_code == status_code
        assert response.json() == {
            "success": False,
            "code": code,
            "message": f"Error {status_code}",
            "details": None,
            "request_id": None,
        }

    assert client.get("/errors/401").headers["www-authenticate"] == "Bearer"
    assert client.get("/errors/429").headers["retry-after"] == "60"


def test_not_found_validation_and_malformed_json_are_standardized() -> None:
    client = TestClient(build_test_app())

    not_found = client.get("/missing")
    validation = client.post("/payload", json={"amount": 0})
    malformed = client.post(
        "/payload",
        content='{"amount":',
        headers={"Content-Type": "application/json"},
    )

    assert not_found.status_code == 404
    assert not_found.json()["code"] == "not_found"
    assert validation.status_code == 400
    assert validation.json()["code"] == "bad_request"
    assert validation.json()["details"][0]["field"] == "body.amount"
    assert malformed.status_code == 400
    assert malformed.json()["code"] == "invalid_json"


def test_transaction_source_validation_returns_serializable_bad_request() -> None:
    client = TestClient(app, raise_server_exceptions=False)

    response = client.post(
        "/transactions/",
        headers={"Idempotency-Key": "invalid-transaction-source"},
        json={
            "account_id": 0,
            "category_id": 2,
            "credit_card_id": 1,
            "amount": 15,
            "transaction_type": "expense",
            "payment_method": "cash",
            "transaction_date": "2026-07-29T19:06:09.461Z",
        },
    )

    assert response.status_code == 400
    body = response.json()
    assert body["code"] == "bad_request"
    assert body["message"] == "Request validation failed"
    assert body["details"][0]["field"] == "body"
    assert (
        body["details"][0]["context"]["error"]
        == "account_id and credit_card_id cannot be provided together"
    )


def test_internal_error_hides_sensitive_details() -> None:
    client = TestClient(build_test_app(), raise_server_exceptions=False)

    response = client.get("/unexpected")

    assert response.status_code == 500
    assert response.json()["code"] == "internal_server_error"
    assert "sensitive" not in response.text


def test_openapi_documents_standard_errors_for_every_operation() -> None:
    openapi = app.openapi()
    expected = {"400", "401", "403", "404", "409", "422", "429", "5XX"}

    for path_item in openapi["paths"].values():
        for operation in path_item.values():
            if not isinstance(operation, dict) or "responses" not in operation:
                continue
            assert expected <= set(operation["responses"])
            for status_code in expected:
                schema = operation["responses"][status_code]["content"]["application/json"][
                    "schema"
                ]
                assert schema["$ref"].endswith("/ErrorResponse")
