import requests
import generate_xml_query
import generate_second_xml_query
import xml.etree.ElementTree as ET
from esthenos import settings
from lxml import etree
from flask import render_template
from esthenos import mainapp
import time


def get_acknowledgement(query_1_header):
    url = settings.ORGS_SETTINGS["highmark-url"]
    response_1 = requests.post(url, verify=False, headers=query_1_header)
    return response_1


def get_query_header(query):
    uname = settings.ORGS_SETTINGS["highmark-uname"]
    passwd = settings.ORGS_SETTINGS["highmark-password"]
    header = {'requestXml':query, 'userid': uname, 'password':passwd, 'productType':'INDV',\
                      'productVersion':'1.0', 'mbrid':settings.ORGS_SETTINGS["esthenos-client-mbrid"], 'reqVolType':'INDV'}
    return header


def get_params_from_ack(parsed_response_1):
    return parsed_response_1.find('.//INQUIRY-UNIQUE-REF-NO').text,\
           parsed_response_1.find('.//REQUEST-DT-TM').text, \
           parsed_response_1.find('.//REPORT-ID').text


def get_response(query_2_header):
    url = settings.ORGS_SETTINGS["highmark-url"]
    return requests.post(url, verify=False, headers=query_2_header)


def send_request(applicant_params, address_params, application_params):
    url = settings.ORGS_SETTINGS["highmark-url"]

    query = generate_xml_query.create_xml_query_1(applicant_params, address_params, application_params)
    mainapp.logger.debug("--"*23)
    mainapp.logger.debug("QUERY 1:%s" % query)
    query_1_header = get_query_header(query)

    mainapp.logger.debug("--"*23)
    mainapp.logger.debug("QUERY HEADER:%s" % query_1_header)

    response_1 = get_acknowledgement(query_1_header)
    mainapp.logger.debug("ACK RESPONSE:%s" % response_1)

    if response_1.status_code != 200:
        return response_1

    parsed_response_1 = ET.fromstring(response_1.content)
    response_1_errors = {}

    if parsed_response_1.findall("./INQUIRY-STATUS/INQUIRY//ERROR"):
        for i in parsed_response_1.findall("./INQUIRY-STATUS/INQUIRY//ERROR"):
            response_1_errors[i.find('./CODE').text] = i.find('./DESCRIPTION').text
        return response_1

    uid, qdt, rid = get_params_from_ack(parsed_response_1)

    query_2 = generate_second_xml_query.create_second_xml_query(uid, qdt, rid)

    mainapp.logger.debug("--"*23)
    mainapp.logger.debug("QUERY 2:%s" % query_2)

    query_2_header = get_query_header(query_2)

    time.sleep(4)
    response_2 = get_response(query_2_header)

    if response_2.status_code != 200:
        return response_2

    return response_2
