# 📖 Modern Python Standards - Quick Reference

**Applied to Badge Generator Project**

---

## 🎯 Type Hints Cheat Sheet

### Function Signatures
```python
# ✅ Basic types
def process(name: str, count: int, ratio: float) -> bool:
    """Process data and return success status."""
    return True

# ✅ Optional types
from typing import Optional
def find_user(user_id: int) -> Optional[str]:
    """Find user or return None if not found."""
    return None

# ✅ List/Dict types
from typing import List, Dict
def get_users() -> List[Dict[str, str]]:
    """Get list of user dictionaries."""
    return [{"name": "John", "id": "001"}]

# ✅ Union types
from typing import Union
def convert(value: Union[str, int]) -> float:
    """Convert string or int to float."""
    return float(value)

# ✅ Callable types
from typing import Callable
def apply_function(func: Callable[[int], str], x: int) -> str:
    """Apply function to value."""
    return func(x)
```

---

## 🔤 F-Strings Usage

```python
# ❌ OLD
message = "Hello %s, you have %d messages" % (name, count)
message = "Hello {}, you have {} messages".format(name, count)

# ✅ NEW - F-strings
message = f"Hello {name}, you have {count} messages"
message = f"User {user['name']} (ID: {user['id']})"
message = f"Processed {items_count} items in {duration:.2f}s"
```

---

## 📁 Pathlib instead of os.path

```python
# ❌ OLD - os.path
import os
file_path = os.path.join(folder, "data.txt")
if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
os.makedirs(folder, exist_ok=True)

# ✅ NEW - pathlib
from pathlib import Path
file_path = Path(folder) / "data.txt"
if file_path.exists():
    content = file_path.read_text()
file_path.parent.mkdir(parents=True, exist_ok=True)
```

---

## 📝 Docstring Format

```python
def download_image(url: str, emp_id: str, timeout: int = 30) -> bool:
    """
    Download an image from the specified URL.
    
    Connects to the server, retrieves the image, and saves it locally.
    Includes automatic retry logic for network errors.
    
    Args:
        url: Base URL of the image server.
        emp_id: Employee ID in format 'name_id_position'.
        timeout: Request timeout in seconds (default: 30).
    
    Returns:
        True if download successful, False otherwise.
    
    Raises:
        ValueError: If emp_id format is invalid.
        requests.Timeout: If download exceeds timeout.
    
    Examples:
        >>> success = download_image('https://api.company.com', 'john_001_SE')
        >>> print(success)
        True
    """
    if not emp_id or '_' not in emp_id:
        raise ValueError(f"Invalid emp_id format: {emp_id}")
    ...
```

---

## ⚠️ Exception Handling

```python
# ❌ OLD - Generic exception
try:
    download_file(url, path)
except Exception as err:
    print(f"Error: {err}")

# ✅ NEW - Specific exceptions
try:
    urllib.request.urlretrieve(url, path, timeout=30)
except urllib.error.HTTPError as err:
    logger.error(f"HTTP {err.code}: {err.reason}")
except urllib.error.URLError as err:
    logger.error(f"Network error: {err.reason}")
except socket.timeout:
    logger.error(f"Request timed out after 30s")
except Exception as err:
    logger.error(f"Unexpected error: {err}")
    raise
```

---

## 🔄 List/Dict Comprehensions

```python
# ❌ OLD - Loop-based
files = []
for item in folder.iterdir():
    if item.is_file() and item.suffix == '.jpg':
        files.append(item.name)

# ✅ NEW - Comprehension
files = [item.name for item in folder.iterdir() 
         if item.is_file() and item.suffix == '.jpg']

# ✅ Dict comprehension
user_map = {user['id']: user['name'] for user in users}

# ✅ Set comprehension
unique_ids = {user['id'] for user in users}
```

---

## 🌐 String Methods

