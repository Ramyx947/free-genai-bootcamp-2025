#!/bin/bash

# Run guardrails tests first
poetry run pytest tests/utils/test_guardrails.py tests/utils/test_middleware.py -v

if [ $? -ne 0 ]; then
    echo "Guardrails tests failed!"
    exit 1
fi

# Run all tests with coverage
poetry run pytest --cov=app tests/ --cov-report=term-missing

if [ $? -ne 0 ]; then
    echo "Tests failed!"
    exit 1
fi

echo "All tests passed successfully!" 