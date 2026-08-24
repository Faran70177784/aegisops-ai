from backend.app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hashing() -> None:
    password = "TestPassword@123"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password(
        "WrongPassword",
        hashed,
    )


def test_jwt_round_trip() -> None:
    subject = "123"

    token = create_access_token(subject)
    decoded_subject = decode_access_token(token)

    assert decoded_subject == subject