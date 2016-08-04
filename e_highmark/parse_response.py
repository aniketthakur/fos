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
    # application_params['LOAN-AMOUNT'] = app.applied_loan

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

def get_valules_from_highmark_response(response):

    loan_bal = 0
    loan_dpd = 0
    indv_resp_list = []
    acct_type_excluded = settings.ORGS_SETTINGS["acct-types-exclude"]
    acct_type_excluded = [x.lower() for x in acct_type_excluded]

    mfi_excluded = settings.ORGS_SETTINGS["mfi-exclude"]
    mfi_excluded = [x.lower() for x in mfi_excluded]

    for i in response.findall(".//INDV-RESPONSE"):
        indv_resp = HighMarkIndvResponse()
        print "1." , i
        indv_resp.mfi_name = i.find(".//MFI").text if i.find(".//MFI") else ''
        indv_resp.mfi_name = i.find(".//MFI").text
        indv_resp.mfi_id = i.find(".//MFI-ID").text if i.find(".//MFI-ID") else ''
        indv_resp.branch = i.find(".//BRANCH").text if i.find(".//LOAN-CYCLE-ID") else ''
        indv_resp.kendra = i.find(".//KENDRA").text if i.find(".//LOAN-CYCLE-ID") else ''
        indv_resp.cns_mr_mbrid = i.find(".//CNSMRMBRID").text if i.find(".//CNSMRMBRID") else ''
        indv_resp.matched_type = i.find(".//MATCHED-TYPE").text if i.find(".//MATCHED-TYPE") else ''
        indv_resp.report_date = i.find(".//reportDt").text if i.find(".//reportDt") else ''
        indv_resp.insert_date = i.find(".//INSERT-DATE").text
        indv_resp.loan_account_type = i.find(".//ACCT-TYPE").text
        indv_resp.loan_frequency = i.find(".//FREQ").text
        indv_resp.loan_status = i.find(".//STATUS").text
        indv_resp.loan_account_number = i.find(".//ACCT-NUMBER").text
        indv_resp.loan_disbursement_amt = int(i.find(".//DISBURSED-AMT").text)
        indv_resp.loan_balance = int(i.find(".//CURRENT-BAL").text)
        indv_resp.loan_installment = int(i.find(".//INSTALLMENT-AMT").text) if i.find(".//INSTALLMENT-AMT") else 0
        indv_resp.loan_overdue = int(i.find(".//OVERDUE-AMT").text) if i.find(".//OVERDUE-AMT") else 0
        indv_resp.loan_dpd = int(i.find(".//DPD").text)
        indv_resp.loan_disbursed_date = i.find(".//DISBURSED-DT").text
        indv_resp.closed_date = i.find(".//CLOSED-DT").text if i.find(".//CLOSED-DT") else ''
        indv_resp.loan_cycle_id = i.find(".//LOAN-CYCLE-ID").text
        indv_resp.loan_info_as_on = i.find(".//INFO-AS-ON").text
        indv_resp.loan_history = i.find(".//COMBINED-PAYMENT-HISTORY").text if i.find(".//COMBINED-PAYMENT-HISTORY") else ''
        indv_resp.dpd_30 = int(i.find(".//TOT-DPD-30").text)
        indv_resp.dpd_60 = int(i.find(".//TOT-DPD-60").text)
        indv_resp.dpd_90 = int(i.find(".//TOT-DPD-90").text)
        loan_bal = loan_bal+indv_resp.loan_balance
        loan_dpd = loan_dpd+indv_resp.dpd_60+indv_resp.dpd_90
        if i.find(".//ACCT-TYPE") and i.find(".//ACCT-TYPE").text.lower() not in acct_type_excluded and \
                i.find(".//STATUS") and i.find(".//STATUS").text.strip().lower() == "active":
            indv_resp.is_prohibited = True

            indv_resp.save()
            indv_resp_list.append(indv_resp)

    return [indv_resp_list, loan_bal, loan_dpd]

def get_sum_overdue_amount(response):

    amount = 0
    for indv in response.findall("./INDV-RESPONSES/INDV-RESPONSE-LIST/INDV-RESPONSE"):
        if (int(indv.find("./GROUP-DETAILS/TOT-DPD-60").text) > 0 or int(indv.find("./GROUP-DETAILS/TOT-DPD-90").text) > 0) \
                and indv.find("./LOAN-DETAIL/STATUS").text.lower() == "active":
            amount += int(indv.find("./LOAN-DETAILS/OVERDUE-AMOUNT").text)

    return amount


def get_kendra_id(response):
    return 0


def get_national_id_card(response):

    if response.find(".//INDV-REPORT/REQUEST/IDS") is not None and response.findall(".//INDV-REPORT/REQUEST/IDS/ID"):
        for i in response.findall(".//INDV-REPORT/REQUEST/IDS/ID"):
            if i.find(".//TYPE").text == 'ID02':
                return i.find(".//VALUE").text
            elif i.find(".//TYPE").text == 'ID03':
                return i.find(".//VALUE").text

        return response.find(".//INDV-REPORT/REQUEST/IDS/ID/VALUE").text
    else:
        return "000000000"


def get_num_active_account(response):

    diff_mfis = Counter()

    for indv in response.findall(".//INDV-RESPONSE"):
        if indv.find(".//LOAN-DETAIL/STATUS").text.lower() == "active":
            diff_mfis[indv.find("./MFI").text.lower().strip()] += 1

    return len(diff_mfis)
