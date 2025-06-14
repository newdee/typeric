# 📦 typeric

**typeric** is a practical type utility toolkit for Python, focused on clarity, safety, and ergonomics. It was originally built to make my own development experience smoother, but I hope it proves useful to others as well.  
It currently provides lightweight, pattern-matchable types like `Result` and `Option` — inspired by Rust — with plans to include more common type patterns and error-handling abstractions.

```bash
pip install typeric
```

---

## 🚀 Features

- ✅ **Functional-style `Result` type**  
  `Ok(value)` and `Err(error)` with powerful `.map()`, `.and_then()`, `.combine()`, `.spread()` helpers — inspired by Rust’s `Result`.

- 🌀 **Lightweight `Option` type**  
  `Some(value)` and `NONE` to handle nullable data safely, with `.map()`, `.unwrap_or()`, `.is_some()` and more.

- 🔁 **Seamless conversion decorators**  
  - `@resulty`: Wraps any function to return `Result` instead of raising exceptions.  
  - `@optiony`: Wraps any function to return `Option`, converting `None` or exceptions into `NONE`.

- 🧩 **Pattern matching support**  
  Supports Python’s `match` syntax via `__match_args__` for both `Ok/Err` and `Some/NONE`.

- 🔒 **Immutable and composable**  
  Safe and clean method chains using `.map()`, `.combine()`, `.inspect()`, etc.

- 🔧 **Clean type signatures**  
  Fully typed: `Result[T, E]` and `Option[T]` with static analysis and IDE support.

- 🛠️ **Extensible foundation**  
  Designed for easy extension — more algebraic types (`Either`, `Validated`, etc.) can be added naturally.

---

## 🔍 Quick Example


### `Result`

```python
from typeric.result import Result, Ok, Err, resulty, resulty_async, optiony, optiony_async

def parse_number(text: str) -> Result[int, str]:
    try:
        return Ok(int(text))
    except ValueError:
        return Err("Not a number")

match parse_number("42"):
    case Ok(value):
        print("Parsed:", value)
    case Err(error):
        print("Failed:", error)

# let function return Result[T,str]
@resulty
def add(x: int, y: int) -> int:
    return x + y

res = add(1, 2)
if res.is_ok():
    print("Result:", res.unwrap())
else:
    print("Error:", res.err)

# let async function return Result[T,str]
@resulty_async
async def async_add(x: int, y: int) -> int:
    return x + y

res = await async_add(1, 2)
if res.is_ok():
    print("Result:", res.unwrap())
else:
    print("Error:", res.err)

def func_a(x: int) -> Result[int, str]:
    if x < 0:
        return Err("negative input")
    return Ok(x * 2)


@spreadable
def func_b(y: int) -> Result[int, str]:
    a = func_a(y).spread()
    return Ok(a + 1)


def test_func_b_success():
    assert func_b(5) == Ok(11)  # 5*2=10 +1=11


def test_func_b_propagate_error():
    assert func_b(-2) == Err("negative input")

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
```

### `Option`

```python
from typeric.option import Option, Some, NONE
from typeric.wrap_func import get_time_sync 
def maybe_get(index: int, items: list[str]) -> Option[str]:
    if 0 <= index < len(items):
        return Some(items[index])
    return NONE

match maybe_get(1, ["a", "b", "c"]):
    case Some(value):
        print("Got:", value)
    case NONE:
        print("Nothing found")

@get_time_sync # This decorator is used for synchronous functions to measure execution time.
@optiony
def get_number(x: int) -> int | None:
    if x > 0:
        return x
    return None

@optiony_async
async def fetch_data(flag: bool) -> str | None:
    if flag:
        return "data"
    return None
```

---

## ✅ Test


Run tests with:

```bash
uv run pytest -v
```

---

## 📦 Roadmap

- Async `Result`
- `OptionResult` combinators
- `Try`, `Either`, `NonEmptyList`, etc.
---

## 📄 License

MIT
