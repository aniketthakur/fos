from lxml import etree
from esthenos import settings
import time


def add_header(root):
    etree.SubElement(root, "PRODUCT-TYP").text="INDV"
    etree.SubElement(root, "PRODUCT-VER").text="1.0"
    etree.SubElement(root, "REQ-MBR").text=settings.ORGS_SETTINGS["esthenos-client-mbrid"]
    etree.SubElement(root, "SUB-MBR-ID").text=settings.ORGS_SETTINGS["esthenos-client"]
    etree.SubElement(root, "INQ-DT-TM").text=time.strftime("%d-%m-%Y %H:%M:%S")
    etree.SubElement(root, "REQ-ACTN-TYP").text="ISSUE"
    etree.SubElement(root, "TEST-FLAG").text="N"
    etree.SubElement(root, "AUTH-FLG").text="Y"
    etree.SubElement(root, "AUTH-TITLE").text="USER"
    etree.SubElement(root, "RES-FRMT").text="XML/HTML"
    etree.SubElement(root, "MEMBER-PRE-OVERRIDE").text="N"
    etree.SubElement(root, "RES-FRMT-EMBD").text="Y"
    etree.SubElement(root, "LOS-NAME").text=settings.ORGS_SETTINGS["los-name"]
    etree.SubElement(root, "LOS-VENDER").text=settings.ORGS_SETTINGS["los-vendor"]
    etree.SubElement(root, "LOS-VERSION").text=settings.ORGS_SETTINGS["los-version"]
    mfi = etree.SubElement(root, "MFI")
    etree.SubElement(mfi, "INDV").text="true"
    etree.SubElement(mfi, "SCORE").text="true"
    etree.SubElement(mfi, "GROUP").text="true"
    consumer = etree.SubElement(root, "CONSUMER")
    etree.SubElement(consumer, "INDV").text="true"
    etree.SubElement(consumer, "SCORE").text="true"
    etree.SubElement(root, "IOI").text="true"


def add_inquiry(root, ref_no, date_time, report_id):
    etree.SubElement(root, "INQUIRY-UNIQUE-REF-NO").text=ref_no
    etree.SubElement(root, "REQUEST-DT-TM").text=date_time
    etree.SubElement(root, "REPORT-ID").text=report_id


def create_second_xml_query(ref_no, date_time, report_id):

    root = etree.Element("REQUEST-REQUEST-FILE")
    head = etree.SubElement(root, "HEADER-SEGMENT")

    add_header(head)
    inquiry = etree.SubElement(root, "INQUIRY")
    add_inquiry(inquiry,ref_no, date_time, report_id)
    r = etree.tostring(root, pretty_print=True)

    return etree.tostring(root)