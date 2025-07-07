import os
import pytest
from django.conf import settings


def pytest_configure():
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
