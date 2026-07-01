app_name = "forms"
app_title = "Forms"
app_publisher = "Mohsin Akhtar"
app_description = "Survey and Form Builder for Frappe"
app_email = "mohsin@frappe.io"
app_license = "mit"
app_logo_url = "/assets/forms/images/forms-mark.svg"

export_python_type_annotations = True

# Route /survey/<code> → survey.html SPA entry
website_route_rules = [
	{"from_route": "/survey/<path:survey_code>", "to_route": "survey"},
	{"from_route": "/forms/<path:subpath>", "to_route": "forms"},
]

# After install — seed roles + templates
after_install = "forms.forms.install.after_install"

# Scheduled tasks
scheduler_events = {
	"daily": [
		"forms.forms.tasks.close_expired_surveys",
	],
}

# Apps screen entry
add_to_apps_screen = [
	{
		"name": "forms",
		"logo": "/assets/forms/images/forms-mark.svg",
		"title": "Forms",
		"route": "/forms",
	}
]
