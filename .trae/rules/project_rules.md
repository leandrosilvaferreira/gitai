---
description: Global Rules for Sequential Thinking
globs: 
alwaysApply: true
---
- Always use tool sequentialthinking to analyse, plan and execute modifications in source code


---
description: Git Integration and Command Execution Rules
globs: **/*.py,**/*.sh
alwaysApply: false
---
# Git Integration Rules

- Use `subprocess.run()` to execute Git commands.
- Always check the return code of the subprocess call to handle potential errors (`check=True`).
- Capture `stdout` and `stderr` to get command output and error details.
- Decode the output from bytes to string using a specific encoding, preferably UTF-8.
- Sanitize any user input that is passed to shell commands to prevent command injection vulnerabilities.


---
description: Python Coding Standards and Best Practices
globs: **/*.py
alwaysApply: false
---
# Python Best Practices

- Follow PEP 8 style guide for all Python code.
- Use type hints for function signatures to improve clarity and allow static analysis.
- Prefer f-strings for string formatting (`f"hello {name}"`).
- Keep functions small and focused on a single responsibility.
- Use list comprehensions for creating lists concisely.


---
description: Testing Standards and Practices
globs: **/test_*.py,**/tests/**/*.py,**/*_test.py
alwaysApply: false
---
# Testing Rules

- Write unit tests for new features and bug fixes.
- Use the `pytest` framework for writing and running tests.
- Use mocks (e.g., `unittest.mock`) to isolate units under test from external dependencies like APIs and the filesystem.
- Organize tests in a `tests/` directory, mirroring the `src/` structure.
- Aim for high test coverage for critical parts of the codebase.
- Tests should be fast, reliable, and independent of each other.


---
description: Shell Script Development Rules
globs: **/*.sh,**/*.bash,**/scripts/**/*
alwaysApply: false
---
# Shell Script Rules

- Start scripts with a shebang (e.g., `#!/bin/bash`).
- Use `set -e` to make the script exit immediately if a command exits with a non-zero status.
- Use `set -u` to treat unset variables as an error.
- Use `set -o pipefail` to cause a pipeline to return the exit status of the last command to exit with a non-zero status.
- Quote all variables (`"$VAR"`) to prevent word splitting and globbing issues.
- Use `$(command)` for command substitution instead of backticks.


---
description: File I/O Operations Rules
globs: **/*.py
alwaysApply: false
---
# File I/O Rules

- Use `with open(...) as f:` syntax to ensure files are automatically closed.
- Always specify the file encoding, e.g., `open('file.txt', 'r', encoding='utf-8')`.
- Use the `pathlib` module for object-oriented filesystem paths, as it provides a cleaner, cross-platform API.
- Handle potential `IOError` or `FileNotFoundError` exceptions when dealing with file operations.
- Avoid constructing paths by string concatenation; use `pathlib` or `os.path.join()` instead.


---
description: Error Handling Best Practices
globs:
alwaysApply: true
---
# Error Handling Rules

- Implement a consistent error handling strategy across the application.
- Use specific, custom exceptions where appropriate to convey clear error conditions.
- Catch specific exceptions rather than using a blanket `except Exception:`.
- Log errors with sufficient context (e.g., stack trace, relevant variables) to facilitate debugging.
- For a CLI, ensure that errors result in a non-zero exit code and a clear message to the user on `stderr`.


---
description: Documentation Standards and Requirements
globs: **/*.py,**/*.md,**/*.rst
alwaysApply: false
---
# Documentation Rules

- All public functions, classes, and modules should have a docstring explaining their purpose, arguments, and return values.
- Follow a consistent docstring format (e.g., Google, reStructuredText).
- Use inline comments to explain complex or non-obvious parts of the code.
- Keep the `README.md` and other documentation files (`RELEASER.md`) up-to-date with any changes to functionality, setup, or usage.
- Ensure all examples in the documentation are tested and working.

---
description: CLI Design and Implementation Rules
globs: **/*cli*.py,**/main.py,**/__main__.py
alwaysApply: false
---
# CLI Design Rules

- Use Python's `argparse` module for parsing command-line arguments.
- Provide clear and descriptive help messages for all arguments (`help='...'`).
- Define default values for optional arguments where it makes sense.
- Validate user inputs and provide friendly error messages for invalid arguments.
- Ensure the CLI returns appropriate exit codes (0 for success, non-zero for errors).


---
description: API Client Implementation Rules
globs: **/*.py,**/api/**/*.py,**/client/**/*.py
alwaysApply: false
---
# API Client Rules

- Centralize API call logic into dedicated functions.
- Implement robust error handling for API requests, including connection errors, timeouts, and API-specific errors (e.g., rate limits, authentication).
- Use `try...except` blocks to gracefully handle potential `requests.exceptions.RequestException` or provider-specific exceptions.
- Configure a reasonable timeout for all external API calls.
- Avoid exposing API keys directly in the code; always load them from environment variables.
