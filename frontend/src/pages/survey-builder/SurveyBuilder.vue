<template>
  <div class="flex h-screen overflow-hidden bg-gray-50">
    <!-- Left: Question panel -->
    <aside class="builder-sidebar flex flex-col">
      <!-- Header -->
      <div class="p-4 border-b border-gray-100 flex items-center gap-2">
        <button @click="router.push('/forms')" class="p-1.5 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
        </button>
        <span class="text-sm font-medium text-gray-700 truncate flex-1">{{ store.survey.survey_title }}</span>
      </div>

      <!-- Question type picker -->
      <div class="p-3 border-b border-gray-100">
        <p class="text-xs font-medium text-gray-400 mb-2 px-1">Add question</p>
        <div class="space-y-1 max-h-56 overflow-y-auto">
          <div v-for="group in QUESTION_GROUPS" :key="group">
            <p class="text-xs text-gray-400 font-medium px-2 pt-2 pb-1">{{ group }}</p>
            <button
              v-for="qt in groupedTypes[group]"
              :key="qt.value"
              @click="store.addQuestion(qt.value)"
              class="w-full text-left flex items-center gap-2 px-2 py-1.5 rounded-lg text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-700 transition-colors"
            >
              <span class="text-xs">{{ qt.label }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Questions list -->
      <div class="flex-1 overflow-y-auto p-2" ref="sortableList">
        <div
          v-for="(q, i) in store.survey.questions"
          :key="q.id"
          @click="store.setActiveQuestion(q.id)"
          class="flex items-center gap-2 px-3 py-2.5 rounded-lg cursor-pointer mb-1 group transition-colors"
          :class="store.activeQuestionId === q.id ? 'bg-blue-50 text-blue-700' : 'hover:bg-gray-100 text-gray-700'"
        >
          <span class="drag-handle select-none text-gray-300 group-hover:text-gray-400 text-xs">⠿</span>
          <span class="text-xs text-gray-400 w-4 flex-shrink-0">{{ i + 1 }}</span>
          <span class="text-sm truncate flex-1">{{ q.question || "Untitled question" }}</span>
          <span v-if="q.required" class="text-red-400 text-xs">*</span>
        </div>
        <div v-if="!store.survey.questions.length" class="text-center text-gray-400 text-sm py-6">
          Add questions from above
        </div>
      </div>
    </aside>

    <!-- Center: Canvas -->
    <main class="flex-1 flex flex-col overflow-hidden">
      <!-- Toolbar -->
      <div class="bg-white border-b border-gray-200 px-6 h-14 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <button
            v-for="tab in ['Questions', 'Settings', 'Theme']"
            :key="tab"
            @click="activeTab = tab"
            class="text-sm font-medium px-3 py-1.5 rounded-lg transition-colors"
            :class="activeTab === tab ? 'bg-blue-50 text-blue-600' : 'text-gray-500 hover:text-gray-700'"
          >{{ tab }}</button>
        </div>

        <div class="flex items-center gap-3">
          <span v-if="store.dirty" class="text-xs text-gray-400">Unsaved changes</span>
          <button
            @click="saveAndClose"
            :disabled="store.saving"
            class="text-sm text-gray-600 border border-gray-200 px-3 py-1.5 rounded-lg hover:bg-gray-50 transition-colors"
          >{{ store.saving ? "Saving…" : "Save" }}</button>
          <a
            v-if="store.survey.name && store.survey.status === 'Published'"
            :href="`/survey/${store.survey.survey_code}`"
            target="_blank"
            class="text-sm text-gray-600 border border-gray-200 px-3 py-1.5 rounded-lg hover:bg-gray-50 transition-colors"
          >Preview ↗</a>
          <button
            @click="publishSurvey"
            class="text-sm font-medium px-4 py-1.5 rounded-lg transition-colors"
            :class="store.survey.status === 'Published'
              ? 'bg-green-50 text-green-700 border border-green-200 hover:bg-green-100'
              : 'bg-blue-600 text-white hover:bg-blue-700'"
          >
            {{ store.survey.status === "Published" ? "✓ Published" : "Publish" }}
          </button>
        </div>
      </div>

      <!-- Tab content -->
      <div class="flex-1 overflow-y-auto">
        <!-- Questions tab -->
        <div v-if="activeTab === 'Questions'" class="max-w-2xl mx-auto py-8 px-4">
          <!-- Form header card -->
          <div class="bg-white rounded-xl border border-gray-200 p-6 mb-4 shadow-sm">
            <input
              v-model="store.survey.survey_title"
              @input="store.dirty = true"
              class="w-full text-2xl font-bold text-gray-900 border-none outline-none bg-transparent placeholder-gray-300"
              placeholder="Form Title"
            />
            <input
              v-model="store.survey.description"
              @input="store.dirty = true"
              class="w-full text-sm text-gray-500 border-none outline-none bg-transparent mt-2 placeholder-gray-300"
              placeholder="Form description (optional)"
            />
          </div>

          <!-- Question cards -->
          <QuestionCard
            v-for="q in store.survey.questions"
            :key="q.id"
            :question="q"
            :active="store.activeQuestionId === q.id"
            @click="store.setActiveQuestion(q.id)"
            @update="(patch) => store.updateQuestion(q.id, patch)"
            @duplicate="store.duplicateQuestion(q.id)"
            @remove="store.removeQuestion(q.id)"
            @add-after="(type) => store.addQuestion(type, q.id)"
            class="mb-3"
          />

          <!-- Add question -->
          <button
            @click="store.addQuestion('Short Answer')"
            class="w-full border-2 border-dashed border-gray-200 rounded-xl py-4 text-sm text-gray-400 hover:border-blue-300 hover:text-blue-500 hover:bg-blue-50 transition-colors flex items-center justify-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Add question
          </button>
        </div>

        <!-- Settings tab -->
        <div v-if="activeTab === 'Settings'" class="max-w-2xl mx-auto py-8 px-4">
          <SurveySettings />
        </div>

        <!-- Theme tab -->
        <div v-if="activeTab === 'Theme'" class="max-w-2xl mx-auto py-8 px-4">
          <ThemeEditor />
        </div>
      </div>
    </main>

    <!-- Right: Question settings panel -->
    <aside v-if="store.activeQuestion && activeTab === 'Questions'" class="w-72 bg-white border-l border-gray-200 overflow-y-auto">
      <QuestionSettings
        :question="store.activeQuestion"
        @update="(patch) => store.updateQuestion(store.activeQuestionId, patch)"
      />
    </aside>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useSurveyStore } from "@/stores/survey";
