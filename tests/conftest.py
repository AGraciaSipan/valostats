from uuid import uuid4

import pytest


@pytest.fixture()
def uuid():
    return uuid4()
