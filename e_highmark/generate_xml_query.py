from lxml import etree
from xml_headers import *
from xml_inquiry import *


def create_xml_query_1(applicant_params, address_params, application_params):

    root = etree.Element("REQUEST-REQUEST-FILE")
    head = etree.SubElement(root, "HEADER-SEGMENT")
    add_header(head)
    inquiry = etree.SubElement(root, "INQUIRY")
    add_inquiry(inquiry, applicant_params, address_params, application_params)

    r = etree.tostring(root, pretty_print=True)

    return etree.tostring(root)
