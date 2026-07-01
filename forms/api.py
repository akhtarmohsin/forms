"""
Forms app — all whitelisted API endpoints.
No DocTypes. All data stored in a single JSON document per survey.
"""
from __future__ import annotations

import json
from datetime import datetime, date

import frappe
from frappe import _
from frappe.utils import now_datetime, get_url, cstr
from frappe.rate_limiter import rate_limit

# ---------------------------------------------------------------------------
# Survey CRUD
# ---------------------------------------------------------------------------

@frappe.whitelist()
def get_surveys(status: str = None, search: str = None) -> list:
	"""List surveys owned by the current user (or all, for Survey Manager)."""
	filters: dict = {}
	if not frappe.has_permission("Forms Survey", "read", throw=False):
		filters["owner"] = frappe.session.user
	if status:
		filters["status"] = status

	surveys = frappe.get_all(
		"Forms Survey",
		filters=filters,
		fields=["name", "survey_title", "survey_code", "status", "total_responses",
		        "modified", "owner"],
		order_by="modified desc",
		limit=200,
	)
	if search:
		s = search.lower()
		surveys = [x for x in surveys if s in (x.survey_title or "").lower()]
	return surveys


@frappe.whitelist()
def get_survey(name: str) -> dict:
	"""Return full survey document including questions."""
	frappe.has_permission("Forms Survey", "read", doc=name, throw=True)
	doc = frappe.get_doc("Forms Survey", name)
	return _serialize_survey(doc)


@frappe.whitelist()
def get_survey_by_code(survey_code: str) -> dict:
	"""Public endpoint: return survey for respondents."""
	name = frappe.db.get_value("Forms Survey", {"survey_code": survey_code}, "name")
	if not name:
		frappe.throw(_("Survey not found"), frappe.DoesNotExistError)

	doc = frappe.get_doc("Forms Survey", name)

	if doc.status != "Published":
		frappe.throw(_("This survey is not currently accepting responses"), frappe.PermissionError)

	_check_dates(doc)

	if doc.require_login and frappe.session.user == "Guest":
		frappe.throw(_("Please log in to take this survey"), frappe.PermissionError)

	return {
		"survey": {
			"name": doc.name,
			"survey_title": doc.survey_title,
			"description": doc.description,
			"status": doc.status,
			"allow_anonymous_responses": doc.allow_anonymous_responses,
			"allow_multiple_responses": doc.allow_multiple_responses,
			"require_login": doc.require_login,
			"display_progress_bar": doc.display_progress_bar,
			"shuffle_questions": doc.shuffle_questions,
			"thank_you_message": doc.thank_you_message or "Thank you for your response!",
			"redirect_url": doc.redirect_url,
			"survey_code": doc.survey_code,
		},
		"questions": _get_questions(doc),
		"theme": _safe_json(doc.theme_config),
	}


@frappe.whitelist()
def create_survey(data: str) -> dict:
	"""Create a new survey."""
	payload = json.loads(data)
	doc = frappe.new_doc("Forms Survey")
	doc.survey_title = payload.get("survey_title") or "Untitled Form"
	doc.description = payload.get("description", "")
	doc.status = "Draft"
	doc.allow_anonymous_responses = payload.get("allow_anonymous_responses", 0)
	doc.require_login = payload.get("require_login", 1)
	doc.allow_multiple_responses = payload.get("allow_multiple_responses", 0)
	doc.display_progress_bar = payload.get("display_progress_bar", 1)
	doc.shuffle_questions = payload.get("shuffle_questions", 0)
	doc.thank_you_message = payload.get("thank_you_message", "")
	doc.redirect_url = payload.get("redirect_url", "")
	doc.start_date = payload.get("start_date") or None
	doc.end_date = payload.get("end_date") or None
	doc.theme_config = json.dumps(payload.get("theme_config", {}))
	doc.questions_data = json.dumps(payload.get("questions", []))
	doc.insert()
	return {"name": doc.name, "survey_code": doc.survey_code}


