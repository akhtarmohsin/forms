<template>
  <div>
    <!-- Star Rating -->
    <div v-if="question.question_type === 'Star Rating'" class="flex items-center gap-1">
      <span v-for="i in 5" :key="i" class="text-2xl" :class="i <= 3 ? 'text-amber-400' : 'text-gray-200'">★</span>
    </div>

    <!-- Rating 1-5 -->
    <div v-else-if="question.question_type === 'Rating'" class="flex gap-2">
      <button
        v-for="i in 5" :key="i"
        class="w-9 h-9 rounded-lg border-2 text-sm font-semibold transition-colors"
        :class="i === 3 ? 'border-blue-500 bg-blue-50 text-blue-600' : 'border-gray-200 text-gray-500'"
      >{{ i }}</button>
    </div>

    <!-- NPS -->
    <div v-else-if="question.question_type === 'Net Promoter Score'" class="space-y-2">
      <div class="flex gap-1.5 flex-wrap">
        <button
          v-for="i in 11" :key="i"
          class="w-9 h-9 rounded-lg border-2 text-xs font-semibold transition-colors"
          :class="i - 1 === 8 ? 'border-blue-500 bg-blue-50 text-blue-600' : 'border-gray-200 text-gray-500'"
        >{{ i - 1 }}</button>
      </div>
      <div class="flex justify-between text-xs text-gray-400">
        <span>Not at all likely</span><span>Extremely likely</span>
      </div>
    </div>

    <!-- Slider -->
    <div v-else-if="question.question_type === 'Slider'" class="flex items-center gap-3">
      <span class="text-xs text-gray-400">{{ question.min_value ?? 1 }}</span>
      <input type="range" :min="question.min_value ?? 1" :max="question.max_value ?? 10" value="5" class="flex-1 accent-blue-600" readonly />
      <span class="text-xs text-gray-400">{{ question.max_value ?? 10 }}</span>
    </div>

    <!-- Linear Scale -->
    <div v-else class="flex gap-2">
      <button
        v-for="i in scaleCount" :key="i"
        class="min-w-[36px] h-9 px-2 rounded-lg border-2 text-xs font-semibold transition-colors"
        :class="i === Math.ceil(scaleCount/2) ? 'border-blue-500 bg-blue-50 text-blue-600' : 'border-gray-200 text-gray-500'"
      >{{ (question.min_value ?? 1) + i - 1 }}</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
const props = defineProps({ question: Object });
const scaleCount = computed(() => {
  const min = props.question?.min_value ?? 1;
  const max = props.question?.max_value ?? 5;
  return Math.min(max - min + 1, 10);
});
</script>
