<template>
	<div class="flex h-screen flex-col bg-gray-50">
		<!-- Navbar — Frappe standard -->
		<header class="relative z-10 grid grid-cols-3 items-center border-b bg-white p-2">
			<!-- Left: Logo + Title -->
			<div class="flex items-center gap-2 pl-1">
				<div
					class="flex h-7 w-7 items-center justify-center rounded-md bg-blue-600 flex-shrink-0"
				>
					<svg
						class="h-4 w-4 text-white"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
						/>
					</svg>
				</div>
				<span class="text-base font-semibold text-gray-900">Forms</span>
			</div>

			<!-- Center: Search + Tabs -->
			<div class="flex items-center justify-center gap-1">
				<button
					v-for="tab in tabs"
					:key="tab.value"
					@click="activeTab = tab.value"
					class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors"
					:class="
						activeTab === tab.value
							? 'bg-gray-100 text-gray-900'
							: 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
					"
				>
					{{ tab.label }}
				</button>
			</div>

			<!-- Right: Search + New button + Avatar -->
			<div class="flex items-center justify-end gap-2">
				<!-- Search -->
				<div class="relative">
					<svg
						class="absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-gray-400"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0"
						/>
					</svg>
					<input
						v-model="search"
						type="text"
						placeholder="Search forms…"
						class="h-7 w-44 rounded-md border border-gray-200 pl-8 pr-3 text-sm text-gray-700 placeholder-gray-400 focus:border-gray-300 focus:outline-none focus:ring-1 focus:ring-gray-300"
					/>
				</div>

				<!-- New Form button -->
				<button
					@click="createNew"
					class="inline-flex h-7 items-center gap-1.5 rounded-md bg-gray-900 px-3 text-sm font-medium text-white hover:bg-gray-700 transition-colors"
				>
					<svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M12 4v16m8-8H4"
						/>
					</svg>
					New Form
				</button>

				<!-- User avatar dropdown -->
				<div class="relative" ref="avatarRef">
					<button
						@click="showUserMenu = !showUserMenu"
						class="flex h-7 w-7 items-center justify-center rounded-full bg-gray-200 text-xs font-semibold text-gray-600 hover:bg-gray-300 transition-colors overflow-hidden"
					>
						<img
							v-if="userImage"
							:src="userImage"
							:alt="userInitials"
							class="h-full w-full object-cover"
						/>
						<span v-else>{{ userInitials }}</span>
					</button>
					<!-- Dropdown -->
					<div
						v-if="showUserMenu"
						class="absolute right-0 top-9 w-44 rounded-lg border border-gray-100 bg-white py-1 shadow-lg z-50"
					>
						<div class="border-b border-gray-100 px-3 py-2">
							<p class="text-sm font-medium text-gray-900 truncate">
								{{ fullName }}
							</p>
							<p class="text-xs text-gray-400 truncate">{{ sessionUser }}</p>
						</div>
						<a
							href="/app"
							class="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50"
						>
							<svg
								class="h-3.5 w-3.5 text-gray-400"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
								/>
							</svg>
							Desk
						</a>
						<button
							@click="logout"
							class="flex w-full items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50"
						>
							<svg
								class="h-3.5 w-3.5 text-gray-400"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
								/>
							</svg>
							Logout
						</button>
					</div>
				</div>
			</div>
		</header>

		<main class="flex-1 overflow-y-auto">
			<div class="max-w-7xl mx-auto px-6 py-8">
				<!-- Loading -->
				<div
					v-if="loading"
					class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
				>
					<div
						v-for="i in 8"
						:key="i"
						class="bg-white rounded-xl border border-gray-200 p-5 animate-pulse h-40"
					/>
				</div>

				<!-- Empty state -->
				<div
					v-else-if="filteredSurveys.length === 0"
					class="flex flex-col items-center justify-center py-24 text-center"
				>
					<div
						class="w-16 h-16 bg-blue-50 rounded-2xl flex items-center justify-center mb-4"
					>
						<svg
							class="w-8 h-8 text-blue-500"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="1.5"
								d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
							/>
						</svg>
					</div>
					<h3 class="text-lg font-semibold text-gray-900 mb-2">No forms yet</h3>
					<p class="text-gray-500 mb-6 text-sm max-w-xs">
						Create your first form to start collecting responses from your audience.
					</p>
					<button
						@click="createNew"
						class="inline-flex h-7 items-center gap-1.5 rounded-md bg-gray-900 px-3 text-sm font-medium text-white hover:bg-gray-700 transition-colors"
					>
						Create a form
					</button>
				</div>

				<!-- Survey grid -->
				<div
					v-else
					class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
				>
					<SurveyCard
						v-for="s in filteredSurveys"
						:key="s.name"
						:survey="s"
						@edit="editSurvey(s)"
						@delete="deleteSurvey(s)"
						@duplicate="duplicateSurvey(s)"
						@view-responses="viewResponses(s)"
						@analytics="viewAnalytics(s)"
						@toggle-status="toggleStatus(s)"
					/>
				</div>
			</div>
		</main>

		<!-- Template picker dialog -->
		<TemplatePickerDialog
			v-if="showTemplatePicker"
			@close="showTemplatePicker = false"
			@select="onTemplateSelected"
		/>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useSurveyStore } from "@/stores/survey";