@frappe.whitelist()
def update_survey(name: str, data: str) -> dict:
	"""Update an existing survey."""
	frappe.has_permission("Forms Survey", "write", doc=name, throw=True)
	payload = json.loads(data)
	doc = frappe.get_doc("Forms Survey", name)
	doc.survey_title = payload.get("survey_title", doc.survey_title)
	doc.description = payload.get("description", doc.description)
	doc.allow_anonymous_responses = payload.get("allow_anonymous_responses", doc.allow_anonymous_responses)
	doc.require_login = payload.get("require_login", doc.require_login)
	doc.allow_multiple_responses = payload.get("allow_multiple_responses", doc.allow_multiple_responses)
	doc.display_progress_bar = payload.get("display_progress_bar", doc.display_progress_bar)
	doc.shuffle_questions = payload.get("shuffle_questions", doc.shuffle_questions)
	doc.thank_you_message = payload.get("thank_you_message", doc.thank_you_message)
	doc.redirect_url = payload.get("redirect_url", doc.redirect_url)
	doc.start_date = payload.get("start_date") or None
	doc.end_date = payload.get("end_date") or None
	if "theme_config" in payload:
		doc.theme_config = json.dumps(payload["theme_config"])
	if "questions" in payload:
		doc.questions_data = json.dumps(payload["questions"])
	doc.save()
	return {"name": doc.name, "survey_code": doc.survey_code}


@frappe.whitelist()
def delete_survey(name: str) -> dict:
	frappe.has_permission("Forms Survey", "delete", doc=name, throw=True)
	frappe.delete_doc("Forms Survey", name)
	return {"deleted": name}


@frappe.whitelist()
def duplicate_survey(name: str) -> dict:
	frappe.has_permission("Forms Survey", "read", doc=name, throw=True)
	original = frappe.get_doc("Forms Survey", name)
	doc = frappe.copy_doc(original)
	doc.survey_title = f"Copy of {original.survey_title}"
	doc.status = "Draft"
	doc.total_responses = 0
	doc.survey_code = None
	doc.insert()
	return {"name": doc.name}


@frappe.whitelist()
def publish_survey(name: str) -> dict:
	frappe.has_permission("Forms Survey", "write", doc=name, throw=True)
	frappe.db.set_value("Forms Survey", name, "status", "Published")
	url = f"{get_url()}/survey/{frappe.db.get_value('Forms Survey', name, 'survey_code')}"
	return {"status": "Published", "url": url}


@frappe.whitelist()
def unpublish_survey(name: str) -> dict:
	frappe.has_permission("Forms Survey", "write", doc=name, throw=True)
	frappe.db.set_value("Forms Survey", name, "status", "Draft")
	return {"status": "Draft"}


@frappe.whitelist()
def close_survey(name: str) -> dict:
	frappe.has_permission("Forms Survey", "write", doc=name, throw=True)
	frappe.db.set_value("Forms Survey", name, "status", "Closed")
	return {"status": "Closed"}


# ---------------------------------------------------------------------------
# Responses
# ---------------------------------------------------------------------------

