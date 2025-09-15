<script lang="ts">
	import { onMount } from 'svelte';
	import { API_BASE } from '$lib/config';
	import { page } from '$app/stores';
	import { get } from 'svelte/store';
	import { browser } from '$app/environment';
	const question_id = get(page).params.id;
	let question: Question | null = null;
	let stats: Stats | null = null;
	let loading = true;
	let error = '';

	async function fetchQuestionStats() {
		loading = true;
		error = '';
		try {
			const res_q = await fetch(`${API_BASE}/v1/questions/${question_id}`);
			if (res_q.ok) {
				question = await res_q.json();
			}

			const res = await fetch(`${API_BASE}/v1/questions/${question_id}/stats`);
			if (res.ok) {
				stats = await res.json();
			} else {
				error = 'Failed to load visitor stats.';
			}
		} catch (e) {
			error = 'Error loading visitor stats.';
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		fetchQuestionStats();
	});
</script>

{#if loading}
	<p class="message --info">Loading...</p>
{:else if error}
	<p class="message --error">{error}</p>
{:else if stats}
	{#if question}
		<h2>Question</h2>
		<p>
			{question.text}
		</p>
	{/if}

	<p>
		Visited {stats.visits} times
	</p>

	<a href="/questions/{question_id}">Back to question</a>
{/if}
