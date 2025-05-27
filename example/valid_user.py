from typeric.result import Err, Ok, Result


def validate_username(username: str) -> Result[str, str]:
    if username.strip():
        return Ok(username)
    return Err("Username is empty")


def validate_age(age: int) -> Result[int, str]:
    if age > 0:
        return Ok(age)
    return Err("Age must > 0")


def validate_email(email: str) -> Result[str, str]:
    if "@" in email:
        return Ok(email)
    return Err("Invalid email")


# ✅ results combine
def validate_user_data(
    username: str, age: int, email: str
) -> Result[tuple[tuple[str, int], str], str]:
    return (
        validate_username(username)
        .combine(validate_age(age))
        .combine(validate_email(email))
    )


result1 = validate_user_data("alice", 30, "alice@example.com")
print(result1)  # Ok((('alice', 30), 'alice@example.com'))

result2 = validate_user_data("", -5, "invalid-email")
print(result2.errs)  # Err(['Username is empty', 'Age must > 0', 'Invalid email'])
