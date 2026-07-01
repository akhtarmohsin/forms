<template>
  <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-sm space-y-6">
    <h2 class="text-base font-semibold text-gray-900">Form Settings</h2>

    <div class="grid grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1.5">Start Date</label>
        <input type="date" v-model="store.survey.start_date" @change="store.dirty = true"
          class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1.5">End Date</label>
        <input type="date" v-model="store.survey.end_date" @change="store.dirty = true"
          class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>
    </div>

    <div class="space-y-3">
      <label v-for="s in settings" :key="s.key" class="flex items-center justify-between">
        <div>
          <span class="text-sm font-medium text-gray-700">{{ s.label }}</span>
          <p class="text-xs text-gray-400">{{ s.desc }}</p>
        </div>
        <div class="relative flex-shrink-0 ml-4">
          <input type="checkbox" :checked="store.survey[s.key]"
            @change="store.updateSurveyMeta({ [s.key]: $event.target.checked })"
            class="sr-only peer" />
          <div class="w-9 h-5 bg-gray-200 rounded-full peer peer-checked:bg-blue-600 transition-colors cursor-pointer" />
          <div class="absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow transition-transform peer-checked:translate-x-4 pointer-events-none" />
        </div>
      </label>
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1.5">Thank You Message</label>
      <textarea
        v-model="store.survey.thank_you_message"
        @input="store.dirty = true"
        rows="3"
        class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1.5">Redirect URL after submission</label>
      <input
        v-model="store.survey.redirect_url"
        @input="store.dirty = true"
        type="url"
        placeholder="https://example.com"
        class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>
  </div>
</template>

<script setup>
import { useSurveyStore } from "@/stores/survey";
const store = useSurveyStore();

const settings = [
  { key: "allow_anonymous_responses", label: "Allow anonymous responses", desc: "Responses won't be linked to user accounts" },
  { key: "allow_multiple_responses", label: "Allow multiple responses", desc: "Same user can submit more than once" },
  { key: "require_login", label: "Require login", desc: "Only logged-in users can respond" },
  { key: "display_progress_bar", label: "Show progress bar", desc: "Display progress indicator at the top" },
  { key: "shuffle_questions", label: "Shuffle questions", desc: "Randomize question order for each respondent" },
];
</script>