import { surveyAPI } from "@/utils/api";
import SurveyCard from "@/components/ui/SurveyCard.vue";
import TemplatePickerDialog from "@/components/ui/TemplatePickerDialog.vue";

const router = useRouter();
const surveyStore = useSurveyStore();

const surveys = ref([]);
const loading = ref(true);
const search = ref("");
const activeTab = ref("all");
const showTemplatePicker = ref(false);
const showUserMenu = ref(false);
const avatarRef = ref(null);

const fullName = computed(
	() => window.frappe?.boot?.user_info?.full_name || window.frappe?.session?.user || ""
);
const sessionUser = computed(() => window.frappe?.session?.user || "");
const userImage = computed(() => window.frappe?.boot?.user_info?.user_image || null);
const userInitials = computed(() => {
	const name = fullName.value;
	if (!name) return "?";
	const parts = name.trim().split(" ");
	return parts.length >= 2
		? (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
		: name[0].toUpperCase();
});

const tabs = [
	{ value: "all", label: "All" },
	{ value: "Draft", label: "Draft" },
	{ value: "Published", label: "Published" },
	{ value: "Closed", label: "Closed" },
];

const filteredSurveys = computed(() => {
	let list = surveys.value;
	if (activeTab.value !== "all") {
		list = list.filter((s) => s.status === activeTab.value);
	}
	if (search.value.trim()) {
		const q = search.value.toLowerCase();
		list = list.filter((s) => s.survey_title?.toLowerCase().includes(q));
	}
	return list;
});

async function logout() {
	await fetch("/api/method/logout", {
		method: "POST",
		headers: { "X-Frappe-CSRF-Token": window.csrf_token || "" },
	});
	window.location.href = "/login";
}

function onClickOutside(e) {
	if (avatarRef.value && !avatarRef.value.contains(e.target)) {
		showUserMenu.value = false;
	}
}

onMounted(() => {
	loadSurveys();
	document.addEventListener("click", onClickOutside);
});
onUnmounted(() => document.removeEventListener("click", onClickOutside));

async function loadSurveys() {
	loading.value = true;
	try {
		const result = await surveyAPI.list();
		surveys.value = result || [];
	} catch {
		surveys.value = [];
	} finally {
		loading.value = false;
	}
}

function createNew() {
	showTemplatePicker.value = true;
}

function onTemplateSelected(templateData) {
	showTemplatePicker.value = false;
	surveyStore.reset();
	if (templateData) {
		surveyStore.loadSurvey(templateData);
	}
	router.push("/forms/new");
}

function editSurvey(s) {
	router.push(`/forms/edit/${s.name}`);
}

async function deleteSurvey(s) {
	if (!confirm(`Delete "${s.survey_title}"? This cannot be undone.`)) return;
	await surveyAPI.delete(s.name);
	surveys.value = surveys.value.filter((x) => x.name !== s.name);
}

async function duplicateSurvey(s) {
	const result = await surveyAPI.duplicate(s.name);
	await loadSurveys();
	router.push(`/forms/edit/${result.name}`);
}

function viewResponses(s) {
	router.push({ path: `/forms/analytics/${s.name}`, query: { tab: "responses" } });
}

function viewAnalytics(s) {
	router.push(`/forms/analytics/${s.name}`);
}

async function toggleStatus(s) {
	if (s.status === "Draft") {
		await surveyAPI.publish(s.name);
		s.status = "Published";
	} else if (s.status === "Published") {
		await surveyAPI.unpublish(s.name);
		s.status = "Draft";
	}
}
</script>
