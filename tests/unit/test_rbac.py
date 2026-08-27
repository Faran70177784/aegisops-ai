from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from backend.app.api.rbac import require_permission


def test_require_permission_allows_user_with_permission():
    user = SimpleNamespace(
        role=SimpleNamespace(
            name="admin",
            permissions=[
                SimpleNamespace(name="users:create"),
            ],
        )
    )

    checker = require_permission("users:create")

    result = checker(user)

    assert result is user


def test_require_permission_rejects_user_without_permission():
    user = SimpleNamespace(
        role=SimpleNamespace(
            name="analyst",
            permissions=[
                SimpleNamespace(name="users:read"),
            ],
        )
    )

    checker = require_permission("users:create")

    with pytest.raises(HTTPException) as exc_info:
        checker(user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Insufficient permissions."


def test_require_permission_rejects_user_without_role():
    user = SimpleNamespace(role=None)

    checker = require_permission("users:create")

    with pytest.raises(HTTPException) as exc_info:
        checker(user)

    assert exc_info.value.status_code == 403
    assert (
        exc_info.value.detail
        == "User does not have an assigned role."
    )