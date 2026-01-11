import json
import os
import unittest

from json_saver import JSONSaver


class TestJSONSaver(unittest.TestCase):
    """
    Test cases for the JSONSaver class.
    """

    TEST_FILE = "test_vacancies.json"

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Remove test file if it exists
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

        try:
            self.saver = JSONSaver(self.TEST_FILE)
        except Exception:
            self.fail("Failed to create JSONSaver instance")

    def tearDown(self):
        """Tear down test fixtures after each test method."""
        # Remove test file after test
        try:
            if os.path.exists(self.TEST_FILE):
                os.remove(self.TEST_FILE)
        except (OSError, IOError):
            pass  # Ignore cleanup errors

    def test_create_file_if_not_exists(self):
        """Test that file is created if it doesn't exist."""
        # Remove file to test creation
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

        try:
            saver = JSONSaver(self.TEST_FILE)
            self.assertTrue(os.path.exists(self.TEST_FILE))

            # Check file is valid JSON
            with open(self.TEST_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.assertEqual(data, [])
        except (OSError, IOError) as e:
            self.fail(f"Test failed with exception: {e}")

    def test_add_vacancy(self):
        """Test adding a vacancy to the file."""
        vacancy = {
            "name": "Python Developer",
            "url": "https://hh.ru/vacancy/123456",
            "salary": {"from": 100000, "to": 150000},
            "description": "Development of Python applications",
        }

        try:
            self.saver.add_vacancy(vacancy)

            # Check file exists and contains the vacancy
            self.assertTrue(os.path.exists(self.TEST_FILE))

            with open(self.TEST_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["name"], "Python Developer")
            self.assertEqual(data[0]["url"], "https://hh.ru/vacancy/123456")
        except Exception as e:
            self.fail(f"Test failed with exception: {e}")
        finally:
            # Remove the temporary file
            if os.path.exists(self.TEST_FILE):
                os.remove(self.TEST_FILE)

    def test_add_vacancy_duplicate(self):
        """Test that duplicate vacancies are not added."""
        vacancy = {
            "name": "Python Developer",
            "url": "https://hh.ru/vacancy/123456",
            "salary": {"from": 100000, "to": 150000},
            "description": "Development of Python applications"
        }

        try:
            # Add vacancy twice
            self.saver.add_vacancy(vacancy)
            self.saver.add_vacancy(vacancy)

            # Check only one vacancy in file
            with open(self.TEST_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.assertEqual(len(data), 1)
        except (OSError, IOError) as e:
            self.fail(f"Test failed with exception: {e}")

    def test_get_vacancies_no_criteria(self):
        """Test getting all vacancies without criteria."""
        vacancy1 = {
            "name": "Python Developer",
            "url": "https://hh.ru/vacancy/123456",
            "salary": {"from": 100000, "to": 150000},
            "description": "Python development"
        }

        vacancy2 = {
            "name": "Java Developer",
            "url": "https://hh.ru/vacancy/789012",
            "salary": {"from": 120000, "to": 180000},
            "description": "Java development"
        }

        try:
            self.saver.add_vacancy(vacancy1)
            self.saver.add_vacancy(vacancy2)

            vacancies = self.saver.get_vacancies()

            self.assertEqual(len(vacancies), 2)
            self.assertEqual(vacancies[0]["name"], "Python Developer")
            self.assertEqual(vacancies[1]["name"], "Java Developer")
        except (OSError, IOError) as e:
            self.fail(f"Test failed with exception: {e}")

    def test_get_vacancies_with_string_criteria(self):
        """Test getting vacancies with string search criteria."""
        vacancy1 = {
            "name": "Python Developer",
            "url": "https://hh.ru/vacancy/123456",
            "salary": {"from": 100000, "to": 150000},
            "description": "Looking for Python developer with Django experience",
        }

        vacancy2 = {
            "name": "Java Developer",
            "url": "https://hh.ru/vacancy/789012",
            "salary": {"from": 120000, "to": 180000},
            "description": "Java developer needed for backend development",
        }

        try:
            self.saver.add_vacancy(vacancy1)
            self.saver.add_vacancy(vacancy2)

            # Search for Python
            python_vacancies = self.saver.get_vacancies("Python")
            self.assertEqual(len(python_vacancies), 1)
            self.assertEqual(python_vacancies[0]["name"], "Python Developer")

            # Search for Java
            java_vacancies = self.saver.get_vacancies("Java")
            self.assertEqual(len(java_vacancies), 1)
            self.assertEqual(java_vacancies[0]["name"], "Java Developer")

            # Search for Django
            django_vacancies = self.saver.get_vacancies("Django")
            self.assertEqual(len(django_vacancies), 1)
            self.assertEqual(django_vacancies[0]["name"], "Python Developer")
        except Exception as e:
            self.fail(f"Test failed with exception: {e}")

    def test_get_vacancies_with_callable_criteria(self):
        """Test getting vacancies with callable criteria."""
        vacancy1 = {
            "name": "Python Developer",
            "url": "https://hh.ru/vacancy/123456",
            "salary": {"from": 100000, "to": 150000},
            "description": "Python development",
        }

        vacancy2 = {
            "name": "Senior Python Developer",
            "url": "https://hh.ru/vacancy/789012",
            "salary": {"from": 200000, "to": 250000},
            "description": "Senior Python development",
        }

        try:
            self.saver.add_vacancy(vacancy1)
            self.saver.add_vacancy(vacancy2)

            # Filter by high salary
            high_salary_vacancies = self.saver.get_vacancies(lambda v: v["salary"]["from"] > 150000)

            self.assertEqual(len(high_salary_vacancies), 1)
            self.assertEqual(high_salary_vacancies[0]["name"], "Senior Python Developer")
        except Exception as e:
            self.fail(f"Test failed with exception: {e}")

    def test_delete_vacancy(self):
        """Test deleting a vacancy from the file."""
        vacancy1 = {
            "name": "Python Developer",
            "url": "https://hh.ru/vacancy/123456",
            "salary": {"from": 100000, "to": 150000},
            "description": "Python development",
        }

        vacancy2 = {
            "name": "Java Developer",
            "url": "https://hh.ru/vacancy/789012",
            "salary": {"from": 120000, "to": 180000},
            "description": "Java development",
        }

        try:
            self.saver.add_vacancy(vacancy1)
            self.saver.add_vacancy(vacancy2)

            # Delete Python Developer
            self.saver.delete_vacancy(vacancy1)

            # Check remaining vacancy
            vacancies = self.saver.get_vacancies()
            self.assertEqual(len(vacancies), 1)
            self.assertEqual(vacancies[0]["name"], "Java Developer")

            # Try to delete non-existent vacancy
            self.saver.delete_vacancy(vacancy1)  # Should not raise exception

            # Check still only one vacancy
            vacancies = self.saver.get_vacancies()
            self.assertEqual(len(vacancies), 1)
            self.assertEqual(vacancies[0]["name"], "Java Developer")
        except Exception as e:
            self.fail(f"Test failed with exception: {e}")
