""" Fixtures files for type version manager
"""
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface
from core_composer_app.components.type.models import Type
from core_composer_app.components.type_version_manager.models import TypeVersionManager


class TypeVersionManagerFixtures(FixtureInterface):
    """Type Version Manager fixtures"""

    type_1_1 = None
    type_1_2 = None
    type_1_3 = None
    type_2_1 = None
    type_vm_1 = None
    type_vm_2 = None
    type_vm_collection = None

    def insert_data(self):
        """Insert a set of Types and Type Version Managers.

        Returns:

        """
        self.type_vm_1 = TypeVersionManager(
            title="type 1",
            user=None,
            is_disabled=False,
        )
        self.type_vm_1.save_version_manager()
        self.type_1_1 = Type(
            filename="type1_1.xsd",
            content="content1_1",
            hash="hash1_1",
            is_complex=True,
            version_manager=self.type_vm_1,
        )
        self.type_1_1.save_template()
        self.type_1_2 = Type(
            filename="type1_2.xsd",
            content="content1_2",
            hash="hash1_2",
            is_complex=True,
            version_manager=self.type_vm_1,
            is_disabled=True,
        )
        self.type_1_2.save_template()
        self.type_1_3 = Type(
            filename="type1_3.xsd",
            content="content1_3",
            hash="hash1_3",
            is_complex=True,
            version_manager=self.type_vm_1,
            is_current=True,
        )
        self.type_1_3.save_template()

        self.type_vm_2 = TypeVersionManager(
            title="type 2",
            user="1",
            is_disabled=False,
        )
        self.type_vm_2.save_version_manager()

        self.type_2_1 = Type(
            filename="type2_1.xsd",
            content="content2_1",
            hash="hash2_1",
            is_complex=True,
            version_manager=self.type_vm_2,
            is_current=True,
        )
        self.type_2_1.save_template()

        self.type_vm_collection = [self.type_vm_1, self.type_vm_2]
