<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div class="max-w-6xl mx-auto px-6 h-14 flex items-center gap-4">
        <button @click="router.push('/forms')" class="p-1.5 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
        </button>
        <h1 class="font-semibold text-gray-900 truncate">{{ survey?.survey_title || "Analytics" }}</h1>
        <div class="ml-auto flex items-center gap-2">
          <button
            v-for="tab in tabs"
            :key="tab"
            @click="activeTab = tab"
            class="text-sm px-3 py-1.5 rounded-lg transition-colors font-medium"
            :class="activeTab === tab ? 'bg-blue-50 text-blue-600' : 'text-gray-500 hover:text-gray-700'"
          >{{ tab }}</button>
        </div>
      </div>
    </header>

    <main class="max-w-6xl mx-auto px-6 py-8">
      <!-- Loading -->
      <div v-if="loading" class="flex items-center justify-center py-24">
        <div class="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
      </div>

      <!-- Summary tab -->
      <div v-else-if="activeTab === 'Summary'">
        <!-- Stats row -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div v-for="stat in stats" :key="stat.label" class="bg-white rounded-xl border border-gray-200 p-5">
            <p class="text-xs text-gray-400 font-medium">{{ stat.label }}</p>
            <p class="text-2xl font-bold text-gray-900 mt-1">{{ stat.value }}</p>
          </div>
        </div>

        <!-- Daily responses chart -->
        <div class="bg-white rounded-xl border border-gray-200 p-6 mb-6">
          <h3 class="text-sm font-semibold text-gray-700 mb-4">Responses Over Time</h3>
          <div class="h-48 flex items-end gap-1.5">
            <div
              v-for="(d, i) in analytics?.daily_responses || []"
              :key="i"
              class="flex-1 bg-blue-500 rounded-t-sm hover:bg-blue-600 transition-colors cursor-default relative group"
              :style="{ height: `${(d.count / maxDaily) * 100}%`, minHeight: '4px' }"
            >
              <div class="absolute -top-8 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                {{ d.day }}: {{ d.count }}
              </div>
            </div>
          </div>
          <div v-if="!analytics?.daily_responses?.length" class="h-48 flex items-center justify-center text-gray-400 text-sm">
            No response data yet
          </div>
        </div>

        <!-- Share box -->
        <div class="bg-white rounded-xl border border-gray-200 p-6">
          <h3 class="text-sm font-semibold text-gray-700 mb-4">Share this Form</h3>
          <div class="flex items-center gap-3">
            <input
              :value="shareUrl"
              readonly
              class="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-600 bg-gray-50 focus:outline-none"
            />
            <button @click="copyUrl" class="bg-blue-600 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
              {{ copied ? "Copied!" : "Copy Link" }}
            </button>
          </div>
        </div>
      </div>

      <!-- Questions tab -->
      <div v-else-if="activeTab === 'Questions'">
        <div
          v-for="q in analytics?.question_stats || []"
          :key="q.question"
          class="bg-white rounded-xl border border-gray-200 p-6 mb-4"
        >
          <h3 class="text-sm font-semibold text-gray-900 mb-1">{{ q.question }}</h3>
          <p class="text-xs text-gray-400 mb-4">{{ q.question_type }} · {{ q.total_answers }} responses</p>

          <!-- Distribution bars -->
          <div v-if="q.distribution" class="space-y-2">
            <div
              v-for="(count, option) in q.distribution"
              :key="option"
              class="flex items-center gap-3"
            >
              <span class="text-sm text-gray-600 w-32 truncate flex-shrink-0">{{ option }}</span>
              <div class="flex-1 bg-gray-100 rounded-full h-3 overflow-hidden">
                <div
                  class="h-3 bg-blue-500 rounded-full transition-all"
                  :style="{ width: `${(count / q.total_answers * 100).toFixed(1)}%` }"
                />
              </div>
              <span class="text-xs text-gray-400 w-12 text-right flex-shrink-0">{{ count }}</span>
            </div>
          </div>

          <!-- Average -->
          <div v-if="q.average" class="flex items-center gap-3">
            <div class="text-3xl font-bold text-blue-600">{{ q.average }}</div>
            <div class="text-sm text-gray-400">avg. rating</div>
          </div>

          <!-- NPS -->
          <div v-if="q.nps !== undefined" class="flex items-center gap-3">
            <div class="text-3xl font-bold" :class="q.nps >= 50 ? 'text-green-600' : q.nps >= 0 ? 'text-yellow-600' : 'text-red-600'">
              {{ q.nps > 0 ? "+" : "" }}{{ q.nps }}
            </div>
            <div class="text-sm text-gray-400">NPS Score</div>
          </div>
        </div>

        <div v-if="!analytics?.question_stats?.length" class="text-center py-12 text-gray-400">
          No completed responses yet
        </div>
      </div>

      <!-- Responses tab -->
      <div v-else-if="activeTab === 'Responses'">
        <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
            <span class="text-sm font-medium text-gray-700">{{ responses.length }} response(s)</span>
            <button @click="exportResponses" class="text-sm text-blue-600 hover:text-blue-700">
              Export CSV
            </button>
          </div>
          <div v-if="!responses.length" class="text-center py-12 text-gray-400 text-sm">
            No responses yet
          </div>
          <table v-else class="w-full text-sm">
            <thead class="bg-gray-50 text-xs text-gray-500 uppercase">
              <tr>
                <th class="px-6 py-3 text-left">Respondent</th>
                <th class="px-6 py-3 text-left">Status</th>
                <th class="px-6 py-3 text-left">Submitted</th>
                <th class="px-6 py-3 text-left">Duration</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr
                v-for="r in responses"
                :key="r.name"
                class="hover:bg-gray-50 transition-colors"
              >
                <td class="px-6 py-4 text-gray-900">{{ r.respondent_name || r.email || "Anonymous" }}</td>
                <td class="px-6 py-4">
                  <span
                    class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                    :class="r.completion_status === 'Completed' ? 'bg-green-50 text-green-700' : 'bg-yellow-50 text-yellow-700'"
                  >{{ r.completion_status }}</span>
                </td>
                <td class="px-6 py-4 text-gray-500">{{ formatDate(r.submitted_on) }}</td>
                <td class="px-6 py-4 text-gray-500">{{ formatDuration(r.duration) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { surveyAPI, analyticsAPI, responseAPI } from "@/utils/api";

const route = useRoute();
const router = useRouter();
const survey = ref(null);
const analytics = ref(null);
const responses = ref([]);
const loading = ref(true);
const copied = ref(false);
const activeTab = ref(route.query.tab === "responses" ? "Responses" : "Summary");
const tabs = ["Summary", "Questions", "Responses"];

const stats = computed(() => [
  { label: "Total Responses", value: analytics.value?.total_responses || 0 },
  { label: "Completed", value: analytics.value?.completed_responses || 0 },
  { label: "Completion Rate", value: `${analytics.value?.completion_rate || 0}%` },
  { label: "Avg. Duration", value: formatDuration(analytics.value?.average_duration) },
]);

const maxDaily = computed(() => {
  const data = analytics.value?.daily_responses || [];
  return Math.max(...data.map((d) => d.count), 1);
});

const shareUrl = computed(() =>
  survey.value ? `${window.location.origin}/survey/${survey.value.survey_code}` : ""
);

async function copyUrl() {
  await navigator.clipboard.writeText(shareUrl.value);
  copied.value = true;
  setTimeout(() => (copied.value = false), 2000);
}

async function exportResponses() {
  const url = await responseAPI.export(route.params.name);
  window.open(url, "_blank");
}

function formatDate(d) {
  if (!d) return "—";
  return new Date(d).toLocaleString("en", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
}

function formatDuration(s) {
  if (!s) return "—";
  const m = Math.floor(s / 60);
  const sec = s % 60;
  return m > 0 ? `${m}m ${sec}s` : `${sec}s`;
}

onMounted(async () => {
  const name = route.params.name;
  try {
    const [s, a, r] = await Promise.all([
      surveyAPI.get(name),
      analyticsAPI.get(name),
      responseAPI.list(name),
    ]);
    survey.value = s;
    analytics.value = a;
    responses.value = r || [];
  } finally {
    loading.value = false;
  }
});
</script>
