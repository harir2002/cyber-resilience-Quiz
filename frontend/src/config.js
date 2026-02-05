// Basic configuration for API URL
// Vercel will set VITE_API_URL environment variable
// Local development falls back to localhost:8000

// Hardcoded fallback to Render URL for production if VITE_API_URL is missing
export const API_BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? '' : 'https://harir2002-cyber-quiz.hf.space');

