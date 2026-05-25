# 🚀 Smart Retry

[![PyPI version](https://img.shields.io/pypi/v/smart-retry.svg)](https://pypi.org/project/smart-retry/)
[![Python versions](https://img.shields.io/pypi/pyversions/smart-retry.svg)](https://pypi.org/project/smart-retry/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, production-ready retry library for Python. **Smart Retry** simplifies error handling with a clean, decorator-based API supporting both synchronous and asynchronous execution.

---

## 📖 Table of Contents

- [Why Smart Retry?](#-why-smart-retry)
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Advanced Configuration](#-advanced-configuration)
- [Lifecycle Hooks](#-lifecycle-hooks)
- [Manual Engine Usage](#-manual-engine-usage)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🤔 Why Smart Retry?

Building resilient systems requires robust error handling. **Smart Retry** takes the boilerplate out of retry logic:

- **Zero Dependencies**: Keep your project lean.
- **Unified API**: One decorator for both `def` and `async def`.
- **Extensible**: Easily plug in custom backoff strategies and lifecycle hooks.
- **Type Safe**: Designed with modern Python standards in mind.

---

## ✨ Features

- 🔄 **Sync & Async**: Seamlessly works with traditional and coroutine functions.
- 📉 **Backoff Strategies**: Built-in Exponential, Linear, and Fixed backoff.
- 🎯 **Selective Retries**: Target specific exceptions.
- 🪝 **Observability**: Hooks for `on_retry`, `on_success`, and `on_fail`.
- 🛠️ **Developer Friendly**: Minimalist API with powerful defaults.

---

## 📥 Installation

```bash
pip install python-smart-retry==0.1.0
```

For development:

```bash
git clone https://github.com/ishtiaqmahmood/smart-retry.git
cd smart-retry
pip install -e .
```

---

## ⚡ Quick Start

### Basic Decorator

```python
from smart_retry import retry

@retry(max_attempts=3)
def unreliable_service():
    # This will be retried up to 3 times on any Exception
    return perform_network_call()
```

### Async Support

```python
import asyncio
from smart_retry import retry

@retry(max_attempts=5)
async def fetch_api_data():
    return await async_client.get("https://api.example.com")
```

---

## ⚙️ Advanced Configuration

### Targeted Exceptions

Only retry when specific errors occur:

```python
@retry(
    max_attempts=5,
    exceptions=(ConnectionError, TimeoutError)
)
def stable_task():
    pass
```

### Custom Backoff

Choose from built-in strategies or provide your own:

```python
from smart_retry.backoff import linear_backoff, fixed_backoff

@retry(backoff=linear_backoff)
def linear_task():
    pass

@retry(backoff=fixed_backoff)
def fixed_task():
    pass
```

---

## 🪝 Lifecycle Hooks

Monitor and react to the retry lifecycle:

```python
def on_retry(error, attempt):
    logging.warning(f"Attempt {attempt} failed: {error}")

@retry(max_attempts=3, on_retry=on_retry)
def monitored_task():
    pass
```

---

## 🛠️ Manual Engine Usage

For more control, use the `RetryEngine` directly:

```python
from smart_retry import RetryEngine

engine = RetryEngine(max_attempts=3)

# Synchronous execution
result = engine.run_sync(my_func, arg1, kwarg1=val)

# Asynchronous execution
result = await engine.run_async(my_async_func)
```

---

## 📚 API Reference

### `retry` Decorator

| Parameter      | Type       | Default               | Description                 |
| -------------- | ---------- | --------------------- | --------------------------- |
| `max_attempts` | `int`      | `3`                   | Maximum number of attempts. |
| `exceptions`   | `tuple`    | `(Exception,)`        | Exception types to catch.   |
| `backoff`      | `callable` | `exponential_backoff` | Delay strategy function.    |
| `on_retry`     | `callable` | `None`                | `callback(error, attempt)`  |
| `on_success`   | `callable` | `None`                | `callback(result)`          |
| `on_fail`      | `callable` | `None`                | `callback(error)`           |

---

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👤 Author

**Ishtiaq Mahmood** - [GitHub](https://github.com/ishtiaqmahmood)

Project Link: [https://github.com/ishtiaqmahmood/smart-retry](https://github.com/ishtiaqmahmood/smart-retry)
