<template>
	<div
		class="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-md transition-shadow group relative flex flex-col"
	>
		<!-- Status badge -->
		<div class="flex items-start justify-between mb-3">
			<span
				class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
				:class="statusClass"
				>{{ survey.status }}</span
			>
			<!-- Actions menu -->
			<div class="relative">
				<button
					@click.stop="menuOpen = !menuOpen"
					class="w-7 h-7 rounded-md flex items-center justify-center text-gray-400 hover:text-gray-700 hover:bg-gray-100 opacity-0 group-hover:opacity-100 transition-opacity"
				>
					<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
						<path
							d="M12 5a1.5 1.5 0 110 3 1.5 1.5 0 010-3zm0 5.5a1.5 1.5 0 110 3 1.5 1.5 0 010-3zm0 5.5a1.5 1.5 0 110 3 1.5 1.5 0 010-3z"
						/>
					</svg>
				</button>
				<transition name="fade">
					<div
						v-if="menuOpen"
						v-click-outside="() => (menuOpen = false)"
						class="absolute right-0 top-8 bg-white border border-gray-200 rounded-lg shadow-lg py-1 z-20 w-44"
					>
						<button @click="act('edit')" class="menu-item">Edit</button>
						<button @click="act('toggle-status')" class="menu-item">
							{{ survey.status === "Published" ? "Unpublish" : "Publish" }}
						</button>
						<button @click="act('view-responses')" class="menu-item">
							View Responses
						</button>
						<button @click="act('analytics')" class="menu-item">Analytics</button>
						<button @click="copyLink" class="menu-item">Copy Link</button>
						<button @click="act('duplicate')" class="menu-item">Duplicate</button>
						<div class="border-t border-gray-100 my-1" />
						<button
							@click="act('delete')"
							class="menu-item text-red-600 hover:bg-red-50"
						>
							Delete
						</button>
					</div>
				</transition>
			</div>
		</div>

		<!-- Title -->
		<h3
			@click="$emit('edit')"
			class="font-semibold text-gray-900 text-sm leading-tight mb-1 cursor-pointer hover:text-blue-600 line-clamp-2 flex-1"
		>
			{{ survey.survey_title || "Untitled Form" }}
		</h3>

		<!-- Meta -->
		<div
			class="text-xs text-gray-400 mt-auto pt-3 border-t border-gray-100 flex items-center justify-between"
		>
			<span
				>{{ survey.total_responses || 0 }} response{{
					survey.total_responses !== 1 ? "s" : ""
				}}</span
			>
			<span>{{ formatDate(survey.modified) }}</span>
		</div>
	</div>
</template>

<script setup>
import { ref, computed } from "vue";

const props = defineProps({ survey: Object });
const emit = defineEmits([
	"edit",
	"delete",
	"duplicate",
	"view-responses",
	"analytics",
	"toggle-status",
]);
const menuOpen = ref(false);

const statusClass = computed(() => ({
	"bg-yellow-50 text-yellow-700": props.survey.status === "Draft",
	"bg-green-50 text-green-700": props.survey.status === "Published",
	"bg-red-50 text-red-700": props.survey.status === "Closed",
	"bg-gray-100 text-gray-500": props.survey.status === "Archived",
}));

function act(ev) {
	menuOpen.value = false;
	emit(ev);
}

function copyLink() {
	menuOpen.value = false;
	const url = `${window.location.origin}/survey/${props.survey.survey_code}`;
	navigator.clipboard.writeText(url);
}

function formatDate(d) {
	if (!d) return "";
	return new Date(d).toLocaleDateString("en", { month: "short", day: "numeric" });
}

// click-outside directive
const vClickOutside = {
	mounted(el, binding) {
		el._clickOutside = (e) => {
			if (!el.contains(e.target)) binding.value(e);
		};
		document.addEventListener("click", el._clickOutside);
	},
	unmounted(el) {
		document.removeEventListener("click", el._clickOutside);
	},
};
</script>

<style scoped>
.menu-item {
	width: 100%;
	text-align: left;
	padding: 8px 16px;
	font-size: 0.875rem;
	color: #374151;
	transition: background 0.1s;
}
.menu-item:hover {
	background: #f9fafb;
}
.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.1s;
}
.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}
</style>
