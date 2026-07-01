<template>
	<div
		class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4"
		@click.self="$emit('close')"
	>
		<div
			class="bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[80vh] flex flex-col overflow-hidden"
		>
			<div class="flex items-center justify-between p-6 border-b border-gray-100">
				<h2 class="text-lg font-semibold">Start with a template</h2>
				<button
					@click="$emit('close')"
					class="text-gray-400 hover:text-gray-600 transition-colors"
				>
					<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M6 18L18 6M6 6l12 12"
						/>
					</svg>
				</button>
			</div>

			<div class="overflow-y-auto flex-1 p-6">
				<!-- Blank option -->
				<button
					@click="$emit('select', null)"
					class="w-full flex items-center gap-4 p-4 rounded-xl border-2 border-dashed border-blue-300 bg-blue-50 hover:bg-blue-100 transition-colors mb-6 text-left"
				>
					<div
						class="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center flex-shrink-0"
					>
						<svg
							class="w-5 h-5 text-white"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M12 4v16m8-8H4"
							/>
						</svg>
					</div>
					<div>
						<div class="font-semibold text-blue-700">Blank Form</div>
						<div class="text-sm text-blue-500">Start from scratch</div>
					</div>
				</button>

				<!-- Templates -->
				<div v-if="loading" class="grid grid-cols-2 gap-3">
					<div
						v-for="i in 6"
						:key="i"
						class="h-24 bg-gray-100 rounded-xl animate-pulse"
					/>
				</div>
				<div v-else>
					<p class="text-xs font-medium text-gray-400 uppercase tracking-wider mb-3">
						Templates
					</p>
					<div class="grid grid-cols-2 gap-3">
						<button
							v-for="t in templates"
							:key="t.name"
							@click="selectTemplate(t)"
							class="flex items-start gap-3 p-4 rounded-xl border border-gray-200 hover:border-blue-400 hover:bg-blue-50 transition-colors text-left"
						>
							<div
								class="w-9 h-9 rounded-lg flex-shrink-0 flex items-center justify-center text-white text-base"
								:style="{ background: categoryColor(t.category) }"
							>
								{{ categoryEmoji(t.category) }}
							</div>
							<div class="min-w-0">
								<div class="font-medium text-gray-900 text-sm truncate">
									{{ t.template_name }}
								</div>
								<div class="text-xs text-gray-400 truncate">{{ t.category }}</div>
							</div>
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { templateAPI } from "@/utils/api";

const emit = defineEmits(["close", "select"]);
const templates = ref([]);
const loading = ref(true);

onMounted(async () => {
	try {
		templates.value = await templateAPI.list();
	} catch {
		templates.value = [];
	} finally {
		loading.value = false;
	}
});

async function selectTemplate(t) {
	const { templateAPI: api } = await import("@/utils/api");
	const result = await api.createFromTemplate(t.name, t.template_name);
	emit("select", result);
}

const COLORS = {
	"Customer Satisfaction": "#10b981",
	"Employee Feedback": "#6366f1",
	"Exit Interview": "#f59e0b",
	"Event Feedback": "#ec4899",
	"Market Research": "#3b82f6",
	"Training Evaluation": "#8b5cf6",
	"Product Feedback": "#14b8a6",
	Custom: "#6b7280",
};
const EMOJIS = {
	"Customer Satisfaction": "😊",
	"Employee Feedback": "👥",
	"Exit Interview": "👋",
	"Event Feedback": "🎉",
	"Market Research": "📊",
	"Training Evaluation": "📚",
	"Product Feedback": "🚀",
	Custom: "📋",
};
function categoryColor(c) {
	return COLORS[c] || "#6b7280";
}
function categoryEmoji(c) {
	return EMOJIS[c] || "📋";
}
</script>
