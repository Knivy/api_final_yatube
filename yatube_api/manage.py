#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management import (  # type: ignore
    execute_from_command_line,)


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatube_api.settings')
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
