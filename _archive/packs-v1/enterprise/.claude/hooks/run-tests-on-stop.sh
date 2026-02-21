#!/bin/bash
# PostStop hook: Runs project tests when Claude Code session stops
# Optionally blocking in enterprise (configure via settings)

BLOCKING="${CLAUDE_TEST_BLOCKING:-false}"

# Detect test runner
TEST_CMD=""
if [ -f "package.json" ]; then
    # Node.js project
    if command -v npm >/dev/null 2>&1; then
        TEST_CMD="npm test"
    fi
elif [ -f "pytest.ini" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
    # Python project
    if command -v pytest >/dev/null 2>&1; then
        TEST_CMD="pytest"
    fi
elif [ -f "Makefile" ]; then
    # Check for test target
    if grep -q "^test:" Makefile; then
        TEST_CMD="make test"
    fi
fi

if [ -n "$TEST_CMD" ]; then
    if [ "$BLOCKING" = "true" ]; then
        # Blocking mode: wait for tests
        $TEST_CMD
        exit $?
    else
        # Non-blocking mode: run in background
        $TEST_CMD >/dev/null 2>&1 &
    fi
fi

exit 0
