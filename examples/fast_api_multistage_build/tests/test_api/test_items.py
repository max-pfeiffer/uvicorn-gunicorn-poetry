import random
from unittest import TestCase

import pytest

from starlette import status

from app.main import ITEMS


@pytest.mark.usefixtures("client")
class ApiItemsTestCase(TestCase):

    def test_items(self):
        key, value = random.choice(list(ITEMS.items()))

        response = self.client.get('/items/{}'.format(key))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
