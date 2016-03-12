import xml.etree.ElementTree as ET
from e_organisation.models import EsthenosOrgApplication
from highmark_request import *
from esthenos import settings
import time
import xml.etree.ElementTree as ET
from e_organisation.models import *
from esthenos import mainapp
import re
from collections import Counter
from e_organisation.models import *

def validate_address_params(address_params):

    if not address_params['type_1_city']:
        address_params['type_1_city'] = "KOLKATA"
    if not address_params['type_1_state']:
        address_params['type_1_state'] = "WB"
    if not address_params['type_1_pincode']:
        address_params['type_1_pincode'] = "700012"
    if not address_params['type_1_address']:
        address_params['type_1_address'] = "123 Silk Road Kolkata"


def validate_application_params(application_params):

    if not application_params['BRANCH-ID']:
        application_params['BRANCH-ID'] = "564453"
    # SERIOUS ERROR IF EMPTY
    if not application_params['LOS-APP-ID']:
        application_params['LOS-APP-ID'] = "432rr32434sfsd33rr"
    if not application_params['LOAN-AMOUNT']:
        application_params['LOAN-AMOUNT'] = "10000"


def get_query_params_from_app(app):

    mainapp.logger.debug("=---------------------------INQUIRY HEADER--------------------=")

    application_params = {}
    address_params = {}
    applicant_params = {}

    applicant_name_headers = ['applicant_name_1', 'applicant_name_2', 'applicant_name_3',\
                                  'applicant_name_4', 'applicant_name_5']

    applicant_name = app.applicant_kyc.name.strip().split(" ")

    if applicant_name[0] in ["Mr.", "Mrs.", "Miss", "Late"]:
        applicant_name = applicant_name[1:]

    for i in range(len(applicant_name), 5):
        applicant_name.append("")

    for i, j in zip(applicant_name_headers, applicant_name):
        applicant_params[i] = j

    applicant_id_headers = ['ID01', 'ID02', 'ID03', 'ID04', 'ID05', 'ID06', 'ID07']
    applicant_id_headers_values = ['', '', app.applicant_kyc.kyc_number, '', '', '', '']

    applicant_params["IDS"] = {}

    for i,j in enumerate(zip(applicant_id_headers,applicant_id_headers_values)):
        applicant_params["IDS"][j[0]] = j[1]

    applicant_params['applicant_age_as_on'] = "29/07/2015"

    applicant_params['applicant_dob'] = app.applicant_kyc.dob
    applicant_params['applicant_age'] = app.applicant_kyc.age
    applicant_params['id_type_1'] = "ID01"
    applicant_params['id_type_1_value'] = str(app.applicant_kyc.kyc_number)
    applicant_params['applicant_phone_type_1'] = "P01"
    applicant_params['applicant_phone_1'] = app.applicant_kyc.phone_number

    applicant_relation_headers = ['K01', 'K02', 'K03', 'K04', 'K05', 'K06', 'K07']
    applicant_relation_headers_values = [app.applicant_kyc.father_or_husband_name, app.applicant_kyc.spouse_name]

    applicant_params["REL"] = {}
    i = 0
    for j in applicant_relation_headers_values:
        if j:
            applicant_params["REL"][applicant_relation_headers[i]] = j
            mainapp.logger.debug("RELATION: %s " % i)
            mainapp.logger.debug("RELATION: %s " % applicant_params["REL"][applicant_relation_headers[i]])
            i += 1

    address_params = {}
    address_params['address_type_1'] = "D01"
    address_params['type_1_address'] = app.applicant_kyc.address

    address_params['type_1_city'] = app.applicant_kyc.district
    address_params['type_1_state'] = app.applicant_kyc.state
    address_params['type_1_pincode'] = app.applicant_kyc.pincode

    application_params = {}
    application_params['BRANCH-ID'] = str(app.branch.id)
    application_params['LOS-APP-ID'] = str(app.id)
    application_params['LOAN-AMOUNT'] = app.applied_loan

    validate_address_params(address_params)
    validate_application_params(application_params)

    return applicant_params, address_params, application_params

def get_highmark_response_applications(applications):

    responses_list = []
    for app in applications:
        applicant_params, address_params, application_params= get_query_params_from_app(app)
        response = handle_request_response(applicant_params, address_params, application_params)
        mainapp.logger.debug("highmark response appid:%s  response:%s" % (app.application_id, response.content[:1500]))

        if response.status_code == 200 and ET.fromstring(response.content).find("./INDV-REPORTS") is not None:
            response_p = ET.fromstring(response.content)
            app.highmark_response = response.content
            app.update_status(140)
            app.save()
            mainapp.logger.debug("[HIGHMARK] application verification successful appid:%s status:%s" % (app.application_id, app.status))

        elif response.status_code != 200:
            app.update_status(130)
            app.save()
            mainapp.logger.debug("[HIGHMARK] application verification failed appid:%s response-status:%s" % (app.application_id, response.status_code))

        else:
            mainapp.logger.debug("[HIGHMARK] application verification failed appid:%s response-status:%s" % (app.application_id, response.status_code))

        responses_list.append(response)

    return responses_list


def handle_request_response(applicant_params, address_params, application_params):

    resp = send_request(applicant_params, address_params, application_params)

    return resp