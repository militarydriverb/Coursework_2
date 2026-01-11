import unittest

from vacancy import Vacancy


class TestVacancy(unittest.TestCase):
    """
    Test cases for the Vacancy class.
    """

    def test_initialization(self):
        """Test vacancy initialization with valid data."""
        vacancy = Vacancy(
            name="Python Developer",
            url="https://hh.ru/vacancy/123456",
            salary={"from": 100000, "to": 150000},
            description="Development of Python applications",
        )

        self.assertEqual(vacancy.name, "Python Developer")
        self.assertEqual(vacancy.url, "https://hh.ru/vacancy/123456")
        self.assertEqual(vacancy.salary["from"], 100000)
        self.assertEqual(vacancy.salary["to"], 150000)
        self.assertEqual(vacancy.description, "Development of Python applications")

    def test_name_validation(self):
        """Test name validation."""
        # Test empty name
        with self.assertRaises(ValueError):
            Vacancy("", "https://example.com", {"from": 100000}, "Description")

        # Test whitespace name
        with self.assertRaises(ValueError):
            Vacancy("   ", "https://example.com", {"from": 100000}, "Description")

    def test_url_validation(self):
        """Test URL validation."""
        # Test invalid URL (not starting with http)
        with self.assertRaises(ValueError):
            Vacancy("Python Developer", "example.com", {"from": 100000}, "Description")

        # Test valid URL
        vacancy = Vacancy("Python Developer", "http://example.com", {"from": 100000}, "Description")
        self.assertEqual(vacancy.url, "http://example.com")

    def test_salary_validation_none(self):
        """Test salary validation when salary is None."""
        vacancy = Vacancy("Python Developer", "https://example.com", None, "Description")
        self.assertEqual(vacancy.salary["from"], 0)
        self.assertEqual(vacancy.salary["to"], 0)

    def test_salary_validation_dict(self):
        """Test salary validation with dictionary."""
        # Test with both from and to
        vacancy = Vacancy(
            "Python Developer",
            "https://example.com",
            {"from": 100000, "to": 150000},
            "Description",
        )
        self.assertEqual(vacancy.salary["from"], 100000)
        self.assertEqual(vacancy.salary["to"], 150000)

        # Test with only from
        vacancy = Vacancy("Python Developer", "https://example.com", {"from": 100000}, "Description")
        self.assertEqual(vacancy.salary["from"], 100000)
        self.assertEqual(vacancy.salary["to"], 0)

        # Test with only to
        vacancy = Vacancy("Python Developer", "https://example.com", {"to": 150000}, "Description")
        self.assertEqual(vacancy.salary["from"], 0)
        self.assertEqual(vacancy.salary["to"], 150000)

    def test_salary_validation_string(self):
        """Test salary validation with string."""
        # Test range format
        vacancy = Vacancy(
            "Python Developer",
            "https://example.com",
            "100 000-150 000 руб.",
            "Description",
        )
        self.assertEqual(vacancy.salary["from"], 100000)
        self.assertEqual(vacancy.salary["to"], 150000)

        # Test single value
        vacancy = Vacancy("Python Developer", "https://example.com", "120000 руб.", "Description")
        self.assertEqual(vacancy.salary["from"], 120000)
        self.assertEqual(vacancy.salary["to"], 120000)

        # Test value without spaces
        vacancy = Vacancy("Python Developer", "https://example.com", "80000", "Description")
        self.assertEqual(vacancy.salary["from"], 80000)
        self.assertEqual(vacancy.salary["to"], 80000)

    def test_comparison_methods(self):
        """Test comparison methods."""
        vacancy1 = Vacancy(
            "Python Developer 1",
            "https://example.com/1",
            {"from": 100000},
            "Description 1",
        )

        vacancy2 = Vacancy(
            "Python Developer 2",
            "https://example.com/2",
            {"from": 150000},
            "Description 2",
        )

        # Test less than
        self.assertTrue(vacancy1 < vacancy2)
        self.assertFalse(vacancy2 < vacancy1)

        # Test less than or equal
        self.assertTrue(vacancy1 <= vacancy2)
        self.assertTrue(vacancy1 <= vacancy1)

        # Test greater than
        self.assertTrue(vacancy2 > vacancy1)
        self.assertFalse(vacancy1 > vacancy2)

        # Test greater than or equal
        self.assertTrue(vacancy2 >= vacancy1)
        self.assertTrue(vacancy1 >= vacancy1)

        # Test equality
        vacancy3 = Vacancy(
            "Python Developer 3",
            "https://example.com/3",
            {"from": 100000},
            "Description 3",
        )
        self.assertTrue(vacancy1 == vacancy3)
        self.assertFalse(vacancy1 == vacancy2)

    def test_string_representation(self):
        """Test string representation methods."""
        vacancy = Vacancy(
            name="Python Developer",
            url="https://hh.ru/vacancy/123456",
            salary={"from": 100000, "to": 150000},
            description="Development of Python applications",
        )

        # Test __str__
        str_output = str(vacancy)
        self.assertIn("Python Developer", str_output)
        self.assertIn("100000-150000 руб.", str_output)
        self.assertIn("https://hh.ru/vacancy/123456", str_output)
        self.assertIn("Описание: Development of Python applications", str_output)

        # Test __repr__
        repr_output = repr(vacancy)
        self.assertIn("Vacancy", repr_output)
        self.assertIn("name='Python Developer'", repr_output)
        self.assertIn("url='https://hh.ru/vacancy/123456'", repr_output)
        self.assertIn("salary={'from': 100000, 'to': 150000}", repr_output)
