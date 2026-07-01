<template>
  <div>
    <textarea
      v-if="isLong"
      readonly
      :placeholder="question.placeholder || 'Long answer text…'"
      rows="3"
      class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm resize-none bg-gray-50 text-gray-400 cursor-default"
    />
    <input
      v-else
      readonly
      :type="inputType"
      :placeholder="question.placeholder || placeholder"
      class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm bg-gray-50 text-gray-400 cursor-default"
    />
  </div>
</template>

<script setup>
import { computed } from "vue";
const props = defineProps({ question: Object });
const isLong = computed(() => ["Long Answer", "Paragraph"].includes(props.question?.question_type));
const inputType = computed(() => {
  const m = { Email: "email", Phone: "tel", URL: "url", Number: "number" };
  return m[props.question?.question_type] || "text";
});
const placeholder = computed(() => {
  const m = { Email: "email@example.com", Phone: "+1 555 000 0000", URL: "https://", Number: "0" };
  return m[props.question?.question_type] || "Short answer text…";
});
</script>
