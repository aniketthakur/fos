import time
import unittest
import generate_xml_query
import generate_second_xml_query
import xml.etree.ElementTree as ET
from esthenos import settings
import highmark_request as hmr
from esthenos import settings

def generate_sample_query():

	application_params = {}
	address_params = {}
	applicant_params = {}
	applicant_name_headers = ['applicant_name_1', 'applicant_name_2', 'applicant_name_3', 'applicant_name_4', \
	                          'applicant_name_5']
	applicant_name = "BISAMILLA KHAJESAB BADEGHAR".split(" ")

	for i in range(len(applicant_name), 5):
		applicant_name.append("")

	for i, j in zip(applicant_name_headers, applicant_name):
		applicant_params[i] = j

	applicant_id_headers = ['ID01', 'ID02', 'ID03', 'ID04', 'ID05', 'ID06', 'ID07']
	applicant_id_headers_values = ['IYP1358100', '', '']

	applicant_params["IDS"] = {}
	i = 0

	for j in applicant_id_headers_values:
		if j:
			applicant_params["IDS"][applicant_id_headers[i]] = j
			i += 1

	applicant_params['REL'] = {}

	applicant_params['applicant_age_as_on'] = "29/07/2015"
	applicant_params['applicant_dob'] = ''
	applicant_params['applicant_age'] = '34'
	applicant_params['applicant_phone_type_1'] = "P01"
	applicant_params['applicant_phone_1'] = '123456'
	applicant_params['applicant_phone_type_2'] = "P02"
	applicant_params['applicant_phone_2'] = '4355456789'

	address_params = {}
	address_params['address_type_1'] = "D01"
	address_params['type_1_address'] = '666/2.ASANGI H NO 623 RIND 713 JAMAKHANDI RABAKAVI KA KOLKATTA'
	address_params['type_1_city'] = "24 PARGANAS"
	address_params['type_1_state'] = 'West Bengal'
	address_params['type_1_pincode'] = '743290'

	application_params = {}
	application_params['INQUIRY-UNIQUE-REF-NO'] = '03441cvxv3443vv'
	application_params['CREDT-INQ-PURPS-TYP'] = 'ACCT-ORIG'
	application_params['CREDT-INQ-PURPS-TYP-DESC'] = 'ACCT-ORIG'
	application_params['CREDT-RPT-ID'] = '006f000026EGk7JJFS'
	application_params['CREDT-REQ-TYP'] = 'INDV'
	application_params['CREDT-RPT-TRN-DT-TM'] = time.strftime("%d-%m-%Y %H:%M:%S")
	application_params['KENDRA-ID'] = 'House'
	application_params['BRANCH-ID'] = '3008'
	application_params['LOS-APP-ID'] = 'a0Yf0000003fL7xEAE12345'
	application_params['LOAN-AMOUNT'] = '20000'

	query = generate_xml_query.create_xml_query_1(applicant_params, address_params, application_params)

	return query

