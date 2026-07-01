export const QUESTION_TYPES = [
	// Basic
	{ value: "Short Answer", label: "Short Answer", icon: "minus", group: "Text" },
	{ value: "Long Answer", label: "Long Answer", icon: "align-left", group: "Text" },
	{ value: "Number", label: "Number", icon: "hash", group: "Text" },
	{ value: "Email", label: "Email", icon: "mail", group: "Text" },
	{ value: "Phone", label: "Phone", icon: "phone", group: "Text" },
	{ value: "URL", label: "URL / Link", icon: "link", group: "Text" },
	// Date/Time
	{ value: "Date", label: "Date", icon: "calendar", group: "Date & Time" },
	{ value: "Time", label: "Time", icon: "clock", group: "Date & Time" },
	{ value: "Date & Time", label: "Date & Time", icon: "calendar", group: "Date & Time" },
	// Choice
	{ value: "Multiple Choice", label: "Multiple Choice", icon: "circle", group: "Choice" },
	{ value: "Checkbox", label: "Checkboxes", icon: "check-square", group: "Choice" },
	{ value: "Dropdown", label: "Dropdown", icon: "chevron-down", group: "Choice" },
	{ value: "Yes/No", label: "Yes / No", icon: "toggle-right", group: "Choice" },
	// Scale
	{ value: "Rating", label: "Rating (1–5)", icon: "star", group: "Scale" },
	{ value: "Star Rating", label: "Star Rating", icon: "star", group: "Scale" },
	{ value: "Linear Scale", label: "Linear Scale", icon: "sliders", group: "Scale" },
	{ value: "Slider", label: "Slider", icon: "sliders", group: "Scale" },
	{ value: "Net Promoter Score", label: "NPS (0–10)", icon: "trending-up", group: "Scale" },
	// Ranking
	{ value: "Ranking", label: "Ranking", icon: "list", group: "Advanced" },
	{ value: "Matrix", label: "Matrix / Grid", icon: "grid", group: "Advanced" },
	// Media
	{ value: "File Upload", label: "File Upload", icon: "upload", group: "Media" },
	{ value: "Signature", label: "Signature", icon: "edit-2", group: "Media" },
];

export const QUESTION_GROUPS = [...new Set(QUESTION_TYPES.map((q) => q.group))];

export function getQuestionType(value) {
	return QUESTION_TYPES.find((q) => q.value === value);
}

export function makeQuestion(type = "Short Answer") {
	return {
		id: crypto.randomUUID(),
		question: "",
		question_type: type,
		required: false,
		description: "",
		placeholder: "",
		options:
			type === "Multiple Choice" || type === "Checkbox" || type === "Dropdown"
				? ["Option 1"]
				: [],
		allow_other: false,
		min_value: null,
		max_value: null,
		min_length: null,
		max_length: null,
		page_number: 1,
		section_name: "",
		conditional_logic: null,
		image: null,
		weight: 1,
	};
}

export function hasOptions(type) {
	return ["Multiple Choice", "Checkbox", "Dropdown", "Ranking"].includes(type);
}

export function isScaleType(type) {
	return ["Rating", "Star Rating", "Linear Scale", "Slider", "Net Promoter Score"].includes(
		type
	);
}
