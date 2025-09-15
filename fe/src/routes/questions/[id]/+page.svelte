<script lang="ts">
	import { onMount } from 'svelte';
	import { API_BASE } from '$lib/config';
	import { page } from '$app/stores';
	import { get } from 'svelte/store';
	import { browser } from '$app/environment';
	const question_id = get(page).params.id;
	let question: Question | null = null;
	let answers: Answer[];
	let loading = true;
	let error = '';
	let text = '';
	let message = '';

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		try {
			const response = await fetch(`${API_BASE}/v1/questions/${question_id}/answers`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ text })
			});

			if (response.ok) {
				message = 'Answer submitted successfully!';
				text = '';

				fetchAnswers();
			} else {
				message = 'Failed to submit answer.';
			}
		} catch (error) {
			message = 'Error submitting answer.';
		}
	}

	async function fetchAnswers() {
		loading = true;
		error = '';
		try {
			const res_q = await fetch(`${API_BASE}/v1/questions/${question_id}`);
			if (res_q.ok) {
				question = await res_q.json();
			}

			const res = await fetch(`${API_BASE}/v1/questions/${question_id}/answers`);
			if (res.ok) {
				const answers_response: Answers = await res.json();
				answers = answers_response.results;
			} else {
				error = 'Failed to load answers.';
			}
		} catch (e) {
			error = 'Error loading answers.';
			console.error(e);
		} finally {
			loading = false;
		}
	}

	async function logVisit() {
		if (!browser) return; // guard against SSR
		try {
			await fetch(`${API_BASE}/v1/events`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					object: 'question',
					id: question_id
				})
			});
		} catch (_) {
			// no-op: logging shouldn't break UX
		}
	}

	onMount(() => {
		fetchAnswers();
		logVisit();
	});
</script>

<form on:submit|preventDefault={handleSubmit}>
	<label for="answer">Answer:</label>
	<input id="answer" type="text" bind:value={text} required />
	<button type="submit">Submit</button>
</form>

{#if loading}
	<p class="message --info">Loading...</p>
{:else if error}
	<p class="message --error">{error}</p>
{:else}
	{#if question}
		<h2>Question</h2>
		<p>
			{question.text}
		</p>
	{/if}
	<h2>Answers</h2>
	<ul class="answers-list">
		{#each answers as answer}
			<li>{answer.text}</li>
		{/each}
	</ul>
	<a href="/questions/{question_id}/stats">Show Visitor Stats</a>
{/if}
