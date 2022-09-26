"""Unit tests for composer xml operations
"""
# TODO: add tests for other xml utils

from os.path import join, dirname, abspath
from unittest.case import TestCase

from core_main_app.commons.exceptions import CoreError
from core_main_app.utils.xml import validate_xml_schema
from core_composer_app.utils.xml import (
    _insert_element_type,
    check_type_core_support,
    COMPLEX_TYPE,
    SIMPLE_TYPE,
)

RESOURCES_PATH = join(dirname(abspath(__file__)), "data")


class TestInsertElementType(TestCase):
    """Test Insert Element Type"""

    def setUp(self):
        """setUp"""

        self.root_xpath = "xsd:complexType/xsd:sequence"
        self.type_name = "new"

    def test_add_type_to_base(self):
        """test_add_type_to_base"""

        base_filename = "base.xsd"
        type_filename = "type.xsd"
        # load test resources
        with open(join(RESOURCES_PATH, base_filename), "r") as base_file:
            base_content = base_file.read()
        with open(join(RESOURCES_PATH, type_filename), "r") as type_file:
            type_content = type_file.read()

        result_tree = _insert_element_type(
            base_content,
            self.root_xpath,
            type_content,
            self.type_name,
            join(RESOURCES_PATH, type_filename),
        )

        errors = validate_xml_schema(result_tree, request=None)
        self.assertTrue(errors is None)

    def test_add_type_with_target_namespace_to_base(self):
        """test_add_type_with_target_namespace_to_base"""

        base_filename = "base.xsd"
        type_filename = "type_target_ns.xsd"
        # load test resources
        with open(join(RESOURCES_PATH, base_filename), "r") as base_file:
            base_content = base_file.read()
        with open(join(RESOURCES_PATH, type_filename), "r") as type_file:
            type_content = type_file.read()

        with self.assertRaises(CoreError):
            _insert_element_type(
                base_content,
                self.root_xpath,
                type_content,
                self.type_name,
                join(RESOURCES_PATH, type_filename),
            )

    def test_add_type_to_base_with_target_namespace(self):
        """test_add_type_to_base_with_target_namespace"""

        base_filename = "base_target_ns.xsd"
        type_filename = "type.xsd"
        # load test resources
        with open(join(RESOURCES_PATH, base_filename), "r") as base_file:
            base_content = base_file.read()
        with open(join(RESOURCES_PATH, type_filename), "r") as type_file:
            type_content = type_file.read()

        result_tree = _insert_element_type(
            base_content,
            self.root_xpath,
            type_content,
            self.type_name,
            join(RESOURCES_PATH, type_filename),
        )

        errors = validate_xml_schema(result_tree, request=None)
        self.assertTrue(errors is None)

    def test_add_type_with_target_namespace_to_base_with_same_target_namespace(
        self,
    ):
        """test_add_type_with_target_namespace_to_base_with_same_target_namespace"""

        base_filename = "base_target_ns.xsd"
        type_filename = "type_base_target_ns.xsd"
        # load test resources
        with open(join(RESOURCES_PATH, base_filename), "r") as base_file:
            base_content = base_file.read()
        with open(join(RESOURCES_PATH, type_filename), "r") as type_file:
            type_content = type_file.read()

        result_tree = _insert_element_type(
            base_content,
            self.root_xpath,
            type_content,
            self.type_name,
            join(RESOURCES_PATH, type_filename),
        )

        errors = validate_xml_schema(result_tree, request=None)
        self.assertTrue(errors is None)

    def test_add_type_with_target_namespace_to_base_with_different_target_namespace(
        self,
    ):
        """test_add_type_with_target_namespace_to_base_with_different_target_namespace"""

        base_filename = "base_target_ns.xsd"
        type_filename = "type_target_ns.xsd"
        # load test resources
        with open(join(RESOURCES_PATH, base_filename), "r") as base_file:
            base_content = base_file.read()
        with open(join(RESOURCES_PATH, type_filename), "r") as type_file:
            type_content = type_file.read()

        with self.assertRaises(CoreError):
            _insert_element_type(
                base_content,
                self.root_xpath,
                type_content,
                self.type_name,
                join(RESOURCES_PATH, type_filename),
            )

    def test_add_type_with_target_namespace_prefix_to_base(self):
        """test_add_type_with_target_namespace_prefix_to_base"""

        base_filename = "base.xsd"
        type_filename = "type_target_ns_prefix.xsd"
        # load test resources
        with open(join(RESOURCES_PATH, base_filename), "r") as base_file:
            base_content = base_file.read()
        with open(join(RESOURCES_PATH, type_filename), "r") as type_file:
            type_content = type_file.read()

        result_tree = _insert_element_type(
            base_content,
            self.root_xpath,
            type_content,
            self.type_name,
            join(RESOURCES_PATH, type_filename),
        )

        errors = validate_xml_schema(result_tree, request=None)
        self.assertTrue(errors is None)

    def test_add_type_with_target_namespace_prefix_to_base_with_same_target_namespace_prefix(
        self,
    ):
        """test_add_type_with_target_namespace_prefix_to_base_with_same_target_namespace_prefix"""

        base_filename = "base_target_ns.xsd"
        type_filename = "type_base_target_ns_prefix.xsd"
        # load test resources
        with open(join(RESOURCES_PATH, base_filename), "r") as base_file:
            base_content = base_file.read()
        with open(join(RESOURCES_PATH, type_filename), "r") as type_file:
            type_content = type_file.read()

        result_tree = _insert_element_type(
            base_content,
            self.root_xpath,
            type_content,
            self.type_name,
            join(RESOURCES_PATH, type_filename),
        )

        errors = validate_xml_schema(result_tree, request=None)
        self.assertTrue(errors is None)

    def test_add_type_with_target_namespace_prefix_to_base_with_different_target_namespace_prefix(
        self,
    ):
        """test_add_type_with_target_namespace_prefix_to_base_with_different_target_namespace_prefix"""

        base_filename = "base_target_ns.xsd"
        type_filename = "type_target_ns_prefix.xsd"
        # load test resources
        with open(join(RESOURCES_PATH, base_filename), "r") as base_file:
            base_content = base_file.read()
        with open(join(RESOURCES_PATH, type_filename), "r") as type_file:
            type_content = type_file.read()

        result_tree = _insert_element_type(
            base_content,
            self.root_xpath,
            type_content,
            self.type_name,
            join(RESOURCES_PATH, type_filename),
        )

        errors = validate_xml_schema(result_tree, request=None)
        self.assertTrue(errors is None)


class TestTypeDefinition(TestCase):
    """Test Type Definition"""

    def test_simple_type(self):
        """test_simple_type"""

        type_filename = "type.xsd"
        # load test resources
        with open(join(RESOURCES_PATH, type_filename), "r") as type_file:
            type_content = type_file.read()

        type_content = check_type_core_support(type_content)

        self.assertEqual(type_content, SIMPLE_TYPE)

    def test_complex_type(self):
        """test_complex_type"""

        type_filename = "type_complex.xsd"
        # load test resources
        with open(join(RESOURCES_PATH, type_filename), "r") as type_file:
            type_content = type_file.read()

        type_content = check_type_core_support(type_content)

        self.assertEqual(type_content, COMPLEX_TYPE)
