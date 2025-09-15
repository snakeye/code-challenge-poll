interface Question {
	id: number;
	text: string;
}

interface Questions {
	count: number;
	results: Question[];
}

interface Answer {
	id: number;
	text: string;
}

interface Answers {
	count: number;
	results: Answer[];
}

interface Stats {
	visits: number;
}
