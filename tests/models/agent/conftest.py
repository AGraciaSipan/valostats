import pytest


@pytest.fixture(
    params=[
        {"uuid": "4ee40330-ecdd-4f2f-98a8-eb1243428373", "displayName": "Controller"},
        {"uuid": "dbe8757e-9e92-4ed4-b39f-9dfc589691d4", "displayName": "Duelist"},
        {"uuid": "1b47567f-8f7b-444b-aae3-b0c634622d10", "displayName": "Initiator"},
        {"uuid": "5fc02f99-4091-4486-a531-98459a3e95e9", "displayName": "Sentinel"},
    ]
)
def role_data(request):
    return request.param
