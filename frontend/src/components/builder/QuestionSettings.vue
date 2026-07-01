<template>
	<div class="p-4">
		<h3 class="text-sm font-semibold text-gray-700 mb-4">Question Settings</h3>

		<!-- Help text -->
		<div class="mb-4">
			<label class="block text-xs font-medium text-gray-500 mb-1"
				>Description / Help Text</label
			>
			<textarea
				:value="question.description"
				@input="$emit('update', { description: $event.target.value })"
				rows="2"
				class="w-full text-sm border border-gray-200 rounded-lg p-2.5 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
				placeholder="Add help text for respondents…"
			/>
		</div>

		<!-- Placeholder -->
		<div v-if="isTextType" class="mb-4">
			<label class="block text-xs font-medium text-gray-500 mb-1">Placeholder</label>
			<input
				:value="question.placeholder"
				@input="$emit('update', { placeholder: $event.target.value })"
				class="w-full text-sm border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
				placeholder="Placeholder text…"
			/>
		</div>

		<!-- Options editor -->
		<div v-if="hasOptions" class="mb-4">
			<label class="block text-xs font-medium text-gray-500 mb-1">Options</label>
			<div class="space-y-1.5">
				<div v-for="(opt, i) in localOptions" :key="i" class="flex items-center gap-2">
					<input
						v-model="localOptions[i]"
						@blur="saveOptions"
						class="flex-1 text-sm border border-gray-200 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
						:placeholder="`Option ${i + 1}`"
					/>
					<button
						@click="removeOption(i)"
						class="text-gray-300 hover:text-red-400 transition-colors flex-shrink-0"
					>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M6 18L18 6M6 6l12 12"
							/>
						</svg>
					</button>
				</div>
				<button
					@click="addOption"
					class="text-xs text-blue-600 hover:text-blue-700 flex items-center gap-1 mt-1"
				>
					<svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M12 4v16m8-8H4"
						/>
					</svg>
					Add option
				</button>
			</div>
			<label class="flex items-center gap-2 mt-3 cursor-pointer">
				<input
					type="checkbox"
					:checked="question.allow_other"
					@change="$emit('update', { allow_other: $event.target.checked })"
					class="rounded text-blue-600"
				/>
				<span class="text-xs text-gray-600">Allow "Other" option</span>
			</label>
		</div>

		<!-- Scale range -->
		<div v-if="isScale" class="mb-4 grid grid-cols-2 gap-3">
			<div>
				<label class="block text-xs font-medium text-gray-500 mb-1">Min Value</label>
				<input
					type="number"
					:value="question.min_value ?? 1"
					@input="$emit('update', { min_value: Number($event.target.value) })"
					class="w-full text-sm border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
				/>
			</div>
			<div>
				<label class="block text-xs font-medium text-gray-500 mb-1">Max Value</label>
				<input
					type="number"
					:value="question.max_value ?? 10"
					@input="$emit('update', { max_value: Number($event.target.value) })"
					class="w-full text-sm border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
				/>
			</div>
		</div>

		<!-- Text length limits -->
		<div v-if="isTextType" class="mb-4 grid grid-cols-2 gap-3">
			<div>
				<label class="block text-xs font-medium text-gray-500 mb-1">Min Length</label>
				<input
					type="number"
					:value="question.min_length ?? ''"
					@input="
						$emit('update', {
							min_length: $event.target.value ? Number($event.target.value) : null,
						})
					"
					class="w-full text-sm border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
					placeholder="–"
				/>
			</div>
			<div>
				<label class="block text-xs font-medium text-gray-500 mb-1">Max Length</label>
				<input
					type="number"
					:value="question.max_length ?? ''"
					@input="
						$emit('update', {
							max_length: $event.target.value ? Number($event.target.value) : null,
						})
					"
					class="w-full text-sm border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
					placeholder="–"
				/>
			</div>
		</div>

		<!-- Required toggle -->
		<label class="flex items-center gap-3 cursor-pointer mb-3">
			<div class="relative">
				<input
					type="checkbox"
					:checked="question.required"
					@change="$emit('update', { required: $event.target.checked })"
					class="sr-only peer"
				/>
				<div
					class="w-9 h-5 bg-gray-200 rounded-full peer peer-checked:bg-blue-600 transition-colors"
				/>
				<div
					class="absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow transition-transform peer-checked:translate-x-4"
				/>
			</div>
			<span class="text-sm text-gray-700">Required</span>
		</label>

		<!-- Conditional logic (simple) -->
		<div class="border-t border-gray-100 pt-4 mt-4">
			<label class="block text-xs font-medium text-gray-500 mb-2">Conditional Logic</label>
			<p class="text-xs text-gray-400">
				Advanced conditional logic can be configured after saving.
			</p>
		</div>
	</div>
</template>

<script setup>
import { ref, watch, computed } from "vue";
import { hasOptions as _hasOptions, isScaleType } from "@/utils/questions";

const props = defineProps({ question: Object });
const emit = defineEmits(["update"]);

const localOptions = ref([...(props.question?.options || [])]);

watch(
	() => props.question?.options,
	(v) => {
		localOptions.value = [...(v || [])];
	},
	{ deep: true }
);

const hasOptions = computed(() => _hasOptions(props.question?.question_type));
const isScale = computed(() => isScaleType(props.question?.question_type));
const isTextType = computed(() => {
	const t = props.question?.question_type;
	return [
		"Short Answer",
		"Long Answer",
		"Paragraph",
		"Number",
		"Email",
		"Phone",
		"URL",
	].includes(t);
});

function addOption() {
	localOptions.value.push(`Option ${localOptions.value.length + 1}`);
	saveOptions();
}

function removeOption(i) {
	localOptions.value.splice(i, 1);
	saveOptions();
}

function saveOptions() {
	emit("update", { options: [...localOptions.value] });
}
</script>
