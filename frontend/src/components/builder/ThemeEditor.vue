<template>
  <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-sm space-y-6">
    <h2 class="text-base font-semibold text-gray-900">Theme</h2>

    <div class="grid grid-cols-2 gap-4">
      <div v-for="c in colors" :key="c.key">
        <label class="block text-xs font-medium text-gray-500 mb-1.5">{{ c.label }}</label>
        <div class="flex items-center gap-2">
          <input
            type="color"
            :value="store.survey.theme_config[c.key]"
            @input="update(c.key, $event.target.value)"
            class="w-8 h-8 rounded-lg border border-gray-200 cursor-pointer p-0.5"
          />
          <input
            :value="store.survey.theme_config[c.key]"
            @input="update(c.key, $event.target.value)"
            class="flex-1 text-xs border border-gray-200 rounded-lg px-2 py-1.5 font-mono focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
    </div>

    <div>
      <label class="block text-xs font-medium text-gray-500 mb-1.5">Font Family</label>
      <select
        :value="store.survey.theme_config.font_family"
        @change="update('font_family', $event.target.value)"
        class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option>Inter</option>
        <option>Georgia</option>
        <option>Roboto</option>
        <option>Montserrat</option>
        <option>Lato</option>
        <option>Open Sans</option>
      </select>
    </div>

    <div>
      <label class="block text-xs font-medium text-gray-500 mb-1.5">Border Radius: {{ store.survey.theme_config.border_radius }}px</label>
      <input
        type="range" min="0" max="24"
        :value="store.survey.theme_config.border_radius"
        @input="update('border_radius', Number($event.target.value))"
        class="w-full accent-blue-600"
      />
    </div>

    <!-- Preview -->
    <div class="border border-gray-200 rounded-xl p-4 bg-gray-50">
      <p class="text-xs text-gray-400 mb-3 font-medium">PREVIEW</p>
      <div :style="previewStyle" class="p-4 rounded-lg">
        <div :style="cardStyle" class="p-4 rounded-lg mb-3 shadow-sm">
          <p :style="{ color: store.survey.theme_config.text_color, fontSize: '14px', fontWeight: '600', marginBottom: '8px', fontFamily: store.survey.theme_config.font_family }">
            Sample Question
          </p>
          <input type="text" placeholder="Short answer text" readonly
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm bg-white text-gray-400 cursor-default" />
        </div>
        <button :style="btnStyle" class="px-4 py-2 rounded-lg text-sm font-medium">
          Next →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useSurveyStore } from "@/stores/survey";
const store = useSurveyStore();

const colors = [
  { key: "primary_color", label: "Primary Color" },
  { key: "background_color", label: "Background" },
  { key: "card_color", label: "Card Color" },
  { key: "text_color", label: "Text Color" },
  { key: "button_color", label: "Button Color" },
];

function update(key, val) {
  store.updateSurveyMeta({
    theme_config: { ...store.survey.theme_config, [key]: val },
  });
}

const previewStyle = computed(() => ({
  background: store.survey.theme_config.background_color,
  borderRadius: `${store.survey.theme_config.border_radius}px`,
  fontFamily: store.survey.theme_config.font_family,
}));
const cardStyle = computed(() => ({
  background: store.survey.theme_config.card_color,
  borderRadius: `${store.survey.theme_config.border_radius}px`,
}));
const btnStyle = computed(() => ({
  background: store.survey.theme_config.button_color,
  color: "#fff",
  borderRadius: `${store.survey.theme_config.border_radius}px`,
}));
</script>
