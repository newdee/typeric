# 📦 typeric

**typeric** is a practical type utility toolkit for Python, focused on clarity, safety, and ergonomics, it was originally built to make my own development experience smoother, but I hope it proves useful to others as well.
It currently provides a lightweight, pattern-matchable `Result` type — similar to Rust's `Result` — with plans to include more common type patterns and error-handling abstractions.

```bash
pip install typeric
```

---

## 🚀 Features

- ✅ Functional-style `Result` type: `Ok(value)` and `Err(error)`
- 🧩 Pattern matching support (`__match_args__`)
- 🔒 Immutable with `.map()` / `.map_err()` / `.unwrap()` / `.unwrap_or()` helpers
- 🔧 Clean type signatures: `Result[T, E]` (with default `E = Exception`)
- 🛠️ Built for extensibility — more type tools coming

---

## 🔍 Quick Example

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

---

## 📂 Real-World Example

```python
from functools import partial
import hashlib
from pathlib import Path
from typing import BinaryIO
from typeric.result import Result, Ok, Err


def get_md5(file_obj: BinaryIO) -> Result[str, Exception]:
    try:
        md5 = hashlib.md5()
        while chunk := file_obj.read(8096):
            md5.update(chunk)
        file_obj.seek(0)
        return Ok(md5.hexdigest())
    except Exception as e:
        return Err(e)


def is_exist(element: str, file_sets: set[str], auto_add: bool = True) -> bool:
    exist = element in file_sets
    if not exist and auto_add:
        file_sets.add(element)
    return exist


def file_exist(file_obj: BinaryIO, file_sets: set[str], auto_add: bool = True) -> Result[bool, Exception]:
    match get_md5(file_obj):
        case Ok(md5):
            print("md5:", md5)
        case Err(e):
            print("error occurred:", e)
    func = partial(is_exist, file_sets=file_sets, auto_add=auto_add)
    return get_md5(file_obj).map(func=func)
```

---

## ✅ Test

```python
def test_file() -> None:
    file_set: set[str] = set()
    files = [Path("test1.pdf"), Path("test1.pdf"), Path("test2.pdf")]
    for file in files:
        with open(file, "rb") as f:
            result = file_exist(f, file_set)
            assert result.is_ok()
```

Run tests with:

```bash
uv pytest -v
```

---

## 📦 Roadmap

- `Validated` type for batch error collection
- Async `Result`

---

## 📄 License

MIT
