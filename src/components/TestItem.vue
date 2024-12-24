<script setup>
defineProps({
	input: {
		type: String,
		required: true,
	},
});
</script>

<template>
	<div class="flex justify-center font-serif font-light text-5xl text-white">
		<h1 class="bg-black italic w-screen text-center">
			{{ input }}
		</h1>
	</div>
</template>
