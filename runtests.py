#! /usr/bin/env python

import os
import subprocess
import sys

import pytest

PYTEST_ARGS = {
    "default": ["tests", "--allow-skip-extra-system-req"],
    "fast": ["tests", "-q"],
}

sys.path.append(os.path.dirname(__file__))


def exit_on_failure(ret, message=None):
    if ret:
        sys.exit(ret)


def split_class_and_function(string):
    class_string, function_string = string.split(".", 1)
    return "%s and %s" % (class_string, function_string)


def is_function(string):
    # `True` if it looks like a test function is included in the string.
    return string.startswith("test_") or ".test_" in string


def is_class(string):
    # `True` if first character is uppercase - assume it's a class name.
    return string[0] == string[0].upper()


if __name__ == "__main__":
    try:
        sys.argv.remove("--fast")
    except ValueError:
        style = "default"
    else:
        style = "fast"

    if len(sys.argv) > 1:
        pytest_args = sys.argv[1:]
        first_arg = pytest_args[0]
        if first_arg.startswith("-"):
            pytest_args = ["tests"] + pytest_args
        elif is_class(first_arg) and is_function(first_arg):
            expression = split_class_and_function(first_arg)
            pytest_args = ["tests", "-k", expression] + pytest_args[1:]
        elif is_class(first_arg) or is_function(first_arg):
            pytest_args = ["tests", "-k", pytest_args[0]] + pytest_args[1:]
    else:
        pytest_args = PYTEST_ARGS[style]

    exit_on_failure(pytest.main(pytest_args))