@frappe.whitelist(allow_guest=True)
@rate_limit(limit=30, seconds=60)
def submit_response(survey_code: str, answers: str, response_id: str = None) -> dict:
	"""Submit a completed survey response."""
	survey_name = frappe.db.get_value("Forms Survey", {"survey_code": survey_code}, "name")
	if not survey_name:
		frappe.throw(_("Survey not found"))

	survey = frappe.get_doc("Forms Survey", survey_name)
	if survey.status != "Published":
		frappe.throw(_("Survey is not accepting responses"))

	_check_dates(survey)
	_check_duplicate(survey)

	answers_data = json.loads(answers) if isinstance(answers, str) else answers
	now = now_datetime()

	doc = frappe.new_doc("Forms Response")
	doc.survey = survey_name
	doc.survey_code = survey_code
	doc.completion_status = "Completed"
	doc.submitted_on = now
	doc.start_time = now
	doc.end_time = now

	user = frappe.session.user
	if user and user != "Guest":
		doc.respondent_email = user
		doc.respondent_name = frappe.db.get_value("User", user, "full_name") or user

	doc.ip_address = frappe.local.request_ip if hasattr(frappe.local, "request_ip") else None
	doc.answers_data = json.dumps(answers_data)

	if response_id:
		# Update existing draft
		try:
			existing = frappe.get_doc("Forms Response", response_id)
			existing.completion_status = "Completed"
			existing.submitted_on = now
			existing.end_time = now
			existing.answers_data = json.dumps(answers_data)
			existing.save(ignore_permissions=True)
			_bump_response_count(survey_name)
			return {"response_id": existing.name, "status": "Completed"}
		except frappe.DoesNotExistError:
			pass

	doc.insert(ignore_permissions=True)
	_bump_response_count(survey_name)
	return {"response_id": doc.name, "status": "Completed"}


@frappe.whitelist(allow_guest=True)
def save_draft(survey_code: str, answers: str, response_id: str = None) -> dict:
	"""Save a draft response."""
	survey_name = frappe.db.get_value("Forms Survey", {"survey_code": survey_code}, "name")
	if not survey_name:
		frappe.throw(_("Survey not found"))

	answers_data = json.loads(answers) if isinstance(answers, str) else answers

	if response_id:
		try:
			doc = frappe.get_doc("Forms Response", response_id)
			if doc.completion_status != "Completed":
				doc.answers_data = json.dumps(answers_data)
				doc.save(ignore_permissions=True)
				return {"response_id": doc.name}
		except frappe.DoesNotExistError:
			pass

	doc = frappe.new_doc("Forms Response")
	doc.survey = survey_name
	doc.survey_code = survey_code
	doc.completion_status = "Draft"
	doc.answers_data = json.dumps(answers_data)
	if frappe.session.user != "Guest":
		doc.respondent_email = frappe.session.user
	doc.insert(ignore_permissions=True)
	return {"response_id": doc.name}


@frappe.whitelist()
def get_responses(survey: str, page: int = 1) -> list:
	frappe.has_permission("Forms Survey", "read", doc=survey, throw=True)
	return frappe.get_all(
		"Forms Response",
		filters={"survey": survey},
		fields=["name", "respondent_name", "respondent_email", "completion_status",
		        "submitted_on", "ip_address"],
		order_by="submitted_on desc",
		limit_start=(int(page) - 1) * 50,
		limit_page_length=50,
	)


@frappe.whitelist()
def get_response(name: str) -> dict:
	doc = frappe.get_doc("Forms Response", name)
	return {
		"name": doc.name,
		"survey": doc.survey,
		"completion_status": doc.completion_status,
		"respondent_name": doc.respondent_name,
		"respondent_email": doc.respondent_email,
		"submitted_on": str(doc.submitted_on) if doc.submitted_on else None,
		"answers": _safe_json(doc.answers_data),
	}


@frappe.whitelist()
def export_responses(survey: str) -> str:
	"""Export responses as CSV. Returns file URL."""
	import csv, io
	from frappe.utils.file_manager import save_file

	frappe.has_permission("Forms Survey", "read", doc=survey, throw=True)

	s_doc = frappe.get_doc("Forms Survey", survey)
	questions = _get_questions(s_doc)
	responses = frappe.get_all(
		"Forms Response",
		filters={"survey": survey},
		fields=["name", "respondent_name", "respondent_email", "completion_status",
		        "submitted_on", "answers_data"],
		order_by="submitted_on desc",
		limit=10000,
	)

	buf = io.StringIO()
	writer = csv.writer(buf)
	header = ["Response ID", "Respondent", "Email", "Status", "Submitted On"]
	header += [q["question"] for q in questions]
	writer.writerow(header)

	for r in responses:
		answers = {a["question"]: a.get("answer", "") for a in (_safe_json(r.answers_data) or [])}
		row = [r.name, r.respondent_name, r.respondent_email, r.completion_status, r.submitted_on]
		row += [answers.get(q["question"], "") for q in questions]
		writer.writerow(row)

	content = buf.getvalue().encode("utf-8")
	file_doc = save_file(f"{survey}_responses.csv", content, "Forms Survey", survey, is_private=0)
	return file_doc.file_url


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------

