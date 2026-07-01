<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Top Nav -->
    <header class="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <span class="font-semibold text-gray-900 text-lg">Forms</span>
        </div>
        <div class="flex items-center gap-3">
          <span class="text-sm text-gray-500">{{ userDisplay }}</span>
          <button
            @click="createNew"
            class="inline-flex items-center gap-2 bg-blue-600 text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            New Form
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8">
      <!-- Filters & search -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center gap-3">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            @click="activeTab = tab.value"
            class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            :class="activeTab === tab.value
              ? 'bg-blue-50 text-blue-600'
              : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'"
          >
            {{ tab.label }}
          </button>
        </div>
        <div class="relative">
          <svg class="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0" />
          </svg>
          <input
            v-model="search"
            type="text"
            placeholder="Search forms…"
            class="pl-9 pr-4 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent w-56"
          />
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <div v-for="i in 8" :key="i" class="bg-white rounded-xl border border-gray-200 p-5 animate-pulse h-40" />
      </div>

      <!-- Empty state -->
      <div v-else-if="filteredSurveys.length === 0" class="flex flex-col items-center justify-center py-24 text-center">
        <div class="w-16 h-16 bg-blue-50 rounded-2xl flex items-center justify-center mb-4">
          <svg class="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-900 mb-2">No forms yet</h3>
        <p class="text-gray-500 mb-6 text-sm max-w-xs">Create your first form to start collecting responses from your audience.</p>
        <button @click="createNew" class="bg-blue-600 text-white text-sm font-medium px-5 py-2.5 rounded-lg hover:bg-blue-700 transition-colors">
          Create a form
        </button>
      </div>

      <!-- Survey grid -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
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
    </main>

    <!-- Template picker dialog -->
    <TemplatePickerDialog v-if="showTemplatePicker" @close="showTemplatePicker = false" @select="onTemplateSelected" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
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

const userDisplay = computed(() => {
  return window.frappe?.boot?.user_info?.full_name || window.frappe?.session?.user || "";
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

onMounted(loadSurveys);
</script>
