# GlueHome Python Package

This Python package provides a client for interacting with the GlueHome API, allowing you to control and monitor your GlueHome smart locks.

## Features

- Authentication with GlueHome API
- Retrieve information about all your locks
- Get details for specific locks
- Control locks (lock/unlock)

## Installation

You can install the GlueHome package using pip:

```bash
pip install gluehome
```

## Usage

Here's a quick example of how to use the GlueHome package:

```python
from gluehome import GlueAuth, GlueClient

# Authenticate and get API key
auth = GlueAuth("your_username", "your_password")
api_key = auth.issue_api_key()

# Create a client
client = GlueClient(api_key)

# Get all locks
all_locks = client.get_all_locks()

# Get a specific lock
lock = client.get_lock("lock_id")

# Get multiple specific locks
locks = client.get_locks(["lock_id1", "lock_id2"])

# Control a lock
lock.lock()  # Lock the door
lock.unlock()  # Unlock the door

# Update lock information
lock.update()

# Get lock information
print(f"Lock: {lock.description}")
print(f"Status: {lock.connection_status}")
print(f"Battery: {lock.battery_status}%")
print(f"Last event: {lock.last_lock_event.event_type} at {lock.last_lock_event.event_time}")
```

## Configuration

The package requires an API key for authentication. You can either:

1. Provide your GlueHome username and password to `GlueAuth` to generate an API key.
2. Use an existing API key directly with `GlueClient`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This package is not officially associated with or endorsed by GlueHome.
