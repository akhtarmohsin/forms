import frappe
from frappe.utils import today


def close_expired_surveys() -> None:
	expired = frappe.db.get_all(
		"Forms Survey",
		filters={"status": "Published", "end_date": ("<", today())},
		pluck="name",
	)
	for name in expired:
		frappe.db.set_value("Forms Survey", name, "status", "Closed")
	if expired:
		frappe.db.commit()
