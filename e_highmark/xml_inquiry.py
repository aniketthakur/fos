from lxml import etree
import random
import hashlib
from esthenos import settings
import time
from esthenos import mainapp

def get_code_from_state_name(state):

    state_code_dict = { 'Andhra Pradesh': 'AP', 'Arunachal Pradesh': 'AR', 'Assam': 'AS', 'Bihar': 'BR', 'Chhattisgarh': 'CG', 'Goa': 'GA', 'Gujarat': 'GJ', 'Haryana': 'HR',\
      'Himachal Pradesh': 'HP', 'Jammu and Kashmir': 'JK', 'Jharkhand': 'JH', 'Karnataka': 'KA', 'Kerala': 'KL', 'Madhya Pradesh': 'MP', 'Maharashtra': 'MH',\
      'Manipur': 'MN', 'Meghalaya': 'ML', 'Mizoram': 'MZ', 'Nagaland': 'NL', 'Orissa': 'OR', 'Punjab': 'PB', 'Rajasthan': 'RJ', 'Sikkim': 'SK', 'Tamil Nadu': 'TN', \
      'Tripura': 'TR', 'Telangana': 'TG', 'Uttarakhand': 'UK', 'Uttar Pradesh': 'UP', 'West Bengal': 'WB', 'Tamil Nadu': 'TN', 'Tripura': 'TR', 'Andaman and Nicobar Islands': 'AN',\
      'Chandigarh': 'CH', 'Dadra and Nagar Haveli': 'DH', 'Daman and Diu': 'DD', 'Delhi': 'DL', 'Lakshadweep': 'LD', 'Pondicherry': 'PY'}

    state = ' '.join(filter((lambda x: len(x) > 0), state.strip().split(' ')))

    try:
        code = state_code_dict[state]
    except KeyError:
        code = 'WB'

    return code


def add_applicant_dob(root, p1, p2, p3):

    etree.SubElement(root, 'AGE').text = str(p3)



def add_applicant_id(root, applicant_ids):
    for i in applicant_ids:
        id_r = etree.SubElement(root, 'ID')
        etree.SubElement(id_r, 'TYPE').text = str(i)
        etree.SubElement(id_r, 'VALUE').text = str(applicant_ids[i])


def add_applicant_phone(root, p1, p2):

    phone = etree.SubElement(root, 'PHONE')
    etree.SubElement(phone, 'TELE-NO').text = str(p1)
    etree.SubElement(phone, 'TELE-NO-TYPE').text = str(p2)


def add_applicant_nominee(root):

    etree.SubElement(root, 'NAME').text = ""
    etree.SubElement(root, 'TYPE').text = ""


def add_applicant_key_person(root):

    etree.SubElement(root, 'NAME').text = ""
    etree.SubElement(root, 'TYPE').text = ""


def add_applicant_relation(root, applicant_relations):
    if applicant_relations:
        for i in applicant_relations:
            r = etree.SubElement(root, 'RELATION')
            etree.SubElement(r, 'NAME').text = applicant_relations[i]
            etree.SubElement(r, 'TYPE').text = i


def add_applicant(root, applicant_params):

    name = etree.SubElement(root, 'APPLICANT-NAME')
    etree.SubElement(name, 'NAME1').text = applicant_params['applicant_name_1']
    etree.SubElement(name, 'NAME2').text = applicant_params['applicant_name_2']
    etree.SubElement(name, 'NAME3').text = applicant_params['applicant_name_3']
    etree.SubElement(name, 'NAME4').text = applicant_params['applicant_name_4']
    etree.SubElement(name, 'NAME5').text = applicant_params['applicant_name_5']

    dob = etree.SubElement(root, 'DOB')
    add_applicant_dob(dob, applicant_params['applicant_age_as_on'], applicant_params['applicant_dob'],\
                      applicant_params['applicant_age'])

    ids = etree.SubElement(root, 'IDS')
    add_applicant_id(ids, applicant_params["IDS"])


def add_address(root, address_params):

    address = etree.SubElement(root, 'ADDRESS')

    etree.SubElement(address, 'TYPE').text = address_params['address_type_1']
    etree.SubElement(address, 'ADDRESS-1').text = address_params['type_1_address']
    etree.SubElement(address, 'CITY').text = address_params['type_1_city']
    etree.SubElement(address, 'STATE').text = get_code_from_state_name(address_params['type_1_state'])
    etree.SubElement(address, 'PIN').text = address_params['type_1_pincode']


def add_application(root, application_params):

    st = ''.join([str(application_params[x]) for x in application_params])
    etree.SubElement(root, 'INQUIRY-UNIQUE-REF-NO').text=hashlib.sha224(st).hexdigest()[0:15]+\
                                                         hashlib.sha224(str(random.randrange(0,10**9))).hexdigest()[:10]
    etree.SubElement(root, 'CREDT-INQ-PURPS-TYP-DESC').text="ACCT-ORIG"
    etree.SubElement(root, 'CREDT-INQ-PURPS-TYP').text="ACCT-ORIG"
    etree.SubElement(root, 'CREDIT-INQUIRY-STAGE').text="PRE-DISB"
    etree.SubElement(root, 'CREDT-REQ-TYP').text="INDV"
    etree.SubElement(root, 'CREDT-RPT-TRN-DT-TM').text=time.strftime("%d-%m-%Y %H:%M:%S")
    etree.SubElement(root, 'MBR-ID').text=settings.ORGS_SETTINGS["esthenos-client-mbrid"]
    etree.SubElement(root, 'BRANCH-ID').text = application_params['BRANCH-ID']
    etree.SubElement(root, 'LOS-APP-ID').text = application_params['LOS-APP-ID']
    etree.SubElement(root, 'LOAN-AMOUNT').text= str(application_params['LOAN-AMOUNT'])


def add_inquiry(root, applicant_params, address_params, application_params):

    applicant_header = etree.SubElement(root, 'APPLICANT-SEGMENT')
    add_applicant(applicant_header, applicant_params)
    address_header = etree.SubElement(root, 'ADDRESS-SEGMENT')
    add_address(address_header, address_params)
    application_header = etree.SubElement(root, 'APPLICATION-SEGMENT')
    add_application(application_header, application_params)