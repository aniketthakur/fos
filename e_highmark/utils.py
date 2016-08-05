from esthenos import mainapp
import xml.etree.ElementTree as ET
from e_organisation.models import *
import esthenos


def get_loan_bal_dpd_from_highmark_response(response):

	s2 = ""
	bal = 0
	dpd = 0

	if response:
		root = ET.fromstring(response)

		for i in root.findall(".//INDV-RESPONSE"):
			if i.find(".//LOAN-DETAIL/ACCT-TYPE").text.lower() not in esthenos.settings.ORGS_SETTINGS["acct-types-exclude"] and \
							i.find(".//LOAN-DETAIL/STATUS").text.lower() == "active":
				s2 = s2 + "\n" + str(i.find(".//MFI").text) + "/" + str(i.find(".//INFO-AS-ON").text) + "/" + str(i.find(".//CURRENT-BAL").text) + "/" + str(str(i.find(".//OVERDUE-AMT").text)) + "/" +str(int(i.find(".//TOT-DPD-60").text)+int(i.find(".//TOT-DPD-90").text))
				bal = bal+int(i.find(".//CURRENT-BAL").text)
				dpd = dpd+int(i.find(".//TOT-DPD-60").text)+int(i.find(".//TOT-DPD-90").text)

	s2 = s2.strip()
	return s2, bal, dpd