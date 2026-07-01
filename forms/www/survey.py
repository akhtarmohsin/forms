import frappe


def get_context(context):
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
	context.csrf_token = frappe.sessions.get_csrf_token()
	context.session_user = frappe.session.user
	context.logged_in = frappe.session.user != "Guest"
