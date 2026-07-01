<template>
  <div :style="cardStyle" class="p-6 shadow-sm border border-gray-100">
    <!-- Question text -->
    <p class="font-semibold mb-1" :style="{ color: theme.text_color }">
      {{ question.question }}
      <span v-if="question.required" style="color:#ef4444"> *</span>
    </p>
    <p v-if="question.description" class="text-sm text-gray-400 mb-4">{{ question.description }}</p>

    <!-- Short/Long text -->
    <input
      v-if="['Short Answer','Email','Phone','URL'].includes(question.question_type)"
      :type="inputType"
      :value="answer"
      @input="$emit('answer', $event.target.value)"
      :placeholder="question.placeholder || ''"
      class="w-full border border-gray-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 transition-all"
      :style="focusStyle"
    />
    <input
      v-else-if="question.question_type === 'Number'"
      type="number"
      :value="answer"
      @input="$emit('answer', Number($event.target.value))"
      :min="question.min_value"
      :max="question.max_value"
      class="w-full border border-gray-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2"
    />
    <textarea
      v-else-if="['Long Answer','Paragraph'].includes(question.question_type)"
      :value="answer"
      @input="$emit('answer', $event.target.value)"
      :placeholder="question.placeholder || 'Your answer…'"
      rows="4"
      class="w-full border border-gray-200 rounded-lg px-3 py-2.5 text-sm resize-none focus:outline-none focus:ring-2"
    />
    <input
      v-else-if="['Date','Time','Date & Time'].includes(question.question_type)"
      :type="inputType"
      :value="answer"
      @input="$emit('answer', $event.target.value)"
      class="border border-gray-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2"
    />

    <!-- Choice -->
    <div v-else-if="['Multiple Choice','Yes/No','True/False'].includes(question.question_type)" class="space-y-2">
      <label
        v-for="opt in displayOptions"
        :key="opt"
        class="option-item cursor-pointer select-none"
        :class="{ selected: answer === opt }"
        @click="$emit('answer', opt)"
      >
        <div class="w-4 h-4 rounded-full border-2 flex items-center justify-center flex-shrink-0 transition-colors"
          :style="answer === opt ? { borderColor: theme.primary_color, background: theme.primary_color } : { borderColor: '#d1d5db' }">
          <div v-if="answer === opt" class="w-2 h-2 rounded-full bg-white" />
        </div>
        <span class="text-sm text-gray-700">{{ opt }}</span>
      </label>
      <label v-if="question.allow_other" class="option-item cursor-pointer" :class="{ selected: isOther }">
        <div class="w-4 h-4 rounded-full border-2 flex items-center justify-center flex-shrink-0"
          :style="isOther ? { borderColor: theme.primary_color, background: theme.primary_color } : { borderColor: '#d1d5db' }">
          <div v-if="isOther" class="w-2 h-2 rounded-full bg-white" />
        </div>
        <span class="text-sm text-gray-500 italic">Other:</span>
        <input
          type="text"
          v-model="otherText"
          @focus="$emit('answer', otherText || '')"
          @input="$emit('answer', $event.target.value)"
          class="border-b border-gray-300 text-sm focus:outline-none flex-1"
          placeholder="Please specify…"
        />
      </label>
    </div>

    <!-- Checkbox -->
    <div v-else-if="question.question_type === 'Checkbox'" class="space-y-2">
      <label
        v-for="opt in displayOptions"
        :key="opt"
        class="option-item cursor-pointer select-none"
        :class="{ selected: checkboxSelected(opt) }"
        @click="toggleCheckbox(opt)"
      >
        <div class="w-4 h-4 rounded border-2 flex items-center justify-center flex-shrink-0 transition-colors"
          :style="checkboxSelected(opt) ? { borderColor: theme.primary_color, background: theme.primary_color } : { borderColor: '#d1d5db' }">
          <svg v-if="checkboxSelected(opt)" class="w-2.5 h-2.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
          </svg>
        </div>
        <span class="text-sm text-gray-700">{{ opt }}</span>
      </label>
    </div>

    <!-- Dropdown -->
    <select
      v-else-if="question.question_type === 'Dropdown'"
      :value="answer"
      @change="$emit('answer', $event.target.value)"
      class="w-full border border-gray-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2"
    >
      <option value="">Select an option…</option>
      <option v-for="opt in displayOptions" :key="opt" :value="opt">{{ opt }}</option>
    </select>

    <!-- Star Rating -->
    <div v-else-if="question.question_type === 'Star Rating'" class="flex items-center gap-2">
      <button
        v-for="i in 5" :key="i"
        @click="$emit('answer', i)"
        class="text-3xl transition-colors"
        :style="{ color: (answer || 0) >= i ? '#f59e0b' : '#e5e7eb' }"
      >★</button>
      <span v-if="answer" class="text-sm text-gray-400 ml-2">{{ answer }}/5</span>
    </div>

    <!-- Rating 1-5 -->
    <div v-else-if="question.question_type === 'Rating'" class="flex gap-2">
      <button
        v-for="i in 5" :key="i"
        @click="$emit('answer', i)"
        class="w-10 h-10 rounded-xl border-2 font-semibold text-sm transition-all"
        :style="answer === i ? { borderColor: theme.primary_color, background: theme.primary_color, color: '#fff' } : { borderColor: '#e5e7eb', color: '#6b7280' }"
      >{{ i }}</button>
    </div>

    <!-- NPS -->
    <div v-else-if="question.question_type === 'Net Promoter Score'" class="space-y-2">
      <div class="flex gap-2 flex-wrap">
        <button
          v-for="i in 11" :key="i"
          @click="$emit('answer', i - 1)"
          class="w-10 h-10 rounded-xl border-2 font-semibold text-sm transition-all"
          :style="answer === (i-1) ? { borderColor: theme.primary_color, background: theme.primary_color, color: '#fff' } : { borderColor: '#e5e7eb', color: '#6b7280' }"
        >{{ i - 1 }}</button>
      </div>
      <div class="flex justify-between text-xs text-gray-400">
        <span>Not at all likely</span><span>Extremely likely</span>
      </div>
    </div>

    <!-- Linear Scale -->
    <div v-else-if="question.question_type === 'Linear Scale'" class="flex gap-2 flex-wrap">
      <button
        v-for="i in scaleCount" :key="i"
        @click="$emit('answer', scaleMin + i - 1)"
        class="min-w-[40px] h-10 px-2 rounded-xl border-2 font-semibold text-sm transition-all"
        :style="answer === (scaleMin + i - 1) ? { borderColor: theme.primary_color, background: theme.primary_color, color: '#fff' } : { borderColor: '#e5e7eb', color: '#6b7280' }"
      >{{ scaleMin + i - 1 }}</button>
    </div>

    <!-- Slider -->
    <div v-else-if="question.question_type === 'Slider'" class="flex items-center gap-4">
      <span class="text-sm text-gray-400">{{ scaleMin }}</span>
      <input
        type="range"
        :min="scaleMin"
        :max="scaleMax"
        :value="answer ?? scaleMin"
        @input="$emit('answer', Number($event.target.value))"
        class="flex-1"
        :style="{ accentColor: theme.primary_color }"
      />
      <span class="text-sm text-gray-400">{{ scaleMax }}</span>
      <span class="text-sm font-bold w-8 text-center" :style="{ color: theme.primary_color }">{{ answer ?? scaleMin }}</span>
    </div>

    <!-- File Upload -->
    <div v-else-if="question.question_type === 'File Upload'">
      <label class="border-2 border-dashed border-gray-200 rounded-xl p-6 flex flex-col items-center cursor-pointer hover:border-blue-300 hover:bg-blue-50 transition-colors">
        <svg class="w-8 h-8 text-gray-300 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
        </svg>
        <p class="text-sm text-gray-500">Click to upload</p>
        <input type="file" class="hidden" @change="handleFile" />
      </label>
      <p v-if="answer" class="text-xs text-green-600 mt-1">{{ answer }}</p>
    </div>

    <!-- Fallback -->
    <input
      v-else
      type="text"
      :value="answer"
      @input="$emit('answer', $event.target.value)"
      class="w-full border border-gray-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2"
    />
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const props = defineProps({
  question: Object,
  answer: [String, Number, Array],
  theme: Object,
});
const emit = defineEmits(["answer"]);

