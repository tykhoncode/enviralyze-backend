import pytest
from lists.models import List

pytestmark = pytest.mark.django_db

def test_list_str(user):
    lst = List.objects.create(name="Groceries", owner=user)
    assert str(lst) == "Groceries (custom list)"