<template>
	<div class="border-2 border-dashed border-gray-200 rounded-lg p-6 text-center bg-gray-50">
		<svg
			class="w-8 h-8 text-gray-300 mx-auto mb-2"
			fill="none"
			stroke="currentColor"
			viewBox="0 0 24 24"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="1.5"
				d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
			/>
		</svg>
		<p class="text-sm text-gray-400">{{ label }}</p>
	</div>
</template>

<script setup>
import { computed } from "vue";
const props = defineProps({ question: Object });
const label = computed(() =>
	props.question?.question_type === "Signature" ? "Draw signature here" : "Click to upload file"
);
</script>
