#!/bin/bash
# PostStop hook: Runs project tests when Claude Code session stops
# Non-blocking in power pack

# Detect test runner
if [ -f "package.json" ]; then
    # Node.js project
    if command -v npm >/dev/null 2>&1; then
        npm test >/dev/null 2>&1 &
    fi
elif [ -f "pytest.ini" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
    # Python project
    if command -v pytest >/dev/null 2>&1; then
        pytest >/dev/null 2>&1 &
    fi
elif [ -f "Makefile" ]; then
    # Check for test target
    if grep -q "^test:" Makefile; then
        make test >/dev/null 2>&1 &
    fi
fi

# Always allow (non-blocking)
exit 0
