# Python Patterns — Snippet Templates

Dùng các mẫu này để lưu nhanh vào snippet CLI:

## Context Manager
```python
from contextlib import contextmanager

@contextmanager
def managed_resource():
    resource = acquire()
    try:
        yield resource
    finally:
        release(resource)
```

## Dataclass
```python
from dataclasses import dataclass, field

@dataclass
class Item:
    name: str
    value: float
    tags: list = field(default_factory=list)
```

## Decorator
```python
import functools

def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # before
        result = func(*args, **kwargs)
        # after
        return result
    return wrapper
```

## Retry với exponential backoff
```python
import time

def retry(max_attempts=3, delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))
        return wrapper
    return decorator
```