import { surveyAPI } from "@/utils/api";
import { QUESTION_TYPES, QUESTION_GROUPS } from "@/utils/questions";
import QuestionCard from "@/components/builder/QuestionCard.vue";
import QuestionSettings from "@/components/builder/QuestionSettings.vue";
import SurveySettings from "@/components/builder/SurveySettings.vue";
import ThemeEditor from "@/components/builder/ThemeEditor.vue";

const route = useRoute();
const router = useRouter();
const store = useSurveyStore();
const activeTab = ref("Questions");

const groupedTypes = computed(() => {
  return QUESTION_TYPES.reduce((acc, qt) => {
    if (!acc[qt.group]) acc[qt.group] = [];
    acc[qt.group].push(qt);
    return acc;
  }, {});
});

onMounted(async () => {
  const name = route.params.name;
  if (name) {
    const data = await surveyAPI.get(name);
    store.loadSurvey(data);
  } else if (!store.survey.questions.length) {
    store.addQuestion("Short Answer");
  }
});

// Auto-save on route leave
watch(
  () => route.path,
  async (newPath, oldPath) => {
    if (store.dirty && store.survey.survey_title) {
      await store.save();
    }
  }
);

async function saveAndClose() {
  await store.save();
}

async function publishSurvey() {
  await store.save();
  if (store.survey.status === "Published") {
    await surveyAPI.unpublish(store.survey.name);
    store.survey.status = "Draft";
  } else {
    await surveyAPI.publish(store.survey.name);
    store.survey.status = "Published";
  }
}
</script>
