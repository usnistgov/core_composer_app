"""XML utils for Composer app
"""
from core_main_app.commons.exceptions import CoreError, XMLError
from core_main_app.utils.xml import is_well_formed_xml
from xml_utils.xsd_tree.xsd_tree import XSDTree


def check_type_core_support(xsd_string):
    """Check that the format of the the type is supported by the current version of the Core

    Args:
        xsd_string:

    Returns:

    """
    error_message = "A type should be a valid XML schema containing only one type definition " \
                    "(Allowed tags are: simpleType or complexType and include)."

    # check that well formatted first
    if not is_well_formed_xml(xsd_string):
        raise XMLError('Uploaded file is not well formatted XML.')

    # build the tree
    xsd_tree = XSDTree.build_tree(xsd_string)

    # get elements
    elements = xsd_tree.findall("*")

    if len(elements) > 0:
        # only simpleType, complexType or include
        for element in elements:
            if 'complexType' not in element.tag \
                    and 'simpleType' not in element.tag \
                    and 'include' not in element.tag:
                raise CoreError(error_message)

        # only one type
        cpt_type = 0
        for element in elements:
            if 'complexType' in element.tag or 'simpleType' in element.tag:
                cpt_type += 1
                if cpt_type > 1:
                    raise CoreError(error_message)
    else:
        raise CoreError(error_message)
