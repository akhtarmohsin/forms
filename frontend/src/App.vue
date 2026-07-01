<template>
	<router-view />
</template>

<script setup>
import { onMounted } from "vue";

onMounted(() => {
	// Ensure CSRF token is set for frappe-ui requests
	if (window.csrf_token && window.csrf_token !== "{{ csrf_token }}") {
		document.cookie = `X-Frappe-CSRF-Token=${window.csrf_token}`;
	}
});
</script>
