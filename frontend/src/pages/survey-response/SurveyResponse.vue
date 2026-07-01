<template>
  <div class="min-h-screen" :style="bgStyle">
    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center min-h-screen">
      <div class="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
    </div>

    <!-- Error -->
    <div v-else-if="error" class="flex items-center justify-center min-h-screen p-4">
      <div class="bg-white rounded-2xl shadow-xl p-8 max-w-md text-center">
        <div class="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
        </div>
        <h2 class="text-lg font-semibold text-gray-900 mb-2">{{ error }}</h2>
        <a href="/" class="text-sm text-blue-600 hover:underline">Return home</a>
      </div>
    </div>

    <!-- Thank you -->
    <div v-else-if="submitted" class="flex items-center justify-center min-h-screen p-4">
      <div class="bg-white rounded-2xl shadow-xl p-10 max-w-md text-center w-full">
        <div class="w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6" :style="{ background: theme.primary_color + '20' }">
          <svg class="w-10 h-10" :style="{ color: theme.primary_color }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
        </div>
        <div class="text-gray-800 text-base" v-html="survey.thank_you_message" />
      </div>
    </div>

    <!-- Survey form -->
    <div v-else class="max-w-2xl mx-auto py-10 px-4">
      <!-- Header card -->
      <div :style="cardStyle" class="mb-4 overflow-hidden shadow-sm">
        <div class="h-2" :style="{ background: theme.primary_color }" />
        <div class="p-8">
          <h1 class="text-2xl font-bold mb-2" :style="{ color: theme.text_color }">{{ survey.survey_title }}</h1>
          <p v-if="survey.description" class="text-sm opacity-70" :style="{ color: theme.text_color }" v-html="survey.description" />
        </div>
      </div>

      <!-- Progress bar -->
      <div v-if="survey.display_progress_bar" class="mb-4">
        <div class="flex justify-between text-xs text-gray-500 mb-1">
          <span>Page {{ currentPage }} of {{ totalPages }}</span>
          <span>{{ Math.round(currentPage / totalPages * 100) }}%</span>
        </div>
        <div class="h-1.5 bg-gray-200 rounded-full overflow-hidden">
          <div
            class="h-1.5 rounded-full transition-all duration-500"
            :style="{ width: `${currentPage / totalPages * 100}%`, background: theme.primary_color }"
          />
        </div>
      </div>

      <!-- Questions on current page -->
      <div class="space-y-4">
        <ResponseQuestion
          v-for="q in currentPageQuestions"
          :key="q.id"
          :question="q"
          :theme="theme"
          :answer="answers[q.id]"
          @answer="(val) => setAnswer(q.id, val)"
        />
      </div>

      <!-- Navigation -->
      <div class="flex items-center justify-between mt-6">
        <button
          v-if="currentPage > 1"
          @click="currentPage--"
          class="px-6 py-2.5 rounded-xl border-2 text-sm font-semibold transition-colors"
          :style="{ borderColor: theme.primary_color, color: theme.primary_color }"
        >← Back</button>
        <div v-else />

        <button
          v-if="currentPage < totalPages"
          @click="nextPage"
          class="px-6 py-2.5 rounded-xl text-sm font-semibold transition-colors"
          :style="{ background: theme.primary_color, color: '#fff' }"
        >Next →</button>
        <button
          v-else
          @click="submitSurvey"
          :disabled="submitting"
          class="px-6 py-2.5 rounded-xl text-sm font-semibold transition-opacity"
          :style="{ background: theme.primary_color, color: '#fff' }"
          :class="submitting ? 'opacity-60 cursor-not-allowed' : ''"
        >{{ submitting ? "Submitting…" : "Submit" }}</button>
      </div>

      <!-- Draft note -->
      <p v-if="lastSaved" class="text-center text-xs text-gray-400 mt-4">
        Draft saved {{ lastSaved }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRoute } from "vue-router";
import { responseAPI, surveyAPI } from "@/utils/api";
import ResponseQuestion from "@/components/questions/ResponseQuestion.vue";

const route = useRoute();
const loading = ref(true);
const error = ref(null);
const submitted = ref(false);
const submitting = ref(false);
const survey = ref(null);
const questions = ref([]);
const theme = ref({
  primary_color: "#4f46e5",
  background_color: "#f9fafb",
  card_color: "#ffffff",
  text_color: "#111827",
  border_radius: 12,
});
const answers = ref({});
const currentPage = ref(1);
const responseId = ref(null);
const lastSaved = ref(null);
let autoSaveInterval = null;

const bgStyle = computed(() => ({
  background: theme.value.background_color,
  fontFamily: theme.value.font_family || "Inter, sans-serif",
}));

const cardStyle = computed(() => ({
  background: theme.value.card_color,
  borderRadius: `${theme.value.border_radius}px`,
  border: "1px solid #e5e7eb",
}));

const pages = computed(() => {
  const map = {};
  for (const q of questions.value) {
    const p = q.page_number || 1;
    if (!map[p]) map[p] = [];
    map[p].push(q);
  }
  return map;
});

const totalPages = computed(() => Math.max(...Object.keys(pages.value).map(Number), 1));

const currentPageQuestions = computed(() => pages.value[currentPage.value] || []);

function setAnswer(id, val) {
  answers.value = { ...answers.value, [id]: val };
}

function nextPage() {
  const required = currentPageQuestions.value.filter((q) => q.required);
  for (const q of required) {
    const a = answers.value[q.id];
    if (!a && a !== 0) {
      alert(`"${q.question}" is required.`);
      return;
    }
  }
  currentPage.value++;
  window.scrollTo(0, 0);
}

function collectAnswers() {
  return questions.value.map((q) => ({
    question: q.question,
    question_type: q.question_type,
    answer: String(answers.value[q.id] ?? ""),
  }));
}

async function saveDraft() {
  if (!survey.value) return;
  const ans = collectAnswers();
  try {
    const result = await responseAPI.saveDraft(route.params.code, ans, responseId.value);
    if (result?.response_id) responseId.value = result.response_id;
    const now = new Date();
    lastSaved.value = now.toLocaleTimeString("en", { hour: "2-digit", minute: "2-digit" });
  } catch {}
}

async function submitSurvey() {
  const required = currentPageQuestions.value.filter((q) => q.required);
  for (const q of required) {
    const a = answers.value[q.id];
    if (!a && a !== 0) {
      alert(`"${q.question}" is required.`);
      return;
    }
  }
  submitting.value = true;
  try {
    const ans = collectAnswers();
    await responseAPI.submit(route.params.code, ans, {
      response_id: responseId.value,
    });
    if (autoSaveInterval) clearInterval(autoSaveInterval);
    submitted.value = true;
    if (survey.value.redirect_url) {
      setTimeout(() => { window.location.href = survey.value.redirect_url; }, 2500);
    }
  } finally {
    submitting.value = false;
  }
}

onMounted(async () => {
  try {
    const data = await surveyAPI.getByCode(route.params.code);
    survey.value = data.survey;
    questions.value = data.questions || [];
    if (data.theme) Object.assign(theme.value, data.theme);
    if (survey.value.shuffle_questions) {
      questions.value = [...questions.value].sort(() => Math.random() - 0.5);
    }
  } catch (e) {
    error.value = e?.exc_type === "PermissionError"
      ? "This survey requires login to access."
      : "Survey not found or unavailable.";
  } finally {
    loading.value = false;
  }

  autoSaveInterval = setInterval(saveDraft, 30000);
});

onUnmounted(() => {
  if (autoSaveInterval) clearInterval(autoSaveInterval);
});
</script>