class XMLQueryTest(unittest.TestCase):

	def setUp(self):
		pass

	@classmethod
	def setUpClass(self):
		self.query_1 = generate_sample_query()
		self.request_1_header = hmr.get_query_header(self.query_1)
		self.ack = hmr.get_acknowledgement(self.request_1_header)
		self.ack_params = hmr.get_params_from_ack(ET.fromstring(self.ack.content))
		self.query_2 = generate_second_xml_query.create_second_xml_query(self.ack_params[0], self.ack_params[1], self.ack_params[2])
		self.request_2_header = hmr.get_query_header(self.query_2)
		self.query_2_response = hmr.get_response(self.request_2_header)
		self.query_1_up = self.query_1
		self.query_1 = ET.fromstring(self.query_1)
		self.query_2 = ET.fromstring(self.query_2)


	#Inquiry Header
	def test_occur_header_segment(self):
		self.assertNotEquals(str(self.query_1.find(".//HEADER-SEGMENT")), 'None')
		self.assertEqual(len(self.query_1.findall(".//HEADER-SEGMENT")), 1)


	def test_occur_sub_mbr_id(self):
		self.assertNotEquals(str(self.query_1.find(".//SUB-MBR-ID")), 'None')
		self.assertEqual(len(self.query_1.findall(".//SUB-MBR-ID")), 1)

	def test_occur_inq_dt_tm(self):
		self.assertNotEquals(str(self.query_1.find(".//INQ-DT-TM")), 'None')
		self.assertEqual(len(self.query_1.findall(".//INQ-DT-TM")), 1)

	def test_occur_req_actn_typ(self):
		self.assertNotEquals(str(self.query_1.find(".//REQ-ACTN-TYP")), 'None')
		self.assertEqual(len(self.query_1.findall(".//REQ-ACTN-TYP")), 1)

	def test_occur_test_flg(self):
		self.assertNotEquals(str(self.query_1.find(".//TEST-FLG")), 'None')
		self.assertEqual(len(self.query_1.findall(".//TEST-FLG")), 1)
		self.assertEqual(self.query_1.find(".//TEST-FLG").text, 'N')

	def test_occur_auth_flg(self):
		self.assertNotEquals(str(self.query_1.find(".//AUTH-FLG")), 'None')
		self.assertEqual(len(self.query_1.findall(".//AUTH-FLG")), 1)


	def test_occur_res_frmt(self):
		self.assertNotEquals(str(self.query_1.find(".//RES-FRMT")), 'None')
		self.assertEqual(len(self.query_1.findall(".//RES-FRMT")), 1)


	def test_occur_member_pre_override(self):
		self.assertNotEquals(self.query_1.find(".//MEMBER-PRE-OVERRIDE"), 'None')
		self.assertEqual(len(self.query_1.findall(".//MEMBER-PRE-OVERRIDE")), 1)


	def test_occur_res_frmt_embd(self):
		self.assertNotEquals(self.query_1.find(".//RES-FRMT-EMBD"), 'None')
		self.assertEqual(len(self.query_1.findall(".//RES-FRMT-EMBD")), 1)
		self.assertEquals(self.query_1.find("./HEADER-SEGMENT/RES-FRMT").text.lower(), "XML/HTML".lower())


	def test_occur_los_version(self):
		self.assertNotEquals(self.query_1.find(".//LOS-VERSION"), 'None')
		self.assertEqual(len(self.query_1.findall(".//LOS-VERSION")), 1)
		self.assertEqual(str(self.query_1.find(".//LOS-VERSION").text), settings.ORGS_SETTINGS["los-version"])


	def test_occur_los_name(self):
		self.assertNotEquals(self.query_1.find(".//LOS-NAME"), 'None')
		self.assertEqual(len(self.query_1.findall(".//LOS-NAME")), 1)
		self.assertEqual(self.query_1.find(".//LOS-NAME").text.lower(), settings.ORGS_SETTINGS["los-name"].lower())


	def test_occur_los_vendor(self):
		self.assertEqual(len(self.query_1.findall(".//LOS-VENDER")), 1)
		self.assertEqual(self.query_1.find(".//LOS-VENDER").text.lower(), settings.ORGS_SETTINGS["los-vendor"].lower())


	#Inquiry Header
	def test_occur_inquiry(self):
		self.assertNotEquals(self.query_1.find(".//INQUIRY"), 'None')
		self.assertEqual(len(self.query_1.findall(".//INQUIRY")), 1)


	#Inquiry Applicant
	def test_occur_applicant_segment(self):
		self.assertNotEquals(len(self.query_1.findall(".//APPLICANT-SEGMENT")), 0)
		self.assertEqual(len(self.query_1.findall(".//APPLICANT-SEGMENT")), 1)


	def test_occur_applicant_segment_name(self):
		self.assertNotEquals(self.query_1.find(".//APPLICANT-SEGMENT/APPLICANT-NAME"), 'None')
		self.assertEqual(len(self.query_1.findall(".//APPLICANT-SEGMENT/APPLICANT-NAME")), 1)


	def test_occur_applicant_segment_dob(self):
		self.assertNotEquals(self.query_1.find(".//APPLICANT-SEGMENT/DOB"), 'None')
		self.assertEqual(len(self.query_1.findall(".//APPLICANT-SEGMENT/DOB")), 1)
		self.assertTrue(len(self.query_1.findall(".//APPLICANT-SEGMENT/DOB/DOB-DATE")) < 2)
		self.assertTrue(len(self.query_1.findall(".//APPLICANT-SEGMENT/DOB/AGE")) < 2)
		self.assertTrue(len(self.query_1.findall(".//APPLICANT-SEGMENT/DOB/AGE-AS-ON")) < 2)


	def test_occur_applicant_segment_id(self):
		self.assertNotEquals(self.query_1.find(".//APPLICANT-SEGMENT/IDS"), 'None')
		self.assertEqual(len(self.query_1.findall(".//APPLICANT-SEGMENT/IDS")), 1)
		self.assertTrue(len(self.query_1.findall(".//APPLICANT-SEGMENT/IDS/ID")) > 0)
		id_types = ['ID01', 'ID02', 'ID03', 'ID04', 'ID05', 'ID06', 'ID07']
		for i in self.query_1.findall(".//APPLICANT-SEGMENT/IDS/ID"):
			self.assertEqual(len(i.findall("./TYPE")), 1)
			self.assertEqual(len(i.findall("./VALUE")), 1)
			self.assertTrue(i.find('./TYPE').text in id_types)


	def test_occur_applicant_segment_relation(self):
		self.assertTrue(len(self.query_1.findall(".//APPLICANT-SEGMENT/RELATIONS")) < 2)
		if len(self.query_1.findall(".//APPLICANT-SEGMENT/RELATIONS")) == 1:
			self.assertTrue(len(self.query_1.findall(".//APPLICANT-SEGMENT/RELATIONS/RELATION")) > 0)
			for i in self.query_1.findall(".//APPLICANT-SEGMENT/RELATIONS/RELATION"):
				self.assertTrue(len(i.findall("./NAME")), 1)
				self.assertTrue(len(i.findall("./TYPE")), 1)


	def test_occur_applicant_segment_key_person(self):
		kp = self.query_1.findall(".//APPLICANT-SEGMENT/KEYPERSON")
		self.assertTrue(len(kp) < 2)
		if len(kp) == 1:
			self.assertEqual(len(kp.findall("./NAME")), 1)
			self.assertEqual(len(kp.findall("./TYPE")), 1)


	def test_occur_applicant_segment_nominee(self):
		ne = self.query_1.findall(".//APPLICANT-SEGMENT/NOMINEE")
		self.assertTrue(len(ne) < 2)
		if len(ne) == 1:
			self.assertEqual(len(ne[0].findall("./NAME")), 1)
			self.assertEqual(len(ne[0].findall("./TYPE")), 1)


	#Inquiry Address
	def test_occur_address_segment(self):
		self.assertNotEquals(self.query_1.find("./INQUIRY/ADDRESS-SEGMENT"), 'None')
		self.assertEqual(len(self.query_1.findall("./INQUIRY/ADDRESS-SEGMENT")), 1)


	def test_occur_address_segment_address(self):
		address = self.query_1.findall("./INQUIRY/ADDRESS-SEGMENT/ADDRESS")
		self.assertTrue(len(address) > 0)
		address_type = ['D01', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07', 'D08']
		for i in address:
			self.assertEqual(len(i.findall('./TYPE')), 1)
			self.assertTrue(i.find('./TYPE').text in address_type)
			self.assertEqual(len(i.findall('./ADDRESS-1')), 1)
			self.assertEqual(len(i.findall('./CITY')), 1)
			self.assertEqual(len(i.findall('./STATE')), 1)
			self.assertEqual(len(i.find('./STATE').text), 2)


	#Inquiry Application
	def test_occur_application_segment(self):
		self.assertNotEquals(self.query_1.find(".//APPLICATION-SEGMENT"), 'None')
		self.assertEqual(len(self.query_1.findall(".//APPLICATION-SEGMENT")), 1)


	def test_occur_application_segment_inquiry_ref_no(self):
		self.assertEqual(len(self.query_1.findall(".//APPLICATION-SEGMENT/INQUIRY-UNIQUE-REF-NO")), 1)


	def test_occur_application_segment_credit_inq_purps_typ(self):
		self.assertEqual(len(self.query_1.findall(".//APPLICATION-SEGMENT/CREDT-INQ-PURPS-TYP")), 1)


	def test_occur_application_segment_credit_inquiry_stage(self):
		self.assertEqual(len(self.query_1.findall(".//APPLICATION-SEGMENT/CREDIT-INQUIRY-STAGE")), 1)


	def test_occur_application_segment_credit_rept_id(self):
		self.assertIn(len(self.query_1.findall(".//APPLICATION-SEGMENT/CREDT-RPT-ID")), [0,1])


	def test_occur_application_segment_credit_req_typ(self):
		self.assertEqual(len(self.query_1.findall(".//APPLICATION-SEGMENT/CREDT-REQ-TYP")), 1)


	def test_occur_application_segment_credit_rpt_trn_dt_tm(self):
		self.assertEqual(len(self.query_1.findall(".//APPLICATION-SEGMENT/CREDT-RPT-TRN-DT-TM")), 1)


	def test_occur_application_segment_mbr_id(self):
		self.assertEqual(len(self.query_1.findall(".//APPLICATION-SEGMENT/MBR-ID")), 1)

	def test_occur_application_segment_kendra_id(self):
		self.assertEqual(len(self.query_1.findall(".//APPLICATION-SEGMENT/KENDRA-ID")), 1)

	def test_occur_application_segment_branch_id(self):
		self.assertEqual(len(self.query_1.findall(".//APPLICATION-SEGMENT/BRANCH-ID")), 1)

	def test_occur_application_segment_kendra_id(self):
		self.assertEqual(len(self.query_1.findall(".//APPLICATION-SEGMENT/LOS-APP-ID")), 1)

	def test_occur_application_segment_loan_amount(self):
		self.assertTrue(len(self.query_1.find(".//APPLICATION-SEGMENT/LOAN-AMOUNT")) < 2)

	def test_request_1_header_req_vol_type(self):
		self.assertTrue('reqVolType' in self.request_1_header.keys())
		self.assertEquals(self.request_1_header['reqVolType'], 'INDV')

	def test_request_1_header_userid(self):
		self.assertTrue('userid' in self.request_1_header.keys())
		self.assertEquals(self.request_1_header['userid'], settings.ORGS_SETTINGS['highmark-uname'])

	def test_request_1_header_password(self):
		self.assertTrue('password' in self.request_1_header.keys())
		self.assertEquals(self.request_1_header['password'], settings.ORGS_SETTINGS['highmark-password'])

	def test_request_1_header_req_vol_type(self):
		self.assertTrue('reqVolType' in self.request_1_header.keys())
		self.assertEquals(self.request_1_header['reqVolType'], 'INDV')

	def test_request_1_header_product_type(self):
		self.assertTrue('productType' in self.request_1_header.keys())
		self.assertEquals(self.request_1_header['productType'], 'INDV')

	def test_request_1_header_product_version(self):
		self.assertTrue('productType' in self.request_1_header.keys())
		self.assertEquals(self.request_1_header['productVersion'], '1.0')

	def test_request_1_header_mbrid(self):
		self.assertTrue('mbrid' in self.request_1_header.keys())
		self.assertEquals(self.request_1_header['mbrid'], settings.ORGS_SETTINGS['esthenos-client-mbrid'])

	def test_request_1_header_req_xml(self):
		self.assertTrue('requestXml' in self.request_1_header.keys())
		self.assertEquals(self.request_1_header['requestXml'], self.query_1_up)

	#ACKNOWLEDGEMENT
	# def test_acknowledgement(self):
	# 	self.ack.content

	#Second Query
	def test_second_query_req_actn_typ(self):
		self.assertTrue(len(self.query_2.findall(".//REQ-ACTN-TYP")) == 1)
		self.assertEquals(self.query_2.find(".//REQ-ACTN-TYP").text.lower(), "ISSUE".lower())

	def test_second_query_inquiry_segment(self):
		self.assertTrue(len(self.query_2.findall("./INQUIRY")) == 1)

	def test_second_query_inquiry_segment_ref_no(self):
		self.assertTrue(len(self.query_2.findall("./INQUIRY/INQUIRY-UNIQUE-REF-NO")) == 1)

	def test_second_query_inquiry_segment_report_id(self):
		self.assertTrue(len(self.query_2.findall("./INQUIRY/REPORT-ID")) == 1)

	def test_second_query_header_req_actn_typ(self):
		self.assertTrue(len(self.query_2.findall(".//REQ-ACTN-TYP")) == 1)
		self.assertEquals(self.query_2.find(".//REQ-ACTN-TYP").text.lower(), "ISSUE".lower())

	def test_second_query_header_res_frmt(self):
		self.assertTrue(len(self.query_2.findall("./HEADER-SEGMENT/RES-FRMT")) == 1)
		self.assertEquals(self.query_2.find("./HEADER-SEGMENT/RES-FRMT").text.lower(), "XML/HTML".lower())

	def test_second_query_header_mfi(self):
		self.assertTrue(len(self.query_2.findall("./HEADER-SEGMENT/MFI")) == 1)

	def test_second_query_header_mfi_indv(self):
		self.assertTrue(len(self.query_2.findall("./HEADER-SEGMENT/MFI/INDV")) == 1)
		self.assertEquals(self.query_2.find("./HEADER-SEGMENT/MFI/INDV").text.lower(), "true")

	def test_second_query_header_mfi_score(self):
		self.assertTrue(len(self.query_2.findall("./HEADER-SEGMENT/MFI/SCORE")) == 1)
		self.assertEquals(self.query_2.find("./HEADER-SEGMENT/MFI/SCORE").text.lower(), "true")

	def test_second_query_header_mfi_group(self):
		self.assertTrue(len(self.query_2.findall("./HEADER-SEGMENT/MFI/GROUP")) == 1)
		self.assertEquals(self.query_2.find("./HEADER-SEGMENT/MFI/GROUP").text.lower(), "true")

	def test_second_query_header_consumer(self):
		self.assertTrue(len(self.query_2.findall("./HEADER-SEGMENT/CONSUMER")) == 1)


	def test_second_query_header_consumer_indv(self):
		self.assertTrue(len(self.query_2.findall("./HEADER-SEGMENT/CONSUMER/INDV")) == 1)
		self.assertEquals(self.query_2.find("./HEADER-SEGMENT/CONSUMER/INDV").text.lower(), "true")

	def test_second_query_header_consumer_score(self):
		self.assertTrue(len(self.query_2.findall("./HEADER-SEGMENT/MFI/SCORE")) == 1)
		self.assertEquals(self.query_2.find("./HEADER-SEGMENT/MFI/SCORE").text.lower(), "true")

	def test_second_query_header_ioi(self):
		self.assertTrue(len(self.query_2.findall("./HEADER-SEGMENT/IOI")) == 1)
		self.assertEquals(self.query_2.find("./HEADER-SEGMENT/IOI").text.lower(), "true")

	def test_second_query_header_product_type(self):
		self.assertNotEquals(str(self.query_2.find("./HEADER-SEGMENT/PRODUCT-TYP")), 'None')
		self.assertEqual(len(self.query_2.findall("./HEADER-SEGMENT/PRODUCT-TYP")), 1)
		self.assertEquals(self.query_2.find("./HEADER-SEGMENT/PRODUCT-TYP").text, 'INDV')

	def test_second_query_header_product_ver(self):
		self.assertNotEquals(str(self.query_2.find("./HEADER-SEGMENT/PRODUCT-VER")), 'None')
		self.assertEqual(len(self.query_2.findall("./HEADER-SEGMENT/PRODUCT-VER")), 1)
		self.assertEquals(self.query_2.find("./HEADER-SEGMENT/PRODUCT-VER").text, '1.0')

	def test_second_query_header_req_mbr(self):
		self.assertNotEquals(str(self.query_2.find("./HEADER-SEGMENT/REQ-MBR")), 'None')
		self.assertEqual(len(self.query_2.findall("./HEADER-SEGMENT/REQ-MBR")), 1)
		self.assertEquals(self.query_2.find("./HEADER-SEGMENT/REQ-MBR").text, settings.ORGS_SETTINGS['esthenos-client-mbrid'])

	def test_second_query_header_submbr_id(self):
		self.assertNotEquals(str(self.query_2.find("./HEADER-SEGMENT/SUB-MBR-ID")), 'None')
		self.assertEqual(len(self.query_2.findall("./HEADER-SEGMENT/SUB-MBR-ID")), 1)
		self.assertEquals(self.query_2.find("./HEADER-SEGMENT/SUB-MBR-ID").text, settings.ORGS_SETTINGS['esthenos-client'])

	def test_second_query_header_test_flg(self):
		self.assertNotEquals(str(self.query_1.find("./HEADER-SEGMENT/TEST-FLG")), 'None')
		self.assertEqual(len(self.query_1.findall("./HEADER-SEGMENT/TEST-FLG")), 1)
		self.assertEqual(self.query_1.find("./HEADER-SEGMENT/TEST-FLG").text, 'N')

	def test_second_query_header_auth_flg(self):
		self.assertNotEquals(str(self.query_1.find("./HEADER-SEGMENT/AUTH-FLG")), 'None')
		self.assertEqual(len(self.query_1.findall("./HEADER-SEGMENT/AUTH-FLG")), 1)
		self.assertEqual(self.query_1.find("./HEADER-SEGMENT/AUTH-FLG").text, 'Y')

	def test_second_query_header_auth_title(self):
		self.assertNotEquals(str(self.query_1.find("./HEADER-SEGMENT/AUTH-TITLE")), 'None')
		self.assertEqual(len(self.query_1.findall("./HEADER-SEGMENT/AUTH-TITLE")), 1)
		self.assertEqual(self.query_1.find("./HEADER-SEGMENT/AUTH-TITLE").text, 'USER')

if __name__== "__main__":
	unittest.main()
