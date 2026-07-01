import frappe


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.local.flags.redirect_location = "/login?redirect-to=/forms"
		raise frappe.Redirect

	context.no_cache = 1
	import socket
	def _vite_running():
		try:
			s = socket.create_connection(("localhost", 8083), timeout=0.3)
			s.close()
			return True
		except OSError:
			return False
	context.vite_dev = frappe.conf.developer_mode and _vite_running()

	user = frappe.session.user
	user_doc = frappe.db.get_value("User", user, ["full_name", "user_image"], as_dict=True) or {}
	context.csrf_token = frappe.sessions.get_csrf_token()
	context.session_user = user
	context.full_name = user_doc.get("full_name", "")
	context.user_image = user_doc.get("user_image", "")
