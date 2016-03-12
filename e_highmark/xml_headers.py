import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lxml import etree
import time
from esthenos import settings

def add_mfi(root):
    etree.SubElement(root, "INDV").text="true"
    etree.SubElement(root, "SCORE").text="true"
    etree.SubElement(root, "GROUP").text="true"


def add_consumer(root):
    etree.SubElement(root, "INDV").text="true"
    etree.SubElement(root, "SCORE").text="true"


def add_header(root):

    etree.SubElement(root, "PRODUCT-TYP").text="INDV"
    etree.SubElement(root, "PRODUCT-VER").text="1.0"
    etree.SubElement(root, "REQ-MBR").text=settings.ORGS_SETTINGS["esthenos-client-mbrid"]
    etree.SubElement(root, "SUB-MBR-ID").text=settings.ORGS_SETTINGS["esthenos-client"]
    etree.SubElement(root, "INQ-DT-TM").text=time.strftime("%d-%m-%Y %H:%M:%S")
    etree.SubElement(root, "REQ-ACTN-TYP").text="SUBMIT"
    etree.SubElement(root, "TEST-FLG").text="N"
    etree.SubElement(root, "AUTH-FLG").text="Y"
    etree.SubElement(root, "AUTH-TITLE").text="USER"
    etree.SubElement(root, "RES-FRMT").text="XML/HTML"
    etree.SubElement(root, "MEMBER-PRE-OVERRIDE").text="N"
    etree.SubElement(root, "RES-FRMT-EMBD").text="Y"
    etree.SubElement(root, "LOS-NAME").text=settings.ORGS_SETTINGS["los-name"]
    etree.SubElement(root, "LOS-VENDER").text=settings.ORGS_SETTINGS["los-vendor"]
    etree.SubElement(root, "LOS-VERSION").text=settings.ORGS_SETTINGS["los-version"]

    mfi_head = etree.SubElement(root, 'MFI')
    add_mfi(mfi_head)

    consumer_head = etree.SubElement(root, 'CONSUMER')
    add_consumer(consumer_head)

    etree.SubElement(root, 'IOI').text="true"