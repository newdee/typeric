# 📦 typeric

**typeric** is a practical type utility toolkit for Python, focused on clarity, safety, and ergonomics. It was originally built to make my own development experience smoother, but I hope it proves useful to others as well.  
It currently provides lightweight, pattern-matchable types like `Result` and `Option` — inspired by Rust — with plans to include more common type patterns and error-handling abstractions.

```bash
pip install typeric
```

---

## 🚀 Features
- ✅ Functional-style `Result` type: `Ok(value)` and `Err(error)`
- 🌀 Lightweight `Option` type: `Some(value)` and `NONE`
- 🧩 Pattern matching support (`__match_args__`)
- 🔒 Immutable with `.map()` / `.map_err()` / `.unwrap()` / `.unwrap_or()` helpers
- 🔧 Clean type signatures: `Result[T, E]` and `Option[T]`
- 🛠️ Built for extensibility — more type tools coming

---

## 🔍 Quick Example


### `Result`

```python
from typeric.result import Result, Ok, Err

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
```

### `Option`

```python
from typeric.option import Option, Some, NONE

def maybe_get(index: int, items: list[str]) -> Option[str]:
    if 0 <= index < len(items):
        return Some(items[index])
    return NONE

match maybe_get(1, ["a", "b", "c"]):
    case Some(value):
        print("Got:", value)
    case NONE:
        print("Nothing found")
```

---

## ✅ Test


Run tests with:

```bash
uv run pytest -v
```

---

## 📦 Roadmap

- `Validated` type for batch error collection
- Async `Result`
- `OptionResult` combinators
- `Try`, `Either`, `NonEmptyList`, etc.
---

## 📄 License

MIT
