const BASE = "/api/method/forms.api";

async function call(method, args = {}) {
	const res = await fetch(`${BASE}.${method}`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-Frappe-CSRF-Token": window.csrf_token || "",
		},
		body: JSON.stringify(args),
	});
	const data = await res.json();
	if (data.exc) {
		const err = new Error(data.exc_type || "API Error");
		err.exc_type = data.exc_type;
		err.message = data._error_message || data.exc;
		throw err;
	}
	return data.message;
}

export const surveyAPI = {
	list: (filters = {}) => call("get_surveys", filters),
	get: (name) => call("get_survey", { name }),
	create: (data) => call("create_survey", { data: JSON.stringify(data) }),
	update: (name, data) => call("update_survey", { name, data: JSON.stringify(data) }),
	delete: (name) => call("delete_survey", { name }),
	duplicate: (name) => call("duplicate_survey", { name }),
	publish: (name) => call("publish_survey", { name }),
	unpublish: (name) => call("unpublish_survey", { name }),
	close: (name) => call("close_survey", { name }),
	getByCode: (code) => call("get_survey_by_code", { survey_code: code }),
};

export const responseAPI = {
	submit: (surveyCode, answers, meta = {}) =>
		call("submit_response", {
			survey_code: surveyCode,
			answers: JSON.stringify(answers),
			...meta,
		}),
	saveDraft: (surveyCode, answers, responseId = null) =>
		call("save_draft", {
			survey_code: surveyCode,
			answers: JSON.stringify(answers),
			response_id: responseId,
		}),
	list: (survey, page = 1) => call("get_responses", { survey, page }),
	get: (name) => call("get_response", { name }),
	export: (survey) => call("export_responses", { survey }),
};

export const analyticsAPI = {
	get: (survey) => call("get_analytics", { survey }),
};

export const templateAPI = {
	list: () => call("get_templates"),
	createFromTemplate: (templateName, title) =>
		call("create_from_template", { template_name: templateName, survey_title: title }),
};

export const questionBankAPI = {
	list: (search = "") => call("get_question_bank", { search }),
	create: (data) => call("create_question_bank_item", { data: JSON.stringify(data) }),
};

export const invitationAPI = {
	send: (survey, recipients) =>
		call("send_invitations", { survey, recipients: JSON.stringify(recipients) }),
};