@frappe.whitelist()
def get_analytics(survey: str) -> dict:
	frappe.has_permission("Forms Survey", "read", doc=survey, throw=True)

	responses = frappe.get_all(
		"Forms Response",
		filters={"survey": survey},
		fields=["name", "completion_status", "submitted_on", "answers_data"],
	)

	total = len(responses)
	completed_responses = [r for r in responses if r.completion_status == "Completed"]
	completed = len(completed_responses)

	# Daily counts
	daily: dict = {}
	for r in completed_responses:
		if r.submitted_on:
			day = str(r.submitted_on)[:10]
			daily[day] = daily.get(day, 0) + 1
	daily_list = sorted([{"day": k, "count": v} for k, v in daily.items()], key=lambda x: x["day"])

	# Question stats
	s_doc = frappe.get_doc("Forms Survey", survey)
	questions = _get_questions(s_doc)
	q_stats = _compute_question_stats(questions, completed_responses)

	return {
		"total_responses": total,
		"completed_responses": completed,
		"completion_rate": round(completed / total * 100, 1) if total else 0,
		"average_duration": 0,
		"daily_responses": daily_list[-30:],
		"question_stats": q_stats,
	}


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

@frappe.whitelist()
def get_templates() -> list:
	return frappe.get_all(
		"Forms Template",
		filters={"is_system_template": 1},
		fields=["name", "template_name", "category", "description"],
		order_by="template_name asc",
	)


@frappe.whitelist()
def create_from_template(template_name: str, survey_title: str = None) -> dict:
	template = frappe.get_doc("Forms Template", template_name)
	data = _safe_json(template.survey_data) or {}
	doc = frappe.new_doc("Forms Survey")
	doc.survey_title = survey_title or template.template_name
	doc.description = data.get("description", "")
	doc.status = "Draft"
	doc.questions_data = json.dumps(data.get("questions", []))
	doc.insert()
	return _serialize_survey(doc)


# ---------------------------------------------------------------------------
# Question Bank
# ---------------------------------------------------------------------------

@frappe.whitelist()
def get_question_bank(search: str = "") -> list:
	filters = {}
	if search:
		filters["question"] = ["like", f"%{search}%"]
	return frappe.get_all(
		"Forms Question Bank",
		filters=filters,
		fields=["name", "question", "question_type", "category", "options"],
		limit=100,
	)


@frappe.whitelist()
def create_question_bank_item(data: str) -> dict:
	payload = json.loads(data)
	doc = frappe.new_doc("Forms Question Bank")
	doc.question = payload["question"]
	doc.question_type = payload.get("question_type", "Short Answer")
	doc.category = payload.get("category", "")
	doc.options = json.dumps(payload.get("options", []))
	doc.insert()
	return {"name": doc.name}


# ---------------------------------------------------------------------------
# Invitations
# ---------------------------------------------------------------------------

