import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { makeQuestion } from "@/utils/questions";
import { surveyAPI } from "@/utils/api";

export const useSurveyStore = defineStore("survey", () => {
	const survey = ref({
		name: null,
		survey_title: "Untitled Form",
		description: "",
		status: "Draft",
		allow_anonymous_responses: false,
		require_login: true,
		allow_multiple_responses: false,
		display_progress_bar: true,
		shuffle_questions: false,
		thank_you_message: "Thank you for completing this survey!",
		redirect_url: "",
		theme_config: {
			primary_color: "#4f46e5",
			background_color: "#f9fafb",
			card_color: "#ffffff",
			text_color: "#111827",
			button_color: "#4f46e5",
			font_family: "Inter",
			border_radius: 12,
		},
		questions: [],
		start_date: null,
		end_date: null,
	});

	const activeQuestionId = ref(null);
	const saving = ref(false);
	const dirty = ref(false);

	const activeQuestion = computed(
		() => survey.value.questions.find((q) => q.id === activeQuestionId.value) || null
	);

	function setActiveQuestion(id) {
		activeQuestionId.value = id;
	}

	function addQuestion(type = "Short Answer", afterId = null) {
		const q = makeQuestion(type);
		if (afterId) {
			const idx = survey.value.questions.findIndex((x) => x.id === afterId);
			survey.value.questions.splice(idx + 1, 0, q);
		} else {
			survey.value.questions.push(q);
		}
		activeQuestionId.value = q.id;
		dirty.value = true;
		return q;
	}

	function removeQuestion(id) {
		const idx = survey.value.questions.findIndex((q) => q.id === id);
		if (idx === -1) return;
		survey.value.questions.splice(idx, 1);
		if (activeQuestionId.value === id) {
			activeQuestionId.value = survey.value.questions[Math.max(0, idx - 1)]?.id || null;
		}
		dirty.value = true;
	}

	function duplicateQuestion(id) {
		const q = survey.value.questions.find((x) => x.id === id);
		if (!q) return;
		const copy = { ...JSON.parse(JSON.stringify(q)), id: crypto.randomUUID() };
		const idx = survey.value.questions.findIndex((x) => x.id === id);
		survey.value.questions.splice(idx + 1, 0, copy);
		activeQuestionId.value = copy.id;
		dirty.value = true;
	}

	function updateQuestion(id, patch) {
		const q = survey.value.questions.find((x) => x.id === id);
		if (q) {
			Object.assign(q, patch);
			dirty.value = true;
		}
	}

	function reorderQuestions(newOrder) {
		survey.value.questions = newOrder;
		dirty.value = true;
	}

	function updateSurveyMeta(patch) {
		Object.assign(survey.value, patch);
		dirty.value = true;
	}

	function loadSurvey(data) {
		survey.value = {
			...survey.value,
			...data,
			questions: (data.questions || []).map((q) => ({
				...q,
				id: q.id || crypto.randomUUID(),
				options: q.options || [],
			})),
		};
		dirty.value = false;
		activeQuestionId.value = survey.value.questions[0]?.id || null;
	}

	async function save() {
		saving.value = true;
		try {
			const payload = {
				...survey.value,
				questions: survey.value.questions.map((q, i) => ({ ...q, idx: i + 1 })),
			};
			let result;
			if (survey.value.name) {
				result = await surveyAPI.update(survey.value.name, payload);
			} else {
				result = await surveyAPI.create(payload);
				survey.value.name = result.name;
			}
			dirty.value = false;
			return result;
		} finally {
			saving.value = false;
		}
	}

	function reset() {
		survey.value = {
			name: null,
			survey_title: "Untitled Form",
			description: "",
			status: "Draft",
			allow_anonymous_responses: false,
			require_login: true,
			allow_multiple_responses: false,
			display_progress_bar: true,
			shuffle_questions: false,
			thank_you_message: "Thank you for completing this survey!",
			redirect_url: "",
			theme_config: {
				primary_color: "#4f46e5",
				background_color: "#f9fafb",
				card_color: "#ffffff",
				text_color: "#111827",
				button_color: "#4f46e5",
				font_family: "Inter",
				border_radius: 12,
			},
			questions: [],
			start_date: null,
			end_date: null,
		};
		activeQuestionId.value = null;
		dirty.value = false;
	}

	return {
		survey,
		activeQuestionId,
		activeQuestion,
		saving,
		dirty,
		setActiveQuestion,
		addQuestion,
		removeQuestion,
		duplicateQuestion,
		updateQuestion,
		reorderQuestions,
		updateSurveyMeta,
		loadSurvey,
		save,
		reset,
	};
});
