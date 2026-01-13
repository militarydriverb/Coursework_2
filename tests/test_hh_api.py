import unittest
from unittest.mock import Mock, patch

from hh_api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):
    """
    Test cases for the HeadHunterAPI class.
    """

    @patch("hh_api.requests.get")
    def test_connect_to_api_success(self, mock_get):
        """Test successful connection to API."""
        # Mock successful response
        # mock_response = Mock()
        mock_response = Mock(status_code = 200)
        mock_get.return_value = mock_response

        try:
            api = HeadHunterAPI()
            result = api.connect_to_api()

            self.assertTrue(result)
            mock_get.assert_called_once()
        except Exception as e:
            self.fail(f"Test failed with exception: {e}")

    @patch("hh_api.requests.get")
    def test_connect_to_api_failure(self, mock_get):
        """Test failed connection to API."""
        # Mock failed response
        mock_get.side_effect = Exception("Connection failed")

        try:
            api = HeadHunterAPI()
            result = api.connect_to_api()

            self.assertFalse(result)
        except Exception:
            self.fail("Test failed with exception")

    @patch("hh_api.HeadHunterAPI.connect_to_api")
    @patch("hh_api.requests.get")
    def test_get_vacancies_success(self, mock_get, mock_connect):
        """Test successful retrieval of vacancies."""
        # Mock successful connection
        mock_connect.return_value = True

        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "Python Developer",
                    "alternate_url": "https://hh.ru/vacancy/123456",
                    "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                    "snippet": {"requirement": "Python experience required"},
                }
            ],
            "pages": 1,
        }
        mock_get.return_value = mock_response

        try:
            api = HeadHunterAPI()
            vacancies = api.get_vacancies("Python")

            self.assertEqual(len(vacancies), 1)
            self.assertEqual(vacancies[0]["name"], "Python Developer")
            self.assertEqual(vacancies[0]["url"], "https://hh.ru/vacancy/123456")
            # Compare salary without currency as it's not in the expected format
            self.assertEqual(vacancies[0]["salary"]["from"], 100000)
            self.assertEqual(vacancies[0]["salary"]["to"], 150000)
            self.assertEqual(vacancies[0]["description"], "Python experience required")
        except Exception as e:
            self.fail(f"Test failed with exception: {e}")

    @patch("hh_api.HeadHunterAPI.connect_to_api")
    def test_get_vacancies_connection_failure(self, mock_connect):
        """Test vacancies retrieval when connection fails."""
        # Mock failed connection
        mock_connect.return_value = False

        try:
            api = HeadHunterAPI()
            vacancies = api.get_vacancies("Python")

            # Check that we get an empty list when connection fails
            self.assertEqual(len(vacancies), 0)
            mock_connect.assert_called_once()
        except Exception:
            self.fail("Test failed with exception")

    @patch("hh_api.HeadHunterAPI.connect_to_api")
    @patch("hh_api.requests.get")
    def test_get_vacancies_request_exception(self, mock_get, mock_connect):
        """Test vacancies retrieval when request raises exception."""
        # Mock successful connection
        mock_connect.return_value = True

        # Mock request exception
        mock_get.side_effect = Exception("Request failed")

        try:
            api = HeadHunterAPI()
            vacancies = api.get_vacancies("Python")

            # Should return empty list when request fails
            self.assertEqual(len(vacancies), 0)
        except Exception as e:
            self.fail(f"Test failed with exception: {e}")

    @patch("hh_api.HeadHunterAPI.connect_to_api")
    @patch("hh_api.requests.get")
    def test_get_vacancies_key_error(self, mock_get, mock_connect):
        """Test vacancies retrieval when response has unexpected structure."""
        # Mock successful connection
        mock_connect.return_value = True

        # Mock response with missing keys
        # mock_response = Mock()
        mock_response = Mock(status_code = 200)
        mock_response.json.return_value = {}  # Empty response
        mock_get.return_value = mock_response

        try:
            api = HeadHunterAPI()
            vacancies = api.get_vacancies("Python")

            # Should return empty list when response has unexpected structure
            self.assertEqual(len(vacancies), 0)
        except Exception as e:
            self.fail(f"Test failed with exception: {e}")