@frappe.whitelist()
def send_invitations(survey: str, recipients: str) -> dict:
	frappe.has_permission("Forms Survey", "write", doc=survey, throw=True)
	s_doc = frappe.get_doc("Forms Survey", survey)
	recs = json.loads(recipients) if isinstance(recipients, str) else recipients
	sent = 0
	survey_url = f"{get_url()}/survey/{s_doc.survey_code}"

	for r in recs:
		email = r.get("email")
		if not email:
			continue
		frappe.sendmail(
			recipients=[email],
			subject=_("You're invited: {0}").format(s_doc.survey_title),
			message=_(
				"<p>Hello {0},</p>"
				"<p>You've been invited to complete this survey: <strong>{1}</strong></p>"
				"<p><a href='{2}' style='background:#4f46e5;color:#fff;padding:10px 20px;border-radius:8px;"
				"text-decoration:none;display:inline-block'>Take Survey →</a></p>"
			).format(r.get("name", email), s_doc.survey_title, survey_url),
		)
		sent += 1
	return {"sent": sent}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _serialize_survey(doc) -> dict:
	return {
		"name": doc.name,
		"survey_title": doc.survey_title,
		"survey_code": doc.survey_code,
		"description": doc.description,
		"status": doc.status,
		"allow_anonymous_responses": bool(doc.allow_anonymous_responses),
		"allow_multiple_responses": bool(doc.allow_multiple_responses),
		"require_login": bool(doc.require_login),
		"display_progress_bar": bool(doc.display_progress_bar),
		"shuffle_questions": bool(doc.shuffle_questions),
		"thank_you_message": doc.thank_you_message,
		"redirect_url": doc.redirect_url,
		"start_date": str(doc.start_date) if doc.start_date else None,
		"end_date": str(doc.end_date) if doc.end_date else None,
		"theme_config": _safe_json(doc.theme_config),
		"questions": _get_questions(doc),
		"total_responses": doc.total_responses or 0,
		"modified": str(doc.modified),
	}


def _get_questions(doc) -> list:
	return _safe_json(doc.questions_data) or []


def _safe_json(val):
	if not val:
		return None
	if isinstance(val, (dict, list)):
		return val
	try:
		return json.loads(val)
	except (json.JSONDecodeError, TypeError):
		return None


def _check_dates(survey) -> None:
	from frappe.utils import getdate, today
	if survey.start_date and getdate(survey.start_date) > getdate(today()):
		frappe.throw(_("This survey has not started yet"))
	if survey.end_date and getdate(survey.end_date) < getdate(today()):
		frappe.throw(_("This survey has ended"))


def _check_duplicate(survey) -> None:
	if survey.allow_multiple_responses:
		return
	if frappe.session.user == "Guest":
		return
	existing = frappe.db.exists(
		"Forms Response",
		{"survey": survey.name, "respondent_email": frappe.session.user, "completion_status": "Completed"},
	)
	if existing:
		frappe.throw(_("You have already submitted a response to this survey"))


def _bump_response_count(survey_name: str) -> None:
	frappe.db.sql(
		"UPDATE `tabForms Survey` SET total_responses = total_responses + 1 WHERE name = %s",
		survey_name,
	)


def _compute_question_stats(questions: list, completed_responses: list) -> list:
	stats = []
	for q in questions:
		qtext = q.get("question", "")
		qtype = q.get("question_type", "")
		all_answers = []

		for r in completed_responses:
			answers = _safe_json(r.answers_data) or []
			for a in answers:
				if a.get("question") == qtext:
					val = a.get("answer")
					if val not in (None, ""):
						all_answers.append(str(val))

		stat: dict = {
			"question": qtext,
			"question_type": qtype,
			"total_answers": len(all_answers),
		}

		if qtype in ("Multiple Choice", "Checkbox", "Dropdown", "Yes/No", "True/False"):
			counts: dict = {}
			for a in all_answers:
				for v in a.split(","):
					v = v.strip()
					if v:
						counts[v] = counts.get(v, 0) + 1
			stat["distribution"] = counts

		elif qtype in ("Rating", "Star Rating", "Linear Scale", "Slider"):
			nums = []
			for a in all_answers:
				try:
					nums.append(float(a))
				except ValueError:
					pass
			stat["average"] = round(sum(nums) / len(nums), 2) if nums else 0

		elif qtype == "Net Promoter Score":
			scores = []
			for a in all_answers:
				try:
					scores.append(int(float(a)))
				except ValueError:
					pass
			if scores:
				promoters = sum(1 for s in scores if s >= 9)
				detractors = sum(1 for s in scores if s <= 6)
				stat["nps"] = round((promoters - detractors) / len(scores) * 100, 1)

		stats.append(stat)
	return stats
