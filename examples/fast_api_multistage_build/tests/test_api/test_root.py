from unittest import TestCase

import pytest

from starlette import status


@pytest.mark.usefixtures("client")
class ApiRootTestCase(TestCase):

    def test_root(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
