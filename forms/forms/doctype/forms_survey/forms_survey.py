import frappe
from frappe.model.document import Document


class FormsSurvey(Document):
	def before_insert(self):
		if not self.survey_code:
			self.survey_code = frappe.generate_hash(length=10).upper()

	def before_save(self):
		if not self.survey_code:
			self.survey_code = frappe.generate_hash(length=10).upper()
