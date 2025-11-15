Access Nested Map Utility
This project provides generic Python utility functions for working with nested maps, fetching JSON from URLs, and memoization. It includes thorough unit tests for the access_nested_map function following strict Python standards and best practices.

Features
Access values in nested maps using a sequence of keys.

Fetch JSON data from remote URLs.

Memoize method results for performance optimization.

Comprehensive unit tests for key utility functions using unittest and parameterized.

Requirements
All files are interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7).

All files start with a shebang line: #!/usr/bin/env python3.

All files end with a new line and are executable.

Code adheres to pycodestyle (version 2.5).

All modules, classes, and functions have meaningful documentation strings.

All functions and coroutines are type-annotated.

File Structure
text
.
├── utils.py
├── test_utils.py
└── README.md
Usage
Access Nested Map
python
from utils import access_nested_map

nested_map = {"a": {"b": {"c": 42}}}
result = access_nested_map(nested_map, ["a", "b", "c"])
print(result)  # Output: 42
Run Tests
To run the unit tests for access_nested_map, execute:

bash
python3 -m unittest test_utils.py
Testing Dependencies
Install test dependencies:

bash
pip install parameterized
Code Style
This project follows pycodestyle (PEP8).
Check your code style with:

bash
pycodestyle utils.py test_utils.py
