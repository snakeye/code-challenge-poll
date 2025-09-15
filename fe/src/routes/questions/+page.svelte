<script lang="ts">
	import { onMount } from 'svelte';
	import { API_BASE } from '$lib/config';
	let questions: Question[] = [];
	let loading = true;
	let error = '';
	let text = '';
	let message = '';

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		message = '';
		try {
			const response = await fetch(`${API_BASE}/v1/questions`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ text })
			});
			if (response.ok) {
				message = 'Question submitted successfully!';
				text = '';
				fetchQuestions();
			} else {
				message = 'Failed to submit question.';
			}
		} catch (error) {
			message = 'Error submitting question.';
		}
	}

	async function fetchQuestions() {
		loading = true;
		error = '';
		try {
			const res = await fetch(`${API_BASE}/v1/questions`);
			if (res.ok) {
				const questions_response: Questions = await res.json();
				questions = questions_response.results;
			} else {
				error = 'Failed to load questions.';
			}
		} catch (e) {
			error = 'Error loading questions.';
			console.error(e);
		} finally {
			loading = false;
		}
	}

	onMount(fetchQuestions);
</script>

<form on:submit|preventDefault={handleSubmit}>
	<label for="question">Question:</label>
	<input id="question" type="text" bind:value={text} required />
	<button type="submit">Submit</button>
</form>

{#if message}
	<p>{message}</p>
{/if}

{#if loading}
	<p class="message --info">Loading questions...</p>
{:else if error}
	<p class="message --error">{error}</p>
{:else}
	<h2>All Questions</h2>

	<ul class="questions-list">
		{#each questions as question}
			<li>
				{question.text}
				<a href="/questions/{question.id}">Show Answers</a>
			</li>
		{/each}
	</ul>
{/if}