const otherText = ref("");
const isOther = computed(() => {
  const opts = displayOptions.value;
  return props.answer !== undefined && !opts.includes(props.answer) && props.answer !== "";
});

const cardStyle = computed(() => ({
  background: props.theme?.card_color || "#fff",
  borderRadius: `${props.theme?.border_radius || 12}px`,
}));
const focusStyle = computed(() => ({ "--tw-ring-color": props.theme?.primary_color }));

const inputType = computed(() => {
  const m = { Email: "email", Phone: "tel", URL: "url", Date: "date", Time: "time", "Date & Time": "datetime-local" };
  return m[props.question?.question_type] || "text";
});

const displayOptions = computed(() => {
  const t = props.question?.question_type;
  if (t === "Yes/No") return ["Yes", "No"];
  if (t === "True/False") return ["True", "False"];
  return props.question?.options || [];
});

const scaleMin = computed(() => props.question?.min_value ?? 1);
const scaleMax = computed(() => props.question?.max_value ?? 10);
const scaleCount = computed(() => Math.min(scaleMax.value - scaleMin.value + 1, 10));

function checkboxSelected(opt) {
  if (!props.answer) return false;
  const vals = Array.isArray(props.answer) ? props.answer : String(props.answer).split(",").map((s) => s.trim());
  return vals.includes(opt);
}

function toggleCheckbox(opt) {
  const current = Array.isArray(props.answer)
    ? [...props.answer]
    : props.answer ? String(props.answer).split(",").map((s) => s.trim()) : [];
  const idx = current.indexOf(opt);
  if (idx === -1) current.push(opt);
  else current.splice(idx, 1);
  emit("answer", current.join(", "));
}

function handleFile(e) {
  const file = e.target.files[0];
  if (file) emit("answer", file.name);
}
</script>
