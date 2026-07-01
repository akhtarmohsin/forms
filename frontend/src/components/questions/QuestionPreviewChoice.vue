<template>
  <div class="space-y-1.5">
    <div
      v-if="question.question_type === 'Dropdown'"
      class="border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-400 bg-gray-50 flex items-center justify-between"
    >
      <span>Select an option</span>
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
      </svg>
    </div>
    <template v-else>
      <div
        v-for="(opt, i) in displayOptions"
        :key="i"
        class="option-item"
      >
        <div
          class="w-4 h-4 rounded-full border-2 border-gray-300 flex-shrink-0"
          :class="isCheckbox ? 'rounded' : 'rounded-full'"
        />
        <span class="text-sm text-gray-500">{{ opt }}</span>
      </div>
      <div v-if="question.allow_other" class="option-item">
        <div class="w-4 h-4 rounded-full border-2 border-gray-300 flex-shrink-0" />
        <span class="text-sm text-gray-400 italic">Other…</span>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed } from "vue";
const props = defineProps({ question: Object });
const isCheckbox = computed(() => props.question?.question_type === "Checkbox");
const displayOptions = computed(() => {
  const opts = props.question?.options || [];
  if (opts.length) return opts.slice(0, 5);
  if (["Yes/No"].includes(props.question?.question_type)) return ["Yes", "No"];
  if (["True/False"].includes(props.question?.question_type)) return ["True", "False"];
  return ["Option 1", "Option 2", "Option 3"];
});
</script>
