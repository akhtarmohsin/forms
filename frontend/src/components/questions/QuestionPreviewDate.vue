<template>
  <input
    readonly
    :type="inputType"
    class="border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-400 bg-gray-50 cursor-default"
    :class="isDateTime ? 'w-full' : 'w-40'"
  />
</template>

<script setup>
import { computed } from "vue";
const props = defineProps({ question: Object });
const isDateTime = computed(() => props.question?.question_type === "Date & Time");
const inputType = computed(() => {
  if (props.question?.question_type === "Time") return "time";
  if (props.question?.question_type === "Date & Time") return "datetime-local";
  return "date";
});
</script>
