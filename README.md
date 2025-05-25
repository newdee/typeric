# 📦 typeric

**typeric** is a practical type utility toolkit for Python, focused on clarity, safety, and ergonomics. It was originally built to make my own development experience smoother, but I hope it proves useful to others as well.  
It currently provides lightweight, pattern-matchable types like `Result` and `Option` — inspired by Rust — with plans to include more common type patterns and error-handling abstractions.

```bash
pip install typeric
```

---

## 🚀 Features
- ✅ Functional-style `Result` type: `Ok(value)` and `Err(error)`
- 🌀 Lightweight `Option` type: `Some(value)` and `None_()`
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
```

### `Option`

```python
from typeric.option import Option, Some, None_

def maybe_get(index: int, items: list[str]) -> Option[str]:
    if 0 <= index < len(items):
        return Some(items[index])
    return None_()

match maybe_get(1, ["a", "b", "c"]):
    case Some(value):
        print("Got:", value)
    case None_():
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
