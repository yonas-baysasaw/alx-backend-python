#!/usr/bin/env python3
"""
Unit tests for utility functions: access_nested_map, get_json, and memoize.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize
from typing import Mapping, Sequence, Any, Dict


class TestAccessNestedMap(unittest.TestCase):
    """
    Tests for access_nested_map, which retrieves values from nested dicts
    using a provided path.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence,
                               expected: Any) -> None:
        """Test successful value retrieval via valid nested paths."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping,
                                         path: Sequence) -> None:
        """Test that KeyError is raised when accessing invalid paths."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        self.assertEqual(
            str(context.exception),
            f"'{path[-1]}'"
        )


class TestGetJson(unittest.TestCase):
    """
    Tests for get_json, ensuring it performs HTTP GET and returns JSON data.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: Dict) -> None:
        """Test return value of get_json using a mocked HTTP response."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch(
            'utils.requests.get',
            return_value=mock_response
        ) as mock_get:

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Tests for the memoize decorator, confirming values are cached after the
    first call.
    """

    def test_memoize(self) -> None:
        """Test memoization behavior using a simple class."""

        class TestClass:
            """Simple class for testing the memoize decorator."""

            def a_method(self) -> int:
                return 42

            @memoize
            def a_property(self) -> int:
                """Memoized property returning a_method result."""
                return self.a_method()

        with patch.object(
            TestClass, 'a_method', return_value=42
        ) as mock_method:

            instance = TestClass()

            self.assertEqual(instance.a_property, 42)
            self.assertEqual(instance.a_property, 42)

            mock_method.assert_called_once()
