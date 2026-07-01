<template>
  <div
    class="question-card cursor-pointer"
    :class="{ active }"
  >
    <!-- Question header -->
    <div class="flex items-start gap-3">
      <span class="drag-handle mt-1 select-none">⠿</span>
      <div class="flex-1 min-w-0">
        <!-- Question text -->
        <div class="flex items-start gap-2 mb-3">
          <input
            v-model="q.question"
            @click.stop
            @input="emit('update', { question: q.question })"
            class="flex-1 text-sm font-medium text-gray-900 border-none outline-none bg-transparent placeholder-gray-400"
            placeholder="Question"
          />
          <span v-if="q.required" class="text-red-500 text-sm font-semibold flex-shrink-0">*</span>
        </div>

        <!-- Input preview -->
        <component :is="previewComponent" :question="q" />
      </div>
    </div>

    <!-- Toolbar (visible when active) -->
    <div v-if="active" class="flex items-center justify-between mt-4 pt-3 border-t border-gray-100">
      <div class="flex items-center gap-1">
        <select
          :value="q.question_type"
          @change="emit('update', { question_type: $event.target.value })"
          @click.stop
          class="text-xs border border-gray-200 rounded-lg px-2 py-1.5 text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option v-for="qt in QUESTION_TYPES" :key="qt.value" :value="qt.value">{{ qt.label }}</option>
        </select>
      </div>
      <div class="flex items-center gap-1">
        <button
          @click.stop="emit('duplicate')"
          class="p-1.5 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors"
          title="Duplicate"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
          </svg>
        </button>
        <button
          @click.stop="emit('remove')"
          class="p-1.5 rounded-lg text-gray-400 hover:text-red-500 hover:bg-red-50 transition-colors"
          title="Delete"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
          </svg>
        </button>
        <label class="flex items-center gap-1.5 cursor-pointer select-none">
          <input
            type="checkbox"
            :checked="q.required"
            @change="emit('update', { required: $event.target.checked })"
            @click.stop
            class="rounded text-blue-600 focus:ring-blue-500"
          />
          <span class="text-xs text-gray-500">Required</span>
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive } from "vue";
import { QUESTION_TYPES } from "@/utils/questions";
import QuestionPreviewText from "@/components/questions/QuestionPreviewText.vue";
import QuestionPreviewChoice from "@/components/questions/QuestionPreviewChoice.vue";
import QuestionPreviewScale from "@/components/questions/QuestionPreviewScale.vue";
import QuestionPreviewDate from "@/components/questions/QuestionPreviewDate.vue";
import QuestionPreviewFile from "@/components/questions/QuestionPreviewFile.vue";

const props = defineProps({ question: Object, active: Boolean });
const emit = defineEmits(["update", "duplicate", "remove", "add-after", "click"]);

const q = computed(() => props.question);

const previewComponent = computed(() => {
  const type = props.question?.question_type;
  if (["Multiple Choice", "Checkbox", "Dropdown", "Yes/No", "True/False", "Ranking"].includes(type))
    return QuestionPreviewChoice;
  if (["Rating", "Star Rating", "Linear Scale", "Slider", "Net Promoter Score"].includes(type))
    return QuestionPreviewScale;
  if (["Date", "Time", "Date & Time"].includes(type))
    return QuestionPreviewDate;
  if (["File Upload", "Signature"].includes(type))
    return QuestionPreviewFile;
  return QuestionPreviewText;
});
</script>
