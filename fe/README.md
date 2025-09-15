# Frontend: Code Challenge Poll (SvelteKit)

Simple SvelteKit app for creating questions, adding answers, and viewing visitor stats. It talks to the FastAPI backend via a configurable base URL.

## Prerequisites
- Node.js LTS (use `nvm` for convenience)
- npm 9+

```bash
nvm use   # uses the version from .nvmrc
```

## Getting Started
Install dependencies and start the dev server:

```bash
npm install
npm run dev
```

Open with a new browser tab automatically:

```bash
npm run dev -- --open
```

By default the app runs on `http://localhost:5173` and expects the backend at `http://localhost:8000`.

## Configuration
The backend base URL is configured via a public env var:

- `PUBLIC_API_BASE_URL` — base URL of the API (default `http://localhost:8000`).

Create a `.env` file in `fe/` (or use `.env.local`) based on `.env.example`:

```env
PUBLIC_API_BASE_URL=http://localhost:8000
```

Environment variables prefixed with `PUBLIC_` are embedded at build time (see `src/lib/config.ts`).

## Scripts
- `npm run dev`: Start Vite dev server
- `npm run build`: Build the app
- `npm run preview`: Preview the production build locally
- `npm run check`: Type-check with `svelte-check`
- `npm run lint`: Lint with ESLint + Prettier (no fixes)
- `npm run format`: Format with Prettier (writes changes)
- `npm test` or `npm run test:unit`: Run unit tests with Vitest

## Testing
Vitest is configured for both browser and node environments.

```bash
npm test          # run tests once
npm run test:unit # start Vitest (watch mode by default)
```

## Linting and Formatting

```bash
npm run lint    # check
npm run format  # write fixes
```

## Backend Integration
Make sure the backend is running and reachable at `PUBLIC_API_BASE_URL`. Default backend URL is `http://localhost:8000` and CORS must allow the frontend origin.