```python
# ✅ Use modern string methods
text = "  hello world  "
text.strip()              # Remove whitespace
text.lower()              # Lowercase
text.upper()              # Uppercase
text.startswith("hello")  # Check prefix
text.endswith(".jpg")     # Check suffix
text.split(",")           # Split by delimiter
",".join(items)           # Join with separator

# ✅ String case checking
"hello".isalpha()         # All letters?
"123".isdigit()           # All digits?
"Hello123".isalnum()      # Letters and digits?
```

---

## 🎁 Context Managers

```python
# ✅ File operations
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ✅ Multiple files
with open(in_file) as fin, open(out_file, 'w') as fout:
    fout.write(fin.read())

# ✅ Queue operations
with queue.Queue() as q:
    # Work with queue
    pass
```

---

## 🔍 Type Checking Tips

```python
from typing import Dict, List, Optional, Union, Tuple

# ✅ Complex types
def process_data(
    items: List[Dict[str, int]],
    config: Optional[Dict[str, str]] = None
) -> Tuple[bool, List[str]]:
    """Process items and return status with messages."""
    messages = []
    return True, messages

# ✅ Generic types
from typing import TypeVar, Generic
T = TypeVar('T')
class Container(Generic[T]):
    def store(self, item: T) -> None: ...
    def retrieve(self) -> T: ...
```

---

## 📋 Private vs Public Methods

```python
class DataManager:
    """Manage data operations."""
    
    # ✅ Public method (no underscore)
    def process_file(self, filepath: str) -> bool:
        """Main public API."""
        return self._validate(filepath) and self._execute(filepath)
    
    # ✅ Private method (single underscore)
    def _validate(self, filepath: str) -> bool:
        """Internal validation."""
        return True
    
    # ✅ Internal implementation (double underscore)
    def __execute(self, filepath: str) -> bool:
        """Internal-only method."""
        return True
```

---

## 🧪 Code Examples from Project

### Image Crawler
```python
class ImageCrawler:
    def __init__(
        self,
        workers: int = 10,
        base_url: str = "https://...",
        timeout: int = 30
    ) -> None:
        self.workers = workers
        self.base_url = base_url
        self.timeout = timeout

    def download_image(self, url: str, emp_id: str) -> bool:
        """Download single image with error handling."""
        try:
            urllib.request.urlretrieve(url, filepath, timeout=self.timeout)
            return True
        except urllib.error.HTTPError as err:
            logger.error(f"HTTP error: {err}")
            return False
```

### Name Verifier
```python
class ImageNameVerifier:
    def verify_name(self, name: str, counter: int = 1) -> bool:
        """Verify filename against pattern."""
        is_valid = bool(self.regex.match(name))
        status = "✓" if is_valid else "✗"
        self.logger.info(f"{counter:4} [{status}] {name}")
        return is_valid
```

---

## ✅ Checklist for New Code

- [ ] All functions have type hints
- [ ] All functions have docstrings
- [ ] Using f-strings for formatting
- [ ] Using pathlib for file paths
- [ ] Specific exception handling
- [ ] Proper logging instead of print()
- [ ] Private methods start with `_`
- [ ] Constants in UPPER_CASE
- [ ] PEP-8 formatting
- [ ] 79 character line limit (comments/docstrings)
- [ ] 88 character line limit (code)

---

## 🚀 Commands for Validation

```bash
# Check type hints with Mypy
mypy tools/image_crawler.py

# Check style with Pylint
pylint tools/image_crawler.py

# Format with Black
black tools/image_crawler.py

# Check with Flake8
flake8 tools/image_crawler.py

# Run tests
python -m pytest tests/

# Check all at once
make check
```

---

## 📚 Python Documentation

- [Type Hints](https://docs.python.org/3/library/typing.html)
- [Pathlib](https://docs.python.org/3/library/pathlib.html)
- [F-strings](https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals)
- [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Google Style Docstrings](https://google.github.io/styleguide/pyguide.html)

---

**Keep code clean, typed, and documented!** ✨
