import json

import frappe


def after_install() -> None:
	_create_roles()
	_create_templates()
	frappe.db.commit()


def _create_roles() -> None:
	for role in ["Survey Manager", "Survey Designer", "Survey Analyst", "Survey User"]:
		if not frappe.db.exists("Role", role):
			frappe.get_doc({"doctype": "Role", "role_name": role, "desk_access": 1}).insert()


def _create_templates() -> None:
	templates = [
		{
			"template_name": "Customer Satisfaction",
			"category": "Customer Satisfaction",
			"is_system_template": 1,
			"description": "Measure customer satisfaction with your product or service.",
			"survey_data": json.dumps(
				{
					"description": "We value your feedback. This will only take 2 minutes.",
					"questions": [
						{
							"id": "q1",
							"question": "How satisfied are you with our product?",
							"question_type": "Rating",
							"required": True,
							"options": [],
							"page_number": 1,
						},
						{
							"id": "q2",
							"question": "How likely are you to recommend us to a friend or colleague?",
							"question_type": "Net Promoter Score",
							"required": True,
							"options": [],
							"page_number": 1,
						},
						{
							"id": "q3",
							"question": "What do you like most about our product?",
							"question_type": "Long Answer",
							"required": False,
							"options": [],
							"page_number": 2,
						},
						{
							"id": "q4",
							"question": "What can we improve?",
							"question_type": "Long Answer",
							"required": False,
							"options": [],
							"page_number": 2,
						},
						{
							"id": "q5",
							"question": "Overall experience",
							"question_type": "Star Rating",
							"required": True,
							"options": [],
							"page_number": 2,
						},
					],
				}
			),
		},
		{
			"template_name": "Employee Feedback",
			"category": "Employee Feedback",
			"is_system_template": 1,
			"description": "Gather anonymous employee feedback to improve culture.",
			"survey_data": json.dumps(
				{
					"description": "Your response is anonymous and confidential.",
					"questions": [
						{
							"id": "q1",
							"question": "How satisfied are you with your current role?",
							"question_type": "Rating",
							"required": True,
							"options": [],
							"page_number": 1,
						},
						{
							"id": "q2",
							"question": "Do you feel your work is valued?",
							"question_type": "Yes/No",
							"required": True,
							"options": [],
							"page_number": 1,
						},
						{
							"id": "q3",
							"question": "How would you rate team collaboration?",
							"question_type": "Star Rating",
							"required": True,
							"options": [],
							"page_number": 1,
						},
						{
							"id": "q4",
							"question": "What challenges are you facing?",
							"question_type": "Long Answer",
							"required": False,
							"options": [],
							"page_number": 2,
						},
						{
							"id": "q5",
							"question": "How likely are you to recommend this company as a great place to work?",
							"question_type": "Net Promoter Score",
							"required": True,
							"options": [],
							"page_number": 2,
						},
					],
				}
			),
		},
		{
			"template_name": "Exit Interview",
			"category": "Exit Interview",
			"is_system_template": 1,
			"description": "Understand why employees leave.",
			"survey_data": json.dumps(
				{
					"description": "Thank you for your time with us. Your feedback helps us improve.",
					"questions": [
						{
							"id": "q1",
							"question": "Primary reason for leaving",
							"question_type": "Multiple Choice",
							"required": True,
							"options": [
								"Better opportunity",
								"Relocation",
								"Personal reasons",
								"Compensation",
								"Work environment",
								"Career growth",
								"Other",
							],
							"page_number": 1,
						},
						{
							"id": "q2",
							"question": "How satisfied were you with your role overall?",
							"question_type": "Rating",
							"required": True,
							"options": [],
							"page_number": 1,
						},
						{
							"id": "q3",
							"question": "How was your relationship with your manager?",
							"question_type": "Rating",
							"required": True,
							"options": [],
							"page_number": 2,
						},
						{
							"id": "q4",
							"question": "What did you enjoy most about working here?",
							"question_type": "Long Answer",
							"required": False,
							"options": [],
							"page_number": 2,
						},
						{
							"id": "q5",
							"question": "Would you consider returning in the future?",
							"question_type": "Yes/No",
							"required": False,
							"options": [],
							"page_number": 2,
						},
					],
				}
			),
		},
		{
			"template_name": "Event Feedback",
			"category": "Event Feedback",
			"is_system_template": 1,
			"description": "Collect post-event feedback.",
			"survey_data": json.dumps(
				{
					"description": "Thank you for attending! Please share your feedback.",
					"questions": [
						{
							"id": "q1",
							"question": "How would you rate the event overall?",
							"question_type": "Star Rating",
							"required": True,
							"options": [],
							"page_number": 1,
						},
						{
							"id": "q2",
							"question": "How relevant was the content to your needs?",
							"question_type": "Rating",
							"required": True,
							"options": [],
							"page_number": 1,
						},
						{
							"id": "q3",
							"question": "What did you find most valuable?",
							"question_type": "Long Answer",
							"required": False,
							"options": [],
							"page_number": 2,
						},
						{
							"id": "q4",
							"question": "What could be improved for next time?",
							"question_type": "Long Answer",
							"required": False,
							"options": [],
							"page_number": 2,
						},
						{
							"id": "q5",
							"question": "Would you attend our next event?",
							"question_type": "Yes/No",
							"required": True,
							"options": [],
							"page_number": 2,
						},
					],
				}
			),
		},
		{
			"template_name": "Market Research",
			"category": "Market Research",
			"is_system_template": 1,
			"description": "Understand your market and customer preferences.",
			"survey_data": json.dumps(
				{
					"description": "Help us understand you better.",
					"questions": [
						{
							"id": "q1",
							"question": "Age range",
							"question_type": "Multiple Choice",
							"required": True,
							"options": ["Under 18", "18-24", "25-34", "35-44", "45-54", "55+"],
							"page_number": 1,
						},
						{
							"id": "q2",
							"question": "How did you hear about us?",
							"question_type": "Multiple Choice",
							"required": False,
							"options": [
								"Social Media",
								"Search Engine",
								"Friend/Family",
								"Advertisement",
								"Other",
							],
							"page_number": 1,
						},
						{
							"id": "q3",
							"question": "What factors influence your purchase decision?",
							"question_type": "Checkbox",
							"required": False,
							"options": ["Price", "Quality", "Brand", "Reviews", "Convenience", "Features"],
							"page_number": 2,
						},
						{
							"id": "q4",
							"question": "Any other feedback?",
							"question_type": "Long Answer",
							"required": False,
							"options": [],
							"page_number": 2,
						},
					],
				}
			),
		},
	]

	for t in templates:
		if not frappe.db.exists("Forms Template", t["template_name"]):
			frappe.get_doc({"doctype": "Forms Template", **t}).insert()
